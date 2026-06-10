import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QCalendarWidget
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtGui import QTextCharFormat, QColor

class ModernCalendar(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)
        self.calendar = QCalendarWidget(self)
        # Basic styling
        self.calendar.setStyleSheet("QCalendarWidget QAbstractItemView:enabled { font-size: 14px; }")
        self.calendar.currentPageChanged.connect(self.highlight_holidays)
        self.layout.addWidget(self.calendar)
        self.setWindowTitle("Modern Calendar")
        self.highlight_holidays(self.calendar.yearShown(), self.calendar.monthShown())

    def highlight_holidays(self, year, month):
        # Fetch and highlight holidays
        conn = sqlite3.connect('calendar.db')
        cursor = conn.cursor()
        cursor.execute("SELECT holiday_date FROM holidays WHERE strftime('%Y-%m', holiday_date) = ?", 
                       (f"{year}-{month:02d}",))
        
        fmt = QTextCharFormat()
        fmt.setForeground(QColor(Qt.GlobalColor.red))
        for (date_str,) in cursor.fetchall():
            self.calendar.setDateTextFormat(QDate.fromString(date_str, "yyyy-MM-dd"), fmt)
        conn.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ModernCalendar()
    ex.show()
    sys.exit(app.exec())

