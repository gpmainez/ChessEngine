import typer
from enum import Enum
from datetime import datetime
from typing import Annotated

app = typer.Typer(help="CLI typer")

class Measurement(str, Enum):
    PM10 = "PM10"
    PM25 = "PM2.5"
    O3 = "O3"
    NO2 = "NO2"
    SO2 = "SO2"
    CO = "CO"
    C6H6 = "C6H6"

class Frequency(str, Enum):
    g1 = "1g"
    g24 = "24g"

@app.callback()
def global_options(
    ctx: typer.Context,
    measurement: Annotated[Measurement, typer.Option(help="Mierzona wielkość")],
    frequency: Annotated[Frequency, typer.Option(help="Częstotliwość")],
    start: Annotated[datetime, typer.Option(formats=["%Y-%m-%d"], help="Początek (RRRR-MM-DD)")],
    end: Annotated[datetime, typer.Option(formats=["%Y-%m-%d"], help="Koniec (RRRR-MM-DD)")]):
    ctx.obj = {
        "measurement": measurement,
        "frequency": frequency,
        "start": start,
        "end": end
    }

@app.command()
def random(ctx: typer.Context):
    params = ctx.obj
    typer.echo(f"Moduł losujący (Typer)")
    typer.echo(f"Szukam stacji dla {params['measurement']} w oknie {params['start'].date()} : {params['end'].date()}")

@app.command()
def statistics(
    ctx: typer.Context,
    station: Annotated[str, typer.Option(help="Identyfikator stacji")]):
    params = ctx.obj
    typer.echo(f"Moduł analityczny (Typer)")
    typer.echo(f"Obliczanie statystyk dla stacji: {station}")

if __name__ == "__main__":
    app()