from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QGraphicsDropShadowEffect,
)
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import QLocale, Qt, QDate
from holiday_manager import HolidayManager
from utils import get_theme_palette, indonesia_date, indonesia_date_month


class DateWidget(QWidget):
    def __init__(self, theme="light"):
        super().__init__()

        self.current_date = QDate.currentDate()
        self.dragPosition = None
        self.holiday_manager = HolidayManager()
        self.theme = theme
        self.theme_palette = get_theme_palette(self.theme)

        self.initUI()

    def initUI(self):
        self.setFixedSize(250, 350)
        self.setLocale(
            QLocale(QLocale.Language.Indonesian, QLocale.Country.Indonesia)
        )
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.container = QWidget(self)
        self.container.setStyleSheet(
            """
            QWidget {
                background-color: rgba(255, 255, 255, 0.8);
                border-radius: 12px;
                color: #333333;
            }
            """
        )

        main_layout = QVBoxLayout(self.container)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(8)

        self.close_btn = QPushButton("✕", self)
        self.close_btn.clicked.connect(self.close)
        self.close_btn.setFixedSize(24, 24)
        self.close_btn.setStyleSheet(
            """
            QPushButton {
                background-color: rgba(255, 107, 107, 0.6);
                color: white;
                border: none;
                border-radius: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(255, 71, 87, 0.8);
            }
            """
        )
        self.close_btn.raise_()

        nav_layout = QHBoxLayout()

        self.prev_btn = QPushButton("◀")
        self.prev_btn.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
                border: none;
                font-size: 40px;
                color: #5DADE2;
            }
            QPushButton:hover {
                color: #3498DB;
            }
            """
        )
        self.prev_btn.clicked.connect(self.show_previous_date)

        self.next_btn = QPushButton("▶")
        self.next_btn.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
                border: none;
                font-size: 40px;
                color: #5DADE2;
            }
            QPushButton:hover {
                color: #3498DB;
            }
            """
        )
        self.next_btn.clicked.connect(self.show_next_date)

        self.month_label = QLabel()
        self.month_label.setStyleSheet(
            """
            background-color: #5DADE2;
            color: white;
            padding: 5px 10px;
            border-radius: 8px;
            font-weight: bold;
            """
        )
        self.month_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.month_label.setFont(QFont("Arial", 14))

        nav_layout.addWidget(self.prev_btn)
        nav_layout.addWidget(self.month_label)
        nav_layout.addWidget(self.next_btn)
        main_layout.addLayout(nav_layout)

        self.day_of_week = QLabel()
        self.day_of_week.setStyleSheet(
            """
            color: rgb(128, 145, 146);
            padding: 5px;
            text-align: center;
            font-weight: bold;
            """
        )
        self.day_of_week.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.day_of_week.setFont(QFont("Arial", 12))
        main_layout.addWidget(self.day_of_week)

        self.date_label = QLabel()
        self.date_label.setStyleSheet(
            """
            color: #5DADE2;
            padding: 10px;
            text-align: center;
            border-radius: 10px;
            """
        )
        self.date_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.date_label.setFont(QFont("Arial", 48, QFont.Weight.Bold))
        main_layout.addWidget(self.date_label)

        self.holiday_label = QLabel("Tidak ada Event")
        self.holiday_label.setStyleSheet(
            """
            color: rgb(224, 52, 32);
            padding: 8px;
            text-align: center;
            border-radius: 8px;
            background-color: rgba(236, 220, 96, 0.6);
            font-weight: bold;
            """
        )
        self.holiday_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.holiday_label.setFont(QFont("Arial", 10))
        main_layout.addWidget(self.holiday_label)

        self.full_date_label = QLabel()
        self.full_date_label.setStyleSheet(
            """
            color: rgb(17, 17, 17);
            padding: 5px;
            text-align: center;
            font-weight: bold;
            """
        )
        self.full_date_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.full_date_label.setFont(QFont("Arial", 9))
        main_layout.addWidget(self.full_date_label)

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(15)
        self.shadow.setColor(QColor(0, 0, 0, 50))
        self.shadow.setOffset(0, 3)
        self.container.setGraphicsEffect(self.shadow)

        main_layout_container = QVBoxLayout(self)
        main_layout_container.addWidget(self.container)
        main_layout_container.setContentsMargins(0, 0, 0, 0)

        self.apply_theme()
        self.update_date(self.current_date)
        self.move_to_corner("top-left")

    def update_date(self, date):
        self.current_date = date
        self.month_label.setText(indonesia_date_month(date, "long").upper())
        self.day_of_week.setText(indonesia_date("date_only", date))
        self.date_label.setText(date.toString("d"))
        self.full_date_label.setText(indonesia_date("custom", date))

        holiday = self.holiday_manager.get_holiday(date)
        self.holiday_label.setText(holiday)

        if date == QDate.currentDate():
            self.date_label.setStyleSheet(
                f"""
                color: {self.theme_palette['active_date_text']};
                background-color: {self.theme_palette['active_date_bg']};
                padding: 10px;
                text-align: center;
                border-radius: 10px;
                """
            )
        else:
            self.date_label.setStyleSheet(
                f"""
                color: {self.theme_palette['date_text']};
                padding: 10px;
                text-align: center;
                border-radius: 10px;
                """
            )

    def apply_theme(self):
        theme = self.theme_palette

        self.container.setStyleSheet(
            f"""
            QWidget {{
                background-color: {theme['container_bg']};
                border-radius: 12px;
                color: {theme['text_color']};
            }}
            """
        )

        self.close_btn.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {theme['close_button_bg']};
                color: {theme['close_button_text']};
                border: none;
                border-radius: 12px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {theme['close_button_hover']};
            }}
            """
        )

        nav_button_style = f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                font-size: 40px;
                color: {theme['nav_button_color']};
            }}
            QPushButton:hover {{
                color: {theme['nav_button_hover']};
            }}
            """
        self.prev_btn.setStyleSheet(nav_button_style)
        self.next_btn.setStyleSheet(nav_button_style)

        self.month_label.setStyleSheet(
            f"""
            background-color: {theme['accent_color']};
            color: {theme['accent_text']};
            padding: 5px 10px;
            border-radius: 8px;
            font-weight: bold;
            """
        )

        self.day_of_week.setStyleSheet(
            f"""
            color: {theme['secondary_text']};
            padding: 5px;
            text-align: center;
            font-weight: bold;
            """
        )

        self.date_label.setStyleSheet(
            f"""
            color: {theme['date_text']};
            padding: 10px;
            text-align: center;
            border-radius: 10px;
            """
        )

        self.holiday_label.setStyleSheet(
            f"""
            color: {theme['holiday_text']};
            padding: 8px;
            text-align: center;
            border-radius: 8px;
            background-color: {theme['holiday_bg']};
            font-weight: bold;
            """
        )

        self.full_date_label.setStyleSheet(
            f"""
            color: {theme['full_date_text']};
            padding: 5px;
            text-align: center;
            font-weight: bold;
            """
        )

        self.shadow.setColor(QColor(theme['shadow_color']))

    def set_theme(self, theme):
        self.theme = theme
        self.theme_palette = get_theme_palette(self.theme)
        self.apply_theme()
        self.update_date(self.current_date)

    def show_previous_date(self):
        self.update_date(self.current_date.addDays(-1))

    def show_next_date(self):
        self.update_date(self.current_date.addDays(1))

    def move_to_corner(self, corner="top-right", margin=12):
        screen = QApplication.primaryScreen().availableGeometry()
        x = screen.left() + margin
        y = screen.top() + margin

        if corner == "top-right":
            x = screen.right() - self.width() - margin
        elif corner == "top-left":
            x = screen.left() + margin
        elif corner == "bottom-right":
            x = screen.right() - self.width() - margin
            y = screen.bottom() - self.height() - margin
        elif corner == "bottom-left":
            x = screen.left() + margin
            y = screen.bottom() - self.height() - margin
        else:
            raise ValueError(f"Unknown corner: {corner}")

        self.move(x, y)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragPosition = (
                event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            )
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self.dragPosition is not None:
            self.move(event.globalPosition().toPoint() - self.dragPosition)
            event.accept()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        margin = 1
        self.close_btn.move(self.width() - self.close_btn.width() - margin, margin)

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.show_next_date()
        else:
            self.show_previous_date()
        event.accept()
