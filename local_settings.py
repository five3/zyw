
import os

DEBUG = True

# Make these unique, and don't share it with anybody.
SECRET_KEY = "58c19c0e-66a4-4205-9a54-6f6aa79e62a1f7c840d2-78f3-44ce-87c0-9c0c900b04531b5f446e-e5db-4a48-ad9e-605a628afa43"
NEVERCACHE_KEY = "4a65e2cf-ed5c-4056-8c8f-2842c50eac568b7b090d-f0c5-40ac-8770-3575bcd800f04c247638-bc1c-497c-9e3b-87efb2298738"

DATABASES = {
    "default": {
        # Ends with "postgresql_psycopg2", "mysql", "sqlite3" or "oracle".
        "ENGINE": "django.db.backends.mysql",
        # DB name or path to database file if using sqlite3.
        "NAME": "mzproject",
        # Not used with sqlite3.
        "USER": "root",
        # Not used with sqlite3.
        "PASSWORD": "changeit!",
        # Set to empty string for localhost. Not used with sqlite3.
        "HOST": "localhost",
        # Set to empty string for default. Not used with sqlite3.
        "PORT": "3306",
    }
}

DB_TYPE='mysql'
DB_STRING='localhost/3306/root/changeit!/mzproject'
DB_TABEL_PREFIX='mz_'

ROOT_PATH=os.getcwd()+'/'
LOGIN_URL = '/backend/login/'
LOGIN_REDIRECT_URL = '/backend/'
APPEND_SLASH = False

SITE_ID = 1
SITE_DICT = {'localhost':1, 'www.zhiyuw.com':1, 'www.tc-zhiyuw.com':2,
             'www.cz-zhiyuw.com':3, 'www.aq-zhiyuw.com':4, 'www.la-zhiyuw.com':5,
             'www.hn-zhiyuw.com':6, 'www.chz-zhiyuw.com':7}
SITE_LOGO = {'localhost' : '/static/zhiyuw/cy_images/images/logo.png',
             'www.zhiyuw.com' : '/static/zhiyuw/cy_images/images/logo.png',
             'www.tc-zhiyuw.com' : '/static/zhiyuw/cy_images/images/logo_tongcheng.png',
             'www.cz-zhiyuw.com' : '/static/zhiyuw/cy_images/images/logo_chizhou.png',
             'www.aq-zhiyuw.com' : '/static/zhiyuw/cy_images/images/logo_anqing.png',
             'www.la-zhiyuw.com' : '/static/zhiyuw/cy_images/images/logo_luan.png',
             'www.hn-zhiyuw.com' : '/static/zhiyuw/cy_images/images/logo_huainan.png',
             'www.chz-zhiyuw.com' :'/static/zhiyuw/cy_images/images/logo_chuzhou.png'}