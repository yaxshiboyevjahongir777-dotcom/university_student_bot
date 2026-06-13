import aiosqlite

DB_FILE = "university.db"
# 🎯 MANA SHU QATOR JETISHMAYOTGAN EDI:
db_conn = None

async def init_db():
    global db_conn
    db_conn = await aiosqlite.connect(DB_FILE)
    db_conn.row_factory = aiosqlite.Row
    
    # Jadvallarni yaratish
    await db_conn.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            telegram_id INTEGER PRIMARY KEY,
            full_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    await db_conn.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            course INTEGER DEFAULT 1,
            phone_number TEXT DEFAULT 'Mavjud emas',
            extra_info TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    
    # ⚡️ TEZLIKNI UPGRADE QILUVCHI INDEKS ⚡️
    await db_conn.execute('''
        CREATE INDEX IF NOT EXISTS idx_students_full_name 
        ON students (full_name);
    ''')
    
    YOUR_TELEGRAM_ID = 7018187696
    await db_conn.execute(
        "INSERT OR IGNORE INTO admins (telegram_id, full_name) VALUES (?, ?)",
        (YOUR_TELEGRAM_ID, "Jahongir Yaxshiboyev")
    )
    await db_conn.commit()