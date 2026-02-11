import asyncio
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = "7961957203:AAEZ1PQXOhxYY_dofzdLRhLR73Rar_NZnro"
JOIN_CHANNEL = "@finalshotir"
STORAGE_CHANNEL = "@FinalStorage"


async def auto_delete(context, chat_id, msg_id):
    await asyncio.sleep(120)
    try:
        await context.bot.delete_message(chat_id, msg_id)
    except:
        pass


async def is_member(bot, user_id):
    member = await bot.get_chat_member(JOIN_CHANNEL, user_id)
    return member.status in ["member", "administrator", "creator"]


async def send_file(context, chat_id, msg_id):
    sent = await context.bot.copy_message(
        chat_id=chat_id,
        from_chat_id=STORAGE_CHANNEL,
        message_id=msg_id
    )
    context.application.create_task(
        auto_delete(context, chat_id, sent.message_id)
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not await is_member(context.bot, user_id):
        await update.message.reply_text(
            f"❌ ابتدا عضو شو:\nhttps://t.me/{JOIN_CHANNEL.replace('@','')}"
        )
        return

    if context.args and context.args[0].isdigit():
        msg_id = int(context.args[0])
        await send_file(context, update.effective_chat.id, msg_id)
        return

    await update.message.reply_text("❗ لینک دانلود نامعتبر است")


async def get_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.text.isdigit():
        return

    msg_id = int(update.message.text)
    await send_file(context, update.effective_chat.id, msg_id)


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_number))

    print("Bot Running...")
    app.run_polling()


if name == "main":
    main()
