import telebot
import config
import random

from telebot import types

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('фото/Hi.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)

    # keyboard_клава_тоесть
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("🗃разное")
    item2 = types.KeyboardButton("🖼медия")
    # item3 = types.KeyboardButton("загадки")
    markup.add(item1, item2)

    bot.send_message(message.chat.id,"Добро пожаловать, {0.first_name}!"
                                     "\nЯ - <b>{1.first_name}</b>, бот созданный чтобы быть подопытным кроликом."
                     .format(message.from_user, bot.get_me()),parse_mode='html', reply_markup=markup)

    chatId = message.chat.id
    text = message.text.lower


@bot.message_handler(content_types=['text'])
def test(message):
    chatId = message.chat.id
    text = message.text.lower
    if message.chat.type == 'private':
        if message.text == '🎲 Рандомное число':
            bot.send_message(message.chat.id, str(random.randint(0, 100)))
        elif message.text == '😊 Как дела?':
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Хорошо", callback_data='good')
            item2 = types.InlineKeyboardButton("Не очень", callback_data='bad')
            markup.add(item1, item2)
            bot.send_message(message.chat.id, 'Отлично, сам как?', reply_markup=markup)
        elif message.text == '🖼медия':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Хочу обои")
            item2 = types.KeyboardButton("скинь гифку")
            back = types.KeyboardButton("◀назад")
            markup.add(item1, item2, back, )
            bot.send_message(message.chat.id, 'фото или гиф?', reply_markup=markup)
        elif message.text == '🗃разное':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("🎲 Рандомное число")
            item2 = types.KeyboardButton("😊 Как дела?")
            item3 = types.KeyboardButton("Расскажи о себе?")
            back = types.KeyboardButton("◀назад")
            markup.add(item1, item2, item3, back)
            bot.send_message(message.chat.id, 'м?', reply_markup=markup)
        elif message.text == 'Расскажи о себе?':
            bot.send_message(message.chat.id,
                             'я бот созданый криворуким програмистом, сейчас умею отправлять стикер, гифку, фото'
                             '\nТак же могу тебя послать')
        elif message.text == 'test':
            bot.send_message(message.chat.id, 'держи')
            oboi = ["фото2/oboi1.jpg", "фото2/oboi2.jpg", "фото2/oboi3.jpg", "фото2/oboi4.jpg", "фото2/oboi5.jpg",
                    "фото2/oboi6.jpg", "фото2/oboi7.jpg", "фото2/oboi8.jpg", "фото2/oboi9.jpg", "фото2/oboi10.jpg",
                    "фото2/oboi11.jpg", "фото2/oboi12.jpg", "фото2/oboi13.jpg", "фото2/oboi14.jpg", "фото2/oboi15.jpg",
                    "фото2/oboi16.jpg"]
            img_path = random.choice(oboi)
            bot.send_photo(message.chat.id, photo=open(img_path, 'rb'))
        elif message.text == 'Хочу обои':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Хочу крутые обои😎")
            item2 = types.KeyboardButton("Аниме")
            back = types.KeyboardButton("◀назад")
            markup.add(item1, item2, back, )
            bot.send_message(message.chat.id, 'Аниме или крутые обои😎?', reply_markup=markup)
        elif message.text == 'Хочу крутые обои😎':
            bot.send_message(message.chat.id, 'держи😎')
            oboi = ["фото2/oboi1.jpg", "фото2/oboi2.jpg", "фото2/oboi3.jpg", "фото2/oboi4.jpg", "фото2/oboi5.jpg",
                    "фото2/oboi6.jpg",]
            img_path = random.choice(oboi)
            bot.send_photo(message.chat.id, photo=open(img_path, 'rb'))
        elif message.text == 'Аниме':
            bot.send_message(message.chat.id, 'держи😎')
            oboi = ["фото2/oboi7.jpg", "фото2/oboi8.jpg", "фото2/oboi9.jpg", "фото2/oboi10.jpg",
                    "фото2/oboi11.jpg", "фото2/oboi12.jpg", "фото2/oboi13.jpg", "фото2/oboi14.jpg", "фото2/oboi15.jpg",
                    "фото2/oboi16.jpg"]
            img_path = random.choice(oboi)
            bot.send_photo(message.chat.id, photo=open(img_path, 'rb'))
        elif message.text in ["Привет", "привет", ]:
            bot.send_message(message.chat.id, 'Привет')
            gif1 = open("гиф/AnimatedSticker5.tgs", 'rb')
            bot.send_sticker(message.chat.id, gif1)
        elif message.text in ["почему ты материшься?", "Почему ты материшься?", "Почему ты посылаешь?",
                              "почему ты посылаешь?", "Почему ты посылаешь меня?", "почему ты посылаешь меня?"]:
            bot.send_message(message.chat.id, 'Вам пишет разработчик:'
                                              '\n"Зачем я научил бота посылать в ответ? ЗАЧЕМ?.."')
            foto1 = open("фото/ric.jpg", 'rb')
            bot.send_photo(message.chat.id, foto1)
        elif message.text in ["Иди на хуй", "Иди нахуй", "иди на хуй", "иди нахуй", "пошел на хуй", "пошёл на хуй",
                              "пошел нахуй", "пошёл нахуй", "Пошел на хуй", "Пошёл нахуй", "Пошёл на хуй"]:
            bot.send_message(message.chat.id, 'сам иди на хуй')
            gif2 = open("гиф/Sticker.tgs", 'rb')
            bot.send_sticker(message.chat.id, gif2)
        elif message.text == 'скинь гифку':
            bot.send_message(message.chat.id, 'держи')
            gif = ["гиф/gif.gif", "гиф/ser.gif", "гиф/gif2.gif", "гиф/gif3.gif"]
            gif_path = random.choice(gif)
            bot.send_video(message.chat.id, open(gif_path, 'rb'))
        elif message.text == '◀назад':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("🗃разное")
            item2 = types.KeyboardButton("🖼медия")
            # item3 = types.KeyboardButton("загадки")
            markup.add(item1, item2)
            bot.send_message(message.chat.id, 'да?', reply_markup=markup)
        elif message.text in ["Vi", "vi", "VI", "Ви", "ви", "ВИ", "Bot_vi", "Bot_Vi", "Bot", "bot", "Бот", "бот"]:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("🗃разное")
            item2 = types.KeyboardButton("🖼медия")
            # item3 = types.KeyboardButton("загадки")
            markup.add(item1, item2)
            bot.send_message(message.chat.id, 'Я тут, что-то хотели?', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'я не понимаю тебя')


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


# RUN
bot.polling(none_stop=True)