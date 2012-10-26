# -*- coding: utf-8 -*-

import re
import time
import hashlib

from datetime import date
from os.path import basename

from django.db import models 
from django.template import Context
from django.template import Template
from django.contrib.sites.models import Site

from django_extensions.db.fields import CreationDateTimeField
from django_extensions.db.fields import ModificationDateTimeField

from common.datastructures import Enumeration

from httpplus.constants import HTTP_STATUS_CODE_CHOICES
from documents import constants, strings

class Realm(models.Model):
    name = models.CharField(strings.NAME, max_length=128, unique=True)
    prefix = models.SlugField(strings.PREFIX)
    description = models.TextField(strings.DESCRIPTION)
    created_at = CreationDateTimeField(strings.CREATED_AT)
    updated_at = ModificationDateTimeField(strings.UPDATED_AT)

    class Meta:
        ordering = ('name','created_at', )
        verbose_name = strings.REALM
        verbose_name_plural = strings.REALM_PLURAL

    def __unicode__(self):
        return self.name

    def apply_text_substitutions(self, text):
        substitutions = self.textsubstitution_set.all()
        for s in substitutions:
            regexp = re.compile(s.regexp)
            result = regexp.subn(s.sub, text)
            text = result[0]
        return text
    
class DocumentManager(models.Manager):

    def drafts(self):
        status = Document.PUBLICATION_STATUS_CHOICES.DRAFT
        return self.filter(publication_status=status)

    def in_preview(self):
        status = Document.PUBLICATION_STATUS_CHOICES.PREVIEW
        return self.filter(publication_status=status)

    def published(self):
        status = Document.PUBLICATION_STATUS_CHOICES.PUBLISHED
        return self.filter(publication_status=status)

    def renderable(self):
        status = Document.PUBLICATION_STATUS_CHOICES.DRAFT
        return self.exclude(publication_status=status)


