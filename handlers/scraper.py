import aiohttp
from bs4 import BeautifulSoup

# Sizning universitetingiz HEMIS manzillari
HEMIS_LOGIN_URL = "https://student.navoiy-uni.uz/dashboard/login"
HEMIS_STUDENTS_URL = "https://student.navoiy-uni.uz/dashboard/student/index"

# ⚠️ BU YERGA O'ZINGIZNING HEMIS XODIM (YOKI ADMIN) LOGIN VA PAROLINGIZNI YOZING
LOGIN_DATA = {
    "LoginForm[username]": "Sizning_HEMIS_Loginingiz",
    "LoginForm[password]": "Sizning_HEMIS_Parolingiz"
}

async def parse_university_site(url: str = None):
    """
    HEMIS tizimiga login/parol orqali kirib, talabalarni parslash funksiyasi.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    # URL yuborilsa o'shani oladi, bo'lmasa standart talabalar ro'yxati sahifasiga kiradi
    target_url = url if url else HEMIS_STUDENTS_URL
    
    async with aiohttp.ClientSession() as session:
        try:
            # 1. HEMIS-ga login so'rovi yuborish va sessiyani (cookie) ushlab qolish
            async with session.post(HEMIS_LOGIN_URL, data=LOGIN_DATA, headers=headers, timeout=15) as login_resp:
                if login_resp.status != 200:
                    print("❌ HEMIS tizimiga kirish muvaffaqiyatsiz tugadi (Login/Parol xato bo'lishi mumkin).")
                    return []
            
            # 2. Avtorizatsiyadan o'tgan holatda talabalar sahifasini yuklab olish
            async with session.get(target_url, headers=headers, timeout=15) as response:
                if response.status != 200:
                    print(f"❌ Sahifani yuklab bo'lmadi. Status kod: {response.status}")
                    return []
                
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                students_data = []
                
                # HEMIS tizimida odatda ma'lumotlar jadval (table -> tr) ichida turadi.
                # Quyida jadval qatorlarini topamiz (odatda 'id' yoki klaslar orqali):
                rows = soup.find_all('tr') 
                
                for row in rows:
                    try:
                        cols = row.find_all('td')
                        if len(cols) < 4: # Agar ustunlar soni kam bo'lsa, bu talaba qatori emas
                            continue
                            
                        # HEMIS jadval strukturasiga qarab ustunlar tartibini moslaymiz:
                        # 0-ustun: # (tartib raqami), 1-ustun: Rasm va F.I.SH, 2-ustun: Guruh/Kurs va h.k.
                        
                        # Ism va familiyani olish (odatda 'td' ichidagi 'a' tegi yoki matn bo'ladi)
                        name_tag = cols[1].find('a')
                        name = name_tag.text.strip() if name_tag else cols[1].text.strip()
                        
                        # Agar ustunda talaba ismi bo'lmasa, tashlab ketamiz
                        if not name or len(name) < 5:
                            continue
                            
                        # Rasmni olish
                        img_tag = cols[1].find('img') or cols[0].find('img')
                        photo = img_tag['src'] if img_tag else None
                        
                        # Telefon raqami va guruh/kurs ma'lumotlarini qidirish
                        # HEMIS sahifangizdagi ustunlar o'rniga qarab cols[X] raqamlarini o'zgartirishingiz mumkin
                        phone = cols[3].text.strip() if len(cols) > 3 else "Mavjud emas"
                        course_text = cols[2].text.strip() if len(cols) > 2 else "1"
                        
                        # Kurs raqamini matndan ajratib olish (Macalan: "3-kurs" -> 3)
                        course = 1
                        for char in course_text:
                            if char.isdigit():
                                course = int(char)
                                break
                        
                        students_data.append({
                            "full_name": name, 
                            "photo_url": photo, 
                            "region": "Viloyat", # Agar jadvalda bo'lsa dynamic qilinadi
                            "district": "Tuman", 
                            "phone_number": phone, 
                            "email": None,
                            "course": course, 
                            "birth_date": "Ko'rsatilmagan"
                        })
                    except Exception as e:
                        continue
                        
                return students_data
                
        except Exception as e:
            print(f"⚠️ HEMIS Skraping tizimida xatolik: {e}")
            return []