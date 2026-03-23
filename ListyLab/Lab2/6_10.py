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


