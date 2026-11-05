# Chess – Python Bitboard Engine

Gra w szachy z silnikiem opartym na bitboardach (64-bit), interfejsem desktopowym Pygame oraz webowym FastAPI. Obsługuje Chess960 (Fischer Random Chess), AI z algorytmem Minimax + Alpha-Beta Pruning oraz zapis/odczyt stanu gry w formacie FEN.

---

## Architektura projektu

```
Project/
├── engine/
│   ├── Board.py       # bitboardy, make_move, undo_move, FEN
│   ├── Generator.py   # generowanie ruchów figur
│   ├── Manager.py     # logika gry, walidacja, roszady
│   ├── Strategy.py    # wzorzec Strategia dla AI
│   └── AI.py          # Minimax + Alpha-Beta, heurystyka PST
├── static/
│   ├── index.html     # interfejs webowy
│   ├── app.js         # klient JavaScript
│   └── style.css
├── images/            # grafiki figur (wp.png, bk.png, ...)
├── tests/
│   ├── test_board.py  # testy Board i FEN
│   ├── test_manager.py
│   └── test_ai.py
├── front.py           # interfejs Pygame (desktopowy)
├── main.py            # serwer FastAPI (webowy)
├── requirements.txt
├── Dockerfile         # wdrożenie wersji webowej
└── chess.spec         # konfiguracja PyInstaller (exe)
```

---

## Zależności

```bash
pip install -r requirements.txt
```

Plik `requirements.txt`:
```
fastapi
uvicorn[standard]
pygame (pygame-ce dla pythona 13)
```

---

## Uruchomienie

### Wersja desktopowa (Pygame)

```bash
python front.py
```

**Sterowanie:**
| Klawisz / Akcja | Opis |
|---|---|
| Klik LPM na figurę | zaznaczenie / wybór ruchu |
| Klik PPM | odznaczenie |
| `S` | zapis stanu gry do `savegame.fen` |
| `L` | wczytanie gry z `savegame.fen` |
| `D` | menu wyboru poziomu trudności AI |

**Poziomy trudności AI:**
| Poziom | Nazwa | Strategia |
|---|---|---|
| 0 | Extra Easy | losowe ruchy |
| 1 | Easy | Minimax depth 1 |
| 2 | Medium | Minimax depth 3 |
| 3 | Hard | Minimax depth 5 |

---

### Wersja webowa (FastAPI)

```bash
uvicorn main:app --reload
```

Otwórz przeglądarkę: [http://localhost:8000](http://localhost:8000)

**Endpointy API:**
| Metoda | Ścieżka | Opis |
|---|---|---|
| `POST` | `/api/move` | ruch gracza `{"source": "e2", "target": "e4"}` |
| `GET/POST` | `/api/save` | zapis stanu do `savegame.fen` |
| `GET/POST` | `/api/load` | wczytanie stanu z `savegame.fen` |

---

## Wdrożenie

### Docker (wersja webowa)

```bash
# budowanie obrazu
docker build -t chess-web .

# uruchomienie
docker run -p 8000:8000 chess-web
```

Serwer dostępny pod: [http://localhost:8000](http://localhost:8000)

---

### PyInstaller (wersja desktopowa → .exe)

```bash
pip install pyinstaller
pyinstaller chess.spec
```

Plik wykonywalny powstaje w `dist/chess.exe` – nie wymaga zainstalowanego Pythona.

---

## Testy

```bash
python -m pytest tests/ -v
```

Ponad 100 testów jednostkowych pokrywających:
- walidację i roundtrip FEN
- `make_move` / `undo_move` / `get_piece`
- generowanie ruchów (pionki, skoczki, wieże, król)
- wykrywanie mata i pata
- roszady
- strategie AI (`RandomMoveStrategy`, `MinimaxAlphaBetaStrategy`)
- integralność planszy po przeszukiwaniu Minimax
