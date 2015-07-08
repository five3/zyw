from __future__ import unicode_literals

from django.conf.urls import patterns, url

urlpatterns = patterns('members.views',

    url("^imageUp/?$", 'postimage'),
    url("^profile/?$", 'profile'),
    url("^password/?$", 'password'),
    url("^bgmusic/?$", 'bgmusic'),
    url("^zhaopin/?$", 'zhaopin'),
    url("^shuoshuo/?$", 'shuoshuo'),
    url("^post/(.*)/$", 'post'),
    url("^$", 'index'),
)

handler404 = "mezzanine.core.views.page_not_found"
handler500 = "mezzanine.core.views.server_error"
