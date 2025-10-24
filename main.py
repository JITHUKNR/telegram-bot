import os
import logging
from flask import Flask, request, jsonify
from telegram import Bot, Update
from telegram.ext import Dispatcher
from openai import OpenAI

# ലോഗിംഗ് സജ്ജീകരണം
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# 1. Environment Variables-ൽ നിന്ന് കീകൾ എടുക്കുക
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# 2. പ്രധാന ഒബ്ജക്റ്റുകൾ ഉണ്ടാക്കുക
app = Flask(__name__)
client = OpenAI(api_key=OPENAI_API_KEY) # OpenAI ക്ലയിന്റ്
bot = Bot(token=TELEGRAM_TOKEN)          # ടെലിഗ്രാം ബോട്ട് ഒബ്‌ജക്റ്റ്

# 3. AI ലോജിക് ഫംഗ്ഷൻ
def get_ai_response(prompt):
    """ഒരു യൂസർ മെസ്സേജ് സ്വീകരിച്ച് OpenAI API-ലേക്ക് അയച്ച് മറുപടി നേടുന്നു."""
    try:
        response = client.chat.completions.create(
            # നിങ്ങളുടെ ഇഷ്ടമുള്ള മോഡൽ ഉപയോഗിക്കാം
            model="gpt-3.5-turbo", 
            messages=[
                {"role": "system", "content": "You are a helpful and friendly AI Telegram bot. Answer in a conversational style."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"AI API Error: {e}")
        return "Sorry, I ran into an error while processing your request."

# 4. വെബ്‌ഹുക്ക് റൂട്ട് - ഇവിടെയാണ് ടെലിഗ്രാമിൽ നിന്നുള്ള മെസ്സേജുകൾ വരുന്നത്
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == "POST":
        # JSON ഡാറ്റയിൽ നിന്ന് അപ്‌ഡേറ്റ് ഒബ്ജക്റ്റ് ഉണ്ടാക്കുക
        update = Update.de_json(request.get_json(force=True), bot)
        
        try:
            chat_id = update.message.chat.id
            text = update.message.text
            
            # AI പ്രതികരണം നേടുക
            ai_response = get_ai_response(text)
            
            # മറുപടി തിരികെ അയയ്ക്കുക
            bot.send_message(chat_id=chat_id, text=ai_response)
            
        except AttributeError:
            # message എന്ന കീ ഇല്ലാത്ത മറ്റ് അപ്‌ഡേറ്റുകൾ അവഗണിക്കുക
            pass

        # ടെലിഗ്രാമിന് 200 OK മറുപടി നൽകുക
    return "ok"

# 5. ഹോം റൂട്ട് (ആരോഗ്യ പരിശോധനയ്ക്കായി)
@app.route('/')
def index():
    return "Bot is running on Render!"

# # gunicorn ആണ് Render-ൽ സ്റ്റാർട്ട് ചെയ്യുന്നത്, ഈ ഭാഗം ലോക്കൽ ടെസ്റ്റിങ്ങിന് മാത്രം മതി.
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
