from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QTextBrowser
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class LevelResultDialog(QDialog):
    def __init__(self, level: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"📊 Ваш уровень: {level}")
        self.resize(750, 600)
        self.setup_ui(level)

    def setup_ui(self, level):
        layout = QVBoxLayout()

        # Заголовок
        title = QLabel(f"🎯 Ваш текущий уровень: <b>{level}</b>")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        layout.addSpacing(20)

        # Цель
        target = QLabel("Цель: <b>B2</b> (Upper-Intermediate)")
        target.setFont(QFont("Arial", 18))
        target.setAlignment(Qt.AlignCenter)
        layout.addWidget(target)
        layout.addSpacing(30)

        # Персональный план
        plan_text = self._get_plan(level)
        plan_browser = QTextBrowser()
        plan_browser.setHtml(plan_text)
        plan_browser.setStyleSheet("""
            QTextBrowser {
                background-color: #f9f9f9;
                border: 1px solid #ddd;
                border-radius: 10px;
                padding: 20px;
                font-size: 15px;
                line-height: 1.6;
            }
        """)
        layout.addWidget(plan_browser)

        # Кнопка старта
        start_btn = QPushButton("🚀 Начать обучение")
        start_btn.setFixedSize(250, 60)
        start_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border-radius: 15px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        start_btn.clicked.connect(self.accept)
        layout.addWidget(start_btn, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def _get_plan(self, level: str) -> str:
        if level == "A1":
            weeks = 24
            focus = "Базовая лексика (1000 слов) + простые предложения"
            daily = "20 минут чтения + 10 минут говорения"
        elif level == "A2":
            weeks = 16
            focus = "Повседневные ситуации + прошедшее время"
            daily = "30 минут чтения + 15 минут говорения"
        else:  # B1
            weeks = 12
            focus = "Сложные конструкции + идиомы"
            daily = "40 минут чтения + 20 минут говорения"

        return f"""
        <h2>📅 Персональный план до B2</h2>
        <p><b>Срок:</b> ~{weeks} недель при регулярных занятиях</p>
        <p><b>Фокус на:</b> {focus}</p>
        <p><b>Ежедневно:</b> {daily}</p>

        <h3>🔥 Еженедельный цикл</h3>
        <ul>
            <li><b>Понедельник:</b> Новые слова + карточки</li>
            <li><b>Вторник:</b> Чтение новостей (BBC/VOA)</li>
            <li><b>Среда:</b> Говорение (микрофон + фидбек)</li>
            <li><b>Четверг:</b> Грамматика + упражнения</li>
            <li><b>Пятница:</b> Аудирование (подкасты)</li>
            <li><b>Суббота:</b> Повторение недели</li>
            <li><b>Воскресенье:</b> Отдых или фильм на английском</li>
        </ul>

        <h3>📈 Как отслеживать прогресс</h3>
        <p>Во вкладке <b>«Прогресс»</b> вы увидите:</p>
        <ul>
            <li>График роста уровня</li>
            <li>Слабые места в грамматике</li>
            <li>Рекомендации по улучшению</li>
        </ul>
        """