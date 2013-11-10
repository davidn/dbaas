# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SaltJob'
        db.create_table(u'jids', (
            ('jid', self.gf('django.db.models.fields.CharField')(max_length=255, primary_key=True)),
            ('load', self.gf('salt_jobs.models.MediumText')()),
        ))
        db.send_create_signal(u'salt_jobs', ['SaltJob'])

        # Adding model 'SaltReturn'
        db.create_table(u'salt_returns', (
            ('pk', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fun', self.gf('django.db.models.fields.CharField')(max_length=50, db_index=True)),
            ('jid', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('s_return', self.gf('salt_jobs.models.MediumText')(db_column=u'return')),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('sucess', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('full_ret', self.gf('salt_jobs.models.MediumText')()),
        ))
        db.send_create_signal(u'salt_jobs', ['SaltReturn'])


    def backwards(self, orm):
        # Deleting model 'SaltJob'
        db.delete_table(u'jids')

        # Deleting model 'SaltReturn'
        db.delete_table(u'salt_returns')


    models = {
        u'salt_jobs.saltjob': {
            'Meta': {'object_name': 'SaltJob', 'db_table': "u'jids'"},
            'jid': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'}),
            'load': ('salt_jobs.models.MediumText', [], {})
        },
        u'salt_jobs.saltreturn': {
            'Meta': {'object_name': 'SaltReturn', 'db_table': "u'salt_returns'"},
            'full_ret': ('salt_jobs.models.MediumText', [], {}),
            'fun': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'jid': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'pk': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            's_return': ('salt_jobs.models.MediumText', [], {'db_column': "u'return'"}),
            'sucess': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['salt_jobs']