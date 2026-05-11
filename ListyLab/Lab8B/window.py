import sys

from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout,
                             QVBoxLayout, QFormLayout, QListWidget, QLabel,
                             QLineEdit, QPushButton, QFileDialog, QMessageBox, QListWidgetItem, QDateTimeEdit,
                             QSplitter, QGroupBox)
from PyQt6.QtCore import Qt, QDateTime
from PyQt6.QtGui import QPalette, QColor

from ListyLab.Lab8B import app
from ListyLab.Lab8B.app import appLogic


class Window(QMainWindow):
    def __init__(self, logic: appLogic):
        super().__init__()
        self.logic = logic
        self.setWindowTitle("Log browser")
        self.resize(900, 600)

        self.create_widgets()
        self.apply_minimal_tweaks()

    def apply_minimal_tweaks(self):
        self.setStyleSheet("""
            QLineEdit[readOnly="true"] {
                background-color: #2b2b2b;
                color: #a6e3a1; 
                border: 1px solid #555;
                border-radius: 3px;
                padding: 4px;
            }
            QGroupBox {
                font-weight: bold;
                border: 1px solid #666;
                border-radius: 5px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
                color: #89b4fa; 
            }
        """)

    def create_widgets(self):
        main_wi = QWidget()
        self.setCentralWidget(main_wi)
        main_layout = QVBoxLayout(main_wi)
        main_layout.setContentsMargins(10, 10, 10, 10)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)

        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 5, 0)

        self.load_button = QPushButton("Load File")
        self.load_button.setMinimumHeight(30)
        self.load_button.clicked.connect(self.load_logs)
        left_layout.addWidget(self.load_button)

        filter_group = QGroupBox("Time Filter")
        filter_layout = QHBoxLayout(filter_group)

        self.date_from = QDateTimeEdit(self)
        self.date_from.setCalendarPopup(True)
        self.date_from.setDisplayFormat("yyyy-MM-dd HH:mm:ss")

        self.date_to = QDateTimeEdit(self)
        self.date_to.setCalendarPopup(True)
        self.date_to.setDisplayFormat("yyyy-MM-dd HH:mm:ss")

        self.btn_filter = QPushButton("Filter")
        self.btn_filter.clicked.connect(self.filter_list)

        filter_layout.addWidget(QLabel("From:"))
        filter_layout.addWidget(self.date_from)
        filter_layout.addWidget(QLabel("To:"))
        filter_layout.addWidget(self.date_to)
        filter_layout.addWidget(self.btn_filter)

        left_layout.addWidget(filter_group)

        self.list_widget = QListWidget()
        self.list_widget.itemSelectionChanged.connect(self.selection)
        left_layout.addWidget(self.list_widget)

        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(5, 0, 0, 0)

        details_group = QGroupBox("File Details")
        form_layout = QFormLayout(details_group)
        form_layout.setSpacing(10)

        self.field_ip = QLineEdit();
        self.field_ip.setReadOnly(True)
        self.field_date = QLineEdit();
        self.field_date.setReadOnly(True)
        self.field_method = QLineEdit();
        self.field_method.setReadOnly(True)
        self.field_host = QLineEdit();
        self.field_host.setReadOnly(True)
        self.field_uri = QLineEdit();
        self.field_uri.setReadOnly(True)
        self.field_status = QLineEdit();
        self.field_status.setReadOnly(True)

        form_layout.addRow(QLabel("IP:"), self.field_ip)
        form_layout.addRow(QLabel("Data and time:"), self.field_date)
        form_layout.addRow(QLabel("HTTP Method:"), self.field_method)
        form_layout.addRow(QLabel("Host:"), self.field_host)
        form_layout.addRow(QLabel("URI:"), self.field_uri)
        form_layout.addRow(QLabel("Status code:"), self.field_status)

        right_layout.addWidget(details_group)
        right_layout.addStretch()

        nav_layout = QHBoxLayout()
        self.btn_prev = QPushButton("Previous")
        self.btn_next = QPushButton("Next")
        self.btn_prev.setMinimumHeight(30)
        self.btn_next.setMinimumHeight(30)

        self.btn_prev.setEnabled(False)
        self.btn_next.setEnabled(False)

        self.btn_prev.clicked.connect(self.select_prev)
        self.btn_next.clicked.connect(self.select_next)

        nav_layout.addWidget(self.btn_prev)
        nav_layout.addWidget(self.btn_next)

        right_layout.addLayout(nav_layout)

        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([550, 350])


    def load_logs(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Wybierz plik logów", "",
                                                   "Wszystkie pliki (*);;Pliki tekstowe (*.txt *.log)")
        if file_name:
            try:
                self.logic.load_logs_to_app(file_name)
                self.refresh_list()

                if self.logic.logs:
                    min_dt = self.logic.logs[0].timestamp
                    max_dt = self.logic.logs[-1].timestamp

                    self.date_from.setDateTime(
                        QDateTime(min_dt.year, min_dt.month, min_dt.day, min_dt.hour, min_dt.minute, min_dt.second))
                    self.date_to.setDateTime(
                        QDateTime(max_dt.year, max_dt.month, max_dt.day, max_dt.hour, max_dt.minute, max_dt.second))

            except Exception as e:
                QMessageBox.critical(self, "Err", f"Could not load file:\n{e}")

    def refresh_list(self):
        self.list_widget.clear()
        for i, log in enumerate(self.logic.logs):
            item = QListWidgetItem(log.http_preview())
            item.setData(Qt.ItemDataRole.UserRole, i)
            self.list_widget.addItem(item)

    def filter_list(self):
        start_date = self.date_from.dateTime().toPyDateTime()
        end_date = self.date_to.dateTime().toPyDateTime()
        self.logic.filter_date(start_date, end_date)
        self.refresh_list()

    def selection(self):
        selected_items = self.list_widget.selectedItems()
        if not selected_items:
            self.field_ip.clear();
            self.field_date.clear();
            self.field_method.clear()
            self.field_host.clear();
            self.field_uri.clear();
            self.field_status.clear()
            self.btn_prev.setEnabled(False);
            self.btn_next.setEnabled(False)
            return

        item = selected_items[0]
        log_index = item.data(Qt.ItemDataRole.UserRole)
        log_entry = self.logic.get_index_log(log_index)

        if log_entry:
            self.field_ip.setText(str(log_entry.ip))
            self.field_date.setText(str(log_entry.timestamp))
            self.field_method.setText(str(log_entry.method))
            self.field_host.setText(str(log_entry.host))
            self.field_uri.setText(str(log_entry.uri))
            self.field_status.setText(str(log_entry.status))

        current_row = self.list_widget.currentRow()
        self.btn_prev.setEnabled(current_row > 0)
        self.btn_next.setEnabled(current_row < self.list_widget.count() - 1)

    def select_prev(self):
        current_row = self.list_widget.currentRow()
        if current_row > 0: self.list_widget.setCurrentRow(current_row - 1)

    def select_next(self):
        current_row = self.list_widget.currentRow()
        if current_row < self.list_widget.count() - 1: self.list_widget.setCurrentRow(current_row + 1)


def set_dark_theme(app: QApplication):
    app.setStyle("Fusion")
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.ColorRole.Window, QColor(45, 45, 45))
    dark_palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.Base, QColor(30, 30, 30))
    dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(45, 45, 45))
    dark_palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)

    app.setPalette(dark_palette)


if __name__ == "__main__":
    app_window = QApplication(sys.argv)
    set_dark_theme(app_window)
    log_app = appLogic()
    window = Window(log_app)
    window.show()
    sys.exit(app_window.exec())
