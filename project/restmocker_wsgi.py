import os
import sys
import site
from os.path import dirname, join, realpath
from distutils.sysconfig import get_python_lib

ROOT_DIR = realpath(join(dirname(__file__), '..'))
PYTHON_VERSION = '%d.%d' % (sys.version_info[0], sys.version_info[1])

USE_VIRTUAL_ENV = True

if USE_VIRTUAL_ENV:
    SITE_PACKAGES_DIR = '%s/env/lib/python%s/site-packages' % (
        ROOT_DIR,
        PYTHON_VERSION
    )
else:
    SITE_PACKAGES_DIR = get_python_lib()

ALLDIRS = [SITE_PACKAGES_DIR]

# Remember original sys.path.
prev_sys_path = list(sys.path)

# Add each new site-packages directory.
for directory in ALLDIRS:
  site.addsitedir(directory)

# Reorder sys.path so new directories at the front.
new_sys_path = []
for item in list(sys.path):
    if item not in prev_sys_path:
        new_sys_path.append(item)
        sys.path.remove(item)
sys.path[:0] = new_sys_path

# Project-specific paths
APPS_DIR = realpath(join(ROOT_DIR, 'apps/'))
PROJ_DIR = realpath(join(ROOT_DIR, 'project/'))

sys.path.insert(0, ROOT_DIR)
sys.path.insert(1, APPS_DIR)
sys.path.insert(2, PROJ_DIR)

# Uncomment for debugging purposes
# print SITE_PACKAGES_DIR
# sys.exit()

os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'

# Avoid ``[Errno 13] Permission denied: '/var/www/.python-eggs'`` messages
os.environ['PYTHON_EGG_CACHE'] = '/tmp/egg-cache'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
