from PySide6.QtWidgets import QMainWindow, QTabWidget
from ui.windows.today_tab import TodayTab
from ui.windows.progress_tab import ProgressTab
from ui.windows.reading_tab import ReadingTab  # ← импорт из windows


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lang Trainer")
        self.resize(1000, 700)

        self.tabs = QTabWidget()
        self.today_tab = TodayTab()
        self.reading_tab = ReadingTab()  # ← ReadingTab
        self.progress_tab = ProgressTab()

        self.tabs.addTab(self.today_tab, "🏠 Сегодня")
        self.tabs.addTab(self.reading_tab, "📖 Чтение")  # ← вкладка добавлена
        self.tabs.addTab(self.progress_tab, "📈 Прогресс")

        self.setCentralWidget(self.tabs)