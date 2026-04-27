import os
import shutil
from pathlib import Path
from datetime import datetime

# UWAGA: Zmień 'zad5' na nazwę Twojego pliku z klasą Measurements!
from zad5 import Measurements
from zad4 import SeriesValidator
from zad2 import TimeSeries


def przygotuj_poligon_testowy(katalog: str):
    """Tworzy ekstremalne pliki testowe."""
    path = Path(katalog)
    if path.exists():
        shutil.rmtree(path)
    path.mkdir()

    # 1. PLIK IDEALNY (Happy Path)
    (path / "1_idealny_PM10.csv").write_text(
        "Nr,1,2\n"
        "Kod stacji,DsGlog,DsLegnica\n"
        "Wskaźnik,PM10,PM10\n"
        "Czas uśredniania,24g,24g\n"
        "Jednostka,ug/m3,ug/m3\n"
        "Kod stanowiska,Glog-1,Leg-1\n"
        "01/01/23 12:00,10.5,12.1\n"
        "01/02/23 12:00,15.2,18.0\n"
        "01/03/23 12:00,,8.5\n",  # Celowy brak danych (zwykły przecinek)
        encoding='utf-8'
    )

    # 2. PLIK ZEPSUTY STRUKTURALNIE (Test _scan_directory)
    (path / "2_smieci.csv").write_text(
        "Faktura VAT nr 123/2023\n"
        "Do zapłaty: 1500 PLN\n"
        "Termin: wczoraj",
        encoding='utf-8'
    )

    # 3. PLIK Z ZEPSUTYMI DANYMI (Test _load_file)
    (path / "3_wirus_O3.csv").write_text(
        "Nr,1,2\n"
        "Kod stacji,MzWarsz,KpKrakow\n"
        "Wskaźnik,O3,O3\n"
        "Czas uśredniania,1h,1h\n"
        "Jednostka,ug/m3,ug/m3\n"
        "Kod stanowiska,W1,K1\n"
        "zła_data_w_ogóle,15.0,20.0\n"  # BŁĄD 1: Zły format daty
        "01/02/23 12:00,BŁĄD,5.5\n"  # BŁĄD 2: Tekst zamiast liczby
        "01/03/23 12:00,10.0\n"  # BŁĄD 3: Ucięty wiersz (brak pomiaru dla Krakowa)
        "01/04/23 12:00,12.0,14.0\n",  # JEDEN POPRAWNY WIERSZ (żeby zobaczyć, czy program przetrwał)
        encoding='utf-8'
    )


# Prosty walidator testowy, żeby sprawdzić zadanie 7
class TestValidator(SeriesValidator):
    def analyze(self, series: TimeSeries) -> list[str]:
        bledy = []
        for val in series.values:
            if val is not None and val > 15.0:
                bledy.append(f"Wartość {val} > 15.0!")
        return bledy


if __name__ == "__main__":
    katalog_testowy = "poligon_danych"
    przygotuj_poligon_testowy(katalog_testowy)

    print("\n" + "=" * 50)
    print(" ROZPOCZĘCIE TESTÓW SYSTEMU ".center(50, "="))
    print("=" * 50 + "\n")

    print("--- ETAP 1: Skanowanie (Oczekiwane 1 ostrzeżenie o 'smieci.csv') ---")
    pomiary = Measurements(katalog_testowy)

    print(f"\n[WYNIK] System załadował {len(pomiary)} stacji do katalogu.")
    print(f"[WYNIK] Dostępne wskaźniki w pamięci: {list(pomiary._file_dict.keys())}")
    assert "PM10" in pomiary and "O3" in pomiary, "Brak oczekiwanych wskaźników!"

    print("\n--- ETAP 2: Pobieranie danych i walka z zepsutymi wierszami ---")
    print("(Oczekiwane 2 ostrzeżenia o złej dacie i złej wartości dla pliku O3)")
    serie_o3 = pomiary.get_by_parameter("O3")

    warszawa_o3 = next(ts for ts in serie_o3 if ts.kod_stacji == "MzWarsz")
    krakow_o3 = next(ts for ts in serie_o3 if ts.kod_stacji == "KpKrakow")

    print("\n[WYNIK] Analiza uratowanych danych dla Warszawy:")
    print(f"Daty: {warszawa_o3.dates}")
    print(f"Wartości: {warszawa_o3.values}")
    assert warszawa_o3.values == [None, 10.0, 12.0], "Niepoprawne parsowanie Warszawy!"

    print("\n[WYNIK] Analiza uratowanych danych dla Krakowa:")
    print(f"Wartości: {krakow_o3.values}")
    assert krakow_o3.values == [5.5, None, 14.0], "Niepoprawne parsowanie Krakowa!"

    print("\n--- ETAP 3: Leniwe ładowanie i Test get_by_station ---")
    stacje_glogow = pomiary.get_by_station("DsGlog")
    print(f"[WYNIK] Pobrano {len(stacje_glogow)} serię dla Głogowa.")
    print(f"[WYNIK] Wartości Głogów PM10: {stacje_glogow[0].values}")

    print("\n--- ETAP 4: Test Walidatorów (Zadanie 7) ---")
    # Badamy wszystkie wczytane już serie (PM10 i O3) naszym testowym walidatorem (> 15.0)
    raport = pomiary.detect_all_anomalies([TestValidator()])

    for klucz, bledy in raport.items():
        print(f"Raport dla [{klucz}]:")
        for b in bledy:
            print(f"  -> {b}")

    print("\n" + "=" * 50)
    print(" WSZYSTKIE TESTY ZAKOŃCZONE SUKCESEM! ".center(50, "="))
    print("=" * 50 + "\n")