import os
import json
import asyncio
import logging
import threading
import math
import aiohttp
from datetime import datetime
import pytz
from typing import Dict, List, Set
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from telegram.constants import ParseMode
import openai

# Health check uchun Flask app

app = Flask(**name**)

@app.route(’/health’)
def health():
return ‘Bot ishlaydi’, 200

@app.route(’/’)
def home():
return ‘Masjidlar Bot’, 200

def run_flask():
app.run(host=‘0.0.0.0’, port=int(os.environ.get(‘PORT’, 8000)))

# Logging

logging.basicConfig(
format=’%(asctime)s - %(name)s - %(levelname)s - %(message)s’,
level=logging.INFO
)
logger = logging.getLogger(**name**)

# Bot sozlamalari

BOT_TOKEN = os.getenv(‘BOT_TOKEN’, ‘1436546945:AAFInxVnh3D-B1D4nI6y6I4vxMP5jK-12H4’)
OPENAI_API_KEY = os.getenv(‘OPENAI_API_KEY’)
CHANNEL_USERNAME = ‘quqonnamozvaqti’

# OpenAI sozlamalari

openai.api_key = OPENAI_API_KEY

# Foydalanuvchi sozlamalari saqlash

user_settings = {}

# Masjidlar royxati

MASJIDLAR = {
“NORBUTABEK”: “NORBUTABEK JOME MASJIDI”,
“GISHTLIK”: “GISHTLIK JOME MASJIDI”,
“SHAYXULISLOM”: “SHAYXULISLOM JOME MASJIDI”,
“HADYA_HOJI”: “HADYA HOJI SHALDIRAMOQ JOME MASJIDI”,
“AFGONBOG”: “AFGONBOG JOME MASJIDI”,
“SAYYID_AXMADHON”: “SAYYID AXMADHON HOJI JOME MASJIDI”,
“DEGRIZLIK”: “DEGRIZLIK JOME MASJIDI”,
“SHAYXON”: “SHAYXON JOME MASJIDI”,
“ZINBARDOR”: “ZINBARDOR JOME MASJIDI”,
“ZAYNUL_OBIDIN”: “ZAYNUL OBIDIN AYRILISH JOME MASJIDI”,
“HAZRATI_ABBOS”: “HAZRATI ABBOS MOLBOZORI JOME MASJIDI”,
“SAODAT”: “SAODAT JOME MASJIDI”,
“TOLABOY”: “MUHAMMAD SAID XUJA TOLABOY JOME MASJIDI”
}

# Namaz vaqtlari

masjidlar_data = {
“NORBUTABEK”: {“Bomdod”: “04:45”, “Peshin”: “12:50”, “Asr”: “17:45”, “Shom”: “19:35”, “Hufton”: “21:15”},
“GISHTLIK”: {“Bomdod”: “04:45”, “Peshin”: “12:50”, “Asr”: “17:15”, “Shom”: “19:30”, “Hufton”: “21:00”},
“SHAYXULISLOM”: {“Bomdod”: “04:45”, “Peshin”: “12:45”, “Asr”: “17:35”, “Shom”: “19:35”, “Hufton”: “21:15”},
“HADYA_HOJI”: {“Bomdod”: “04:55”, “Peshin”: “12:50”, “Asr”: “17:30”, “Shom”: “19:15”, “Hufton”: “20:55”},
“AFGONBOG”: {“Bomdod”: “04:50”, “Peshin”: “12:50”, “Asr”: “17:30”, “Shom”: “19:20”, “Hufton”: “20:55”},
“SAYYID_AXMADHON”: {“Bomdod”: “04:50”, “Peshin”: “12:50”, “Asr”: “17:20”, “Shom”: “19:20”, “Hufton”: “21:15”},
“DEGRIZLIK”: {“Bomdod”: “04:30”, “Peshin”: “12:45”, “Asr”: “17:35”, “Shom”: “19:35”, “Hufton”: “21:15”},
“SHAYXON”: {“Bomdod”: “04:40”, “Peshin”: “12:45”, “Asr”: “17:30”, “Shom”: “19:30”, “Hufton”: “21:00”},
“ZINBARDOR”: {“Bomdod”: “04:30”, “Peshin”: “12:45”, “Asr”: “17:35”, “Shom”: “19:35”, “Hufton”: “21:15”},
“ZAYNUL_OBIDIN”: {“Bomdod”: “04:40”, “Peshin”: “12:45”, “Asr”: “17:35”, “Shom”: “19:35”, “Hufton”: “21:15”},
“HAZRATI_ABBOS”: {“Bomdod”: “04:40”, “Peshin”: “12:45”, “Asr”: “17:35”, “Shom”: “19:35”, “Hufton”: “21:15”},
“SAODAT”: {“Bomdod”: “04:55”, “Peshin”: “12:50”, “Asr”: “17:20”, “Shom”: “19:10”, “Hufton”: “21:00”},
“TOLABOY”: {“Bomdod”: “04:40”, “Peshin”: “12:45”, “Asr”: “17:35”, “Shom”: “19:35”, “Hufton”: “21:15”}
}

