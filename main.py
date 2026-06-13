import asyncio
import os
import logging
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import config.database as db
from handlers import admin_router, user_router

# 1. Yangi middleware'ni import qilamiz
from middlewares.throttling import ThrottlingMiddleware

load_dotenv()

async def main():
    logging.basicConfig(level=logging.INFO)
    
    await db.init_db()
    
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher()
    
    # 2. SHU YERDA MIDDLEWARE'NI REJISTRATSIYA QILAMIZ
    # Har bir kelgan xabar handlerga borishdan oldin 1 soniya kutadi
    dp.message.middleware(ThrottlingMiddleware(slow_down_time=1.0))
    
    # Routerlarni ulash
    dp.include_routers(admin_router, user_router)
    
    print("🚀 Bot tizimi Throttling (1s kechikish) bilan muvaffaqiyatli yoqildi...")
    
    try:
        await dp.start_polling(bot)
    finally:
        if db.db_conn:
            await db.db_conn.close()
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())