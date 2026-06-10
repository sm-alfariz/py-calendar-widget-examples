import sys
import json
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QCalendarWidget,
    QPushButton,
    QLabel,
    QScrollArea,
    QFrame,
)
from PyQt6.QtCore import Qt, QDate, QPoint
from PyQt6.QtGui import QTextCharFormat, QColor

class ModernCalendar(QWidget):
    def __init__(self):
        super().__init__()
        # 1. Load Holiday Data from your JSON structure
        self.holidays = self.load_holiday_json()
        self.drag_position = QPoint()
        self.initUI()

    def load_holiday_json(self):
        # Open your local file with UTF-8 encoding to support characters like in "Isra Mi'raj"
        try:
            with open("tgl_merah.json", "r", encoding="utf-8") as file:
                # Use json.load() for files, NOT json.loads()
                raw_list = json.load(file)

            # Re-map list of dictionaries into a fast-lookup key-value dictionary {"YYYY-MM-DD": "Name"}
            return {
                item["date"]: item["name"]
                for item in raw_list
                if item.get("type") == "holiday"
            }
        except FileNotFoundError:
            print("Error: 'holidays.json' file not found. Creating empty holiday list.")
            return {}
        except Exception as e:
            print(f"Error loading JSON: {e}")
            return {}

    def initUI(self):
        # 2. Frameless and Translucent setup
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # 3. Main Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Container widget for rounded corners and styling
        self.container = QWidget(self)
        self.container.setObjectName("MainContainer")
        container_layout = QVBoxLayout(self.container)
        container_layout.setContentsMargins(0, 0, 0, 10)
        container_layout.setSpacing(5)

        # 4. Top Header Bar Layout (Draggable area)
        self.header_bar = QWidget(self)
        self.header_bar.setObjectName("HeaderBar")
        header_layout = QHBoxLayout(self.header_bar)
        header_layout.setContentsMargins(0, 5, 0, 5)
        header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Close Button
        self.close_btn = QPushButton("✕", self)
        self.close_btn.setObjectName("CloseButton")
        self.close_btn.setFixedSize(30, 30)
        self.close_btn.clicked.connect(self.close)
        header_layout.addWidget(self.close_btn)

        container_layout.addWidget(self.header_bar)

        # 5. Calendar Widget
        self.calendar = QCalendarWidget(self)
        self.calendar.setGridVisible(False)
        self.calendar.setVerticalHeaderFormat(
            QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader
        )
        self.calendar.currentPageChanged.connect(self.update_month_holidays)
        container_layout.addWidget(self.calendar)

        # 6. Scrollable Holiday List at Bottom
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)

        self.holiday_list_label = QLabel(self)
        self.holiday_list_label.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )
        self.holiday_list_label.setObjectName("HolidayListLabel")
        self.holiday_list_label.setWordWrap(True)

        self.scroll_area.setWidget(self.holiday_list_label)
        container_layout.addWidget(self.scroll_area)

        layout.addWidget(self.container)

        self.setLayout(layout)
        self.setFixedSize(300, 520)

        # 7. Setup Visual Highlights and Initial List
        self.highlight_holidays()
        self.update_month_holidays(
            self.calendar.yearShown(), self.calendar.monthShown()
        )

        # 8. Modern QSS Styling
        self.setStyleSheet("""
            QWidget#MainContainer {
                background-color: white;
                border-radius: 15px;
            }
            QWidget#HeaderBar {
                background-color: #4CAF50;
                border-top-left-radius: 15px;
                border-top-right-radius: 15px;
            }
            QPushButton#CloseButton {
                background-color: rgba(255, 255, 255, 0.2);
                color: white;
                border: none;
                border-radius: 15px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton#CloseButton:hover {
                background-color: #e81123;
                color: white;
            }
            QCalendarWidget QWidget {
                alternate-background-color: #f0f0f0;
            }
            QCalendarWidget QAbstractItemView {
                background-color: transparent;
                selection-background-color: #352DA7;
                selection-color: white;
            }
            QCalendarWidget QAbstractItemView:enabled {
                color: #333333;
            }
            QCalendarWidget QWidget#qt_calendar_navigationbar {
                background-color: #352DA7;
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
            QScrollArea {
                background: transparent;
            }
            QLabel#HolidayListLabel {
                color: #555555;
                font-size: 13px;
                line-height: 18px;
                padding: 5px 15px;
            }
        """)

    # 9. Window Dragging Logic
    def mousePressEvent(self, event):
        if self.header_bar.underMouse() and event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = (
                event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            )
            event.accept()

    def mouseMoveEvent(self, event):
        if (
            event.buttons() == Qt.MouseButton.LeftButton
            and not self.drag_position.isNull()
        ):
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.drag_position = QPoint()
        event.accept()

    def highlight_holidays(self):
        holiday_format = QTextCharFormat()
        holiday_format.setForeground(QColor("#E81123")) #352DA7 #E81123
        holiday_format.setFontWeight(700)

        for date_str in self.holidays.keys():
            qdate = QDate.fromString(date_str, "yyyy-MM-dd")
            if qdate.isValid():
                self.calendar.setDateTextFormat(qdate, holiday_format)

    def update_month_holidays(self, year, month):
        current_month_holidays = []

        for date_str in sorted(self.holidays.keys()):
            qdate = QDate.fromString(date_str, "yyyy-MM-dd")
            if qdate.isValid() and qdate.year() == year and qdate.month() == month:
                formatted_day = qdate.toString("MMM d")
                current_month_holidays.append(
                    f"• <b>{formatted_day}</b> : {self.holidays[date_str]}"
                )

        if current_month_holidays:
            title = f"<b style='color: #4CAF50;'>Holidays this month:</b><br>"
            self.holiday_list_label.setText(title + "<br>".join(current_month_holidays))
        else:
            self.holiday_list_label.setText(
                "<i style='color: #888888;'>No holidays this month</i>"
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ModernCalendar()
    ex.show()
    sys.exit(app.exec())
