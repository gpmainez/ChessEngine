import csv


def parse_file(filename):
    data = []
    with open(filename, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:

            id = row['Nr']
            code = row['Kod stacji']
            inter_code = row['Kod międzynarodowy']
            print(id, code, inter_code)
            print("________________")

            data.append(row)

    return data
if __name__ == '__main__':
    data = parse_file('stacje.csv')