# Masjidlar koordinatalari (Google Maps dan olingan)

MASJID_COORDINATES = {
“NORBUTABEK”: (40.3847, 71.7434),
“GISHTLIK”: (40.3890, 71.7401),
“SHAYXULISLOM”: (40.3821, 71.7456),
“HADYA_HOJI”: (40.3765, 71.7289),
“AFGONBOG”: (40.3912, 71.7523),
“SAYYID_AXMADHON”: (40.3923, 71.7612),
“DEGRIZLIK”: (40.3734, 71.7367),
“SHAYXON”: (40.3801, 71.7378),
“ZINBARDOR”: (40.3692, 71.7234),
“ZAYNUL_OBIDIN”: (40.3856, 71.7445),
“HAZRATI_ABBOS”: (40.3834, 71.7423),
“SAODAT”: (40.3798, 71.7398),
“TOLABOY”: (40.3867, 71.7489)
}

def calculate_distance(lat1, lon1, lat2, lon2):
“”“Ikki nuqta orasidagi masofani hisoblash (km) - havo yo’li”””
R = 6371  # Yer radiusi km da

```
lat1_rad = math.radians(lat1)
lat2_rad = math.radians(lat2)
delta_lat = math.radians(lat2 - lat1)
delta_lon = math.radians(lon2 - lon1)

a = (math.sin(delta_lat / 2) * math.sin(delta_lat / 2) +
     math.cos(lat1_rad) * math.cos(lat2_rad) *
     math.sin(delta_lon / 2) * math.sin(delta_lon / 2))
c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

return R * c
```

async def get_driving_distance(start_lat, start_lon, end_lat, end_lon):
“”“OSRM API orqali yo’l bo’yicha masofani olish”””
try:
url = f”http://router.project-osrm.org/route/v1/driving/{start_lon},{start_lat};{end_lon},{end_lat}”
params = {
‘overview’: ‘false’,
‘alternatives’: ‘false’,
‘steps’: ‘false’
}

```
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, timeout=10) as response:
            if response.status == 200:
                data = await response.json()
                if data.get('routes'):
                    distance_meters = data['routes'][0]['distance']
                    duration_seconds = data['routes'][0]['duration']
                    return {
                        'distance_km': round(distance_meters / 1000, 1),
                        'duration_minutes': round(duration_seconds / 60),
                        'success': True
                    }
    
    return {'success': False}
    
except Exception as e:
    logger.error(f"OSRM API xatolik: {e}")
    return {'success': False}
```

async def get_ai_response(question: str) -> str:
“”“OpenAI dan javob olish”””
try:
# Masjidlar ro’yxati
masjid_list = “\n”.join([f”• {name}” for name in MASJIDLAR.values()])

