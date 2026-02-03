from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QHeaderView
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from db.database import get_recent_progress  # ← импорт функции БД


class ProgressTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        title = QLabel("📊 История прогресса")
        title.setFont(QFont("Arial", 16, QFont.Bold))

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Дата", "Навык", "Уровень", "Счёт"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addSpacing(10)
        layout.addWidget(self.table)
        self.setLayout(layout)

    def load_data(self):
        """Загружает данные из БД в таблицу"""
        rows = get_recent_progress(limit=20)
        self.table.setRowCount(len(rows))

        for row_idx, row_data in enumerate(rows):
            for col_idx, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row_idx, col_idx, item)

        if not rows:
            self.table.setRowCount(1)
            self.table.setItem(0, 0, QTableWidgetItem("Нет данных"))
            self.table.setSpan(0, 0, 1, 4)

    def refresh(self):
        """Обновляет данные без пересоздания таблицы"""
        self.load_data()