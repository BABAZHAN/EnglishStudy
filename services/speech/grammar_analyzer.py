import re
from typing import List, Dict


class GrammarAnalyzer:
    """
    Rule-based grammar analyzer for English speaking.
    Designed as MVP, LLM-ready later.
    """

    RULES = [
        {
            "pattern": r"\bi am agree\b",
            "message": "Use 'I agree' instead of 'I am agree'.",
            "type": "verb_form",
        },
        {
            "pattern": r"\bhe have\b",
            "message": "Use 'he has' instead of 'he have'.",
            "type": "subject_verb_agreement",
        },
        {
            "pattern": r"\bvery much\b",
            "message": "Consider using a stronger adjective instead of 'very much'.",
            "type": "lexical_choice",
        },
        {
            "pattern": r"\bmore better\b",
            "message": "Use 'better' instead of 'more better'.",
            "type": "comparative_form",
        },
        {
            "pattern": r"\bpeople is\b",
            "message": "Use 'people are' instead of 'people is'.",
            "type": "subject_verb_agreement",
        },
    ]

    def analyze(self, text: str) -> List[Dict[str, str]]:
        """
        Returns a list of grammar issues:
        {
            "type": str,
            "message": str
        }
        """

        issues = []
        lowered = text.lower()

        for rule in self.RULES:
            if re.search(rule["pattern"], lowered):
                issues.append({
                    "type": rule["type"],
                    "message": rule["message"],
                })

        return issues
