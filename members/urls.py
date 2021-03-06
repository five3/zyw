from __future__ import unicode_literals

from django.conf.urls import patterns, url

urlpatterns = patterns('members.views',

    url("^imageUp/?$", 'postimage'),
    url("^profile/?$", 'profile'),
    url("^password/?$", 'password'),
    url("^bgmusic/?$", 'bgmusic'),
    url("^zhaopin/?$", 'zhaopin'),
    url("^shuoshuo/?$", 'shuoshuo'),
    url("^pinpai/?$", 'pinpai'),
    url("^tianchi/?$", 'tianchi'),
    url("^xiangwang/?$", 'xiangwang'),
    url("^money/?$", 'money'),
    url("^daohang/(.*)/?$", 'daohang'),
    url("^post/(.*)/$", 'post'),
    url("^cate/?$", 'cate'),
    url("^$", 'index'),
)

handler404 = "mezzanine.core.views.page_not_found"
handler500 = "mezzanine.core.views.server_error"
