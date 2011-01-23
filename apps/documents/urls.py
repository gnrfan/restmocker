# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url

from documents import views

urlpatterns = patterns('',

      url(r'^$',
        views.realm_index,
        name='realm_index'),
      url(r'^(?P<realm_prefix>[-\w]+)/$',
        views.document_index,
        name='document_index'),
      url(r'^api/(?P<realm_prefix>[-\w]+)/(?P<reminder>[^ ]+)$',
        views.document_view,
        name='document_view'),

)
