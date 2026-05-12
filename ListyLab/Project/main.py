from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel


from engine import Board, generator

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static")

class MoveRequest(BaseModel):
    source: str
    target: str


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):

    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/move")
async def make_move(move: MoveRequest):
    print(f"Próba ruchu z {move.source} na {move.target}")

    # -----------------------------------------------------------------
    # Jeśli legalny -> game_board.make_move(...)
    # -----------------------------------------------------------------

    # Na razie ZASYMULUJEMY, że ruch się udał i zwracamy przykładowy FEN
    # (po ruchu e2-e4)
    dummy_new_fen = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1"

    return {"status": "success", "fen": dummy_new_fen}

#uvicorn main:app --reload