import time
import telebot
from telebot import types
import os
import requests
from threading import Thread
BOT_TOKEN = '7716861627:AAG1w3LIIe8XsLUREkwWN8-AOr7BVQuo0PE'
bot = telebot.TeleBot(BOT_TOKEN)
CHANNEL_USERNAME = '@sayfullayev_bekzod_dev'

def is_subscribed(user_id):
    try:
        chat_member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        if chat_member.status in ['member', 'administrator', 'creator']:
            return True
        return False
    except Exception as e:
        return False


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if not is_subscribed(user_id):
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton("Kanalga o'tish", url="https://t.me/sayfullayev_bekzod_dev")
        markup.add(button1)
        bot.send_message(message.chat.id,"Iltimos, botdan foydalanish uchun kanalga obuna bo'ling!\n" "Obuna bo'lgach, yana botga qaytib kelishingizni so'raymiz.",reply_markup=markup)

        return
    add_user(user_id)
    # with open('audio.ogg', 'rb') as voice:
    #     bot.send_voice(message.chat.id, voice)
    username = message.from_user.username
    greeting = f"Salom, @{username}! Sizga qanday yordam bera olaman?" if username else "Salom! Sizga qanday yordam bera olaman?"

    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Portfolio", url="https://sayfullayev-bekzod.onrender.com/")
    button2 = types.InlineKeyboardButton("Kontakt", callback_data="contact")
    button3 = types.InlineKeyboardButton("Resume", callback_data="resume")
    button4 = types.InlineKeyboardButton("Buyurtma berish", callback_data="abs")
    button5 = types.InlineKeyboardButton("Ijtimoyi tarmoqlarimiz", callback_data="it")
    button6 = types.InlineKeyboardButton('Telefon raqam', callback_data="contact_user")
    # button7 = types.InlineKeyboardButton('Murojat yo\'llash', callback_data="feedback")
    markup.add(button1)
    markup.add(button2, button3)
    markup.add(button4)
    markup.add(button5, button6)
    # markup.add(button7)

    bot.send_message(message.chat.id, greeting, reply_markup=markup)

USERS_FILE = 'users.txt'

def add_user(user_id):
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w'): pass
    with open(USERS_FILE, 'r') as f:
        users = f.read().splitlines()
    if str(user_id) not in users:
        with open(USERS_FILE, 'a') as f:
            f.write(f"{user_id}\n")
def get_users_count():
    if not os.path.exists(USERS_FILE):
        return 0
    with open(USERS_FILE, 'r') as f:
        users = f.read().splitlines()
    return len(users)

@bot.message_handler(commands=['count'])
def count_users(message):
    count = get_users_count()
    bot.send_message(message.chat.id, f"Botdagi jami foydalanuvchilar soni: {count}")

@bot.message_handler(commands=['feedback'])
def handle_message(message):
    admin_chat_id = '1258119183'
    bot.send_message(admin_chat_id, f"Yangi xabar: {message.text}")

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "contact":
        bot.send_message(call.message.chat.id, "Biz bilan bog'lanish uchun:\n+998935940135")

    elif call.data == "abs":
        markup = types.InlineKeyboardMarkup()
        button_website = types.InlineKeyboardButton("Website buyurtma", callback_data="website")
        button_bot = types.InlineKeyboardButton("Telegram bot buyurtma", callback_data="bot")
        markup.add(button_website, button_bot)
        bot.send_message(call.message.chat.id, "Xizmatlarimizni tanlang:", reply_markup=markup)
    elif call.data == "it":
        instagram = 'www.instagram.com/_sayful1ayev_/'
        github = 'github.com/SayfullayevBekzod'
        telegram = 't.me/SayfullayevBekzod'
        social_links = f'Instagram: {instagram}\nGitHub: {github}\nTelegram: {telegram}'
        bot.send_message(call.message.chat.id, social_links)
    # elif call.data == 'feedback':
    #     admin_chat_id = '1258119183'
    #     bot.send_message(admin_chat_id, f"Yangi xabar: {call.message.text}")
    elif call.data == 'resume':
        pdf_path = 'Sayfullayevbekzod.pdf'
        try:
            with open(pdf_path, 'rb') as f:
                bot.send_document(call.message.chat.id, f)
        except FileNotFoundError:
            bot.send_message(call.message.chat.id, "Fayl topilmadi. Iltimos, fayl nomini tekshiring.")
    elif call.data == "website":
        bot.send_message(call.message.chat.id, "Qaysi turdagi website kerak?")
    elif call.data == "bot":
        bot.send_message(call.message.chat.id, "Qaysi turdagi telegram bot kerak?")
    elif call.data =='contact_user':
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        button = types.KeyboardButton("Telefon raqamni yuborish", request_contact=True)
        markup.add(button)
        bot.send_message(call.message.chat.id, "Iltimos, telefon raqamingizni yuboring o'zimiz aloqaga chiqamiz:", reply_markup=markup)
        time.sleep(7)
        bot.send_message(call.message.chat.id, 'Rahmat')
    bot.answer_callback_query(call.id)




# @bot.message_handler(commands=['pay'])
# def send_invoice(message):
#     prices = [types.LabeledPrice(label='Xizmat narxi', amount=5000000)]  # 50 000 so'm
#     bot.send_invoice(
#         message.chat.id, title='Xizmat to\'lovi', description='Xizmat uchun to\'lov',
#         provider_token='PROVIDER_TOKEN', currency='UZS', prices=prices,
#         start_parameter='payment-example', invoice_payload='bot-xizmat'
#     )


if __name__ == '__main__':
    print("Bot ishga tushdi...")
    while True:
        try:
            bot.polling(non_stop=True, timeout=60)
        except requests.exceptions.ReadTimeout:
            print("Timeout occurred. Retrying...")
            time.sleep(5)

Thread(target=start).start()