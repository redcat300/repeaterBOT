import json
import requests
from config import keys_input

class ConversionException(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(base, quote, amount):
        try:
            base_code = keys_input.get(base.lower())
            quote_code = keys_input.get(quote.lower())

            if not base_code or not quote_code:
                raise ConversionException('Введена неправильная или несуществующая валюта.')

            if base_code == quote_code:
                raise ConversionException('Нельзя переводить одинаковые валюты.')

            url = f'https://v6.exchangerate-api.com/v6/94990ae591c1e0e5036af7ad/pair/{base_code}/{quote_code}'
            response = requests.get(url)

            if response.status_code != 200:
                raise ConversionException(f'Ошибка в запросе к API. Код состояния: {response.status_code}')

            data = response.json()

            if 'conversion_rate' not in data:
                raise ConversionException('Ошибка в ответе API: conversion_rate не найден')

            if float(amount) < 0:
                raise ConversionException('Количество не может быть меньше 0')

            amount = float(amount)

            converted_amount = amount * data['conversion_rate']
            return converted_amount

        except ValueError:
            raise ConversionException(f'Не удалось обработать количество {amount}')
