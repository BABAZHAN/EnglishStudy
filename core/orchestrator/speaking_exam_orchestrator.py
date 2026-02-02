from typing import Dict

from core.orchestrator.speaking_orchestrator import SpeakingOrchestrator
from core.orchestrator.speaking_questions import get_speaking_question


class SpeakingExamOrchestrator:
    """
    Full speaking exam flow:
    question → answer → evaluation → final summary
    """

    def __init__(self, target_level: str = "B1"):
        self.target_level = target_level
        self.speaking_engine = SpeakingOrchestrator()

    def run(self) -> Dict[str, object]:
        # 1. Get question
        question_data = get_speaking_question(self.target_level)

        # 2. Evaluate answer
        speaking_result = self.speaking_engine.run()

        if "error" in speaking_result:
            return {
                "question": question_data,
                "error": speaking_result["error"],
            }

        # 3. Build final summary
        final_score = self._calculate_final_score(speaking_result)

        summary = self._build_summary(
            speaking_result,
            final_score
        )

        return {
            "question": question_data,
            "result": speaking_result,
            "final_score": final_score,
            "summary": summary,
        }

    # -------------------------------------------------

    def _calculate_final_score(self, result: Dict[str, object]) -> float:
        fluency = result["analysis"]["fluency_score"]
        pronunciation = result["pronunciation"]["pronunciation_score"]
        grammar_penalty = len(result["grammar"]) * 0.05

        score = (
            fluency * 0.5 +
            pronunciation * 0.4 -
            grammar_penalty
        )

        return round(max(0.0, min(1.0, score)), 2)

    def _build_summary(
        self,
        result: Dict[str, object],
        score: float
    ) -> str:
        cefr = result["cefr"]["level"]
        grammar_count = len(result["grammar"])

        return (
            f"Your overall speaking score is {score}. "
            f"Your estimated level is {cefr}. "
            f"You made {grammar_count} grammar mistakes. "
            f"Focus on fluency and clearer pronunciation."
        )
