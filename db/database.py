import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path("data/app.db")
DB_PATH.parent.mkdir(exist_ok=True)


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
                CREATE TABLE IF NOT EXISTS users
                (
                    id
                    INTEGER
                    PRIMARY
                    KEY
                    AUTOINCREMENT,
                    created_at
                    TIMESTAMP
                    DEFAULT
                    CURRENT_TIMESTAMP
                )
                """)

    cur.execute("""
                CREATE TABLE IF NOT EXISTS progress
                (
                    id
                    INTEGER
                    PRIMARY
                    KEY
                    AUTOINCREMENT,
                    user_id
                    INTEGER
                    NOT
                    NULL
                    DEFAULT
                    1,
                    skill
                    TEXT
                    NOT
                    NULL,
                    cefr_level
                    TEXT
                    NOT
                    NULL,
                    score
                    REAL
                    NOT
                    NULL,
                    timestamp
                    TIMESTAMP
                    DEFAULT
                    CURRENT_TIMESTAMP,
                    FOREIGN
                    KEY
                (
                    user_id
                ) REFERENCES users
                (
                    id
                )
                    )
                """)

    # Создаём дефолтного пользователя (если нет)
    cur.execute("INSERT OR IGNORE INTO users (id) VALUES (1)")

    conn.commit()
    conn.close()


def save_progress(skill: str, cefr_level: str, score: float):
    """Сохраняет результат тренировки в БД"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO progress (skill, cefr_level, score) VALUES (?, ?, ?)",
        (skill, cefr_level, score)
    )
    conn.commit()
    conn.close()


def get_recent_progress(limit: int = 10):
    """Получает последние записи из БД"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
                SELECT strftime('%Y-%m-%d %H:%M', timestamp) as date,
            skill,
            cefr_level,
            ROUND(score, 1)
        FROM progress
        ORDER BY timestamp DESC
        LIMIT ?
    """, (limit,))
    rows = cur.fetchall()
    conn.close()
    return rows


def init_articles_table():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Создаём таблицу с колонкой уровня
    cur.execute("""
                CREATE TABLE IF NOT EXISTS articles
                (
                    id
                    INTEGER
                    PRIMARY
                    KEY
                    AUTOINCREMENT,
                    source
                    TEXT
                    NOT
                    NULL,
                    title
                    TEXT
                    NOT
                    NULL,
                    content
                    TEXT
                    NOT
                    NULL,
                    url
                    TEXT
                    NOT
                    NULL
                    UNIQUE,
                    cefr_level
                    TEXT
                    DEFAULT
                    'A2', -- ← новая колонка
                    fetched_at
                    TIMESTAMP
                    DEFAULT
                    CURRENT_TIMESTAMP
                )
                """)

    # Добавляем колонку, если таблица уже существовала без неё
    try:
        cur.execute("ALTER TABLE articles ADD COLUMN cefr_level TEXT DEFAULT 'A2'")
    except sqlite3.OperationalError:
        pass  # Колонка уже существует

    conn.commit()
    conn.close()


# Обнови init_db() — добавь вызов новой функции:
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
                CREATE TABLE IF NOT EXISTS users
                (
                    id
                    INTEGER
                    PRIMARY
                    KEY
                    AUTOINCREMENT,
                    created_at
                    TIMESTAMP
                    DEFAULT
                    CURRENT_TIMESTAMP
                )
                """)

    cur.execute("""
                CREATE TABLE IF NOT EXISTS progress
                (
                    id
                    INTEGER
                    PRIMARY
                    KEY
                    AUTOINCREMENT,
                    user_id
                    INTEGER
                    NOT
                    NULL
                    DEFAULT
                    1,
                    skill
                    TEXT
                    NOT
                    NULL,
                    cefr_level
                    TEXT
                    NOT
                    NULL,
                    score
                    REAL
                    NOT
                    NULL,
                    timestamp
                    TIMESTAMP
                    DEFAULT
                    CURRENT_TIMESTAMP,
                    FOREIGN
                    KEY
                (
                    user_id
                ) REFERENCES users
                (
                    id
                )
                    )
                """)

    cur.execute("INSERT OR IGNORE INTO users (id) VALUES (1)")

    conn.commit()
    conn.close()

    init_articles_table()  # ←

def save_reading_progress(article_id: int, cefr_level: str, comprehension_score: float):
    """Сохраняет результат чтения в БД"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

     # Сохраняем как 'reading' skill
    cur.execute(
        "INSERT INTO progress (skill, cefr_level, score) VALUES (?, ?, ?)",
        ('reading', cefr_level, comprehension_score)
    )

    conn.commit()
    conn.close()
    return cur.lastrowid


def init_user_profile_table():
    """Создаёт таблицу профиля пользователя"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
                CREATE TABLE IF NOT EXISTS user_profile
                (
                    id
                    INTEGER
                    PRIMARY
                    KEY
                    CHECK
                (
                    id =
                    1
                ), -- только одна запись
                    cefr_level TEXT DEFAULT 'A1',
                    target_level TEXT DEFAULT 'B2',
                    last_tested TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    words_learned INTEGER DEFAULT 0
                    )
                """)

    # Создаём дефолтную запись, если нет
    cur.execute("INSERT OR IGNORE INTO user_profile (id, cefr_level) VALUES (1, 'A1')")

    conn.commit()
    conn.close()


def get_user_level() -> str:
    """Получает текущий уровень пользователя"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT cefr_level FROM user_profile WHERE id = 1")
    row = cur.fetchone()
    conn.close()
    return row[0] if row else "A1"


def set_user_level(level: str):
    """Сохраняет уровень пользователя"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "UPDATE user_profile SET cefr_level = ?, last_tested = CURRENT_TIMESTAMP WHERE id = 1",
        (level,)
    )
    conn.commit()
    conn.close()


# Обнови init_db() — добавь вызов новой функции в конец:
def init_db():
    # ... существующий код ...
    init_articles_table()
    init_user_profile_table()  # ← добавь эту строку

if __name__ == "__main__":
    init_db()
    print("✅ База создана: data/app.db")