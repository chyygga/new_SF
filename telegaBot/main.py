import telebot
from extensions import APIException, ConvertValues
from config import keys, TOKEN

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Это учебный телерам-БОТ для конвертации разных валют. ' \
           'Для начала работы введите (через пробел)\n<колличество валюты (дробную часть разделять "точкой"> \
<название валюты, которую будем конвертировать>\
 <название валюты в которую конвертируем>\n Увидеть список всех доступных валют для конвертации: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.upper().split(' ')

        if len(values) != 3:
            raise APIException('Неверное число параметров')

        amount, quote, base = values
        total_res = ConvertValues.get_price(amount, quote, base)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя: \n"{e}"')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду: \n"{e}"')
    else:
        text = f'{amount} {quote} равен ' + str(total_res) + f' {base}'
        bot.send_message(message.chat.id, text)


bot.polling()
