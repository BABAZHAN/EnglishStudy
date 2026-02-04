from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, QProgressBar
from PySide6.QtCore import Qt, Signal, QThread, QObject
from PySide6.QtGui import QFont
from core.orchestrator.speaking_orchestrator import SpeakingOrchestrator
from db.database import save_progress


class SpeakingWorker(QObject):
    finished = Signal(dict)
    error = Signal(str)
    status_update = Signal(str)

    def __init__(self, duration_sec: int = 8):
        super().__init__()
        self.duration_sec = duration_sec
        self.orchestrator = SpeakingOrchestrator()

    def run(self):
        try:
            self.status_update.emit("🎤 Запись речи (8 сек)...")
            result = self.orchestrator.run(duration_sec=self.duration_sec)

            if "error" in result or not result.get("transcript"):
                self.error.emit("Не обнаружено речи. Попробуйте говорить громче.")
                return

            # Сохраняем в БД
            cefr_level = result["cefr"].get("level", "A2")
            fluency_score = result["analysis"].get("fluency", 0.0) * 100
            save_progress("speaking", cefr_level, fluency_score)

            self.finished.emit(result)
        except Exception as e:
            self.error.emit(f"{type(e).__name__}: {str(e)}")


class TodayTab(QWidget):
    progress_updated = Signal()

    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.worker_thread = None

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Заголовок
        title = QLabel("🗣️ Тренировка говорения")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        layout.addStretch()
        layout.addWidget(title, alignment=Qt.AlignCenter)
        layout.addSpacing(20)

        # Статус
        self.status_label = QLabel("Готов к тренировке")
        self.status_label.setFont(QFont("Arial", 14))
        layout.addWidget(self.status_label, alignment=Qt.AlignCenter)
        layout.addSpacing(10)

        # Прогресс-бар
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setVisible(False)
        self.progress_bar.setFixedWidth(300)
        layout.addWidget(self.progress_bar, alignment=Qt.AlignCenter)
        layout.addSpacing(30)

        # Кнопка
        self.start_btn = QPushButton("🎤 Начать тренировку")
        self.start_btn.setFixedSize(320, 75)
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 18px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #a5d6a7;
            }
        """)
        self.start_btn.clicked.connect(self.on_start_clicked)
        layout.addWidget(self.start_btn, alignment=Qt.AlignCenter)
        layout.addStretch()

        self.setLayout(layout)

    def on_start_clicked(self):
        if self.worker_thread and self.worker_thread.isRunning():
            return

        self.start_btn.setEnabled(False)
        self.start_btn.setText("⏹️ Остановить запись")
        self.progress_bar.setVisible(True)
        self.status_label.setText("🎤 Запись... Говорите!")

        self.worker_thread = QThread()
        self.worker = SpeakingWorker(duration_sec=8)
        self.worker.moveToThread(self.worker_thread)

        self.worker_thread.started.connect(self.worker.run)
        self.worker.status_update.connect(self.status_label.setText)
        self.worker.finished.connect(self.on_analysis_finished)
        self.worker.error.connect(self.on_analysis_error)
        self.worker.finished.connect(self.cleanup_thread)
        self.worker.error.connect(self.cleanup_thread)

        self.worker_thread.start()

    def cleanup_thread(self):
        if self.worker_thread:
            self.worker_thread.quit()
            self.worker_thread.wait()
            self.worker_thread = None

    def on_analysis_finished(self, result):
        self.progress_bar.setVisible(False)
        self.start_btn.setEnabled(True)
        self.start_btn.setText("🔄 Повторить тренировку")

        # Безопасная обработка фидбека (любой тип данных)
        feedback = result.get('feedback', 'Нет подробного фидбека')
        if not isinstance(feedback, str):
            try:
                feedback = str(feedback)
            except:
                feedback = "Фидбек недоступен"

        feedback_display = feedback[:200] + "..." if len(feedback) > 200 else feedback

        # Формируем сообщение
        cefr_level = result["cefr"].get("level", "A2")
        fluency = result["analysis"].get("fluency", 0.0) * 100
        transcript = result["transcript"].strip() or "Транскрипция не распознана"
        transcript_display = transcript[:120] + "..." if len(transcript) > 120 else transcript

        QMessageBox.information(
            self,
            f"✅ Результат: Уровень {cefr_level}",
            f"Беглость: {fluency:.1f}%\n\n"
            f"Транскрипция:\n{transcript_display}\n\n"
            f"Совет:\n{feedback_display}"
        )

        self.status_label.setText(f"✅ Уровень {cefr_level} ({fluency:.0f}%)")
        self.progress_updated.emit()

    def on_analysis_error(self, error_msg):
        self.progress_bar.setVisible(False)
        self.start_btn.setEnabled(True)
        self.start_btn.setText("🎤 Повторить тренировку")
        self.status_label.setText("❌ Ошибка записи")
        QMessageBox.warning(
            self,
            "Ошибка анализа",
            f"Не удалось проанализировать речь:\n\n{error_msg}\n\n"
            "💡 Совет: убедитесь, что микрофон подключён и разрешён в системе."
        )