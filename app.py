import os
import logging
from flask import Flask, request, jsonify
from telegram import Bot, Update
from openai import OpenAI

# ലോഗിംഗ് സജ്ജീകരണം (പിശകുകൾ പരിശോധിക്കാൻ ഇത് സഹായിക്കും)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# ==============================================================================
# 1. കീകൾ എടുക്കുന്നു
# ==============================================================================
# Render-ൽ നിങ്ങൾ സജ്ജമാക്കിയ Environment Variables-ൽ നിന്ന് കീകൾ എടുക്കുന്നു
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# ==============================================================================
# 2. പ്രധാന ഒബ്ജക്റ്റുകൾ
# ==============================================================================
app = Flask(__name__)  # Flask ആപ്ലിക്കേഷൻ ഒബ്ജക്റ്റ് (ഇതാണ് Procfile-ൽ app:app എന്ന് കൊടുക്കുന്നത്)
client = OpenAI(api_key=OPENAI_API_KEY) 
bot = Bot(token=TELEGRAM_TOKEN)          

# ==============================================================================
# 3. AI ലോജിക് ഫംഗ്ഷൻ
# ==============================================================================
def get_ai_response(prompt):
    """ഒരു യൂസർ മെസ്സേജ് സ്വീകരിച്ച് OpenAI API-ലേക്ക് അയച്ച് മറുപടി നേടുന്നു."""
    try:
        response = client.chat.completions.create(
            # നിങ്ങളുടെ ഇഷ്ടമുള്ള മോഡൽ ഉപയോഗിക്കാം
            model="gpt-3.5-turbo", 
            messages=[
                {"role": "system", "content": "You are a helpful and friendly AI Telegram bot. Answer briefly and directly in a conversational style."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"AI API Error: {e}")
        return "I apologize, but I encountered an error while contacting the AI service."

# ==============================================================================
# 4. വെബ്‌ഹുക്ക് റൂട്ട് (POST റിക്വസ്റ്റുകൾ ഇവിടെ സ്വീകരിക്കുന്നു)
# ==============================================================================
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == "POST":
        
        try:
            # JSON ഡാറ്റയിൽ നിന്ന് ടെലിഗ്രാം അപ്‌ഡേറ്റ് ഉണ്ടാക്കുന്നു
            update = Update.de_json(request.get_json(force=True), bot)
            
            # മെസ്സേജ് അപ്‌ഡേറ്റ് ആണെങ്കിൽ മാത്രം പ്രതികരിക്കുന്നു
            if update.message and update.message.text:
                chat_id = update.message.chat.id
                text = update.message.text
                
                # AI പ്രതികരണം നേടുക
                ai_response = get_ai_response(text)
                
                # മറുപടി തിരികെ അയയ്ക്കുക
                bot.send_message(chat_id=chat_id, text=ai_response)
            
        except Exception as e:
            # പിശകുകൾ വന്നാൽ ലോഗിൽ രേഖപ്പെടുത്തും
            logging.error(f"Error processing update: {e}")
            pass

        # ടെലിഗ്രാമിന് 200 OK മറുപടി നൽകുന്നു
    return "ok"

# ==============================================================================
# 5. ഹോം റൂട്ട് (ആരോഗ്യ പരിശോധനയ്ക്കായി)
# ==============================================================================
@app.route('/')
def index():
    return "Bot is running on Render! (Health check passed)"
