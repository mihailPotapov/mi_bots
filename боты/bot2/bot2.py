import config
import logging
import telebot

from telebot import types

from aiogram.types import Message, ChatType

from datetime import timedelta

from aiogram import Bot, Dispatcher, types, executor
from filtres import IsAdminFilter

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

dp.filters_factory.bind(IsAdminFilter)


@dp.message_handler(commands=["start", "bot"], commands_prefix='!/')
async def start(message: types.Message):
    await message.answer("что надо? работаю я, работаю\nСкоро буду плату с вас брать")


@dp.message_handler(commands=["help"], commands_prefix='!/')
async def start(message: types.Message):
    await message.answer("привет, забыл список команд? ну ты и тупик, вот тебе список команд")
    await message.answer("/start или /bot - проверить пульс \n/help - читы \n/kick - выкинуть человека за борт \n/ban - забанить \n/unban - разбанить \n/admins - список админов")


@dp.message_handler(is_admin=True, commands=['kick'], commands_prefix='!/',
                    chat_type=[ChatType.GROUP, ChatType.SUPERGROUP])
async def kick_user(message: Message):
    if not message.reply_to_message:
        return await message.reply('это должен быть ответ на сообщение')
    await message.delete()

    user_id = message.reply_to_message.from_user.id
    seconds = 60
    await message.bot.ban_chat_member(chat_id=message.chat.id, user_id=user_id, until_date=timedelta(seconds=seconds))
    return await message.reply_to_message.reply(f'исключен на {seconds} секунд')


@dp.message_handler(is_admin=True, commands=['ban'], commands_prefix='!/',
                    chat_type=[ChatType.GROUP, ChatType.SUPERGROUP])
async def ban_user(message: Message):
    if not message.reply_to_message:
        await message.reply('это должен быть ответ на сообщение')
        return
    await message.delete()

    await message.bot.ban_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id, until_date=timedelta(seconds=29))
    return await message.reply_to_message.reply('забанен!!')


@dp.message_handler(is_admin=True, commands=['unban'], commands_prefix='!/')
async def unban_user(message: Message):
    if not message.reply_to_message:
        await message.reply('это должен быть ответ на сообщение')
        return
    await message.delete()
    await message.bot.unban_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id,
                                        only_if_banned=True)
    username = message.reply_to_message.from_user.username
    return await message.reply_to_message.reply(f'пользователя @{username} пожелели, кто нибудь передайте ему')


@dp.message_handler(commands=['admins'], chat_type=[ChatType.GROUP, ChatType.SUPERGROUP])
async def admins_command(message: Message) -> Message:
    chat_id = message.chat.id
    admins = await message.bot.get_chat_administrators(chat_id)
    text = ''
    for admin in admins:
        text += f'@{admin.user.username} '
    return await message.answer(text, disable_notification=True)


@dp.message_handler(content_types=["new_chat_members"])
async def new_chat(message: types.Message):
    new_member = message.new_chat_members[0]
    await message.answer(f"Привет {new_member.mention}!, рады, что ты присоединился!")
    await message.answer(f"Его пригласил @{message.from_user.username}")
    await message.delete()


@dp.message_handler(content_types=["left_chat_member"])
async def left_chat(message: types.Message):
    await message.answer(f"@{message.from_user.username} покинул нас")
    await message.delete()


@dp.message_handler()
async def filter_messages(message: types.Message):
    if message.text in ["блять","Блять","хуй","Хуй","пизда","Пизда","Идет на хуй","идет на хуй", "Идёт на хуй", "идёт на хуй", "На хуй", "идёт на хуй"]:
        await message.delete()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False)