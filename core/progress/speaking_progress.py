from typing import List, Dict


class SpeakingProgressAnalyzer:
    """
    Analyzes speaking progress across multiple sessions.
    Engine-only, no storage logic.
    """

    def analyze(self, sessions: List[Dict[str, object]]) -> Dict[str, object]:
        """
        sessions: list of exam results (SpeakingExamOrchestrator output)

        Returns progress analytics.
        """

        if len(sessions) < 2:
            return {
                "status": "not_enough_data",
                "message": "At least two sessions are required to analyze progress."
            }

        scores = [s["final_score"] for s in sessions]
        fluency_scores = [s["result"]["analysis"]["fluency_score"] for s in sessions]
        pronunciation_scores = [
            s["result"]["pronunciation"]["pronunciation_score"] for s in sessions
        ]

        score_delta = round(scores[-1] - scores[0], 2)
        fluency_delta = round(fluency_scores[-1] - fluency_scores[0], 2)
        pronunciation_delta = round(pronunciation_scores[-1] - pronunciation_scores[0], 2)

        trend = self._detect_trend(score_delta)

        return {
            "status": "ok",
            "sessions_count": len(sessions),
            "overall_progress": {
                "score_change": score_delta,
                "fluency_change": fluency_delta,
                "pronunciation_change": pronunciation_delta,
                "trend": trend
            },
            "recommendation": self._build_recommendation(
                score_delta,
                fluency_delta,
                pronunciation_delta
            )
        }

    # --------------------------------------------------

    def _detect_trend(self, delta: float) -> str:
        if delta > 0.1:
            return "improving"
        if delta < -0.1:
            return "declining"
        return "stable"

    def _build_recommendation(
        self,
        score_delta: float,
        fluency_delta: float,
        pronunciation_delta: float
    ) -> str:
        if score_delta > 0.1:
            return "Great progress! Keep practicing regularly."
        if fluency_delta < 0:
            return "Focus more on speaking fluently without long pauses."
        if pronunciation_delta < 0:
            return "Work on clearer pronunciation and rhythm."
        return "Your level is stable. Try increasing speaking difficulty."
