from typing import Union
from bs4 import BeautifulSoup
import cloudscraper
import json
from transliterate import translit


class Parser:
    RUBLE_SYMBOL = "₽"

    def __init__(self, minprice: int = 0, maxprice: int = 0, region: str = "Москва", rooms: str = "1-6", page: int = 1):
        self.rooms = rooms
        self.min_price = minprice
        self.max_price = maxprice
        self.region = region
        self.page = page
        self.session = cloudscraper.create_scraper()
        self.session.headers = {'Accept-Language': 'en'}
        self.offers = []

    def get_phone_number(self, link: str) -> Union[str, None]:

        results = self.session.get(url=link)
        results = results.text
        offer_page = BeautifulSoup(results, "lxml")
        try:
            contact_data = offer_page.select("div[data-name='OfferContactsAside']")[0].text
            return contact_data[:16]
        except Exception:
            return None

    def get_rooms_count(self, text: str) -> int:
        if "1-комн" in text or "1-к" in text:
            rooms_count = 1
        elif "2-комн" in text or "2-к" in text:
            rooms_count = 2
        elif "3-комн" in text or "3-к" in text:
            rooms_count = 3
        elif "4-комн" in text or "4-к" in text:
            rooms_count = 4
        elif "5-комн" in text or "5-к" in text:
            rooms_count = 5
        else:
            rooms_count = -1

        return rooms_count

    def get_price(self, offer: BeautifulSoup) -> int:
        price = -1
        elements = offer.select("div[data-name='LinkArea']")[0].select(
            "div[data-name='GeneralInfoSectionRowComponent']"
        )
        for element in elements:
            if self.RUBLE_SYMBOL in element.text:
                price_description = element.text
                price = int("".join(price_description[: price_description.find(self.RUBLE_SYMBOL) - 1].split()))
        return price

    def parse_listing(self, offer):
        offer_info = dict()
        offer_info["link"] = offer.select("div[data-name='LinkArea']")[0].select("a")[0].get("href")
        offer_info["price"] = self.get_price(offer)
        offer_info["rooms"] = self.get_rooms_count(offer.text)
        offer_info["city"] = translit(self.region.capitalize(), "ru", reversed=True)
        offer_info["phone"] = self.get_phone_number(offer_info["link"])
        self.offers.append(offer_info)

    def start_session(self) -> list:
        cities = {'Абакан': '4628', 'Анадырь': '4634', 'Анапа': '5129', 'Архангельск': '4557', 'Астрахань': '4558',
                  'Барнаул': '4555', 'Белгород': '4561', 'Биробиджан': '4569', 'Благовещенск': '4556',
                  'Бронницы': '4690', 'Брянск': '4562', 'Видный': '5922', 'Владивосток': '4604', 'Владикавказ': '4613',
                  'Владимир': '4564', 'Волгоград': '4565', 'Вологда': '4566', 'Волоколамск': '5379', 'Воронеж': '4567',
                  'Воскресенск': '5388', 'Геленджик': '4717', 'Горно-Алтайск': '4554', 'Грозный': '4631',
                  'Дзержинский': '4734', 'Дмитров': '5482', 'Долгопрудный': '4738', 'Дубна': '4741',
                  'Екатеринбург': '4612', 'Жуковский': '4750', 'Звенигород': '4756', 'Иванов': '4570', 'Ижевск': '4624',
                  'Иркутск': '4572', 'Йошкар-Ола': '4591', 'Казань': '4618', 'Калининград': '4574', 'Калуга': '4576',
                  'Кемерово': '4580', 'Киров': '4581', 'Коломна': '4809', 'Королёв': '4813', 'Кострома': '4583',
                  'Красноармейск': '4817', 'Краснодар': '4584', 'Краснознаменск': '4822', 'Красноярск': '4585',
                  'Курган': '4586', 'Курск': '4587', 'Кызыл': '4622', 'Липецк': '4589', 'Лобня': '4848',
                  'Лыткарино': '4851', 'Магадан': '4590', 'Майкоп': '4553', 'Махачкала': '4568', 'Москва': '1',
                  'Мурманск': '4594', 'Назрань': '4571', 'Нальчик': '4573', 'Нарьян-Мар': '4595', 'Новгород': '4596',
                  'Новороссийск': '4896', 'Новосибирск': '4598', 'Омск': '4599', 'Оренбург': '4600',
                  'Орехово-Зуево': '4916', 'Орёл': '4601', 'Пенза': '4602', 'Пермь': '4603', 'Петрозаводск': '4579',
                  'Петропавловск-Камчатский': '4577', 'Подольск': '4935', 'Протвино': '4945', 'Псков': '4605',
                  'Пущино': '4949', 'Реутов': '4958', 'Ростов-На-Дону': '4606', 'Рошаль': '4960', 'Рязань': '4607',
                  'Салехард': '4635', 'Самара': '4608', 'Санкт-Петербург': '2', 'Саранск': '4592', 'Саратов': '4609',
                  'Серпухов': '4983', 'Смоленск': '4614', 'Сочи': '4998', 'Ставрополь': '4615', 'Сургут': '5003',
                  'Сыктывкар': '4582', 'Тамбов': '4617', 'Тверь': '4619', 'Тольятти': '5015', 'Томск': '4620',
                  'Тула': '4621', 'Тюмень': '4623', 'Улан-Удэ': '4563', 'Ульяновск': '4625', 'Уфа': '4560',
                  'Фрязино': '5038', 'Хабаровск': '4627', 'Ханты-Мансийск': '4629', 'Химки': '5044',
                  'Чебоксары': '4633', 'Челябинск': '4630', 'Череповец': '5050', 'Черкесск': '4578', 'Чита': '4720',
                  'Электросталь': '5064', 'Элиста': '4575', 'Южно-Сахалинск': '4611', 'Якутск': '4610',
                  'Ярославль': '4636'}
        try:
            link = "https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p={}" + \
                   f"&region={cities[self.region.title()]}"""
            if 0 >= int(self.rooms) or int(self.rooms) > 6:
                raise TypeError
        except KeyError:
            raise NameError
        except ValueError:
            if 0 >= int(self.rooms[0]) > 6 or 0 >= int(self.rooms[-1]) > 6:
                raise TypeError

        if len(self.rooms) == 3:
            for i in range(int(self.rooms[0]), int(self.rooms[-1]) + 1):
                link += f"&room{i}=1"
        else:
            link += f"&room{int(self.rooms)}=1"

        if self.min_price and self.max_price and self.min_price < self.max_price:
            link += f"&minprice={self.min_price}" + f"&maxprice={self.max_price}"
        elif self.min_price:
            link += f"&minprice={self.min_price}"
        elif self.max_price:
            link += f"&maxprice={self.max_price}"

        search_page = self.session.get(link.format(self.page))
        search_page = search_page.text
        search_page = BeautifulSoup(search_page, 'lxml')
        offers = search_page.select("article[data-name='CardComponent']")

        for ind, blocks in enumerate(offers):
            self.parse_listing(offer=blocks)

        return self.offers


def start(username: str, minprice: int, maxprice: int, pages: int, region: str = "Москва", rooms: str = "1-6", ):
    with open(f'files/{username}.json', 'w') as file:
        result = []
        for i in range(1, pages + 1):
            request = Parser(region=region, rooms=rooms, page=i, minprice=minprice, maxprice=maxprice)
            result += request.start_session()
            print(i, "OK")
        json.dump(result, file)
    return True