```
    # Namoz vaqtlari ma'lumoti
    times_info = ""
    for key, times in masjidlar_data.items():
        name = MASJIDLAR[key]
        times_info += f"\n{name}:\n"
        times_info += f"Bomdod: {times['Bomdod']}, Peshin: {times['Peshin']}, Asr: {times['Asr']}, Shom: {times['Shom']}, Hufton: {times['Hufton']}\n"
    
    system_prompt = f"""Siz Qo'qon shahridagi masjidlar va namoz vaqtlari haqida ma'lumot beradigan yordamchi botsiz.
```

QO’QON SHAHRIDAGI MASJIDLAR:
{masjid_list}

HOZIRGI NAMOZ VAQTLARI:
{times_info}

QOIDALAR:

1. Faqat Qo’qon shahri masjidlari va namoz mavzularida javob bering
1. Agar savol boshqa mavzuda bo’lsa, “Men faqat Qo’qon masjidlari va namoz haqida ma’lumot beraman” deb javob bering
1. Javoblarni o’zbek tilida bering
1. Qisqa va aniq javob bering
1. Namoz vaqtlari haqida so’ralsa, yuqoridagi ma’lumotlardan foydalaning
1. Islomiy adab va hurmatni saqlang

Savol: {question}”””

```
    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ],
        max_tokens=500,
        temperature=0.7
    )
    
    return response.choices[0].message.content.strip()
    
except Exception as e:
    logger.error(f"OpenAI API xatolik: {e}")
    return "❌ Hozirda AI yordamchi ishlamayapti. Keyinroq qaytadan urinib ko'ring."
```

def get_user_selected_masjids(user_id: str) -> Set[str]:
“”“Foydalanuvchi tanlagan masjidlar”””
return set(user_settings.get(str(user_id), {}).get(‘selected_masjids’, []))

def save_user_masjids(user_id: str, selected_masjids: Set[str]):
“”“Foydalanuvchi tanlagan masjidlarni saqlash”””
user_id_str = str(user_id)
if user_id_str not in user_settings:
user_settings[user_id_str] = {}
user_settings[user_id_str][‘selected_masjids’] = list(selected_masjids)

def get_main_keyboard():
“”“Asosiy klaviatura”””
keyboard = [
[‘🕐 Barcha vaqtlar’, ‘⏰ Eng yaqin/uzoq vaqt’],
[‘🕌 Masjidlar’, ‘📍 Eng yaqin masjid’],
[‘⚙️ Sozlamalar’, ‘ℹ️ Yordam’]
]
return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_location_keyboard():
“”“Location so’rash klaviaturasi”””
keyboard = [
[KeyboardButton(“📍 Joylashuvni yuborish”, request_location=True)],
[KeyboardButton(“🔙 Orqaga”)]
]
return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

def get_masjid_selection_keyboard(user_id: str) -> InlineKeyboardMarkup:
“”“Masjidlarni tanlash klaviaturasi”””
selected = get_user_selected_masjids(user_id)
keyboard = []

```
# Masjidlar royxati (2 tadan qatorda)
masjid_items = list(MASJIDLAR.items())
for i in range(0, len(masjid_items), 2):
    row = []
    for j in range(2):
        if i + j < len(masjid_items):
            key, name = masjid_items[i + j]
            # Tanlangan bolsa tick, tanlanmagan bolsa box
            icon = "✅" if key in selected else "⬜"
            # Masjid nomini qisqartirish
            short_name = name.replace("JOME MASJIDI", "").replace("MASJIDI", "").strip()
            if len(short_name) > 15:
                short_name = short_name[:15] + "..."
            row.append(InlineKeyboardButton(
                f"{icon} {short_name}", 
                callback_data=f"toggle_{key}"
            ))
    keyboard.append(row)

# Boshqaruv tugmalari
control_buttons = [
    [
        InlineKeyboardButton("✅ Barchasini tanlash", callback_data="select_all"),
        InlineKeyboardButton("❌ Barchasini bekor qilish", callback_data="deselect_all")
    ],
    [
        InlineKeyboardButton("💾 Saqlash", callback_data="save_settings"),
        InlineKeyboardButton("🔙 Orqaga", callback_data="back_main")
    ]
]
keyboard.extend(control_buttons)

return InlineKeyboardMarkup(keyboard)
```

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
“”“Start buyrugi”””
user_id = update.effective_user.id

