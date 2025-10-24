import os
import logging
from flask import Flask, request
from telegram import Bot, Update
# Google Gemini API ലൈബ്രറി
from google import genai
from google.genai.errors import APIError

# ==============================================================================
# ലോഗിംഗ് സജ്ജീകരണം
# ==============================================================================
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# ==============================================================================
# 1. കീകൾ എടുക്കുന്നു
# ==============================================================================
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
# Render-ൽ സജ്ജമാക്കിയ Gemini കീ എടുക്കുന്നു
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY") 

# ==============================================================================
# 2. പ്രധാന ഒബ്ജക്റ്റുകൾ
# ==============================================================================
app = Flask(__name__)
bot = Bot(token=TELEGRAM_TOKEN)  
# Gemini ക്ലയിൻ്റ് സജ്ജമാക്കുന്നു (കീ നേരിട്ട് Environment Variable-ൽ നിന്ന് വായിക്കും)
try:
    gemini_client = genai.Client(api_key=GEMINI_API_KEY)
except Exception as e:
    logging.error(f"Gemini Client Initialization Error: {e}")

# ==============================================================================
# 3. AI ലോജിക് ഫംഗ്ഷൻ (Gemini ഉപയോഗിച്ച്)
# ==============================================================================
def # app.py-യിലെ get_ai_response ഫംഗ്ഷൻ മാത്രം മാറ്റി ഈ കോഡ് ചേർക്കുക:

def get_ai_response(prompt):
    """യൂസർ മെസ്സേജ് Gemini API-ലേക്ക് അയച്ച് മറുപടി നേടുന്നു."""
    try:
        # Gemini-യുടെ response-ൽ സുരക്ഷാ പിശകുകൾ ഉണ്ടെങ്കിൽ അത് text നൽകില്ല.
        response = gemini_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                "You are a helpful and friendly AI Telegram character. Respond briefly and engagingly to the user's message.",
                prompt
            ]
        )
        
        # ഇവിടെയാണ് പുതിയ സുരക്ഷാ പരിശോധന (New Safety Check)
        if response.text:
            # മറുപടിയിൽ ടെക്സ്റ്റ് ഉണ്ടെങ്കിൽ മാത്രം strip ചെയ്ത് നൽകുന്നു
            return response.text.strip()
        else:
            # ടെക്സ്റ്റ് ഇല്ലെങ്കിൽ ഒരു പിശക് സന്ദേശം നൽകുന്നു
            logging.warning("Gemini returned an empty response or was blocked by a safety filter.")
            return "ക്ഷമിക്കണം, നിങ്ങളുടെ ചോദ്യത്തിന് മറുപടി ലഭ്യമല്ല. ദയവായി ചോദ്യം ലളിതമാക്കാമോ?"

    except APIError as e:
        logging.error(f"Gemini API Error: {e}")
        return f"Gemini API Error: Please check your API Key and usage limits."
    except Exception as e:
        logging.error(f"General AI Exception: {e}")
        return "I apologize, but I encountered a general error."


# ==============================================================================
# 4. വെബ്‌ഹുക്ക് റൂട്ട് (ബാക്കിയെല്ലാം മാറ്റമില്ല)
# ==============================================================================
# app.py, ഈ ഭാഗം മാത്രം മാറ്റി എഴുതുക (ഏകദേശം line 71 മുതൽ)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == "POST":
        try:
            update = Update.de_json(request.get_json(force=True), bot)
            
            if update.message and update.message.text:
                chat_id = update.message.chat.id
                text = update.message.text
                
                # 1. AI പ്രതികരണം നേടുന്നു
                ai_response = get_ai_response(text)
                
                # 2. ടെലിഗ്രാമിലേക്ക് മറുപടി അയക്കുന്നു
                try:
                    bot.send_message(chat_id=chat_id, text=ai_response)
                    logging.info(f"Successfully sent message to chat_id: {chat_id}") # വിജയം ലോഗ് ചെയ്യുന്നു
                except Exception as send_error:
                    logging.error(f"TELEGRAM SEND FAILED: {send_error}") # പരാജയം പ്രത്യേകം ലോഗ് ചെയ്യുന്നു
            
        except Exception as e:
            logging.error(f"Error processing update (General): {e}")
            pass
            
    return "ok"


# ==============================================================================
# 5. ഹോം റൂട്ട്
# ==============================================================================
@app.route('/')
def index():
    return "Telegram bot is running on Gemini API!"
