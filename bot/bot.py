import json
import os
import io

from dotenv import load_dotenv
from telegram import KeyboardButton, ReplyKeyboardMarkup, Update, WebAppInfo
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from db.db import init_db, close_db, get_or_create_user, save_games, save_receipt
from receipt.receipt import generate_transaction_id
from pdf.pdf import generate_receipt_pdf

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

    user = update.effective_user
    chat_id = update.effective_chat.id if update.effective_chat else None
    full_name = user.full_name if user else "Unknown"
    username = user.username if user else None
    telegram_id = user.id if user else None

    # ─── Parse payload ────────────────────────────────────────
    try:
        payload = json.loads(message.web_app_data.data)
    except json.JSONDecodeError:
        await message.reply_text("Invalid data received.")
        return

    games = parse_games(payload)
    bank_name = payload.get("bank_name", "Unknown")
    amount = float(payload.get("amount", 0))
    start_param = payload.get("startParam") or None

    if not games:
        await message.reply_text("No games received.")
        return

    print(f"[WEB_APP_DATA] chat_id={chat_id} full_name={full_name} games={games} bank={bank_name} amount={amount}", flush=True)

    # ─── Save to DB ───────────────────────────────────────────
    user_id = await get_or_create_user(telegram_id, full_name, username, start_param)
    await save_games(user_id, games)

    transaction_id = generate_transaction_id()
    await save_receipt(transaction_id, user_id, bank_name, amount)

    # ─── Generate PDF ─────────────────────────────────────────
    pdf_bytes = generate_receipt_pdf(
        transaction_id=transaction_id,
        full_name=full_name,
        bank_name=bank_name,
        amount=amount,
        games=games,
    )

    # ─── Send PDF to user ─────────────────────────────────────
    pdf_file = io.BytesIO(pdf_bytes)
    pdf_file.name = f"{transaction_id}.pdf"

    await message.reply_document(
        document=pdf_file,
        filename=f"{transaction_id}.pdf",
        caption=f"✅ Payment received!\nTransaction: {transaction_id}",
    )


async def post_init(application: Application) -> None:
    await init_db()


async def post_shutdown(application: Application) -> None:
    await close_db()


def main() -> None:
    load_dotenv()
    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token:
        raise RuntimeError("BOT_TOKEN is missing.")

    app = (
        Application.builder()
        .token(bot_token)
        .post_init(post_init)
        .post_shutdown(post_shutdown)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, on_web_app_data))

    print("Bot is running...", flush=True)
    app.run_polling()


if __name__ == "__main__":
    main()