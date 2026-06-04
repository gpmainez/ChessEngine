import os
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def handle_savegame_backup():
    """Backup savegame.fen before test and restore it after."""
    backup_path = "savegame.fen.bak"
    original_exists = os.path.exists("savegame.fen")
    if original_exists:
        try:
            os.rename("savegame.fen", backup_path)
        except Exception:
            pass
    yield
    if os.path.exists("savegame.fen"):
        try:
            os.remove("savegame.fen")
        except Exception:
            pass
    if original_exists:
        try:
            os.rename(backup_path, "savegame.fen")
        except Exception:
            pass

# --- Tier 1: Feature Coverage ---

def test_get_modes():
    """Test GET /api/modes returns the supported game modes."""
    response = client.get("/api/modes")
    assert response.status_code == 200
    data = response.json()
    assert "modes" in data
    assert "standard" in data["modes"]
    assert "fisher" in data["modes"]

def test_new_game_standard():
    """Test POST /api/new_game standard mode initialization."""
    response = client.post("/api/new_game", json={"mode": "standard", "player_color": "white"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["mode"] == "standard"
    assert data["player_color"] == "white"
    assert "fen" in data
    assert data["fen"].startswith("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -")

def test_new_game_fisher():
    """Test POST /api/new_game fisher mode initialization."""
    response = client.post("/api/new_game", json={"mode": "fisher", "player_color": "white"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["mode"] == "fisher"
    assert data["player_color"] == "white"
    assert "fen" in data
    
    # Pawns are at rank 2 and 7, which should correspond to PPPP and pppp parts of FEN
    parts = data["fen"].split(" ")[0].split("/")
    assert parts[1] == "pppppppp"
    assert parts[6] == "PPPPPPPP"

def test_new_game_ai_first():
    """Test POST /api/new_game when player is black, which triggers AI to move first."""
    response = client.post("/api/new_game", json={"mode": "standard", "player_color": "black"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["mode"] == "standard"
    assert data["player_color"] == "black"
    assert "fen" in data
    # The turn in returned FEN should be 'b' because AI (White) moved first
    assert data["fen"].split(" ")[1] == "b"

def test_make_move_success():
    """Test POST /api/move for a valid player move followed by AI response."""
    # Start game as white (AI is black)
    client.post("/api/new_game", json={"mode": "standard", "player_color": "white"})
    
    # Move e2 to e4
    response = client.post("/api/move", json={"source": "e2", "target": "e4"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "fen" in data
    # Since AI is black, it should respond, and active turn returns to 'w'
    assert data["fen"].split(" ")[1] == "w"

def test_make_move_invalid_move():
    """Test POST /api/move for an illegal move."""
    client.post("/api/new_game", json={"mode": "standard", "player_color": "white"})
    
    # Illegal pawn move (e2 to e5)
    response = client.post("/api/move", json={"source": "e2", "target": "e5"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "error"

def test_save_game():
    """Test POST /api/save saves the game state to savegame.fen."""
    client.post("/api/new_game", json={"mode": "standard", "player_color": "white"})
    response = client.post("/api/save")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "fen" in data
    
    # Check that file was created and contents match
    assert os.path.exists("savegame.fen")
    with open("savegame.fen", "r") as f:
        file_content = f.read().strip()
    assert file_content == data["fen"]

def test_load_game():
    """Test POST /api/load loads the saved game state from savegame.fen."""
    client.post("/api/new_game", json={"mode": "standard", "player_color": "white"})
    # Make a move
    move_res = client.post("/api/move", json={"source": "e2", "target": "e4"})
    fen_after_move = move_res.json()["fen"]
    
    # Save the state
    client.post("/api/save")
    
    # Reset game
    client.post("/api/new_game", json={"mode": "standard", "player_color": "white"})
    
    # Load game
    load_res = client.post("/api/load")
    assert load_res.status_code == 200
    data = load_res.json()
    assert data["status"] == "success"
    assert data["fen"] == fen_after_move

# --- Tier 2: Boundary & Corner Cases ---

def test_invalid_new_game_mode():
    """Test POST /api/new_game with an invalid mode name."""
    response = client.post("/api/new_game", json={"mode": "invalid_mode", "player_color": "white"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "error"
    assert "message" in data

def test_invalid_move_formats():
    """Test POST /api/move with invalid square coordinates."""
    client.post("/api/new_game", json={"mode": "standard", "player_color": "white"})
    
    # TestClient raises KeyError when an unhandled KeyError is thrown by main.py
    with pytest.raises(KeyError):
        client.post("/api/move", json={"source": "e2", "target": "e9"})

def test_invalid_fen_on_load():
    """Test POST /api/load with an invalid FEN string in the save file."""
    # Write invalid FEN to savegame.fen
    with open("savegame.fen", "w") as f:
        f.write("invalid_fen_string_goes_here")
        
    response = client.post("/api/load")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "error"
    assert data["message"] == "invalid fen string"

def test_load_nonexistent_savegame():
    """Test POST /api/load when no savegame.fen file exists."""
    # Delete file if exists
    if os.path.exists("savegame.fen"):
        os.remove("savegame.fen")
        
    response = client.post("/api/load")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "error"
    assert data["message"] == "savegame file not found"

# --- Tier 3: Cross-Feature Combinations ---

def test_cross_feature_workflow():
    """Test a full loop: New Game -> Save -> Load -> Play Move."""
    # 1. New game
    new_res = client.post("/api/new_game", json={"mode": "standard", "player_color": "white"})
    assert new_res.json()["status"] == "success"
    initial_fen = new_res.json()["fen"]

    # 2. Save game
    save_res = client.post("/api/save")
    assert save_res.json()["status"] == "success"
    assert save_res.json()["fen"] == initial_fen

    # 3. Load game
    load_res = client.post("/api/load")
    assert load_res.json()["status"] == "success"
    assert load_res.json()["fen"] == initial_fen

    # 4. Play move
    move_res = client.post("/api/move", json={"source": "g1", "target": "f3"})
    assert move_res.json()["status"] == "success"
    assert move_res.json()["fen"] != initial_fen

# --- Tier 4: Real-world workload (Fool's Mate Checkmate) ---

def test_fools_mate_checkmate():
    """Test playing a sequence of moves resulting in Fool's Mate checkmate."""
    # Initialize game with player as black (AI is white)
    client.post("/api/new_game", json={"mode": "standard", "player_color": "black"})

    # Setup the board FEN right before the checkmate move
    # White has played f3 and g4, Black has played e5. It is Black's turn to move.
    before_mate_fen = "rnbqkbnr/pppp1ppp/8/4p3/6P1/5P2/PPPPP2P/RNBQKBNR b KQkq - 0 2"
    with open("savegame.fen", "w") as f:
        f.write(before_mate_fen)

    # Load the position
    load_res = client.post("/api/load")
    assert load_res.status_code == 200
    assert load_res.json()["status"] == "success"
    assert load_res.json()["fen"].startswith("rnbqkbnr/pppp1ppp/8/4p3/6P1/5P2/PPPPP2P/RNBQKBNR b")

    # Play the checkmate move: Queen d8 to h4 (d8 -> h4)
    move_res = client.post("/api/move", json={"source": "d8", "target": "h4"})
    assert move_res.status_code == 200
    data = move_res.json()
    assert data["status"] == "success"
    assert data["game_over"] == "CHECKMATE"
