#!/usr/bin/env python
#encoding: utf-8

def mk_md5(s):
    import hashlib
    m = hashlib.md5()
    m.update(s)
    return m.hexdigest()

def warp_data(data):
    data = dict(data)
    for k,v in data.items():
        if isinstance(v, list):
            if len(v)>1:
                data[k] = ','.join(v)
            elif len(v)==1:
                data[k] = v[0]
            else:
                data[k] = ''
        else:
            data[k] = ''
    return data

def now():
    import time
    return time.strftime('%Y-%m-%d %X', time.localtime() )

def handle_uploaded_file(f):
    destination = open('static/upload/%s' % f.name,'wb')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    return True

def need_site_id(func):
    def _need_site_id(req, *args):
        # print req.META['HTTP_HOST'], req.META['REMOTE_HOST']
        req.session['site_host'] = req.META['HTTP_HOST'].split(':')[0]
        ret = func(req, *args)
        return ret
    return _need_site_id

import local_settings
def get_site_id(req):
    site_host = req.META['HTTP_HOST'].split(':')[0]
    return local_settings.SITE_DICT.get(site_host, 1)

def get_site_logo(req):
    site_host = req.META['HTTP_HOST'].split(':')[0]
    return local_settings.SITE_LOGO.get(site_host, '')

def convert_dengji_list(*l):
    tl = []
    # print l
    for i in l:
        if i['utype'] == 'gyq':
            i['dengji'] = convert_geren_dengji(i['credits'])
        else:
            i['dengji'] = convert_qiye_dengji(i['credits'])
        tl.append(i)
    # print tl
    return tl

def convert_geren_dengji(credits):
    if credits < 800:
        return "迎客松"
    elif credits <= 999:
        return "迎客松"
    elif credits <= 1399:
        return "帝王树"
    elif credits <= 2099:
        return "凤凰松"
    elif credits <= 2299:
        return "汉柏凌霄"
    elif credits <= 2499:
        return "阿里山神木"
    elif credits <= 2599:
        return "苦槠"
    elif credits <= 3999:
        return "林芝巨柏"
    elif credits <= 4999:
        return "黄帝手植柏"
    elif credits <= 9999:
        return "轩辕柏"
    else:
        return "筠连珙桐"

def convert_qiye_dengji(credits):
    if credits < 150:
        return "无名榕"
    elif credits <= 249:
        return "沙堆榕"
    elif credits <= 299:
        return "樟州榕"
    elif credits <= 399:
        return "学院榕"
    elif credits <= 499:
        return "玉水榕"
    elif credits <= 599:
        return "天马榕"
    elif credits <= 799:
        return "恩平榕"
    elif credits <= 999:
        return "翰林榕"
    elif credits <= 1399:
        return "长宁榕"
    else:
        return "阳朔榕"
