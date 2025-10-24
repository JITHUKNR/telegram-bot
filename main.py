import telebot
import random
from telebot import types

BOT_TOKEN = "8077047057:AAGAN7hqalnJIdAW87_tx9nLBdqtc6Jdmr4"
CHANNEL_USERNAME = "@taecockme"

bot = telebot.TeleBot(BOT_TOKEN)

# /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Normal Reply Keyboard Button
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Send"))
    bot.send_message(message.chat.id, "𝐇𝐄𝐘 𝐁𝐀𝐁𝐘 𝐆𝐔𝐑𝐋🌚🍒.", reply_markup=markup)

# “Send” button clicked
@bot.message_handler(func=lambda message: message.text == "Send")
def send_random_media(message):
    media_links = [
        "https://t.me/taecockme/1",
        "https://t.me/taecockme/2",
        "https://t.me/taecockme/3",
        "https://t.me/taecockme/4"
    ]
    selected = random.choice(media_links)
    bot.send_message(message.chat.id, f"𝐔𝐇𝐌𝐌𝐌 :\n{selected}")

print("Bot is running...")
bot.infinity_polling()