```
# Agar yangi foydalanuvchi bolsa, barcha masjidlarni tanlangan qilib qoyish
if str(user_id) not in user_settings:
    save_user_masjids(user_id, set(MASJIDLAR.keys()))

welcome_message = """🕌 Assalomu alaykum!
```

*Qo’qon Masjidlari Namaz Vaqti Botiga xush kelibsiz!*

🔔 *Bildirishnomalar sozlamalari:*
Siz faqat o’zingiz tanlagan masjidlar uchun push notification olasiz.

⚙️ *Sozlamalar* orqali kerakli masjidlarni belgilashingiz mumkin.

📍 Barcha vaqtlar Qo’qon mahalliy vaqti bo’yicha.”””

```
await update.message.reply_text(
    welcome_message,
    parse_mode=ParseMode.MARKDOWN,
    reply_markup=get_main_keyboard()
)
```

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
“”“Xabarlarni qayta ishlash”””
text = update.message.text
user_id = update.effective_user.id

```
if text == '⚙️ Sozlamalar':
    await handle_settings(update, context)
elif text == '🕌 Masjidlar':
    await handle_all_masjids(update, context)
elif text == '🕐 Barcha vaqtlar':
    await handle_selected_masjids_times(update, context)
elif text == 'ℹ️ Yordam':
    await handle_help(update, context)
elif text == '⏰ Eng yaqin/uzoq vaqt':
    await handle_next_far_prayer(update, context)
elif text == '📍 Eng yaqin masjid':
    await handle_nearest_mosque_request(update, context)
elif text == '🔙 Orqaga':
    await update.message.reply_text(
        "🔙 Asosiy menyuga qaytdingiz",
        reply_markup=get_main_keyboard()
    )
elif update.message.location:
    await handle_location(update, context)
else:
    # AI bilan savol-javob
    if len(text) > 5 and '?' in text or any(word in text.lower() for word in ['qanday', 'nima', 'qachon', 'qayer', 'nech', 'kim']):
        # Typing action ko'rsatish
        await update.message.reply_chat_action('typing')
        
        # AI dan javob olish
        ai_response = await get_ai_response(text)
        await update.message.reply_text(
            f"🤖 *AI Yordamchi:*\n\n{ai_response}",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_main_keyboard()
        )
    else:
        await update.message.reply_text(
            "Quyidagi knopkalardan foydalaning yoki savolingizni yozing:",
            reply_markup=get_main_keyboard()
        )
```

async def handle_nearest_mosque_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
“”“Eng yaqin masjid so’rovi”””
await update.message.reply_text(
“📍 Eng yaqin masjidni topish uchun joylashuvingizni yuboring:”,
reply_markup=get_location_keyboard()
)

async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
“”“Location qabul qilish va eng yaqin masjidni topish”””
user_location = update.message.location
user_lat = user_location.latitude
user_lon = user_location.longitude

