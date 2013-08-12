# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Node.label'
        db.add_column(u'api_node', 'label',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True),
                      keep_default=False)

        # Adding field 'Cluster.label'
        db.add_column(u'api_cluster', 'label',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Node.label'
        db.delete_column(u'api_node', 'label')

        # Deleting field 'Cluster.label'
        db.delete_column(u'api_cluster', 'label')


    models = {
        u'api.cluster': {
            'Meta': {'object_name': 'Cluster'},
            'dbname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'dbpassword': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'dbusername': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'label': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
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
            'flavor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'nodes'", 'to': u"orm['api.Flavor']"}),
            'health_check': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'iops': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'default': "''", 'max_length': '15', 'blank': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'lbr_region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'nodes'", 'to': u"orm['api.LBRRegionNodeSet']"}),
            'nid': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'nodes'", 'to': u"orm['api.Region']"}),
            'security_group': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'storage': ('django.db.models.fields.IntegerField', [], {}),
            'tinc_private_key': ('django.db.models.fields.TextField', [], {'default': "'-----BEGIN RSA PRIVATE KEY-----\\nMIIEowIBAAKCAQEAwqmQpBi76bs+N5WAcXoUtSeipexisMuCZgnyDXzuU4/LcKcu\\nEuZPXBj9R5hReFWyIAeDwVwJXUks0BksCC8jWX3lQB75TIiF7XIbMU1cYuBzSCUD\\nyJBwF/X0VXAFoJlCQ+RafLzIQ735eGEyMwdD7N8BvqdBGnVyf/6waOEQJWtbnsK+\\nCxG8DpAcv0YW6gS0MxYZxJ+oglsPTS224g8PCAS9sQAjuqN0gghDOTHb79V1Inzg\\nW5NBMrh+P8baKgln9bf7rUfkznimld8OKwwcBZBez4Hs0EtjrblSSCp65ACSN8RL\\nkKwBdAPxUjQnkhi6el2jYpdJQDLPOrX2adZsAQIDAQABAoIBAHmmdhnWyzhaJ5uc\\n9lP0MxSy3FZMz7Akviz+ciIzvMzDxCN2lriA7X9kroQbkG5fP538lD42QjPmEvdJ\\ng9bpfnHi122m7a0CdI/bC1tYOTAhjGm9mAuzGBohPrxV8W5X2K2M+2+QmqabBlhQ\\nhYqWM8DH7NM0ut7KHvAWPjCM1gZLZNdzyIArXhmbl5P48xvgWTbioGeC0wEXIrB6\\nN5fqLSzi8RI4zzku33ZZkknMWmpfGoPsQ2CdNrL25MeBs0k9Rf1EnFSeua2l0pFS\\nf3BPn8uAHi4F2P1kbJ661wiRv0Fz6gBlnrTJ0QEFWQxod6nB10FNlYU1pyFfQiem\\nhmzXAQECgYEAybl3QPkgejcZTY5rcd9xJVZ1ZEesjrupmM8pizs1aHp3ZPdAtrfH\\n2SesWuadDlchLv5Ilmf5FxenhdBfZbnKxJm0bQAzYQCmQ4VdI2mFGyQhdMoaCoKz\\n3zxWpQMZpPr5neTdDV9jL9gfq+pII88lKho05cOe9yrmAqNRhK9DxWkCgYEA9wmr\\nZfFwp8unAbLQP9nsz1kQ39QwHa1TzhptB8KKtgkJ2LSvfYAU+8E2bMOzZ56YZAaC\\nTQV5qmRjdIHdjIW+R8jbt+wkZuyAwK3Q8eoDHWnyd2vqZyVUP4qdxYaeBoUfYpuQ\\nEKXkf27lyIhkAD9N3dBDzPriV2PK8IBvlRYSptkCgYBdsrkSw+Ty/67QGGwN25Sp\\nnCww5R3guog/Q1JvqpPXMLNOgY5ckKbSVhw3qNCgvZXbRx+eRTMtJ76XaD83eAIY\\nKbDlxGcZEn0n9cVaUoQSJEkp/0nzQdycv2EbioIZ4L2bOpf2wyzGJ2QmrU7O20PO\\n95dEdgXbluB5rzSJJgObqQKBgQCXyqQ7boBHShZjL8lQAorE2ThKICo0ggUFli06\\nYGo08hbPxi4ykhnSm2Tirdk1qTh/9ZPo2Z1peme19fn411EU8LE5MOspJtbyDZte\\nmeiyESCACposKL68kGLjNRUycmfXgjiiUhy1xKGCd3PixwMEcWzHrbyX7+SJpJFr\\nbPWm+QKBgHRO4d84VX98du8cIHWGtWE0SX5hKYHkyqQCZxb3mAos4eoAY/E6Geez\\nIMFhq/P21j1VAjm314S2UMqop65pnyvsxD5rLgaDaDOIwI0+KvUu0eaEazuLoJhS\\nPsjHWJhJeAxiNMc55TysA+3SGn/Feuesp6EMoOnYG+fPmg2+mbVw\\n-----END RSA PRIVATE KEY-----'"})
        },
        u'api.provider': {
            'Meta': {'object_name': 'Provider'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
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