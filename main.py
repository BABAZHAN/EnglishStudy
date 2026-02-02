import sys
from PySide6.QtWidgets import QApplication
from ui.windows.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Кроссплатформенный стиль

    window = MainWindow()
    window.show()

    sys.exit(app.exec())