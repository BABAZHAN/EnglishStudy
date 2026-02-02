from typing import Dict, Any, List
from faster_whisper import WhisperModel


class SpeechToTextEngine:
    """
    Speech-to-Text engine based on faster-whisper.
    Uses lazy model loading for performance and testability.
    """

    def __init__(
        self,
        model_size: str = "small",
        device: str = "cpu",
        compute_type: str = "int8"
    ) -> None:
        self.model_size = model_size
        self.device = device
        self.compute_type = compute_type
        self._model: WhisperModel | None = None

    def _load_model(self) -> None:
        if self._model is None:
            self._model = WhisperModel(
                self.model_size,
                device=self.device,
                compute_type=self.compute_type
            )

    def transcribe(self, audio_path: str) -> Dict[str, Any]:
        self._load_model()

        segments, info = self._model.transcribe(
            audio_path,
            beam_size=5,
            vad_filter=True
        )

        text_parts: List[str] = []
        segment_data: List[Dict[str, Any]] = []

        for segment in segments:
            text_parts.append(segment.text)
            segment_data.append({
                "start": segment.start,
                "end": segment.end,
                "text": segment.text
            })

        return {
            "text": " ".join(text_parts).strip(),
            "segments": segment_data,
            "language": info.language
        }
