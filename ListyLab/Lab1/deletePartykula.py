# import requests
#
# books = {
#     "opowiesc_wigilijna.txt" : "https://wolnelektury.pl/media/book/txt/dickens-opowiesc-wigilijna.txt",
#     "calineczka.txt": "https://wolnelektury.pl/media/book/txt/calineczka.txt",
#     "brzydkie_kaczatko.txt": "https://wolnelektury.pl/media/book/txt/brzydkie-kaczatko.txt",
#     "krasnoludki.txt": "https://wolnelektury.pl/media/book/txt/o-krasnoludkach-i-sierotce-marysi.txt",
#     "obrona_sokratesa.txt": "https://wolnelektury.pl/media/book/txt/obrona-sokratesa.txt"
# }
#
# for filename, url in books.items():
#     r = requests.get(url)
#
#     if r.status_code == 200:
#         with open(filename, "w", encoding="utf-8") as f:
#             f.write(r.text)
#         print(f"Pobrano: {filename}")
#     else:
#         print(f"Błąd pobierania {filename}: {r.status_code}")




import sys
import io

sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8")

def clean(line):
    return " ".join(line.strip().split())

def main():
    lines = sys.stdin.readlines()
    start = 0

    for i in range(min(10, len(lines)-1)):

        if lines[i].strip() == "" and lines[i+1].strip() == "":
            start = i + 2
            break

    for line in lines[start:]:
        if line.strip() == "":
            print()
        else:
            print(clean(line))

if __name__ == "__main__":
    main()



