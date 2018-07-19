import scrapy
from scrapy.linkextractors import LinkExtractor

from scrapy_splash import SplashRequest

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["toscrape.com"]
    start_urls = ['http://quotes.toscrape.com/']

    # http_user = 'splash-user'
    # http_pass = 'splash-password'


    def start_requests(self):
            yield SplashRequest(
            url='http://quotes.toscrape.com/js',
            callback=self.parse,
        )
    def parse(self, response):
        for quote in response.css("div.quote"):
            yield {
                'text': quote.css("span.text::text").extract_first(),
                'author': quote.css("small.author::text").extract_first(),
                'tags': quote.css("div.tags > a.tag::text").extract(),
            }
