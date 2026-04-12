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

                result = pattern.search(adres)

                if result:
                    street = result.group()[1]
                    number = result.group()[2]
                else:
                    street = adres
                    number = ""

                mytuple = (wojew, city, street, number)
                adresses.append(mytuple)

        return adresses

if __name__ == '__main__':
    my_list = get_adresses("stacje.csv", "Solec Zdrój")
    num = 0

    for i in my_list:
        num += 1
        print(f"num: {num} add: {i}")
