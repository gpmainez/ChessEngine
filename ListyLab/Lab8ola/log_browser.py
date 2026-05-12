import sys
import re
from datetime import datetime, date
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QFileDialog, QListWidget, QLabel,
    QDateEdit, QSpinBox, QFormLayout, QGroupBox, QSplitter, QMessageBox
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor


MONTHS_MAP = {
    "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4,
    "May": 5, "Jun": 6, "Jul": 7, 
    "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
}

TIMEZONES_MAP = {
    "+0000": "UTC", "+0100": "CET", "+0200": "EET","+0330": "IRST", "-0500": "EST", "-0400": "EDT",
    "-0800": "PST", "-0700": "PDT"
}

class LogEntry:
    
    def __init__(self, raw, host, date_str, time_str, timezone, method, resource, status, size):
        self.raw = raw
        self.host = host
        self.date_str = date_str
        self.time_str = time_str
        self.timezone = timezone
        self.method = method
        self.resource = resource
        self.status = status
        self.size = size
        
        # parsowanie daty i miesiaca
        try:
            day, month_str, year = date_str.split('/')
            self.date_obj = date(int(year), MONTHS_MAP.get(month_str, 1), int(day))
        except ValueError:
            #gdy cos nie tak ustawiamy dzisiejsza date
            self.date_obj = date.today()


class LogParser:

    def __init__(self):
        self.entries = []

    def load(self, path):
        self.entries = []
        try:
            with open(path, encoding="utf-8", errors="replace") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    entry = self._parse_line(line)
                    if entry:
                        self.entries.append(entry)
            return True, ""
        except Exception as e: #np nie ma dostepu do pliku
            return False, str(e)

    def _parse_line(self, line):
        try:
            # ip hosta to pierwszy wyraz
            host = line.split()[0]

            # data czas strefa — wewnatrz nawiasow kwadratowych
            bracket = re.search(r'\[(.+?)\]', line).group(1)  # 22/Jan/2019:03:56:20 +0330
            dt_part, timezone = bracket.split()                #rozdziela strefe czasowa od daty+czasu
            
            #zmiana kodu na nazwe
            timezone = TIMEZONES_MAP.get(timezone, timezone)
            
            date_str, time_str = dt_part.split(':',  1)        # data:czas

            # metoda i zasob sa wewnatrz ""
            request = re.search(r'"(.+?)"', line).group(1)     # GET /settings/logo HTTP/1.1
            parts = request.split()
            method = parts[0] # np GET
            resource = parts[1]

            # status i size to dwie liczby po zamknieciu cudzyslowu
            tail = line.split('"')[2].split()     #['200', '2244']
            status = int(tail[0])
            size = int(tail[1]) if tail[1] != '-' else 0

            return LogEntry(
                raw=line,
                host=host,
                date_str=date_str,
                time_str=time_str,
                timezone=timezone,
                method=method,
                resource=resource,
                status=status,
                size=size,
            )
        except (IndexError, AttributeError, ValueError):
            return None #jak cos jest nie tak to pomijamy

    def filter_by_date(self, from_date, to_date):
        return [e for e in self.entries if from_date <= e.date_obj <= to_date]

    def date_range(self):
        if not self.entries:
            return date.today(), date.today()
        dates = [e.date_obj for e in self.entries]
        return min(dates), max(dates)


class LogBrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.parser = LogParser()
        self.filtered = []  #aktualnie widoczne logi
        self._build_ui()
        self._connect_signals()

    def _build_ui(self):
        self.setWindowTitle("HTTP Log Browser")
        self.resize(960, 560)

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)

        #pasek pliku
        file_row = QHBoxLayout()
        self.path_edit = QLineEdit()
        self.path_edit.setReadOnly(True)
        self.path_edit.setPlaceholderText("Wybierz plik .log")
        self.open_btn = QPushButton("Open")
        file_row.addWidget(self.path_edit)
        file_row.addWidget(self.open_btn)
        root.addLayout(file_row)

        #filtry dat
        date_row = QHBoxLayout()
        date_row.addWidget(QLabel("From:"))
        self.date_from = QDateEdit()
        self.date_from.setCalendarPopup(True)
        date_row.addWidget(self.date_from)

        date_row.addWidget(QLabel("To:"))
        self.date_to = QDateEdit()
        self.date_to.setCalendarPopup(True)
        date_row.addWidget(self.date_to)
        date_row.addStretch()
        root.addLayout(date_row)

        #master detail
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # master - lista
        self.log_list = QListWidget()
        splitter.addWidget(self.log_list)

        # detail -formularz
        detail_box = QGroupBox("Details")
        form = QFormLayout(detail_box)

        self.det_host = QLineEdit(); self.det_host.setReadOnly(True)
        self.det_date = QLineEdit(); self.det_date.setReadOnly(True)
        self.det_time = QLineEdit(); self.det_time.setReadOnly(True)
        self.det_tz   = QLineEdit(); self.det_tz.setReadOnly(True)
        self.det_method = QLineEdit(); self.det_method.setReadOnly(True)
        self.det_resource = QLineEdit(); self.det_resource.setReadOnly(True)

        self.det_status = QSpinBox()
        self.det_status.setReadOnly(True)
        self.det_status.setButtonSymbols(QSpinBox.ButtonSymbols.NoButtons)
        self.det_status.setRange(0, 999)

        self.det_size = QLineEdit()
        self.det_size.setReadOnly(True)

        form.addRow("Remote host:", self.det_host)
        form.addRow("Date:", self.det_date)
        form.addRow("Time:", self.det_time)
        form.addRow("Timezone:", self.det_tz)
        form.addRow("Method:", self.det_method)
        self.det_status_layout = QHBoxLayout()
        self.det_status_layout.setContentsMargins(0, 0, 0, 0)
        self.det_status_dot = QLabel()
        self.det_status_dot.setFixedSize(14, 14)
        self.det_status_dot.setStyleSheet("background-color: transparent; border-radius: 7px;")
        
        self.det_status_layout.addWidget(self.det_status)
        self.det_status_layout.addWidget(self.det_status_dot)
        self.det_status_layout.addStretch()

        form.addRow("Resource:", self.det_resource)
        form.addRow("Status code:", self.det_status_layout)
        form.addRow("Size:", self.det_size)

        splitter.addWidget(detail_box)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)
        root.addWidget(splitter)

        #naiwgacja
        nav_row = QHBoxLayout()
        self.prev_btn = QPushButton("Previous")
        self.next_btn = QPushButton("Next")
        self.prev_btn.setEnabled(False)
        self.next_btn.setEnabled(False)
        nav_row.addStretch()
        nav_row.addWidget(self.prev_btn)
        nav_row.addWidget(self.next_btn)
        nav_row.addStretch()
        root.addLayout(nav_row)

    #sygnaly
    def _connect_signals(self):
        self.open_btn.clicked.connect(self._open_file)
        self.date_from.dateChanged.connect(self._apply_filter)
        self.date_to.dateChanged.connect(self._apply_filter)
        self.log_list.currentRowChanged.connect(self._on_row_changed)
        self.prev_btn.clicked.connect(self._go_prev)
        self.next_btn.clicked.connect(self._go_next)

    #obsluga zdarzen
    def _open_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open log file", "", "Log files (*.log);;All files (*)")
        if not path:
            return
            
        success, error_msg = self.parser.load(path)
        if not success:
            QMessageBox.critical(self, "Błąd odczytu pliku", f"Brak dostępu lub błąd pliku:\n{error_msg}")
            return
            
        self.path_edit.setText(path)

        # ustawienie zakresow dat
        d_min, d_max = self.parser.date_range()
        self.date_from.setDateRange(QDate(d_min.year, d_min.month, d_min.day), QDate(d_max.year, d_max.month, d_max.day))
        self.date_to.setDateRange(QDate(d_min.year, d_min.month, d_min.day), QDate(d_max.year, d_max.month, d_max.day))
        self.date_from.setDate(QDate(d_min.year, d_min.month, d_min.day))
        self.date_to.setDate(QDate(d_max.year, d_max.month, d_max.day))

        self._apply_filter()

    def _apply_filter(self):
        qd_from = self.date_from.date()
        qd_to = self.date_to.date()
        from_date = date(qd_from.year(), qd_from.month(), qd_from.day())
        to_date = date(qd_to.year(), qd_to.month(), qd_to.day())

        self.filtered = self.parser.filter_by_date(from_date, to_date)
        self._populate_list()

    def _populate_list(self):
        self.log_list.clear()
        for entry in self.filtered:
            # uciecie do 80 znakow + wielokropek gdy tkst jest za dlugi
            label = entry.raw[:80] + "..." if len(entry.raw) > 30 else entry.raw
            self.log_list.addItem(label)

        if self.filtered:
            self.log_list.setCurrentRow(0)
        else:
            self._clear_detail()
            self._update_nav_buttons()

    def _on_row_changed(self, row):
        if row < 0 or row >= len(self.filtered):
            self._clear_detail()
            self._update_nav_buttons()
            return
        entry = self.filtered[row]
        self.det_host.setText(entry.host)
        self.det_date.setText(entry.date_str)
        self.det_time.setText(entry.time_str)
        self.det_tz.setText(entry.timezone)
        self.det_method.setText(entry.method)
        self.det_resource.setText(entry.resource)
        self.det_status.setValue(entry.status)
        self.det_size.setText(f"{entry.size} Bytes")

        # kolorowa kropka obok statusu
        if 200 <= entry.status < 300:
            self.det_status_dot.setStyleSheet("background-color: #4CAF50; border-radius: 7px;") # zielony
        elif 300 <= entry.status < 400:
            self.det_status_dot.setStyleSheet("background-color: #FF9800; border-radius: 7px;") #pomaranczowy dla przekierowan
        elif entry.status >= 400:
            self.det_status_dot.setStyleSheet("background-color: #F44336; border-radius: 7px;") #czerwony
        else:
            self.det_status_dot.setStyleSheet("background-color: #9E9E9E; border-radius: 7px;") # szary dla reszty

        self._update_nav_buttons()

    def _clear_detail(self):
        for w in (self.det_host, self.det_date, self.det_time,
                  self.det_tz, self.det_method, self.det_resource, self.det_size):
            w.clear()
        self.det_status.setValue(0)
        self.det_status_dot.setStyleSheet("background-color: transparent; border-radius: 7px;")

    def _update_nav_buttons(self):
        row = self.log_list.currentRow()
        count = self.log_list.count()
        # nieaktywny prev przy pierwszym rekordzie
        self.prev_btn.setEnabled(row > 0)
        # nieaktywny next przy ostatnim rekordzie
        self.next_btn.setEnabled(row < count - 1)

    def _go_prev(self):
        row = self.log_list.currentRow()
        if row > 0:
            self.log_list.setCurrentRow(row - 1)

    def _go_next(self):
        row = self.log_list.currentRow()
        if row < self.log_list.count() - 1:
            self.log_list.setCurrentRow(row + 1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LogBrowserWindow()
    window.show()
    sys.exit(app.exec())
