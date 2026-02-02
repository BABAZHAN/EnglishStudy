import sounddevice as sd
from scipy.io.wavfile import write
from pathlib import Path
import time


class MicrophoneInput:
    """
    Records audio from the system microphone and saves it to a WAV file.
    """

    def record(
        self,
        output_path: str,
        duration_sec: int = 10,
        sample_rate: int = 16000,
    ) -> str:
        """
        Records audio and saves it to output_path.
        Returns the path to the recorded file.
        """

        print(f"🎤 Recording for {duration_sec} seconds...")
        audio = sd.rec(
            int(duration_sec * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype="int16",
        )
        sd.wait()

        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        write(str(path), sample_rate, audio)
        print(f"✅ Audio saved to {path}")

        return str(path)
