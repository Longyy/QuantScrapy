# -*- coding: utf-8 -*-
import scrapy
import re
import json
from datetime import datetime, date
import time
from dongfangcaifu_zijin.items import DapandayItem


class DapandaySpider(scrapy.Spider):
    name = 'dapanday'
    allowed_domains = ['push2his.eastmoney.com']
    start_urls = ['http://push2his.eastmoney.com/api/qt/stock/fflow/daykline/get?lmt=0&klt=101&secid=1.000001&secid2=0.399001&fields1=f1,f2,f3,f7&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63,f64,f65&ut=b2884a393a59ad64002292a3e90d46a5&cb=jQuery183042577765205604545_1586253649860&_=1586253650652']
    custom_settings = {
        'ITEM_PIPELINES': {'dongfangcaifu_zijin.pipelines.DapandayPipeline': 302},
    }
    fields = {
        0: "时刻",
        1: "今日主力净流入",
        2: "今日小单净流入",
        3: "今日中单净流入",
        4: "今日大单净流入",
        5: "今日超大单净流入",

        6: "今日主力净占比",
        7: "今日小单净占比",
        8: "今日中单净占比",
        9: "今日大单净占比",
        10: "今日超大单净占比"
    }

    def parse(self, response):
        items = []
        result = re.findall(r"^jQuery[0-9_]*\((.+)\);$", response.text)[0]
        data = json.loads(result)
        if not isinstance(data, dict):
            print("返回数据不是json格式！")
            return

        with open("./lasttimeflag_dapanday.txt", "r") as f:
            line = f.read(10000)
            if line.strip() != "":
                line = json.loads(line)
            else:
                line = {}

        # 取最新存储的数据量
        for i in range(len(data["data"]["klines"])):
            part = str(data["data"]["klines"][i]).split(",")
            if part[0] in line.keys():
                print('当天数据已处理')
                continue
            item = DapandayItem()
            item['last_time'] = part[0] + " 00:00:00"
            item['main_inflow'] = part[1]
            item['small_inflow'] = part[2]
            item['midum_inflow'] = part[3]
            item['big_inflow'] = part[4]
            item['huge_inflow'] = part[5]
            item['main_rate'] = part[6]
            item['small_rate'] = part[7]
            item['midum_rate'] = part[8]
            item['big_rate'] = part[9]
            item['huge_rate'] = part[10]
            items.append(item)

            line[part[0]] = 1

        with open("./lasttimeflag_dapanday.txt", "w") as f:
            f.write(json.dumps(line))

        return items
