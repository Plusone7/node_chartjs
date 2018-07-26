# -*- coding: utf-8 -*-
import scrapy
import random
from scrapy_splash import SplashRequest
from bs4 import BeautifulSoup
from scrapy import Selector
# from spiderTesting.items import SpidertestingItem

class ArcteryxSpider(scrapy.Spider):
    meta = {}
    name = 'arcteryx'
    allowed_domains = ['arcteryx.com']
    start_urls = ['https://arcteryx.com/us/en/c/mens/what-s-new',
                  'https://arcteryx.com/us/en/c/womens/what-s-new']
    product_links = []
    def parse(self, response):  
        # print(response.url)
        yield SplashRequest(
            response.url,
            self.get_all_product_hrefs,
            endpoint='render.html',
            args={
                'har': 1,
                'html': 1,
                'wait':10,
            }
        )

    def get_all_product_hrefs(self, response):
        count = 1
        soup = BeautifulSoup(response.text, "lxml")
        links = soup.select('div.product-tile-inner > a.product-tile__product-link')
        for idx in range(0, len(links), 2):
            url = 'https://arcteryx.com' + links[idx]['href']
            yield SplashRequest(
                url,
                self.parse_product_link,
                endpoint='render.html',
                args={
                    'har': 1,
                    'html': 1,
                    'wait':5,
                }
            )

    def parse_product_link(self, response):
        sel = Selector(text=response.text, type="html")
        print(response.url)
        Colors =[]
        Bulletstmp = []
        soup = BeautifulSoup(response.text, "lxml")
        StyleNumeber = soup.select('div.product-sizing-chart > span')[1].text
        B = soup.select('div.product__short-description > p')[0].text
        Bulletstmp.append(B)
        # Descriptiontmp = soup.select('div.product__description')

        # Color = soup.select('div.product-colour__thumbnail-container__name > span')
        Color = sel.xpath('//div[@class="product-colour__thumbnail-container__name"]/span/text()').extract()
        print(Color)
        # for i in Color:
        #     Colors.append(i.text)
                
        # product_tag = soup.select('div.product__key-features__item > h3')
        # product_tag_content = soup.select('div.product__key-features__item > span')

        # if product_tag[i].text == "Sizes:":
        #         Sizes = product_tag_content[i].text
        #         Size = Sizes.split(',')
                
        # elif product_tag[i].text == "Activity:":
        #         #Sport有\n的問題
        #         Sports = product_tag_content[i].text
        #         Sport = Sports.split('/')
        #         ArcteryxSpider.meta['Sport'] = Sport

        self.meta['StyleNumeber'] = StyleNumeber
        self.meta['Bullets'] = Bulletstmp
        self.meta['Color'] = Colors   
        self.meta['Description'] = sel.xpath('//div[@class="product__description"]/p/text()').extract()
        self.meta['Name'] = soup.select('div.product-name > h1')[0].text
        self.meta['Brand'] = 'Arcteryx'
        self.meta['MinPrice'] = soup.select('span.product-price__value')[0].text
        self.meta['MaxPrice'] = soup.select('span.product-price__value')[0].text
        self.meta['Gender'] = soup.find('a.breadcrumb__list-item-link > span')
        # self.meta['Size'] = Size

        
    

    
        
