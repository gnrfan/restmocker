# -*- coding: utf-8 -*-

from django.contrib import admin

from documents import strings, constants
from documents.models import Realm, Document, TextSubstitution

from documents import strings

class RealmAdmin(admin.ModelAdmin):
    list_display = ('name', 'prefix', 'document_count', 'created_at', )
    search_fields = ('name', 'description', )

    def document_count(self, instance):
        return instance.document_set.count()
    document_count.short_description = strings.DOCUMENT_COUNT_SD

admin.site.register(Realm, RealmAdmin)

class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'realm', 'use_attachment', 'created_at', )
    search_fields = ('title', 'realm', 'description', )
    list_filter = ('realm', 'use_attachment', )

admin.site.register(Document, DocumentAdmin)
admin.site.register(TextSubstitution)
