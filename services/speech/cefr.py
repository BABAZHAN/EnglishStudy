from typing import Dict, List


def estimate_cefr(analysis: Dict[str, float]) -> Dict[str, object]:
    fluency = analysis.get("fluency_score", 0.0)
    wpm = analysis.get("words_per_minute", 0.0)
    pause_ratio = analysis.get("pause_ratio", 1.0)

    strengths: List[str] = []
    weaknesses: List[str] = []

    # ---- Decision logic ----
    if fluency >= 0.75 and wpm >= 120 and pause_ratio < 0.3:
        level = "B2"
    elif fluency >= 0.55 and wpm >= 100:
        level = "B1"
    elif fluency >= 0.35:
        level = "A2"
    else:
        level = "A1"

    # ---- Strengths ----
    if wpm >= 110:
        strengths.append("Good speaking speed")
    if pause_ratio < 0.3:
        strengths.append("Few long pauses")
    if fluency >= 0.6:
        strengths.append("Overall fluent speech")

    # ---- Weaknesses ----
    if wpm < 90:
        weaknesses.append("Speaking speed is too slow")
    if pause_ratio > 0.4:
        weaknesses.append("Too many long pauses")
    if fluency < 0.5:
        weaknesses.append("Speech lacks fluency")

    # ---- Explanation ----
    explanation = (
        f"Your speaking level was estimated as {level} "
        f"based on fluency score ({round(fluency, 2)}), "
        f"speaking speed ({round(wpm, 1)} words per minute), "
        f"and pause ratio ({round(pause_ratio, 2)})."
    )

    return {
        "level": level,
        "explanation": explanation,
        "strengths": strengths,
        "weaknesses": weaknesses,
    }
