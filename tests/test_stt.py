from services.speech.stt_engine import SpeechToTextEngine
from pathlib import Path


def test_stt():
    audio_path = Path("tests/audio/sample.mp3")

    stt = SpeechToTextEngine(model_size="small")
    result = stt.transcribe(str(audio_path))

    print("TEXT:", result["text"])
    assert isinstance(result["text"], str)
    assert len(result["text"]) > 0
