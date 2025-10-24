import telebot
import random

# ഇവിടെ നിന്റെ ബോട്ട് ടോക്കൺ ഇടുക
BOT_TOKEN = "8077047057:AAGAN7hqalnJIdAW87_tx9nLBdqtc6Jdmr4"  # BotFather-ൽ നിന്നുള്ള Token
CHANNEL_USERNAME = "@taecockme"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "ഹായ്! ഞാൻ @taecockme ചാനലിൽ നിന്ന് റാൻഡം ഫോട്ടോ അല്ലെങ്കിൽ വീഡിയോ അയക്കും. 'send' എന്ന് ടൈപ്പ് ചെയ്‌താൽ തുടങ്ങാം.")

@bot.message_handler(func=lambda msg: msg.text and msg.text.lower() == "send")
def send_random_media(message):
    media_links = [
        "https://t.me/taecockme/1",
        "https://t.me/taecockme/2",
        "https://t.me/taecockme/3",
        "https://t.me/taecockme/4"
    ]

    selected = random.choice(media_links)
    bot.send_message(message.chat.id, f"ഇതാ ഒരു റാൻഡം പോസ്റ്റ്:\n{selected}")

print("Bot is running...")
bot.infinity_polling()
