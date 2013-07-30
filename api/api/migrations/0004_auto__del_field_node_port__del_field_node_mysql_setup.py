# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Node.port'
        db.delete_column(u'api_node', 'port')

        # Deleting field 'Node.mysql_setup'
        db.delete_column(u'api_node', 'mysql_setup')


    def backwards(self, orm):
        # Adding field 'Node.port'
        db.add_column(u'api_node', 'port',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=3306),
                      keep_default=False)

        # Adding field 'Node.mysql_setup'
        db.add_column(u'api_node', 'mysql_setup',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)


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
            'nid': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'nodes'", 'to': u"orm['api.RegionNodeSet']"}),
            'security_group': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'storage': ('django.db.models.fields.IntegerField', [], {}),
            'tinc_private_key': ('django.db.models.fields.TextField', [], {'default': "'-----BEGIN RSA PRIVATE KEY-----\\nMIIEpAIBAAKCAQEA0A1Zrf5dnXY0L6CJ09ZRuvfhF7NsyNixOZN52t5Q6SHXVtni\\nadTaPHBcQmN1RvuH8QYnz0LLE9pMe1g+ylftN1zmgJEuIIzqw0fdfkCBe9+Yfv9z\\nMXBTgPEioqojQcF2HbQxR45QiQwuMhNbLRRbuZ6zm8wyqgLMNUaLw4v8uFDuyL2Q\\n6GDKGVshtXXhE4j1JWFHTIkdxLDTVKe3iYIWEnzy7hjZtAUNon7qPc+QIq8DV7pC\\nWyhoN+8s8oNm89hRbE8lsPwXeAzx7im5d/HqcMsKFs3YsCeUBQ4uYcjoCWbe45c+\\nRs5mxF166XiNrSYL2B5anxeFOIlEHNTXOnVwkwIDAQABAoIBAQDCUaXQQAL53fxR\\n+5Sfuc4uXfTr6RaS5OlqiFbI2NojVQtGwEybYkXPK3bQPwq7mJTYxlIKYC1CxqKm\\nlb5XyRXznp5fuLmnh1aBvC6hC+ikZSuOelMB+xLTHOWnnlc9xE7o4XMhjUelKS5A\\ncRm4mgot7Y991ZQAfIp0vAYwRyBsmOGyc4jIu7WdW9bt2adPFJcJ5xyBkGLglvjN\\n2I6g3PjglVk554V58gFmaxDC/VIDAe0CePGjs7GvXk3EJV45kMbCRtI5+Z6YYvnL\\nUxO7DmDbrHWyTem8yJuOVlX0chHEVi/jWeEuoa4oy0i5JbNToOBuQF+w2F0hSqqO\\nk7zYBO9JAoGBANFKrZErqddezUzfTQ1IpNIZ7ha8/etgSLecMlsjh/H3h+6M7NUr\\npNHYenLkdHlqbKyIttM2EzBK9ZbAexFDGd+pgs28JXbIbrghbx0aY6r7j2u7bryP\\nlzVSz3CCoPpzZeD4/7DunB/g0f0YzYvnbp9Wpy6lA4EOXma1rzxvRcbFAoGBAP57\\n2nG4HtaNdpbi2JPZ5cNnIfoZyvUo8Jgyn/FSj4HV7qX49JSQPZ+7D0wonqHVLgAv\\nImYr1ObxxaR9DrYLr+J0q9hpOQrIC1LFTULm++2JJK1n2UxnfDSxsYfjWLNc8yKW\\nm+7ShyX1wKiG1BmK+uVbCi62DbfIDXbYOspK5o93AoGAC7eHkgoEvybyjWwu7yBz\\nAcQr3SAFgyjnyUe4VfveP4ChHozLMX/5ATqCWG5LywRXQy2ANsDfQCPiLedmvGeq\\nSig+R3BSFJ1R/YL5qoJwtADTXa+nmmzbhUO2k1Ds3DibqoWmIuyo1uwKNYYu87co\\nLUl3oJfiY1Y/mLZxMgv0txUCgYBAF/2Kiq7pprNpiTS2+DhQIJeEIB7n5CnEi2uR\\nIhQWxUTX9H3VNQbwRfKyYcCiTcjKLxTg2sVCbT40EXM1Enh39p6ZYNcHCh8f96Vf\\n5kEpMFNWgUNPZPj5ZI+sA+yBMDXkTj5zxf5X5y9gwqSE0mYige1smlmWIgKSHh+g\\nd4DePQKBgQDMmduhSZHOdUdXYhpqoRWw1Am2fdBWjkpPlTUaEvL5vio8I5r5u+gt\\nGnHgq0KjrJu3plruqlsSluZKSq+DrripYh0SHsDTCjtmW9FTjl/s3ud9KaIb8WNd\\nk+TnJg+ideIAeu8FjKPpwST7Y+6SfGP6jwHJY5AUzBNbyzmEoFZYhA==\\n-----END RSA PRIVATE KEY-----'"})
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