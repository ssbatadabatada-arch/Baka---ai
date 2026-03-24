import telebot
import random
import google.generativeai as genai
from flask import Flask
import threading

# --- SETTINGS ---
token = "8629565949:AAH-3Q4K0Hl8LsViFqMt0xbsHeThGnCCUCM"
bot = telebot.TeleBot(token)

# Gemini AI Key & Safety Settings
genai.configure(api_key="AIzaSyDL53uOGG3trGSaIOx1Hlrup8c17vupsQI")

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

model = genai.GenerativeModel(
    model_name='gemini-pro',
    safety_settings=safety_settings
)

# Creator ID
CREATOR_ID = 6956842036
users_data = {}

# --- COMMANDS ---
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Kaise ho! Main hoon Baka AI. 🤖\nCommands: /work, /balance")

@bot.message_handler(commands=['work'])
def work(message):
    uid = message.from_user.id
    earn = random.randint(100, 1000)
    users_data[uid] = users_data.get(uid, 0) + earn
    bot.reply_to(message, f"💸 Tumne {earn} coins kamaye!")

@bot.message_handler(commands=['balance'])
def balance(message):
    bal = users_data.get(message.from_user.id, 0)
    if message.from_user.id == CREATOR_ID: bal = "Unlimited"
    bot.reply_to(message, f"💰 Balance: {bal} coins.")

# --- AI CHAT LOGIC ---
@bot.message_handler(func=lambda message: True, content_types=['text'])
def chat(message):
    # Sirf reply ya tag pe response dega (GC ke liye)
    is_tagged = f"@{bot.get_me().username}" in message.text
    is_reply_to_bot = message.reply_to_message and message.reply_to_message.from_user.id == bot.get_me().id
    
    if message.chat.type == 'private' or is_tagged or is_reply_to_bot:
        try:
            response = model.generate_content(message.text)
            bot.reply_to(message, response.text)
        except:
            bot.reply_to(message, "Dimaag thak gaya hai baka!")

# --- SERVER FOR RENDER ---
app = Flask('')
@app.route('/')
def home(): return "Baka is Online!"

def run(): app.run(host='0.0.0.0', port=8080)
threading.Thread(target=run).start()
bot.polling()


    
