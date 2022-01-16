import json
import requests
from config import keys

class APIException(Exception):
    pass

class ConvertValues:
    @staticmethod
    def get_price(amount: str, quote: str, base: str):
        if quote == base:
            raise APIException('Введены одинаковые валюты')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать колличество. "{amount}"')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту "{quote}"')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту "{base}"')


        r = requests.get(
            f'https://freecurrencyapi.net/api/v2/latest?apikey=0bc89fc0-6e5c-11ec-bc0f-55a46559fa41&base_currency={quote_ticker}')
        total_base = json.loads(r.content)['data']
        total_res = round(total_base.get(keys[base]) * amount, 2)
        return total_res

