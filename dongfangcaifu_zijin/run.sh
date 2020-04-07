#!/usr/bin/env bash
cd /root/QuantScrapy/dongfangcaifu_zijin/dongfangcaifu_zijin/spiders && /usr/local/bin/scrapy crawl zijin -o run.csv
cd /root/QuantScrapy/dongfangcaifu_zijin/dongfangcaifu_zijin/spiders && /usr/local/bin/scrapy crawl dapan -o run_dapan.csv
cd /root/QuantScrapy/dongfangcaifu_zijin/dongfangcaifu_zijin/spiders && /usr/local/bin/scrapy crawl dapanday -o run_dapanday.csv