import scrapy
from scrapy.http import  HtmlResponse
from pprint import pprint
from urllib.parse import urljoin
import csv


class WeatherSpider(scrapy.Spider):
    name = "weather"
    allowed_domains = ["world-weather.ru"]
    start_urls = ["https://world-weather.ru/pogoda/"]

    cities = ["Москва"]

    month_year = 'april-2025'


    def create_csv_file(self, filename):
        """ Создание пустого CSV-файла с заданными заголовками """
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Дата', 'Локация', 'Температура', 'Осадки'])

    def append_to_csv(self, filename, row_data):
        """ Добавление записи в конец существующего CSV-файла """
        print('row_data: ', row_data)
        with open(filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(row_data)

    def clear_csv_content(self,filename):
        """ Полная очистка содержимого CSV-файла"""
        self.create_csv_file(filename)


    def parse(self, response:HtmlResponse):

        self.create_csv_file('weather_data.csv')
        for city in self.cities:
            # Выбираем элемент input по указанному XPath
            xpath_input_field = '/html/body/div[1]/div[1]/div[2]/form/input[1]'
            field_value = response.xpath(xpath_input_field).attrib['name']  # Получаем имя атрибута элемента

            # Отправляем запрос, заполнив поле поиска
            yield scrapy.FormRequest.from_response(response,
                formxpath=xpath_input_field,  # Используем XPath для нахождения формы
                formdata={
                    field_value: city  # Устанавливаем выбранное значение
                },
                callback=self.parse_results_page
            )

    def parse_results_page(self, response:HtmlResponse):
        """Функция для парсинга страниц с результатами поиска"""
        list_absolut_urls = [] # Список url результатов поиска
        list_name_location = [] # Списко названий локаций

        links = response.xpath(f'/html/body/div[1]/div[2]/div[1]/ul[2]/li/a/@href').getall()

        # Формируею список всех результатов поиска
        for i in links:
            list_name_location.append(i.split('/')[-2])
            list_absolut_urls.append('https://'+i+self.month_year)


        for i in range(len(list_absolut_urls)):
            yield scrapy.Request(list_absolut_urls[i], meta= {'name_location':list_name_location[i]},callback=self.parse_station_page)

        return scrapy.Request(url=self.start_urls[0], dont_filter=True)

    def parse_station_page(self, response):
        name_location = response.meta['name_location']
        print('____________')
        print(name_location)

        # Эта строка определяет погоду по дням
        temp_days = response.xpath(f'/html/body/div[1]/div[2]/div[1]/ul[3]/li/a/span/text()').getall() # Температура по дням
        precipitation_days = response.xpath(f'/html/body/div[1]/div[2]/div[1]/ul[3]/li/a/i/@title').getall() # Осадки по дням
        print(temp_days)
        print(precipitation_days)

        # Сохраняю данные в файлы
        for i in range(len(temp_days)):
            list_weather = [f"{i}-{self.month_year}", name_location, temp_days[i], precipitation_days[i]]
            self.append_to_csv("weather_data.csv", list_weather)






        # #Провожу Get запрос
        # for link in links:
        #     yield response.follow(link, callback=self.weather_parse)
        #
        # # print(response.follow(link), type(response.follow(link)))


