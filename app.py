import os
import logging
from flask import Flask, request
from telegram import Bot, Update
import requests # <-- പുതിയ ലൈബ്രറി

# ==============================================================================
# ലോഗിംഗ് സജ്ജീകരണം
# ==============================================================================
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# ==============================================================================
# 1. കീകൾ എടുക്കുന്നു
# ==============================================================================
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
# Render-ൽ നിങ്ങൾ സജ്ജമാക്കിയ പുതിയ കീ
HUGGINGFACE_TOKEN = os.environ.get("HUGGINGFACE_TOKEN") 

# ==============================================================================
# 2. Hugging Face മോഡൽ സെറ്റ് ചെയ്യുക (ഇത് നിങ്ങൾ മാറ്റണം)
# ==============================================================================
# ശ്രദ്ധിക്കുക: <MODEL_ID> എന്നതിന് പകരം നിങ്ങൾ ഇഷ്ടപ്പെടുന്ന ഒരു LLM-ൻ്റെ ID നൽകണം.
# ഉദാഹരണത്തിന്: 'google/flan-t5-large' അല്ലെങ്കിൽ 'mistralai/Mistral-7B-Instruct-v0.2'
MODEL_ID = "gpt2" # <-- പരീക്ഷണത്തിനായി gpt2 എന്ന ലളിതമായ മോഡൽ നൽകുന്നു. നിങ്ങൾക്ക് ഇഷ്ടമുള്ളത് മാറ്റാം.

API_URL = f"https://router.huggingface.co/hf-inference/{MODEL_ID}" 
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_TOKEN}"}

# ==============================================================================
# 3. പ്രധാന ഒബ്ജക്റ്റുകൾ
# ==============================================================================
app = Flask(__name__)
bot = Bot(token=TELEGRAM_TOKEN)          

# ==============================================================================
# 4. AI ലോജിക് ഫംഗ്ഷൻ (Hugging Face ഉപയോഗിച്ച്)
# ==============================================================================
def get_ai_response(prompt):
    """യൂസർ മെസ്സേജ് Hugging Face Inference API-ലേക്ക് അയച്ച് മറുപടി നേടുന്നു."""
    
    try:
        # ഒരു കഥാപാത്രത്തിൻ്റെ മറുപടി ലഭിക്കാൻ prompt-ൽ സിസ്റ്റം നിർദ്ദേശം ചേർക്കുന്നു
        full_prompt = f"You are a helpful and friendly AI character. Respond to this message briefly: {prompt}"
        
        payload = {
            "inputs": full_prompt,
            "parameters": {
                "max_new_tokens": 100, 
                "temperature": 0.7, 
                "return_full_text": False
            }
        }
        
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        
        if response.status_code != 200:
            # API-യിൽ പിശക് വന്നാൽ (ഉദാ: ടോക്കൺ തെറ്റ്, മോഡൽ ലഭ്യമല്ല)
            logging.error(f"Hugging Face API Error: Status {response.status_code}, Response: {response.text}")
            return f"Hugging Face Error (Status: {response.status_code}). Check your HUGGINGFACE_TOKEN or MODEL_ID."
        
        data = response.json()
        
        # ജനറേറ്റ് ചെയ്ത ടെക്സ്റ്റ് extract ചെയ്യുക
        if data and isinstance(data, list) and 'generated_text' in data[0]:
            return data[0]['generated_text'].strip()
        else:
            logging.error(f"AI response format error: {data}")
            return "AI response format error."

    except Exception as e:
        logging.error(f"Hugging Face API Exception: {e}")
        return "I apologize, but I encountered a network error while contacting the AI service."

# ==============================================================================
# 5. വെബ്‌ഹുക്ക് റൂട്ട് (POST റിക്വസ്റ്റുകൾ ഇവിടെ സ്വീകരിക്കുന്നു)
# ==============================================================================
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == "POST":
        try:
            update = Update.de_json(request.get_json(force=True), bot)
            
            if update.message and update.message.text:
                chat_id = update.message.chat.id
                text = update.message.text
                
                ai_response = get_ai_response(text)
                bot.send_message(chat_id=chat_id, text=ai_response)
            
        except Exception as e:
            logging.error(f"Error processing update: {e}")
            pass

    return "ok"

# ==============================================================================
# 6. ഹോം റൂട്ട്
# ==============================================================================
@app.route('/')
def index():
    return "Telegram bot is running on Hugging Face API!"
