from typing import Dict, Any, List
from faster_whisper import WhisperModel


class SpeechToTextEngine:
    """
    Speech-to-Text engine based on faster-whisper.
    """

    def __init__(
        self,
        model_size: str = "small",
        device: str = "cpu",
        compute_type: str = "int8"
    ) -> None:
        """
        model_size: tiny | base | small | medium
        device: cpu | cuda
        compute_type: int8 | float16 | float32
        """
        self.model = WhisperModel(
            model_size,
            device=device,
            compute_type=compute_type
        )

    def transcribe(self, audio_path: str) -> Dict[str, Any]:
        """
        Transcribes audio file to text.

        Returns:
        {
            "text": str,
            "segments": List[dict],
            "language": str
        }
        """
        segments, info = self.model.transcribe(audio_path)

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
