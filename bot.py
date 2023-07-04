import telebot
from telebot import types
from sub2 import find_price
from request import get_price, get_curr_names
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

e = None
controller = None


class APIExeptions(Exception):
    pass


class Buttons():
    # кнопки для выбора источников котировок на старте
    @staticmethod
    def source_choise():
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('Парсим сайт ALPARI', callback_data='alpari')
        btn2 = types.InlineKeyboardButton('Запрос через API', callback_data='api')
        markup.add(btn1, btn2)
        return markup

    # кнопки выбора валюты в парсере
    @staticmethod
    def alpari():
        markup2 = types.InlineKeyboardMarkup(row_width=3)
        btn1 = types.InlineKeyboardButton('Курс Евро', callback_data='euro')
        btn2 = types.InlineKeyboardButton('Курс Доллара', callback_data='bucks')
        btn3 = types.InlineKeyboardButton('Курс Тенге', callback_data='tenge')
        markup2.add(btn1, btn2, btn3)
        return markup2

    # здесь обрабатываем нажатие кнопок - берём соответсвующий адрес страницы и отправляем в парсер.
    def alpari_scrap(callback):
        global e  # помню комментарий про глобальные переменные. Но пока не хватает опыта решиить по-другому.
        if callback.data == 'euro':
            url = 'https://alpari-online.com/ru/markets/cbr/kurs-eur-euro/'
            currency = 'Евро'

        elif callback.data == 'bucks':
            url = 'https://alpari-online.com/ru/markets/cbr/kurs-usd-dollar-usa/'
            currency = 'Доллар'

        elif callback.data == 'tenge':
            url = 'https://alpari-online.com/ru/markets/cbr/kurs-kzt-kazahskij-tenge/'
            currency = 'Тенге'

        e = find_price(url)
        bot.send_message(callback.message.chat.id, f'Текущий курс за 1 {currency} = {e} руб.')


# на старте предлагаем варианты источников котировок
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     """Бот может спарсить котировку с сайта "alpari-online" или сделать запрос"""
                     """ через API. Что выберем?""",
                     reply_markup=Buttons.source_choise())


# диспетчер слушает callback и отправляет в соответствующие ветки сценария.
@bot.callback_query_handler(func=lambda call: True)
def call_query(call):
    global controller
    if call.message:

        if call.data == 'alpari':
            bot.send_message(call.message.chat.id, "Отлично. Теперь выбираем валюту:", reply_markup=Buttons.alpari())

        if call.data == 'euro' or call.data == 'bucks' or call.data == 'tenge':
            controller = 2
            bot.send_message(call.message.chat.id, text=f'Введите сумму в выбранной валюте :',
                             reply_markup=Buttons.alpari_scrap(call))

        if call.data == 'api':
            controller = 3
            bot.send_message(call.message.chat.id, text=f'Ок, запрос по API.\n Введите коды базовой и котировальной '
                                                        f'валют и количество через пробел.\n'
                                                        f'Например: rub usd 1')

        # Подтверждаем серверу телеграм, что обработали нажатие кнопки
    bot.answer_callback_query(callback_query_id=call.id, show_alert=False)



# проверка ошибок и вывод результатов для обоих источников.
# для парсера делаем запрос к get_curr_names(), чтобы получить словарь всех доступных валют. Свой список, как в
# примере на видео в модуле проще и быстрее, но из спортивного интереса хотелось решить этот вопрос именно так))

@bot.message_handler(content_types=['text'])
def calculator(message):
    if controller == 3:
        try:
            quote, base, amount = message.text.upper().split(' ')
        except ValueError:
            bot.send_message(message.chat.id, 'Введите корректные значения')
            # закомментировал вызов своего исключения, так как при отлове ошибки выполнение скрипта прекращается
            # raise APIExeptions('Неправильные значения')
            return
        try:
            amount = float(amount)
        except ValueError:
            bot.send_message(message.chat.id, 'Введите корректное значение количества')
            return
        try:
            quote, base in get_curr_names()
            bot.send_message(message.chat.id, f'Получается {get_price(base, quote, amount)}  в {quote}')
        except:
            bot.send_message(message.chat.id, 'Введите корректные значения валют')
            return

    elif controller == 2:
        global e
        try:
            amount = float(message.text.strip())
        except ValueError:
            bot.send_message(message.chat.id, 'Введите корректное количество')
            return
        total_ = round(float(e) * amount, 2)
        bot.send_message(message.chat.id, f'{total_} рублей')

    bot.send_message(message.chat.id, f'Можем повторить ))\nИли можно вернуться к началу ➡️ /start')


bot.polling(none_stop=True)
