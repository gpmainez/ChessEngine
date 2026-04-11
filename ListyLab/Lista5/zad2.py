import os
import re
from pathlib import Path


def group_measurement_files_by_key(path):
    measurements = {}
    pattern = re.compile(r"(\d+)_([^_]+)_([^.]+)\.csv")

    for filename in os.listdir(path):
        if filename.endswith(".csv") and os.path.isfile(os.path.join(path, filename)):
            result = pattern.search(filename)

            if result:
                file_key = result.groups()
                value = Path(path) / filename

                measurements[file_key] = value

    return measurements

measurement_files = Path("measurements")
results = group_measurement_files_by_key(measurement_files)
num = 0

for key, path in results.items():
    num += 1
    print(f"num: {num} k: {key} |||| f: {path}")
