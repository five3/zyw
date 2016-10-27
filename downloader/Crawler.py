#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyquery import PyQuery as pq
from Config import urls
from Items import *
from Logger import *

class Crawler :
    def __init__(self, base_url, items, logger, data_ite=None, encoding='gbk', ite_start=1, ite_end=100):
        self.base_url = base_url
        self.encoding = encoding
        self.items = items
        self.logger = logger
        if not data_ite:
            self.data_ite = self.ite(ite_start, ite_end)

    def run(self):
        for i in self.data_ite:
            url = self.base_url % i
            self.crawl_it(url, i)

    def crawl_it(self, url, index):
        print 'current url: %s' % url
        doc = pq(url, encoding=self.encoding)
        d = {'index' : index}
        for k, v in self.items.items():
            d[k] = doc(v)
        self.logger(d)

    def set_ite(self, data_ite):
        self.data_ite = data_ite

    def ite(self, start=1, end=100):
        for i in range(start, end):
            yield i


if __name__=='__main__':
    zpcrawler = Crawler(urls['zhaopin_url_format'], zp_items, zp_logger, encoding='gbk', ite_start=15270, ite_end=15272)
    zpcrawler.run()
    # zxcrawler = Crawler(urls['zixun_url_format'], zx_items, zx_logger, encoding='gbk', ite_start=6719, ite_end=6720)
    # zxcrawler.run()

