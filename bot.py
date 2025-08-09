import os
import json
import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Set
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from telegram.constants import ParseMode

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot sozlamalari
BOT_TOKEN = os.getenv('BOT_TOKEN', '1436546945:AAFInxVnh3D-B1D4nI6y6I4vxMP5jK-12H4')
CHANNEL_USERNAME = 'quqonnamozvaqti'

# Foydalanuvchi sozlamalari saqlash
USER_SETTINGS_FILE = 'user_settings.json'
user_settings = {}

# Masjidlar ro'yxati
MASJIDLAR = {
    "NORBUTABEK": "NORBUTABEK JOME MASJIDI",
    "GISHTLIK": "G'ISHTLIK JOME MASJIDI", 
    "SHAYXULISLOM": "SHAYXULISLOM JOME MASJIDI",
    "HADYA_HOJI": "HADYA HOJI SHALDIRAMOQ JOME MASJIDI",
    "AFGONBOG": "AFG'ONBOG' JOME MASJIDI",
    "SAYYID_AXMADHON": "SAYYID AXMADHON HOJI JOME MASJIDI",
    "DEGRIZLIK": "DEGRIZLIK JOME MASJIDI",
    "SHAYXON": "SHAYXON JOME MASJIDI",
    "ZINBARDOR": "ZINBARDOR JOME MASJIDI",
    "ZAYNUL_OBIDIN": "ZAYNUL OBIDIN AYRILISH JOME MASJIDI",
    "HAZRATI_ABBOS": "HAZRATI ABBOS MOLBOZORI JOME MASJIDI",
    "SAODAT": "SAODAT JOME MASJIDI",
    "TOLABOY": "MUHAMMAD SAID XUJA TO'LABOY JOME MASJIDI"
}

# Namaz vaqtlari
masjidlar_data = {
    "NORBUTABEK": {"Bomdod": "04:45", "Peshin": "12:50", "Asr": "17:45", "Shom": "19:35", "Hufton": "21:15"},
    "GISHTLIK": {"Bomdod": "04:45", "Peshin": "12:50", "Asr": "17:15", "Shom": "19:30", "Hufton": "21:00"},
    "SHAYXULISLOM": {"Bomdod": "04:45", "Peshin": "12:45", "Asr": "17:35", "Shom": "19:35", "Hufton": "21:15"},
    "HADYA_HOJI": {"Bomdod": "04:55", "Peshin": "12:50", "Asr": "17:30", "Shom": "19:15", "Hufton": "20:55"},
    "AFGONBOG": {"Bomdod": "04:50", "Peshin": "12:50", "Asr": "17:30", "Shom": "19:20", "Hufton": "20:55"},
    "SAYYID_AXMADHON": {"Bomdod": "04:50", "Peshin": "12:50", "Asr": "17:20", "Shom": "19:20", "Hufton": "21:15"},
    "DEGRIZLIK": {"Bomdod": "04:30", "Peshin": "12:45", "Asr": "17:35", "Shom": "19:35", "Hufton": "21:15"},
    "SHAYXON": {"Bomdod": "04:40", "Peshin": "12:45", "Asr": "17:30", "Shom": "19:30", "Hufton": "21:00"},
    "ZINBARDOR": {"Bomdod": "04:30", "Peshin": "12:45", "Asr": "17:35", "Shom": "19:35", "Hufton": "21:15"},
    "ZAYNUL_OBIDIN": {"Bomdod": "04:40", "Peshin": "12:45", "Asr": "17:35", "Shom": "19:35", "Hufton": "21:15"},
    "HAZRATI_ABBOS": {"Bomdod": "04:40", "Peshin": "12:45", "Asr": "17:35", "Shom": "19:35", "Hufton": "21:15"},
    "SAODAT": {"Bomdod": "04:55", "Peshin": "12:50", "Asr": "17:20", "Shom": "19:10", "Hufton": "21:00"},
    "TOLABOY": {"Bomdod": "04:40", "Peshin": "12:45", "Asr": "17:35", "Shom": "19:35", "Hufton": "21:15"}
}

def load_user_settings():
    """Foydalanuvchi sozlamalarini yuklash"""
    global user_settings
    try:
        if os.path.exists(USER_SETTINGS_FILE):
            with open(USER_SETTINGS_FILE, 'r', encoding='utf-8') as f:
                user_settings = json.load(f)
        else:
            user_settings = {}
    except Exception as e:
        logger.error(f"Sozlamalar yuklashda xatolik: {e}")
        user_settings = {}

