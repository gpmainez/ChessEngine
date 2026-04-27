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

    seria = TimeSeries("PM2.5", "222", "24h", daty, wartosci, "mg/m3")

    klasy = [SimpleReporter(), OutlierDetector(k=2), ThresholdDetector(20), ZeroSpikeDetector()]

    for detektor in klasy:
        wynik = detektor.analyze(seria)
        print(f"{detektor} a wynik to {wynik}")



if __name__ == "__main__":
    main()