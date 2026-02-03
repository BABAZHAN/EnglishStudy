from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QLabel, QPushButton
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from content.rss_fetcher import get_articles, fetch_articles


class ArticleListWidget(QWidget):
    article_selected = Signal(str, str, str, int)  # title, content, url

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
        """Загружает статьи из БД"""
        self.list_widget.clear()
        articles = get_articles(limit=15)

        if not articles:
            self.list_widget.addItem("Нет статей. Нажмите «Обновить контент»")
            return

        for art_id, source, title, content, url, date in articles:
            item = QListWidgetItem(f"[{source.upper()}] {title}")
            item.setData(Qt.UserRole, (art_id, title, content, url))
            self.list_widget.addItem(item)

    def on_refresh(self):
        """Обновляет контент из RSS"""
        self.refresh_btn.setEnabled(False)
        self.refresh_btn.setText("⏳ Загрузка...")

        saved = fetch_articles()

        self.load_articles()
        self.refresh_btn.setEnabled(True)
        self.refresh_btn.setText(f"✅ +{saved} новых" if saved else "🔄 Обновить контент")

    def on_item_clicked(self, item):
        data = item.data(Qt.UserRole)
        if data:
            art_id, title, content, url = data
            self.article_selected.emit(title, content, url, art_id)