def save_user_settings():
    """Foydalanuvchi sozlamalarini saqlash"""
    try:
        with open(USER_SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(user_settings, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Sozlamalar saqlashda xatolik: {e}")

def get_user_selected_masjids(user_id: str) -> Set[str]:
    """Foydalanuvchi tanlagan masjidlar"""
    return set(user_settings.get(str(user_id), {}).get('selected_masjids', []))

def save_user_masjids(user_id: str, selected_masjids: Set[str]):
    """Foydalanuvchi tanlagan masjidlarni saqlash"""
    user_id_str = str(user_id)
    if user_id_str not in user_settings:
        user_settings[user_id_str] = {}
    user_settings[user_id_str]['selected_masjids'] = list(selected_masjids)
    save_user_settings()

def get_main_keyboard():
    """Asosiy klaviatura"""
    keyboard = [
        ['🕐 Barcha vaqtlar', '📍 Eng yaqin vaqt'],
        ['🕌 Masjidlar', '⚙️ Sozlamalar'],
        ['🔔 Bildirishnomalar', 'ℹ️ Yordam']
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_masjid_selection_keyboard(user_id: str) -> InlineKeyboardMarkup:
    """Masjidlarni tanlash klaviaturasi"""
    selected = get_user_selected_masjids(user_id)
    keyboard = []
    
    # Masjidlar ro'yxati (2 tadan qatorda)
    masjid_items = list(MASJIDLAR.items())
    for i in range(0, len(masjid_items), 2):
        row = []
        for j in range(2):
            if i + j < len(masjid_items):
                key, name = masjid_items[i + j]
                # Tanlangan bo'lsa ✅, tanlanmagan bo'lsa ⬜
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

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start buyrug'i"""
    user_id = update.effective_user.id
    
    # Agar yangi foydalanuvchi bo'lsa, barcha masjidlarni tanlangan qilib qo'yish
    if str(user_id) not in user_settings:
        save_user_masjids(user_id, set(MASJIDLAR.keys()))
    
    welcome_message = """🕌 Assalomu alaykum!

*Qo'qon Masjidlari Namoz Vaqti Botiga xush kelibsiz!*

🔔 *Bildirishnomalar sozlamalari:*
Siz faqat o'zingiz tanlagan masjidlar uchun push notification olasiz.

⚙️ *Sozlamalar* orqali kerakli masjidlarni belgilashingiz mumkin."""
    
    await update.message.reply_text(
        welcome_message,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=get_main_keyboard()
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xabarlarni qayta ishlash"""
    text = update.message.text
    user_id = update.effective_user.id
    
    if text == '⚙️ Sozlamalar':
        await handle_settings(update, context)
    elif text == '🔔 Bildirishnomalar':
        await handle_notifications_status(update, context)
    elif text == '🕌 Masjidlar':
        await handle_all_masjids(update, context)
    elif text == '🕐 Barcha vaqtlar':
        await handle_selected_masjids_times(update, context)
    else:
        await update.message.reply_text(
            "Quyidagi knopkalardan foydalaning:",
            reply_markup=get_main_keyboard()
        )

async def handle_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sozlamalar"""
    user_id = update.effective_user.id
    selected = get_user_selected_masjids(user_id)
    
    message = f"""⚙️ *BILDIRISHNOMALAR SOZLAMALARI*

Siz hozirda *{len(selected)} ta masjid* uchun bildirishnoma olasiz.

Quyida masjidlarni tanlang/bekor qiling:
✅ - Tanlangan (push olasiz)  
⬜ - Tanlanmagan (push olmaydigan)

*Eslatma:* Faqat tanlangan masjidlar vaqti yangilanganda push notification olasiz."""
    
    await update.message.reply_text(
        message,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=get_masjid_selection_keyboard(str(user_id))
    )

async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Inline button bosilganda"""
    query = update.callback_query
    await query.answer()
    
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

async def handle_notifications_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bildirishnomalar holati"""
    user_id = str(update.effective_user.id)
    selected = get_user_selected_masjids(user_id)
    
    if not selected:
        message = """🔔 *BILDIRISHNOMALAR HOLATI*

❌ Hech qanday masjid tanlanmagan!
Siz push notification olmaydigan.

⚙️ *Sozlamalar* orqali masjidlarni tanlang."""
    else:
        selected_names = [MASJIDLAR[key] for key in selected]
        message = f"""🔔 *BILDIRISHNOMALAR HOLATI*

✅ Faol - {len(selected)} ta masjid

*Tanlangan masjidlar:*
{chr(10).join([f"• {name}" for name in selected_names])}

Bu masjidlarning vaqti yangilanganda sizga push notification yuboriladi."""
    
    await update.message.reply_text(
        message,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=get_main_keyboard()
    )

async def handle_selected_masjids_times(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tanlangan masjidlar vaqtlari"""
    user_id = str(update.effective_user.id)
    selected = get_user_selected_masjids(user_id)
    
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

async def handle_all_masjids(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Barcha masjidlar (ko'rish uchun)"""
    message = "🕌 *BARCHA MASJIDLAR RO'YXATI:*\n\n"
    
    for i, (key, name) in enumerate(MASJIDLAR.items(), 1):
        message += f"{i}. {name}\n"
    
    message += f"\n📊 Jami: {len(MASJIDLAR)} ta masjid"
    message += "\n\n⚙️ *Sozlamalar* orqali kerakli masjidlarni tanlashingiz mumkin."
    
    await update.message.reply_text(
        message,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=get_main_keyboard()
    )

async def send_push_to_selected_users(masjid_key: str, new_times: Dict[str, str], application):
    """Faqat tanlangan foydalanuvchilarga push yuborish"""
    masjid_name = MASJIDLAR.get(masjid_key, masjid_key)
    now = datetime.now()
    
    message = f"""🕌 *NAMAZ VAQTLARI YANGILANDI*
📅 {now.strftime('%d.%m.%Y')} | ⏰ {now.strftime('%H:%M')}

*{masjid_name}*

🌅 Bomdod: *{new_times['Bomdod']}*
☀️ Peshin: *{new_times['Peshin']}*
🌆 Asr: *{new_times['Asr']}*
🌇 Shom: *{new_times['Shom']}*
🌙 Hufton: *{new_times['Hufton']}*

إِنَّ الصَّلَاةَ كَانَتْ عَلَى الْمُؤْمِنِينَ كِتَابًا مَّوْقُوتًا
_"Albatta, namoz mo'minlarga vaqtida farz qilingandir."_
Niso surasi, 103-oyat

📢 @{CHANNEL_USERNAME}"""
    
    # Faqat bu masjidni tanlagan foydalanuvchilarga yuborish
    sent_count = 0
    for user_id_str, settings in user_settings.items():
        selected_masjids = set(settings.get('selected_masjids', []))
        
        if masjid_key in selected_masjids:
            try:
                await application.bot.send_message(
                    chat_id=int(user_id_str),
                    text=message,
                    parse_mode=ParseMode.MARKDOWN
                )
                sent_count += 1
            except Exception as e:
                logger.error(f"Push yuborishda xatolik {user_id_str}: {e}")
    
    logger.info(f"{masjid_name} uchun {sent_count} ta foydalanuvchiga push yuborildi")

async def monitor_channel_updates():
    """Kanaldan yangilanishlarni kuzatish"""
    logger.info("Kanal monitoring boshlandi...")
    
    while True:
        try:
            # Bu yerda kanaldan yangi postlarni tekshirish logikasi
            # Namaz vaqtlari yangilanganini aniqlash
            # Har bir masjid uchun alohida push yuborish
            
            # Misol: NORBUTABEK masjidi yangilanganda
            # await send_push_to_selected_users("NORBUTABEK", {
            #     "Bomdod": "04:45", "Peshin": "12:50", "Asr": "17:45", 
            #     "Shom": "19:35", "Hufton": "21:15"
            # })
            
            await asyncio.sleep(1800)  # 30 daqiqada bir tekshirish
            
        except Exception as e:
            logger.error(f"Monitoring xatolik: {e}")
            await asyncio.sleep(300)  # 5 daqiqa kutish

def main():
    """Asosiy funksiya"""
    load_user_settings()
    
    try:
        # Bot yaratish - Python 3.13 uchun mos
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Handlerlar
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        application.add_handler(CallbackQueryHandler(handle_callback_query))
        
        logger.info("Bot ishga tushdi!")
        
        # Webhook rejimi (Render uchun)
        PORT = int(os.environ.get('PORT', 8000))
        
        # Kanal monitoring ni alohida task sifatida ishga tushirish
        async def start_monitoring():
            await monitor_channel_updates()
        
        # Background task
        asyncio.create_task(start_monitoring())
        
        # Webhook ishga tushirish
        application.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path=BOT_TOKEN,
            webhook_url=f"https://masjidlar-bot.onrender.com/{BOT_TOKEN}"
        )
        
    except Exception as e:
        logger.error(f"Bot ishga tushirishda xatolik: {e}")
        # Agar webhook ishlamasa, polling rejimini sinab ko'rish
        try:
            application.run_polling(drop_pending_updates=True)
        except Exception as polling_error:
            logger.error(f"Polling ham ishlamadi: {polling_error}")

if __name__ == '__main__':
    main()
