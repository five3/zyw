#!/usr/bin/env python
#encoding: utf-8

def singleton(className):
    def wrapped():
        it =  className.__dict__.get('__it__')
        if it is not None:
            return it

        className.__it__=className()
        return className.__it__
    return wrapped

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText

from email.utils import COMMASPACE,formatdate
from email import encoders

import os
def send_mail(server, fro, to, subject, text, files=[]):
    assert type(server) == dict
    assert type(to) == list
    assert type(files) == list

    msg = MIMEMultipart()
    msg['From'] = fro
    msg['Subject'] = subject
    msg['To'] = COMMASPACE.join(to) #COMMASPACE==', '
    msg['Date'] = formatdate(localtime=True)
    msg.attach(MIMEText(text, 'html', 'utf-8'))

    for f in files:
        part = MIMEBase('application', 'octet-stream') #'octet-stream': binary data
        part.set_payload(open(f, 'rb').read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
        msg.attach(part)

    import smtplib
    smtp = smtplib.SMTP(server['name'], server['port'])
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(server['user'], server['passwd'])
    smtp.sendmail(fro, to, msg.as_string())
    smtp.close()

def send_reset_email(url, to_email):
    server = {'name':'smtp.163.com', 'user':'five3', 'passwd':'cxwfive3~', 'port':25}
    fro = 'five3@163.com'
    to = [to_email]
    subject = '''【重要】职语网密码重置邮件'''

    text = r'''<p>尊敬的会员您好：</p>
            <p>  您目前正在申请密码重置流程，若非本人操作请尽快与管理员联系并修改密码!</p>
            <p>  若修改密码请在有效期内点击重置密码链接<a href='%s' target='_blank'>%s</a></p>
            <p>                                                        --职语网</p>
            ''' % (url, url)
    files = ['top_category.txt']
    send_mail(server, fro, to, subject, text)

def send_http(url, method='GET', type='JSON'):
    import requests
    r = requests.get(url, verify=False)
    r.encoding = 'utf-8'
    try:
        return r.json()
    except Exception, ex:
        print ex.message
        return None