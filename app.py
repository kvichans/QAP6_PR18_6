import telebot
from config import keys, TOKEN
from extensions import ConvertionException, PriceHelper


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])  # обработчик команд start и help
def help(message: telebot.types.Message):
    text = '''
Чтобы начать работу, введите команду боту в следующем формате:
    <есть> <нужно> [<объем>]
где
    <есть> - имя исходной валюты 
    <нужно> - в какую валюту перевести
    <объем> - количество исходной валюты
Имена валют можно вводить не полностью,
а первые три символа.

Чтобы увидеть доступные валюты введите: 
    /values
'''
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])  # обработчик команды values - какие валюты доступны
def values(message: telebot.types.Message):
    text = 'Доступные валюты:\n  ' + '\n  '.join(
        f'{key[:3]}[{key[3:]}]' for key in keys
    )
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])  # обработчик конвертации валют
def convert(message: telebot.types.Message):
    print(f'convert: in={message.text}')
    values = message.text.split()
    # Проверяем, что пользователь ввёл 2 или 3 необходимых параметра
    if not(len(values) in (2, 3)):
        return bot.reply_to(message, 'Неверное количество параметров\nДля получения справки введите /help')
    quote, base = values[0], values[1]
    amount = values[2] if len(values)==3 else '1'

    try:
        total_base = PriceHelper.get_price(quote, base, amount)
    except ConvertionException as e:
        print(f'convert: err={e}')
        return bot.reply_to(message, f'{e}')
    except Exception as e:
        return bot.reply_to(message, f'Не удалось обработать команду \n {e}')

    # Итоговый вывод конвертации
    text = f'Цена {amount} {quote} в {base} - {total_base}' \
            if amount != '1' else \
           f'Цена {quote} в {base} - {total_base}'
    print(f'convert: out={text}')
    bot.send_message(message.chat.id, text)


bot.polling()
