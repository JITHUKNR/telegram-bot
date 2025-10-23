import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# BOT_TOKEN
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("𝐇𝐄𝐘 𝐁𝐀𝐁𝐘 𝐆𝐔𝐑𝐋🌚🍒")

# Log all text messages safely
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_name = update.message.from_user.username
    text = update.message.text

    # Safe logging: only logs to Render, not storing permanently
    logger.info(f"Message from {user_name} ({user_id}): {text}")

    # Optional: reply back
    await update.message.reply_text(f"You said: {text}")

# Application setup
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

app.run_polling()
