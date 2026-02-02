import pyttsx3


class TextToSpeechEngine:
    """
    Offline TTS engine (engine-level).
    """

    def __init__(self, rate: int = 170):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", rate)

    def speak(self, text: str) -> None:
        if not text:
            return
        self.engine.say(text)
        self.engine.runAndWait()
