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


def parse_games(data: dict) -> list[list[int]]:
    raw_games = data.get("games")
    if not isinstance(raw_games, list):
        return []

    parsed_games = []
    for game in raw_games:
        if isinstance(game, list) and len(game) == 2:
            parsed_games.append([int(game[0]), int(game[1])])
    return parsed_games


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

    games = parse_games(payload)

    print(
        f"[WEB_APP_DATA] chat_id={chat_id} full_name={full_name} games={games}",
        flush=True,
    )

    if not games:
        await message.reply_text("No games received.")
        return

    games_text = "\n".join(
        f"Game {i + 1}: {g[0]} , {g[1]}" for i, g in enumerate(games)
    )
    await message.reply_text(f"Thank you {full_name}!\n\n{games_text}")


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