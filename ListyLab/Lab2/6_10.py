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


