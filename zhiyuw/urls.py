from __future__ import unicode_literals

from django.conf.urls import patterns, url
from mezzanine.core.views import direct_to_template


urlpatterns = patterns('zhiyuw.views',

    url("^$", 'index', name='zhiyuw'),
    url("^ktq", 'kaituoqquan'),
    url("^gyq", 'gengyunqun'),
    url("^(xxc|bw|tzl|ylxw|wxjl|sy|sh|bjys|zxmk|zjmk|rlzx|zuzhi|geren|qtalh|zc|fl|ss|lz|qtzyk)$", 'category'),
    url("^(fsb|nxt|alh|zyk)$", 'second_cate'),
    url("^gbook$", 'gbook'),
    url("^contact$", 'contact'),
    url("^login$", 'login'),
    url("^logout$", 'logout'),
    url("^register", 'register'),
    url("^member", 'member'),
    url("^qiye_comment", 'qiye_comment'),
    url("^search", 'search'),
    url("^comment", 'comment'),
    url("^(.*)/show-(\d+)\.html$", 'article'),
)

handler404 = "mezzanine.core.views.page_not_found"
handler500 = "mezzanine.core.views.server_error"
