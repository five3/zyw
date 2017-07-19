#encoding: utf-8
__author__ = 'xwchen2'
import Uploader
import os
##上传配置
config = {
    "savePath" : "%s/static/um/upload" % os.getcwd(),           ##存储文件夹
    "imageUrl" : "/static/um/upload",
    "maxSize" : 5000,                  ##允许的文件最大尺寸，单位KB
    "allowFiles" : ( ".gif" , ".png" , ".jpg" , ".jpeg" , ".bmp" )  ##允许的文件格式
}

from django import forms
class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    upfile = forms.FileField()

def imageup(f):
    up = Uploader.uploader(f, config)
    info = up.getFileInfo()
    return info

import time
def save_image(form, post, f, img_dir, fname):
    form = form(post, f)
    if not form.is_valid():
        return False, '提交的数据不符合要求'
    try:
        if not os.path.exists(img_dir):
            os.makedirs(img_dir)
        file_name = '%s/%s_%s' % (img_dir, time.strftime('%Y%m%d%H%M%S'), f[fname].name)
        print file_name
        destination = open(file_name, 'wb+')
        for chunk in f[fname].chunks():
            destination.write(chunk)
        destination.close()
        return file_name
    except Exception, e:
        print e

