import telebot
import config
import random
import masiv_filtr
from telebot import types

import sqlite3

# config
# внутри config.cfg -> TOKEN: ''
bot = telebot.TeleBot(config.Config('../config.cfg')['TOKEN'])

# добавлено для избавления дублирования
main_menu = "Выберите действие:"
media_menu = "Выберите тип медиа:"
misc_menu = "Выберите разное:"

back_button = "◀назад"

# подключение к базе
def connect_to_database():
    conn = sqlite3.connect('../sqlbase.db')
    return conn, conn.cursor()

def is_user_exists(user_id):
    conn, cursor = connect_to_database()
    cursor.execute("SELECT user_id FROM users WHERE user_id=?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def add_new_user(user_id):
    conn, cursor = connect_to_database()
    cursor.execute("INSERT INTO users (user_id, balance) VALUES (?, ?)", (user_id, 0))
    conn.commit()
    conn.close()

@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('фото/Hi.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)

    # добавляем пользователя
    user_id = message.from_user.id
    print(user_id)
    if not is_user_exists(user_id):
        add_new_user(user_id)

    # keyboard_клава_тоесть
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("🗃разное")
    item2 = types.KeyboardButton("🖼медия")
    # item3 = types.KeyboardButton("загадки")
    markup.add(item1, item2)

    bot.send_message(message.chat.id,"Добро пожаловать, {0.first_name}!"
                                     "\nЯ - <b>{1.first_name}</b>, бот созданный чтобы быть подопытным кроликом."
                     .format(message.from_user, bot.get_me()),parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def test(message):
    # переменные chat_id и text небыли использованы
    chat_id = message.chat.id
    text = message.text.lower()
    user_id = message.from_user.id

    if message.chat.type == 'private':
        # теперь не бесплатно
        if text == '🎲 рандомное число':
            current_balance = get_user_balance(user_id)
            
            if current_balance < 10:
                bot.send_message(chat_id, "У вас недостаточно средств для этой операции. Вам нужно 10 монет.")
            else:
                new_balance = current_balance - 10
                update_user_balance(user_id, new_balance)
                bot.send_message(chat_id, f"Баланс: {new_balance}")
                bot.send_message(chat_id, f" Выпало число: {str(random.randint(0, 100))}")

        elif text == '🤑 заработать денег':
            current_balance = get_user_balance(user_id)
            new_balance = current_balance + 1
            update_user_balance(user_id, new_balance)
            bot.send_message(chat_id, f"💰 Вы заработали 1 монету. Баланс: {new_balance}")
        
        elif text == '💼 мой баланс':
            current_balance = get_user_balance(user_id)
            bot.send_message(chat_id, f"💵 Баланс: {current_balance}")

        elif text == '😊 как дела?':
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Хорошо", callback_data='good')
            item2 = types.InlineKeyboardButton("Не очень", callback_data='bad')
            markup.add(item1, item2)
            bot.send_message(chat_id, 'Отлично, сам как?', reply_markup=markup)
        elif text == '🖼медия':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Хочу обои")
            item2 = types.KeyboardButton("Скинь гифку")
            item3 = types.KeyboardButton(back_button)
            markup.add(item1, item2, item3)
            bot.send_message(chat_id, media_menu, reply_markup=markup)
        elif text == '🗃разное':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("🎲 Рандомное число")
            item2 = types.KeyboardButton("😊 Как дела?")
            item3 = types.KeyboardButton("Расскажи о себе?")
            item4 = types.KeyboardButton("🤑 Заработать денег")
            item5 = types.KeyboardButton("💼 Мой баланс")
            item6 = types.KeyboardButton(back_button)
            markup.add(item1, item2, item3, item4, item5, item6)
            bot.send_message(chat_id, misc_menu, reply_markup=markup)
        elif text == 'расскажи о себе?':
            bot.send_message(chat_id, 'я бот созданый криворуким програмистом, сейчас умею отправлять стикер, гифку, фото\nТак же могу тебя послать')
        elif text == 'хочу обои':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Хочу крутые обои😎")
            item2 = types.KeyboardButton("Аниме")
            item3 = types.KeyboardButton(back_button)
            markup.add(item1, item2, item3)
            bot.send_message(chat_id, 'Аниме или крутые обои😎?', reply_markup=markup)
        elif text == 'хочу крутые обои😎':
            send_random_image(chat_id, masiv_filtr.oboi_gryt)
        elif text == 'аниме':
            send_random_image(chat_id, masiv_filtr.oboi_anime)
        elif text in ["привет"]:
            bot.send_message(chat_id, 'Привет')
            gif1 = open("гиф/AnimatedSticker5.tgs", 'rb')
            bot.send_sticker(chat_id, gif1)
        elif text in masiv_filtr.otvet:
            bot.send_message(chat_id, 'Вам пишет разработчик:\n"Зачем я научил бота посылать в ответ? ЗАЧЕМ?.."')
            foto1 = open("фото/ric.jpg", 'rb')
            bot.send_photo(chat_id, foto1)
        elif text in masiv_filtr.mat:
            bot.send_message(chat_id, 'Сам иди на хуй')
            gif2 = open("гиф/Sticker.tgs", 'rb')
            bot.send_sticker(chat_id, gif2)
        elif text == 'скинь гифку':
            bot.send_message(chat_id, 'держи')
            gif_path = send_random_image(chat_id, masiv_filtr.gif)
            bot.send_video(chat_id, open(gif_path, 'rb'))
        elif text == back_button:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("🗃разное")
            item2 = types.KeyboardButton("🖼медия")
            # item3 = types.KeyboardButton("загадки")
            markup.add(item1, item2)
            bot.send_message(chat_id, main_menu, reply_markup=markup)
        elif text in masiv_filtr.Vi:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("🗃разное")
            item2 = types.KeyboardButton("🖼медия")
            # item3 = types.KeyboardButton("загадки")
            markup.add(item1, item2)
            bot.send_message(chat_id, 'Я тут, что-то хотели?', reply_markup=markup)
        else:
            bot.send_message(chat_id, 'я не понимаю тебя')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, 'Вот и отличненько 😊')
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'Бывает 😢')

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="😊 Как дела?",
                                  reply_markup=None)
    except Exception as e:
        print(repr(e))

def send_random_image(chat_id, image_list):
    if image_list:
        bot.send_message(chat_id, 'держи 😎')
        img_path = random.choice(image_list)
        bot.send_photo(chat_id, photo=open(img_path, 'rb'))

def get_user_balance(user_id):
    conn, cursor = connect_to_database()
    cursor.execute("SELECT balance FROM users WHERE user_id=?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0

def update_user_balance(user_id, new_balance):
    conn, cursor = connect_to_database()
    cursor.execute("UPDATE users SET balance=? WHERE user_id=?", (new_balance, user_id))
    conn.commit()
    conn.close()

# RUN
bot.polling(none_stop=True)