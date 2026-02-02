from PySide6.QtWidgets import QWidget, QHBoxLayout
from ui.widgets.article_list import ArticleListWidget
from ui.widgets.article_reader import ArticleReaderWidget


class ReadingTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout()

        # Список статей (30% ширины)
        self.article_list = ArticleListWidget()
        self.article_list.setFixedWidth(350)

        # Читалка (70% ширины)
        self.article_reader = ArticleReaderWidget()

        # Связь: клик по статье → отображение контента
        self.article_list.article_selected.connect(self.article_reader.set_article)

        layout.addWidget(self.article_list)
        layout.addWidget(self.article_reader, 1)

        self.setLayout(layout)