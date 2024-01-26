import telebot
import psycopg2
from telebot import types
from data_manager import TOKEN
from openai import OpenAI

client = OpenAI(api_key='')

bot = telebot.TeleBot(TOKEN)
gpt_chat_enabled = {}  # Используем словарь для хранения состояния чата

# Конфигурация подключения к базе данных
db_config = {
    "host": "localhost",
    "database": "bot_gpt",
    "user": "postgres",
    "password": "123"
}


def get_db_connection():
    conn = psycopg2.connect(**db_config)
    return conn


def user_exists(nickname_user):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE nickname_user = %s", (nickname_user,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user is not None


# Функция для добавления пользователя в БД
def add_user_to_db(name_user, nickname_user, id_chat):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name_user, nickname_user, id_chat) VALUES (%s, %s, %s)",
                   (name_user, nickname_user, id_chat))
    conn.commit()
    cursor.close()
    conn.close()


@bot.message_handler(commands=['start'])
def welcome(message):
    user = message.from_user
    hi = open('image/Hi.webp', 'rb')
    if user_exists(user.username):
        bot.send_sticker(message.chat.id, hi)
        bot.send_message(message.chat.id, "Рад снова вас видеть!", reply_markup=start_menu())
        print("новый пользователь", user.first_name, user.username, message.chat.id)
    else:
        bot.send_sticker(message.chat.id, hi)
        add_user_to_db(user.first_name, user.username, message.chat.id)
        bot.send_message(message.chat.id, "Рад видеть новое лицо!", reply_markup=start_menu())


# Функция для включения режима GPT чата
@bot.message_handler(commands=['gpt_chat'])
def enable_gpt_chat(message):
    chat_id = message.chat.id
    gpt_chat_enabled[chat_id] = True
    bot.send_message(chat_id, "Режим GPT чата включен.")


# Функция для отключения режима GPT чата
@bot.message_handler(commands=['back', 'stop'])
def disable_gpt_chat(message):
    chat_id = message.chat.id
    gpt_chat_enabled[chat_id] = False
    bot.send_message(chat_id, "Режим GPT чата отключен.")


# Функция для обработки входящих сообщений
@bot.message_handler(func=lambda message: True)
def gpt(message):
    chat_id = message.chat.id
    if gpt_chat_enabled.get(chat_id, False):
        prompt = message.text
        msg = bot.send_message(message.chat.id, 'Сообщение принято. Ждем ответа..')
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=[
                {"role": "system", "content": "Ты русский, научный помощник"},
                {"role": "user", "content": prompt}
            ]
        )
        gpt_text = response.choices[0].message.content
        tokens = response.usage.total_tokens
        bot.delete_message(message.chat.id, msg.message_id)
        bot.send_message(message.chat.id, gpt_text)
        bot.send_message(message.chat.id, f"потрачено следующее количество токенов: {tokens}")
        print('\nвопрос:', prompt)
        print('\nответ:', gpt_text)
        print('потрачено токенов:', tokens)
    else:
        bot.reply_to(message, "режим GPT отключен")


def start_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_chat_gpt = types.KeyboardButton("/gpt_chat")
    item2 = types.KeyboardButton("/start")
    item3 = types.KeyboardButton("расскажи анекдот про программиста")
    item5 = types.KeyboardButton("/stop")
    markup.add(item_chat_gpt, item2, item5, item3)
    return markup


if __name__ == "__main__":
    print('Запущен...')
    bot.polling(none_stop=True)
