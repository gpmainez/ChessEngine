import csv
import re
from datetime import datetime
from pathlib import Path
from unittest import result


def get_dates(path):
    with open(path, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        pattern = re.compile(r"^(\d{4})-(\d{2})-(\d{2})$")

        output = set()

        for row in reader:
            date = row["Data uruchomienia"]
            close_date = row["Data zamknięcia"]

            for d in (date, close_date):
                if d and pattern.search(d):
                    try:
                        datetime.strptime(d, "%Y-%m-%d")
                        output.add(d)
                    except ValueError:
                        pass

        return output


def get_locations(path):
    with open(path, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        pattern = re.compile(r"^-?\d+\.\d{6}$")
        locations = []

        for row in reader:
            lat_str = row["WGS84 φ N"]
            lon_str = row["WGS84 λ E"]

            if lon_str and lat_str and pattern.match(lat_str) and pattern.match(lon_str):
                lat = float(lat_str)
                lon = float(lon_str)

                if -90.0 <= lat <= 90.0 and -180.0 <= lon <= 180.0:
                    locations.append((lat, lon))

        return locations


def get_werid_name_stations(path):
    with open(path, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        pattern = re.compile(r"^[^-]+-[^-]+$")

        stations = []
        for row in reader:
            name = row["Nazwa stacji"]
            if name and pattern.match(name):
                result = pattern.search(name)
                if result:
                    stations.append(result.group())

        return stations


def change_spaces(path):
    with open(path, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        dict = {
            'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l', 'ń': 'n', 'ó': 'o', 'ś': 's', 'ź': 'z', 'ż': 'z',
            'Ą': 'A', 'Ć': 'C', 'Ę': 'E', 'Ł': 'L', 'Ń': 'N', 'Ó': 'O', 'Ś': 'S', 'Ź': 'Z', 'Ż': 'Z'
        }
        pattern = re.compile(r"\s+")

        pattern_dict = re.compile(r"[ąćęłńóśźżĄĆĘŁŃÓŚŹŻ]")

        cleaned_stations = []

        for row in reader:
            name = row["Nazwa stacji"]
            if name:
                name = pattern.sub("_", name)
                name = pattern_dict.sub(lambda match: dict[match.group()], name)
                cleaned_stations.append(name)

    return cleaned_stations


def mob_ending_stations(path):
    with open(path, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        pattern = re.compile(r"MOB$")
        pattern_type = re.compile(r"mobilna")

        stations = []
        for row in reader:
            id = row["Nr"]
            code = row["Kod stacji"]
            typee = row["Rodzaj stacji"]
            if code and typee:
                code_result = pattern.search(code)
                typee_result = pattern_type.search(typee)

            if code_result:

                if not typee_result:
                    mytuple = (id, code, typee)
                    stations.append(mytuple)

        if len(stations) != 0:
            print(stations)
            return False
        return True


def separated_locations(path):
    with open(path, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        pattern = re.compile(r"^[^-]+\s+-\s+[^-]+\s+-\s+[^-]+$")

        stations = []
        for row in reader:
            name = row["Nazwa stacji"]

            if name and pattern.match(name):
                stations.append(name.strip())

        return stations


def stacje_z_ulica(path):
    with open(path, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        pattern = re.compile(r",\s*(ul|al)\.", re.IGNORECASE)

        stations = []
        for row in reader:
            name = row["Nazwa stacji"]

            if name and pattern.search(name):
                stations.append(name.strip())

        return stations
