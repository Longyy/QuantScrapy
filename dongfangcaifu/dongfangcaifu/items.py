# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DongfangcaifuItem(scrapy.Item):
    # define the fields for your item here like:
    # 定义字段

    # 开收盘状态
    stat = scrapy.Field()

    # 名称
    name = scrapy.Field()

    # 代码
    code = scrapy.Field()

    # 最新价
    last = scrapy.Field()

    # 涨跌额
    zhang_die_e = scrapy.Field()

    # 涨跌幅
    zhang_die_fu = scrapy.Field()

    # 开盘价
    open = scrapy.Field()

    # 最高价
    high = scrapy.Field()

    # 最低价
    low = scrapy.Field()

    # 昨收价
    prev_close = scrapy.Field()

    # 振幅
    zhen_fu = scrapy.Field()

    # 最新行情时间
    last_time = scrapy.Field()

    # 爬取时间
    created_time = scrapy.Field()

    # 所属市场
    area = scrapy.Field()
