from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CallbackContext

from ..storage.memory_db import CATEGORIES, BTN_CATEGORIES, get_category_items


def show_categories(update: Update, context: CallbackContext):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton("Ishda")],
            [KeyboardButton("Ko'chada")],
            [KeyboardButton("Dam olishda")],
            [KeyboardButton("⬅️ Orqaga")],
        ],
        resize_keyboard=True,
    )
    update.message.reply_text("📁 Qaysi kategoriyani ochamiz?", reply_markup=kb)


def open_category(update: Update, context: CallbackContext):
    text = (update.message.text or "").strip()

    if text == "⬅️ Orqaga":
        kb = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(BTN_CATEGORIES)]], resize_keyboard=True
        )
        update.message.reply_text("Bosh menyu.", reply_markup=kb)
        return

    if text not in CATEGORIES:
        return  # boshqa text bo'lsa jim turamiz (xohlasangiz xabar beramiz)

    user_id = update.effective_user.id
    items = get_category_items(context.bot_data, user_id, text)

    if not items:
        update.message.reply_text(f"❗️ {text} kategoriyasida musiqa yo‘q.")
        return

    update.message.reply_text(f"🎧 {text} musiqalari:")
    for it in items:
        update.message.reply_audio(audio=it["file_id"], caption=it.get("title", ""))
