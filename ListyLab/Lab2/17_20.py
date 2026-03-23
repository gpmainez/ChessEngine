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

    ip_counts = {}

    for entry in log:
        try:
            ip = entry[2]

            if not isinstance(ip, str):
                continue

            ip_counts[ip] = ip_counts.get(ip, 0) + 1

        except IndexError:
            continue

    sus_ips = []
    for ip, count in ip_counts.items():

        if count >= threshold:
            sus_ips.append(ip)

    return sus_ips

#alternatywa dla tego def_sus
# def detect_sus(log, threshold):
#     if not isinstance(log, list) or not isinstance(threshold, (int, float)) or threshold <= 0:
#         return []
#
#     ip_stats = {}
#
#     for entry in log:
#         try:
#             ip = entry[2]
#             status = entry[9]
#
#             if not isinstance(ip, str):
#                 continue
#
#             if ip not in ip_stats:
#                 ip_stats[ip] = {'total': 0, 'errors_404': 0}
#
#             ip_stats[ip]['total'] += 1
#             if status == 404:
#                 ip_stats[ip]['errors_404'] += 1
#
#         except IndexError:
#             continue

    sus_ips = []
    for ip, stats in ip_stats.items():
        if stats['total'] >= threshold or stats['errors_404'] >= (threshold / 2):
            sus_ips.append(ip)

    return sus_ips
