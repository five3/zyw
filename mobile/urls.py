from __future__ import unicode_literals

from django.conf.urls import patterns, url
from mezzanine.core.views import direct_to_template
from django.contrib.auth import views

urlpatterns = patterns('mobile.views',
    url("^$", 'index', name='zhiyuw'),
    url("^(xxc|bw|tzl|ylxw|wxjl|sy|sh|bjys|zxmk|zjmk|rlzx|zuzhi|geren|qtalh|zc|fl|ss|lz|qtzyk|zpcj|zxcj|gyrc)$", 'list'),
    url("^(fsb|nxt|alh|zyk)$", 'second_cate'),
    url("^contact$", 'contact'),
    url("^ktq", 'ktq'),
    url("^gyq", 'gyq'),
    url("^login$", 'login'),
    url("^register", 'register'),
    url("^agreen$", 'agreen'),
    url("^logout$", 'logout'),
    url("^(.*)/show-(\d+)\.html$", 'article'),
    url("^post/(.*)$", 'post'),
    url("^myarts", 'myarts'),
    url("^xiangwang", 'xiangwang'),
    url("^navigate/(.*)$", 'navigate'),
    url("^tianchi", 'tianchi'),
    url("^pinpai", 'pinpai'),
    url("^caifu", 'caifu'),
    url("^money", 'money'),
    url("^info/(.*)$", 'info'),
    url("^3rd_qq_login", 'qq_login'),
    url("^3rd_yd", 'third_yd'),
    url("^3rd_weixin_login", 'weixin_login'),
    url("^forgotpwd", 'forgotpwd'),
)

handler404 = "mezzanine.core.views.page_not_found"
handler500 = "mezzanine.core.views.server_error"
