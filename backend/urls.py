from __future__ import unicode_literals

from django.conf.urls import patterns, url
from mezzanine.core.views import direct_to_template
from django.contrib.auth import views

urlpatterns = patterns('backend.views',

    url("^post/(.*)/$", 'post'),
    url("^comments/(.*)/$", 'comments'),
    url("^gbook/(.*)/$", 'gbook'),
    url("^category/(.*)/$", 'category'),
    url("^login/?$", views.login, {'template_name': 'backend/login.html'}),
    url("^logout/?$", views.logout_then_login, {'login_url': '/backend/login/'}),
    url("^imageUp/?$", 'postimage'),
    url("^$", 'index'),
)

handler404 = "mezzanine.core.views.page_not_found"
handler500 = "mezzanine.core.views.server_error"
