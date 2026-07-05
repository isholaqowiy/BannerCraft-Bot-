import aiosqlite
from config import DB_NAME

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                joined_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                prompt TEXT,
                image_url TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        await db.commit()

async def register_user(user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
        await db.commit()

async def save_banner_log(user_id: int, prompt: str, url: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("INSERT INTO history (user_id, prompt, image_url) VALUES (?, ?, ?)", (user_id, prompt, url))
        await db.commit()

async def get_user_history(user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT prompt, image_url FROM history WHERE user_id = ? ORDER BY id DESC LIMIT 5", (user_id,)) as cursor:
            return [{"prompt": row[0], "url": row[1]} for row in await cursor.fetchall()]