```
await update.message.reply_text("🔍 Eng yaqin masjidni qidirayapman...")

# Havo yo'li bo'yicha barcha masjidlarni tartiblash
air_distances = []
for masjid_key, coordinates in MASJID_COORDINATES.items():
    masjid_lat, masjid_lon = coordinates
    air_distance = calculate_distance(user_lat, user_lon, masjid_lat, masjid_lon)
    air_distances.append({
        'key': masjid_key,
        'air_distance': air_distance
    })

# Eng yaqin 3 ta masjidni olish (yo'l bo'yicha tekshirish uchun)
air_distances.sort(key=lambda x: x['air_distance'])
top_3_masjids = air_distances[:3]

await update.message.reply_text("🛣️ Yo'l bo'yicha masofalarni hisoblayman...")

# Yo'l bo'yicha masofalarni hisoblash
road_distances = []
for masjid_info in top_3_masjids:
    masjid_key = masjid_info['key']
    masjid_lat, masjid_lon = MASJID_COORDINATES[masjid_key]
    
    # OSRM API dan yo'l masofasini olish
    driving_result = await get_driving_distance(user_lat, user_lon, masjid_lat, masjid_lon)
    
    if driving_result['success']:
        road_distances.append({
            'key': masjid_key,
            'road_distance': driving_result['distance_km'],
            'duration': driving_result['duration_minutes'],
            'air_distance': masjid_info['air_distance']
        })
    else:
        # Agar OSRM ishlamasa, havo yo'li masofasini ishlatish
        road_distances.append({
            'key': masjid_key,
            'road_distance': masjid_info['air_distance'],
            'duration': None,
            'air_distance': masjid_info['air_distance']
        })

if road_distances:
    # Yo'l bo'yicha eng yaqinni topish
    road_distances.sort(key=lambda x: x['road_distance'])
    closest_mosque_info = road_distances[0]
    closest_mosque = closest_mosque_info['key']
    
    # Eng yaqin masjid ma'lumotlari
    masjid_name = MASJIDLAR[closest_mosque]
    times = masjidlar_data[closest_mosque]
    
    # Hozirgi vaqt
    qoqon_tz = pytz.timezone('Asia/Tashkent')
    now = datetime.now(qoqon_tz)
    current_time = now.strftime("%H:%M")
    
    # Eng yaqin namoz vaqtini topish
    prayer_names = ["Bomdod", "Peshin", "Asr", "Shom", "Hufton"]
    next_prayer = None
    
    for prayer in prayer_names:
        prayer_time = times[prayer]
        if prayer_time > current_time:
            next_prayer = {'name': prayer, 'time': prayer_time}
            break
    
    # Masjid koordinatalari
    masjid_lat, masjid_lon = MASJID_COORDINATES[closest_mosque]
    
    # Distance formatini o'zgartirish
    road_distance = closest_mosque_info['road_distance']
    air_distance = closest_mosque_info['air_distance']
    duration = closest_mosque_info['duration']
    
    if road_distance < 1:
        distance_text = f"{int(road_distance * 1000)} metr"
    else:
        distance_text = f"{road_distance} km"
    
    message = f"""📍 *ENG YAQIN MASJID*
```

🕌 {masjid_name}
🛣️ Yo’l bo’yicha: {distance_text}”””

```
    if duration:
        message += f"\n🚗 Haydash vaqti: ~{duration} daqiqa"
    
    if abs(road_distance - air_distance) > 1:
        message += f"\n✈️ Havo yo'li: {air_distance:.1f} km"
    
    if next_prayer:
        message += f"""
```

🕐 *ENG YAQIN NAMOZ:*
🌆 {next_prayer[‘name’]}: *{next_prayer[‘time’]}*”””

```
    message += f"""
```

⏰ Hozirgi vaqt: {current_time} (Qo’qon vaqti)

📋 *Barcha vaqtlar:*
🌅 Bomdod: *{times[‘Bomdod’]}*  ☀️ Peshin: *{times[‘Peshin’]}*
🌆 Asr: *{times[‘Asr’]}*     🌇 Shom: *{times[‘Shom’]}*  
🌙 Hufton: *{times[‘Hufton’]}*

