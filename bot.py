import os
import random
import string

from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

load_dotenv()
TOKEN = os.getenv("TOKEN")

def generate_password(length: int, use_special: bool = True) -> str:
    chars = string.ascii_letters + string.digits
    if use_special:
        chars += "!@#$%^&*()_+=-{}[]<>?"
    return ''.join(random.choice(chars) for _ in range(length))

def get_keyboard(length, use_special):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 Сгенерировать", callback_data=f"regen:{length}:{int(use_special)}")],
        [
            InlineKeyboardButton("➕ длина", callback_data=f"len:{length+1}:{int(use_special)}"),
            InlineKeyboardButton("➖ длина", callback_data=f"len:{max(4, length-1)}:{int(use_special)}"),
        ],
        [
            InlineKeyboardButton(
                "❌ Спецсимволы" if use_special else "✔ Спецсимволы",
                callback_data=f"spec:{length}:{int(not use_special)}"
            )
        ]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я генератор паролей.\n"
        "Можешь использовать кнопки или написать /password 12",
        reply_markup=get_keyboard(12, True)
    )

async def password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.messag
