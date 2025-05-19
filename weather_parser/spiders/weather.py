import scrapy
from scrapy.http import  HtmlResponse


class WeatherSpider(scrapy.Spider):
    name = "weather"
    allowed_domains = ["pogodaiklimat.ru"]
    start_urls = ["http://www.pogodaiklimat.ru/archive.php"]

    def parse(self, response):
        print(response.status)
        print('**********************')
        print(response.url)

