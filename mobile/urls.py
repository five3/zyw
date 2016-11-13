from __future__ import unicode_literals

from django.conf.urls import patterns, url
from mezzanine.core.views import direct_to_template
from django.contrib.auth import views

urlpatterns = patterns('mobile.views',
    url("^$", 'index', name='zhiyuw'),
    url("^article", 'article'),
    url("^caifu", 'caifu'),
    url("^(xxc|bw|tzl|ylxw|wxjl|sy|sh|bjys|zxmk|zjmk|rlzx|zuzhi|geren|qtalh|zc|fl|ss|lz|qtzyk|zpcj|zxcj|gyrc)$", 'list'),
    # url("^(fsb|nxt|alh|zyk)$", 'second_cate'),
    url("^navigate", 'navigate'),
    # url("^contact$", 'contact'),
    url("^login$", 'login'),
    # url("^logout$", 'logout'),
    url("^register", 'register'),
    url("^post", 'post'),
    url("^shuka", 'shuka'),
    # url("^(.*)/show-(\d+)\.html$", 'article'),
)

handler404 = "mezzanine.core.views.page_not_found"
handler500 = "mezzanine.core.views.server_error"