🗺️ *Masjid joylashuvi:*
[Yandex xaritada ko’rish](https://yandex.com/maps/?pt={masjid_lon},{masjid_lat}&z=18)
[Google xaritada ko’rish](https://maps.google.com/?q={masjid_lat},{masjid_lon})”””

```
    await update.message.reply_text(
        message,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=get_main_keyboard(),
        disable_web_page_preview=True
    )
else:
    await update.message.reply_text(
        "❌ Eng yaqin masjidni aniqlab bo'lmadi. Qaytadan urinib ko'ring.",
        reply_markup=get_main_keyboard()
    )
```

async def handle_next_far_prayer(update: Update, context: ContextTypes.DEFAULT_TYPE):
“”“Eng yaqin va eng uzoq namoz vaqtlari”””
user_id = str(update.effective_user.id)
selected = get_user_selected_masjids(user_id)

```
if not selected:
    await update.message.reply_text(
        "❌ Hech qanday masjid tanlanmagan!\n⚙️ Sozlamalar orqali masjidlarni tanlang.",
        reply_markup=get_main_keyboard()
    )
    return

# Qo'qon vaqt zonasi
qoqon_tz = pytz.timezone('Asia/Tashkent')
now = datetime.now(qoqon_tz)
current_time = now.strftime("%H:%M")
current_date = now.strftime("%d.%m.%Y")

# Namoz nomlari
prayer_names = ["Bomdod", "Peshin", "Asr", "Shom", "Hufton"]

# Hozirgi vaqtga qarab eng yaqin va eng uzoq namozni topish
next_prayers = []
far_prayers = []

for masjid_key in selected:
    if masjid_key in masjidlar_data:
        times = masjidlar_data[masjid_key]
        name = MASJIDLAR[masjid_key]
        
        for prayer in prayer_names:
            prayer_time = times[prayer]
            if prayer_time > current_time:
                next_prayers.append({
                    'masjid': name,
                    'masjid_key': masjid_key,
                    'prayer': prayer,
                    'time': prayer_time
                })
                break
        
        # Eng uzoq namoz (oxirgi namoz)
        last_prayer = prayer_names[-1]  # Hufton
        far_prayers.append({
            'masjid': name,
            'masjid_key': masjid_key,
            'prayer': last_prayer,
            'time': times[last_prayer]
        })

# 1-chi xabar: Hozirgi vaqtga qarab
if next_prayers:
    next_prayers.sort(key=lambda x: x['time'])
    next_prayer = next_prayers[0]
    
    far_prayers.sort(key=lambda x: x['time'], reverse=True)
    far_prayer = far_prayers[0]
    
    message1 = f"""📍 *ENG YAQIN NAMOZ VAQTI*
```

🕌 {next_prayer[‘masjid’]}
🕐 {next_prayer[‘prayer’]}: *{next_prayer[‘time’]}*

📍 *ENG UZOQ NAMOZ VAQTI*  
🕌 {far_prayer[‘masjid’]}
🕐 {far_prayer[‘prayer’]}: *{far_prayer[‘time’]}*

⏰ Hozirgi vaqt: {current_time} (Qo’qon vaqti)”””
else:
message1 = f””“📍 Bugun uchun barcha namoz vaqtlari o’tdi.
Ertaga Bomdod vaqti bilan davom etadi.

⏰ Hozirgi vaqt: {current_time} (Qo’qon vaqti)”””

```
await update.message.reply_text(
    message1,
    parse_mode=ParseMode.MARKDOWN,
    reply_markup=get_main_keyboard()
)

# 2-chi xabar: Barcha namozlar bo'yicha eng erta va eng kech
earliest_times = {}
latest_times = {}

for prayer in prayer_names:
    prayer_times = []
    for masjid_key in selected:
        if masjid_key in masjidlar_data:
            prayer_times.append({
                'time': masjidlar_data[masjid_key][prayer],
                'masjid': MASJIDLAR[masjid_key].replace("JOME MASJIDI", "").strip()
            })
    
    if prayer_times:
        prayer_times.sort(key=lambda x: x['time'])
        earliest_times[prayer] = prayer_times[0]
        latest_times[prayer] = prayer_times[-1]

# Emojiler
prayer_emojis = {
    "Bomdod": "🌅",
    "Peshin": "☀️", 
    "Asr": "🌆",
    "Shom": "🌇",
    "Hufton": "🌙"
}

message2 = "⏰ *ENG ERTA BOSHLANADIGAN VAQTLAR:*\n\n"
for prayer in prayer_names:
    if prayer in earliest_times:
        emoji = prayer_emojis[prayer]
        time_info = earliest_times[prayer]
        message2 += f"{emoji} {prayer}: {time_info['time']} - {time_info['masjid']}\n"

message2 += "\n⏰ *ENG KECH BOSHLANADIGAN VAQTLAR:*\n\n"
for prayer in prayer_names:
    if prayer in latest_times:
        emoji = prayer_emojis[prayer]
        time_info = latest_times[prayer]
        message2 += f"{emoji} {prayer}: {time_info['time']} - {time_info['masjid']}\n"

await update.message.reply_text(
    message2,
    parse_mode=ParseMode.MARKDOWN,
    reply_markup=get_main_keyboard()
)
```

async def handle_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
“”“Yordam bolimi”””
help_text = “”“ℹ️ *YORDAM*

*Bot funksiyalari:*
🕐 Barcha vaqtlar - Tanlangan masjidlar namoz vaqtlari
⏰ Eng yaqin/uzoq vaqt - Keyingi va eng uzoq namoz vaqtlari
📍 Eng yaqin masjid - Location asosida eng yaqin masjid
🕌 Masjidlar - Barcha masjidlar ro’yxati
⚙️ Sozlamalar - Masjidlarni tanlash

❓ *TEZ-TEZ SO’RALADIGAN SAVOLLAR:*

*Namoz haqida:*
• Namoz vaqtlari qanday belgilanadi?
• Jamoat namozining fazilati nima?
• Safar paytida namoz qanday o’qiladi?
• Qaza namozlarni qachon o’qish mumkin?

*Masjidlar haqida:*
• Qo’qonda nechta jome masjidi bor?
• Masjidga borish tartib-qoidalari
• Juma namozi soat nechada?
• Eng katta masjid qaysi?

*Bot haqida:*
• Push notification qanday yoqiladi?
• Masjidlarni qanday tanlash mumkin?
• Eng yaqin masjidni qanday topish mumkin?

🤖 *SAVOLLARINGIZ BORMI?*
Qo’qon shahri masjidlari va namoz haqida
savollaringizni yuboring - AI javob beradi! 💬

*Qanday ishlaydi:*

1. Boshlang’ich holatda barcha masjidlar tanlangan
1. Sozlamalar orqali kerakli masjidlarni belgilang
1. Faqat tanlangan masjidlar vaqti yangilanganda push olasiz

*Vaqt zonasi:* Qo’qon mahalliy vaqti (UTC+5)

*Murojaat:*
@{CHANNEL_USERNAME} kanalimizga obuna bo’ling”””

```
await update.message.reply_text(
    help_text,
    parse_mode=ParseMode.MARKDOWN,
    reply_markup=get_main_keyboard()
)
```

async def handle_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
“”“Sozlamalar”””
user_id = update.effective_user.id
selected = get_user_selected_masjids(str(user_id))

```
message = f"""⚙️ *BILDIRISHNOMALAR SOZLAMALARI*
```

Siz hozirda *{len(selected)} ta masjid* uchun bildirishnoma olasiz.

Quyida masjidlarni tanlang/bekor qiling:
✅ - Tanlangan (push olasiz)  
⬜ - Tanlanmagan (push olmaydigan)

*Eslatma:* Faqat tanlangan masjidlar vaqti yangilanganda push notification olasiz.”””

```
await update.message.reply_text(
    message,
    parse_mode=ParseMode.MARKDOWN,
    reply_markup=get_masjid_selection_keyboard(str(user_id))
)
```

async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
“”“Inline button bosilganda”””
query = update.callback_query
await query.answer()

```
user_id = str(query.from_user.id)
data = query.data

if data.startswith("toggle_"):
    # Masjidni tanlash/bekor qilish
    masjid_key = data.replace("toggle_", "")
    selected = get_user_selected_masjids(user_id)
    
    if masjid_key in selected:
        selected.remove(masjid_key)
    else:
        selected.add(masjid_key)
    
    save_user_masjids(user_id, selected)
    
    # Klaviaturani yangilash
    await query.edit_message_reply_markup(
        reply_markup=get_masjid_selection_keyboard(user_id)
    )
    
elif data == "select_all":
    # Barchasini tanlash
    save_user_masjids(user_id, set(MASJIDLAR.keys()))
    await query.edit_message_reply_markup(
        reply_markup=get_masjid_selection_keyboard(user_id)
    )
    
elif data == "deselect_all":
    # Barchasini bekor qilish
    save_user_masjids(user_id, set())
    await query.edit_message_reply_markup(
        reply_markup=get_masjid_selection_keyboard(user_id)
    )
    
elif data == "save_settings":
    # Sozlamalarni saqlash
    selected = get_user_selected_masjids(user_id)
    await query.edit_message_text(
        f"✅ *Sozlamalar saqlandi!*\n\n"
        f"Siz {len(selected)} ta masjid uchun bildirishnoma olasiz:\n"
        f"{', '.join([MASJIDLAR[key].replace('JOME MASJIDI', '').strip() for key in selected])}",
        parse_mode=ParseMode.MARKDOWN
    )
    
elif data == "back_main":
    # Orqaga
    await query.edit_message_text("🔙 Asosiy menyuga qaytdingiz.")
```

async def handle_selected_masjids_times(update: Update, context: ContextTypes.DEFAULT_TYPE):
“”“Tanlangan masjidlar vaqtlari”””
user_id = str(update.effective_user.id)
selected = get_user_selected_masjids(user_id)

```
if not selected:
    await update.message.reply_text(
        "❌ Hech qanday masjid tanlanmagan!\n⚙️ Sozlamalar orqali masjidlarni tanlang.",
        reply_markup=get_main_keyboard()
    )
    return

message = "🕐 *TANLANGAN MASJIDLAR VAQTLARI:*\n\n"

for masjid_key in selected:
    if masjid_key in masjidlar_data:
        times = masjidlar_data[masjid_key]
        name = MASJIDLAR[masjid_key]
        
        message += f"🕌 *{name}*\n"
        message += f"🌅 Bomdod: *{times['Bomdod']}*\n"
        message += f"☀️ Peshin: *{times['Peshin']}*\n"
        message += f"🌆 Asr: *{times['Asr']}*\n"
        message += f"🌇 Shom: *{times['Shom']}*\n"
        message += f"🌙 Hufton: *{times['Hufton']}*\n\n"

await update.message.reply_text(
    message,
    parse_mode=ParseMode.MARKDOWN,
    reply_markup=get_main_keyboard()
)
```

async def handle_all_masjids(update: Update, context: ContextTypes.DEFAULT_TYPE):
“”“Barcha masjidlar (korish uchun)”””
message = “🕌 *BARCHA MASJIDLAR ROYXATI:*\n\n”

```
for i, (key, name) in enumerate(MASJIDLAR.items(), 1):
    message += f"{i}. {name}\n"

message += f"\n📊 Jami: {len(MASJIDLAR)} ta masjid"
message += "\n\n⚙️ *Sozlamalar* orqali kerakli masjidlarni tanlashingiz mumkin."

await update.message.reply_text(
    message,
    parse_mode=ParseMode.MARKDOWN,
    reply_markup=get_main_keyboard()
)
```

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
“”“Xatolik handleri”””
logger.error(msg=“Xatolik yuz berdi:”, exc_info=context.error)

def main():
“”“Asosiy funksiya”””
try:
# Flask’ni background’da ishga tushirish
threading.Thread(target=run_flask, daemon=True).start()

```
    # Application yaratish
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Handlerlarni qoshish
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.LOCATION, handle_location))
    application.add_handler(CallbackQueryHandler(handle_callback_query))
    
    # Xatolik handlerini qoshish
    application.add_error_handler(error_handler)
    
    logger.info("Bot ishga tushmoqda...")
    print("Bot ishga tushdi! ✅")
    
    # Background Worker uchun polling ishlatish
    application.run_polling(
        drop_pending_updates=True,
        allowed_updates=Update.ALL_TYPES
    )
    
except Exception as e:
    logger.error(f"Botni ishga tushirishda xatolik: {e}")
    print(f"❌ Xatolik: {e}")
```

if **name** == ‘**main**’:
main()