import telebot
import requests
from config import TOKEN, keys_input
from extensions import ConversionException, Converter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = "Для того, чтобы начать работу введите команду боту формате: \n " \
           "<имя валюты(рубль), цену которой он хочет узнать> " \
           "<имя валюты(евро), в которой надо узнать цену первой валюты> " \
           "<количество первой валюты(2)>.\n"  \
           "Список валют команда:  /values"
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Список всех доступных валют:'
    for key in keys_input:
        text = '\n'.join([text, key])
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        text = message.text.lower()
        if len(text.split()) != 3:
            raise ConversionException('Данные введены неверно, вызовите /help для помощи')

        base, quote, amount = text.split()

        try:
            amount = float(amount)
        except ValueError:
            raise ConversionException('Неверный ввод количества. Введите число.')

        result = Converter.get_price(base, quote, float(amount))

        response_text = f'{amount} {keys_input[base]} равно {result:.2f} {keys_input[quote]}'
        bot.send_message(message.chat.id, response_text)

    except ConversionException as e:
        bot.send_message(message.chat.id, f'Ошибка: {e}')

bot.polling(none_stop=True)
