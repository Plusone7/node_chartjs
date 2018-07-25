# -*- coding: utf-8 -*-
import scrapy
import random
from scrapy_splash import SplashRequest
from bs4 import BeautifulSoup
# from spiderTesting.items import SpidertestingItem

class ArcteryxSpider(scrapy.Spider):
    all_product_hrefs = []
    name = 'arcteryx'
    allowed_domains = ['arcteryx.com']
    start_urls = ['https://arcteryx.com/us/en/c/mens/what-s-new',
                  'https://arcteryx.com/us/en/c/womens/what-s-new']
    product_links = []
    def parse(self, response):  
        # SplashRequest(response.url, self.get_all_product_hrefs, endpoint='render.html', args={'har':1, 'html':1, 'wait':10})
        # soup = BeautifulSoup(response.text, "lxml")
        # links = soup.select('div.product-tile-inner')
        # print(links)
        print(response.url)
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
        
        # next_page = response.xpath('//li[@class="right-arrow"]/a/@href').extract_first()
        # yield scrapy.Request(next_page, callback = self.parse, dont_filter = True)

    def parse_product_link(self, response):
        print(response.url)
        
    def get_all_product_hrefs(self, response):
        count = 1
        soup = BeautifulSoup(response.text, "lxml")
        links = soup.select('div.product-tile-inner > a.product-tile__product-link')
        for idx in range(0, len(links), 2):
            # print(links[idx]['href'])
            url = 'https://arcteryx.com' + links[idx]['href']
            # self.all_product_hrefs.append(links[idx]['href'])
            # print(url)
            yield SplashRequest(
                url,
                self.parse_product_link,
                endpoint='render.html',
                args={
                    'har': 1,
                    'html': 1,
                    'wait':10,
                }
            )

    
        
