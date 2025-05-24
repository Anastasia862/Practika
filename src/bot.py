import random
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

TOKEN = "7272092912:AAGhoWeu8i3GLjVrH7V5ttRUNnhwIT1BDc0"

async def start(update: Update, _: CallbackContext) -> None:
    await update.message.reply_text(
        "Привет! Давай сыграем в игру 'Угадай число'.\n"
        "Используй команду /guess чтобы начать."
    )

async def start_guess_game(update: Update, context: CallbackContext) -> None:
    secret_number = random.randint(1, 100)
    context.user_data["secret_number"] = secret_number
    await update.message.reply_text(
        "🎮 Я загадал число от 1 до 100. Попробуй угадать!\n"
        "Отправь мне число и проверь свою удачу."
    )

async def handle_guess(update: Update, context: CallbackContext) -> None:
    if "secret_number" not in context.user_data:
        await update.message.reply_text("Сначала начните игру командой /guess")
        return

    try:
        user_guess = int(update.message.text)
        secret_number = context.user_data["secret_number"]

        if user_guess < secret_number:
            await update.message.reply_text("Моё число больше!")
        elif user_guess > secret_number:
            await update.message.reply_text("Моё число меньше!")
        else:
            await update.message.reply_text(f"🎉 Правильно! Это было число {secret_number}!")
            del context.user_data["secret_number"]
    except ValueError:
        await update.message.reply_text("Пожалуйста, введите число!")

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("guess", start_guess_game))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_guess))

    application.run_polling()

if __name__ == "__main__":
    main()
