from zad4 import OutlierDetector, ThresholdDetector, ZeroSpikeDetector
from zad2 import TimeSeries
import datetime
if __name__ == '__main__':

    outlier = OutlierDetector(k = 2)
    zerospike = ZeroSpikeDetector()
    treshold = ThresholdDetector(threshold= 10)

    daty = [datetime.date(2022, 7, i) for i in range(1,11)]

    wartosci = [6.7, 10, None, 0, None, 26.67, 11.4, 9.6, 11, 19.245]
    wartosci_puste = []
    wartosci_none = [None,0,0,0.0, None, None, 0.0, 0, None, None,0,0,0,0,0,0,0]
    wartosci_ogromne = [10, 10, 10, -10000, 10, 10, 10, 10, 10, 10020]
    wartosc_pojedyncza = [2]

    seria1 = TimeSeries("NO2", "Rymarska20NO2_zwykledane","1h",daty, wartosci, "ug/m3")
    seria_puste = TimeSeries("H2O", "Krydusowo63_puste","24h", [], wartosci_puste, "gg/m3")    
    seria_none = TimeSeries("CO2", "Ulowo5_none_i 0","1h", daty, wartosci_none, "mg/cm3")
    seria_ogromne = TimeSeries("Ni" ,"Gruzja65_duze odchylenia","24h",daty, wartosci_ogromne, "g/m3")
    seria_pojedyncze = TimeSeries("Ni" ,"AAA_jedna wartosc w liscie","24h",[datetime.date(2020,2,2)], wartosc_pojedyncza, "g/m3")

    serie = [seria1, seria_puste, seria_none, seria_ogromne, seria_pojedyncze]
    for seria in serie:
        print(f"\n\n Seria {seria.kod_stacji} ")
        print(f"{outlier} analiza: {outlier.analyze(seria)}\n")
        print(f"{zerospike} analiza: {zerospike.analyze(seria)}\n")  
        print(f"{treshold} analiza: {treshold.analyze(seria)}\n")  