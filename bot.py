import os
import json
import logging
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode
import math

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv('BOT_TOKEN', '1436546945:AAFInxVnh3D-B1D4nI6y6I4vxMP5jK-12H4')
CHANNEL_USERNAME = os.getenv('CHANNEL_USERNAME', 'quqonnamozvaqti')
DATA_FILE = 'masjidlar_data.json'

masjidlar_data = {}

MASJID_LOCATIONS = {
    "NORBUTABEK JOME MASJIDI": {"latitude": 40.539106, "longitude": 70.952241, "address": "Yangi Chorsu"},
    "G'ISHTLIK JOME MASJIDI": {"latitude": 40.528657, "longitude": 70.928307, "address": "G'ishtlik mahallasi"},
    "SHAYXULISLOM JOME MASJIDI": {"latitude": 40.543609, "longitude": 70.945079, "address": "Shayxulislom mahallasi"},
    "HADYA HOJI SHALDIRAMOQ JOME MASJIDI": {"latitude": 40.526414, "longitude": 70.942138, "address": "Shaldiramoq"},
    "AFG'ONBOG' JOME MASJIDI": {"latitude": 40.507149, "longitude": 70.921600, "address": "Afg'onbog' mahallasi"},
    "SAYYID AXMADHON HOJI JOME MASJIDI": {"latitude": 40.587726, "longitude": 70.907420, "address": "Dang'ara tumani"},
    "DEGRIZLIK JOME MASJIDI": {"latitude": 40.587726, "longitude": 70.907420, "address": "Degrizlik mahallasi"},
    "SHAYXON JOME MASJIDI": {"latitude": 40.523430, "longitude": 70.950863, "address": "Shayxon mahallasi"},
    "ZINBARDOR JOME MASJIDI": {"latitude": 40.529738, "longitude": 70.948655, "address": "Isfara guzar"},
    "ZAYNUL OBIDIN AYRILISH JOME MASJIDI": {"latitude": 40.544612, "longitude": 70.963684, "address": "Ayrilish mahallasi"},
    "XAZRATI ABBOS MOLBOZORI JOME MASJIDI": {"latitude": 40.521234, "longitude": 70.966085, "address": "Molbozor mahallasi"},
    "SAODAT JOME MASJIDI": {"latitude": 40.549047, "longitude": 70.972652, "address": "Saodat mahallasi"},
    "MUHAMMAD SAID XUJA TO'LABOY JOME MASJIDI": {"latitude": 40.567974, "longitude": 70.949198, "address": "To'laboy mahallasi"}
}

NAMAZ_TIMES = ['Bomdod', 'Peshin', 'Asr', 'Shom', 'Hufton']

def get_main_keyboard():
    keyboard = [
        ['🕐 Barcha vaqtlar', '📍 Eng yaqin vaqt'],
        ['🕌 Masjidlar', '🔄 Yangilash']
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = """🕌 Assalomu alaykum!

Qo'qon Masjidlari Namaz Vaqti Botiga xush kelibsiz!

🕐 Barcha vaqtlar - Masjidlar namaz vaqtlari
📍 Eng yaqin vaqt - Keyingi namaz vaqti
🕌 Masjidlar - 13 ta masjid ro'yxati
🔄 Yangilash - Ma'lumotlarni yangilash"""
    
    await update.message.reply_text(welcome_message, reply_markup=get_main_keyboard())

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text == '🕌 Masjidlar':
        message = "🕌 Qo'qon shahri masjidlari:\n\n"
        for i, (masjid, location) in enumerate(MASJID_LOCATIONS.items(), 1):
            message += f"{i}. {masjid}\n   📍 {location['address']}\n\n"
        
        await update.message.reply_text(message, reply_markup=get_main_keyboard())
    
    elif text == '🔄 Yangilash':
        await update.message.reply_text('✅ Ma\'lumotlar yangilandi!', reply_markup=get_main_keyboard())
    
    else:
        await update.message.reply_text("Quyidagi knopkalardan foydalaning:", reply_markup=get_main_keyboard())

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    logger.info("Bot ishga tushdi!")
    
    PORT = int(os.environ.get('PORT', 8000))
    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=BOT_TOKEN,
        webhook_url=f"https://masjidlar-bot.onrender.com/{BOT_TOKEN}"
    )

if __name__ == '__main__':
    main()echo "python-telegram-bot==20.7" > requirements.txt
echo "python-dotenv==1.0.0" >> requirements.txt
nano README.md

nano README.md
øimport os
import json
import logging
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode
import math

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv('BOT_TOKEN', '1436546945:AAFInxVnh3D-B1D4nI6y6I4vxMP5jK-12H4')
CHANNEL_USERNAME = os.getenv('CHANNEL_USERNAME', 'quqonnamozvaqti')
DATA_FILE = 'masjidlar_data.json'

masjidlar_data = {}

