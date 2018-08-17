import scrapy
import requests
from scrapy_splash import SplashRequest
from bs4 import BeautifulSoup
from scrapy import Selector
import requests
import time
class AmazonSpider(scrapy.Spider):
    name = 'as'
    allowed_domains = ['www.amazon.com']
    meta = {}
    start_urls = ['https://www.amazon.com/Best-Sellers-Sports-Outdoors-Mens-Shirts/zgbs/sporting-goods/11444073011']
    hrefs = []

    def parse(self, response):
        print(response.url)
        soup = BeautifulSoup(response.text, "lxml")
        page_number = soup.select('ul.a-pagination > li.a-normal')[0].text
        
        for i in range(1,int(page_number)+1):
            print("=================================== Page " + str(i) + "===================================")
            url = str(response.url)
            print(url)
            get_html = requests.get(url)
            soup = BeautifulSoup(get_html.text,"lxml")
            links = soup.select("li.zg-item-immersion")
            for item in links:
                hrefs_tmp = item.find("a").attrs["href"]
                self.hrefs.append(hrefs_tmp)
            print(self.hrefs) 

        for link in self.hrefs:
            product_url = 'https://www.amazon.com' + link
            self.meta['Url'] = product_url
            print("==================" + product_url + "==================")

            self.parse_product_link(product_url)
            
    def parse_product_link(self,product_href):
        get_html = requests.get(product_href)
        soup = BeautifulSoup(get_html.text,"html.parser")

        StyleNumber_code = soup.select('div#detailBullets_feature_div > ul > li > span')
        if (len(StyleNumber_code)== 5):
            catch_ASIN = StyleNumber_code[2].text
            split_tag = catch_ASIN.split("ASIN:\n")[1]
            StyleNumber = split_tag.split("\n")[1]
        elif (len(StyleNumber_code) == 6):
            catch_model_number = StyleNumber_code[4].text
            split_tag = catch_model_number.split("Item model number:\n")[1]
            StyleNumber = split_tag.split("\n")[1]
        elif (StyleNumber_code == []):
            StyleNumber_code = soup.select('div.content > ul > li')
            tmp = StyleNumber_code[1].text
            StyleNumber = tmp.split(": ")[1]
        meta['StyleNumber'] = StyleNumber


        Bullets_tmp = soup.select('div#feature-bullets > ul.a-unordered-list > li > span')
        Bullets = []
        for i in Bullets_tmp:
            tmp = i.text.split("\n\t\t\t\t\t\t\t")[1]
            Bullets.append(tmp)
        meta['Bullets'] = Bullets

        try:
            Description = soup.select('div#productDescription > p')[0].text
            Description = Description.split("\n")[0]
            meta['Description'] = Description
        except:
            meta['Description'] = 'None'

        Name = soup.select('span#productTitle')[0].text
        Name = Name.split("\n")[9].replace(' ','')
        meta['Name'] = Name

        meta['Brand'] = 'Amazon'

        price = soup.select('span#priceblock_ourprice')[0].text
        price = price.split(" - ")
        meta['MinPrice'] = price[0]
        meta['MaxsPrice'] = price[1]

        Gender = soup.select('li.zg_hrsr_item > span.zg_hrsr_ladder > a')
        for i in Gender:
            a = i.text
            if a == 'Men' or a == 'Women':
                meta['Gender'] = a

        Color = soup.select('ul.a-unordered-list')
        for item in Color:
            a = item.select('li.swatchSelect')
            for i in a:
                Color = i['title']
        Color = Color.split('Click to select ')[1]
        meta['Color'] = Color

        size_option = soup.select('span.a-dropdown-container')
        Size = []
        for S_index in size_option:
            S_index = S_index.text.replace(' ','')
        S_tmp = S_index.split("\n")
        for item in S_tmp:
            if item != "" and item != "Select":
                Size.append(item)

        meta['Size'] = Size

        meta['Sport'] = []

        meta['Clothing'] = []

        meta['Material'] = Bullets[0]

        meta['Feature'] = []

        AverageRating = soup.select('span.arp-rating-out-of-text')[0].text
        meta['AverageRating'] = AverageRating[0:3]

        ReveiwNumber = soup.select('span#acrCustomerReviewText')[0].text
        ReveiwNumber = ReveiwNumber.split(' customer reviews')[0]
        meta['ReveiwNumber'] = ReveiwNumber

        ImageUrl = soup.select('div.imgTagWrapper')
        Imagetmp=''
        for item in ImageUrl:
            Imagetmp = item.find("img").attrs['data-a-dynamic-image']
            break   
        Imagetmp = Imagetmp.split(',')[0].replace('"','')
        Imagetmp = Imagetmp.replace('{','')
        ImageUrl = Imagetmp.split(':[')[0]
        meta['ImageUrl'] = ImageUrl

        meta['Url'] = 'https://www.amazon.com' + hrefs[1]

        localtime = time.asctime(time.localtime(time.time()))
        meta['localtime'] = localtime

        print(self.meta)
