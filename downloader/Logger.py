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
    data['title'] = d.get('zhiwei').text() + ' 招聘'
    data['content'] = u'<h2>单位名称：%s</h2><p>职位介绍：<br>%s</p>' % (d.get('company').text(), d.get('detail').text())
    data['cate'] = 24
    data['reference'] = d.get('request_info').get('url')
    controller.save_content(data)
    with open(config['zp']['log'], 'w') as f:
        f.write('%s\n' % d.get('index'))


def zx_logger(d):
    data = {}
    if not d.get('title'):
        print 'no data get'
        return
    data['title'] = d.get('title').text()
    data['content'] = d.get('content').html()
    des = os.path.join(config.get('images_dir'), 'zx')
    downloader = DownloadImage(des)
    for img in d.get('imgs'):
        src = img.attrib.get('src')
        if not src.startswith('http'):
            src = '%s://%s:%s%s' % (d.get('request_info').get('proxy'), d.get('request_info').get('hostname'), d.get('request_info').get('port', 80), src)
        img_path = downloader.download_image(src)
        if img_path:
            img_static_path = config.get('static_dir') + img_path.replace(config.get('images_dir'), '')
            data['content'] = data['content'].replace('src="%s"' % src, 'src="%s"' % img_static_path)
        else:
            with open(config.get('log'), 'a') as f:
                f.write('Download Image Fail "' + src + '" For url:' + d.get('request_info').get('url'))
    data['cate'] = 25
    data['reference'] = d.get('request_info').get('url')
    controller.save_content(data)
    with open(config['zx']['log'], 'w') as f:
        f.write('%s\n' % d.get('index'))	


