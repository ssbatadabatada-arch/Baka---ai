import telebot
import random
import google.generativeai as genai
from flask import Flask
import threading
import time

# --- SETTINGS ---
token = "8629565949:AAH-3Q4K0Hl8LsViFqMt0xbsHeThGnCCUCM"
bot = telebot.TeleBot(token)

# Gemini AI Key (Fix kiya gaya bracket)
genai.configure(api_key="AIzaSyBXds0p_JEDrBImu1nfA_04Nx_8mF-368I")
model = genai.GenerativeModel('gemini-pro')

# Creator ID (Aapki ID)
CREATOR_ID = 6956842036

# Game Data
users_data = {}
users_health = {}
CREATOR_COINS = 999999999999 # Aapke liye unlimited!

# --- HELPERS ---
def get_balance(uid):
    if uid == CREATOR_ID: return CREATOR_COINS
    return users_data.get(uid, 0)

def set_balance(uid, amount):
    if uid != CREATOR_ID: users_data[uid] = amount

def get_name(user):
    if not user: return "Unknown"
    name = user.first_name
    if user.last_name: name += f" {user.last_name}"
    return name

# --- GAME COMMANDS ---
@bot.message_handler(commands=['start'])
def start(message):
    user_name = get_name(message.from_user)
    welcome_msg = (
        f"Kaise ho {user_name}! Main hoon tumhara AI dost, 'Baka'! 🤖\n\n"
        "**Features:**\n\n"
        "💰 **Economy:**\n"
        "/work - Paise kamao (kaam karke)\n"
        "/rob - Chori karo (group ke kisi member se)\n"
        "/kill - Dusre ko maaro aur uske paise lo (Risk hai!)\n"
        "/balance - Paise check karo\n\n"
        "🎭 **Fun:**\n"
        "/slap - Kisi ko thappad maaro\n"
        "/kiss - Kisi ko pappi do\n"
        "/hug - Kisi ko gale lagao\n\n"
        "Mujhse ek scche dost ki tarah Hindi mein baat karo! 🥳"
    )
    bot.reply_to(message, welcome_msg)

@bot.message_handler(commands=['work'])
def work(message):
    uid = message.from_user.id
    earn = random.randint(100, 1000)
    current_bal = get_balance(uid)
    new_bal = current_bal + earn
    set_balance(uid, new_bal)
    bot.reply_to(message, f"💸 Tumne mehnat karke {earn} coins kamaye! \nAb tumhare paas: {get_balance(uid)} coins hain.")

@bot.message_handler(commands=['balance'])
def balance(message):
    uid = message.from_user.id
    bal = get_balance(uid)
    bot.reply_to(message, f"💰 Tumhare khate mein {bal} coins hain.")

@bot.message_handler(commands=['rob'])
def rob(message):
    if not message.reply_to_message:
        return bot.reply_to(message, "⚠️ Baka! Kisi ke message par reply karke /rob use karo.")
    
    uid = message.from_user.id
    victim_id = message.reply_to_message.from_user.id
    
    if uid == victim_id: return bot.reply_to(message, "Ye kya! Apne aap ko thodi lootoge baka!")

    current_bal = get_balance(uid)
    victim_bal = get_balance(victim_id)

    if victim_bal < 10: return bot.reply_to(message, "Gareeb ki chori nahi karte!")

    success = random.choice([True, False])
    if success:
        steal_pct = random.randint(10, 50)
        steal_amt = int(victim_bal * (steal_pct / 100))
        set_balance(uid, current_bal + steal_amt)
        set_balance(victim_id, victim_bal - steal_amt)
        bot.reply_to(message, f"🎉 *Super*! Tumne chori kar li aur {steal_amt} coins loot liye!")
    else:
        loss_pct = random.randint(10, 20)
        loss_amt = int(current_bal * (loss_pct / 100))
        set_balance(uid, max(0, current_bal - loss_amt))
        bot.reply_to(message, f"😿 *Bad Luck*! Tum pakde gaye aur jurmane mein {loss_amt} coins gawa diye.")

@bot.message_handler(commands=['kill'])
def kill(message):
    if not message.reply_to_message:
        return bot.reply_to(message, "⚠️ Baka! Kisi ke message par reply karke /kill use karo.")
    
    uid = message.from_user.id
    victim_id = message.reply_to_message.from_user.id
    
    if uid == victim_id: return bot.reply_to(message, "Khud ko kyu maar rahe ho baka!")

    current_bal = get_balance(uid)
    victim_bal = get_balance(victim_id)

    success = (random.randint(1, 10) == 1) # 10% Chance

    if success:
        total_coins = victim_bal
        set_balance(uid, current_bal + total_coins)
        set_balance(victim_id, 0)
        bot.reply_to(message, f"💀 **Khatam!** Tumne use dher kar diya aur uske saare {total_coins} coins loot liye!")
    else:
        my_loss = current_bal
        set_balance(uid, 0)
        bot.reply_to(message, f"🩸 *Oh no!* Tum khud maare gaye aur apne saare {my_loss} coins gawa diye.")

# --- FUN COMMANDS ---
@bot.message_handler(commands=['slap'])
def slap(message):
    if not message.reply_to_message: return bot.reply_to(message, "Kisi ko thappad maarne ke liye reply karein.")
    user = get_name(message.from_user)
    victim = get_name(message.reply_to_message.from_user)
    bot.reply_to(message, f"👋 {user} ne {victim} ko ek zor daar *THAPPAD* maara!")

@bot.message_handler(commands=['kiss'])
def kiss(message):
    if not message.reply_to_message: return bot.reply_to(message, "Pappi dene ke liye reply karein.")
    user = get_name(message.from_user)
    victim = get_name(message.reply_to_message.from_user)
    bot.reply_to(message, f"💋 {user} ne {victim} ko ek pyaari si *Pappi* di!")

@bot.message_handler(commands=['hug'])
def hug(message):
    if not message.reply_to_message: return bot.reply_to(message, "Gale lagne ke liye reply karein.")
    user = get_name(message.from_user)
    victim = get_name(message.reply_to_message.from_user)
    bot.reply_to(message, f"🤗 {user} ne {victim} ko zor se *HUG* kiya!")

# --- AI CHAT LOGIC (Hindi) ---
@bot.message_handler(func=lambda message: True)
def chat(message):
    try:
        # AI Instructions in Hindi
        prompt = f"Tum Baka AI ho. Ek mazedaar dost ki tarah Hindi mein baat karo. User ne kaha: {message.text}"
        response = model.generate_content(prompt)
        bot.reply_to(message, response.text)
    except:
        bot.reply_to(message, "Baka, dimaag thoda thak gaya hai, baad mein baat karein?")

# --- RENDER SERVER ---
app = Flask('')
@app.route('/')
def home(): return "Baka AI Bot is Online!"

def run(): app.run(host='0.0.0.0', port=8080)
threading.Thread(target=run).start()

bot.polling()

    
