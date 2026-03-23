
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


