import telebot
import apsw
import threading
from telebot import types
from data_manager import TOKEN
from openai import OpenAI

client = OpenAI(api_key='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')

bot = telebot.TeleBot(TOKEN)
gpt_chat_enabled = False

# Создание и подключение к базе данных SQLite с использованием apsw
conn = apsw.Connection("gpt_chat.db")
cursor_lock = threading.Lock()


@bot.message_handler(commands=['start'])
def welcome(message):
    hi = open('image/Hi.webp', 'rb')
    bot.send_sticker(message.chat.id, hi)
    bot.send_message(message.chat.id, 'Привет, я ChatGPT s telegram.', reply_markup=start_menu(), )


# Функция для включения режима GPT чата
@bot.message_handler(commands=['gpt_chat'])
def enable_gpt_chat(message):
    # Включение режима GPT чата для текущего пользователя
    user_id = message.from_user.id
    with cursor_lock:
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET gpt_chat_enabled = 1 WHERE user_id = ?', (user_id,))
        conn.commit()
    bot.send_message(message.chat.id, "Режим GPT чата включен. Отправьте мне сообщение для начала чата.")


# Функция для отключения режима GPT чата
@bot.message_handler(commands=['back', 'stop'])
def disable_gpt_chat(message):
    # Отключение режима GPT чата для текущего пользователя
    user_id = message.from_user.id
    with cursor_lock:
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET gpt_chat_enabled = 0 WHERE user_id = ?', (user_id,))
        conn.commit()
    bot.send_message(message.chat.id, "Режим GPT чата отключен.")


# Функция для обработки входящих сообщений
@bot.message_handler(func=lambda message: True)
def gpt(message):
    # Получение состояния режима GPT чата для текущего пользователя
    user_id = message.from_user.id
    with cursor_lock:
        cursor = conn.cursor()
        cursor.execute('SELECT gpt_chat_enabled FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if result is not None:
            gpt_chat_enabled = result[0]
            print(f"User {user_id}, GPT chat enabled: {gpt_chat_enabled}")
        else:
            print(f"User {user_id} not found in the database.")
            gpt_chat_enabled = 0

    if gpt_chat_enabled:
        # получаем вопрос от пользователя
        prompt = message.text
        msg = bot.send_message(message.chat.id, 'Сообщение принято. Ждем ответа..')
        # prompt = str(input())  водим ответ в консоле
        # gpt-4, gpt-4 turbo попробовать новую модель позже
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=[
                {"role": "system", "content": "Ты русский, научный помощник"},
                {"role": "user", "content": prompt}
            ]
        )
        # gpt_text=str(response)
        gpt_text2 = response.choices[0].message.content
        tokens = response.usage.total_tokens
        # удаление сообщение
        # bot.edit_message_text("...", chat_id=message.chat.id, message_id=msg.message_id)
        bot.delete_message(message.chat.id, msg.message_id)
        #  ответ пишет пользователю
        bot.send_message(message.chat.id, gpt_text2)
        bot.send_message(message.chat.id, f"потрачено следующее количество токенов: {tokens}")
        # ответ в консоле
        print('\nвопрос:', prompt)
        print('\nответ:', gpt_text2)
        print('потрачено токенов:', tokens)
    else:
        bot.reply_to(message, "режим gpt отключен" )


def start_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_chat_gpt = types.KeyboardButton("/gpt_chat")
    item2 = types.KeyboardButton("/start")
    item3 = types.KeyboardButton("расскажи анекдот про программиста")
    item4 = types.KeyboardButton("🎭 текущая роль")
    item5 = types.KeyboardButton("/stop")
    item6 = types.KeyboardButton("🎭 задать роль")
    markup.add(item_chat_gpt, item2, item3, item4, item5, item6)
    return markup


if __name__ == "__main__":
    print('Запущен...')
    bot.polling(none_stop=True)
