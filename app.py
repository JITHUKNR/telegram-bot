import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Bot token from BotFather
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # <-- ഇവിടെ നിന്റെ ടോക്കൺ ഇടുക

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ഹായ്! ഞാൻ നിങ്ങളുടെ AI സഹായിയാണ്. എന്തു സഹായമാണ് വേണ്ടത്? 😊")

# Echo message
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    reply_text = f"നീ പറഞ്ഞു: {user_text}"
    await update.message.reply_text(reply_text)

# Main function
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("Bot is running...")
    app.run_polling()
