import os
import random
import string
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Загружаем токен из .env
load_dotenv()
TOKEN = os.getenv("TOKEN")

# Генерация пароля
def generate_password(length: int) -> str:
    chars = string.ascii_letters + string.digits + "!@#$%^&*()"
    return ''.join(random.choice(chars) for _ in range(length))

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот-генератор паролей.\n"
        "Напиши /password <длина>\nНапример: /password 12"
    )

# /password
async def password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Использование: /password <длина>")
        return
    try:
        length = int(context.args[0])
    except ValueError:
        await update.message.reply_text("Длина должна быть числом.")
        return
    pwd = generate_password(length)
    await update.message.reply_text(f"Ваш пароль: `{pwd}`", parse_mode="Markdown")

# Запуск бота
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("password", password))
    print("Бот запущен и ждёт сообщений...")
    app.run_polling()  # <- работает на Windows без JobQueue и ошибок pytz

if __name__ == "__main__":
    main()
