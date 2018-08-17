# -*- coding: utf-8 -*-
import scrapy
import random
from scrapy_splash import SplashRequest
from bs4 import BeautifulSoup
from ..items import SpidertestingItem
# from spiderTesting.items import SpidertestingItem

class AdidasSpider(scrapy.Spider):
    name = 'adidas'
    meta = {}
    allowed_domains = ['www.adidas.com']
    start_urls = ['https://www.adidas.com/us/men-new_arrivals',
                  'https://www.adidas.com/us/women-new_arrivals']
    product_links = []
    def parse(self, response):
        # print('url', response.url)
        soup = BeautifulSoup(response.text, "lxml")
        results = soup.select('a.product-images-js')
        for product in results:
            # print(product)
            if 'shoes' not in product['href']:
                self.product_links.append('https://www.adidas.com' + product['href'])
                print(product['href'])
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
        Item = SpidertestingItem()
        soup = BeautifulSoup(response.body,'lxml')
        tmp = response.url.split('/')
        Item['Size'] = []
        sizes = soup.select('div.gl-square-list__cta')
        for size in sizes:
            size = size.get_text()
            Item['Size'].append(size)
        Item['StyleNumber'] = tmp[len(tmp)-1].split('.')[0]
        Item['Description'] = soup.select('div.wrapper___1HYKp > p')[0].text
        Item['Name'] = soup.select('h1.product_title')[0].text
        Item['Brand'] = "adidas"
        Item['MinPrice'] = soup.select('span.gl-price')[0].text
        Item['MaxPrice'] = soup.select('span.gl-price')[0].text
        Item['Gender'] = soup.select('a.gl-link > span')[1].text
        Colortmp = soup.select('div.gl-vspacing-l > div.color_text___mgoYV')[0].text
        Color = Colortmp.split('/')
        Item['Color'] = Color
        Item['Url'] = response.url
        imgUrl = soup.select('img.performance-item')[0]
        Item['ImageUrl'] = imgUrl['src']
        Materialtmp = soup.select('li.gl-vspacing-m')
        
        materials=[]
        for i in Materialtmp:
            materials.append(i.text)
        Item['Material'] = materials
        try:
            reviewNumber = soup.select('div.product_reviews___IhPrB > span > a')[0].text
            Item['ReviewNumber'] = reviewNumber
        except:
            Item['ReviewNumber'] = 0

        try:
            bh4 = soup.select('div.wrapper___1HYKp > h4')[0].text
            bh5 = soup.select('div.wrapper___1HYKp > h5')[0].text
            Item['Bullets'] = [bh4,bh5]
        except:
            Item['Bullets'] = materials
        
        try:
            averageRating = soup.select('h4.number_rating___ehhcp')[0].text
            Item['AverageRating'] = averageRating
        except:
            Item['AverageRating'] = 0
        # print(Item)
        return Item
        