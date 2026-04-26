import csv
from datetime import datetime
from pathlib import Path
from zad2 import TimeSeries


class Measurements:
    def __init__(self, directory_path: str):
        self.directory_path = Path(directory_path)
        self._file_catalog = {}
        self._loaded_series: list['TimeSeries'] = []

        # Zabezpieczenie przed ponownym wczytywaniem tego samego pliku
        self._loaded_files = set()
        self._scan_directory()

    def _scan_directory(self):
        for file_path in self.directory_path.glob('*.csv'):

            if "stacje" in file_path.name.lower(): continue

            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                try:
                    next(reader)
                    row_stacje = next(reader)
                    station_codes = row_stacje[1:]
                    row_parametr = next(reader)
                    param_name = row_parametr[1]
                except StopIteration:
                    continue

            if param_name not in self._file_catalog:
                self._file_catalog[param_name] = []

            self._file_catalog[param_name].append({
                'path': str(file_path),
                'stations_num': len(station_codes),
                'stations': station_codes
            })

    def __len__(self) -> int:
        total_series = 0
        for parameter_files in self._file_catalog.values():
            for file_info in parameter_files:
                total_series += file_info["stations_num"]
        return total_series

    def __contains__(self, parameter_name: str) -> bool:
        return parameter_name in self._file_catalog

    def _load_file_to_memory(self, file_path: str, parameter_name: str):

        if file_path in self._loaded_files:
            return

        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)

            # skip wierszy
            next(reader)
            row_stacje = next(reader)
            station_codes = row_stacje[1:]

            next(reader)  # Wiersz 3: Wskaźnik

            row_czas = next(reader)  # Wiersz 4: Czas uśredniania
            czas_usredniania = row_czas[1] if len(row_czas) > 1 else "1h"

            row_jednostka = next(reader)  # Wiersz 5: Jednostka
            jednostka = row_jednostka[1] if len(row_jednostka) > 1 else ""

            next(reader)  # Wiersz 6: Kod stanowiska

            dates = []
            values_per_station = {station: [] for station in station_codes}

            # --- Właściwe czytanie pomiarów ---
            for row in reader:
                if not row: continue

                # Format daty dopasowany do Twojego pliku: 01/16/23 12:00
                date_val = datetime.strptime(row[0], "%m/%d/%y %H:%M")
                dates.append(date_val)

                for i, station in enumerate(station_codes):
                    val_str = row[i + 1]
                    val = float(val_str) if val_str.strip() else None
                    values_per_station[station].append(val)

            for station in station_codes:
                ts = TimeSeries(
                    nazwa_wskaznika=parameter_name,
                    kod_stacji=station,
                    czas_usredniania=czas_usredniania,  # Automatycznie z pliku
                    dates=dates.copy(),
                    values=values_per_station[station],
                    unit=jednostka  # Automatycznie z pliku
                )
                self._loaded_series.append(ts)

        # Zaznaczamy plik jako wczytany
        self._loaded_files.add(file_path)

    def get_by_parameter(self, parameter_name: str) -> list['TimeSeries']:
        if parameter_name in self._file_catalog:
            for file_info in self._file_catalog[parameter_name]:
                self._load_file_to_memory(file_info['path'], parameter_name)

        # Poprawka: uzywamy .nazwa_wskaznika zamiast .name
        return [ts for ts in self._loaded_series if ts.nazwa_wskaznika == parameter_name]

    def get_by_station(self, station_code: str) -> list['TimeSeries']:
        for param_name, files_list in self._file_catalog.items():
            for file_info in files_list:
                if station_code in file_info['stations']:
                    self._load_file_to_memory(file_info['path'], param_name)

        # Poprawka: uzywamy .kod_stacji zamiast .station_code
        return [ts for ts in self._loaded_series if ts.kod_stacji == station_code]

    def detect_all_anomalies(self, validators: list['SeriesValidator'], preload: bool = False) -> dict:
        """
        Przechodzi przez serie czasowe i szuka anomalii przy pomocy przekazanych walidatorów.
        """
        # Zadanie 6a: Jeśli preload=True, wymuszamy wczytanie absolutnie wszystkich plików z katalogu
        if preload:
            for param_name, files_list in self._file_catalog.items():
                for file_info in files_list:
                    self._load_file_to_memory(file_info['path'], param_name)

        # Zadanie 7: Słownik do agregacji wyników
        raport_anomalii = {}

        # Jeśli preload=False, pętla przejdzie tylko po tym, co już było wcześniej w self._loaded_series
        for ts in self._loaded_series:
            # Tworzymy czytelny klucz dla słownika, żeby klient wiedział, gdzie jest błąd
            klucz_serii = f"{ts.kod_stacji} - {ts.nazwa_wskaznika}"
            bledy_dla_serii = []

            # Uruchamiamy każdą "strategię" (walidator) z listy
            for validator in validators:
                wynik = validator.analyze(ts)
                # Wynik to lista stringów (lub pusta, jeśli jest OK). Jeśli coś tam jest, dodajemy.
                if wynik:
                    bledy_dla_serii.extend(wynik)

            # Zapisujemy do raportu TYLKO stacje, w których coś poszło nie tak
            if bledy_dla_serii:
                raport_anomalii[klucz_serii] = bledy_dla_serii

        return raport_anomalii
