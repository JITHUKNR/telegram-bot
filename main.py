import os
import openai
from telebot import TeleBot

# Load OpenAI API key from environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Telegram Bot token from environment variable
bot = TeleBot(os.environ.get("TELEGRAM_BOT_TOKEN"))

@bot.message_handler(func=lambda msg: True)
def handle(msg):
    user_msg = msg.text
    response = openai.ChatCompletion.create(
        model="gpt-5-mini",
        messages=[
            {"role": "system", "content": "You are Taekook from BTS, extremely flirty, playful, hot, full of emojis 🌚😏🔥💦💖👅💋😉✨😍💫."},
            {"role": "user", "content": user_msg}
        ]
    )
    bot.reply_to(msg, response.choices[0].message['content'])

bot.polling()
