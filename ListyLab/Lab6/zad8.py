from zad4 import OutlierDetector, ThresholdDetector, ZeroSpikeDetector
from zad2 import TimeSeries
import statistics, datetime
class SimpleReporter:

    def __str__(self):
        return "SimpleReporter()"
    def analyze(self, series: 'TimeSeries'):
        clean_vals = [v for v in series.values if v is not None]
        if not clean_vals:
            return [f"Info: {series.nazwa_wskaznika} at {series.kod_stacji} has no valid data"]
            
        avg = statistics.mean(clean_vals)
        return [f"Info: {series.nazwa_wskaznika} at {series.kod_stacji} has mean = {avg:.2f}"]

def main():
    daty = [datetime.date(2020, 7, i) for i in range(1,11)]
    wartosci = [6.7, 10, None, 1.0, None, 20.67, 11.4, 9.6, 11, 19.245]
    wartosci_zle = [None] * 10
    wartosci3 = [6.7, 10, 999, 1.0, None, 20.67, 11.4, 9.6, 11, 19.245]
    wartosc4 = [2]

    seria = TimeSeries("PM2.5", "222", "24h", daty, wartosci, "mg/m3")
    seria2 = TimeSeries("PM2.5", "3UL4", "24h", daty, wartosci_zle, "mg/m3")
    seria3 = TimeSeries("PM2.5", "AD1XON", "24h", daty, wartosci3, "mg/m3")
    seria4 = TimeSeries("PM2.5", "oL444", "24h", [datetime.date(2010,4,20)], wartosc4, "kg/m3")

    klasy = [SimpleReporter(), OutlierDetector(k=2), ThresholdDetector(20), ZeroSpikeDetector()]

    print("\n\n testy dla zwykłej listy")
    for detektor in klasy:
        wynik = detektor.analyze(seria)
        print(f"{detektor} a wynik to {wynik}\n")

    print("\n\n testy dla pustej listy")
    for detektor in klasy:
        wynik = detektor.analyze(seria2)
        print(f"{detektor} a wynik to {wynik}\n")

    print("\n\n testy dla listy z bardzo duzymi pomiarami")
    for detektor in klasy:
        wynik = detektor.analyze(seria3)
        print(f"{detektor} a wynik to {wynik}\n")

    print("\n\n lista1 elementowa")
    for detektor in klasy:
        wynik = detektor.analyze(seria4)
        print(f"{detektor} a wynik to {wynik}\n")


if __name__ == "__main__":
    main()