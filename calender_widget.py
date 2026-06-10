import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QGraphicsDropShadowEffect,
)
from PyQt6.QtGui import QFont, QColor, QIcon
from PyQt6.QtCore import Qt, QDate


class HolidayManager:
    def __init__(self):
        # Predefined holidays for 2025
        self.holidays = {
            QDate(2026, 1, 13): "Duruthu Full Moon Poya Day",
            QDate(2026, 1, 14): "Tamil Thai Pongal Day",
            QDate(2026, 2, 4): "Independence Day",
            QDate(2026, 2, 12): "Navam Full Moon Poya Day",
            QDate(2026, 2, 26): "Mahasivarathri Day",
            QDate(2026, 3, 13): "Medin Full Moon Poya Day",
            QDate(2026, 3, 31): "Ramazan Festival Day",
            QDate(2026, 4, 12): "Bak Full Moon Poya Day",
            QDate(2026, 4, 13): "Day Before Sinhala & Tamil New Year Day",
            QDate(2026, 4, 14): "Sinhala & Tamil New Year Day",
            QDate(2026, 4, 15): "Special Bank Holiday",
            QDate(2026, 4, 18): "Good Friday",
            QDate(2026, 5, 1): "May Day",
            QDate(2026, 5, 12): "Vesak Full Moon Poya Day",
            QDate(2026, 5, 13): "Day following Vesak Full Moon Poya Day",
            QDate(2026, 6, 7): "Hadji Festival Day",
            QDate(2026, 6, 10): "Poson Full Moon Poya Day",
            QDate(2026, 7, 10): "Esala Full Moon Poya Day",
            QDate(2026, 8, 8): "Nikini Full Moon Poya Day",
            QDate(2026, 9, 5): "Holy Prophet's Birthday",
            QDate(2026, 9, 7): "Binara Full Moon Poya Day",
            QDate(2026, 10, 6): "Vap Full Moon Poya Day",
            QDate(2026, 10, 20): "Deepavali Festival Day",
            QDate(2026, 11, 5): "Ill Full Moon Poya Day",
            QDate(2026, 12, 4): "Unduvap Full Moon Poya Day",
            QDate(2026, 12, 25): "Christmas Day",
            # Example holiday on the current date
        }

    def get_holiday(self, date):
        return self.holidays.get(date, "No holidays")


class DateWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.current_date = QDate.currentDate()
        self.holiday_manager = HolidayManager()
        self.initUI()

    def initUI(self):
        # Light transparent theme configuration
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Main container widget
        container = QWidget(self)
        container.setStyleSheet("""
            QWidget {
                background-color: rgba(255, 255, 255, 0.8);
                border-radius: 12px;
                color: #333333;
            }
        """)

        # Main layout
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(8)

        # Close button layout
        close_layout = QHBoxLayout()
        close_btn = QPushButton("✕")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF6B6B;
                color: white;
                border: none;
                border-radius: 15px;
                width: 25px;
                height: 25px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FF4757;
            }
        """)
        close_btn.clicked.connect(self.close)
        close_layout.addStretch()
        close_layout.addWidget(close_btn)
        main_layout.addLayout(close_layout)

        # Navigation and Month Layout
        nav_layout = QHBoxLayout()

        # Previous Date Button
        prev_btn = QPushButton("◀")
        prev_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                font-size: 40px;
                color: #5DADE2;
            }
            QPushButton:hover {
                color: #3498DB;
            }
        """)
        prev_btn.clicked.connect(self.show_previous_date)

        # Next Date Button
        next_btn = QPushButton("▶")
        next_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                font-size: 40px;
                color: #5DADE2;
            }
            QPushButton:hover {
                color: #3498DB;
            }
        """)
        next_btn.clicked.connect(self.show_next_date)

        # Month Label
        self.month_label = QLabel("MAR")
        self.month_label.setStyleSheet("""
            background-color: #5DADE2;
            color: white;
            padding: 5px 10px;
            border-radius: 8px;
            font-weight: bold;
        """)
        self.month_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.month_label.setFont(QFont("Arial", 14))

        nav_layout.addWidget(prev_btn)
        nav_layout.addWidget(self.month_label)
        nav_layout.addWidget(next_btn)
        main_layout.addLayout(nav_layout)

        # Day of Week Label
        self.day_of_week = QLabel()
        self.day_of_week.setStyleSheet("""
            color:rgb(128, 145, 146);
            padding: 5px;
            text-align: center;
            font-weight:bold;
        """)
        self.day_of_week.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.day_of_week.setFont(QFont("Arial", 12))
        main_layout.addWidget(self.day_of_week)

        # Date Label
        self.date_label = QLabel()
        self.date_label.setStyleSheet("""
            color: #5DADE2;
            padding: 10px;
            text-align: center;
            border-radius: 10px;
        """)
        self.date_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.date_label.setFont(QFont("Arial", 48, QFont.Weight.Bold))
        main_layout.addWidget(self.date_label)

        # Holiday Label
        self.holiday_label = QLabel("No Holidays")
        self.holiday_label.setStyleSheet("""
            color:rgb(224, 52, 32);
            padding: 8px;
            text-align: center;
            border-radius: 8px;
            background-color: rgba(236, 220, 96, 0.6);
            font-weight:bold;
        """)
        self.holiday_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.holiday_label.setFont(QFont("Arial", 10))
        main_layout.addWidget(self.holiday_label)

        # Full Date Label
        self.full_date_label = QLabel()
        self.full_date_label.setStyleSheet("""
            color:rgb(17, 17, 17);
            padding: 5px;
            text-align: center;
            font-weight:bold;
        """)
        self.full_date_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.full_date_label.setFont(QFont("Arial", 9))
        main_layout.addWidget(self.full_date_label)

        # Add shadow effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 50))
        shadow.setOffset(0, 3)
        container.setGraphicsEffect(shadow)

        # Set the main layout
        main_layout_container = QVBoxLayout(self)
        main_layout_container.addWidget(container)
        main_layout_container.setContentsMargins(0, 0, 0, 0)

        # Initial date update
        self.update_date(self.current_date)

        # Resize and center
        self.resize(250, 350)
        self.center_on_screen()

    def update_date(self, date):
        self.current_date = date
        self.month_label.setText(date.toString("MMM").upper())
        self.day_of_week.setText(date.toString("dddd"))
        self.date_label.setText(date.toString("d"))
        self.full_date_label.setText(date.toString("dddd, MMMM d, yyyy"))

        # Update holiday
        holiday = self.holiday_manager.get_holiday(date)
        self.holiday_label.setText(holiday)

        # Highlight today's date
        if date == QDate.currentDate():
            self.date_label.setStyleSheet("""
                color: white;
                background-color: #5DADE2;
                padding: 10px;
                text-align: center;
                border-radius: 10px;
            """)
        else:
            self.date_label.setStyleSheet("""
                color: #5DADE2;
                padding: 10px;
                text-align: center;
                border-radius: 10px;
            """)

    def show_previous_date(self):
        previous_date = self.current_date.addDays(-1)
        self.update_date(previous_date)

    def show_next_date(self):
        next_date = self.current_date.addDays(1)
        self.update_date(next_date)

    def center_on_screen(self):
        screen = QApplication.primaryScreen().geometry()
        self.move(
            (screen.width() - self.width()) // 2, (screen.height() - self.height()) // 2
        )

    # Make the window movable
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragPosition = (
                event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            )
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.dragPosition)
            event.accept()


def main():
    app = QApplication(sys.argv)
    widget = DateWidget()
    widget.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
