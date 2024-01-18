# import telebot
# from telebot import types
# from data_manager import TOKEN
# # TOKEN = "5676606819:AAFmECqYhffaGAaJOD4SThzOcICSQNNEF0I"
# from openai import OpenAI
# # запрос пишем в консоле, ответ получаем тоже в консоле
# prompt= str(input())
# client = OpenAI(api_key="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")
# completion = client.chat.completions.create(
#     model="gpt-3.5-turbo-1106",
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": prompt}
#     ]
# )
# print('Вопрос:', prompt)
# print('\nОтвет:')
# print(completion.choices[0].message)
# попытка запустить через aiogram
# import openai
# from aiogram import Bot, types, Dispatcher
# from aiogram.utils import executor
#
# # from openai import OpenAI
# token = "5676606819:AAFmECqYhffaGAaJOD4SThzOcICSQNNEF0I"
#
# openai.api_key = "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"
#
# bot = Bot(token)
# bots = Dispatcher(bot)
#
#
# @bots.message_handler()
# async def send(message: types.Message):
#     response = openai.Completion.create(
#         model="text-davinci-003",
#         prompt=message.text,
#         temperature=0.9,
#         max_tokens=1000,
#         top_p=1.0,
#         frequency_penalty=0.0,
#         presence_penalty=0.6,
#         stop=["You:"]
#     )
#     await message.answer(response['choices'][0]['text'])
#
#
# executor.start_polling(bots, skip_updates=True)

# попытка  не удачная telebot
#
# import telebot
# import openai
# from data_manager import TOKEN, OPENAI_API_KEY
#
# openai.api_key = OPENAI_API_KEY
# bot = telebot.TeleBot(TOKEN)

# @bot.message_handler(content_types=['text'])
# def talk(message):
#     response = openai.Completion.create(
#         model="text-davinci-003",
#         prompt=message.text,
#         temperature=0.5,
#         max_tokens=1000,
#         top_p=1.0,
#         frequency_penalty=0.5,
#         presence_penalty=0.5
#     )
#     bot.send_message(message.chat.id, gpt_text)
#
#
# bot.polling(none_stop=True)





# @bot.message_handler(content_types=['text'])
# def gpt(message):
#     chat_id = message.chat.id
#     text = message.text.lower()
#     if message.chat.type == 'private':
#         if text == '🎭 задать роль':
#             bot.send_message(chat_id, 'Какую роль желаете? ')
#
#     elif text == '🗃 gpt_chat':
#         bot.send_message(chat_id, 'Я gpt_chat что желаете? ')
#
#     elif text == '🎭 текущая роль':
#         bot.send_message(chat_id, 'Я русский, научный помощник ')
#
#     else:


