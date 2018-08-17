# -*- coding: utf-8 -*-
import scrapy
import requests 
from bs4 import BeautifulSoup
import logging
log = logging.getLogger('scrapy.proxies')
class ProxySpider(scrapy.Spider):
    name = 'proxy'
    allowed_domains = ['www.us-proxy.orgt']
    start_urls = ['https://www.us-proxy.org']
    proxies = []
    def parse(self, response):
        response = requests.get('https://www.us-proxy.org/')
        soup = BeautifulSoup(response.content, 'lxml')
        trs = soup.select("#proxylisttable tr")
        
        for tr in trs:
            tr_soup = BeautifulSoup(str(tr), 'lxml')
            tds = tr_soup.select("td")
            if len(tds) > 4:
                addr = tds[0].text
                port = tds[1].text
                anonymity = tds[4].text
                proxy_ip = "http://{0}:{1}".format(addr, port)
                if anonymity != 'anonymous': 
                    self.proxies.append(proxy_ip)
        log.info('Using proxy <%s>, %d proxies left' % (self.proxies[0], len(self.proxies)))
                