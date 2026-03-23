import telebot
import random
import google.generativeai as genai
from flask import Flask
import threading
import time

# --- SETTINGS ---
token = "8629565949:AAH-3Q4K0Hl8LsViFqMt0xbsHeThGnCCUCM"
bot = telebot.TeleBot(token)

# Gemini AI Key
genai.configure(api_key="AIzaSyBXds0p_JEDrBImu1nfA_04Nx_8mF-368I")
model = genai.GenerativeModel('gemini-pro')

# Creator ID
CREATOR_ID = 6956842036

# Game Data
users_data = {}
CREATOR_COINS = 999999999999

# --- HELPERS ---
def get_balance(uid):
    if uid == CREATOR_ID: return CREATOR_COINS
    return users_data.get(uid, 0)

def set_balance(uid, amount):
    if uid != CREATOR_ID: users_data[uid] = amount

def get_name(user):
    return user.first_name if user else "Dost"

# --- COMMANDS ---
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, f"Kaise ho {get_name(message.from_user)}! Main hoon Baka AI. 🤖\n\nCommands: /work, /rob, /kill, /balance")

@bot.message_handler(commands=['work'])
def work(message):
    uid = message.from_user.id
    earn = random.randint(100, 1000)
    set_balance(uid, get_balance(uid) + earn)
    bot.reply_to(message, f"💸 Tumne {earn} coins kamaye!")

@bot.message_handler(commands=['balance'])
def balance(message):
    bot.reply_to(message, f"💰 Balance: {get_balance(message.from_user.id)} coins.")

# --- AI CHAT (Only when Tagged or Replied) ---
@bot.message_handler(func=lambda message: True, content_types=['text'])
def chat(message):
    # Sirf tab reply dega jab koi bot ko tag kare ya reply kare
    is_tagged = f"@{bot.get_me().username}" in message.text
    is_reply_to_bot = message.reply_to_message and message.reply_to_message.from_user.id == bot.get_me().id
    
    if message.chat.type == 'private' or is_tagged or is_reply_to_bot:
        try:
            prompt = f"Tum Baka AI ho. Hindi mein mazaakiya dost ki tarah reply do: {message.text}"
            response = model.generate_content(prompt)
            bot.reply_to(message, response.text)
        except:
            bot.reply_to(message, "Dimaag thak gaya hai baka!")

# --- SERVER ---
app = Flask('')
@app.route('/')
def home(): return "Baka Live!"

def run(): app.run(host='0.0.0.0', port=8080)
threading.Thread(target=run).start()
bot.polling()


    
