# -*- coding: utf-8 -*-
import scrapy
import requests
from scrapy_splash import SplashRequest
from bs4 import BeautifulSoup
from scrapy import Selector
import requests
# from spiderTesting.items import SpidertestingItem

class AdidasSpider(scrapy.Spider):
    name = 'lululemon'
    meta = {}
    allowed_domains = ['www.lululemon.com']
    start_urls = ['https://shop.lululemon.com/c/women-top',
                   'https://shop.lululemon.com/c/women-bottoms']
    product_links = []
    def parse(self, response):
        soup = BeautifulSoup(response.text, "lxml")
        page_number = int(soup.select('p.results')[0].text.replace(' items',''))
        for i in range(1, (page_number/9)+1):
            url = str(response.url) + '?page=' + str(i)
            r = requests.get(url)
            print(url)
            soup = BeautifulSoup(r.text, "lxml")
            results = soup.select('div.swiper-wrapper > a.swiper-slide')
            for product in results:
                self.product_links.append(product['href'])
        self.product_links = list(set(self.product_links))
        print(len(self.product_links))
        
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
    
    def parse_product_link(self, response):
        print(response.url)
        soup = BeautifulSoup(response.body,'lxml')
    

           
        