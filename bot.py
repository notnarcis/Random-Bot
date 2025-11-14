import random
from telegram.ext import Updater, CommandHandler

TOKEN = "8578175082:AAHttuCSz4xVlvJAiG4Zi3vphxl4jCnoTjg"

def start(update, context):
    update.message.reply_text(
        "Привет! Я бот-генератор паролей.\n"
        "Напиши /password длина\nНапример: /password 12"
    )

def password(update, context):
    if len(context.args) != 1:
        update.message.reply_text("Использование: /password 12")
        return

    try:
        length = int(context.args[0])
    except ValueError:
        update.message.reply_text("Длина должна быть числом.")
        return

    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"
    generated = "".join(random.choice(chars) for _ in range(length))

    update.message.reply_text(f"Ваш пароль: \n`{generated}`", parse_mode="Markdown")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("password", password))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
    
