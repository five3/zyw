#!/usr/bin/env python
#encoding: utf-8
from __future__ import absolute_import, unicode_literals

import os
import sys


# Corrects some pathing issues in various contexts, such as cron jobs,
# and the project layout still being in Django 1.3 format.
from settings import PROJECT_ROOT, PROJECT_DIRNAME
sys.path.append(os.path.abspath(os.path.join(PROJECT_ROOT, "..")))

##设置python环境为utf-8编码
import sys
print 'default python env coding:', sys.getdefaultencoding()
reload(sys)
sys.setdefaultencoding('utf-8')
print 'current python env coding:', sys.getdefaultencoding()

# Add the site ID CLI arg to the environment, which allows for the site
# used in any site related queries to be manually set for management
# commands.
for i, arg in enumerate(sys.argv):
    if arg.startswith("--site"):
        os.environ["MEZZANINE_SITE_ID"] = arg.split("=")[1]
        sys.argv.pop(i)


# Run Django.
if __name__ == "__main__":
    settings_module = "%s.settings" % PROJECT_DIRNAME
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
