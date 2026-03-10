import json
import os

from dotenv import load_dotenv
from telegram import KeyboardButton, ReplyKeyboardMarkup, Update, WebAppInfo
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

APP_URL = "https://number-bot-beryl.vercel.app/"
OPEN_APP_TEXT = "🚀 Open App"


def parse_selected_numbers(data: dict) -> list[int]:
    raw_numbers = data.get("selectedNumbers")
    if not isinstance(raw_numbers, list):
        return []

    parsed_numbers = []
    for value in raw_numbers:
        if isinstance(value, int):
            parsed_numbers.append(value)
    return parsed_numbers


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return

    keyboard = [[KeyboardButton(text=OPEN_APP_TEXT, web_app=WebAppInfo(url=APP_URL))]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Tap button to open app:", reply_markup=markup)


async def on_web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    if not message or not message.web_app_data:
        return

    chat_id = update.effective_chat.id if update.effective_chat else None
    full_name = (
        update.effective_user.full_name if update.effective_user else None
    ) or "Unknown user"

    try:
        payload = json.loads(message.web_app_data.data)
    except json.JSONDecodeError:
        print(f"[WEB_APP_DATA] chat_id={chat_id} invalid_json", flush=True)
        await message.reply_text("Invalid data received from Mini App.")
        return

    selected_numbers = parse_selected_numbers(payload)
    numbers_text = ", ".join(str(num) for num in selected_numbers) if selected_numbers else "-"

    print(
        f"[WEB_APP_DATA] chat_id={chat_id} full_name={full_name} selected_numbers={selected_numbers}",
        flush=True,
    )
    await message.reply_text(f"Thank you {full_name}\nYour numbers: {numbers_text}")


def main() -> None:
    load_dotenv()
    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token:
        raise RuntimeError("BOT_TOKEN is missing. Set it in your environment or .env file.")

    app = Application.builder().token(bot_token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, on_web_app_data))

    print("Bot is running. Waiting for Telegram updates...", flush=True)
    app.run_polling()


if __name__ == "__main__":
    main()
