# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
from datetime import datetime
from .tools.PymysqlUtil import PymysqlUtil


class DongfangcaifuPipeline(object):
    __config = {
        "host": "127.0.0.1",
        "user": "root",
        "password": "lcvip122911",
        "database": "LQuant"
    }

    def __init__(self):
        self.db = PymysqlUtil()
        # self.f = open("./eastmoney_pipeline.json", 'w')

    def process_item(self, item, spider):
        item['last_time'] = datetime.strftime(datetime.fromtimestamp(item['last_time']), "%Y-%m-%d %H:%M:%S")
        time_now = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
        item['created_time'] = time_now
        sql = """
        insert into global_index_price(code,last,zhang_die_e,zhang_die_fu,open,high,
        low,prev_close,zhen_fu,last_time,created_time) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        sql.strip()
        data = (item['code'], item['last'], item['zhang_die_e'], item['zhang_die_fu'], item['open'],
                item['high'], item['low'], item['prev_close'], item['zhen_fu'], item['last_time'],
                item['created_time'])
        # print(sql)
        # print(data)
        result = self.db.insert(sql, data)
        if not result:
            print('插入失败！')

        # self.f.write(json.dumps(dict(item), ensure_ascii=False) + ",\n")
        return item

    def close_spider(self, spider):
        self.db.close()
        # self.f.close()
