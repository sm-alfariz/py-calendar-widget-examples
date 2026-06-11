import sys
from PyQt6.QtWidgets import QApplication
from date_widget import DateWidget

def main():
    app = QApplication(sys.argv)
    widget = DateWidget(theme="light")  # You can switch to "light" or "dark" theme
    widget.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
