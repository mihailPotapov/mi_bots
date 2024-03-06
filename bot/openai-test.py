from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from pathlib import Path
import os
import random
import openai
import asyncio
import traceback
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from data_manager import TOKEN
from db_utils2 import (
    user_exists,
    get_db_pool,
    update_user_tokens,
    add_user_to_db,
    get_current_role,
    update_chat_role,
    get_role_name,
    get_user_tokens,
    get_user_id_somehow,
    get_all_voices,
    update_user_voice_choice,
    ensure_user_exists,
)


BACK_BUTTON = "◀ назад"

BACK_BUTTON2 = "◀ назад в настройки"
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
    "новая команда /speech позволит вам озвучить текст пример '/speech я gpt бот, чем могу помочь?'"
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
# флаги
active_chats = {}
user_flags = {}
# Проверяем и создаем папку для временного хранения аудиофайлов, если необходимо
temp_audio_folder = Path("temp_audio")
temp_audio_folder.mkdir(exist_ok=True)


async def get_voice_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    voices = await get_all_voices(db_pool)  # Это функция, которую вам нужно реализовать для получения голосов из БД
    for voice in voices:
        callback_data = f"voice_{voice['id']}"  # Пример callback_data, можете адаптировать под свои нужды
        keyboard.add(types.InlineKeyboardButton(text=voice['name_voice'], callback_data=callback_data))
    return keyboard


async def on_startup(dispatcher):
    global db_pool
    db_pool = await get_db_pool()
    print('Бот запущен и подключение к БД установлено.')


@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    with open('image/Hi.webp', 'rb') as hi:
        user = message.from_user
        if await user_exists(user.username, db_pool):
            await message.answer_sticker(hi)
            await message.answer("Рад снова вас видеть!", reply_markup=start_menu())
            await message.answer(WELCOME_MESSAGE)
            print('зашел старый пользователь')
        else:
            await message.answer_sticker(hi)
            await add_user_to_db(user.first_name, user.username, message.chat.id, db_pool)
            await message.answer("Рад видеть новое лицо!", reply_markup=start_menu())
            await message.answer(WELCOME_MESSAGE)
            print("новый пользователь", user.first_name, user.username, message.chat.id)


@dp.message_handler(commands=['gpt_chat'])
async def enable_gpt_chat(message: types.Message, db_pool):
    chat_id = message.chat.id
    user_id = await get_user_id_somehow(chat_id, db_pool)  # Убедитесь, что эта функция реализована
    if user_id is None:
        await message.answer("Пользователь не найден.")
        return

    async with db_pool.acquire() as conn:
        # Проверяем наличие пользователя в таблице tokens и обновляем данные
        row = await conn.fetchrow("SELECT id_user FROM tokens WHERE id_user = $1", user_id)
        if not row:
            await conn.execute("INSERT INTO tokens (id_user, token) VALUES ($1, $2)", user_id, 10000)

        # Проверяем и обновляем запись в chat_roles для этого чата
        row = await conn.fetchrow("SELECT id_chat FROM chat_roles WHERE id_chat = $1", chat_id)
        if not row:
            await conn.execute("INSERT INTO chat_roles (id_chat, id_roles) VALUES ($1, $2)", chat_id, 1)

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
async def list_roles(message: types.Message, db_pool):
    # Предполагаем, что db_pool глобально доступен и уже инициализирован, например, в функции on_startup

    async with db_pool.acquire() as conn:  # Получаем соединение из пула
        # В asyncpg нет необходимости создавать курсор для выполнения запроса
        roles = await conn.fetch("SELECT id_roles, name_roles FROM roles")

    markup_roles = InlineKeyboardMarkup()
    for role in roles:
        button = InlineKeyboardButton(role['name_roles'], callback_data=f"setrole_{role['id_roles']}")
        markup_roles.add(button)

    await message.answer("Вот текущие доступные роли:", reply_markup=markup_roles)


