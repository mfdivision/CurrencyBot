import requests
import json

# это функция для конвертирования валют
def get_price(base, quote, amount):
    r = requests.get(
        f'https://api.getgeoapi.com/v2/currency/convert?api_key=0b6645ae10336e7a654786b7d9597eefd3cb48c1&from={base}&to={quote}&amount={amount}&format=json')
    answer = (round(float(json.loads(r.content)['rates'][f'{quote}']['rate_for_amount']), 2))

    return answer

# это функция для получения списка доступных валют на сервере
def get_curr_names():
    r = requests.get('https://api.getgeoapi.com/v2/currency/convert?api_key=0b6645ae10336e7a654786b7d9597eefd3cb48c1')

    q = json.loads(r.content)['rates'].keys()
    return q
