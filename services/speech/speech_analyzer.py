from typing import Dict, Any, List


class SpeechAnalyzer:
    """
    Analyzes speech transcription produced by faster-whisper.
    Computes fluency-related metrics for speaking evaluation.
    """

    def analyze(self, transcript: Dict[str, Any]) -> Dict[str, Any]:
        """
        transcript format:
        {
            "text": str,
            "segments": [
                {"start": float, "end": float, "text": str}
            ],
            "language": str
        }
        """

        segments: List[Dict[str, Any]] = transcript.get("segments", [])
        full_text: str = transcript.get("text", "")

        if not segments:
            return self._empty_result()

        # ---- Time calculations ----
        total_speech_time = segments[-1]["end"] - segments[0]["start"]

        pause_durations = self._calculate_pauses(segments)
        total_pause_time = sum(pause_durations)

        # ---- Text calculations ----
        word_count = len(full_text.split())

        # ---- Metrics ----
        words_per_minute = (
            word_count / total_speech_time * 60
            if total_speech_time > 0
            else 0
        )

        pause_ratio = (
            total_pause_time / total_speech_time
            if total_speech_time > 0
            else 0
        )

        avg_pause_length = (
            sum(pause_durations) / len(pause_durations)
            if pause_durations
            else 0
        )

        fluency_score = self._calculate_fluency(
            words_per_minute,
            pause_ratio,
            avg_pause_length
        )

        return {
            "word_count": word_count,
            "speech_time_sec": round(total_speech_time, 2),
            "pause_time_sec": round(total_pause_time, 2),
            "words_per_minute": round(words_per_minute, 1),
            "pause_ratio": round(pause_ratio, 3),
            "average_pause_sec": round(avg_pause_length, 2),
            "fluency_score": round(fluency_score, 2),
        }

    # ------------------------------------------------------------------

    def _calculate_pauses(self, segments: List[Dict[str, Any]]) -> List[float]:
        pauses = []
        for i in range(1, len(segments)):
            pause = segments[i]["start"] - segments[i - 1]["end"]
            if pause > 0.15:  # ignore micro-pauses
                pauses.append(pause)
        return pauses

    def _calculate_fluency(
        self,
        wpm: float,
        pause_ratio: float,
        avg_pause: float
    ) -> float:
        """
        Fluency score heuristic (0.0 – 1.0)
        """

        # Ideal ranges for B1–B2
        wpm_score = min(wpm / 160, 1.0)          # 140–160 is good
        pause_penalty = max(0.0, 1 - pause_ratio * 2)
        avg_pause_penalty = max(0.0, 1 - avg_pause / 1.2)

        return max(
            0.0,
            min(1.0, (wpm_score + pause_penalty + avg_pause_penalty) / 3)
        )

    def _empty_result(self) -> Dict[str, Any]:
        return {
            "word_count": 0,
            "speech_time_sec": 0,
            "pause_time_sec": 0,
            "words_per_minute": 0,
            "pause_ratio": 0,
            "average_pause_sec": 0,
            "fluency_score": 0.0,
        }
