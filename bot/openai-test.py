from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import os
import random
import openai
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from data_manager import TOKEN
from db_utils222 import (
    user_exists,
    add_user_to_db,
    get_current_role,
    update_chat_role,
    get_db_connection,
    get_role_name,
    update_user_tokens,
    get_user_tokens,
    get_user_id_somehow,
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

if not encrypted_api_key:
    raise Exception("Зашифрованный API ключ не найден в .env файле.")

# Чтение ключа шифрования
with open("secret.key", "rb") as key_file:
    key = key_file.read()

# Расшифровка API ключа
fernet = Fernet(key)
decrypted = fernet.decrypt(encrypted_api_key.encode())
api_key1 = decrypted.decode()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())
client = openai.OpenAI(api_key=api_key1)
active_chats = {}


def start_menu() -> types.ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton('gpt_chat🤖'))
    markup.add(KeyboardButton('стоп⛔'), KeyboardButton('настройки⚙'))
    markup.add(KeyboardButton('сменить роль🎭'), KeyboardButton('текущая роль🎭'))
    return markup


@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    with open('image/Hi.webp', 'rb') as hi:
        user = message.from_user
        if await user_exists(user.username):
            await message.answer_photo(hi)
            await message.answer("Рад снова вас видеть!", reply_markup=start_menu())
            await message.answer(WELCOME_MESSAGE)
        else:
            await message.answer_photo(hi)
            await add_user_to_db(user.first_name, user.username, message.chat.id)
            await message.answer("Рад видеть новое лицо!", reply_markup=start_menu())
            await message.answer(WELCOME_MESSAGE)
            print("новый пользователь", user.first_name, user.username, message.chat.id)


@dp.message_handler(commands=['gpt_chat'])
async def enable_gpt_chat(message: types.Message):
    chat_id = message.chat.id
    user_id = get_user_id_somehow(message.chat.id)
    # Подключение к базе данных и обновление информации о пользователе
    # Следующий блок кода аналогичен вашей логике работы с базой данных

    async with get_db_connection() as conn:
        async with conn.cursor() as cursor:
            # Проверяем наличие пользователя в таблице tokens и обновляем данные
            await cursor.execute("SELECT id_user FROM tokens WHERE id_user = %s", (user_id,))
            if not await cursor.fetchone():
                await cursor.execute("INSERT INTO tokens (id_user, token) VALUES (%s, 10000)", (user_id,))
                await conn.commit()

            # Проверяем и обновляем запись в chat_roles для этого чата
            await cursor.execute("SELECT id_chat FROM chat_roles WHERE id_chat = %s", (chat_id,))
            if not await cursor.fetchone():
                await cursor.execute("INSERT INTO chat_roles (id_chat, id_roles) VALUES (%s, %s)", (chat_id, 1))
                await conn.commit()

    # Активация чата
    active_chats[chat_id] = True
    await message.answer("Режим GPT чата включен.")
    await message.answer("Меню GPT:", reply_markup=gpt_menu())


@dp.message_handler(commands=['stop'])
async def disable_gpt_stop_chat(message: types.Message):
    active_chats.pop(message.chat.id, None)
    await message.answer("Режим GPT чата отключен.")
    await message.answer("Главное меню:", reply_markup=start_menu())


@dp.message_handler(commands=['settings'])
async def disable_gpt_settings_chat(message: types.Message):
    active_chats.pop(message.chat.id, None)
    await message.answer("Режим GPT чата отключен для настройки.")
    await message.answer("Меню для настройки gpt:", reply_markup=menu_settings())


@dp.message_handler(commands=['gpt_roles'])
async def list_roles(message: types.Message):
    async with get_db_connection() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT id_roles, name_roles FROM roles")
            roles = await cursor.fetchall()

    markup_roles = InlineKeyboardMarkup()
    for role in roles:
        button = InlineKeyboardButton(role[1], callback_data=f"setrole_{role[0]}")
        markup_roles.add(button)

    await message.answer("Вот текущие доступные роли:", reply_markup=markup_roles)