class Document(models.Model):
    """
    Represents a response returned by the web service.
    """
    
    PUBLICATION_STATUS_CHOICES = Enumeration([
        (1, 'DRAFT', strings.DRAFT),
        (2, 'PREVIEW', strings.PREVIEW),
        (3, 'PUBLISHED', strings.PUBLISHED)
    ])

    realm = models.ForeignKey(Realm, verbose_name=strings.REALM)
    title = models.CharField(strings.TITLE, max_length=128)
    regexp = models.CharField(strings.REGEXP, max_length=255)
    template = models.TextField(strings.TEMPLATE, null=True, blank=True)
    verbs = models.CharField(
        strings.VERBS, 
        max_length=128, 
        default=constants.DEFAULT_VERBS
    )
    description = models.TextField(strings.DESCRIPTION, null=True, blank=True)
    mime_type = models.CharField(strings.MIME_TYPE, max_length=128, 
        default='application/json')
    status_code = models.PositiveIntegerField(
        strings.STATUS_CODE,
        choices=HTTP_STATUS_CODE_CHOICES,
        default=200
    )
    headers = models.TextField(strings.HEADERS, null=True, blank=True)
    sample_uri = models.CharField(
        strings.SAMPLE_URI, 
        max_length=255, 
        null=True, 
        blank=True
    )
    attachment = models.FileField(strings.ATTACHMENT,
        upload_to='attachments/',
        blank=True, null=True)
    use_attachment = models.BooleanField(strings.USE_ATTACHMENT, 
        default=False, help_text=strings.USE_ATTACHMENT_HELP)
    usage = models.TextField(strings.USAGE, null=True, blank=True)
    publication_status = models.PositiveIntegerField(
        strings.PUBLICATION_STATUS,
        choices=PUBLICATION_STATUS_CHOICES,
        default=PUBLICATION_STATUS_CHOICES.DRAFT
    )
    created_at = CreationDateTimeField(strings.CREATED_AT)
    updated_at = ModificationDateTimeField(strings.UPDATED_AT)

    objects = DocumentManager()

    class Meta:
        ordering = ('title','created_at', )
        verbose_name = strings.DOCUMENT
        verbose_name_plural = strings.DOCUMENT_PLURAL

    def __unicode__(self):
        return self.title

    def get_regexp(self):
        return re.compile(self.regexp)

    def get_verbs(self):
        return tuple([v.strip().upper() for v in self.verbs.split(',')])

    def method_matches(self, method):
        return method in self.get_verbs()

    def regexp_matches(self, uri_fragment):
        regexp = self.get_regexp()
        return bool(regexp.match(uri_fragment))

    def headers_match(self, headers={}):
        doc_headers = self.get_django_headers()
        for h,v in doc_headers.iteritems():
            if h not in headers or \
                headers[h] != v:
                return False
        return True

    def match(self, uri_fragment, method='GET', headers={}):
        return self.regexp_matches(uri_fragment) and \
            self.method_matches(method) and \
            self.headers_match(headers)

    def get_headers_as_dict(self):
        if self.headers is not None:
            return dict([
                [i.strip() for i in l.split(':')] \
                for l in self.headers.splitlines() if ":" in l
            ])
        else:
            return {}

    def get_django_headers(self):
        result = {}
        headers = self.get_headers_as_dict()
        for h,v in headers.iteritems():
            h = "HTTP_%s" % h
            h = h.upper().replace('-', '_') 
            result[h] = v
        return result

    def get_context_dict(self, uri_fragment):
        result = {}
        regexp = self.get_regexp()
        m = regexp.match(uri_fragment)
        if m is not None:
            result = m.groupdict()
        return result

    def render_template(self, uri_fragment):
        t = Template(self.template)
        c = Context(self.get_context_dict(uri_fragment))
        result = t.render(c)
        result = self.realm.apply_text_substitutions(result)
        return result

    def render_as_text(self, uri_fragment):
        result = self.render_template(uri_fragment)
        result = result.replace('\r\n', '\\n')
        result = result.replace('"', '\\"')
        return result

    def get_content_hash(self, uri_fragment):
        if self.attachment and self.use_attachment:
            content = self.attachment.read(self.attachment.size)
            return hashlib.sha1(content.encode('utf8')).hexdigest()
        else:
            content = self.render_template(uri_fragment)
            return hashlib.sha1(content.encode('utf8')).hexdigest()

    def get_last_modified(self):
        return self.updated_at if self.updated_at else self.created_at

    def get_url(self, request):
        return "http://%s%s" % (request.META['SERVER_NAME'], request.path)

    def get_etag(self, request, uri_fragment):
        ts = self.get_last_modified()
        url = self.get_url(request) 
        etag_key = '-'.join([
            hashlib.sha1(url).hexdigest(),
            self.get_content_hash(uri_fragment),
            hashlib.sha1(str(ts)).hexdigest()
        ])
        return hashlib.sha1(etag_key).hexdigest()

    def get_sample_uri(self):
        site = Site.objects.get_current()
        parts = []
        parts.append('http://')
        parts.append(site.domain)
        parts.append('/api/')
        parts.append(self.realm.prefix)
        parts.append(self.sample_uri)
        return ''.join(parts)

class TextSubstitution(models.Model):
    """
    Represents some text to be replaced in the documents of a realm.
    """
    realm = models.ForeignKey(Realm, verbose_name=strings.REALM)
    regexp = models.CharField(strings.REGEXP, max_length=255)
    sub = models.CharField(strings.TEXT_SUBSTITUTION, max_length=255)
    created_at = CreationDateTimeField(strings.CREATED_AT)
    updated_at = ModificationDateTimeField(strings.UPDATED_AT)

    class Meta:
        ordering = ('realm', 'created_at', )
        verbose_name = strings.TEXT_SUBSTITUTION
        verbose_name_plural = strings.TEXT_SUBSTITUTION_PLURAL

    def __unicode__(self):
        return self.regexp
