from typing import Dict


class SpeechFeedbackGenerator:
    """
    Generates pedagogical feedback based on speech fluency analysis.
    """

    def generate(self, analysis: Dict[str, float]) -> Dict[str, str]:
        fluency = analysis.get("fluency_score", 0.0)
        wpm = analysis.get("words_per_minute", 0.0)
        pause_ratio = analysis.get("pause_ratio", 0.0)

        # ---- Overall assessment ----
        if fluency >= 0.75:
            level = "Very good"
            summary = "Your speech was fluent and confident."
        elif fluency >= 0.55:
            level = "Good"
            summary = "Your speech was generally fluent but with some pauses."
        elif fluency >= 0.35:
            level = "Needs improvement"
            summary = "Your speech had noticeable pauses and hesitations."
        else:
            level = "Poor"
            summary = "Your speech lacked fluency and flow."

        # ---- Advice ----
        advice_parts = []

        if wpm < 90:
            advice_parts.append("Try to speak a bit faster.")
        elif wpm > 180:
            advice_parts.append("Try to slow down slightly.")

        if pause_ratio > 0.35:
            advice_parts.append("Work on reducing long pauses.")

        if not advice_parts:
            advice_parts.append("Keep practicing at this pace.")

        return {
            "level": level,
            "summary": summary,
            "advice": " ".join(advice_parts),
        }
