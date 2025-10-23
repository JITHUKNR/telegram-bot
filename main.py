import openai
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import logging

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# BOT persona: playful, flirty, always reply in English
BOT_PERSONA = ("You are a playful, flirty AI assistant named JithuBot. "
               "Always reply in English, even if the user types in Malayalam. "
               "Keep replies friendly, teasing, and fun.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("HEY BABY GURL🌚💜")

async def character_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": BOT_PERSONA},
            {"role": "user", "content": user_text}
        ]
    )
    reply_text = response.choices[0].message.content
    await update.message.reply_text(reply_text)

    # OpenAI API call
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": BOT_PERSONA},
            {"role": "user", "content": user_text}
        ]
    )

    reply_text = response.choices[0].message.content

    # Safe logging
    user_id = update.message.from_user.id
    user_name = update.message.from_user.username
    logger.info(f"Message from {user_name} ({user_id}): {user_text}")

    await update.message.reply_text(reply_text)

# Telegram bot setup
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, character_reply))

app.run_polling()
