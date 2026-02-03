from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont
import random
from db.database import save_progress  # ← импорт функции БД
from PySide6.QtCore import Signal


class TodayTab(QWidget):
    def __init__(self):
        super().__init__()

        self.status_label = QLabel("Готов к тренировке")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setFont(QFont("Arial", 14))

        self.start_btn = QPushButton("🎤 Начать тренировку")
        self.start_btn.setFixedSize(250, 60)
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.start_btn.clicked.connect(self.on_start_clicked)  # ← обработчик клика

        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(self.status_label)
        layout.addSpacing(20)
        layout.addWidget(self.start_btn, alignment=Qt.AlignCenter)
        layout.addStretch()
        self.setLayout(layout)

    def on_start_clicked(self):
        self.status_label.setText("⏳ Анализ речи...")
        self.start_btn.setEnabled(False)

        # Имитация анализа (позже заменим на вызов speaking-core)
        skill = "speaking"
        cefr_level = random.choice(["A2", "B1", "B1", "B2"])
        score = round(random.uniform(65, 95), 1)

        # Сохраняем в БД
        save_progress(skill, cefr_level, score)

        # Показываем результат
        self.status_label.setText(f"✅ Уровень: {cefr_level} ({score}%)")
        QMessageBox.information(
            self,
            "Результат",
            f"Навык: {skill.upper()}\nУровень: {cefr_level}\nСчёт: {score}%"
        )
        self.start_btn.setEnabled(True)
        self.start_btn.setText("🔄 Повторить")


class TodayTab(QWidget):
    progress_updated = Signal()  # ← добавь в начало класса

    def on_start_clicked(self):
        # ... существующий код ...

        # После сохранения прогресса:
        self.progress_updated.emit()  # ← эмитируем сигнал