# -*- coding: utf-8 -*-
import scrapy
import json
import re
from dongfangcaifu.items import DongfangcaifuItem


class EastmoneySpider(scrapy.Spider):
    # 爬虫名
    name = 'eastmoney'
    # 爬取范围，允许爬虫在这个域名下爬取
    allowed_domains = ['50.push2.eastmoney.com']
    # 爬虫执行的请求，将从这里获取
    urls = {
            "亚洲股市1": "http://50.push2.eastmoney.com/api/qt/clist/get?cb=jQuery11240839915950187746_1585402514702&pn=1&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=i:1.000001,i:0.399001,i:0.399005,i:0.399006,i:1.000300,i:100.HSI,i:100.HSCEI,i:124.HSCCI,i:100.TWII,i:100.N225,i:100.KOSPI200,i:100.KS11,i:100.STI,i:100.SENSEX,i:100.KLSE,i:100.SET,i:100.PSI,i:100.KSE100,i:100.VNINDEX,i:100.JKSE,i:100.CSEALL&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f26,f22,f33,f11,f62,f128,f136,f115,f152,f124,f107&_=1585402514703",
            "亚洲股市2": "http://50.push2.eastmoney.com/api/qt/clist/get?cb=jQuery11240839915950187746_1585402514701&pn=2&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=i:1.000001,i:0.399001,i:0.399005,i:0.399006,i:1.000300,i:100.HSI,i:100.HSCEI,i:124.HSCCI,i:100.TWII,i:100.N225,i:100.KOSPI200,i:100.KS11,i:100.STI,i:100.SENSEX,i:100.KLSE,i:100.SET,i:100.PSI,i:100.KSE100,i:100.VNINDEX,i:100.JKSE,i:100.CSEALL&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f26,f22,f33,f11,f62,f128,f136,f115,f152,f124,f107&_=1585402514715",
            "欧洲股市1": "http://50.push2.eastmoney.com/api/qt/clist/get?cb=jQuery11240839915950187746_1585402514702&pn=1&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=i:100.SX5E,i:100.FTSE,i:100.MCX,i:100.AXX,i:100.FCHI,i:100.GDAXI,i:100.RTS,i:100.IBEX,i:100.PSI20,i:100.OMXC20,i:100.BFX,i:100.AEX,i:100.WIG,i:100.OMXSPI,i:100.SSMI,i:100.HEX,i:100.OSEBX,i:100.ATX,i:100.MIB,i:100.ASE,i:100.ICEXI,i:100.PX,i:100.ISEQ&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f26,f22,f33,f11,f62,f128,f136,f115,f152,f124,f107&_=1585402514734",
            "欧洲股市2": "http://50.push2.eastmoney.com/api/qt/clist/get?cb=jQuery11240839915950187746_1585402514702&pn=2&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=i:100.SX5E,i:100.FTSE,i:100.MCX,i:100.AXX,i:100.FCHI,i:100.GDAXI,i:100.RTS,i:100.IBEX,i:100.PSI20,i:100.OMXC20,i:100.BFX,i:100.AEX,i:100.WIG,i:100.OMXSPI,i:100.SSMI,i:100.HEX,i:100.OSEBX,i:100.ATX,i:100.MIB,i:100.ASE,i:100.ICEXI,i:100.PX,i:100.ISEQ&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f26,f22,f33,f11,f62,f128,f136,f115,f152,f124,f107&_=1585402514747",
            "美洲股市": "http://50.push2.eastmoney.com/api/qt/clist/get?cb=jQuery11240839915950187746_1585402514701&pn=1&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=i:100.DJIA,i:100.SPX,i:100.NDX,i:100.TSX,i:100.BVSP,i:100.MXX&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f26,f22,f33,f11,f62,f128,f136,f115,f152,f124,f107&_=1585402514754",
            "澳洲股市": "http://50.push2.eastmoney.com/api/qt/clist/get?cb=jQuery11240839915950187746_1585402514702&pn=1&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=i:100.AS51,i:100.AORD,i:100.NZ50&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f26,f22,f33,f11,f62,f128,f136,f115,f152,f124,f107&_=1585402514764",
            "其他指数": "http://50.push2.eastmoney.com/api/qt/clist/get?cb=jQuery11240839915950187746_1585402514701&pn=1&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=i:100.UDI,i:100.BDI,i:100.CRB&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f26,f22,f33,f11,f62,f128,f136,f115,f152,f124,f107&_=1585402514771",
            }
    start_urls = urls.values()
    fields = {
        "f1": "",
        "f2": "最新价",
        "f3": "涨跌幅",
        "f4": "涨跌额",
        "f5": "成交量(手)",  # 不确定
        "f6": "成交额",      # 不确定
        "f7": "振幅",
        "f8": "",
        "f9": "",
        "f10": "",
        "f12": "代码",
        "f13": "",
        "f14": "名称",
        "f15": "最高价",
        "f16": "最低价",
        "f17": "开盘价",
        "f18": "昨收价",
        "f20": "",
        "f21": "",
        "f23": "",
        "f24": "",
        "f25": "",
        "f26": "",
        "f22": "",
        "f33": "",
        "f11": "",
        "f62": "",
        "f128": "",
        "f136": "",
        "f115": "",
        "f152": "",
        "f124": "最新行情时间",
        "f107": ""
    }

    allowed_fields = ["f2", "f3", "f4", "f7", "f12", "f14", "f15", "f16", "f17", "f18", "f124"]

    def parse(self, response):
        result = re.findall(r"^jQuery[0-9_]*\((.+)\);$", response.text)[0]
        data = json.loads(result)
        # print(data)
        for v in data['data']['diff']:
            item = DongfangcaifuItem()
            if v['f107'] in [5, 3]:
                continue
            for u_k, u_v in self.urls.items():
                if u_v.find(v['f12']) >= 0:
                    item['area'] = u_k[:4]
            item['stat'] = v['f107']  # 5:已收盘，3:盘中休息，其他:交易中
            item['code'] = v['f12']
            item['name'] = v['f14']
            item['last'] = v['f2']
            item['zhang_die_e'] = v['f4']
            item['zhang_die_fu'] = v['f3']
            item['open'] = v['f17']
            item['high'] = v['f15']
            item['low'] = v['f16']
            item['prev_close'] = v['f18']
            item['zhen_fu'] = v['f7']
            item['last_time'] = v['f124']
            # print(item)
            yield item





