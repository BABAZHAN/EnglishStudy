import sys
from PySide6.QtWidgets import QApplication
from ui.windows.main_window import MainWindow
from db.database import init_db  # ← инициализация БД

if __name__ == "__main__":
    init_db()  # ← создаём таблицы и пользователя

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())