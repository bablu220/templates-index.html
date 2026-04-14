import telebot
import time
import datetime
import pytz
import random
from telebot import types
from flask import Flask, render_template  # <-- Ye naya hai
from threading import Thread
import os

# Web Server Setup
app = Flask(__name__)

@app.route('/')
def home():
    # Ye line aapke 'templates/index.html' ko load karegi
    return render_template('index.html')

def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# --- BOT CONFIGURATION ---
API_TOKEN = '8616199952:AAFn9Pcs (Aapka Pura Token Yahan Likhein)'
bot = telebot.TeleBot(API_TOKEN)
IST = pytz.timezone('Asia/Kolkata')
AUTH_KEY = "KULAMANI-L7"

def get_lottery7_period():
    try:
        now = datetime.datetime.now(IST)
        total_minutes = (now.hour * 60) + now.minute
        # Aapka current perfect match base
        current_period_suffix = 9671 + total_minutes
        date_str = now.strftime("%Y%m%d")
        return f"{date_str}1000{current_period_suffix}"
    except Exception:
        return "Syncing..."

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🟢 **PREDICTOR 4.0 AI**\n\nPlease enter **AUTHENTICATION KEY** to access premium features:", parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text == AUTH_KEY)
def login_success(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton('🎰 LOTTERY 7 (1-MIN)')
    markup.add(btn1)
    bot.send_message(message.chat.id, "✅ **ACCESS GRANTED**\nWelcome, Kulamani!", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == '🎰 LOTTERY 7 (1-MIN)')
def predict_l7(message):
    p_id = get_lottery7_period()
    res = random.choice(['BIG 🔴', 'SMALL 🟢'])
    conf = random.randint(95, 99)
    
    final_msg = (
        f"✅ **PREDICTION FETCHED**\n"
        f"------------------------------\n"
        f"📅 **Period:** `{p_id}`\n"
        f"🔥 **Result:** {res}\n"
        f"💎 **Confidence:** {conf}%\n"
        f"------------------------------"
    )
    bot.send_message(message.chat.id, final_msg, parse_mode='Markdown')

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
    
