from abc import ABC, abstractmethod
import statistics
from zad2 import TimeSeries

class SeriesValidator(ABC):
    @abstractmethod
    def analyze(self, series: 'TimeSeries'):
        pass

class OutlierDetector(SeriesValidator):
    def __init__(self, k):
        self.k = k
    def __str__(self):
        return f"OutlierDetector(k={self.k})"

    def analyze(self, series: 'TimeSeries'):
        valid_values = [v for v in series.values if v is not None]

        if len(valid_values) < 2: #bo odchylenie dla 1 wartosci to 0, czyli warunek detekcji to 0 > 0
            return [] 

        avg = statistics.mean(valid_values)
        k_stdev = self.k * statistics.stdev(valid_values)

        messages = []

        for date, val in zip(series.dates, series.values):
            if val is not None:
                if abs(val - avg) > k_stdev:
                    messages.append(f"Wartosc {val} z dnia {date} przekracza dopuszczalna {self.k}-krotnosc odchylenie")
        
        return messages
    
class ZeroSpikeDetector(SeriesValidator):
    def __init__(self, k=3):
        self.k = k

    def __str__(self):
        return f"ZeroSpikeDetector(zeroes or Nones in a row={self.k})"

    def analyze(self, series: 'TimeSeries'):
        messages = []
        consecutive_count = 0
        start_date = None
        last_date = None

        for date, val in zip(series.dates, series.values):
            if val is None or val == 0:
                if consecutive_count == 0:
                    start_date = date
                consecutive_count += 1
                last_date = date
            else:
                if consecutive_count >= self.k:
                    messages.append(f"Wykryto {consecutive_count} zera/braki z rzedu od {start_date} do {last_date} (dopuszczalne {self.k-1})")
                consecutive_count = 0

        if consecutive_count >= self.k:
                messages.append(f"Wykryto {consecutive_count} zera/braki z rzedu od {start_date} do {last_date} (dopuszczalne {self.k-1})")
                
        return messages 
    

class ThresholdDetector(SeriesValidator):
    def __init__(self, threshold):
        self.threshold = threshold

    def __str__(self):
        return f"ThresholdDetector(threshold={self.threshold})"

    def analyze(self, series: 'TimeSeries'):
        messages = []
        
        for date, val in zip(series.dates, series.values):
            if val is not None and val > self.threshold:
                messages.append(f"Przekroczenie progu ({self.threshold})!!!! zarejestrowano {val} w dniu {date}")
                
        return messages