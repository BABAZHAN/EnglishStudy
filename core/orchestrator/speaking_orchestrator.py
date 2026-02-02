from services.speech.microphone import MicrophoneInput
from services.speech.stt_engine import SpeechToTextEngine
from services.speech.speech_analyzer import SpeechAnalyzer
from services.speech.feedback import SpeechFeedbackGenerator
from services.speech.cefr import estimate_cefr
from services.speech.pronunciation import PronunciationAnalyzer
from services.speech.grammar_analyzer import GrammarAnalyzer


class SpeakingOrchestrator:
    """
    Orchestrates the full speaking evaluation pipeline.
    Independent from UI and database.
    """

    def __init__(self):
        self.microphone = MicrophoneInput()
        self.stt_engine = SpeechToTextEngine(
            model_size="small",
            device="cpu",
            compute_type="int8"
        )
        self.analyzer = SpeechAnalyzer()
        self.feedback_generator = SpeechFeedbackGenerator()
        self.pronunciation_analyzer = PronunciationAnalyzer()
        self.grammar_analyzer = GrammarAnalyzer()

    def run(
        self,
        audio_path: str = "tests/audio/speaking_attempt.wav",
        duration_sec: int = 8
    ) -> dict:
        """
        Pipeline:
        1. Record audio
        2. Transcribe
        3. Analyze fluency
        4. Estimate CEFR
        5. Generate feedback
        """

        # 1. Record
        recorded_path = self.microphone.record(
            output_path=audio_path,
            duration_sec=duration_sec
        )

        # 2. STT
        transcript = self.stt_engine.transcribe(recorded_path)

        if not transcript.get("text"):
            return {"error": "No speech detected"}

        # 3. Analysis
        analysis = self.analyzer.analyze(transcript)
        pronunciation = self.pronunciation_analyzer.analyze(transcript)
        grammar_issues = self.grammar_analyzer.analyze(transcript["text"])

        # 4. CEFR
        cefr_result = estimate_cefr(analysis)

        # 5. Feedback
        feedback = self.feedback_generator.generate(analysis)

        return {
            "transcript": transcript["text"],
            "analysis": analysis,
            "pronunciation": pronunciation,
            "grammar": grammar_issues,
            "cefr": cefr_result,
            "feedback": feedback,
        }

