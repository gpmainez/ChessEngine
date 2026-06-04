import os
import sys
import csv
import datetime
from models import init_db, Station, Rental, db

def main() -> None:
    if len(sys.argv) != 3:
        print("Użycie: python load_data.py |sciezka_do_csv| |nazwa_bazy|")
        sys.exit(1)

    csv_path: str = sys.argv[1]
    db_name: str = sys.argv[2]

    if not os.path.exists(csv_path):
        print("blad: podany plik csv nie istnieje")
        sys.exit(1)

    try:
        init_db(db_name)
        db.connect()
        db.create_tables([Station, Rental], safe=True)
    except Exception as e:
        print("blad: baza danych jest zablokowana lub brak dostepu")
        sys.exit(1)

  
    try:
        with open(csv_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
    except PermissionError:
        print("blad: plik csv jest zablokowany przez inny program")
        sys.exit(1)
    except Exception as e:
        print(f"blad odczytu pliku csv: {e}")
        sys.exit(1)

    # pobranie unikalnych nazw stacji
    station_names = set()
    for row in rows:
        st_wyn = row['Stacja wynajmu'].strip()
        st_zwr = row['Stacja zwrotu'].strip()
        if st_wyn:
            station_names.add(st_wyn)
        if st_zwr:
            station_names.add(st_zwr)

    #wstawienie stacji do bazy danych
    try:
        with db.atomic():
            for name in station_names:
                Station.get_or_create(station_name=name)
    except Exception as e:
        print("blad zapisu stacji: baza danych jest zablokowana")
        sys.exit(1)

    #  pobranie id stacji z bazy dla szybkiego mapowania
    station_map = {s.station_name: s.station_id for s in Station.select()}

    rentals = []
    for row in rows:
        try:
            start_time = datetime.datetime.strptime(row['Data wynajmu'].strip(), "%Y-%m-%d %H:%M:%S")
            end_time = datetime.datetime.strptime(row['Data zwrotu'].strip(), "%Y-%m-%d %H:%M:%S")
            
            rentals.append({
                'rental_id': int(row['UID wynajmu']),
                'bike_number': int(row['Numer roweru']),
                'start_time': start_time,
                'end_time': end_time,
                'rental_station': station_map[row['Stacja wynajmu'].strip()],
                'return_station': station_map[row['Stacja zwrotu'].strip()]
                
            })
        except Exception as e:
            print(f"Pominięto wiersz (błąd danych): {e}")

    # zbiorcze wstawienie rekordów wypozyczen, on_conflict_ignore zapobiega duplikatom
    batch_size = 500
    try:
        with db.atomic():
            for i in range(0, len(rentals), batch_size):
                Rental.insert_many(rentals[i:i+batch_size]).on_conflict_ignore().execute()
    except Exception as e:
        print("blad zapisu przejazdow: baza danych jest zablokowana")
        sys.exit(1)

    db.close()
    print(f"Zaimportowano {len(rentals)} wypozyczen")

if __name__ == "__main__":
    main()
