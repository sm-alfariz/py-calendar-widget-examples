import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QCalendarWidget,
    QPushButton,
    QLabel,
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QTextCharFormat, QColor


class ModernCalendar(QWidget):
    def __init__(self):
        super().__init__()
        # 1. Define Holiday Data (Format: 'YYYY-MM-DD')
        self.holidays = {
            "2026-01-01": "New Year's Day",
            "2026-07-04": "Independence Day",
            "2026-11-26": "Thanksgiving",
            "2026-12-25": "Christmas Day",
        }
        self.initUI()

    def initUI(self):
        # 2. Frameless and Translucent setup
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # 3. Main Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Container widget to apply background & rounded corners to everything
        self.container = QWidget(self)
        self.container.setObjectName("MainContainer")
        container_layout = QVBoxLayout(self.container)
        container_layout.setContentsMargins(0, 0, 0, 15)  # Margin at bottom for label

        # 4. Calendar Widget
        self.calendar = QCalendarWidget(self)
        self.calendar.setGridVisible(False)
        self.calendar.setVerticalHeaderFormat(
            QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader
        )
        self.calendar.selectionChanged.connect(self.check_holiday)
        container_layout.addWidget(self.calendar)

        # 5. Holiday Info Label at Bottom
        self.holiday_label = QLabel("Select a date", self)
        self.holiday_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.holiday_label.setObjectName("HolidayLabel")
        container_layout.addWidget(self.holiday_label)

        layout.addWidget(self.container)

        # 6. Floating Close Button
        self.close_btn = QPushButton("✕", self)
        self.close_btn.clicked.connect(self.close)
        self.close_btn.setGeometry(365, 12, 24, 24)

        self.setLayout(layout)
        self.setFixedSize(400, 440)  # Increased height to accommodate the label

        # 7. Apply Holiday Styles to Grid
        self.highlight_holidays()

        # 8. Modern QSS Styling
        self.setStyleSheet("""
            QWidget#MainContainer {
                background-color: white;
                border-radius: 15px;
            }
            QCalendarWidget QWidget {
                alternate-background-color: #f0f0f0;
            }
            QCalendarWidget QAbstractItemView {
                background-color: transparent;
                selection-background-color: #4CAF50;
                selection-color: white;
            }
            QCalendarWidget QAbstractItemView:enabled {
                color: #333333;
            }
            /* Navigation bar styling */
            QCalendarWidget QWidget#qt_calendar_navigationbar {
                background-color: #4CAF50;
                border-top-left-radius: 15px;
                border-top-right-radius: 15px;
            }
            QCalendarWidget QToolButton {
                color: white;
                font-weight: bold;
                icon-size: 20px;
                background-color: transparent;
            }
            QCalendarWidget QToolButton:hover {
                background-color: #45a049;
                border-radius: 5px;
            }
            QCalendarWidget QMenu {
                background-color: white;
            }
            /* Floating Close Button Styling */
            QPushButton {
                background-color: rgba(255, 255, 255, 0.2);
                color: white;
                border: none;
                border-radius: 12px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #e81123;
                color: white;
            }
            /* Holiday Label Styling */
            QLabel#HolidayLabel {
                color: #555555;
                font-size: 14px;
                font-weight: bold;
                padding: 5px;
            }
        """)

        # Trigger initial check for today's date
        self.check_holiday()

    def highlight_holidays(self):
        # Format for styling holiday text color
        holiday_format = QTextCharFormat()
        holiday_format.setForeground(
            QColor("#E81123")
        )  # Distinct red text for holidays
        holiday_format.setFontWeight(700)  # Bold

        for date_str in self.holidays.keys():
            qdate = QDate.fromString(date_str, "yyyy-MM-dd")
            if qdate.isValid():
                self.calendar.setDateTextFormat(qdate, holiday_format)

    def check_holiday(self):
        selected_date = self.calendar.selectedDate().toString("yyyy-MM-dd")
        if selected_date in self.holidays:
            self.holiday_label.setText(f"🎉 {self.holidays[selected_date]}")
            self.holiday_label.setStyleSheet("color: #E81123;")
        else:
            # Revert to standard date display if it is not a holiday
            nice_date = self.calendar.selectedDate().toString("MMMM d, yyyy")
            self.holiday_label.setText(nice_date)
            self.holiday_label.setStyleSheet("color: #555555;")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ModernCalendar()
    ex.show()
    sys.exit(app.exec())
