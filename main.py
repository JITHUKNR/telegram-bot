import os
import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# -------------------------------
# Environment Variables
# -------------------------------
BOT_TOKEN = os.getenv("BOT_TOKEN")                  # Telegram bot token
SOURCE_CHANNEL = "@YourSourceChannel"              # Channel where photos are uploaded
DEST_CHANNEL = "@YourDestinationChannel"          # Channel where bot will send photos
ALLOWED_USERS = {123456789}                        # Optional: allowed user IDs

# -------------------------------
# Logging
# -------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -------------------------------
# Start command
# -------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi 😎! Press the button below to send a photo to the channel.")
    keyboard = [
        [InlineKeyboardButton("📤 Send Random Photo", callback_data="send_photo")]
    ]
    await update.message.reply_text("Choose an action:", reply_markup=InlineKeyboardMarkup(keyboard))

# -------------------------------
# Button callback
# -------------------------------
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # remove "loading"
    user = query.from_user

    # Permission check
    if ALLOWED_USERS and user.id not in ALLOWED_USERS:
        await query.edit_message_text("❌ You are not allowed to send photos.")
        return

    try:
        # Fetch recent messages from source channel
        chat = await context.bot.get_chat(SOURCE_CHANNEL)
        messages = await chat.get_history(limit=50)
        photo_msgs = [msg for msg in messages if msg.photo]

        if not photo_msgs:
            await query.edit_message_text("No photos found in the source channel.")
            return

        # Pick a random photo
        selected_msg = random.choice(photo_msgs)

        # Copy message to destination channel
        await context.bot.copy_message(chat_id=DEST_CHANNEL, from_chat_id=SOURCE_CHANNEL, message_id=selected_msg.message_id)
        await query.edit_message_text("✅ Photo sent to the channel!")

    except Exception as e:
        logger.error(f"Error sending photo: {e}")
        await query.edit_message_text("❌ Failed to send photo. Check bot permissions or channel IDs.")

# -------------------------------
# Main
# -------------------------------
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler, pattern="^send_photo$"))
    app.run_polling()

if __name__ == "__main__":
    main()
