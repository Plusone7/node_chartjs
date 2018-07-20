# -*- coding: utf-8 -*-
import scrapy
import random
from scrapy_splash import SplashRequest
from bs4 import BeautifulSoup
# from spiderTesting.items import SpidertestingItem

class AdidasSpider(scrapy.Spider):
    name = 'adidas'
    allowed_domains = ['www.adidas.com']
    start_urls = ['https://www.adidas.com/us/men-new_arrivals',
                  'https://www.adidas.com/us/women-new_arrivals']
    product_links = []
    def parse(self, response):
        print('url :::::::::::', response.url)
        soup = BeautifulSoup(response.text, "lxml")
        results = soup.select('a.product-images-js')
        for product in results:
            self.product_links.append('https://www.adidas.com' + product['href'])
        for link in self.product_links:
            yield SplashRequest(
                link,
                self.parse_product_link,
                endpoint='render.html',
                args={
                    'har': 1,
                    'html': 1,
                    'wait':10,
                }
            )
        next_page = response.xpath('//li[@class="right-arrow"]/a/@href').extract_first()
        yield scrapy.Request(next_page, callback = self.parse, dont_filter = True)

    def parse_product_link(self, response):
        print(response.url)
        soup = BeautifulSoup(response.body,'lxml')
        d = soup.find_all('div',{"class":"wrapper___1HYKp"},'h4')[0].text
        print(d)
        print('-------------------------------')
    
      
