#!/usr/bin/env python
try:
    import settings # Assumed to be in the same directory.
    import sys
    from os.path import join
    sys.path[0:0] = [
        join(settings.TRUNK_DIR, 'apps'),
        join(settings.TRUNK_DIR, 'deps'),
    ]
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.exit(1)

from django.core.management import execute_manager

if __name__ == "__main__":
    execute_manager(settings)
