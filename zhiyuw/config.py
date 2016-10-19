#！encoding: utf-8
__author__ = 'macy'
from model import *

sql = 'SELECT * FROM ww_setting where 1=1'
sql2 = 'SELECT * FROM ww_banner where 1=1'

global_settings = {
    'settings' : unio().fetchOne(sql),
    'banner_list' : unio().fetchAll(sql2)
}

def reset_setting(d):
    d['settings'] = unio().fetchOne(sql)
    d['banner_list'] = unio().fetchOne(sql2)