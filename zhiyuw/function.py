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
        i['count'] = convert_dengji(i['credits'])
        tl.append(i)
    # print tl
    return tl

def convert_dengji(credits):
    f = ['*']
    if credits < 20:
        return f * 1
    elif credits < 50:
        return f * 2
    elif credits < 100:
        return f * 3
    elif credits < 200:
        return f * 4
    elif credits < 400:
        return f * 5
    elif credits < 800:
        return f * 6
    else:
        return f * 7