import asyncio
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import httpx
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
PORT = int(os.environ.get("PORT", 8000))
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
GOOGLE_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

bot = Bot(token=BOT_TOKEN)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hey! 🚀 Glad you're here.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    chat_id = update.message.chat.id

    headers = {"Authorization": f"Bearer {GOOGLE_API_KEY}"}
    payload = {"prompt": user_text, "temperature": 0.7, "candidate_count": 1, "max_output_tokens": 200}

    async with httpx.AsyncClient() as client:
        r = await client.post(GOOGLE_API_URL, headers=headers, json=payload)
        data = r.json()
        ai_response = data.get("candidates", [{}])[0].get("content", "Sorry, I couldn't generate a reply.")

    await bot.send_message(chat_id=chat_id, text=ai_response)

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run webhook
    await app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=f"https://telegram-bot-k3de.onrender.com/webhook"
    )

if __name__ == "__main__":
    asyncio.run(main())
