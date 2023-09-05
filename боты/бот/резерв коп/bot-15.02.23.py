import telebot
import config
import random
 
from telebot import types
 
bot = telebot.TeleBot(config.TOKEN)
 
@bot.message_handler(commands=['start'])
def welcome(message):
 sti = open('фото/Hi.webp', 'rb')
 bot.send_sticker(message.chat.id , sti)

 #keyboard_клава_тоесть
 markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
 item1 = types.KeyboardButton("🗃разное")
 item2 = types.KeyboardButton("🖼медия")
 markup.add(item1, item2)


 bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданный чтобы быть подопытным кроликом.".format(message.from_user, bot.get_me()),
 parse_mode='html', reply_markup=markup)

 chatId = message.chat.id
 text = message.text.lower

@bot.message_handler(content_types=['text'])
def test(message):
    chatId = message.chat.id
    text = message.text.lower
    if message.chat.type == 'private':
        if message.text == '🎲 Рандомное число':
            bot.send_message(message.chat.id , str(random.randint(0,100)))
        elif message.text == '😊 Как дела?':
            bot.send_message(message.chat.id, 'отлично, сам как?')
        elif message.text == '🖼медия':
                 markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                 item1 = types.KeyboardButton("Хочу обои")
                 item2 = types.KeyboardButton("скинь гифку")
                 back = types.KeyboardButton("◀назад")
                 markup.add(item1, item2, back,)
                 bot.send_message(message.chat.id, 'фото или гиф?', reply_markup=markup)
        elif message.text == '🗃разное':
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton("🎲 Рандомное число")
                item2 = types.KeyboardButton("😊 Как дела?")
                item3 = types.KeyboardButton("Расскажи о себе?")
                back = types.KeyboardButton("◀назад")
                markup.add(item1, item2,item3,back)
                bot.send_message(message.chat.id, 'м?', reply_markup=markup)
        elif message.text == 'Расскажи о себе?':
            bot.send_message(message.chat.id, 'я бот созданый криворуким програмистом, сейчас умею отправлять стикер, гифку и фото')
        elif message.text == 'Хочу обои':
            bot.send_message(message.chat.id, 'держи')
            oboi= ["фото2/oboi1.jpg", "фото2/oboi2.jpg", "фото2/oboi3.jpg", "фото2/oboi4.jpg", "фото2/oboi5.jpg", "фото2/oboi6.jpg", "фото2/oboi7.jpg", "фото2/oboi8.jpg", "фото2/oboi9.jpg", "фото2/oboi10.jpg"]
            img_path = random.choice(oboi)
            bot.send_photo(message.chat.id, photo=open(img_path, 'rb'))
        elif message.text == 'Привет':
            bot.send_message(message.chat.id, 'Привет')
            gif1= open("гиф/AnimatedSticker5.tgs", 'rb')
            bot.send_sticker(message.chat.id , gif1)
        elif message.text == 'Пошёл на хуй':
            bot.send_message(message.chat.id, 'сам иди на хуй')
            gif2= open("гиф/Sticker.tgs", 'rb')
            bot.send_sticker(message.chat.id , gif2)
        elif message.text == 'скинь гифку':
            bot.send_message(message.chat.id, 'держи')
            gif = ["гиф/gif.gif", "гиф/ser.gif", "гиф/gif2.gif", "гиф/gif3.gif"]
            gif_path = random.choice(gif)
            bot.send_video(message.chat.id, open(gif_path, 'rb'))
        elif message.text == '◀назад':
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton("🗃разное")
                item2 = types.KeyboardButton("🖼медия")
                markup.add(item1, item2)
                bot.send_message(message.chat.id, 'да?', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'я не понимаю тебя')
        
   
# RUN
bot.polling(none_stop=True)
