# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Cluster.port'
        db.add_column(u'api_cluster', 'port',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=3306),
                      keep_default=False)

        # Adding field 'Cluster.dbname'
        db.add_column(u'api_cluster', 'dbname',
                      self.gf('django.db.models.fields.CharField')(default='db', max_length=255),
                      keep_default=False)

        # Adding field 'Cluster.dbusername'
        db.add_column(u'api_cluster', 'dbusername',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255),
                      keep_default=False)

        # Adding field 'Cluster.dbpassword'
        db.add_column(u'api_cluster', 'dbpassword',
                      self.gf('django.db.models.fields.CharField')(default='password', max_length=255),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Cluster.port'
        db.delete_column(u'api_cluster', 'port')

        # Deleting field 'Cluster.dbname'
        db.delete_column(u'api_cluster', 'dbname')

        # Deleting field 'Cluster.dbusername'
        db.delete_column(u'api_cluster', 'dbusername')

        # Deleting field 'Cluster.dbpassword'
        db.delete_column(u'api_cluster', 'dbpassword')


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
        u'api.node': {
            'Meta': {'object_name': 'Node'},
            'cluster': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'nodes'", 'to': u"orm['api.Cluster']"}),
            'health_check': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'iops': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'default': "''", 'max_length': '15', 'blank': 'True'}),
            'mysql_setup': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'nid': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'port': ('django.db.models.fields.PositiveIntegerField', [], {'default': '3306'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'nodes'", 'to': u"orm['api.RegionNodeSet']"}),
            'security_group': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'storage': ('django.db.models.fields.IntegerField', [], {}),
            'tinc_private_key': ('django.db.models.fields.TextField', [], {'default': "'-----BEGIN RSA PRIVATE KEY-----\\nMIIEowIBAAKCAQEAiCyWacuZgzsDobTjBFq+t0SqHzrSFDtFyfjsD2wkqAYISmTB\\nIX385evzKXoher3BTAGC5GnMH2Xt23NEQDrDByWx4fz9CpWQ+PqPt7hwdGflptjn\\nhojRLt3Hkq13/JIRuywEVAzlbp2rN/lqD1d0l6MJz2iTD+BRBgUGlggR0qba16m6\\n6z4SA3KVQV5DuoN/qvbKaFpUiIisM1YoaCUp5ADV2HkBoRAw0IVLnJQBNA3+SuWl\\nxoa3O+04rtUHiXRei6wPNq313fs9cA/CV8XBmWHNY+3zTdk30nucZ3Gts7GPF75u\\n1R9cCmSWrBeMQyACq0zzRFBt2DdE7hZtOCOJhwIDAQABAoIBAFrB1NHYF41mJKp+\\n45sAXAHLatL7og5H3uCY3cP9oIS32Ii0lB+dV5Np6ZuoQW4L0Cu3CiTv+lKm3ZuY\\nPFHOmDNIRUFIGuIWAxRd8rFQ5OpAYMgN4mlBAKIKwDubD9AvDlBAKvZVzggmX3oj\\n6jMlZ5i02hH5MaKwL3Aio1wVLsPE5kymq5HT7qkcxlUZ09dpaKtUMxMfWUMtTeIe\\nLV2oZH2iCEDkgUsPPzuOneyt17XBY5t8Lv9l9z0zwq65HgKhTd85rjTb2QbBLprP\\nb7dS5Gc2F1jXNp+8/AjNFhuRX0jWnyHI3oH8vVnXT5dLXJO/J5UB9JM9XV0BVM/o\\nO5Hm6/ECgYEAuSJCbVexhhjPlDAivwSi0kdAqMlqDu41zsvzSUryKzfy9by+DNLc\\nUfggOZd5k1lQlWvPMfhT5kW7IIe4lSo1X6KQ//7QOFC5gJqXGyGxdyTqBCk/mJoA\\nq6IC63A+ZkUqa5LFWqTptXuDkR4XdSGgHkKv6FQP5lCWvq08y6dzDvkCgYEAvEyl\\nL/nHSDLwyze86SRiWyH7Vb8E1G5MgWD2V3gsk4Kww2nhqSwvfBtwYRIQKhG1hMmv\\nTYe1jXFUAyTzGXILzyiMEUuzA82n08YNCZCpkhG1SxipMCcCgeYW7OtRPzOmQTDk\\nVFTPSA2MMBuAVZcbVYqaj2UDmfXVBB2Yp2hi/H8CgYB4OgdpesmOjA5B7gCijCAw\\n7pTPB/4YNBo9cbVMo58g8fSWITxKl6T8lmZXAEezqQzr/FdR3DKgGCitt3XnaMHA\\nmZIQrSoLaGEPY1U+CWN2PEK88QybzWciDtRWkU30nHYv5eDEPNSJRuzqEOCq8GtL\\nO4OBHRY2O5+ptFcG6neOAQKBgFkLpdJaPHNYI6b2ZM+b9SdDmqeh/Za30lYclGIo\\n4mufkhfXKm/mBU6bazl8YUiDt2NkPRJc6u5IeYJDJvMRi6QbeKF1OuLBjmwHbILp\\ndkctOJ6auueaiwUC2jSP04wf0K9jf5ahxKQ+Q908JCRVoQeC1DSbgGh+aI3ZsSb5\\nplXhAoGBAIigXBEy5U601AEnbhiKsw3x4PjHO1lNZBzjcRSSClQBg4EEfFKfI9LZ\\nWeAB4kgtf3Ekhd9mwyaw2B5eGz+8C6zhF88G+n7sTBIpoR+/gZeF5FqlAXBugHah\\nRFDGU8oDGoH2LKlt6CcVxuEWAG5WH72aiXReUrWhzQnXsgt5G/2t\\n-----END RSA PRIVATE KEY-----'"})
        },
        u'api.regionnodeset': {
            'Meta': {'object_name': 'RegionNodeSet'},
            'cluster': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'regions'", 'to': u"orm['api.Cluster']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'launched': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '20'})
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
