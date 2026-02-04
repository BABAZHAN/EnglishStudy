from PySide6.QtWidgets import QMainWindow, QTabWidget, QPushButton, QMessageBox
from ui.windows.today_tab import TodayTab
from ui.windows.progress_tab import ProgressTab
from ui.windows.reading_tab import ReadingTab
from PySide6.QtCore import Signal
from ui.dialogs.placement_test_dialog import PlacementTestDialog
from ui.dialogs.level_result_dialog import LevelResultDialog


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

        # Добавляем кнопку определения уровня
        self.setup_today_tab()

    def on_progress_updated(self):
        """Обновляем таблицу прогресса БЕЗ пересоздания виджета"""
        self.progress_tab.load_data()

    def setup_today_tab(self):
        """Добавляем кнопку определения уровня"""
        # Кнопка определения уровня (если уровень ещё не определён)
        if not self.is_level_detected():
            btn = QPushButton("🎯 Определить мой уровень")
            btn.clicked.connect(self.start_placement_test)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #FFC107;
                    color: black;
                    border-radius: 10px;
                    padding: 10px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #FFB74D;
                }
            """)

            # Добавляем кнопку в layout (после заголовка)
            if hasattr(self.today_tab, 'layout') and self.today_tab.layout():
                self.today_tab.layout().insertWidget(1, btn)
            else:
                # Если layout не найден, добавим в другое место
                self.today_tab.start_btn.setParent(None)
                layout = self.today_tab.layout()
                if layout:
                    layout.insertWidget(1, btn)
                    layout.addWidget(self.today_tab.start_btn)

    def is_level_detected(self) -> bool:
        """Проверяет, определён ли уровень (из БД)"""
        # Позже заменим на реальную проверку из БД
        return False

    def start_placement_test(self):
        """Запуск теста на определение уровня"""
        dialog = PlacementTestDialog(self)
        dialog.level_detected.connect(self.show_level_result)
        dialog.exec()

    def show_level_result(self, level: str):
        """Показать результат + персональный план"""
        dialog = LevelResultDialog(level, self)
        if dialog.exec():
            # После закрытия диалога — обновляем интерфейс
            self.refresh_ui_for_level(level)

    def refresh_ui_for_level(self, level: str):
        """Обновляет интерфейс под уровень пользователя"""
        # Например: подсвечиваем рекомендованные вкладки
        QMessageBox.information(
            self,
            "✅ Готово!",
            f"Ваш уровень {level} сохранён.\n"
            "Теперь контент будет подбираться под ваш уровень!"
        )