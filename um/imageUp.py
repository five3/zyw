#encoding: utf-8
__author__ = 'xwchen2'
import Uploader
import os
##上传配置
config = {
    "savePath" : "%s/static/um/upload" % os.getcwd(),           ##存储文件夹
    "imageUrl" : "/static/um/upload",
    "maxSize" : 1000 ,                  ##允许的文件最大尺寸，单位KB
    "allowFiles" : ( ".gif" , ".png" , ".jpg" , ".jpeg" , ".bmp" )  ##允许的文件格式
}

from django import forms
class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    upfile = forms.FileField()

def imageup(f):
    up = Uploader.uploader(f, config)
    info = up.getFileInfo()
    import json
    return json.dumps(info)
