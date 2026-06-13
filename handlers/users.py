from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
import config.database as db
import time

router = Router()

@router.message(Command("start"))
async def user_start(message: types.Message):
    await message.answer(
        "👋 Universitet talabalarini tezkor qidirish tizimiga xush kelibsiz.\n\n"
        "Talabaning **Ismi, Telefon raqami, Kursi** yoki **ID raqamini** yozib yuboring:"
    )

@router.message()
async def search_students(message: types.Message):
    search_word = message.text.strip()
    
    if len(search_word) < 2:  # Kurslarni (masalan "1") ham qidirish uchun limitni 2 ga tushirdik
        await message.answer("⚠️ Qidiruv uchun kamida 2 ta belgi kiriting.")
        return

    query = f"%{search_word}%" 
    
    start_time = time.perf_counter()
    
    # 🔥 ENg ZO'R QIDIRUV: Ism, telefon yoki qo'shimcha ma'lumotlar (ID, Fakultet) ichidan ham qidiradi
    async with db.db_conn.execute('''
        SELECT id, full_name, course FROM students 
        WHERE LOWER(full_name) LIKE LOWER(?) 
           OR LOWER(phone_number) LIKE LOWER(?)
           OR LOWER(extra_info) LIKE LOWER(?)
        GROUP BY full_name
        LIMIT 10
    ''', (query, query, query)) as cursor:
        rows = await cursor.fetchall()
        
    end_time = time.perf_counter()
    execution_time = (end_time - start_time) * 1000
    
    if not rows:
        await message.answer(
            "🔍 Kechirasiz, kiritilgan ma'lumot bo'yicha hech qanday talaba topilmadi.\n"
            "_Bazada ma'lumot borligini yoki fayl yuklanganini tekshiring._", 
            parse_mode="Markdown"
        )
        return

    builder = InlineKeyboardBuilder()
    for row in rows:
        builder.button(text=f"👨‍🎓 {row['full_name']} ({row['course']}-kurs)", callback_data=f"info_{row['id']}")
    builder.adjust(1)
    
    await message.answer(
        f"🔍 **Topilgan talabalar ro'yxati:**\n"
        f"⏱ _Baza ichki qidiruv tezligi: {execution_time:.2f} ms_\n\n"
        f"Batafsil ko'rish uchun ustiga bosing:", 
        reply_markup=builder.as_markup(),
        parse_mode="Markdown"
    )

@router.callback_query(F.data.startswith("info_"))
async def show_full_profile(callback: types.CallbackQuery):
    student_id = int(callback.data.split("_")[1])
    
    async with db.db_conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)) as cursor:
        s = await cursor.fetchone()
        
    if not s:
        await callback.answer("❌ Talaba ma'lumoti topilmadi.")
        return
        
    profile_msg = (
        f"📋 **TALABA HAQIDA TO'LIQ MA'LUMOT**\n\n"
        f"👤 **F.I.SH:** {s['full_name']}\n"
        f"📚 **📚 Kursi:** {s['course']}-kurs\n"
        f"📞 **Telefon raqami:** {s['phone_number']}\n"
        f"───────────────────\n"
        f"📝 **Fayldan olingan barcha ma'lumotlar:**\n_{s['extra_info']}_\n"
    )
    
    await callback.answer()
    await callback.message.answer(profile_msg, parse_mode="Markdown")