@dp.message_handler(commands=['current_role'])
async def current_role(message: types.Message, db_pool):
    chat_id = message.chat.id
    # Предполагается, что get_db_pool() - это ваша функция для получения пула соединений
    # Убедитесь, что db_pool глобально доступен и уже инициализирован

    async with db_pool.acquire() as conn:  # Получаем соединение из пула
        try:
            # Используем conn.fetchrow() для выполнения запроса и получения одной строки
            role = await conn.fetchrow(
                "SELECT r.name_roles FROM chat_roles cr "
                "JOIN roles r ON cr.id_roles = r.id_roles "
                "WHERE cr.id_chat = $1", chat_id)

            if role:
                await message.answer(f"Текущая роль: {role['name_roles']}")
            else:
                await message.answer("Роль для данного чата не установлена.")
        except Exception as e:
            await message.answer("Произошла ошибка при попытке получить текущую роль.")
            print(f"Произошла ошибка: {e}")


@dp.callback_query_handler(lambda call: call.data.startswith('setrole_'))
async def callback_inline(call: types.CallbackQuery):
    try:
        role_id = int(call.data.split('_')[1])
        chat_id = call.message.chat.id
        # Обновление роли в БД
        await update_chat_role(chat_id, role_id, db_pool)
        # Получение названия новой роли
        role_name = await get_role_name(role_id, db_pool)

        if role_name:
            await call.answer(f"Роль успешно сменена на '{role_name}'.", show_alert=True)
            # Удаление оригинального сообщения с клавиатурой
            await call.message.delete()

            # Отправка нового сообщения без клавиатуры
            await call.message.answer(f"Роль успешно сменена на '{role_name}'.")
        else:
            await call.answer("Произошла ошибка при смене роли.", show_alert=True)
    except Exception as e:
        await call.answer("Произошла ошибка при обработке вашего запроса.", show_alert=True)
        print(f"Ошибка: {e}")


@dp.message_handler(commands=['clear_the_history'])
async def clear_the_history(message: types.Message, db_pool):
    chat_id = message.chat.id
    try:
        # Предполагается, что эта функция корректно возвращает user_id для данного chat_id
        user_id = await get_user_id_somehow(chat_id, db_pool)  # Добавлен db_pool как аргумент, если нужно
        if user_id is None:
            await message.reply("Пользователь не найден.")
            return

        # Используем переданный db_pool напрямую
        async with db_pool.acquire() as conn:  # Получаем соединение из пула
            async with conn.transaction():  # Начинаем транзакцию
                # Предположим, что у вас есть таблица tokens с колонками id_user и token
                await conn.execute("UPDATE tokens SET token = 10000 WHERE id_user = $1", user_id)

        await message.reply("История токенов успешно восстановлена. Текущее количество токенов: 10000.")
    except Exception as e:
        await message.reply("Произошла ошибка при обработке запроса.")
        print(f"Ошибка: {e}")


# обработка голоса
async def get_user_voice_choice(chat_id, db_pool):
    async with db_pool.acquire() as connection:
        # Попытаемся получить выбранный голос пользователя
        user_voice_query = """
        SELECT v.name_voice 
        FROM voice_chat vc 
        JOIN voice v ON vc.voice_id = v.id 
        WHERE vc.chat_id = $1;  
        """
        user_voice_row = await connection.fetchrow(user_voice_query, chat_id)

        # Если у пользователя установлен выбор голоса, возвращаем его
        if user_voice_row:
            return user_voice_row['name_voice']
        else:
            # Если у пользователя не установлен выбор голоса, возвращаем голос по умолчанию (id=1)
            default_voice_query = "SELECT name_voice FROM voice WHERE id = 1;"
            default_voice_row = await connection.fetchrow(default_voice_query)
            return default_voice_row['name_voice'] if default_voice_row else None


