import random
import string
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8578175082:AAHttuCSz4xVlvJAiG4Zi3vphxl4jCnoTjg"  # <-- вставьте сюда токен

def generate_password(length=12):
    chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(chars) for _ in range(length))
    return password

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Сгенерировать пароль", callback_data='generate')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Привет! Нажми кнопку, чтобы сгенерировать пароль:', reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'generate':
        password = generate_password()
        await query.edit_message_text(text=f"Ваш новый пароль:\n`{password}`", parse_mode='Markdown')

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Бот запущен...")
    app.run_polling()

if __name__ == '__main__':
    main()
