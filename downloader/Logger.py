#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Downlmage import DownloadImage
from backend import controller
from Config import config
import os


s = '''<form action="/baoming/" method="post" id="baoming">
        <div style="width:500px; margin:20px auto;">
            <input class="btn btn-primary btn-lg" type="button" value="报名" style="width:100px;" onclick="baoming();">
        </div>
        <div id="baoming_content" style="display:none;">
        <div class="form-group">
            <label class="control-label" for="id_name">姓名&nbsp;&nbsp;</label>
            <input name="name" id="bm_name" class="text" type="text" value="" max-length="10">
        </div>
        <div class="form-group">
            <label class="control-label" for="id_name">性别&nbsp;&nbsp;</label>
            <label>男</label>
            <input name="sex" type="radio" value="male" checked>
            <label>女</label>
            <input name="sex" type="radio" value="female">
        </div>
        <div class="form-group">
            <label class="control-label" for="id_name">手机&nbsp;&nbsp;</label>
            <input name="phone" id="bm_phone" class="text" type="text" value="" max-length="11">
        </div>
        <div class="form-group">
            <label class="control-label" for="id_name">专业&nbsp;&nbsp;</label>
            <input name="zhuanye" id="bm_zhuanye" class="text" type="text" value="" max-length="20">
        </div>
        <div class="form-group">
            <input name="zhiwei" id="bm_zhiwei" type="hidden" value="%s">
            <input name="company" id="bm_company" type="hidden" value="%s">
            <input class="btn btn-primary btn-lg" type="button" value="提交" onclick="baoming2();" style="width:100px;">
        </div>
        </div>
    </form>'''

def zp_logger(d):
    data = {}
    if not d.get('zhiwei'):
        print 'no data get'
        return
    ss = s % (d.get('zhiwei').text(), d.get('company').text())
    data['title'] = d.get('zhiwei').text() + ' 招聘'
    data['content'] = u'<h2>单位名称：%s</h2><p>职位介绍：<br>%s</p>%s' % (d.get('company').text(), d.get('detail').text(), ss)
    data['description'] = (len(d.get('company').text())>35) and d.get('company').text()[:35] or d.get('company').text()
    data['featured_image'] = d.get('imgs') and d.get('imgs')[0] or '/static/zhiyuw/cy_images/images/infor.jpg'
    data['cate'] = 24
    data['reference'] = d.get('request_info').get('url')
    controller.save_content(data)
    with open(config['zp']['log'], 'w') as f:
        f.write('%s\n' % d.get('index'))


def zx_logger(d, cate=25):
    data = {}
    if not d.get('title'):
        print 'no data get'
        return
    data['title'] = d.get('title').text()
    data['content'] = d.get('content').html()
    data['description'] = (len(d.get('content').text())>35) and d.get('content').text()[:35] or d.get('content').text()
    data['featured_image'] = d.get('imgs') and d.get('imgs')[0] or '/static/zhiyuw/cy_images/images/infor.jpg'
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
    data['cate'] = cate
    data['reference'] = d.get('request_info').get('url')
    controller.save_content(data)
    if cate==25:
        with open(config['zx']['log'], 'w') as f:
            f.write('%s\n' % d.get('index'))
    elif cate==26:
        with open(config['gyrc']['log'], 'w') as f:
            f.write('%s-%s-%s\n' % d.get('index')[:3])

def gyrc_logger(d):
    zx_logger(d, 26)