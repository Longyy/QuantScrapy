# -*- coding: utf-8 -*-
import scrapy
import json
import re
from datetime import datetime, date
import time
from dongfangcaifu_zijin.items import DongfangcaifuZijinItem


class ZijinSpider(scrapy.Spider):
    name = 'zijin'
    allowed_domains = ['push2.eastmoney.com']
    start_urls = ['http://push2.eastmoney.com/api/qt/kamt.rtmin/get?fields1=f1,f2,f3,f4&fields2=f51,f52,f53,f54,f55,f56&ut=b2884a393a59ad64002292a3e90d46a5&cb=jQuery18309104654898684308_1585835417660&_=1585835418524']
    fields = {
        0: "时刻",
        1: "沪股通当日净流入",
        2: "沪股通当日余额",
        3: "深股通当日净流入",
        4: "深股通当日余额",
        5: "北向资金当日净流入"
    }

    def parse(self, response):
        items = []
        nan_day_cnt = 0
        bei_day_cnt = 0
        s2n = []
        n2s = []
        result = re.findall(r"^jQuery[0-9_]*\((.+)\);$", response.text)[0]
        data = json.loads(result)
        if not isinstance(data, dict):
            print("返回数据不是json格式！")
            return
        # 取当前日期
        today = date.today()
        # today = '2020-04-01'
        # 取最新存储的数据量
        with open("./lasttimeflag.txt", "r") as f:
            line = f.read(10000)
            if line.strip() != "":
                line = json.loads(line)
                if isinstance(line, dict) and str(today) in line.keys():
                    if "nan" in line[str(today)].keys():
                        nan_day_cnt = line[str(today)]["nan"]
                    if "bei" in line[str(today)].keys():
                        bei_day_cnt = line[str(today)]["bei"]
            else:
                line = {}
        # 处理北向数据
        bei_date = str(today)[0:4] + "-" + data["data"]["s2nDate"]
        # 只处理当天数据
        if str(today) == bei_date:
            # 去掉无效数据
            s2n = [i for i in data["data"]["s2n"] if str(i).split(",")[1] != "-"]
            if len(s2n) > bei_day_cnt:
                # 只处理新增数据
                for i in range(len(s2n)):
                    if i+1 <= bei_day_cnt:
                        continue
                    part = str(s2n[i]).split(",")
                    item = DongfangcaifuZijinItem()
                    item["zijin_type"] = 's2n'
                    item["last_time"] = str(today) + " " + str(part[0]) + ":00"
                    item["hu_in"] = part[1]
                    item["hu_yu"] = part[2]
                    item["shen_in"] = part[3]
                    item["shen_yu"] = part[4]
                    item["inflow"] = part[5]
                    items.append(item)

        # 处理南向数据
        nan_date = str(today)[0:4] + "-" + data["data"]["n2sDate"]
        # 只处理当天数据
        if str(today) == nan_date:
            # 去掉无效数据
            n2s = [i for i in data["data"]["n2s"] if str(i).split(",")[1] != "-"]
            if len(n2s) > nan_day_cnt:
                # 只处理新增数据
                for i in range(len(n2s)):
                    if i + 1 <= nan_day_cnt:
                        continue
                    part = str(n2s[i]).split(",")
                    item = DongfangcaifuZijinItem()
                    item["zijin_type"] = 'n2s'
                    item["last_time"] = str(today) + " " + str(part[0]) + ":00"
                    item["hu_in"] = part[1]
                    item["hu_yu"] = part[2]
                    item["shen_in"] = part[3]
                    item["shen_yu"] = part[4]
                    item["inflow"] = part[5]
                    items.append(item)
        with open("./lasttimeflag.txt", "w") as f:
            line[str(today)] = {"bei": len(s2n), "nan": len(n2s)}
            f.write(json.dumps(line))
        return items