# ОБРАБОТКА И РАБОТА С МОДЕЛЯМИ ДЛЯ ГОЛОСА
@dp.message_handler(commands=['voice'])
async def show_voice_options(message: types.Message):
    keyboard = await get_voice_keyboard()
    await message.answer("Выберите модель голоса:", reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data.startswith('voice_'))
async def handle_voice_choice(callback_query: types.CallbackQuery):
    try:
        voice_id = int(callback_query.data.split('_')[1])
        chat_id = callback_query.message.chat.id  # Используем chat_id вместо user_id

        # Обновляем выбор голосовой модели пользователя в БД
        await update_user_voice_choice(chat_id, voice_id, db_pool)  # Предполагаем, что update_user_voice_choice адаптирован под новую структуру

        # Получаем название новой голосовой модели
        async with db_pool.acquire() as conn:
            voice_name_record = await conn.fetchrow("SELECT name_voice FROM voice WHERE id = $1", voice_id)
        voice_name = voice_name_record['name_voice'] if voice_name_record else 'Неизвестная модель'

        if voice_name:
            await callback_query.answer(f"Модель голоса успешно изменена на '{voice_name}'.", show_alert=True)
            # Удаление оригинального сообщения с клавиатурой
            await callback_query.message.delete()

            # Отправка нового сообщения без клавиатуры
            await callback_query.message.answer(f"Модель голоса успешно изменена на '{voice_name}'.")
        else:
            await callback_query.answer("Произошла ошибка при смене модели голоса.", show_alert=True)
    except Exception as e:
        await callback_query.answer("Произошла ошибка при обработке вашего запроса.", show_alert=True)
        print(f"Ошибка: {e}")


#             проверка модели какая стоит
@dp.message_handler(commands=['the_voice'])
async def get_user_voice_model(message: types.Message, db_pool):
    chat_id = message.chat.id  # Пример изменения: используем chat_id вместо user_id

    async with db_pool.acquire() as conn:
        # Получаем voice_id для данного пользователя/чата
        voice_id_record = await conn.fetchrow("SELECT voice_id FROM voice_chat WHERE chat_id = $1", chat_id)

        if voice_id_record:
            voice_id = voice_id_record['voice_id']
            # Получаем название модели по voice_id
            voice_name_record = await conn.fetchrow("SELECT name_voice FROM voice WHERE id = $1", voice_id)
            if voice_name_record:
                voice_name = voice_name_record['name_voice']
                await message.reply(f"Вы используете голосовую модель: {voice_name}.")
            else:
                await message.reply("Название голосовой модели не найдено.")
        else:
            await message.reply("Вы ещё не выбрали голосовую модель. Используется модель по умолчанию.")




# голосовой обработчик
openai_client = client


@dp.message_handler(commands=['speech'])
async def speech_to_voice(message: types.Message):
    try:
        text_to_speech = message.text[len('/speech '):].strip()

        if not text_to_speech:
            await message.reply("Пожалуйста, введите текст после команды /speech.")
            return

        # Предположим, что chat_id это ID чата, где была вызвана команда
        chat_id = message.chat.id

        # Извлекаем выбор голоса пользователя из базы данных
        user_voice_choice = await get_user_voice_choice(chat_id, db_pool)  # db_pool должен быть доступен

        # Если для пользователя не установлен выбор голоса, используем голос по умолчанию
        if not user_voice_choice:
            user_voice_choice = "nova"  # Значение голоса по умолчанию

        # Создаем голосовое сообщение с выбранным голосом пользователя
        # Проверьте, что openai_client и соответствующие настройки корректно настроены
        response = openai_client.audio.speech.create(
            model="tts-1",
            voice=user_voice_choice,
            input=text_to_speech
        )

        # Сохраняем, отправляем и удаляем аудиофайл
        speech_file_path = temp_audio_folder / f"{message.from_user.id}_{message.message_id}.mp3"
        with speech_file_path.open('wb') as file:
            file.write(response.content)  # Предполагается, что response.content содержит аудиофайл

        with speech_file_path.open('rb') as audio:
            await message.reply_voice(voice=audio)

        speech_file_path.unlink()

    except Exception as e:
        print(f"Произошла ошибка при обработке команды speech: {e}")
        traceback.print_exc()
        await message.reply(f"Произошла ошибка: {e}")


