import logging
from telegram.ext import CommandHandler, MessageHandler, filters, Application
import cian_parser


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
TOKEN = 'TOKEN'
application = Application.builder().token(TOKEN).build()
logger = logging.getLogger(__name__)

user_info = {"username": "", "city": "Москва", "rooms": "1-6", "pages": 2, "min_price": 0, "max_price": 0}


async def send_file(update, context):
    print(user_info["username"])

    chat_id = update.message.chat_id

    file_path = f'files/{user_info["username"]}.json'

    with open(file_path, 'rb') as file:
        await context.bot.send_document(chat_id=chat_id, document=file, caption="Готово!")


async def parse(update, context):
    global user_info
    user = update.message.from_user
    username = user.username
    user_info["username"] = username
    await update.message.reply_text("Подождите, ведётся парсинг...")
    try:

        if user_info["city"] == "" and user_info["rooms"] == "":
            cian_parser.start(username=username, pages=user_info["pages"], minprice=user_info["min_price"], maxprice=user_info["max_price"])
        elif user_info["city"] == "":
            cian_parser.start(username=username, pages=user_info["pages"], rooms=user_info["rooms"], minprice=user_info["min_price"], maxprice=user_info["max_price"])
        elif user_info["rooms"] == "":
            cian_parser.start(username=username, pages=user_info["pages"], region=user_info["city"], minprice=user_info["min_price"], maxprice=user_info["max_price"])
        else:
            cian_parser.start(username=username, pages=user_info["pages"], region=user_info["city"], rooms=user_info["rooms"], minprice=user_info["min_price"], maxprice=user_info["max_price"])
        await send_file(update, context)

    except NameError:
        await update.message.reply_text("Вы ввели город которого нет в реестре. Можете попробовать ввести ближайший "
                                        "крупный к вам город.")
    except TypeError as e:
        await update.message.reply_text("Вы ввели недопустимое количество комнат. Введите количество комнат от 1 до 6", e)


async def available_cities(update, context):
    await update.message.reply_text("Вот доступные города:\n"
                                    "Абакан, Анадырь, Анапа, Архангельск, Астрахань, Барнаул, Белгород, Биробиджан, "
                                    "Благовещенск, Бронницы, Брянск, Видный, Владивосток, Владикавказ, Владимир, "
                                    "Волгоград, Вологда, Волоколамск, Воронеж, Воскресенск, Геленджик, Горно-Алтайск, "
                                    "Грозный, Дзержинский, Дмитров, Долгопрудный, Дубна, Екатеринбург, Жуковский, "
                                    "Звенигород, Иванов, Ижевск, Иркутск, Йошкар-Ола, Казань, Калининград, Калуга, "
                                    "Кемерово, Киров, Коломна, Королёв, Кострома, Красноармейск, Краснодар, "
                                    "Краснознаменск, Красноярск, Курган, Курск, Кызыл, Липецк, Лобня, Лыткарино, "
                                    "Магадан, Майкоп, Махачкала, Москва, Мурманск, Назрань, Нальчик, Нарьян-Мар, "
                                    "Новгород, Новороссийск, Новосибирск, Омск, Оренбург, Орехово-Зуево, Орёл, Пенза, "
                                    "Пермь, Петрозаводск, Петропавловск-Камчатский, Подольск, Протвино, Псков, "
                                    "Пущино, Реутов, Ростов-На-Дону, Рошаль, Рязань, Салехард, Самара, "
                                    "Санкт-Петербург, Саранск, Саратов, Серпухов, Смоленск, Сочи, Ставрополь, Сургут, "
                                    "Сыктывкар, Тамбов, Тверь, Тольятти, Томск, Тула, Тюмень, Улан-Удэ, Ульяновск, "
                                    "Уфа, Фрязино, Хабаровск, Ханты-Мансийск, Чебоксары, Челябинск, Череповец, Чита, "
                                    "Щелково, Электросталь, Якутск, Ярославль")


async def settings(update, context):
    await update.message.reply_text(f"Вот твои настройки сейчас:\nГород: {user_info['city']}\n"
                                    f"Комнаты: {user_info['rooms']}\nКоличество страниц: {user_info['pages']}\n"
                                    f"Минимальная цена: {user_info['min_price']}\nМаксимальная цена: "
                                    f"{user_info['max_price']}")


async def start(update, context):
    await update.message.reply_text(
        'Привет! Я бот, написанный для предоставления мною данных о недвижимости с сайта cian.ru, о том как мной '
        'пользоваться в команде /help!')


async def min_price(update, context):
    minprice = context.args[0]
    user_info["min_price"] = minprice
    await update.message.reply_text("Минимальная цена сохранена. Напишите /minprice 0 чтобы сбросить.")


async def max_price(update, context):
    maxprice = context.args[0]
    user_info["max_price"] = maxprice
    await update.message.reply_text("Максимальная цена сохранена. Напишите /maxprice 0 чтобы сбросить.")


async def city(update, context):
    user_info["city"] = context.args[0].title()
    await update.message.reply_text('Ваш город установлен.')


async def rooms(update, context):
    user_info["rooms"] = context.args[0]
    await update.message.reply_text('Ваше желаемое количество комнат установлено. Чтобы сбросить введите /rooms 1-6.')


async def pages(update, context):
    user_info["pages"] = int(context.args[0])
    await update.message.reply_text('Ваше количество страниц установлено.')


async def help(update, context):
    await update.message.reply_text('Для начала тебе нужно задать мне настройки:\n'
                                    '/available - доступные для поиска города\n'
                                    '/city <город> - указываешь город, в котором хочешь посмотреть недвижимость (по '
                                    'умолчанию Москва). Названия городов которые состоят из двух слов нужно писать '
                                    'строго через дефис\n'
                                    '/rooms <количество комнат> - количество комнат, которое хочешь в квартире  \n'
                                    '/pages <целое число> - количество страниц, которое вы хотите получить в итоге '
                                    'парсинга (по умолчанию выводит одну страницу). Не вводите слишком много страниц, '
                                    'а то обработка будет слишком долгой :)\n'
                                    'Возможно поставить фильтр цены:\n'
                                    '/minprice <целое число рублей> - минимальная нужная вам цена.\n '
                                    '/maxprice <целое число рублей> - максимальная нужная вам цена.\n'
                                    '/settings - текущие настройки\n'
                                    'После установки настроек ты можешь запустить парсер командой /parse.\n'
                                    'Получить данные можно в виде json-файла.\n\n'
                                    'Если вам надо вернуть поиск любого количества комнат, введите /rooms 1-6.\n'
                                    'Отключить фильтр цены возможно присвоив ему значение 0\n'
                                    'Пример: /city Анапа\n/rooms 3\n'
                                    'P.S.: если вы введете минимальное значение цены больше максимального - фильтр '
                                    'просто не сработает\n'
                                    'P.S.1: количество комнат строго одна цифра (от 1 до 6)')


async def unknown(update, context):
    await update.message.reply_text('Извините, я не знаю такой команды.')


def main() -> None:
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    application.add_handler(CommandHandler('settings', settings))

    application.add_handler(CommandHandler('available', available_cities))

    application.add_handler(CommandHandler('help', help))

    application.add_handler(CommandHandler('city', city))

    application.add_handler(CommandHandler('pages', pages))

    application.add_handler(CommandHandler('minprice', min_price))

    application.add_handler(CommandHandler('maxprice', max_price))

    application.add_handler(CommandHandler('parse', parse))

    application.add_handler(CommandHandler('rooms', rooms))

    application.add_handler(MessageHandler(filters.COMMAND, unknown))

    application.run_polling()


if __name__ == '__main__':
    main()
