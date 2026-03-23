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
