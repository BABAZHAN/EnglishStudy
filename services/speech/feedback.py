from typing import Dict


class SpeechFeedbackGenerator:
    """
    Generates feedback for the user based on speech analysis.
    """

    def generate(self, analysis: Dict[str, any]) -> Dict[str, str]:
        """
        Returns feedback messages.
        """
        raise NotImplementedError
