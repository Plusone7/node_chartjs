# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpidertestingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    StyleNumber = scrapy.Field()
    Size = scrapy.Field()
    Bullets = scrapy.Field()
    Description = scrapy.Field()
    Name = scrapy.Field()
    Brand = scrapy.Field()
    MinPrice = scrapy.Field()
    MaxPrice = scrapy.Field()
    Gender = scrapy.Field()
    Color = scrapy.Field()
    Url = scrapy.Field()
    ImageUrl = scrapy.Field()
    Material = scrapy.Field()
    ReviewNumber = scrapy.Field()
    AverageRating = scrapy.Field()
    # pass
