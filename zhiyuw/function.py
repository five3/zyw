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
    return local_settings.SITE_DICT.get(site_host, 0)