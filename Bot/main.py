from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
)

from Bot.config.settings import BOT_TOKEN
from Bot.handlers import (
    start,
    audio_received,
    choose_category,
    cancel,
    WAITING_CATEGORY,
    show_categories,
    open_category,
)
from Bot.storage.memory_db import BTN_CATEGORIES


def main():
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Conversation (audio → kategoriya tanlash)
    conv = ConversationHandler(
        entry_points=[MessageHandler(Filters.audio, audio_received)],
        states={
            WAITING_CATEGORY: [
                MessageHandler(Filters.text & ~Filters.command, choose_category)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(conv)

    dp.add_handler(
        MessageHandler(Filters.regex(f"^{BTN_CATEGORIES}$"), show_categories)
    )
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, open_category))

    updater.start_polling()
    updater.idle()
