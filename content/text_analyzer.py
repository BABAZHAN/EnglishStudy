from wordfreq import zipf_frequency
from collections import Counter


def estimate_text_level(text: str) -> str:
    """Оценивает уровень сложности текста (A1-B2)"""
    words = [w.lower().strip(".,?!;:'\"()[]{}") for w in text.split()]
    words = [w for w in words if w]

    a1_count, b1_count, b2_count = 0, 0, 0
    total = len(words)

    for word in words:
        freq = zipf_frequency(word, 'en')
        if freq > 5.5:
            a1_count += 1
        elif freq > 4.0:
            b1_count += 1
        else:
            b2_count += 1

    a1_percent = a1_count / total if total else 0
    b1_percent = b1_count / total if total else 0

    if a1_percent > 0.7:
        return "A1"
    elif a1_percent > 0.4 and b1_percent > 0.3:
        return "A2"
    elif b1_percent > 0.5:
        return "B1"
    else:
        return "B2"


def get_word_stats(text: str) -> dict:
    """Возвращает статистику по словам"""
    words = [w.lower().strip(".,?!;:'\"()[]{}") for w in text.split()]
    words = [w for w in words if w]

    freq_counter = Counter(words)
    top_words = freq_counter.most_common(10)

    return {
        "word_count": len(words),
        "unique_words": len(freq_counter),
        "top_words": top_words,
        "estimated_level": estimate_text_level(text)
    }