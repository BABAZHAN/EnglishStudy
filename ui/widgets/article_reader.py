from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextBrowser, QPushButton, QHBoxLayout, QFrame
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QFont, QDesktopServices
from content.text_analyzer import get_word_stats
import random
from PySide6.QtWidgets import QMessageBox
from db.database import save_reading_progress


class ArticleReaderWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.set_empty_state()
        self.current_url = None

    def setup_ui(self):
        layout = QVBoxLayout()

        # Заголовок
        self.title_label = QLabel()
        self.title_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.title_label.setWordWrap(True)
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)

        # Контент
        self.content_browser = QTextBrowser()
        self.content_browser.setOpenExternalLinks(True)
        self.content_browser.setStyleSheet("""
            QTextBrowser {
                background-color: #f9f9f9;
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 15px;
                font-size: 15px;
                line-height: 1.5;
            }
        """)
        layout.addWidget(self.content_browser)

        # Панель статистики
        self.stats_frame = QFrame()
        self.stats_frame.setFrameShape(QFrame.StyledPanel)
        self.stats_frame.setStyleSheet("background-color: #f0f0f0; border-radius: 5px;")
        self.stats_layout = QVBoxLayout(self.stats_frame)

        self.level_label = QLabel()
        self.level_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.level_label.setAlignment(Qt.AlignCenter)

        self.stats_layout.addWidget(self.level_label)
        self.stats_layout.addSpacing(5)

        # Кнопка "Прочитано ✓"
        self.done_btn = QPushButton("✅ Прочитано (оценить понимание)")
        self.done_btn.clicked.connect(self.on_done_clicked)  # ← теперь метод существует!
        self.done_btn.setVisible(False)
        self.done_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        layout.addWidget(self.done_btn)

        # Статистика слов
        self.word_stats = QLabel()
        self.word_stats.setFont(QFont("Arial", 11))
        self.word_stats.setAlignment(Qt.AlignCenter)

        self.stats_layout.addWidget(self.word_stats)

        layout.addWidget(self.stats_frame)

        # Кнопка "Открыть оригинал"
        self.open_btn = QPushButton("🌐 Открыть оригинал")
        self.open_btn.clicked.connect(self.on_open_original)
        self.open_btn.setVisible(False)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.open_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        self.setLayout(layout)


    def set_article(self, title: str, content: str, url: str, article_id: int = None):
        self.title_label.setText(title)
        self.content_browser.setHtml(f"<div style='max-width: 800px; margin: 0 auto;'>{content}</div>")
        self.open_btn.setVisible(True)
        self.done_btn.setVisible(True)
        self.current_url = url
        self.current_article_id = article_id

        # Статистика
        stats = get_word_stats(content)
        level = stats["estimated_level"]
        self.level_label.setText(f"Уровень текста: {level}")

        # Цветовая индикация
        if level == "A1":
            self.level_label.setStyleSheet("color: #4CAF50;")
        elif level == "A2":
            self.level_label.setStyleSheet("color: #FFC107;")
        elif level == "B1":
            self.level_label.setStyleSheet("color: #FF9800;")
        else:
            self.level_label.setStyleSheet("color: #F44336;")

        self.word_stats.setText(
            f"Слов: {stats['word_count']} | Уникальных: {stats['unique_words']}"
        )

    def on_done_clicked(self):
        """Сохраняет результат чтения"""
        if not hasattr(self, 'current_article_id'):
            return

        # Имитация оценки понимания
        comprehension = round(random.uniform(70, 95), 1)
        level = self.level_label.text().replace("Уровень текста: ", "")

        # Сохраняем в БД
        save_reading_progress(self.current_article_id, level, comprehension)

        # Уведомление
        QMessageBox.information(
            self,
            "✅ Чтение завершено",
            f"Уровень текста: {level}\nПонимание: {comprehension}%\n\n"
            "Результат сохранён в прогресс!"
        )

        # Скрываем кнопку
        self.done_btn.setVisible(False)


    def set_empty_state(self):
        self.title_label.setText("Выберите статью для чтения")
        self.content_browser.setHtml(
            "<p style='color: #888; text-align: center;'>← Слева выберите статью из списка</p>")
        self.open_btn.setVisible(False)
        self.current_url = None

    def on_open_original(self):
        if self.current_url:
            QDesktopServices.openUrl(QUrl(self.current_url))