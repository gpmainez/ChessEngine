import sys

m1 = __import__('1_5')
m2 = __import__('6_10')
m3 = __import__('11_14')
m4 = __import__('17_20')

print("plik http_first_100k.log PRAWIDZIWE DANE\n")

try:
    with open('http_first_100k.log', 'r') as file:
        logs = m1.read_log(file)
    print(f"Sparsowano {len(logs)} wpisow.")
except FileNotFoundError:
    print("Blad: Nie znaleziono pliku")
    sys.exit()


print("\n- Zad 7 Top 5 adresow IP")
top_ips = m2.get_top_ips(logs, 5)
for ip, count in top_ips:
    print(f"IP: {ip} -> {count} zapytan")

print("\n Zad 12 Rozklad kodow HTTP ")
status_classes = m3.count_status_classes(logs)
print(status_classes)

print("\n Zad 18: Podejrzane IP (prog 1000 zapytan") 
sus_ips = m4.detect_sus(logs, 1000)
print(sus_ips)

print("\n Zad 20: Pelna mini analiza logu")
analiza = m4.analyze_log(logs)
print("Najczestsze IP:", analiza.get("top_ip"))
print("Najczestsze URI:", analiza.get("top_uri"))
print("Liczba bledow (4xx, 5xx):", analiza.get("error_count"))
print("Unikalne sesje:", analiza.get("unique_sessions"))