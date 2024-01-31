import telebot
import os
import random
from telebot import types
from openai import OpenAI
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from data_manager import TOKEN
from db_utils import (
    user_exists,
    add_user_to_db,
    get_current_role,
    update_chat_role,
    get_db_connection,
    get_role_name
)
BACK_BUTTON = "◀ назад"
history_phrases = [
    "расскажи свою историю",
    "расскажи забавный случай у тебя"
]

load_dotenv()

# Чтение зашифрованного API ключа из .env
encrypted_api_key = os.getenv("ENCRYPTED_API_KEY")
WELCOME_MESSAGE = (
    "Что бы начать диалог нажмите на кнопку 'gpt_chat🤖'\n"
    "Что бы завершить диалог нажмите на кнопку 'стоп⛔'\n"
    "Что бы войти в меню для настройки gpt\n Нажмите на кнопку 'настройки⚙'\n"
    "будут доступны следующие кнопки-команды\n"
    "Что бы выбрать роль нажмите 'сменить роль🎭'\n"
    "Что бы проверить текущую роль нажмите 'текущая роль🎭'"
)
# Убедитесь, что зашифрованный ключ существует
if not encrypted_api_key:
    raise Exception("Зашифрованный API ключ не найден в .env файле.")

# Чтение ключа шифрования
with open("secret.key", "rb") as key_file:
    key = key_file.read()

# Расшифровка API ключа
fernet = Fernet(key)
decrypted = fernet.decrypt(encrypted_api_key.encode())
api_key1 = decrypted.decode()

bot = telebot.TeleBot(TOKEN)
client = OpenAI(api_key=api_key1)
active_chats = {}



# Обработчики команд бота
@bot.message_handler(commands=['start'])
def welcome(message):
    hi = open('image/Hi.webp', 'rb')
    user = message.from_user
    if user_exists(user.username):
        bot.send_sticker(message.chat.id, hi)
        bot.send_message(message.chat.id, "Рад снова вас видеть!", reply_markup=start_menu())
        bot.send_message(message.chat.id, WELCOME_MESSAGE)
    else:
        bot.send_sticker(message.chat.id, hi)
        add_user_to_db(user.first_name, user.username, message.chat.id)
        bot.send_message(message.chat.id, "Рад видеть новое лицо!", reply_markup=start_menu())
        bot.send_message(message.chat.id, WELCOME_MESSAGE)
        print("новый пользователь", user.first_name, user.username, message.chat.id)


@bot.message_handler(commands=['gpt_chat🤖'])
def enable_gpt_chat(message):
    chat_id = message.chat.id
    active_chats[chat_id] = True

    # Проверяем, есть ли уже запись в chat_roles для этого чата
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_chat FROM chat_roles WHERE id_chat = %s", (chat_id,))
    if not cursor.fetchone():
        # Если нет, создаем новую запись с начальной ролью (например, id роли 1)
        cursor.execute("INSERT INTO chat_roles (id_chat, id_roles) VALUES (%s, %s)", (chat_id, 1))
        conn.commit()
    cursor.close()
    conn.close()

    bot.send_message(chat_id, "Режим GPT чата включен.")
    bot.send_message(message.chat.id, "Меню gpt:", reply_markup=gpt_menu())


@bot.message_handler(commands=['stop⛔'])
def disable_gpt_stop_chat(message):
    active_chats.pop(message.chat.id, None)
    bot.send_message(message.chat.id, "Режим GPT чата отключен.")
    bot.send_message(message.chat.id, "Главное меню:", reply_markup=start_menu())


@bot.message_handler(commands=['settings⚙'])
def disable_gpt_settings_chat(message):
    active_chats.pop(message.chat.id, None)
    bot.send_message(message.chat.id, "Режим GPT чата отключен для настройки.")
    bot.send_message(message.chat.id, "Меню для настройки gpt:", reply_markup=menu_settings())


@bot.message_handler(commands=['gpt_roles🎭'])
def list_roles(message):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_roles, name_roles FROM roles")
    roles = cursor.fetchall()
    cursor.close()
    conn.close()

    markup_roles = types.InlineKeyboardMarkup()
    for role in roles:
        button = types.InlineKeyboardButton(role[1], callback_data=f"setrole_{role[0]}")
        markup_roles.add(button)

    bot.send_message(message.chat.id, "Вот текущие доступные роли:", reply_markup=markup_roles)


