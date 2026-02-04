from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QMessageBox, QProgressBar
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont


class PlacementTestDialog(QDialog):
    level_detected = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🎯 Определение уровня (5 минут)")
        self.resize(700, 500)

        # ВАЖНО: сначала инициализируем данные
        self.questions = self._get_questions()
        self.current_step = 0
        self.answers = []
        self.selected_answer = None

        self.setup_ui()

    def _get_questions(self):
        return [
            {
                "type": "reading",
                "text": "Прочитайте текст:\n\nClimate change is one of the biggest challenges facing our planet today. Scientists warn that if we don't reduce carbon emissions soon, the consequences could be irreversible.",
                "question": "Что означает 'irreversible' в этом контексте?",
                "options": [
                    "Можно легко исправить",
                    "Нельзя изменить обратно",
                    "Происходит каждый год",
                    "Связано с наукой"
                ],
                "correct": 1
            },
            {
                "type": "grammar",
                "text": "Выберите правильный вариант:",
                "question": "If I ___ rich, I would travel the world.",
                "options": [
                    "am",
                    "was",
                    "were",
                    "will be"
                ],
                "correct": 2
            },
            {
                "type": "vocabulary",
                "text": "Какое слово НЕ подходит к теме 'работа'?",
                "options": [
                    "colleague",
                    "deadline",
                    "beach",
                    "promotion"
                ],
                "correct": 2
            },
            {
                "type": "speaking",
                "text": "🗣️ Ответьте на вопрос (запись 5 сек):\n\nWhat did you do last weekend?",
                "question": "Оценка: беглость + грамматика + словарь",
                "correct": None
            },
            {
                "type": "reading",
                "text": "Прочитайте диалог:\n\nA: 'I've been working here since 2020.'\nB: 'Really? I ___ here for only six months.'",
                "question": "Какое слово пропущено?",
                "options": [
                    "work",
                    "worked",
                    "have worked",
                    "had worked"
                ],
                "correct": 2
            }
        ]

    def setup_ui(self):
        layout = QVBoxLayout()

        # Прогресс
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, len(self.questions))
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        # Текст вопроса
        self.text_label = QLabel()
        self.text_label.setFont(QFont("Arial", 13))
        self.text_label.setWordWrap(True)
        layout.addWidget(self.text_label)

        # Варианты ответов
        self.options_layout = QVBoxLayout()
        layout.addLayout(self.options_layout)

        # Кнопка действия
        self.action_btn = QPushButton("Далее")
        self.action_btn.setEnabled(False)
        self.action_btn.clicked.connect(self.handle_action)
        layout.addWidget(self.action_btn)

        self.setLayout(layout)
        self.show_question(0)

    def show_question(self, step):
        if step >= len(self.questions):
            self.finish_test()
            return

        self.current_step = step
        q = self.questions[step]

        self.progress_bar.setValue(step)
        self.text_label.setText(q["text"])

        # Очистка вариантов
        while self.options_layout.count():
            child = self.options_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Отображение вариантов
        if q["type"] == "speaking":
            record_btn = QPushButton("🎤 Записать ответ (5 сек)")
            record_btn.clicked.connect(self.record_speaking)
            self.options_layout.addWidget(record_btn)
            self.action_btn.setText("Пропустить")
            self.action_btn.setEnabled(True)
        elif "options" in q:
            for idx, option in enumerate(q["options"]):
                btn = QPushButton(f"{chr(65 + idx)}. {option}")
                btn.clicked.connect(lambda _, i=idx: self.select_answer(i))
                self.options_layout.addWidget(btn)
            self.action_btn.setText("Далее")
            self.action_btn.setEnabled(False)

    def select_answer(self, answer_idx):
        self.selected_answer = answer_idx
        self.action_btn.setEnabled(True)

    def record_speaking(self):
        QMessageBox.information(self, "🎤 Запись",
                                "Функция записи будет доступна после полной интеграции с микрофоном.\nПока что оцениваем по другим вопросам.")
        self.answers.append({"type": "speaking", "score": 0.75})
        self.handle_action()

    def handle_action(self):
        q = self.questions[self.current_step]

        if q["type"] != "speaking" and self.selected_answer is not None:
            is_correct = self.selected_answer == q["correct"]
            self.answers.append({"type": q["type"], "correct": is_correct})
            self.selected_answer = None

        self.show_question(self.current_step + 1)

    def finish_test(self):
        correct_count = sum(1 for a in self.answers if a.get("correct", False))
        speaking_scores = [a["score"] for a in self.answers if a.get("type") == "speaking"]
        avg_speaking = sum(speaking_scores) / len(speaking_scores) if speaking_scores else 0.7

        # Определение уровня
        if correct_count >= 4 and avg_speaking > 0.8:
            level = "B1"
        elif correct_count >= 3:
            level = "A2"
        else:
            level = "A1"

        QMessageBox.information(
            self,
            f"✅ Ваш уровень: {level}",
            f"Правильных ответов: {correct_count}/5\n"
            f"Оценка говорения: {avg_speaking * 100:.0f}%\n\n"
            "Теперь вы получите персональный план обучения до B2!"
        )

        self.level_detected.emit(level)
        self.accept()