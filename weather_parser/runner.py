from scrapy.crawler import CrawlerProcess
from scrapy.utils.reactor import install_reactor
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from weather_parser.spiders.weather import WeatherSpider

if __name__ == '__main__':
    configure_logging()
    # install_reactor()
    process = CrawlerProcess(get_project_settings())
    process.crawl(WeatherSpider)
    process.start()