# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DongfangcaifuZijinItem(scrapy.Item):
    # define the fields for your item here like:
    # 类别 1: 北向资金，2: 南向资金
    zijin_type = scrapy.Field()
    # 最新行情时间
    last_time = scrapy.Field()
    # 爬取时间
    created_time = scrapy.Field()
    # 沪股通当日净流入
    hu_in = scrapy.Field()
    # 沪股通当日余额
    hu_yu = scrapy.Field()
    # 深股通当日净流入
    shen_in = scrapy.Field()
    # 深股通当日余额
    shen_yu = scrapy.Field()
    # 北向资金当日净流入
    inflow = scrapy.Field()

