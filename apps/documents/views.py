# -*- coding: utf-8 -*-

import hashlib
import datetime
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_list
from django.views.decorators.http import condition
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.conf import settings

from documents.models import Realm, Document
from documents import settings as documents_settings

def realm_index(request):
    realms = Realm.objects.all().order_by('name')
    return object_list(request, realms,
        template_name='documents/realms.html', 
        paginate_by=documents_settings.REALM_PAGINATE_BY,
        extra_context={})

def document_index(request, realm_prefix):
    realm = get_object_or_404(Realm, prefix=realm_prefix)
    documents = realm.document_set.all()
    return object_list(request, documents,
        template_name='documents/documents.html', 
        paginate_by=documents_settings.DOCUMENT_PAGINATE_BY,
        extra_context={})

def document_etag(request, realm_prefix, reminder):
    try:
        realm = Realm.objects.get(prefix=realm_prefix)
        reminder = '/' + reminder
        forced_mimetype = request.GET.get('mimetype', None)
        documents = realm.document_set.all().order_by('-regexp')
        for doc in documents:
            if doc.match(reminder):
                return doc.get_etag(request, reminder)
    except Realm.DoesNotExist:
        pass

    return hashlib.sha1(str(datetime.datetime.now())).hexdigest()

def document_last_modified(request, realm_prefix, reminder):
    try:
        realm = Realm.objects.get(prefix=realm_prefix)
        reminder = '/' + reminder
        forced_mimetype = request.GET.get('mimetype', None)
        documents = realm.document_set.all().order_by('-regexp')
        for doc in documents:
            if doc.match(reminder):
                return doc.get_last_modified()
    except Realm.DoesNotExist:
        pass

    return datetime.datetime.now()

@csrf_exempt
@condition(etag_func=document_etag, last_modified_func=document_last_modified)
def document_view(request, realm_prefix, reminder):
    realm = get_object_or_404(Realm, prefix=realm_prefix)
    reminder = '/' + reminder
    forced_mimetype = request.GET.get('mimetype', None)
    callback = request.GET.get('callback', None)
    documents = realm.document_set.all().order_by('-regexp')
    for doc in documents:
        if doc.match(reminder, request.method, request.META):
            if forced_mimetype:
                mimetype = forced_mimetype
            else:
                mimetype = doc.mime_type
            if doc.attachment and doc.use_attachment:
                content = doc.attachment.read(doc.attachment.size)
                response = HttpResponse(
                    content=content, 
                    mimetype=mimetype, 
                    status_code=doc.status_code
                )
                response['Accept-Ranges'] = 'bytes'
                response['Content-Length'] = doc.attachment.size
            else:
                if callback:
                    content = '%s("%s");' % (
                        callback,
                        doc.render_as_text(reminder)
                    )
                else:
                    content = doc.render_template(reminder)
                response = HttpResponse(content, mimetype=mimetype)
                response['Accept-Ranges'] = 'bytes'
                response['Content-Length'] = len(content)
            return response
    raise Http404
