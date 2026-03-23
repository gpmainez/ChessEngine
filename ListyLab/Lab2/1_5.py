import sys
import datetime


def read_log(input_stream=None):
    if input_stream is None:
        input_stream = sys.stdin

    parsed_logs = []

    for line in input_stream:
        line = line.strip()

        if not line or line.startswith('#'):
            continue

        parts = line.split('\t')

        if len(parts) < 15:
            continue

        try:
            ts_float = float(parts[0])
            ts = datetime.datetime.fromtimestamp(ts_float)

            uid = parts[1]
            id_orig_h = parts[2]
            id_orig_p = int(parts[3])
            id_resp_h = parts[4]
            id_resp_p = int(parts[5])
            method = parts[7]
            host = parts[8]
            uri = parts[9]

            status_code = parts[14]
            status_code = int(status_code) if status_code != '-' else 0

            entry = (ts, uid, id_orig_h, id_orig_p, id_resp_h, id_resp_p, method, host, uri, status_code)
            parsed_logs.append(entry)

        except ValueError:
            continue

    return parsed_logs


def sort_log(log, index):
    if not isinstance(log, list):
        return []
    try:
        return sorted(log, key=lambda x: x[index])
    except IndexError:
        return log


def get_entries_by_code(log, code):
    if not isinstance(log, list):
        return []
    try:
        target_code = int(code)
    except (ValueError, TypeError):
        return []

    return [entry for entry in log if entry[9] == target_code]


def is_valid_ipv4(ip_str):
    parts = ip_str.split('.')
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isdigit() or not (0 <= int(part) <= 255):
            return False
    return True


def get_entries_by_addr(log, addr):
    if not isinstance(log, list):
        return []

    is_ip = is_valid_ipv4(addr)

    if is_ip:
        return [entry for entry in log if entry[2] == addr]
    else:
        return [entry for entry in log if entry[7] == addr]


def get_failed_reads(log, merge = False):
    if not isinstance(log, list):
        return [] if merge else ([], [])

    list_4xx = []
    list_5xx = []
    for entry in log:
        code = entry[9]
        if isinstance(code, int):
            if 400 <= code < 500:
                list_4xx.append(entry)
            elif 500 <= code < 600:
                list_5xx.append(entry)

    if merge:
        return list_4xx + list_5xx
    else:
        return list_4xx, list_5xx




if __name__ == '__main__':
    import io

    mock_raw_data = """1331901000.000000	CHEt7z3AzG4gyCNgci	192.168.202.79	50465	192.168.229.251	80	1	HEAD	192.168.229.251	/DEASLog02.nsf	-	Mozilla/5.0	0	0	404	Not Found	-	-	-	(empty)	-	-	-	-	-	-	-
1331901000.010000	CKnDAp2ohlvN6rpiXl	192.168.202.80	50467	192.168.229.251	80	1	GET	host.pl	/index.html	-	Mozilla/5.0	0	0	200	OK	-	-	-	(empty)	-	-	-	-	-	-	-
1331901000.030000	CNTrjn42F3LB58MZH6	192.168.202.79	50469	192.168.229.251	80	1	POST	192.168.229.251	/DEASLog04.nsf	-	Mozilla/5.0	0	0	500	Server Error	-	-	-	(empty)	-	-	-	-	-	-	-
za_krotka_linia_ktora_powinna_zostac_pominieta_adrian_adrian
uszkodzony_timestamp	C1D7mK1PlzKEnEyG03	192.168.202.79	50471	192.168.229.251	80	1	HEAD	192.168.229.251	/DEASLog05.nsf	-	Mozilla/5.0	0	0	404	Not Found	-	-	-	(empty)	-	-	-	-	-	-	-
1331901000.050000	CGF1bVMyl9ALKI32l	192.168.202.79	50473	192.168.229.251	80	1	HEAD	192.168.229.251	/DEASLog.nsf	-	Mozilla/5.0	0	0	404	Not Found	-	-	-	(empty)	-	-	-	-	-	-	-"""

    print("Zad 1 - 5")
    
    mock_stream = io.StringIO(mock_raw_data)
    
    print("\nZad 1 Czytanie logow: ")
    parsed = read_log(mock_stream)
    print("Sparsowano wpisow (powinny byc 4 poprawne):", len(parsed))
    if parsed:
        print("Pierwszy element (uid):", parsed[0][1])

    print("\nZad 2 Sortowanie po kodzie statusu, index 9:")
    # powinno rzucic 200
    sorted_logs = sort_log(parsed, 9)
    print("Pierwszy kod na liście po posortowaniu: ", sorted_logs[0][9])
    print("Pusta lista wejściowa: ", sort_log([], 9))
    print("Zly index (99) wyrzuca blad =  zwraca oryginal:", len(sort_log(parsed, 99)) == 4)

    print("\nZad 3 Filtrowanie po kodzie HTTP:")
    print("Kody 200 int: ", len(get_entries_by_code(parsed, 200)))
    print("Kody 404 str, test polimorfizmu:", len(get_entries_by_code(parsed, "404")))
    print("Zly kod wejsciowy (napis):", get_entries_by_code(parsed, "dwiescie"))

    print("\nZad 4 Filtrowanie po adresie IP/hosta:")
    print("IP 192.168.202.79 (3 wpisy):", len(get_entries_by_addr(parsed, "192.168.202.79")))
    print("Host 'host.pl' (1 wpis):", len(get_entries_by_addr(parsed, "host.pl")))
    print("Nieistniejacy host:", get_entries_by_addr(parsed, "GABAGABAGABA.com"))

    print("\nZad 5 Bledy 4__ i 5__:")
    # sa 2x 404 i 1x 500
    merged = get_failed_reads(parsed, merge=True)
    print("Polaczone listy (powinny byc 3):", len(merged))
    
    list_4, list_5 = get_failed_reads(parsed, merge=False)
    print("Rozdzielone - klasa 4__:", len(list_4))
    print("Rozdzielone - klasa 5__:", len(list_5))
    print("Pusta lista logow:", get_failed_reads([]))