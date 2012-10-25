# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Document.verbs'
        db.add_column('documents_document', 'verbs',
                      self.gf('django.db.models.fields.CharField')(default='GET, POST, PUT, DELETE', max_length=128),
                      keep_default=False)

        # Adding field 'Document.status_code'
        db.add_column('documents_document', 'status_code',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=200),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Document.verbs'
        db.delete_column('documents_document', 'verbs')

        # Deleting field 'Document.status_code'
        db.delete_column('documents_document', 'status_code')


    models = {
        'documents.document': {
            'Meta': {'ordering': "('title', 'created_at')", 'object_name': 'Document'},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mime_type': ('django.db.models.fields.CharField', [], {'default': "'application/json'", 'max_length': '128'}),
            'realm': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['documents.Realm']"}),
            'regexp': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sample_uri': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'status_code': ('django.db.models.fields.PositiveIntegerField', [], {'default': '200'}),
            'template': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'use_attachment': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'verbs': ('django.db.models.fields.CharField', [], {'default': "'GET, POST, PUT, DELETE'", 'max_length': '128'})
        },
        'documents.realm': {
            'Meta': {'ordering': "('name', 'created_at')", 'object_name': 'Realm'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'prefix': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        },
        'documents.textsubstitution': {
            'Meta': {'ordering': "('realm', 'created_at')", 'object_name': 'TextSubstitution'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'realm': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['documents.Realm']"}),
            'regexp': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sub': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        }
    }

    complete_apps = ['documents']