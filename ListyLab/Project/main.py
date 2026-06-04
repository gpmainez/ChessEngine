from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from engine.Board import FILE_DICT, validate_fen
from engine.Manager import GameManagerFactory
from engine.Strategy import MinimaxAlphaBetaStrategy

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static")

#inicjalizacja - domyslnie szachy standardowe z ai medium
manager = GameManagerFactory.create("standard")
manager.ai_strategy = MinimaxAlphaBetaStrategy(depth=3)
ai_color = False

#   slownik i funkcja tlumaczaca
def parse_move_to_index(square_str):
    return FILE_DICT[square_str]


class MoveRequest(BaseModel):
    source: str
    target: str


class NewGameRequest(BaseModel):
    mode: str = "standard"
    player_color: str = "white"


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
    global manager, ai_color
    try:
        manager = GameManagerFactory.create(req.mode)
        manager.ai_strategy = MinimaxAlphaBetaStrategy(depth=3)

        #ustalenie koloru gracza i ai
        import random as rand
        chosen = req.player_color
        if chosen == "random":
            chosen = rand.choice(["white", "black"])

        if chosen == "white":
            ai_color = False #ai czarne
        else:
            ai_color = True  #ai biale

        #ruch ai jesli gra jako pierwsze (biale)
        if ai_color == True:
            manager.make_ai_move()

        return {"status": "success", "mode": req.mode, "player_color": chosen, "fen": manager.board.generate_fen()}
    except ValueError as e:
        return {"status": "error", "message": str(e)}


@app.post("/api/move")
async def make_move(move: MoveRequest):
    print(f"--- NOWY RUCH Z PRZEGLADARKI ---")
    print(f"Otrzymano tekstowo: z {move.source} na {move.target}")

    start_pos = parse_move_to_index(move.source)
    target_pos = parse_move_to_index(move.target)

    print(f"Przetlumaczono na indeksy silnika: z {start_pos} na {target_pos}")
    print(f"--------------------------------")

    #sprobuj wykonac ruch gracza
    legal = manager.try_to_move(start_pos, target_pos)
    if not legal:
        return {"status": "error"}

    #sprawdz stan po ruchu gracza
    state = manager.check_game_state()
    if state != "CONTINUE":
        return {"status": "success", "fen": manager.board.generate_fen(), "game_over": state}

    #wykonaj ruch ai
    if manager.board.white_to_move == ai_color:
        manager.make_ai_move()

    state = manager.check_game_state()
    return {
        "status": "success",
        "fen": manager.board.generate_fen(),
        "game_over": state if state != "CONTINUE" else None
    }


@app.get("/api/save")
@app.post("/api/save")
async def api_save():
    #   save board state to file
    try:
        fen = manager.board.generate_fen()
        with open("savegame.fen", "w") as f:
            f.write(fen)
        return {"status": "success", "fen": fen}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.get("/api/load")
@app.post("/api/load")
async def api_load():
    #  load board state from file
    try:
        with open("savegame.fen", "r") as f:
            fen = f.read().strip()
        if not validate_fen(fen):
            return {"status": "error", "message": "invalid fen string"}

        manager.board.load_fen(fen)

        #   trigger ai move if needed
        state = manager.check_game_state()
        if state == "CONTINUE" and manager.board.white_to_move == ai_color:
            manager.make_ai_move()
            state = manager.check_game_state()

        return {
            "status": "success",
            "fen": manager.board.generate_fen(),
            "game_over": state if state != "CONTINUE" else None
        }
    except FileNotFoundError:
        return {"status": "error", "message": "savegame file not found"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
