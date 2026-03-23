
def get_top_uris(log, n=10):
    if not isinstance(log, list) or not isinstance(n, int) or n <= 0:
        return []

    uri_counts = {}
    for entry in log:
        try:
            uri = entry[8]
            if isinstance(uri, str):
                uri_counts[uri] = uri_counts.get(uri, 0) + 1
        except IndexError:
            continue

    sorted_uris = sorted(uri_counts.items(), key=lambda item: item[1], reverse=True)
    return sorted_uris[:n]


def count_status_classes(log):
    if not isinstance(log, list):
        return {}

    classes = {}
    for entry in log:
        try:
            code = entry[9]
            if isinstance(code, int):
                if 200 <= code < 300:
                    classCode = "2xx"
                elif 300 <= code < 400:
                    classCode = "3xx"
                elif 400 <= code < 500:
                    classCode = "4xx"
                elif 500 <= code < 600:
                    classCode = "5xx"
                else:
                    continue

                classes[classCode] = classes.get(classCode, 0) + 1
        except IndexError:
            continue

    return classes

def entry_to_dict(entry):
    if not isinstance(entry, tuple) or len(entry) < 10:
        return {}

    return {
        "ts": entry[0],
        "uid": entry[1],
        "orig_ip": entry[2],
        "orig_port": entry[3],
        "resp_ip": entry[4],
        "resp_port": entry[5],
        "method": entry[6],
        "host": entry[7],
        "uri": entry[8],
        "status": entry[9]
    }

def log_to_dict(log):
    if not isinstance(log, list):
        return {}

    sessions = {}
    for entry in log:
        entry_dict = entry_to_dict(entry)

        if not entry_dict:
            continue

        uid = entry_dict.get("uid")

        if uid not in sessions:
            sessions[uid] = []

        sessions[uid].append(entry_dict)

    return sessions



if __name__ == '__main__':
    import datetime

    t1 = datetime.datetime.fromtimestamp(1000)
    t2 = datetime.datetime.fromtimestamp(2000)

    # (ts, uid, id_orig_h, id_orig_p, id_resp_h, id_resp_p, method, host, uri, status_code)
    test_logs = [
        (t1, "ula", "26.26.26.26", 123, "10.0.0.1", 80, "GET", "firma.pl", "/index.html", 200),
        (t1, "ula", "26.26.26.26", 124, "10.0.0.1", 80, "GET", "firma.pl", "/style.css", 200),
        (t2, "gaba", "67.67.67.67", 125, "10.0.0.1", 80, "POST", "gaba.com", "/dane", 404),
        (t2, "adrian", "67.67.67.67", 126, "10.0.0.1", 80, "GET", "gaba.com", "/index.html", 500),
        (t2, "wyrus", "26.26.26.26", 127, "10.0.0.1", 80, "HEAD", "firma.pl", "/kreda.jpg", 301),
    ]

    print("Zad 11 - 14\n")

    print("Zad 11 Najczestsze URI:")
    top_uris = get_top_uris(test_logs, 2)
    print("Top 2 URI:", top_uris)
    print("Czy /index.html wygrywa (2 wystapienia):", top_uris[0][0] == "/index.html")
    print("Zle dane n=0:", get_top_uris(test_logs, 0))

    print("\nZad 12 Rozklad kodow HTTP:")
    classes = count_status_classes(test_logs)
    print("Klasy statusow:", classes)
    print("Czy 2xx ma 2 wystapienia:", classes.get("2xx") == 2)
    print("Czy 4xx ma 1 wystapienie:", classes.get("4xx") == 1)

    print("\nZad 13 Zamien krotke na slownik:")
    entry_dict = entry_to_dict(test_logs[0])
    print("Pojedynczy wpis slownika ula:", entry_dict)
    print("Czy poprawnie zmapowalo uid:", entry_dict.get("uid") == "ula")
    print("Pusta lub zla krotka:", entry_to_dict(("zla_krotka",)))

    print("\nZad 14 Zamien log na slownik sesji:")
    sessions = log_to_dict(test_logs)
    print("Klucze sesji (uid):", list(sessions.keys()))
    print("Czy ula ma 2 wpisy w liscie:", len(sessions.get("ula", [])) == 2)
    print("Czy gaba ma 1 wpis:", len(sessions.get("gaba", [])) == 1)
    print("Zle dane wejsciowe:", log_to_dict("to nie jest lista"))