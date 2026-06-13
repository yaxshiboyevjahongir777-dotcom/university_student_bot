from aiogram.filters import Filter
from aiogram.types import Message
import config.database as db

class IsAdmin(Filter):
    async def __call__(self, message: Message) -> bool:
        if not db.db_conn:
            return False
        async with db.db_conn.execute("SELECT telegram_id FROM admins WHERE telegram_id = ?", (message.from_user.id,)) as cursor:
            admin = await cursor.fetchone()
            return admin is not None