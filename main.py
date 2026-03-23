import telebot
import random
import google.generativeai as genai
from flask import Flask
import threading

# --- SETTINGS ---
# Tamaro Bot Token
bot = telebot.TeleBot("8629565949:AAH-3Q4K0Hl8LsViFqMt0xbsHeThGnCCUCM")

# !!! AYA TAMARI GEMINI API KEY NAKHO !!!
genai.configure(api_key="TAME_MELVELI_GEMINI_KEY_AYA_PASTE_KARO")
model = genai.GenerativeModel('gemini-pro')

# Game Data (Simple dictionary)
users_data = {}

# --- GAME COMMANDS ---
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Kem cho baka! Hu tamaro AI dost chhu. 🤖\n\nCommands:\n/work - Paisa kamavo\n/rob - Chori karo\n/balance - Check karo\n\nMari sathe sacha dost ni jem vaat karo!")

@bot.message_handler(commands=['work'])
def work(message):
    uid = message.from_user.id
    earn = random.randint(100, 1000)
    users_data[uid] = users_data.get(uid, 0) + earn
    bot.reply_to(message, f"💸 Tame kaam karyu ane {earn} coins kamaya!")

@bot.message_handler(commands=['balance'])
def balance(message):
    bal = users_data.get(message.from_user.id, 0)
    bot.reply_to(message, f"💰 Tamara khata ma {bal} coins chhe.")

# --- AI CHAT LOGIC ---
@bot.message_handler(func=lambda message: True)
def chat(message):
    try:
        # AI Instructions: Fun, Gujarati-Hindi mix
        prompt = f"You are Baka AI. Talk like a close friend in a mix of Gujarati and Hindi. Be cool and funny. User said: {message.text}"
        response = model.generate_content(prompt)
        bot.reply_to(message, response.text)
    except:
        bot.reply_to(message, "Baka, brain thodu thaki gayu chhe, pachhi vaat kariye?")

# --- SERVER FOR RENDER ---
app = Flask('')
@app.route('/')
def home(): return "Baka AI is Live!"

def run(): app.run(host='0.0.0.0', port=8080)
threading.Thread(target=run).start()

bot.polling()
