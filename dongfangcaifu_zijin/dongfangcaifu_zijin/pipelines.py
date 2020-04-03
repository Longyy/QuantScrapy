# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
from datetime import datetime
from .tools.PymysqlUtil import PymysqlUtil


class DongfangcaifuZijinPipeline(object):
    def __init__(self):
        self.db = PymysqlUtil()
        self.f = open("./zijin_pipeline.json", 'w')

    def process_item(self, item, spider):
        time_now = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
        item['created_time'] = time_now
        sql = """
        insert into zijin_in_out(type,hu_in,hu_yu,shen_in,shen_yu,inflow,last_time,
        created_time) values (%s,%s,%s,%s,%s,%s,%s,%s)
        """
        data = (item['zijin_type'], item['hu_in'], item['hu_yu'], item['shen_in'], item['shen_yu'],
                item['inflow'], item['last_time'], item['created_time'])
        result = self.db.insert(sql, data)
        if not result:
            print('Insert Failed!')

        self.f.write(json.dumps(dict(item), ensure_ascii=False) + ",\n")
        return item

    def close_spider(self, spider):
        self.db.close()
        self.f.close()