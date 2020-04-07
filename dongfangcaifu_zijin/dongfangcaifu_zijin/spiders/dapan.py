# -*- coding: utf-8 -*-
import scrapy
import re
import json
from datetime import datetime, date
import time
from dongfangcaifu_zijin.items import DapanItem

class DapanSpider(scrapy.Spider):
    name = 'dapan'
    allowed_domains = ['push2.eastmoney.com']
    start_urls = ['http://push2.eastmoney.com/api/qt/stock/fflow/kline/get?lmt=0&klt=1&secid=1.000001&secid2=0.399001&fields1=f1,f2,f3,f7&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63&ut=b2884a393a59ad64002292a3e90d46a5&cb=jQuery18301298661166185222_1586252446542&_=1586252447331']
    custom_settings = {
        'ITEM_PIPELINES': {'dongfangcaifu_zijin.pipelines.DapanPipeline': 301},
    }
    fields = {
        0: "时刻",
        1: "今日主力净流入",
        2: "今日小单净流入",
        3: "今日中单净流入",
        4: "今日大单净流入",
        5: "今日超大单净流入"
    }

    def parse(self, response):
        items = []
        day_cnt = 0
        result = re.findall(r"^jQuery[0-9_]*\((.+)\);$", response.text)[0]
        data = json.loads(result)
        if not isinstance(data, dict):
            print("返回数据不是json格式！")
            return
        # 取当前日期
        today = date.today()
        # today = '2020-04-01'

        with open("./lasttimeflag_dapan.txt", "r") as f:
            line = f.read(10000)
            if line.strip() != "":
                line = json.loads(line)
                if isinstance(line, dict) and str(today) in line.keys():
                    if "dapan" in line[str(today)].keys():
                        day_cnt = line[str(today)]["dapan"]
            else:
                line = {}

        # 取最新存储的数据量
        for i in range(len(data["data"]["klines"])):
            part = str(data["data"]["klines"][i]).split(",")
            if len(part) != 6:
                print('数据不全')
                continue
            if str(today) != part[0][:10]:
                print('只处理当天数据')
                continue
            if i+1 <= day_cnt:
                print('没有新数据')
                continue
            item = DapanItem()
            item['last_time'] = part[0] + ":00"
            item['main_inflow'] = part[1]
            item['small_inflow'] = part[2]
            item['midum_inflow'] = part[3]
            item['big_inflow'] = part[4]
            item['huge_inflow'] = part[5]
            items.append(item)
        with open("./lasttimeflag_dapan.txt", "w") as f:
            line[str(today)] = {"dapan": len(data["data"]["klines"])}
            f.write(json.dumps(line))
        return items
