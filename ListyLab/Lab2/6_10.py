import datetime

def get_entries_by_extension(log, ext):
    if not isinstance(log, list) or not isinstance(ext, str):
        return []

    ext = ext.lstrip('.')

    filtered_log = []
    for entry in log:
        uri = entry[8]

        if not isinstance(uri, str):
            continue

        clean_uri = uri.split('?')[0]

        if clean_uri.endswith('.' + ext):
            filtered_log.append(entry)

    return filtered_log

def get_top_ips(log, n = 10):
    if not isinstance(log, list) or not isinstance(n, int) or n <= 0:
        return []

    ip_counts = {}
    for entry in log:
        try:
            ip = entry[2]
            ip_counts[ip] = ip_counts.get(ip, 0) + 1
        except IndexError:
            continue

    sorted_ips = sorted(ip_counts.items(), key=lambda item: item[1], reverse=True)
    return sorted_ips[:n]

def get_unique_methods(log):
    if not isinstance(log, list):
        return []

    methods = set()
    for entry in log:
        try:
            m = entry[6]
            if isinstance(m, str):
                methods.add(m)
        except IndexError:
            continue

    return list(methods)


def get_entries_in_time_range(log, start, end):
    if not isinstance(log, list):
        return []

    if not isinstance(start, datetime.datetime) or not isinstance(end, datetime.datetime):
        return []

    return [
        entry for entry in log
        if isinstance(entry[0], datetime.datetime) and start <= entry[0] < end
    ]


def count_by_method(log):
    if not isinstance(log, list):
        return {}

    method_counts = {}
    for entry in log:
        try:
            method = entry[6]
            if isinstance(method, str):
                method_counts[method] = method_counts.get(method, 0) + 1
        except IndexError:
            continue

    return method_counts



if __name__ == '__main__':
    import datetime

    t1 = datetime.datetime.fromtimestamp(1000)
    t2 = datetime.datetime.fromtimestamp(2000)
    t3 = datetime.datetime.fromtimestamp(3000)

    # (ts, uid, id_orig_h, id_orig_p, id_resp_h, id_resp_p, method, host, uri, status_code)
    test_logs = [
        (t1, "ula", "26.26.26.26", 123, "10.0.0.1", 80, "GET", "firma.pl", "/index.html", 200),
        (t2, "gaba", "26.26.26.26", 124, "10.0.0.1", 80, "GET", "gaba.com", "/kreda.jpg?size=26", 200),
        (t2, "adrian", "67.67.67.67", 125, "10.0.0.1", 80, "POST", "firma.pl", "/dane", 201),
        (t3, "kreda", "26.26.26.26", 126, "10.0.0.1", 80, "HEAD", "gaba.com", "/style.css", 200),
        (t3, "wyrus", "67.67.67.67", 127, "10.0.0.1", 80, "GET", "firma.pl", "/adrian", 404),
    ]

    print("Zad 6 - 10\n")

    print("Zad 6 Filtrowanie po rozszerzeniu:")
    print("Rozszerzenie 'jpg':", len(get_entries_by_extension(test_logs, "jpg")) == 1)
    print("Rozszerzenie '.html' (kropka w argumencie):", len(get_entries_by_extension(test_logs, ".html")) == 1)
    print("Nieistniejace 'php':", get_entries_by_extension(test_logs, "php"))
    print("Zly typ argumentu (np int):", get_entries_by_extension(test_logs, 123))

    print("\nZad 7 Najczestsze adresy IP:")
    top_ips = get_top_ips(test_logs, n=2)
    print("Top 2 IP:", top_ips)
    print("Czy 26.26.26.26 ma 3 wystapienia?", top_ips[0][1] == 3)
    print("Zle dane n=0:", get_top_ips(test_logs, 0))

    print("\nZad 8 Unikalne metody HTTP:")
    methods = get_unique_methods(test_logs)
    print("Lista metod:", methods)
    print("Ilosc unikalnych metod (powinny byc 3):", len(methods) == 3)
    print("Pusta lista wejsciowa:", get_unique_methods([]))

    print("\nZad 9 Zakres czasu:")
    start_time = datetime.datetime.fromtimestamp(1500)
    end_time = datetime.datetime.fromtimestamp(2500)
    in_range = get_entries_in_time_range(test_logs, start_time, end_time)
    print("Wpisy w przedziale t2 (powinny byc 2):", len(in_range))
    print("Puste lub zle typy dat:", get_entries_in_time_range(test_logs, "wczoraj", "dzisiaj"))

    print("\nZad 10 Liczba zapytan per metoda:")
    counts = count_by_method(test_logs)
    print("Slownik zliczen:", counts)
    print("Czy GET wystapil 3 razy?", counts.get("GET") == 3)
    print("Pusta lista:", count_by_method([]))