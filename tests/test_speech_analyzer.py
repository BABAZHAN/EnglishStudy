from services.speech.speech_analyzer import SpeechAnalyzer


def test_speech_analyzer_basic():
    transcript = {
        "text": "I would like to talk about artificial intelligence today",
        "segments": [
            {"start": 0.0, "end": 1.5, "text": "I would like"},
            {"start": 2.0, "end": 4.0, "text": "to talk about"},
            {"start": 4.5, "end": 7.0, "text": "artificial intelligence today"},
        ],
        "language": "en",
    }

    analyzer = SpeechAnalyzer()
    result = analyzer.analyze(transcript)

    print(result)

    assert result["words_per_minute"] > 0
    assert 0.0 <= result["fluency_score"] <= 1.0
