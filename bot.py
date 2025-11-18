import os
import random
import string
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
)

import pytz  # для timezone

# Загружаем токен из .env
load_dotenv()
TOKEN = os.getenv("TOKEN")

# Генерация пароля
def generate_password(length: int) -> str:
    chars = string.ascii_letters + string.digits + "!@#$%^&*()"
    return ''.join(random.choice(chars) for _ in range(length))

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Пароль 8 символов", callback_data="8")],
        [InlineKeyboardButton("Пароль 12 символов", callback_data="12")],
        [InlineKeyboardButton("Пароль 16 символов", callback_data="16")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Привет! Выберите длину пароля или используйте /password <длина>:",
        reply_markup=reply_markup,
    )

# Обработка кнопок
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    length = int(query.data)
    pwd = generate_password(length)
    await query.edit_message_text(f"Ваш пароль: `{pwd}`", parse_mode="Markdown")

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

    # Обязательно задаём timezone, чтобы не падало
    app.job_queue.timezone = pytz.timezone("Europe/Moscow")

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("password", password))
    app.add_handler(CallbackQueryHandler(button))

    print("Бот запущен и ждёт сообщений...")
    app.run_polling()

if __name__ == "__main__":
    main()
