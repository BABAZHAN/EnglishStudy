import random
from typing import Dict


SPEAKING_QUESTIONS = {
    "A2": [
        "Tell me about your daily routine.",
        "Describe your favorite hobby.",
    ],
    "B1": [
        "Describe a problem you recently faced and how you solved it.",
        "Talk about a place you would like to visit and why.",
    ],
    "B2": [
        "Do you think technology makes our lives better or worse? Why?",
        "Describe a situation where you had to make an important decision.",
    ],
}


def get_speaking_question(level: str = "B1") -> Dict[str, str]:
    questions = SPEAKING_QUESTIONS.get(level, SPEAKING_QUESTIONS["B1"])
    return {
        "level": level,
        "question": random.choice(questions),
    }
