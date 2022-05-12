import requests
from datetime import datetime
import telebot
from config import token
from telebot import types



def get_data():
    req = requests.get("https://yobit.net/api/3/ticker/btc_usd")
    response = req.json()

    sell_price = response["btc_usd"]["sell"]
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M')}\nSell BTC price: {sell_price}")

def telegram_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=["start"])
    def start_message(message):
        bot.send_message(message.chat.id, "Привет! я бот который умеет показывать цену биткойна в долларах на данный момент")
        keyboard = types.ReplyKeyboardMarkup()  # клавиатура
        key = types.KeyboardButton(text='Price',) # кнопка
        keyboard.add(key)
        bot.send_message(message.from_user.id, text="Попробуй", reply_markup=keyboard)

        @bot.callback_query_handler(func=lambda call: True)
        def callback_worker(call):
            if call.data == "Price":
                bot.send_message(call.message.chat.id, '')


    @bot.message_handler(content_types=["text"])
    def send_text(message):
        if message.text.lower() == "price":
            try:
                req = requests.get("https://yobit.net/api/3/ticker/btc_usd")
                response = req.json()
                sell_price = response["btc_usd"]["sell"]
                bot.send_message(
                    message.chat.id,
                    f"{datetime.now().strftime('%Y-%m-%d %H:%M')}\nSell BTC price: {sell_price}"
                )
            except Exception as ex:
                print(ex)
                bot.send_message(
                    message.chat.id,
                    "damn...something is wrong..."
                )
        else:
            bot.send_message(message.chat.id, "what? check your command!")
    bot.polling()



if __name__ == '__main__':
    get_data()
    telegram_bot(token)