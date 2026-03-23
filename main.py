import telebot
import random
import google.generativeai as genai
from flask import Flask
import threading
import time

# --- SETTINGS ---
token = "8629565949:AAH-3Q4K0Hl8LsViFqMt0xbsHeThGnCCUCM"
bot = telebot.TeleBot(token)

# Gemini AI Key aya nakho (Google AI Studio mathi malse)
genai.configure(api_key="AIzaSyBXds0p_JEDrBImu1nfA_04Nx...")")
model = genai.GenerativeModel('gemini-pro')

# *** AYA TAMARI TELEGRAM ID NAKHO *** (e.g., 12345678)
# Tame unlimited coins mate
CREATOR_ID = 6956842036

# Game Data
users_data = {}
users_health = {}
CREATOR_COINS = 999999999999 # Unlimited for you!

# --- HELPERS ---
def get_balance(uid):
    if uid == CREATOR_ID: return CREATOR_COINS
    return users_data.get(uid, 0)

def set_balance(uid, amount):
    if uid != CREATOR_ID: users_data[uid] = amount

def get_health(uid): return users_health.get(uid, 100)

def set_health(uid, hp): users_health[uid] = max(0, min(100, hp))

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
        f"Kem cho {user_name}! Hu tamaro AI dost, 'Baka'! 🤖\n\n"
        "**Features:**\n\n"
        "💰 **Economy:**\n"
        "/work - Paisa kamavo (work kari ne)\n"
        "/rob - Chori karo (group na user mathi)\n"
        "/kill - Bija ne maren emna badha paisa lo (Risk hoy!)\n"
        "/balance - Check karo\n\n"
        "🎭 **Fun:**\n"
        "/slap - Koik ne thappad maro\n"
        "/kiss - Koik ne chumban dyo\n"
        "/hug - Koik ne hug karo\n\n"
        "Mari sathe sacha dosti jem vaat karo! 🥳"
    )
    bot.reply_to(message, welcome_msg)

@bot.message_handler(commands=['work'])
def work(message):
    uid = message.from_user.id
    earn = random.randint(100, 1000)
    current_bal = get_balance(uid)
    new_bal = current_bal + earn
    set_balance(uid, new_bal)
    bot.reply_to(message, f"💸 Tame majuri kari ne {earn} coins kamaya! \nHave tamari pase: {get_balance(uid)}")

@bot.message_handler(commands=['balance'])
def balance(message):
    uid = message.from_user.id
    bal = get_balance(uid)
    bot.reply_to(message, f"💰 Tamara khata ma {bal} coins chhe.")

@bot.message_handler(commands=['rob'])
def rob(message):
    if not message.reply_to_message:
        return bot.reply_to(message, "⚠️ Baka! Koina text par reply kari ne /rob use karo.")
    
    uid = message.from_user.id
    victim_id = message.reply_to_message.from_user.id
    
    if uid == victim_id: return bot.reply_to(message, "Aa su! Potane rob na karay baka!")

    current_bal = get_balance(uid)
    victim_bal = get_balance(victim_id)

    if victim_bal < 10: return bot.reply_to(message, "Gareeb pase thi chori na karay!")

    success = random.choice([True, False])
    if success:
        steal_pct = random.randint(10, 50)
        steal_amt = int(victim_bal * (steal_pct / 100))
        set_balance(uid, current_bal + steal_amt)
        set_balance(victim_id, victim_bal - steal_amt)
        bot.reply_to(message, f"🎉 *Suuper*! Tame chori ma jitya ane {steal_amt} coins luti lidha!")
    else:
        loss_pct = random.randint(10, 20)
        loss_amt = int(current_bal * (loss_pct / 100))
        set_balance(uid, max(0, current_bal - loss_amt))
        bot.reply_to(message, f"😿 *Bad Luck*! Tame paka thaya ane reverse ma {loss_amt} coins haraai dyo.")

@bot.message_handler(commands=['kill'])
def kill(message):
    if not message.reply_to_message:
        return bot.reply_to(message, "⚠️ Baka! Koina text par reply kari ne /kill use karo.")
    
    uid = message.from_user.id
    victim_id = message.reply_to_message.from_user.id
    
    if uid == victim_id: return bot.reply_to(message, "Aa su! Potane marna na hoy!")

    current_bal = get_balance(uid)
    victim_bal = get_balance(victim_id)

    # 10% chance to kill successfully
    success = (random.randint(1, 10) == 1)

    if success:
        total_coins = victim_bal
        set_balance(uid, current_bal + total_coins)
        set_balance(victim_id, 0)
        bot.reply_to(message, f"💀 **BOOM!** Tame tene mari nakhyu ane emna badha {total_coins} coins luti lidha!")
    else:
        # Reverse Kill Risk
        my_loss = current_bal
        set_balance(uid, 0)
        bot.reply_to(message, f"🩸 *Risk*! Tame mare gaya ane reverse ma tamara badha {my_loss} coins haraai dyo.")

# --- FUN COMMANDS ---
@bot.message_handler(commands=['slap'])
def slap(message):
    if not message.reply_to_message: return bot.reply_to(message, "Koik ne slap marva reply karo.")
    user = get_name(message.from_user)
    victim = get_name(message.reply_to_message.from_user)
    bot.reply_to(message, f"👋 {user} e {victim} ne zor thi *THAPPAD* mari!")

@bot.message_handler(commands=['kiss'])
def kiss(message):
    if not message.reply_to_message: return bot.reply_to(message, "Koik ne chumban dyava reply karo.")
    user = get_name(message.from_user)
    victim = get_name(message.reply_to_message.from_user)
    bot.reply_to(message, f"💋 {user} e {victim} ne ek pyari jivi *CHUMBAN* didhi!")

@bot.message_handler(commands=['hug'])
def hug(message):
    if not message.reply_to_message: return bot.reply_to(message, "Koik ne 'hug' karva reply karo.")
    user = get_name(message.from_user)
    victim = get_name(message.reply_to_message.from_user)
    bot.reply_to(message, f"🤗 {user} e {victim} ne ek zor thi *HUG* kari!")

# --- AI CHAT LOGIC (Always last) ---
@bot.message_handler(func=lambda message: True)
def chat(message):
    try:
        # AI Instructions: Fun, Gujarati-Hindi mix
        prompt = f"You are Baka AI. Talk like a close friend in a mix of Gujarati and Hindi. Be cool and funny. User said: {message.text}"
        response = model.generate_content(prompt)
        bot.reply_to(message, response.text)
    except:
        bot.reply_to(message, "Baka, brain thodu thaki gayu chhe, pachhi vaat kariye?")

# --- RENDER SERVER ---
app = Flask('')
@app.route('/')
def home(): return "Baka AI Game Bot is Live!"

def run(): app.run(host='0.0.0.0', port=8080)
threading.Thread(target=run).start()

bot.polling()
    
