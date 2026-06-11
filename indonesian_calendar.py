import json
from pathlib import Path
import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QCalendarWidget,
    QWidget,
    QVBoxLayout,
    QListWidget,
    QLabel,
)
from PyQt6.QtCore import QDate, QLocale
from PyQt6.QtGui import QColor, QBrush, QTextCharFormat, QFont


class IndonesianCalendar(QWidget):
    """A custom calendar widget for displaying the Indonesian locale with holiday highlights."""

    def __init__(self, parent=None):
        super().__init__(parent)

        # 1. Force the widget instance to use the Indonesian Locale memory footprint
        # This translates weekdays, month names, and headers automatically on Windows 10!
        self.indonesian_locale = QLocale(
            QLocale.Language.Indonesian, QLocale.Country.Indonesia
        )
        self.setLocale(self.indonesian_locale)

        # 2. Initialize the calendar widget and holiday list container
        self.calendar_widget = QCalendarWidget(self)
        # disable vertical header
        self.calendar_widget.setVerticalHeaderFormat(
            QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader
        )
        self.calendar_widget.setLocale(self.indonesian_locale)
        self.calendar_widget.currentPageChanged.connect(self.update_holiday_list)

        # 3. Load Indonesian holidays from JSON file
        self.public_holidays = self.load_public_holidays()

        # 4. Prepare holiday list widget
        self.holiday_list_widget = QListWidget()
        # self.holiday_list_widget.setFixedHeight(140)

        # 5. Layout the calendar + holiday list vertically
        layout = QVBoxLayout(self)
        layout.addWidget(self.calendar_widget)
        layout.addWidget(QLabel("Daftar Hari Libur Bulan Ini:"))
        layout.addWidget(self.holiday_list_widget)
        self.setLayout(layout)

        self.highlight_holidays()
        self.update_holiday_list()

    def load_public_holidays(self):
        """Load holidays from the tgl_merah.json file."""
        holidays = {}
        try:
            file_path = Path(__file__).resolve().parent / "tgl_merah.json"
            with file_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
            for item in data:
                date_str = item.get("date")
                name = item.get("name")
                if date_str and name:
                    holidays[date_str] = name
        except Exception:
            # Fall back to empty holiday list when file is unavailable or invalid
            holidays = {}
        return holidays

    def highlight_holidays(self):
        """Applies explicit holiday highlights onto the Indonesian local calendar."""
        holiday_format = QTextCharFormat()
        holiday_format.setBackground(QBrush(QColor("#FFCDD2")))  # Soft Red
        holiday_format.setForeground(QBrush(QColor("#B71C1C")))  # Deep Red text

        font = QFont()
        font.setBold(True)
        holiday_format.setFont(font)

        for date_str, holiday_name in self.public_holidays.items():
            try:
                year, month, day = map(int, date_str.split("-"))
                holiday_date = QDate(year, month, day)

                holiday_format.setToolTip(holiday_name)
                self.calendar_widget.setDateTextFormat(holiday_date, holiday_format)
            except ValueError:
                continue

        # Highlight today's date specifically with blue bold text.
        today_format = QTextCharFormat()
        today_format.setForeground(QBrush(QColor("#1E88E5")))  # Blue text
        today_font = QFont()
        today_font.setBold(True)
        today_format.setFont(today_font)
        self.calendar_widget.setDateTextFormat(QDate.currentDate(), today_format)

    def update_holiday_list(self):
        """Populate the list of holidays for the currently shown month."""
        self.holiday_list_widget.clear()
        current_year = self.calendar_widget.yearShown()
        current_month = self.calendar_widget.monthShown()
        entries = []

        for date_str, holiday_name in sorted(self.public_holidays.items()):
            try:
                year, month, day = map(int, date_str.split("-"))
            except ValueError:
                continue

            if year == current_year and month == current_month:
                holiday_date = QDate(year, month, day)
                entries.append((day, holiday_date, holiday_name))

        for _, holiday_date, holiday_name in entries:
            display_date = self.indonesian_locale.toString(
                holiday_date, "dddd, dd MMMM yyyy"
            )
            self.holiday_list_widget.addItem(f"{display_date} — {holiday_name}")

        if not entries:
            self.holiday_list_widget.addItem("Tidak ada hari libur bulan ini.")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Optional: Force the entire App layout structure to look identical across OS platforms
    app.setStyle("Fusion")

    window = QMainWindow()
    window.setWindowTitle("Indonesian Native Calendar (PyQt6)")
    window.setGeometry(100, 100, 450, 380)

    calendar = IndonesianCalendar(window)
    window.setCentralWidget(calendar)

    window.show()
    sys.exit(app.exec())
