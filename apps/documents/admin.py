# -*- coding: utf-8 -*-

from django.contrib import admin

from documents import strings, constants
from documents.models import Realm, Document, TextSubstitution

admin.site.register(Realm)
admin.site.register(Document)
admin.site.register(TextSubstitution)
