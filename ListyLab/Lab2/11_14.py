
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

