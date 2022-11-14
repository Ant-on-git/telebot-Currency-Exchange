import json
import requests
from config import currency


class APIException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(qoute, base, amount):
        if qoute == base:
            raise APIException('Нудно указать разные валюты')

        incorrect_currency = tuple(filter(lambda x: x not in currency, (qoute, base)))
        if incorrect_currency:
            if len(incorrect_currency) == 1:
                raise APIException(f'В настоящее время я не могу обработать валюту {incorrect_currency[0]}')
            else:
                raise APIException(f'В настоящее время я не могу обработать валюты {incorrect_currency[0]} \
                                   и {incorrect_currency[1]}')

        if not amount.replace('.', '', 1).isdigit():
            raise APIException(f'Я не знаю такого значения: {amount}')

        base = currency[base]
        qoute = currency[qoute]
        headers = {'apikey': '43h46lYzEhl7JYBMvVXkVTzeqbaYxZdY'}
        exchange_rate = requests.get(f'https://api.apilayer.com/exchangerates_data/convert?'
                                     f'to={base}&from={qoute}&amount={float(amount)}', headers=headers)
        res = json.loads(exchange_rate.content)['result']
        res = '{:,.2f}'.format(res).replace(',', ' ')
        return res


