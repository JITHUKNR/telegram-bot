import os
import logging
from flask import Flask, request
from telegram import Bot, Update
from google import genai
from google.genai.errors import APIError

# ==============================================================================
# Logging setup
# ==============================================================================
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ==============================================================================
# 1. Environment variables
# ==============================================================================
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# ==============================================================================
# 2. Main objects
# ==============================================================================
app = Flask(__name__)
bot = Bot(token=TELEGRAM_TOKEN)

try:
    gemini_client = genai.Client(api_key=GEMINI_API_KEY)
except Exception as e:
    logging.error(f"Gemini Client Initialization Error: {e}")

# ==============================================================================
# 3. Gemini AI Function
# ==============================================================================
def get_ai_response(prompt):
    try:
        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                "You are a friendly Telegram chatbot. Respond briefly and helpfully.",
                prompt
            ]
        )

        if hasattr(response, 'text') and response.text:
            return response.text.strip()
        else:
            logging.warning("Gemini returned empty response or blocked.")
            return "ക്ഷമിക്കണം, മറുപടി ലഭിച്ചില്ല. ദയവായി ചോദ്യം ലളിതമാക്കൂ."
    except APIError as e:
        logging.error(f"Gemini API Error: {e}")
        return "Gemini API Error: Check your API key or usage."
    except Exception as e:
        logging.error(f"General AI Exception: {e}")
        return "സർവർ താൽക്കാലികമായി busy ആണ്. ദയവായി വീണ്ടും ശ്രമിക്കുക."

# ==============================================================================
# 4. Webhook Route
# ==============================================================================
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json(force=True)
        logging.info(f"Incoming update: {data}")  # ✅ Debug log

        update = Update.de_json(data, bot)

        if update.message and update.message.text:
            chat_id = update.message.chat.id
            text = update.message.text.strip()

            ai_response = get_ai_response(text)

            try:
                bot.send_message(chat_id=chat_id, text=ai_response)
                logging.info(f"✅ Sent message to chat_id: {chat_id}")
            except Exception as send_error:
                logging.error(f"❌ TELEGRAM SEND FAILED: {send_error}")
        else:
            logging.warning("No text message found in update.")
    except Exception as e:
        logging.error(f"Webhook Error: {e}")

    return "ok", 200

# ==============================================================================
# 5. Test Route
# ==============================================================================
@app.route('/')
def index():
    return "✅ Telegram bot is running with Gemini API!"

# ==============================================================================
# 6. Run (Render requirement)
# ==============================================================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
