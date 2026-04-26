import csv
from datetime import datetime
from pathlib import Path
from zad2 import TimeSeries
import logging

logging.basicConfig(level=logging.WARNING, format='%(levelname)s: %(message)s')

class Measurements:
    def __init__(self, directory_path: str):
        self.directory_path = Path(directory_path)
        self._file_dict = {}
        self._loaded_timeSeries: list['TimeSeries'] = []

        #wczytywanie tego samego pliku
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
                        logging.warning(f"Plik {file_path.name} to nie GIOŚ. Pomijam.")
                        continue

                    row_stacje = next(reader)
                    if not row_stacje or len(row_stacje) < 2 or row_stacje[0] != "Kod stacji":
                        continue
                    station_codes = row_stacje[1:]

                    row_parametr = next(reader)
                    if not row_parametr or len(row_parametr) < 2 or row_parametr[0] != "Wskaźnik":
                        continue
                    param_name = row_parametr[1]
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
        for parameter_files in self._file_dict.values():
            for file_info in parameter_files:
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
            czas_usredniania = row_czas[1] if len(row_czas) > 1 else "1h"

            row_jednostka = next(reader)  # 5
            jednostka = row_jednostka[1] if len(row_jednostka) > 1 else ""

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
                    logging.warning(f"Błędny format daty w pliku {Path(file_path).name}: '{row[0]}'. Pomijam wiersz.")
                    continue

                dates.append(date_val)

                for i, station in enumerate(station_codes):
                    #uciecie wiersza
                    if i + 1 >= len(row):
                        values_per_station[station].append(None)
                        continue

                    val_str = row[i + 1]

                    # litery zamist liczb
                    try:
                        val = float(val_str) if val_str.strip() else None
                    except ValueError:
                        logging.warning(f"Zła wartość '{val_str}' dla stacji {station}. Ustawiam None.")
                        val = None

                    values_per_station[station].append(val)

            for station in station_codes:
                ts = TimeSeries(
                    nazwa_wskaznika=parameter_name,
                    kod_stacji=station,
                    czas_usredniania=czas_usredniania,
                    dates=dates.copy(),
                    values=values_per_station[station],
                    unit=jednostka
                )
                self._loaded_timeSeries.append(ts)

        # plik wczytany
        self._loaded_files.add(file_path)

    def get_by_parameter(self, parameter_name: str) -> list['TimeSeries']:
        if parameter_name in self._file_dict:
            for file_info in self._file_dict[parameter_name]:
                self._load_file(file_info['path'], parameter_name)

        return [ts for ts in self._loaded_timeSeries if ts.nazwa_wskaznika == parameter_name]

    def get_by_station(self, station_code: str) -> list['TimeSeries']:
        for param_name, files_list in self._file_dict.items():
            for file_info in files_list:
                if station_code in file_info['stations']:
                    self._load_file(file_info['path'], param_name)

        return [ts for ts in self._loaded_timeSeries if ts.kod_stacji == station_code]

    def detect_all_anomalies(self, validators: list['SeriesValidator'], preload: bool = False) -> dict:

        if preload:
            for param_name, files_list in self._file_dict.items():
                for file_info in files_list:
                    self._load_file(file_info['path'], param_name)

        raport_anomalii = {}

        for ts in self._loaded_timeSeries:
            # klucz dla słownika, gdzie jest błąd
            klucz_serii = f"{ts.kod_stacji} - {ts.nazwa_wskaznika}"
            bledy_dla_serii = []

            for validator in validators:
                wynik = validator.analyze(ts)

                if wynik:
                    bledy_dla_serii.extend(wynik)

            if bledy_dla_serii:
                raport_anomalii[klucz_serii] = bledy_dla_serii

        return raport_anomalii