@dp.message_handler(commands=['current_role'])
async def current_role(message: types.Message):
    chat_id = message.chat.id
    async with get_db_connection() as conn:
        async with conn.cursor() as cursor:
            try:
                await cursor.execute(
                    "SELECT r.name_roles FROM chat_roles cr "
                    "JOIN roles r ON cr.id_roles = r.id_roles "
                    "WHERE cr.id_chat = %s", (chat_id,))
                role = await cursor.fetchone()

                if role:
                    await message.answer(f"Текущая роль: {role[0]}")
                else:
                    await message.answer("Роль для данного чата не установлена.")
            except Exception as e:
                print(f"Произошла ошибка: {e}")


@dp.callback_query_handler(lambda call: call.data.startswith('setrole_'))
async def callback_inline(call: types.CallbackQuery):
    role_id = int(call.data.split('_')[1])
    chat_id = call.message.chat.id

    # Обновление роли в БД
    await update_chat_role(chat_id, role_id)

    # Получение названия новой роли
    role_name = await get_role_name(role_id)

    await call.answer(f"Роль успешно сменена на '{role_name}'.", show_alert=True)
    # Удаление оригинального сообщения с клавиатурой
    await call.message.delete()

    # Отправка нового сообщения без клавиатуры
    await call.message.answer(f"Роль успешно сменена на '{role_name}'.")


@dp.message_handler(commands=['clear_the_history'])
async def clear_the_history(message: types.Message):
    chat_id = message.chat.id
    user_id = await get_user_id_somehow(chat_id)
    if user_id is None:
        await bot.send_message(chat_id, "Пользователь не найден.")
        return

    conn = await get_db_connection()
    async with conn.transaction():
        await conn.execute("UPDATE tokens SET token = 10000 WHERE id_user = $1", user_id)

    await conn.close()

    await bot.send_message(chat_id, "История токенов успешно восстановлена. Текущее количество токенов: 10000.")


@dp.message_handler()
async def gpt(message: types.Message):
    chat_id = message.chat.id
    # Специальные команды, работающие независимо от режима GPT
    if 'gpt_chat🤖' in message.text.lower():
        await enable_gpt_chat(message)
    elif 'стоп⛔' in message.text.lower():
        await disable_gpt_stop_chat(message)
    elif 'настройки⚙' in message.text.lower():
        await disable_gpt_settings_chat(message)
    elif 'сменить роль🎭' in message.text.lower():
        await list_roles(message)
    elif 'текущая роль🎭' in message.text.lower():
        await current_role(message)
    elif 'очистить историю' in message.text.lower():
        await clear_the_history(message)
    elif BACK_BUTTON in message.text.lower():
        await message.answer("Главное меню:", reply_markup=start_menu())
    elif chat_id in active_chats:
        current_tokens = await get_user_tokens(chat_id)
        await message.answer(f"Текущее количество токенов: {current_tokens}")

        if current_tokens <= 0:
            await message.answer("У вас не достаточно токенов.")
            return

        prompt = message.text if 'история' not in message.text.lower() else random.choice(history_phrases)
        await message.answer('Сообщение принято. Ждем ответа..')

        role = await get_current_role(chat_id)
        system_message = f"Ты {role}" if role else "Ты помощник"
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ]
        )

        tokens_used = response.usage.total_tokens
        if current_tokens < tokens_used:
            await message.answer("У вас не достаточно токенов.")
            return

        gpt_text = response.choices[0].message.content
        await message.answer(gpt_text)
        await message.answer(f"Потрачено следующее количество токенов: {tokens_used}")

        await update_user_tokens(chat_id, tokens_used)
        new_token_balance = current_tokens - tokens_used
        await message.answer(f"Текущее количество токенов: {new_token_balance}")
    else:
        await message.reply("режим GPT отключен")


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
    back_button = types.KeyboardButton(BACK_BUTTON)
    markup_gpt.add(item_chat_gpt, item1, item2, item3, back_button)
    return markup_gpt


def menu_settings():
    markup_settings = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("текущая роль🎭")
    item2 = types.KeyboardButton("сменить роль🎭")
    item3 = types.KeyboardButton("очистить историю")
    back_button = types.KeyboardButton(BACK_BUTTON)
    markup_settings.add(item1, item2, item3, back_button)
    return markup_settings


if __name__ == '__main__':
    print('запущен')
    executor.start_polling(dp)
    print('выключен')