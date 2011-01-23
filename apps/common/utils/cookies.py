# -*- coding: utf-8 -*-

import datetime
from django.contrib.sites.models import Site
from django.conf import settings

def set_cookie(response, key, value, days_expire = 7):
    if days_expire is None:
        max_age = 365*24*60*60  #one year
    else:
        max_age = days_expire*24*60*60 
    site = Site.objects.get_current()
    domain = getattr(settings, 'SESSION_COOKIE_DOMAIN', site.domain)
    expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
    response.set_cookie(key, value, max_age=max_age, expires=expires, domain=domain, secure=settings.SESSION_COOKIE_SECURE or None)
    return response
