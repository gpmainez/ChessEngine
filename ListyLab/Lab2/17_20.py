def get_session_paths(log):
    if not isinstance(log, list):
        return {}

    paths = {}
    for entry in log:
        try:
            uid = entry[1]
            uri = entry[8]

            if not isinstance(uid, str) or not isinstance(uri, str):
                continue

            if uid not in paths:
                paths[uid] = []

            paths[uid].append(uri)

        except IndexError:
            continue

    return paths




def detect_sus(log, threshold):
     if not isinstance(log, list) or not isinstance(threshold, (int, float)) or threshold <= 0:
         return []

     ip_stats = {}

     for entry in log:
         try:
             ip = entry[2]
             status = entry[9]

             if not isinstance(ip, str):
                 continue

             if ip not in ip_stats:
                 ip_stats[ip] = {'total': 0, 'errors_404': 0}

             ip_stats[ip]['total'] += 1
             if status == 404:
                 ip_stats[ip]['errors_404'] += 1

         except IndexError:
             continue

     sus_ips = []
     for ip, stats in ip_stats.items():
         if stats['total'] >= threshold or stats['errors_404'] >= (threshold / 2):
             sus_ips.append(ip)

     return sus_ips


def get_extension_stats(log):
    if not isinstance(log, list):
        return {}

    stats = {}
    for entry in log:
        try:
            uri = entry[8]
            
            if not isinstance(uri, str):
                continue
            clean_uri = uri.split('?')[0]
            path_parts = clean_uri.split('/')
            last_part = path_parts[-1] if path_parts else ""

            if '.' in last_part:
                ext = last_part.split('.')[-1].lower()
                
                if ext.isalnum() and len(ext) < 10:
                    stats[ext] = stats.get(ext, 0) + 1

        except IndexError:
            continue

    return stats

def analyze_log(log):
    """dodatkowe funkcje zaproponowane przez nas to zliczanie requestow oraz liczenie unikalnych sesji """
    if not isinstance(log, list) or len(log) == 0:
        return {}

    ip_counts = {}
    uri_counts = {}
    method_counts = {}
    error_count = 0
    unique_uids = set()

    for entry in log:
        try:
            uid = entry[1]
            ip = entry[2]
            method = entry[6]
            uri = entry[8]
            status = entry[9]

            if isinstance(ip, str):
                ip_counts[ip] = ip_counts.get(ip, 0) + 1

            if isinstance(uri, str):
                uri_counts[uri] = uri_counts.get(uri, 0) + 1

            if isinstance(method, str):
                method_counts[method] = method_counts.get(method, 0) + 1

            if isinstance(status, int) and status >= 400:
                error_count += 1

            if isinstance(uid, str):
                unique_uids.add(uid)

        except IndexError:
            continue

    top_ip = max(ip_counts, key=ip_counts.get) if ip_counts else None
    top_uri = max(uri_counts, key=uri_counts.get) if uri_counts else None

    return {
        "top_ip": top_ip,
        "top_uri": top_uri,
        "method_distribution": method_counts,
        "error_count": error_count,
        "total_requests": len(log),
        "unique_sessions": len(unique_uids)
    }




if __name__ == '__main__':
    import datetime

    t = datetime.datetime.fromtimestamp(1000)

    # (ts, uid, id_orig_h, id_orig_p, id_resp_h, id_resp_p, method, host, uri, status_code)
    test_logs = [
        (t, "ula", "26.26.26.26", 123, "10.0.0.1", 80, "GET", "firma.pl", "/index.html", 200),
        (t, "ula", "26.26.26.26", 124, "10.0.0.1", 80, "GET", "firma.pl", "/style.css", 200),
        (t, "ula", "26.26.26.26", 125, "10.0.0.1", 80, "GET", "firma.pl", "/tajne.txt", 404),
        (t, "ula", "26.26.26.26", 126, "10.0.0.1", 80, "GET", "firma.pl", "/admin.php", 404),
        (t, "gaba", "67.67.67.67", 127, "10.0.0.1", 80, "POST", "gaba.com", "/dane.json", 500),
        (t, "adrian", "1.1.1.1", 128, "10.0.0.1", 80, "GET", "host.pl", "/kreda.jpg?size=26", 200)
    ]

    print("Zad 17 - 20\n")

    print("Zad 17 Odtwarzanie sesji uzytkownika:")
    paths = get_session_paths(test_logs)
    print("Sciezki ula:", paths.get("ula"))
    print("Czy ula ma 4 sciezki:", len(paths.get("ula", [])) == 4)
    print("Zle dane:", get_session_paths({}))

    print("\nZad 18 Podejrzane IP:")
    # ula (26.26.26.26) ma 4 zapytania w tym dwa 404.
    # Przy progu 4 zlapie sie z obu warunkow (total >= 4 oraz 404 >= 2)
    sus = detect_sus(test_logs, 4)
    print("Podejrzane IP (prog 4):", sus)
    print("Czy 26.26.26.26 jest podejrzane:", "26.26.26.26" in sus)
    print("Zle dane (ujemny prog):", detect_sus(test_logs, -1))

    print("\nZad 19 Rozklad rozszerzen plikow:")
    ext_stats = get_extension_stats(test_logs)
    print("Statystyki rozszerzen:", ext_stats)
    print("Czy html wystapil 1 raz:", ext_stats.get("html") == 1)
    print("Czy wycieto kreda.jpg ignorujac parametry:", ext_stats.get("jpg") == 1)
    print("Pusta lista:", get_extension_stats([]))

    print("\nZad 20 Mini analiza logu:")
    analiza = analyze_log(test_logs)
    print("Wynik analizy:", analiza)
    print("Czy top IP to 26.26.26.26:", analiza.get("top_ip") == "26.26.26.26")
    print("Czy zliczono 3 bledy (dwa 404, jedno 500):", analiza.get("error_count") == 3)
    print("Zle dane wejsciowe:", analyze_log("error"))