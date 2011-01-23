# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Document.sample_uri'
        db.add_column('documents_document', 'sample_uri', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)

        # Removing unique constraint on 'Document', fields ['title']
        db.delete_unique('documents_document', ['title'])

        # Removing unique constraint on 'Document', fields ['regexp']
        db.delete_unique('documents_document', ['regexp'])


    def backwards(self, orm):
        
        # Deleting field 'Document.sample_uri'
        db.delete_column('documents_document', 'sample_uri')

        # Adding unique constraint on 'Document', fields ['title']
        db.create_unique('documents_document', ['title'])

        # Adding unique constraint on 'Document', fields ['regexp']
        db.create_unique('documents_document', ['regexp'])


    models = {
        'documents.document': {
            'Meta': {'object_name': 'Document'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mime_type': ('django.db.models.fields.CharField', [], {'default': "'application/json'", 'max_length': '128'}),
            'realm': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['documents.Realm']"}),
            'regexp': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sample_uri': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'template': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        },
        'documents.realm': {
            'Meta': {'object_name': 'Realm'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'prefix': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        }
    }

    complete_apps = ['documents']
