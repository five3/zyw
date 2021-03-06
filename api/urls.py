from __future__ import unicode_literals

from django.conf.urls import patterns, url

urlpatterns = patterns('members.views',
    url("^post/(.*)/$", 'postapi'),
)

handler404 = "mezzanine.core.views.page_not_found"
handler500 = "mezzanine.core.views.server_error"
