"""
WSGI config for BillingWidget project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os, sys, site

path = os.path.dirname(os.path.abspath(__file__))

if path not in sys.path:
    sys.path.insert(0, path)

sys.path.append( path + '/home')
sys.path.append( path + '/HomeCloud')

os.environ["DJANGO_SETTINGS_MODULE"] = "HomeCloud.settings"

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
