from telegram import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import ConversationHandler
from Bot.storage.memory_db import CATEGORIES, BTN_CATEGORIES, add_music

WAITING_CATEGORY = 1


def audio_received(update, context):
    audio = update.message.audio

    if not audio:
        update.message.reply_text("Audio topilmadi.")
        return ConversationHandler.END

    context.user_data["pending_audio_file_id"] = audio.file_id
    context.user_data["pending_audio_title"] = audio.title or audio.file_name or "Audio"

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton("Ishda")],
            [KeyboardButton("Ko'chada")],
            [KeyboardButton("Dam olishda")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

    update.message.reply_text(
        "Musiqani qaysi kategoriyaga saqlaymiz?", reply_markup=keyboard
    )

    return WAITING_CATEGORY


def choose_category(update, context):
    text = update.message.text
    user_id = update.effective_user.id

    if text not in CATEGORIES:
        update.message.reply_text("Iltimos, faqat knopkadan tanlang.")
        return WAITING_CATEGORY

    file_id = context.user_data.get("pending_audio_file_id")
    title = context.user_data.get("pending_audio_title", "Audio")

    if not file_id:
        update.message.reply_text("Audio topilmadi.")
        return ConversationHandler.END

    add_music(context.bot_data, user_id, text, file_id, title)

    context.user_data.clear()

    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(BTN_CATEGORIES)]], resize_keyboard=True
    )

    update.message.reply_text(f"✅ Saqlandi: {text}", reply_markup=keyboard)

    return ConversationHandler.END


def cancel(update, context):
    context.user_data.clear()
    update.message.reply_text("Bekor qilindi.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END
