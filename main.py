import sys
from PyQt6.QtWidgets import QApplication, QWidget, QCalendarWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt, QPoint


class ModernCalendar(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground) 
        self.main_layout = QVBoxLayout()
        self.drag_position = QPoint()
        self.cal_widget = QCalendarWidget() 
        self.initUI()

    def initUI(self):
        layout = self.main_layout

        # Create Calendar
        cal = self.cal_widget
        cal.setGridVisible(False)  # Hide the old grid lines

        # Modern Stylesheet
        style = """
            /* Navigation bar (Month and Year) */
            QCalendarWidget #qt_calendar_navigationbar {
                background-color: #2b2b2b;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
            
            /* Previous and Next Buttons */
            QCalendarWidget QToolButton {
                color: white;
                background-color: transparent;
                border-radius: 4px;
                icon-size: 16px;
                margin: 5px;
            }
            QCalendarWidget QToolButton:hover {
                background-color: #3d3d3d;
            }
            
            /* Month/Year Menu */
            QCalendarWidget QMenu {
                background-color: #2b2b2b;
                color: white;
            }
            
            /* Weekday Headers (Mon, Tue, etc.) */
            QCalendarWidget QWidget#qt_calendar_widget {
                alternate-background-color: #f0f0f0;
            }
            
            /* Day Cell Styling */
            QCalendarWidget QAbstractItemView:enabled {
                color: #e0e0e0;
                background-color: #1e1e1e;
                selection-background-color: #0d6efd;
                selection-color: white;
            }
            
            QCalendarWidget QAbstractItemView:disabled {
                color: #595959;
                background-color: #1e1e1e;
            }
        """
        cal.setStyleSheet(style)

        container = QWidget(self)
        container.setStyleSheet(""" 
                                QWidget { 
                                    background-color: #1e1e1e;
                                    border-top-left-radius: 10px;
                                    border-top-right-radius: 10px;
                                    border-bottom-right-radius: 0;
                                    border-bottom-left-radius: 0;
                            }  
                                """)
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(12, 12, 12, 12)
        container_layout.setSpacing(8)

        self.title_bar = QWidget(container)
        self.title_bar.setFixedHeight(32)
        self.title_bar.setObjectName("TitleBar")
        title_bar_layout = QHBoxLayout(self.title_bar)
        title_bar_layout.setContentsMargins(0, 0, 0, 0)
        title_bar_layout.addStretch()

        close_btn = QPushButton("✕")
        close_btn.setFixedSize(28, 28)
        close_btn.setStyleSheet(
            """
            QPushButton {
                background-color: rgba(255, 255, 255, 0.12);
                color: white;
                border: none;
                border-radius: 14px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.22);
            }
            """
        )
        close_btn.clicked.connect(self.close)
        title_bar_layout.addWidget(close_btn)

        container_layout.addWidget(self.title_bar)
        container_layout.addWidget(cal)

        layout.addWidget(container)
        self.setLayout(layout)
        self.setWindowTitle("Modern Calendar")
        self.setFixedSize(350, 300)
        self.resize(350, 300)
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.title_bar.underMouse():
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Sets modern default look
    ex = ModernCalendar()
    ex.show()
    sys.exit(app.exec())
