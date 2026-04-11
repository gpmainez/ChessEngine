import csv
import re


def get_adresses(path, city):
    adresses = []

    with open(path, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        pattern = re.compile(r"^(.*?)\s+(\d+[a-zA-Z]*)$")

        for row in reader:
            if row["Miejscowość"] == city:
                wojew = row["Województwo"]
                adres = row["Adres"]

                if adres != "":
                    result = pattern.search(adres)

                    if result:
                        street = result.group()[1]
                        number = result.group()[2]
                    else:
                        street = adres
                        number = ""
                else:
                    street = ""
                    number = ""

                mytuple = (wojew, city, street, number)

                adresses.append(mytuple)

    return adresses


my_list = get_adresses("stacje.csv", "Głogów")
num = 0

for i in my_list:
    num += 1
    print(f"num: {num} add: {i}")
