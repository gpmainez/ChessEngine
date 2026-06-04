import os
import pytest
from engine.Bridge import GameInterfaceBridge
from engine.Manager import GameManagerFactory, BasicGameManager, FisherChessGameManager
from engine.Board import FILE_DICT

def test_bridge_initialization_standard():
    manager = GameManagerFactory.create("standard")
    bridge = GameInterfaceBridge(manager)
    assert bridge.manager == manager
    assert bridge.get_fen() == "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    assert bridge.is_game_over() is False
    assert bridge.get_game_result() is None
    assert bridge.white_to_move is True

def test_bridge_initialization_fisher():
    manager = GameManagerFactory.create("fisher")
    bridge = GameInterfaceBridge(manager)
    assert bridge.manager == manager
    assert len(bridge.get_fen()) > 0
    assert bridge.is_game_over() is False
    assert bridge.get_game_result() is None
    assert bridge.white_to_move is True

def test_bridge_make_move():
    manager = GameManagerFactory.create("standard")
    bridge = GameInterfaceBridge(manager)
    # Move e2 -> e4
    success = bridge.make_move("e2", "e4")
    assert success is True
    assert bridge.get_fen().split(" ")[0].split("/")[4] == "4P3" # white pawn on e4
    assert bridge.white_to_move is False

def test_bridge_make_invalid_move():
    manager = GameManagerFactory.create("standard")
    bridge = GameInterfaceBridge(manager)
    # Invalid move e2 -> e5 (blocked/illegal)
    success = bridge.make_move("e2", "e5")
    assert success is False

def test_bridge_get_legal_moves():
    manager = GameManagerFactory.create("standard")
    bridge = GameInterfaceBridge(manager)
    moves = bridge.get_legal_moves("e2")
    assert "e3" in moves
    assert "e4" in moves
    assert "e5" not in moves

def test_bridge_make_ai_move():
    manager = GameManagerFactory.create("standard")
    bridge = GameInterfaceBridge(manager)
    # AI playing as Black (make a white move first, then AI moves)
    bridge.make_move("e2", "e4")
    ai_move = bridge.make_ai_move(1) # difficulty/depth 1
    assert ai_move is not None
    start, target = ai_move
    assert isinstance(start, str)
    assert isinstance(target, str)
    assert start in FILE_DICT
    assert target in FILE_DICT

def test_bridge_save_load_game(tmp_path):
    manager = GameManagerFactory.create("standard")
    bridge = GameInterfaceBridge(manager)
    
    # Make a move
    bridge.make_move("e2", "e4")
    original_fen = bridge.get_fen()
    
    # Save to temp path
    save_file = str(tmp_path / "test_savegame.fen")
    save_success = bridge.save_game(save_file)
    assert save_success is True
    
    # Load to a new bridge
    new_manager = GameManagerFactory.create("standard")
    new_bridge = GameInterfaceBridge(new_manager)
    
    load_success = new_bridge.load_game(save_file)
    assert load_success is True
    assert new_bridge.get_fen() == original_fen

def test_bridge_game_over_checkmate():
    # Setup a fool's mate position
    manager = GameManagerFactory.create("standard")
    bridge = GameInterfaceBridge(manager)
    bridge.make_move("f2", "f3")
    bridge.make_move("e7", "e5")
    bridge.make_move("g2", "g4")
    bridge.make_move("d8", "h4")
    
    assert bridge.is_game_over() is True
    assert bridge.get_game_result() == "CHECKMATE"

def test_bridge_get_piece():
    manager = GameManagerFactory.create("standard")
    bridge = GameInterfaceBridge(manager)
    assert bridge.get_piece("e2") == "wp"
    assert bridge.get_piece("e1") == "wk"
    assert bridge.get_piece("e7") == "bp"
    assert bridge.get_piece("e4") is None
