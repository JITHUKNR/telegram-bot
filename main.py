import openai
from telebot import TeleBot

bot = TeleBot("8077047057:AAGAN7hqalnJIdAW87_tx9nLBdqtc6Jdmr4")
openai.api_key = "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"

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
