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

        if len(parts) < 12:
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

            status_code = parts[11]
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