# главный обработчик
@dp.message_handler()
async def gpt(message: types.Message):
    chat_id = message.chat.id
    if 'gpt_chat🤖' in message.text.lower():
        await enable_gpt_chat(message, db_pool)
    elif 'стоп⛔' in message.text.lower():
        await disable_gpt_stop_chat(message)
    elif 'настройки⚙' in message.text.lower():
        await disable_gpt_settings_chat(message)
    elif 'сменить роль🎭' in message.text.lower():
        await list_roles(message, db_pool)
    elif 'сменить голос🗣' in message.text.lower():
        await show_voice_options(message)
    elif 'текущая модель голоса🗣' in message.text.lower():
        await get_user_voice_model(message, db_pool)
    elif 'текущая роль🎭' in message.text.lower():
        await current_role(message, db_pool)
    elif 'роли🎭' in message.text.lower():
        await message.answer("Меню для настройки ролей:", reply_markup=menu_settings_role())
    elif 'голоса🗣' in message.text.lower():
        await message.answer("Меню для настройки модели голоса:", reply_markup=menu_settings_voice())
    elif 'очистить историю⌛' in message.text.lower():
        await clear_the_history(message, db_pool)
    elif BACK_BUTTON2 in message.text.lower():
        await message.answer("Меню для настройки gpt:", reply_markup=menu_settings())
    elif BACK_BUTTON in message.text.lower():
        await message.answer("Главное меню:", reply_markup=start_menu())
    elif chat_id in active_chats:
        current_tokens = await get_user_tokens(chat_id, db_pool)
        msg2 = await message.answer(f"Текущее количество токенов: {current_tokens}")

        if current_tokens <= 0:
            await message.answer("У вас не достаточно токенов.")
            return

        prompt = message.text if 'история' not in message.text.lower() else random.choice(history_phrases)
        msg = await message.answer('Сообщение принято. Ждем ответа..')

        role = await get_current_role(chat_id, db_pool)
        system_message = f"Ты {role}" if role else "Ты помощник"
        # Предполагается, что `client` инициализирован с нужными настройками OpenAI
        response = await asyncio.get_event_loop().run_in_executor(None, lambda: client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            max_tokens=700
        ))

        tokens_used = response.usage.total_tokens
        if current_tokens < tokens_used:
            await message.answer("У вас не достаточно токенов.")
            return

        gpt_text = response.choices[0].message.content
        await bot.delete_message(chat_id, msg.message_id)
        await bot.delete_message(chat_id, msg2.message_id)
        await message.answer(gpt_text)
        await message.answer(f"Потрачено следующее количество токенов: {tokens_used}")

        await update_user_tokens(chat_id, -tokens_used, db_pool)
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
    item1 = types.KeyboardButton("роли🎭")
    item2 = types.KeyboardButton("голоса🗣")
    item3 = types.KeyboardButton("очистить историю⌛")
    back_button = types.KeyboardButton(BACK_BUTTON)
    markup_settings.add(item1, item2, item3, back_button)
    return markup_settings


def menu_settings_role():
    markup_settings = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("текущая роль🎭")
    item2 = types.KeyboardButton("сменить роль🎭")
    back_button = types.KeyboardButton(BACK_BUTTON2)
    markup_settings.add(item1, item2, back_button)
    return markup_settings


def menu_settings_voice():
    markup_settings = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("сменить голос🗣")
    item2 = types.KeyboardButton("текущая модель голоса🗣")
    back_button = types.KeyboardButton(BACK_BUTTON2)
    markup_settings.add(item1, item2, back_button)
    return markup_settings


async def on_shutdown(dispatcher):
    await db_pool.close()
    print('Бот выключен и соединение с БД закрыто.')

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)