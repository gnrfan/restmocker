# -*- coding: utf-8 -*-

from urlparse import urlsplit

from django.conf import settings
from django.contrib.sites.models import Site

def get_remote_static_url():
    """
    Builds the remote static url to be used in HTML emails
    """
    static_url = settings.STATIC_URL
    if static_url.startswith('http'):
        return static_url

    site = Site.objects.get_current()
    remote_url = 'http://' + site.domain + static_url
    return remote_url

def strip_url_path(path):
    """ returns the path of a url, no domain"""
    return urlsplit(path).path

def paths(request):
    """
    Sets into context the STATIC_URL and MEDIA_URL so they can be
    used in templates
    """
    return {
        'remote_static_url': get_remote_static_url(),
        'static_url': settings.STATIC_URL,
        'media_url': settings.MEDIA_URL,
        'referer': strip_url_path(request.META.get('HTTP_REFERER', '/')),
    }

def current_site(request):
    """
    Returns the current site
    """
    site = Site.objects.get_current()
    return {'site': site}
