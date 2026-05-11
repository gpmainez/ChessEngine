import sys
import datetime
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class HttpLogParse:
    url: str
    timestamp: datetime.datetime
    ip: str
    method: str
    host: str
    uri: str
    status: int

    def http_preview(self) -> str:
        if len(self.url) > 30:
            return self.url[:30] + "..."
        return self.url


def parse_log(line: str) -> Optional[HttpLogParse]:
    line = line.strip()
    if not line or line.startswith('#'):
        return None

    parts = line.split('\t')
    if len(parts) < 15:
        return None

    try:
        ts_float = float(parts[0])
        ts = datetime.datetime.fromtimestamp(ts_float)

        status_code = parts[14]
        status_code = int(status_code) if status_code != '-' else 0

        return HttpLogParse(
            url=line,
            timestamp=ts,
            ip=parts[2],
            method=parts[7],
            host=parts[8],
            uri=parts[9],
            status=status_code
        )
    except ValueError:
        return None