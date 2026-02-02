import feedparser
import html
from datetime import datetime
from db.database import DB_PATH
import sqlite3

SOURCES = {
    "bbc": "https://www.bbc.co.uk/learningenglish/english/features/6-minute-english/rss",
    "voa": "https://learningenglish.voanews.com/api/zq?iid=2195&did=2200&zid=3313&fmt=rss"
}


def fetch_articles(limit_per_source=3):
    """Забирает статьи из RSS и сохраняет в БД"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    total_saved = 0
    for source, url in SOURCES.items():
        try:
            feed = feedparser.parse(url)
            entries = feed.entries[:limit_per_source]

            for entry in entries:
                # Очистка HTML
                title = html.unescape(entry.title.strip())
                content = html.unescape(entry.summary.strip()) if hasattr(entry, 'summary') else ""
                link = entry.link

                # Проверка на дубликат
                cur.execute("SELECT id FROM articles WHERE url = ?", (link,))
                if cur.fetchone():
                    continue

                # Сохранение
                cur.execute(
                    "INSERT INTO articles (source, title, content, url) VALUES (?, ?, ?, ?)",
                    (source, title, content, link)
                )
                total_saved += 1

        except Exception as e:
            print(f"⚠️ Ошибка при загрузке {source}: {e}")

    conn.commit()
    conn.close()
    return total_saved


def get_articles(limit=10):
    """Получает статьи из БД"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
                SELECT id,
                       source,
                       title,
                       content,
                       url,
                       strftime('%Y-%m-%d', fetched_at) as date
                FROM articles
                ORDER BY fetched_at DESC
                    LIMIT ?
                """, (limit,))
    rows = cur.fetchall()
    conn.close()
    return rows


if __name__ == "__main__":
    saved = fetch_articles()
    print(f"✅ Сохранено новых статей: {saved}")
    articles = get_articles()
    print(f"\nПоследние статьи:")
    for art in articles[:3]:
        print(f"- [{art[1].upper()}] {art[2]}")