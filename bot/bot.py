import telebot
import random
import masiv_filtr
from telebot import types
from data_manager import TOKEN, UserDatabase

# Константы
BACK_BUTTON = "◀ назад"
WELCOME_MESSAGE = (
    "Добро пожаловать, {0.first_name}!\n"
    "Я - <b>{1.first_name}</b>, бот созданный для проверки разный функций."
)

# Инициализация бота и базы данных
bot = telebot.TeleBot(TOKEN)
db = UserDatabase('userdatabase.db')

@bot.message_handler(commands=['start'])
def welcome(message):
    hi = open('image/Hi.webp', 'rb')
    bot.send_sticker(message.chat.id, hi)

    user_id = message.from_user.id

    if not db.is_user_exists(user_id):
        db.add_new_user(user_id)

    bot.send_message(message.chat.id, WELCOME_MESSAGE.format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=start_menu())

@bot.message_handler(content_types=['text'])
def main(message):
    chat_id = message.chat.id
    text = message.text.lower()
    user_id = message.from_user.id

    if message.chat.type == 'private':
        if text == '🎲 рандомное число':
            perform_purchase(chat_id, user_id, 10, lambda: bot.send_message(chat_id, f"Выпало число: {str(random.randint(0, 1000))}"))

        elif text == '🤑 заработать денег':
            current_balance = db.get_user_balance(user_id)
            new_balance = current_balance + 1
            db.update_user_balance(user_id, new_balance)
            bot.send_message(chat_id, f"💰 Вы заработали 1 монету.\n💵 Баланс: {new_balance}")
        
        elif text == '💼 мой баланс':
            current_balance = db.get_user_balance(user_id)
            bot.send_message(chat_id, f"💵 Баланс: {current_balance}")

        elif text == '😊 как дела?':
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("хорошо", callback_data='good')
            item2 = types.InlineKeyboardButton("не очень", callback_data='bad')
            markup.add(item1, item2)
            bot.send_message(chat_id, 'Отлично, сам как? 😊', reply_markup=markup)

        elif text == '🖼 медия':
            media_menu(chat_id)
            
        elif text == '🗃 разное':
            diverse_menu(chat_id)

        elif text == 'расскажи о себе?':
            bot.send_message(chat_id, 'Я - бот, созданный для предоставления различных услуг. ')
# ошибка попробовать найти решение
        elif text == 'Что ты умеешь?':
            bot.send_message(chat_id, 'Я - бот, который умеет отправлять фото и gif, и задавать рандомное число ')
       
        elif text == 'хочу обои':
            wallpapers_menu(chat_id)

        elif text == 'хочу крутые обои 😎':
            perform_purchase(chat_id, user_id, 21, lambda: send_random_image(chat_id, masiv_filtr.oboi_gryt))

        elif text == 'аниме':
            perform_purchase(chat_id, user_id, 22, lambda: send_random_image(chat_id, masiv_filtr.oboi_anime))

        elif text == ['привет','Привет']:
            bot.send_message(chat_id, 'Привет! 👋')
            bot.send_sticker(chat_id, sticker=open("gif/AnimatedSticker.tgs", 'rb'))

        elif text in masiv_filtr.otvet:
            bot.send_photo(chat_id, photo=open("image/ric.jpg", 'rb'))

        elif text in masiv_filtr.mat:
            bot.send_message(chat_id, 'Сам иди на хуй! 😡')
            bot.send_sticker(chat_id, sticker=open("gif/Sticker.tgs", 'rb'))

        elif text == 'скинь гифку':
            perform_purchase(chat_id, user_id, 30, lambda: (
                bot.send_message(chat_id, 'Держи гифку! 😎'),
                bot.send_document(chat_id, document=open(random.choice(masiv_filtr.gif), 'rb'))
            ))
                        
        elif text == BACK_BUTTON:
            bot.send_message(chat_id, "Главное меню:", reply_markup=start_menu())

        elif text in masiv_filtr.Vi:
            diverse_menu(chat_id)

        elif text == 'чит деньги':
            current_balance = db.get_user_balance(user_id)
            new_balance = current_balance + 100000
            db.update_user_balance(user_id, new_balance)
            bot.send_message(chat_id, f"💰 Вы заработали 100000 монету так как вы вип.\n💵 Баланс: {new_balance}")

        else:
            bot.send_message(chat_id, 'Я не понимаю тебя. 😕')
            bot.send_message(chat_id, 'Проверьте правильно ли Вы ввели команду, используйте лучше клавиатуру.')

def start_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("🗃 разное")
    item2 = types.KeyboardButton("🖼 медия")
    markup.add(item1, item2)
    return markup

def media_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("хочу обои")
    item2 = types.KeyboardButton("скинь гифку")
    item3 = types.KeyboardButton(BACK_BUTTON)
    markup.add(item1, item2, item3)
    bot.send_message(chat_id, "Выберите тип медиа:", reply_markup=markup)

def diverse_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("🎲 рандомное число")
    item2 = types.KeyboardButton("😊 как дела?")
    item3 = types.KeyboardButton("расскажи о себе?")
    item4 = types.KeyboardButton("🤑 заработать денег")
    item5 = types.KeyboardButton("💼 мой баланс")
    item6 = types.KeyboardButton("Что ты умеешь?")
    item7 = types.KeyboardButton(BACK_BUTTON)
    markup.add(item1, item2, item3, item4, item5, item6,item7)
    bot.send_message(chat_id, "Выберите раздел:", reply_markup=markup)

def wallpapers_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("хочу крутые обои 😎")
    item2 = types.KeyboardButton("аниме")
    item3 = types.KeyboardButton(BACK_BUTTON)
    markup.add(item1, item2, item3)
    bot.send_message(chat_id, 'Аниме или крутые обои? 😎', reply_markup=markup)

def send_random_image(chat_id, image_list):
    if image_list:
        bot.send_message(chat_id, 'Держи! 😎')
        img_path = random.choice(image_list)
        bot.send_photo(chat_id, photo=open(img_path, 'rb'))

def perform_purchase(chat_id, user_id, item_price, item_action):
    current_balance = db.get_user_balance(user_id)
    
    if current_balance < item_price:
        needed_coins = item_price - current_balance
        message = f"У вас недостаточно средств для этой операции. Вам нужно {needed_coins} монет."
        bot.send_message(chat_id, message)
    else:
        new_balance = current_balance - item_price
        db.update_user_balance(user_id, new_balance)
        bot.send_message(chat_id, f"💵 Баланс: {new_balance}")
        item_action()

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, 'Вот и отличненько! 😊')
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'Бывает. 😢')

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Как дела? 😊", reply_markup=None)
    except Exception as e:
        print(repr(e))

if __name__ == "__main__":
    print('Запущен...')
    bot.polling(none_stop=True)
