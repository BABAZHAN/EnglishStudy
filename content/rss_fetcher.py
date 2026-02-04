import feedparser
import html
from datetime import datetime
from db.database import DB_PATH
import sqlite3
from content.text_analyzer import estimate_text_level

SOURCES = {
    "bbc": "https://www.bbc.co.uk/learningenglish/english/features/6-minute-english/rss",
    "voa": "https://learningenglish.voanews.com/api/zq?iid=2195&did=2200&zid=3313&fmt=rss"
}


def fetch_articles(limit_per_source=3):
    """Забирает статьи из RSS и сохраняет в БД с оценкой уровня"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    total_saved = 0
    for source, url in SOURCES.items():
        try:
            feed = feedparser.parse(url)
            entries = feed.entries[:limit_per_source]

            for entry in entries:
                title = html.unescape(entry.title.strip())
                content = html.unescape(entry.summary.strip()) if hasattr(entry, 'summary') else ""
                link = entry.link

                # Проверка на дубликат
                cur.execute("SELECT id FROM articles WHERE url = ?", (link,))
                if cur.fetchone():
                    continue

                # Оценка уровня статьи
                level = estimate_text_level(content)

                # Сохранение с уровнем
                cur.execute(
                    "INSERT INTO articles (source, title, content, url, cefr_level) VALUES (?, ?, ?, ?, ?)",
                    (source, title, content, link, level)
                )
                total_saved += 1

        except Exception as e:
            print(f"⚠️ Ошибка при загрузке {source}: {e}")

    conn.commit()
    conn.close()
    return total_saved


def get_articles(user_level: str = "A2", limit=10):
    """Получает статьи из БД, фильтруя по уровню пользователя"""
    from db.database import DB_PATH
    import sqlite3

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Получаем ВСЕ статьи с их уровнями
    cur.execute("""
                SELECT id,
                       source,
                       title,
                       content,
                       url,
                       cefr_level,
                       strftime('%Y-%m-%d', fetched_at) as date
                FROM articles
                ORDER BY fetched_at DESC
                """)
    all_articles = cur.fetchall()
    conn.close()

    # Фильтрация на стороне Python
    filtered = []
    levels_order = ["A1", "A2", "B1", "B2", "B2+"]

    try:
        user_idx = levels_order.index(user_level)
    except ValueError:
        user_idx = 0  # Если уровень не распознан — считаем A1

    for art in all_articles:
        art_level = art[5]  # cefr_level

        try:
            art_idx = levels_order.index(art_level)
            # Разрешаем статьи: на 1 уровень проще, такой же, на 1 уровень сложнее
            if abs(art_idx - user_idx) <= 1:
                filtered.append(art)
        except ValueError:
            # Если уровень статьи не распознан — показываем
            filtered.append(art)

    return filtered[:limit]


if __name__ == "__main__":
    saved = fetch_articles()
    print(f"✅ Сохранено новых статей: {saved}")
    articles = get_articles()
    print(f"\nПоследние статьи:")
    for art in articles[:3]:
        print(f"- [{art[1].upper()}] {art[2]}")