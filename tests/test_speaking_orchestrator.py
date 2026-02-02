def test_grammar_feedback(monkeypatch):
    from core.orchestrator.speaking_orchestrator import SpeakingOrchestrator

    orch = SpeakingOrchestrator()

    orch.microphone.record = lambda *a, **k: "tests/audio/sample.mp3"
    orch.stt_engine.transcribe = lambda p: {
        "text": "I am agree that people is very much happy",
        "segments": [
            {"start": 0.0, "end": 4.0, "text": "I am agree that people is very much happy"}
        ],
        "language": "en",
    }

    result = orch.run()

    assert "grammar" in result
    assert len(result["grammar"]) >= 1
