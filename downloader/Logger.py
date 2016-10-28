#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Downlmage import DownloadImage
from backend import controller
from Config import config
import os


def zp_logger(d):
    data = {}
    if not d.get('zhiwei'):
        print 'no data get'
        return
    with open(config['zp']['log'], 'w') as f:
        f.write('%s\n' % d.get('index'))
    data['title'] = d.get('zhiwei').text()
    data['content'] = u'<h2>%s</h2><h4>%s</h4><p>职位介绍：<br>%s</p>' % (d.get('zhiwei').text(), d.get('company').text(), d.get('detail').text())
    data['cate'] = 24
    # print data['content']
    controller.save_content(data)


def zx_logger(d):
    data = {}
    if not d.get('title'):
        print 'no data get'
        return
    with open(config['zx']['log'], 'w') as f:
        f.write('%s\n' % d.get('index'))
    data['title'] = d.get('title').text()
    data['content'] = d.get('content').html()
    des = os.path.join(config.get('images_dir'), 'zx')
    downloader = DownloadImage(des)
    for img in d.get('imgs'):
        src = img.attrib.get('src')
        img_path = downloader.download_image(src)
        img_static_path = config.get('static_dir') + img_path.replace(config.get('images_dir'), '')
        data['content'].replace('src="%s"' % src, 'src="%s"' % img_static_path)
    data['cate'] = 25
    # print data['content']
    controller.save_content(data)


