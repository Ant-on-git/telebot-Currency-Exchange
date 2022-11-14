import telebot
from config import TOKEN, currency
from extensions import APIException, CurrencyConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start_help(message):
    text = "Чтобы перевести вылюту, нужно отправить мне сообщение в формате: \n \
<имя валюты> <в какую валюту перевести> <количество переводимой валюты>. \n \
Например, чтобы перевести 1000 долларов в рубли, нужно отправить сообщение: \n \
доллар рубль 1000\n \n \
Чтобы вывести список доступных валют, введите команду \n /values\n  \
Для повтора инструкции введите команду \n \
/help"
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message):
    text = 'Доступные валюты:\n - ' + '\n - '.join(currency.keys())
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def transfer(message):
    values = message.text.split()
    try:
        if len(values) != 3:
            raise APIException('Не верный формат сообщения')
        quote, base, amount = map(str.lower, values)
        res = CurrencyConverter().get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, e)
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду \n {e}')
    else:
        text = f'{amount} {currency[quote]} = {res} {currency[base]}'
        bot.reply_to(message, text)


if __name__ == '__main__':
    bot.polling(none_stop=True)



