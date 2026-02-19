from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CallbackContext
from ..storage.memory_db import BTN_CATEGORIES


def start(update: Update, context: CallbackContext):
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(BTN_CATEGORIES)]], resize_keyboard=True
    )
    update.message.reply_text(
        "Assalomu alaykum!\n\n"
        "🎵 Audio yuboring — men qaysi kategoriyaga saqlashni so'rayman.\n"
        f"📁 {BTN_CATEGORIES} bo'limidan musiqalarni eshitasiz.",
        reply_markup=kb,
    )
