#encoding: utf-8
__author__ = 'xwchen2'

import os
import time

stateMap = {
        '0' : "SUCCESS",
        "POST": "文件大小超出 post_max_size 限制" ,
        "SIZE": "文件大小超出网站限制",
        "TYPE" : "不允许的文件类型" ,
        "DIR" : "目录创建失败" ,
        "IO" : "输入输出错误" ,
        "UNKNOWN" : "未知错误",
        "MOVE" : "文件保存时出错",
        "DIR_ERROR" : "创建目录失败"
}

class uploader:
    def __init__(self, f, config, base64 = False):
        self.f = f
        self.config = config
        self.stateInfo = stateMap['0'];
        self.upFile(base64)

    def upFile(self, base64):
        ##处理base64上传
        if ( "base64" == base64 ):
            pass

        try:
            if not self.checkFileType():
                self.stateInfo = self.stateMap['TYPE']
                return

            if not self.checkFileSize():
                self.stateInfo = self.stateMap['SIZE']
                return

            td = time.strftime('/%Y-%m-%d/')
            path = self.config['savePath'] + td
            self.name = '%s_%s' % (int(time.time()), self.f.name)
            self.url = td +self.name
            if not os.path.exists(path):
                os.makedirs(path)
            self.filePath = path + self.name
            destination = open(self.filePath, 'wb+')
            for chunk in self.f.chunks():
                destination.write(chunk)
            destination.close()
        except Exception, e:
            print e
            import traceback
            traceback.print_exc()

    def checkFileType(self):
        ext = self.f.name.split('.')[1]
        self.fileType = '.'+ext
        if '.'+ext not in self.config['allowFiles']:
            return False
        return True

    def checkFileSize(self):
        self.fileSize = self.f.size
        if self.fileSize > self.config['maxSize'] * 1024:
            return False
        return True

    def getFileInfo(self):
        return {
            "originalName" : self.f.name,
            "name" : self.name,
            "url" : self.url,
            "size" : self.fileSize,
            "type" : self.fileType,
            "state" : self.stateInfo,
            "abs_url" : '%s%s' % (self.config['imageUrl'], self.url),
            }