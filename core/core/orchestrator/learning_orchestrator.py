from services.speech.microphone import MicrophoneInput
from services.speech.stt_engine import SpeechToTextEngine
from services.speech.speech_analyzer import SpeechAnalyzer


class LearningOrchestrator:
    def __init__(self) -> None:
        self.microphone = MicrophoneInput()
        self.stt = SpeechToTextEngine(model_size="small")
        self.analyzer = SpeechAnalyzer()

    def handle_speaking(self) -> dict:
        """
        Full speaking pipeline:
        microphone → STT → analysis
        """

        audio_path = self.microphone.record(
            output_path="data/audio/speaking.wav",
            duration_sec=10,
        )

        transcript = self.stt.transcribe(audio_path)
        analysis = self.analyzer.analyze(transcript)

        return {
            "transcript": transcript["text"],
            "analysis": analysis,
        }
