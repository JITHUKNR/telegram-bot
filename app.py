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
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")  # Render-ൽ സജ്ജമാക്കിയ കീ

# ==============================================================================
# 2. പ്രധാന ഒബ്ജക്റ്റുകൾ
# ==============================================================================
app = Flask(__name__)
bot = Bot(token=TELEGRAM_TOKEN)

# Gemini ക്ലയന്റ് സജ്ജമാക്കുന്നു
try:
    gemini_client = genai.Client(api_key=GEMINI_API_KEY)
except Exception as e:
    logging.error(f"Gemini Client Initialization Error: {e}")

# ==============================================================================
# 3. AI ലോജിക് ഫംഗ്ഷൻ
# ==============================================================================
def get_ai_response(prompt):
    """യൂസർ മെസ്സേജ് Gemini API-ലേക്ക് അയച്ച് മറുപടി നേടുന്നു."""
    try:
        response = gemini_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                "You are a helpful and friendly AI Telegram character. Respond briefly and engagingly to the user's message.",
                prompt
            ]
        )

        if response.text:
            return response.text.strip()
        else:
            logging.warning("Gemini returned an empty response or was blocked by a safety filter.")
            return "ക്ഷമിക്കണം, മറുപടി ലഭ്യമല്ല. ദയവായി ചോദ്യം ലളിതമാക്കാമോ?"

    except APIError as e:
        logging.error(f"Gemini API Error: {e}")
        return "Gemini API Error: നിങ്ങളുടെ API Key അല്ലെങ്കിൽ usage പരിശോധിക്കുക."
    except Exception as e:
        logging.error(f"General AI Exception: {e}")
        return "എന്തോ പിശക് സംഭവിച്ചു 😅. കുറച്ച് കഴിഞ്ഞ് വീണ്ടും ശ്രമിക്കൂ."


# ==============================================================================
# 4. വെബ്‌ഹുക്ക് റൂട്ട്
# ==============================================================================
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

                # 🔹 Debug print — Render logs-ൽ കാണാം
                print(f"User said: {text} | Gemini replied: {ai_response}")

                # 2. ടെലിഗ്രാമിലേക്ക് മറുപടി അയക്കുന്നു
                try:
                    bot.send_message(chat_id=chat_id, text=ai_response)
                    logging.info(f"✅ Successfully sent message to chat_id: {chat_id}")
                except Exception as send_error:
                    logging.error(f"🚫 TELEGRAM SEND FAILED: {send_error}")
            
        except Exception as e:
            logging.error(f"Error processing update (General): {e}")
            
    return "ok"

# ==============================================================================
# 5. ഹോം റൂട്ട്
# ==============================================================================
@app.route('/')
def index():
    return "🚀 Telegram bot is running on Gemini API!"


# ==============================================================================
# 6. Render-ൽ Gunicorn വഴി ഓടും
# ==============================================================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
