# app.py
import logging
import asyncio
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import httpx

# ---- CONFIG ----
BOT_TOKEN = "8077047057:AAEfM3ka2VBchsxZkl7ED3bVAyfFowPGP50"
PORT = 10000  # Render default port
GOOGLE_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
GOOGLE_API_KEY = "YOUR_GOOGLE_API_KEY"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)

# ---- HANDLERS ----
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hey! 🚀 Glad you're here. How can I help you today?")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    chat_id = update.message.chat.id

    # Call Google Gemini API
    headers = {"Authorization": f"Bearer {GOOGLE_API_KEY}"}
    payload = {
        "prompt": user_text,
        "temperature": 0.7,
        "candidate_count": 1,
        "max_output_tokens": 200
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(GOOGLE_API_URL, headers=headers, json=payload)
        data = response.json()
        ai_response = data.get("candidates", [{}])[0].get("content", "Sorry, I couldn't generate a reply.")

    # Send reply
    await bot.send_message(chat_id=chat_id, text=ai_response)

# ---- MAIN ----
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run webhook on Render
    await app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=f"https://telegram-bot-k3de.onrender.com/webhook"
    )

if __name__ == "__main__":
    asyncio.run(main())
