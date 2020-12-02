import requests
import json
from config import keys, keys3


class ConvertionException(Exception):  # создали свой класс обработки исключений (ошибок ввода)
    pass


class PriceHelper:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        try:
            amount = float(amount)
        except ValueError:  # проверка, что количество валюты ввели цифрами
            raise ConvertionException(f'Неудачный объем: {amount}')
        if quote[:3] not in keys3:
            raise ConvertionException(f'Неизвестная исходная валюта: {quote}')
        if base[:3] not in keys3:
            raise ConvertionException(f'Неизвестная валюта: {base}')

        if quote == base:
            return amount
        quote_ticker = keys3[quote[:3]]
        base_ticker = keys3[base[:3]]

        response = requests.get(
            f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}'
        )

        total_base = json.loads(response.content)[base_ticker]
        return round(amount * total_base, 5)
