from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QLabel, QPushButton
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from content.rss_fetcher import get_articles, fetch_articles
from db.database import get_user_level  # ← новый импорт


class ArticleListWidget(QWidget):
    article_selected = Signal(str, str, str, int)  # title, content, url, article_id

    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.load_articles()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Заголовок
        title = QLabel("📰 Статьи для чтения")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(title)

        # Кнопка обновления
        self.refresh_btn = QPushButton("🔄 Обновить контент")
        self.refresh_btn.clicked.connect(self.on_refresh)
        layout.addWidget(self.refresh_btn)

        # Список статей
        self.list_widget = QListWidget()
        self.list_widget.itemClicked.connect(self.on_item_clicked)
        layout.addWidget(self.list_widget)

        self.setLayout(layout)

    def load_articles(self):
        """Загружает статьи из БД с фильтрацией по уровню пользователя"""
        self.list_widget.clear()

        # Получаем уровень пользователя из БД
        user_level = get_user_level()

        # Получаем отфильтрованные статьи
        articles = get_articles(user_level=user_level, limit=15)

        if not articles:
            self.list_widget.addItem(f"Нет статей для уровня {user_level}. Нажмите «Обновить контент»")
            self.refresh_btn.setText(f"🔄 Уровень: {user_level}")
            return

        # Отображаем статьи с бейджами уровня
        for art in articles:
            art_id, source, title, content, url, level, date = art

            # Бейдж уровня
            badge = "🟢" if level == "A1" else "🟡" if level == "A2" else "🟠" if level == "B1" else "🔴"
            item_text = f"{badge} [{source.upper()}] {title}"

            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, (art_id, title, content, url))
            self.list_widget.addItem(item)

        # Обновляем текст кнопки с уровнем
        self.refresh_btn.setText(f"🔄 Уровень: {user_level}")

    def on_refresh(self):
        """Обновляет контент из RSS"""
        self.refresh_btn.setEnabled(False)
        self.refresh_btn.setText("⏳ Загрузка...")

        saved = fetch_articles()

        self.load_articles()
        self.refresh_btn.setEnabled(True)

    def on_item_clicked(self, item):
        """Эмитирует сигнал при клике на статью"""
        data = item.data(Qt.UserRole)
        if data:
            art_id, title, content, url = data
            self.article_selected.emit(title, content, url, art_id)