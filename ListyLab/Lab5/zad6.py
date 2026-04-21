import argparse
import logging
import sys
import csv
import random
from datetime import datetime

from zad2 import group_measurement_files_by_key

class StdOutFilter(logging.Filter):
    def filter(self, record):
        return record.levelno <= logging.WARNING

def setup_logger():
    logger = logging.getLogger('gios_analyzer')
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(levelname)s | %(message)s')


    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.addFilter(StdOutFilter())
    stdout_handler.setFormatter(formatter)

    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.ERROR)
    stderr_handler.setFormatter(formatter)

    logger.addHandler(stdout_handler)
    logger.addHandler(stderr_handler)

    return logger

logger = setup_logger()


def validate_date(value):
    try:
        datetime.strptime(value, '%Y-%m-%d')
        return value
    except ValueError:
        raise argparse.ArgumentTypeError(f"Błedna data: '{value}'. Wymagany format RRRR-MM-DD.")

def validate_measurement(value):
    allowed_values = {'PM10', 'PM2.5', 'O3', 'NO2', 'SO2', 'CO', 'C6H6'}
    val_upper = value.upper()
    if val_upper not in allowed_values:
        raise argparse.ArgumentTypeError(f"Nierozpoznana wielkość '{value}'. Dozwolone: {', '.join(allowed_values)}.")
    return val_upper

def execute_random(args):
    logger.info("Moduł losujący")
    
    try:
        start_year = str(datetime.strptime(args.start, '%Y-%m-%d').year)
        target_key = (start_year, args.measurement, args.frequency)
        logger.debug(f"Szukany klucz pliku: {target_key}")

        measurements_dir = "measurements"
        all_files = group_measurement_files_by_key(measurements_dir)

        if target_key not in all_files:
            logger.warning(f"Brak dostępnych pomiarów (brak pliku) dla parametrów: {target_key}.")
            return

        file_path = all_files[target_key]
        
        logger.info(f"Otwieranie pliku z pomiarami: {file_path}")

        valid_stations = set()
        
        start_date = datetime.strptime(args.start, '%Y-%m-%d')
        end_date = datetime.strptime(args.end, '%Y-%m-%d')

        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            
            next(reader)                
            stations_row = next(reader) 
            next(reader)                
            next(reader)                
            next(reader)                
            next(reader)                
            
            station_codes = stations_row[1:] 

            for row in reader:
                raw_row = ",".join(row) + "\n"
                size = len(raw_row.encode('utf-8'))
                logger.debug(f"Przeczytano wiersz. Rozmiar: {size} bajtów.")

                if not row or not row[0]:
                    continue

                date_str = row[0]
                try:
                    measurement_date = datetime.strptime(date_str, '%m/%d/%y %H:%M')
                except ValueError:
                    continue

                measurement_day = measurement_date.replace(hour=0, minute=0, second=0, microsecond=0)

                if start_date <= measurement_day <= end_date:
                    for i, value in enumerate(row[1:]):
                        if value.strip():
                            valid_stations.add(station_codes[i])

        logger.info(f"Zamykanie pliku z pomiarami: {file_path}")

        if not valid_stations:
            logger.warning("Plik istnieje ale filtr dat zwrocil pustą listę. Brak pomiarów w zadanym oknie.")
        else:
            random_station = random.choice(list(valid_stations))
            print(f"\n=> Znaleziona losowa stacja mierząca {args.measurement}: {random_station}\n")

    except FileNotFoundError as e:
        logger.error(f"KRYTYCZNY błąd dostępu do plików: {e}")

def execute_statistics(args):
    logger.info("Moduł analityczny")
    logger.info(f"Obliczanie średniej i odchylenia dla stacji: {args.station}")



def build_parser():
    parser = argparse.ArgumentParser(description="CLI dla danych pogodowych GIOŚ")
    
    parser.add_argument('--measurement', type=validate_measurement, required=True, help="Badany parametr (np. PM10)")
    parser.add_argument('--frequency', choices=['1g', '24g'], required=True, help="Próbkowanie czasowe")
    parser.add_argument('--start', type=validate_date, required=True, help="Data startowa (RRRR-MM-DD)")
    parser.add_argument('--end', type=validate_date, required=True, help="Data końcowa (RRRR-MM-DD)")

    subparsers = parser.add_subparsers(dest='action', required=True, help="Dostępne operacje:")

    cmd_random = subparsers.add_parser('random', help="Zwraca losową stację")
    cmd_random.set_defaults(run=execute_random)

    cmd_statistics = subparsers.add_parser('statistics', help="Zbiera dane dla stacji")
    cmd_statistics.add_argument('--station', required=True, help="Identyfikator stacji")
    cmd_statistics.set_defaults(run=execute_statistics)

    return parser

def main():
    parser = build_parser()
    args = parser.parse_args()
    args.run(args)

if __name__ == '__main__':
    main()