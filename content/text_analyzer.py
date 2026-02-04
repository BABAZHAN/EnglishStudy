from wordfreq import zipf_frequency
from collections import Counter

# Пороговые значения для уровней CEFR (на основе Zipf frequency)
CEFR_THRESHOLDS = {
    "A1": 5.8,  # Очень частые слова
    "A2": 5.0,
    "B1": 4.2,
    "B2": 3.5,
    "C1": 2.8
}


def estimate_text_level(text: str) -> str:
    """Оценивает уровень сложности текста (A1-B2) на основе частотности слов"""
    words = [w.lower().strip(".,?!;:'\"()[]{}") for w in text.split()]
    words = [w for w in words if w and w.isalpha()]  # Только буквы

    if not words:
        return "A1"

    # Считаем среднюю частотность слов
    total_freq = 0
    valid_words = 0

    for word in words:
        freq = zipf_frequency(word, 'en')
        if freq > 0:  # Игнорируем неизвестные слова
            total_freq += freq
            valid_words += 1

    avg_freq = total_freq / valid_words if valid_words else 0

    # Определяем уровень по порогам
    if avg_freq >= CEFR_THRESHOLDS["A1"]:
        return "A1"
    elif avg_freq >= CEFR_THRESHOLDS["A2"]:
        return "A2"
    elif avg_freq >= CEFR_THRESHOLDS["B1"]:
        return "B1"
    elif avg_freq >= CEFR_THRESHOLDS["B2"]:
        return "B2"
    else:
        return "B2+"  # Сложный текст


def get_word_stats(text: str) -> dict:
    """Возвращает статистику по словам"""
    words = [w.lower().strip(".,?!;:'\"()[]{}") for w in text.split()]
    words = [w for w in words if w and w.isalpha()]

    freq_counter = Counter(words)
    top_words = freq_counter.most_common(10)

    return {
        "word_count": len(words),
        "unique_words": len(freq_counter),
        "top_words": top_words,
        "estimated_level": estimate_text_level(text),
        "avg_word_length": sum(len(w) for w in words) / len(words) if words else 0
    }


def is_article_suitable(article_level: str, user_level: str) -> bool:
    """
    Проверяет, подходит ли статья под уровень пользователя.
    Правило: статья может быть на 1 уровень сложнее или на 1 уровень проще.
    """
    levels = ["A1", "A2", "B1", "B2", "B2+"]

    try:
        article_idx = levels.index(article_level)
        user_idx = levels.index(user_level if user_level in levels else "A1")

        # Разрешаем статьи: [уровень-1, уровень, уровень+1]
        return abs(article_idx - user_idx) <= 1
    except ValueError:
        return True  # Если уровень не распознан — показываем статью