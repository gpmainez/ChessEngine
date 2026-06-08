import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from engine.Board import FILE_DICT, validate_fen
from engine.Manager import GameManagerFactory
from engine.Strategy import MinimaxAlphaBetaStrategy
from engine.Bridge import GameInterfaceBridge

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static")

#inicjalizacja - domyslnie szachy standardowe z ai medium
manager = GameManagerFactory.create("standard")
bridge = GameInterfaceBridge(manager)
ai_color = False
current_difficulty = 3



class MoveRequest(BaseModel):
    source: str
    target: str


class NewGameRequest(BaseModel):
    mode: str = "standard"
    player_color: str = "white"
    difficulty: int = 3


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/api/modes")
async def get_modes():
    #zwraca dostepne tryby gry
    return {"modes": GameManagerFactory.MODES}


@app.post("/api/new_game")
async def new_game(req: NewGameRequest):
    #   tworzy nowa gre z wybranym trybem przez fabryke
    global manager, bridge, ai_color, current_difficulty
    try:
        manager = GameManagerFactory.create(req.mode)
        bridge = GameInterfaceBridge(manager)
        current_difficulty = req.difficulty

        #ustalenie koloru gracza i ai
        import random as rand
        chosen = req.player_color
        if chosen == "random":
            chosen = rand.choice(["white", "black"])

        if chosen == "white":
            ai_color = False #ai czarne
        elif chosen == "black":
            ai_color = True  #ai biale
        else:
            ai_color = None  # PvP (both)

        #ruch ai jesli gra jako pierwsze (biale) i ai jest wlaczone
        if ai_color == True:
            bridge.make_ai_move(current_difficulty)

        return {"status": "success", "mode": req.mode, "player_color": chosen, "fen": bridge.get_fen()}
    except ValueError as e:
        return {"status": "error", "message": str(e)}


@app.post("/api/move")
async def make_move(move: MoveRequest):
    print(f"--- NOWY RUCH Z PRZEGLADARKI ---")
    print(f"Otrzymano tekstowo: z {move.source} na {move.target}")

    # Zachowanie spójności: rzucamy KeyError przy niepoprawnych współrzędnych
    if move.source not in FILE_DICT or move.target not in FILE_DICT:
        raise KeyError(f"Invalid coordinate: {move.source} or {move.target}")

    #sprobuj wykonac ruch gracza
    legal = bridge.make_move(move.source, move.target)
    if not legal:
        return {"status": "error"}

    #sprawdz stan po ruchu gracza
    if bridge.is_game_over():
        return {"status": "success", "fen": bridge.get_fen(), "game_over": bridge.get_game_result()}

    #wykonaj ruch ai
    if ai_color is not None and bridge.white_to_move == ai_color:
        bridge.make_ai_move(current_difficulty)

    state = bridge.get_game_result()
    return {
        "status": "success",
        "fen": bridge.get_fen(),
        "game_over": state
    }


@app.get("/api/save")
@app.post("/api/save")
async def api_save():
    #   save board state to file
    try:
        if bridge.save_game("savegame.fen"):
            return {"status": "success", "fen": bridge.get_fen()}
        else:
            return {"status": "error", "message": "could not save game"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.get("/api/load")
@app.post("/api/load")
async def api_load():
    #  load board state from file
    try:
        if not os.path.exists("savegame.fen"):
            return {"status": "error", "message": "savegame file not found"}
        
        success = bridge.load_game("savegame.fen")
        if not success:
            return {"status": "error", "message": "invalid fen string"}

        #   trigger ai move if needed
        if ai_color is not None and not bridge.is_game_over() and bridge.white_to_move == ai_color:
            bridge.make_ai_move(current_difficulty)

        state = bridge.get_game_result()
        return {
            "status": "success",
            "fen": bridge.get_fen(),
            "game_over": state,
            "player_color": "both" if ai_color is None else ("black" if ai_color else "white"),
            "difficulty": current_difficulty
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
