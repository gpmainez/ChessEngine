import csv


def parse_file(filename):
    data = []
    with open(filename, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            # debug na wszelki niech zostanie
            # kurcznie neiw idzlaem ze python ma tak przyjemny strumien albo to format pliku chuj wi tbh
            #uwierz lub nie ale tez jak korzystasz z biblioteki pandas to normalnie mozesz jak w R dataframe i tez gra OLA OLA EJ!
            id = row['Nr']
            code = row['Kod stacji']
            inter_code = row['Kod międzynarodowy']
            print("bible date could be us\n")
            print(id, code, inter_code)
            print("________________")

            data.append(row)

    return data
if __name__ == '__main__':
    data = parse_file('stacje.csv')
