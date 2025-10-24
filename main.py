import os
from telebot import TeleBot
from openai import OpenAI

# Initialize OpenAI client with environment variable
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

# Initialize Telegram bot with environment variable
bot = TeleBot(os.environ['TELEGRAM_BOT_TOKEN'])

@bot.message_handler(func=lambda msg: True)
def handle(msg):
    user_msg = msg.text

    # Create chat completion with Taekook personality
    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {
                "role": "system",
                "content": "You are Taekook from BTS, extremely flirty, playful, hot, full of emojis 🌚😏🔥💦💖👅💋😉✨😍💫."
            },
            {
                "role": "user",
                "content": user_msg
            }
        ]
    )

    # Reply to user
    import time

bot.reply_to(msg, response.choices[0].message.content)
time.sleep(0.5)  # half-second delay

# Start the bot
bot.polling()
