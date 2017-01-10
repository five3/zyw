#！encoding: utf-8
__author__ = 'macy'
from model import *

sql = 'SELECT * FROM ww_setting where 1=1'
sql2 = '''SELECT * FROM ww_banner where t='web' order by id desc limit 0,10'''
sql3 = '''SELECT * FROM ww_banner where t='mobile' order by id desc limit 0,10'''
sql4 = '''SELECT * FROM ww_banner where t='ydy' order by id desc limit 0,10'''

qq_appid = '101379426'

global_settings = {
    'settings' : unio().fetchOne(sql),
    'banner_list' : unio().fetchAll(sql2),
    'banner_list_mobile' : unio().fetchAll(sql3),
    'banner_list_ydy' : unio().fetchAll(sql4),
}

def reset_setting(d):
    d['settings'] = unio().fetchOne(sql)
    d['banner_list'] = unio().fetchAll(sql2)
    d['banner_list_mobile'] = unio().fetchAll(sql3)
    d['banner_list_ydy'] = unio().fetchAll(sql4)