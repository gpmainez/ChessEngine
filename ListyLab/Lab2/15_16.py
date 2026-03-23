import datetime

def print_dict_entry_dates(log_dict):
    if not isinstance(log_dict, dict):
        print("err.")
        return

    for uid, entries in log_dict.items():
        req_count = len(entries)
        if req_count == 0:
            continue

        print(f"\n--- stats: {uid} ---")

        ips = set(e.get("orig_ip") for e in entries if e.get("orig_ip"))
        print(f"IP: {', '.join(ips)}")
        print(f"rq count: {req_count}")

        dates = [e.get("ts") for e in entries if isinstance(e.get("ts"), datetime.datetime)]
        if dates:
            print(f"first rq: {min(dates)}")
            print(f"last rq:  {max(dates)}")

        methods = [e.get("method") for e in entries if e.get("method")]
        method_counts = {}
        for m in methods:
            method_counts[m] = method_counts.get(m, 0) + 1

        print("% methods HTTP:")
        for m, count in method_counts.items():
            percentage = (count / req_count) * 100
            print(f"  - {m}: {percentage:.2f}%")

        codes_2xx = sum(1 for e in entries if isinstance(e.get("status"), int) and 200 <= e.get("status") < 300)
        ratio = codes_2xx / req_count
        print(f"2xx ratio: {ratio:.2f} ({codes_2xx}/{req_count})")

def get_most_active_session(log_dict):
    if not isinstance(log_dict, dict) or not log_dict:
        return None

    try:
        return max(log_dict, key=lambda uid: len(log_dict[uid]))
    except TypeError:
        return None



if __name__ == '__main__':

    t1 = datetime.datetime.fromtimestamp(1000)
    t2 = datetime.datetime.fromtimestamp(2000)
    t3 = datetime.datetime.fromtimestamp(3000)

    mock_log_dict = {
        "ula": [
            {"ts": t1, "orig_ip": "26.26.26.26", "method": "GET", "status": 200},
            {"ts": t2, "orig_ip": "26.26.26.26", "method": "POST", "status": 404}
        ],
        "ola": [
            {"ts": t1, "orig_ip": "67.67.67.67", "method": "GET", "status": 200},
            {"ts": t2, "orig_ip": "67.67.67.67", "method": "GET", "status": 200},
            {"ts": t3, "orig_ip": "67.67.67.67", "method": "HEAD", "status": 500}
        ],
        "adrian": [
            {"ts": t3, "orig_ip": "26.26.26.26", "method": "PUT", "status": 403}
        ]
    }

    print("Zad 15 - 16\n")

    print("Zad 15 Statystyki sesji:")

    print_dict_entry_dates(mock_log_dict)
    
    print("\n[Haczyki Zad 15 - puste i bledne dane]")
    print_dict_entry_dates({})
    print_dict_entry_dates("to_nie_jest_slownik")

    print("\nZad 16 Najaktywniejsza sesja:")
    active = get_most_active_session(mock_log_dict)
    print("Najaktywniejszy uid (powinna byc ola, bo ma 3 wpisy):", active)
    print("Czy poprawnie wybrano ola:", active == "ola")
    print("Pusty slownik:", get_most_active_session({}))
    print("Zly typ danych:", get_most_active_session(["brak", "danych"]))