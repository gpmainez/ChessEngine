import argparse
from datetime import datetime

def validate_date(value):
    try:
        datetime.strptime(value, '%Y-%m-%d')
        return value
    except ValueError:
        raise argparse.ArgumentTypeError(f"Bledna data: '{value}'. Wymagany format RRRR-MM-DD.")

def validate_measurement(value):

    allowed_values = {'PM10', 'PM2.5', 'O3', 'NO2', 'SO2', 'CO', 'C6H6'}
    val_upper = value.upper()
    if val_upper not in allowed_values:
        raise argparse.ArgumentTypeError(f"Nierozpoznana wielkość '{value}'. Dozwolone: {', '.join(allowed_values)}.")
    return val_upper


def execute_random(args):
    print("Moduł losujący")
    print(f"Szukam stacji dla {args.measurement} z pomiarami w oknie {args.start} : {args.end}")

def execute_statistics(args):
    print("Moduł analityczny")
    print(f"Obliczanie średniej i odchylenia dla stacji: {args.station}")


def build_parser():
    parser = argparse.ArgumentParser(description="CLI dla danych pogodowych")
    
    parser.add_argument('--measurement', type=validate_measurement, required=True, help="Badany parametr (np. PM10)")
    parser.add_argument('--frequency', choices=['1g', '24g'], required=True, help="Próbkowanie czasowe")
    parser.add_argument('--start', type=validate_date, required=True, help="Data startowa (RRRR-MM-DD)")
    parser.add_argument('--end', type=validate_date, required=True, help="Data końcowa (RRRR-MM-DD)")

    subparsers = parser.add_subparsers(dest='action', required=True, help="Dostępne operacje:")

    cmd_random = subparsers.add_parser('random', help="Zwraca dane losowej stacji dla zadanych kryteriów")
    cmd_random.set_defaults(run=execute_random)

    cmd_statistics = subparsers.add_parser('statistics', help="Zbiera dane dla konkretnej stacji")
    cmd_statistics.add_argument('--station', required=True, help="Identyfikator stacji docelowej")
    cmd_statistics.set_defaults(run=execute_statistics)

    return parser

def main():
    parser = build_parser()
    args = parser.parse_args()
    
    args.run(args)

if __name__ == '__main__':
    main()