import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# BOT_TOKEN from environment
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "HEY BABY GURL 😉"
    )

# Character / playful reply
async def character_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if "hi" in text or "hello" in text:
        reply = "ഹായ് 😏! എവിടെയായിരുന്നു നീ ഇനിയുള്ളത് കാണാതെ?"
    elif "how are you" in text:
        reply = "ഞാൻ super 😎, നീ എന്നെ കാണുമ്പോൾ സുഖമാണോ?"
    elif "flirt" in text or "cute" in text:
        reply = "എവിടെയും നിന്നെ പോലെ cute ആരുമില്ല 😏"
    else:
        reply = "😅 ഹോ, interesting! പിന്നെ continue ചെയ്‌താൽ കാണാം 😉"

    # Safe logging for debug
    user_id = update.message.from_user.id
    user_name = update.message.from_user.username
    logger.info(f"Message from {user_name} ({user_id}): {text}")

    await update.message.reply_text(reply)

# Application setup
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, character_reply))

app.run_polling()
