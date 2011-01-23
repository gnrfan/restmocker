from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

# Uncomment the next two lines to enable the admin:
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    url(r'^', include('documents.urls')),
)

if settings.DEBUG:
    from django.views.static import serve

    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$',
            serve, {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        url(r'^static/(?P<path>.*)$',
            serve, {'document_root': settings.STATIC_ROOT}),
        url(r'^favicon\.ico$',
            'django.views.generic.simple.redirect_to',
            {'url': '/static/images/favicon.ico'}),
    )

