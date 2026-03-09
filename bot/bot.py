from telegram import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo, Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import json, os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
APP_URL = "https://number-bot-beryl.vercel.app/"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [[KeyboardButton(text="🚀 Open App ", web_app=WebAppInfo(url=APP_URL))]]
    await update.message.reply_text("Tap button to open app:", reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True))

async def on_web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    raw = update.effective_message.web_app_data.data
    chat_id = update.effective_chat.id if update.effective_chat else None
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        print(f"[WEB_APP_DATA] chat_id={chat_id} invalid_json", flush=True)
        await update.effective_message.reply_text("Invalid data received from Mini App.")
        return

    full_name = data.get("fullName") or "Unknown user"
    selected_numbers = data.get("selectedNumbers") or []
    code = data.get("code") or "-"
    numbers_text = ", ".join(str(n) for n in selected_numbers) if selected_numbers else "-"
    print(
        f"[WEB_APP_DATA] chat_id={chat_id} full_name={full_name} selected_numbers={selected_numbers} code={code}",
        flush=True,
    )

    await update.effective_message.reply_text(
        f"Name: {full_name}\nNumbers: {numbers_text}\nCode: {code}"
    )

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, on_web_app_data))
print("Bot is running. Waiting for Telegram updates...", flush=True)
app.run_polling()
