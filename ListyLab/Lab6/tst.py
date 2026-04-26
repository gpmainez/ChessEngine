import time


from Lab6.zad5 import Measurements


# Atrapa walidatora z Zadania 8 (albo użyj prawdziwego OutlierDetector)
class SeriesValidator:
    pass


class DummyValidator(SeriesValidator):
    def analyze(self, series):

        if series.missing_count > 0:
            return [f"Znaleziono {series.missing_count} braków danych!"]
        return []


# ==========================================
# ROZPOCZYNAMY TESTY
# ==========================================

if __name__ == "__main__":
    print("--- 1. INICJALIZACJA SYSTEMU ---")
    start = time.time()

    pomiary = Measurements('measurements')
    koniec = time.time()
    print(f"System wstał w {koniec - start:.4f} s.")
    print(f"Potencjalnych stacji do załadowania: {len(pomiary)}")


    nazwa_testowa = 'As(PM10)'
    print(f"Czy mamy dane o '{nazwa_testowa}'? {'Tak' if nazwa_testowa in pomiary else 'Nie'}")

    print("\n--- 2. PIERWSZE CZYTANIE (Dysk) ---")
    start = time.time()

    stacja_ts = pomiary.get_by_station('DsGlogWiStwo')
    koniec = time.time()
    print(f"Znalazłem {len(stacja_ts)} serii dla tej stacji.")
    print(f"Czytanie z dysku zajęło: {koniec - start:.4f} s.")

    print("\n--- 3. DRUGIE CZYTANIE (Cache - powinno być natychmiastowe!) ---")
    start = time.time()
    stacja_ts_znowu = pomiary.get_by_station('DsGlogWiStwo')
    koniec = time.time()
    print(f"Czytanie z pamięci RAM zajęło: {koniec - start:.6f} s.")

    print("\n--- 4. TEST DETEKCJI BŁĘDÓW ---")
    walidatory = [DummyValidator()]


    raport = pomiary.detect_all_anomalies(walidatory, preload=False)

    print("Raport z anomalii (tylko wczytane dane):")
    for stacja, bledy in raport.items():
        print(f"  [{stacja}] -> {bledy}")