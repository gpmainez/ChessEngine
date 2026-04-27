import csv
import os
from datetime import datetime
from pathlib import Path
from zad2 import TimeSeries
import logging
from zad4 import SeriesValidator

logging.basicConfig(level=logging.WARNING, format='%(levelname)s: %(message)s')


class Measurements:
    def __init__(self, directory_path: str):
        self.directory_path = Path(directory_path)
        self._file_dict = {}
        self._loaded_timeSeries: list[TimeSeries] = []

        if not self.directory_path.exists() or not self.directory_path.is_dir():
            logging.error(f"'{self.directory_path}' nie istnieje!")
            return

        #R_ok read accces
        #X_ok enter
        if not os.access(self.directory_path, os.R_OK | os.X_OK):
            logging.error(f"Brak uprawnień (Permission Denied) do folderu '{self.directory_path}'!")
            return

        self._loaded_files = set()
        self._scan_directory()

    def _scan_directory(self):
        for file_path in self.directory_path.glob('*.csv'):

            if "stacje" in file_path.name.lower(): continue

            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                try:
                    row1 = next(reader)
                    if not row1 or row1[0] != "Nr":
                        logging.warning(f"wrong {file_path.name} file structure")
                        continue

                    row_stacje = next(reader)
                    if not row_stacje or len(row_stacje) < 2 or row_stacje[0] != "Kod stacji":
                        continue
                    station_codes = row_stacje[1:]

                    row_param = next(reader)
                    if not row_param or len(row_param) < 2 or row_param[0] != "Wskaźnik":
                        continue
                    param_name = row_param[1]
                except StopIteration:
                    continue

            if param_name not in self._file_dict:
                self._file_dict[param_name] = []

            self._file_dict[param_name].append({
                'path': str(file_path),
                'stations_num': len(station_codes),
                'stations': station_codes
            })

    def __len__(self) -> int:
        total_series = 0
        for files in self._file_dict.values():
            for file_info in files:
                total_series += file_info["stations_num"]
        return total_series

    def __contains__(self, parameter_name: str) -> bool:
        return parameter_name in self._file_dict

    def _load_file(self, file_path: str, parameter_name: str):

        if file_path in self._loaded_files:
            return

        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)

            # skip wierszy
            next(reader)
            row_stacje = next(reader)
            station_codes = row_stacje[1:]

            next(reader)  # 3

            row_czas = next(reader)  # 4
            time = row_czas[1] if len(row_czas) > 1 else "1h"

            row_typ_pomiaru = next(reader)  # 5
            typ_pomiaru = row_typ_pomiaru[1] if len(row_typ_pomiaru) > 1 else ""

            next(reader)  # 6

            dates = []
            values_per_station = {}
            for station in station_codes:
                values_per_station[station] = []

            for row in reader:
                if not row: continue

                try:
                    date_val = datetime.strptime(row[0], "%m/%d/%y %H:%M")
                except (ValueError, IndexError):
                    logging.warning(f"zły format daty {Path(file_path).name}: '{row[0]}'. skip wiersz")
                    continue

                dates.append(date_val)

                for i, station in enumerate(station_codes):
                    # uciecie wiersza
                    if i + 1 >= len(row):
                        values_per_station[station].append(None)
                        continue
                    # get value
                    val_str = row[i + 1]

                    # litery
                    try:
                        val = float(val_str) if val_str.strip() else None
                    except ValueError:
                        logging.warning(f" zła wartość (litera zmaist liczby) '{val_str}' default None.")
                        val = None

                    values_per_station[station].append(val)

            for station in station_codes:
                ts = TimeSeries(
                    nazwa_wskaznika=parameter_name,
                    kod_stacji=station,
                    time=time,
                    dates=dates.copy(),
                    values=values_per_station[station],
                    unit=typ_pomiaru
                )
                self._loaded_timeSeries.append(ts)

        # plik wczytany
        self._loaded_files.add(file_path)

    def get_by_parameter(self, parameter_name: str) -> list[TimeSeries]:
        if parameter_name in self._file_dict:
            for file_info in self._file_dict[parameter_name]:
                self._load_file(file_info['path'], parameter_name)

        return [ts for ts in self._loaded_timeSeries if ts.nazwa_wskaznika == parameter_name]

    def get_by_station(self, station_code: str) -> list[TimeSeries]:
        for param_name, files_list in self._file_dict.items():
            for file_info in files_list:
                if station_code in file_info['stations']:
                    self._load_file(file_info['path'], param_name)

        return [ts for ts in self._loaded_timeSeries if ts.kod_stacji == station_code]

    def detect_all_anomalies(self, validators: list[SeriesValidator], preload: bool = False) -> dict:

        if preload:
            for param_name, files_list in self._file_dict.items():
                for file_info in files_list:
                    self._load_file(file_info['path'], param_name)

        error_dict = {}

        for ts in self._loaded_timeSeries:
            key = f"{ts.kod_stacji} - {ts.nazwa_wskaznika}"
            error_in_sers = []

            for validator in validators:
                res = validator.analyze(ts)

                if res:
                    error_in_sers.extend(res)

            if error_in_sers:
                error_dict[key] = error_in_sers

        return error_dict