@bot.message_handler(commands=['current_role🎭'])
def current_role(message):
    chat_id = message.chat.id
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Запрос для получения текущей роли для чата
        cursor.execute(
            "SELECT r.name_roles FROM chat_roles cr "
            "JOIN roles r ON cr.id_roles = r.id_roles "
            "WHERE cr.id_chat = %s", (chat_id,))
        role = cursor.fetchone()

        # Отладочная печать результата запроса
        # print(f"Результат запроса для чата {chat_id}: {role}")

        if role:
            bot.send_message(chat_id, f"Текущая роль: {role[0]}")
        else:
            bot.send_message(chat_id, "Роль для данного чата не установлена.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        cursor.close()
        conn.close()


# Функция обработки нажатия на кнопку inline-клавиатуры
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data.startswith('setrole_'):
            role_id = int(call.data.split('_')[1])
            chat_id = call.message.chat.id

            # Обновление роли в БД
            update_chat_role(chat_id, role_id)

            # Получение названия новой роли
            role_name = get_role_name(role_id)

            bot.answer_callback_query(call.id, f"Роль успешно сменена на '{role_name}'.")
            # Удаление оригинального сообщения с клавиатурой
            bot.delete_message(chat_id, call.message.message_id)

            # Отправка нового сообщения без клавиатуры
            bot.send_message(chat_id, f"Роль успешно сменена на '{role_name}'.")


@bot.message_handler(func=lambda message: True)
def gpt(message):
    if message.chat.id in active_chats:
        # Проверка на слово "history"
        if 'история' in message.text.lower():
            prompt = random.choice(history_phrases)
        else:
            prompt = message.text

        msg = bot.send_message(message.chat.id, 'Сообщение принято. Ждем ответа..')
        role = get_current_role(message.chat.id)
        system_message = f"Ты {role}, помощник" if role else "Ты помощник"
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ]
        )
        tokens = response.usage.total_tokens
        gpt_text = response.choices[0].message.content
        bot.delete_message(message.chat.id, msg.message_id)
        bot.send_message(message.chat.id, gpt_text)
        bot.send_message(message.chat.id, f"потрачено следующее количество токенов: {tokens}")
        print('\nвопрос:', prompt)
        print('\nответ:', gpt_text)
        print('потрачено токенов:', tokens)

    elif BACK_BUTTON in message.text.lower():
        bot.send_message(message.chat.id, "Главное меню:", reply_markup=start_menu())

    elif 'сменить роль🎭' in message.text.lower():
        list_roles(message)

    elif 'текущая роль🎭' in message.text.lower():
        current_role(message)

    elif 'настройки⚙' in message.text.lower():
        disable_gpt_settings_chat(message)

    elif 'gpt_chat🤖' in message.text.lower():
        enable_gpt_chat(message)

    elif 'стоп⛔' in message.text.lower():
        disable_gpt_stop_chat(message)

    else:
        bot.reply_to(message, "режим GPT отключен")


# Вспомогательные функции
def start_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_chat_gpt = types.KeyboardButton("gpt_chat🤖")
    item1 = types.KeyboardButton("/start")
    item2 = types.KeyboardButton("настройки⚙")
    markup.add(item_chat_gpt, item1, item2)
    return markup


def gpt_menu():
    markup_gpt = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_chat_gpt = types.KeyboardButton("gpt_chat🤖")
    item1 = types.KeyboardButton("история")
    item2 = types.KeyboardButton("стоп⛔")
    item3 = types.KeyboardButton("настройки⚙")
    item4 = types.KeyboardButton(BACK_BUTTON)
    markup_gpt.add(item_chat_gpt, item1, item2, item3, item4)
    return markup_gpt


def menu_settings():
    markup_settings = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("текущая роль🎭")
    item2 = types.KeyboardButton("сменить роль🎭")
    item3 = types.KeyboardButton(BACK_BUTTON)
    markup_settings.add(item1, item2, item3,)
    return markup_settings


if __name__ == "__main__":
    print('Запущен...')
    bot.polling(none_stop=True)
    print('Выключен...')