# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Flavor'
        db.create_table(u'api_flavor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('provider', self.gf('django.db.models.fields.related.ForeignKey')(related_name='flavors', to=orm['api.Provider'])),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ram', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('cpus', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal(u'api', ['Flavor'])

        # Adding model 'Region'
        db.create_table(u'api_region', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('provider', self.gf('django.db.models.fields.related.ForeignKey')(related_name='regions', to=orm['api.Provider'])),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('image', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('lbr_region', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('key_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('security_group', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'api', ['Region'])

        # Adding model 'Provider'
        db.create_table(u'api_provider', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'api', ['Provider'])


    def backwards(self, orm):
        # Deleting model 'Flavor'
        db.delete_table(u'api_flavor')

        # Deleting model 'Region'
        db.delete_table(u'api_region')

        # Deleting model 'Provider'
        db.delete_table(u'api_provider')


    models = {
        u'api.cluster': {
            'Meta': {'object_name': 'Cluster'},
            'dbname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'dbpassword': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'dbusername': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'port': ('django.db.models.fields.PositiveIntegerField', [], {'default': '3306'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        u'api.flavor': {
            'Meta': {'object_name': 'Flavor'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'cpus': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'provider': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'flavors'", 'to': u"orm['api.Provider']"}),
            'ram': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'api.lbrregionnodeset': {
            'Meta': {'object_name': 'LBRRegionNodeSet'},
            'cluster': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'lbr_regions'", 'to': u"orm['api.Cluster']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'launched': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lbr_region': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'api.node': {
            'Meta': {'object_name': 'Node'},
            'cluster': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'nodes'", 'to': u"orm['api.Cluster']"}),
            'health_check': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'iops': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'default': "''", 'max_length': '15', 'blank': 'True'}),
            'lbr_region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'nodes'", 'to': u"orm['api.LBRRegionNodeSet']"}),
            'nid': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'security_group': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'storage': ('django.db.models.fields.IntegerField', [], {}),
            'tinc_private_key': ('django.db.models.fields.TextField', [], {'default': "'-----BEGIN RSA PRIVATE KEY-----\\nMIIEowIBAAKCAQEA25yIq5omxCjb5O5ATSHR3Hw2i+7YkTxpahrR9kDrDS7M2TaX\\nFzOSVJAu2yUpP3+R2XaJ5t3wdjvBNNJCwpgn2tS4LTkOErUiB9eX9IUhS774hyNW\\nzhlsjvTc9pT7fEBjvRL64QK/o4Z06HDEvFMt2i6P2U0xjZU3ZGG3zTLA/QaA95Zq\\ndH2LoSwbxevMntuiMeCnCU53MkzoBIlFW9ap1BM8xXZTunbKqKiL2NHKGa1L0icr\\nGNaifPsyHbDFm4zDJD/J7UwoJ4DmZu1/JQYJvN7ZSJzZYr56LExHP5oyEYCgZxZh\\nMCYUx/kCVSoaAvajC3rvmqYckXplg6j8MH2w3QIDAQABAoIBAHKn/xLYoHS5gFS9\\nrwSWK6MZlsDoKllpWP/0kLoomo9/Z6PgRHHwku1jeZMgi7CDQfpvUQAfz3NrLywM\\nup4uImC1vpKdvyM1Plcp0EPxXbjWM5sacC+aRns8jECQ99ufInOMfT8M2FDf2hmh\\nBpXsN3w54xBopP5ucUUPX47aeLegvb9O18xWo4ktqA413YMi+j/EgwXhgPIsOZ5T\\nhbh7EY5khfw2U/c29rpkxYfgTcXvYqatPlqoEOkF8ri49m2hyP+X+rdJgHX2+VVz\\nxhmAG4Tm1vO1Q45W6ITescn9HLLXhsTZDvQxkArX92L9oFAVdiAoWXVrcGRBWAOk\\nxDFybWECgYEA4Y4mQhK3xla5K7PVIS7dV4f+rHZ79wrPknQoYSOA0NuEKvUfuOoc\\njKZHBhFO5SrM/iCAiNAAJ+cNxRx2QzM5u1oQ4eLC5RBHUeTPmHY39j90+2kkxXD6\\nKpJRISFHLL2PO8xWVbW7fxTXXZrEtLSPAsVnu0TWCyRBr5kfiUkkt48CgYEA+UEA\\nakIuR0wdsemFu5dBK1bA26ug1GcTqWbcSESKNJkavQ23oOCrx7nAJ2m8EsuVParU\\nBrjWobkC0209ROMV3mts5iGb0ate0LB3W5mhNQf11rsqVOuGAqjUu2RNlXWMw73E\\nRB8iMDZkuWpzvHjrJBejkAzAwvV/m1zxqF4cOtMCgYEAmGjxORxkycS4AuvVTELa\\nldbzI548TcYkVJXg4yKWXIq4WD6iXNT0zaVdwJ/Za8jsE5vqvoeuU0gxacu9rdLj\\nY9GMLtaHUzkYuCGglSjsz5w5c9isXC3nHPUZlQVjjrvYGVQN0oSmWUy/6iQ2XtTS\\n/dBeM5BkActSB1G0mZOvF8kCgYBWIth54BUOHofEi+bjRQoIaBqNz2ns/RIWYK2P\\na+A2/RH4c10aA4pZox98f1W3SRNyFC7hg87oZH9NgVrDC5brHkSr4sFuW8KQa+tT\\nhGvpX67dXiDq59mP4bhiae9FzzGuE05YHEo8Tw/P47HLWB4qguDLTxzuQtiuYBhD\\nDwLCcQKBgHuaI+6N5WStGVM72IuJJMnjGqgd0ZYPpBCycxKCjHPC8azLz5zuzGi6\\nsvIlYcQMJ2nTsK4OBMyBgR2IJvq+p/5aF3HViPNh3zBMJx3MgK7XhDOdTwnBqT+e\\njxBhiF+F3YYxAreTguKAmEC7WxdKbhf6z28/Z/8RKtMkVraRs+3q\\n-----END RSA PRIVATE KEY-----'"})
        },
        u'api.provider': {
            'Meta': {'object_name': 'Provider'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'api.region': {
            'Meta': {'object_name': 'Region'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'key_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'lbr_region': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'provider': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'regions'", 'to': u"orm['api.Provider']"}),
            'security_group': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['api']