MASJID_LOCATIONS = {
    "NORBUTABEK JOME MASJIDI": {"latitude": 40.539106, "longitude": 70.952241, "address": "Yangi Chorsu"},
    "G'ISHTLIK JOME MASJIDI": {"latitude": 40.528657, "longitude": 70.928307, "address": "G'ishtlik mahallasi"},
    "SHAYXULISLOM JOME MASJIDI": {"latitude": 40.543609, "longitude": 70.945079, "address": "Shayxulislom mahallasi"},
    "HADYA HOJI SHALDIRAMOQ JOME MASJIDI": {"latitude": 40.526414, "longitude": 70.942138, "address": "Shaldiramoq"},
    "AFG'ONBOG' JOME MASJIDI": {"latitude": 40.507149, "longitude": 70.921600, "address": "Afg'onbog' mahallasi"},
    "SAYYID AXMADHON HOJI JOME MASJIDI": {"latitude": 40.587726, "longitude": 70.907420, "address": "Dang'ara tumani"},
    "DEGRIZLIK JOME MASJIDI": {"latitude": 40.587726, "longitude": 70.907420, "address": "Degrizlik mahallasi"},
    "SHAYXON JOME MASJIDI": {"latitude": 40.523430, "longitude": 70.950863, "address": "Shayxon mahallasi"},
    "ZINBARDOR JOME MASJIDI": {"latitude": 40.529738, "longitude": 70.948655, "address": "Isfara guzar"},
    "ZAYNUL OBIDIN AYRILISH JOME MASJIDI": {"latitude": 40.544612, "longitude": 70.963684, "address": "Ayrilish mahallasi"},
    "XAZRATI ABBOS MOLBOZORI JOME MASJIDI": {"latitude": 40.521234, "longitude": 70.966085, "address": "Molbozor mahallasi"},
    "SAODAT JOME MASJIDI": {"latitude": 40.549047, "longitude": 70.972652, "address": "Saodat mahallasi"},
    "MUHAMMAD SAID XUJA TO'LABOY JOME MASJIDI": {"latitude": 40.567974, "longitude": 70.949198, "address": "To'laboy mahallasi"}
}

NAMAZ_TIMES = ['Bomdod', 'Peshin', 'Asr', 'Shom', 'Hufton']

def get_main_keyboard():
    keyboard = [
        ['🕐 Barcha vaqtlar', '📍 Eng yaqin vaqt'],
        ['🕌 Masjidlar', '📍 Location bo\'yicha'],
        ['🔄 Yangilash', 'ℹ️ Yordam']
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def load_data():
    global masjidlar_data
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                masjidlar_data = json.load(f)
        else:
            test_times = {
                "Bomdod": "04:45",
                "Peshin": "12:50", 
                "Asr": "17:20",
                "Shom": "19:15",
                "Hufton": "21:20"
            }
            
            masjidlar_data = {}
            for masjid_name in MASJID_LOCATIONS.keys():
                masjidlar_data[masjid_name] = {
                    "times": test_times.copy(),
                    "last_update": datetime.now().strftime("%d.%m.%Y")
                }
            save_data()
    except Exception as e:
        logger.error(f"Ma'lumotlarni yuklashda xatolik: {e}")

def save_data():
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(masjidlar_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Saqlashda xatolik: {e}")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = """🕌 Assalomu alaykum!

*Qo'qon Masjidlari Namoz Vaqti Botiga xush kelibsiz!*

🕐 *Barcha vaqtlar* - Barcha masjidlar vaqtlari
📍 *Eng yaqin vaqt* - Keyingi namaz vaqti
🕌 *Masjidlar* - 13 ta masjid ro'yxati
📍 *Location bo'yicha* - GPS orqali eng yaqin masjid
🔄 *Yangilash* - Ma'lumotlarni yangilash
ℹ️ *Yordam* - Bot haqida ma'lumot"""
    
    await update.message.reply_text(
        welcome_message, 
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=get_main_keyboard()
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text == '🕌 Masjidlar':
        message = "🕌 *Qo'qon shahri masjidlari:*\n\n"
        for i, (masjid, location) in enumerate(MASJID_LOCATIONS.items(), 1):
            message += f"{i}. {masjid}\n   📍 {location['address']}\n\n"
        
        await update.message.reply_text(
            message, 
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_main_keyboard()
        )
    
    elif text == 'ℹ️ Yordam':
        help_text = f"""📖 *Bot haqida:*

🕐 Barcha vaqtlar - Masjidlar namaz vaqtlari
📍 Eng yaqin vaqt - Keyingi namaz vaqti
🕌 Masjidlar - 13 ta masjid ro'yxati
📍 Location bo'yicha - GPS orqali eng yaqin masjid
🔄 Yangilash - Ma'lumotlarni yangilash

📢 Ma'lumotlar: @{CHANNEL_USERNAME}"""
        
        await update.message.reply_text(
            help_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_main_keyboard()
        )
    
    elif text == '🔄 Yangilash':
        await update.message.reply_text('🔄 Ma\'lumotlar yangilanmoqda...')
        
        for masjid_name in masjidlar_data:
            masjidlar_data[masjid_name]['last_update'] = datetime.now().strftime("%d.%m.%Y")
        save_data()
        
        await update.message.reply_text(
            '✅ Ma\'lumotlar yangilandi!',
            reply_markup=get_main_keyboard()
        )
    
    else:
        await update.message.reply_text(
            "Quyidagi knopkalardan foydalaning:",
            reply_markup=get_main_keyboard()
        )

def main():
    load_data()
    
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    logger.info("Bot ishga tushdi!")
    
    PORT = int(os.environ.get('PORT', 8000))
    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=BOT_TOKEN,
        webhook_url=f"https://masjidlar-bot.onrender.com/{BOT_TOKEN}"
    )

if __name__ == '__main__':
    main()
