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

MASJID_LOCATIONS = {
    "NORBUTABEK JOME MASJIDI": {"latitude": 40.539106, "longitude": 70.952241, "address": "Yangi Chorsu"},
    "G'ISHTLIK JOME MASJIDI": {"latitude": 40.528657, "longitude": 70.928307, "address": "G'ishtlik mahallasi"},
    "SHAYXULISLOM JOME MASJIDI": {"latitude": 40.543609, "longitude": 70.945079, "address": "Shayxulislom mahallasi"},
    "HADYA HOJI SHALDIRAMOQ JOME MASJIDI": {"latitude": 40.526414, "longitude": 70.942138, "address": "Shaldiramoq"},
    "AFG'ONBOG' JOME MASJIDI": {"latitude": 40.507149, "longitude": 70.921600, "address": "Afg'onbog' mahallasi"}
}

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
    main()
