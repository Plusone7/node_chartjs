# -*- coding: utf-8 -*-
import scrapy
import random
from scrapy_splash import SplashRequest
from bs4 import BeautifulSoup
# from spiderTesting.items import SpidertestingItem

class AdidasSpider(scrapy.Spider):
    name = 'adidas'
    meta = {}
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
        tmp = response.url.split('/')
        self.meta['StyleNumber'] = tmp[len(tmp)-1].split('.')[0]
        bh4 = soup.select('div.wrapper___1HYKp > h4')[0].text
        bh5 = soup.select('div.wrapper___1HYKp > h5')[0].text
        Bullets = [bh4,bh5]
        self.meta['Bullets'] = Bullets
        self.meta['Description'] = soup.select('div.wrapper___1HYKp > p')[0].text
        self.meta['Name'] = soup.select('h1.product_title')[0].text
        self.meta['Brand'] = "adidas"
        self.meta['MinPrice'] = soup.select('span.gl-price')[0].text
        self.meta['MaxPrice'] = soup.select('span.gl-price')[0].text
        self.meta['Gender'] = soup.select('a.gl-link > span')[1].text
        Colortmp = soup.select('div.gl-vspacing-l > div.color_text___mgoYV')[0].text
        Color = Colortmp.split('/')
        self.meta['Color'] = Color
        Materialtmp = soup.select('li.gl-vspacing-m')
        Material=[]
        for i in Materialtmp:
            Material.append(i.text)
        self.meta['Material'] = Material
        try:
             # [ <a class="gl-hidden-l gl-link gl-body--small gl-no-margin-bottom">3</a>, 
             #   <a class="gl-hidden-s-m gl-link gl-body--small gl-no-margin-bottom"> Read all 3 reviews</a> ]
            ReviewNumber = soup.select('div.product_reviews___IhPrB > span > a')[0].text
            self.meta['ReviewNumber'] = ReviewNumber
        except:
            self.meta['ReviewNumber'] = 0
           
        