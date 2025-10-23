import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import random

BOT_TOKEN = os.getenv("BOT_TOKEN")
SOURCE_CHANNEL = "@YourSourceChannel"  # Channel where photos exist
DEST_CHANNEL = "@YourDestinationChannel"  # Where bot will send

async def send_random_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Fetch recent messages from source channel
    messages = await context.bot.get_chat(SOURCE_CHANNEL).get_history(limit=50)
    
    # Filter only photo messages
    photo_msgs = [msg for msg in messages if msg.photo]
    if not photo_msgs:
        await update.message.reply_text("No photos found in channel.")
        return

    # Pick a random photo
    selected_msg = random.choice(photo_msgs)

    # Send photo to destination channel (can be same as source)
    await context.bot.copy_message(chat_id=DEST_CHANNEL, from_chat_id=SOURCE_CHANNEL, message_id=selected_msg.message_id)
    await update.message.reply_text("✅ Photo sent!")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Use /sendphoto to get a photo from channel.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("sendphoto", send_random_photo))
    app.run_polling()

if __name__ == "__main__":
    main()
