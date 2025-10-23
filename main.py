import os
import logging
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# -------------------------------
# Environment Variables
# -------------------------------
BOT_TOKEN = os.getenv("BOT_TOKEN")            # Telegram Bot token
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # OpenAI API key
openai.api_key = OPENAI_API_KEY

# -------------------------------
# Logging
# -------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -------------------------------
# Bot persona (Taekook male flirting style)
# -------------------------------
BOT_PERSONA = (
    "You are a playful, flirty male AI assistant named JithuBot. "
    "You talk like BTS Taekook (Taehyung & Jungkook) in style—teasing, charming, cute flirting. "
    "Always reply in English, even if the user types in Malayalam. "
    "Keep replies friendly, fun, and full of personality, like a male character chatting with someone you like."
)

# -------------------------------
# /start command
# -------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hey 😎, I’m JithuBot! Wanna chat with me? 😉")

# -------------------------------
# AI-powered auto reply
# -------------------------------
async def character_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    try:
        # OpenAI API call with proper persona
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": BOT_PERSONA},
                {"role": "user", "content": user_text}
            ]
        )

        reply_text = response.choices[0].message.content

        # Logging user messages
        user_id = update.message.from_user.id
        user_name = update.message.from_user.username
        logger.info(f"Message from {user_name} ({user_id}): {user_text}")

        # Send reply
        await update.message.reply_text(reply_text)

    except Exception as e:
        logger.error(f"Error in character_reply: {e}")
        await update.message.reply_text("Oops 😅, something went wrong. Try again!")

# -------------------------------
# Main Bot Setup
# -------------------------------
app = ApplicationBuilder().token(BOT_TOKEN).build()

# Command handler
app.add_handler(CommandHandler("start", start))

# Message handler for all normal text messages
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, character_reply))

# Run bot
app.run_polling()
