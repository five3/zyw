#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

cwd = os.path.dirname(__file__)
config = {
    'images_dir' : os.path.join(cwd, '../static/uploadfiles'),
    'static_dir' : '/static/uploadfiles',
    'zp' : {
        'log' : 'zp.index'
    },
    'zx' : {
        'log' : 'zx.index'
    },
    'gyrc' : {
        'log' : 'gyrc.index'
    },'log': 'downloader.log'
}

urls = {
    'zhaopin_url_format' : 'http://www.qyjob.org/zhiwei/job-%s.html',
    'zixun_url_format' : 'http://www.qyjob.org/article/articledetail-%s.html',
    'guoyuan_url_format' : 'http://www.gyrcai.com/xwzx/jh/%s/%s/%s.html',
}