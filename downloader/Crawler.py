#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyquery import PyQuery as pq
from Config import urls, config
import threading
from Items import *
from Logger import *
from urlparse import urlparse

class Crawler(threading.Thread):
    def __init__(self, base_url, items, logger, data_ite=None, encoding='gbk', ite_start=1, ite_end=100):
        threading.Thread.__init__(self)
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
        parsed = urlparse(url)
        d['request_info'] = {
            'proxy' :  parsed.scheme,
            'hostname' : parsed.hostname,
            'port' : parsed.port or 80,
            'url' : url
        }
        self.logger(d)

    def set_ite(self, data_ite):
        self.data_ite = data_ite

    def ite(self, start=1, end=100):
        for i in range(start, end):
            yield i


def get_index(x):
    try:
        with open(config[x]['log'], 'r') as f:
            return f.read()
    except:
        pass


def start():
    threads = []
    zp_start = get_index('zp')
    if zp_start:
        zp_start = int(zp_start)
    else:
        zp_start = 13000
    print zp_start
    threads.append(Crawler(urls['zhaopin_url_format'], zp_items, zp_logger, encoding='gbk', ite_start=zp_start+1, ite_end=zp_start+1000))

    zx_start = get_index('zx')
    if zx_start:
        zx_start = int(zx_start)
    else:
        zx_start = 1000
    print zx_start
    threads.append(Crawler(urls['zixun_url_format'], zx_items, zx_logger, encoding='gbk', ite_start=zx_start+1, ite_end=zx_start+1000))

    for t in threads:
        t.start()

    for t in threads:
        t.join()


if __name__=='__main__':
    start()
