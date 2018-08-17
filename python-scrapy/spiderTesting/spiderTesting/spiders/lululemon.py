# -*- coding: utf-8 -*-
import scrapy
import requests
from scrapy_splash import SplashRequest
from bs4 import BeautifulSoup
from scrapy import Selector
import requests
import json
# from spiderTesting.items import SpidertestingItem
class AdidasSpider(scrapy.Spider):
    api_url = 'ttps://shop.lululemon.com/api'
    name = 'lululemon'
    meta = {}
    allowed_domains = ['www.lululemon.com']
    start_urls = ['https://shop.lululemon.com/c/women-top',
                   'https://shop.lululemon.com/c/women-bottoms']
    product_links = []
    def parse(self, response):
        print(response.url)
        soup = BeautifulSoup(response.text, "lxml")
        page_number = int(soup.select('p.results')[0].text.replace(' items',''))
        
 #       print('lululemon Total Page :' int((page_number/9)+1) )
 #       print('Please wait.......')
        for i in range(1, int((page_number/9)+1)):
            url = str(response.url) + '?page=' + str(i)
            r = requests.get(url)
            soup = BeautifulSoup(r.text, "lxml")
            results = soup.select('div.swiper-wrapper > a.swiper-slide')
            for product in results:
                self.product_links.append(product['href'])
        self.product_links = list(set(self.product_links))        
        print(len(self.product_links))

        for link in self.product_links:
            product_url = 'https://shop.lululemon.com/api' + link
            self.meta['Url'] = 'https://shop.lululemon.com' + link
            self.parse_product_link(product_url)
            
    def parse_product_link(self, product_api):
        r = requests.get(product_api)
        products_json = json.loads(r.text)
        attributes = products_json['data']['attributes']['product-attributes']['product-content-feature']
        summary = products_json['data']['attributes']['product-summary']
        self.meta['Name'] = summary['title']
        self.meta['Size'] = summary['product-sizes']
        self.meta['Clonthing'] = summary['product-category']
        self.meta['Gender'] = summary['gender']
        self.meta['Brand'] = self.name
        self.meta['StyleNumber'] = summary['repository-id'][4:]
        self.meta['MaxPrice'] = summary['price']
        try:
            self.meta['Material'] = products_json['data']['attributes']['product-attributes']['product-content-fabric'][0]['fabricDescription']
        except:
            self.meta['Material'] = []
        try:
            self.meta['MinPrice'] = summary['product-sale-price']
        except:
            self.meta['MinPrice'] = self.meta['MaxPrice']
        self.meta['Description'] = summary['why-we-made-this']
        colors = summary['color-group']
        self.meta['Color']=[]
        for color in colors:
            self.meta['Color'].append(color['name'])
        if attributes:
            self.meta['Sport'] = attributes[0]['f5Features']
            self.meta['Feature'] =[]
            for f in attributes[0]['f5Features'][-2:]:
                self.meta['Feature'].append(f['featureName'])
        
        print(self.meta)
    

           
        
