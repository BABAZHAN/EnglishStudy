from typing import Dict, Any, List


class PronunciationAnalyzer:
    """
    Heuristic pronunciation analysis based on Whisper segments.
    """

    def analyze(self, transcript: Dict[str, Any]) -> Dict[str, Any]:
        segments = transcript.get("segments", [])
        text = transcript.get("text", "")

        if not segments or not text:
            return self._empty_result()

        word_count = len(text.split())
        segment_count = len(segments)

        # Average words per segment
        words_per_segment = word_count / segment_count if segment_count else 0

        # Segment duration stats
        durations = [
            seg["end"] - seg["start"] for seg in segments if seg["end"] > seg["start"]
        ]

        avg_segment_duration = (
            sum(durations) / len(durations) if durations else 0
        )

        # Heuristics
        clarity_score = min(words_per_segment / 6, 1.0)
        rhythm_score = min(avg_segment_duration / 2.5, 1.0)

        pronunciation_score = round((clarity_score + rhythm_score) / 2, 2)

        issues: List[str] = []

        if words_per_segment < 2:
            issues.append("Words are spoken too separately")
        if avg_segment_duration > 4.0:
            issues.append("Speech segments are too long")
        if pronunciation_score < 0.4:
            issues.append("Pronunciation lacks clarity")

        return {
            "pronunciation_score": pronunciation_score,
            "avg_words_per_segment": round(words_per_segment, 2),
            "avg_segment_duration": round(avg_segment_duration, 2),
            "issues": issues,
        }

    def _empty_result(self) -> Dict[str, Any]:
        return {
            "pronunciation_score": 0.0,
            "avg_words_per_segment": 0.0,
            "avg_segment_duration": 0.0,
            "issues": ["No speech detected"],
        }
