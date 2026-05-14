from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from frontUtlis import UserApi

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static")

# ---------------------------------------------------------
# 1. NASZ TŁUMACZ (Słownik i funkcja z Twojego pomysłu)
# ---------------------------------------------------------
FILE_DICT = {
    'a1': 0, 'b1': 1, 'c1': 2, 'd1': 3, 'e1': 4, 'f1': 5, 'g1': 6, 'h1': 7,
    'a2': 8, 'b2': 9, 'c2': 10, 'd2': 11, 'e2': 12, 'f2': 13, 'g2': 14, 'h2': 15,
    'a3': 16, 'b3': 17, 'c3': 18, 'd3': 19, 'e3': 20, 'f3': 21, 'g3': 22, 'h3': 23,
    'a4': 24, 'b4': 25, 'c4': 26, 'd4': 27, 'e4': 28, 'f4': 29, 'g4': 30, 'h4': 31,
    'a5': 32, 'b5': 33, 'c5': 34, 'd5': 35, 'e5': 36, 'f5': 37, 'g5': 38, 'h5': 39,
    'a6': 40, 'b6': 41, 'c6': 42, 'd6': 43, 'e6': 44, 'f6': 45, 'g6': 46, 'h6': 47,
    'a7': 48, 'b7': 49, 'c7': 50, 'd7': 51, 'e7': 52, 'f7': 53, 'g7': 54, 'h7': 55,
    'a8': 56, 'b8': 57, 'c8': 58, 'd8': 59, 'e8': 60, 'f8': 61, 'g8': 62, 'h8': 63
}


def parse_move_to_index(square_str):
    return FILE_DICT[square_str]


# ---------------------------------------------------------

class MoveRequest(BaseModel):
    source: str
    target: str
    user_api = UserApi()


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.post("/api/move")
async def make_move(move: MoveRequest):
    print(f"--- NOWY RUCH Z PRZEGLĄDARKI ---")
    print(f"Otrzymano tekstowo: z {move.source} na {move.target}")


    start_pos, target_pos = move.user_api.web_move_parser(move.source, move.target)



    print(f"Przetłumaczono na indeksy silnika: z {start_pos} na {target_pos}")
    print(f"--------------------------------")

    # Na razie wysyłamy do frontu błąd, zeby bierka "odbijała się"
    # z powrotem. W następnym kroku podepniemy tu Twój silnik!
    return {"status": "error"}