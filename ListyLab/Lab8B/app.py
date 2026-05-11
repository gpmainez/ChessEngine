import datetime
import sys
from typing import Optional, List

from ListyLab.Lab8B.parser import HttpLogParse, parse_log


class appLogic:

    def __init__(self):

        self.logs: List[HttpLogParse] = []
        self.all_logs: List[HttpLogParse] = []

    def load_logs_to_app(self, filepath: str) -> None:

        self.all_logs.clear()
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                entry = parse_log(line)
                if entry:
                    self.all_logs.append(entry)
        self.logs = self.all_logs.copy()

    def get_index_log(self, index: int) -> Optional[HttpLogParse]:
        if 0 <= index < len(self.logs):
            return self.logs[index]
        return None

    def filter_date(self, start_dt: datetime, end_dt: datetime):
        self.logs = [log for log in self.all_logs if start_dt <= log.timestamp <= end_dt]
