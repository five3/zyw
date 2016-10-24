#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyquery import PyQuery as pq
import controller

class Crawler :
    def __init__(self, base_url, items, logger, data_ite=None, encoding='utf-8'):
        self.base_url = base_url
        self.encoding = encoding
        self.items = items
        self.logger = logger
        if not data_ite:
            self.data_ite = self.ite(100, 1000)

    def run(self):
        for i in self.data_ite:
            url = self.base_url % i
            self.crawl_it(url)

    def crawl_it(self, url):
        print 'current url: %s' % url
        doc = pq(url, encoding=self.encoding)
        d = {}
        for k, v in self.items.items():
            d[k] = doc(v).text()
        self.logger(d)

    def set_ite(self, data_ite):
        self.data_ite = data_ite

    def ite(self, start=1, end=100):
        for i in range(start, end):
            yield i

urls = {
    'zhaopin_url_format' : 'http://www.qyjob.org/zhiwei/job-%s.html',
    'zixun_url_format' : 'http://www.qyjob.org/article/articledetail-%s.html',
    'guoyuan_url_format' : 'http://www.gyrcai.com/xwzx/jh/%s/%s/%s.html',
}
zp_items = {
    'zhiwei':'.jobztd',
    'company':'.hbdz',
    'detail': '.jobjs2',
}
def zp_logger(d):
    data = {}
    if not d.get('zhiwei'):
        print 'no data get'
        return
    data['zhiwei'] = d.get('zhiwei')
    data['content'] = '<h2>%s</h2><h4>%s</h4><p>职位介绍：<br>%s</p>' % (d.get('zhiwei'), d.get('company'), d.get('detail'))
    data['cate'] = 24
    print data
    # controller.save_content(data)

if __name__=='__main__':
    crawler = Crawler(urls['zhaopin_url_format'], zp_items, zp_logger)
    crawler.run()
