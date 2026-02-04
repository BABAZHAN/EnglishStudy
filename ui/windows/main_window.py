from PySide6.QtWidgets import QMainWindow, QTabWidget
from ui.windows.today_tab import TodayTab
from ui.windows.progress_tab import ProgressTab
from ui.windows.reading_tab import ReadingTab  # ← импорт из windows
from PySide6.QtCore import Signal, QObject


class MainWindow(QMainWindow):
    progress_updated = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lang Trainer")
        self.resize(1000, 700)

        # СНАЧАЛА создаем все виджеты
        self.today_tab = TodayTab()
        self.reading_tab = ReadingTab()
        self.progress_tab = ProgressTab()

        # ПОТОМ подключаем сигналы
        self.today_tab.progress_updated.connect(self.on_progress_updated)
        self.reading_tab.article_reader.done_btn.clicked.connect(self.on_progress_updated)

        # Создаем вкладки
        self.tabs = QTabWidget()
        self.tabs.addTab(self.today_tab, "🏠 Сегодня")
        self.tabs.addTab(self.reading_tab, "📖 Чтение")
        self.tabs.addTab(self.progress_tab, "📈 Прогресс")

        self.setCentralWidget(self.tabs)

    def on_progress_updated(self):
        """Обновляем таблицу прогресса БЕЗ пересоздания виджета"""
        self.progress_tab.load_data()  # ← просто перезагружаем данные