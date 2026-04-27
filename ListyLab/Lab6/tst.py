from zad5 import Measurements

from zad4 import ThresholdDetector, ZeroSpikeDetector

if __name__ == "__main__":

    pomiary = Measurements("testowe_pomiary")
    pomiary2 = Measurements("measurements")
    pomiary3 = Measurements("priv")


    pomiary.get_by_parameter("NO2")
    pomiary.get_by_parameter("PM10")
    pomiary2.get_by_parameter("As(PM10)")
    pomiary.get_by_parameter("O3")
    pomiary3.get_by_parameter("O3")

    valid = [
        ZeroSpikeDetector(k=3),
        ThresholdDetector(threshold=200.0)
    ]

    from unittest.mock import patch

    # "Oszukujemy" system, że os.access zawsze zwraca False dla testu
    with patch("os.access", return_value=False):
        pomiary3 = Measurements("C:/Users/pc/Desktop/Nowy folder")
        # Teraz na 100% zobaczysz log: ERROR: Brak uprawnień...

    for ts in pomiary._loaded_timeSeries:
        print(f"\n[Stacja: {ts.kod_stacji}] | Wskaźnik: {ts.nazwa_wskaznika}")
        print(f"   -> Daty: {ts.dates}")
        print(f"   -> Wartości: {ts.values}")

    res = pomiary.detect_all_anomalies(valid)
    for stacja, error in res.items():
        print(f"\n przekracza progi {stacja}")
        for blad in error:
            print(f"    -> {blad}")