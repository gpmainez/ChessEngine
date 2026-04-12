import csv
import io
from collections import defaultdict
from datetime import datetime

def read_gios_csv(filepath_or_buffer):

    measurements = []
    stations = []
    parameters = []

    if isinstance(filepath_or_buffer, str):
        f = open(filepath_or_buffer, 'r', encoding='utf-8')
    else:
        f = filepath_or_buffer  #testy ze zmiennej tekstowej

    reader = csv.reader(f)

    for row in reader:
        if not row:
            continue

        header = row[0]

        if header == "Kod stacji":
            stations = row[1:]
        elif header == "Wskaźnik":
            parameters = row[1:]
        elif header in ["Nr", "Czas uśredniania", "Jednostka", "Kod stanowiska"]:
            continue
        else:
            timestamp = header
            values = row[1:]

            for i, val in enumerate(values):
                if i < len(stations):
                    station = stations[i]
                    param = parameters[i] if i < len(parameters) else "Nieznany"
                    measurements.append((timestamp, val.strip(), station, param))

    if isinstance(filepath_or_buffer, str):
        f.close()

    return measurements


def detect_anomalies(measurements, jump_threshold=2.0, alarm_threshold=5.0, max_invalid_ratio=0.2):
    grouped_data = defaultdict(list)
    for time_str, val, station, param in measurements:
        grouped_data[(station, param)].append((time_str, val))

    anomalies = []

    for (station, param), data in grouped_data.items():
        try:
            data.sort(key=lambda x: datetime.strptime(x[0], "%m/%d/%y %H:%M"))
        except ValueError:
            data.sort(key=lambda x: x[0])

        invalid_count = 0
        total_count = len(data)

        for i in range(total_count):
            time_str, val = data[i]

            if val is None or val == "":
                invalid_count += 1
                continue

            try:
                val_float = float(val)
            except ValueError:
                invalid_count += 1
                continue

            #niepoprwane wartosci
            if val_float <= 0:
                invalid_count += 1
                anomalies.append({
                    "type": "wrong value", "station": station, "time": time_str,
                    "msg": f"suspicious value: {val_float} (zbyt niska/ujemna)."
                })
                continue

            #nagle skoki wartosci (szukodzenie czujnika)
            if i > 0:
                prev_time, prev_val = data[i - 1]
                if prev_val not in (None, "") and float(prev_val) > 0:
                    delta = abs(val_float - float(prev_val))
                    if delta > jump_threshold:
                        anomalies.append({
                            "type": "SKOK", "station": station, "time": time_str,
                            "msg": f"Nagły skok o {delta:.2f} (z {float(prev_val):.2f} na {val_float:.2f})."
                        })

            #prog alarmowy (jakis tam trheshold)
            if val_float > alarm_threshold:
                #tylko unikalne zmiany (pomiar moze byc taki sam przez tydzien jesli meirzony jest raz na tydzien)
                if i == 0 or float(data[i - 1][1] or 0) != val_float:
                    anomalies.append({
                        "type": "ALARM", "station": station, "time": time_str,
                        "msg": f"Przekroczono próg: {val_float} > {alarm_threshold} dla {param}."
                    })



        #uszkodzony czujnik
        if total_count > 0:
            invalid_ratio = invalid_count / total_count
            if invalid_ratio >= max_invalid_ratio:
                anomalies.append({
                    "type": "Error czujnik", "station": station, "time": "",
                    "msg": f"Zbyt wiele braków: {invalid_ratio * 100:.1f}% pomiarów odrzucono ({invalid_count}/{total_count})."
                })

    return anomalies



def uruchom_testy():

    dane_csv = """Nr,1,2,3,4,5
Kod stacji,DsGlogWiStwo,DsLegAlRzecz,DsOsieczow21,DsPolKasztan,DsWalbrzWyso
Wskaźnik,As(PM10),As(PM10),As(PM10),As(PM10),As(PM10)
Czas uśredniania,24g,24g,24g,24g,24g
Jednostka,ng/m3,ng/m3,ng/m3,ng/m3,ng/m3
Kod stanowiska,DsGlogWiStwo-As(PM10)-24g,DsLegAlRzecz-As(PM10)-24g,DsOsieczow21-As(PM10)-24g,DsPolKasztan-As(PM10)-24g,DsWalbrzWyso-As(PM10)-24g
01/01/23 12:00,1.57,13.38,0.79,1.78,1.02
01/02/23 12:00,5.93,3.79,1.81,3.2,0.5
01/03/23 12:00,5.93,3.79,1.81,3.2,
01/04/23 12:00,,3.79,1.81,3.2,0.5
01/05/23 12:00,1.8,7.78,2.08,3.44,0.5"""

    pomiary = read_gios_csv(io.StringIO(dane_csv))
    print(f"test {len(pomiary)} pomiarów. Przykładowy: {pomiary[0]}\n")

    print("anomalies: ")
    wyniki = detect_anomalies(pomiary, jump_threshold=3.0, alarm_threshold=10.0)



    file = "measurements/2023_As(PM10)_24g.csv"
    readings = read_gios_csv(file)

    wynik2 = detect_anomalies(readings, jump_threshold=15.0, alarm_threshold=25.0)

    for idx, anomalia in enumerate(wyniki, 1):
        print(f"{idx}. [{anomalia['type']}] {anomalia['station']} | {anomalia['time']}")
        print(f"   -> {anomalia['msg']}")

    print("______________________________________")
    print("test with example values: \n")

    for idx, anomalia in enumerate(wynik2, 1):
        print(f"{idx}. [{anomalia['type']}] {anomalia['station']} | {anomalia['time']}")
        print(f"   -> {anomalia['msg']}")


uruchom_testy()