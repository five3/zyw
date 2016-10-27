#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import os


class DownloadImage:
    def __init__(self, des_dir):
        self.des_dir = des_dir
        if not os.path.exists(des_dir):
            os.mkdir(des_dir)

    def download_image(self, src, fn=None):
        if not fn:
            fn = src.split('/')[-1]

        print "Download Image File=", fn
        r = requests.get(src, stream=True) # here we need to set stream = True parameter
        full_name = self.des_dir + '/' + fn
        with open(full_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    f.flush()
            f.close()
        return full_name

if __name__=='__main__':
    di = DownloadImage('./imgs')
    di.download_image('https://www.baidu.com/img/baidu_jgylogo3.gif')
