import datetime
import numpy as np

class TimeSeries:
    def __init__(self, nazwa_wskaznika, kod_stacji, czas_usredniania, dates, values, unit):
        self.nazwa_wskaznika = nazwa_wskaznika
        self.kod_stacji = kod_stacji
        self.czas_usredniania = czas_usredniania
        self.dates = dates
        self.values = values
        self.unit = unit
    def __str__(self):
        return f"{self.nazwa_wskaznika}, jednostka {self.unit}"
    def __repr__(self):
        return f"TimeSeries(nazwa_wskaznika={self.nazwa_wskaznika}, kod_stacji={self.kod_stacji}, czas_usredniania={self.czas_usredniania}, dates={self.dates}, values={self.values}, unit={self.unit})"
    def __getitem__(self, key):

        if isinstance(key, (int, slice)):
            if isinstance(key, int):
                return (self.dates[key], self.values[key])
            else: return list(zip(self.dates[key], self.values[key]))

        elif isinstance(key, datetime.datetime):
            try:
                idx = self.dates.index(key) 
                return self.values[idx]
            except ValueError:
                raise KeyError(f"Nie znaleziono daty {key}")

        elif isinstance(key, datetime.date):
            results = []
            for d, v in zip(self.dates, self.values):
                if d.date() == key:
                    results.append(v)
            if not results:
                raise KeyError(f"Nie znaleziono dnia {key}")
            return results

        #nie wpadlismy w zadnego if instance
        raise TypeError("Niepoprawny typ klucza.")
    
    @property
    def missing_count(self):
        return self.values.count(None)
    
    def completeness(self):
        total = len(self.values)
        missing = self.missing_count
        if total == 0:
            return 0.0
        return (total - missing) / total * 100
    
daty = [datetime.datetime(2026, 4, 20),
         datetime.datetime(2026, 4, 20), datetime.datetime(2026, 4, 21)]
wartosci = [10.5, None, 8.7]

ts = TimeSeries("PM10", "6767", "1h", daty, wartosci, "g/m3")

print(ts)
print(repr(ts))
print(ts[0])
print(ts[0:2])
print(ts[datetime.datetime(2026, 4, 20)])
print(ts[datetime.date(2026, 4, 20)])
print(f"missing count: {ts.missing_count}")
print(f"completness: {ts.completeness()}%")
try:
    print(ts[datetime.date(2026, 4, 30)])
except KeyError:
    print("blad!")