from __future__ import unicode_literals

from django.conf.urls import patterns, url
from mezzanine.core.views import direct_to_template
from django.contrib.auth import views

urlpatterns = patterns('backend.views',

    url("^post/(.*)/$", 'post'),
    url("^comments/(.*)/$", 'comments'),
    url("^gbook/(.*)/$", 'gbook'),
    url("^users/(.*)/$", 'users'),
    url("^admin/(.*)/$", 'admin'),
    url("^manage/(.*)/$", 'manage'),
    url("^category/(.*)/$", 'category'),
    url("^profile/?$", 'profile'),
    url("^resetpw/?$", 'resetpw'),
    # url("^login/?$", views.login, {'template_name': 'backend/login.html'}),
    url("^login/?$", 'login'),
    url("^logout/?$", views.logout_then_login, {'login_url': '/backend/login/'}),
    url("^imageUp/?$", 'postimage'),
    url("^imageUp/?$", 'postimage'),
    url("^$", 'index'),
)

handler404 = "mezzanine.core.views.page_not_found"
handler500 = "mezzanine.core.views.server_error"
