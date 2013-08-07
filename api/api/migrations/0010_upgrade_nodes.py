# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        for node in orm['api.Node'].objects.all():
            provider = orm['api.Provider'].objects.get(code=node.old_region[:2])
            node.flavor = provider.flavors.get(code=node.size)
            node.region = provider.regions.get(code=node.old_region[3:])
            node.save()

    def backwards(self, orm):
        for node in orm['api.Node'].objects.all():
            node.size = node.flavor.code
            node.old_region = node.region.provider.code + '-' + node.region.code
            node.save()

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
            'flavor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'nodes'", 'to': u"orm['api.Flavor']"}),
            'health_check': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'iops': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'default': "''", 'max_length': '15', 'blank': 'True'}),
            'lbr_region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'nodes'", 'to': u"orm['api.LBRRegionNodeSet']"}),
            'nid': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'old_region': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'nodes'", 'to': u"orm['api.Region']"}),
            'security_group': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'storage': ('django.db.models.fields.IntegerField', [], {}),
            'tinc_private_key': ('django.db.models.fields.TextField', [], {'default': "'-----BEGIN RSA PRIVATE KEY-----\\nMIIEpAIBAAKCAQEAlMp8P14MHOgsvgCinPLwaS0AWQskCiS2EdUHDRpEG0fqgias\\nzakJN2wCJX895SVKrQXJeORtTQ5YXEzzEVfoucMK9flM15i6VZICm/wwcnSQcJHY\\nfsIs9wdQM+w0rnGRtMMJ2PB61nwdW7WQAsRqji+7zYSoMISaaAHA62xxsQnLGgU+\\n8QLPnrErzpcjPDinf7tas4eJgbeJn8U0JIZnaIzLBbBshKKpCBanp56xtKOd+vY5\\nesXm0fBgcsP2oV9QFaxNLbC4fNEjhR3jBRsKQEaw2yXt06atUUQUo5ohml+TLNMW\\nDBvcL/dXSEROCLrigVJIySmSu08Ld7rIj9YgcwIDAQABAoIBAQCJINTB0ft36MLT\\nmeJEo+HODRt09T+R2aOza5HEEaETQ4RtzxcTs+Y6neCcjliNB4F7VQoJ0PyrN71X\\n09Nw+IQUMB259LlNOgUBOEAPYq2DzsoP9VqB+JNYV/Ui5V7oJuMSpW498eREKL8l\\n9n9zDXLm+DctgkU/8fYcRQF398oQTn50hVhKaE2Bk7oogk/QJ3+2kEYvcRiTlzWp\\nQzuPyrYJ4OlltW7KX7FGPYxrZHYmZr3GGnY20LKhnull10pJRwGWDv2yYmclWiji\\n8Y7/zbx7Au/lfyFfDkykbN/vPDZLJxflLyX6lUf0p2pHJHW/2/WtB3T3OvGsCm9s\\nln/bsEWBAoGBAL5LM4SBk5nwzWHtavPMCKh7vxtUx0DszyN1VMaoVL+1t1h0j1w5\\nawj9FL7tQ27wfoRJ7pvJkH4jjpS9jS2diUhEj9DcDt4jVEwy37IJaQRm/L6xHGMW\\nvdM2e+nr2iQS2FCp14lXr/0W5HAZlniB34sasyQ3GKSBZDCVDKi+OYlfAoGBAMgq\\nsR965H7PLnhzQpi+ah0iKbJz4N5L31ctP+t4xtKJtWzXqUi3Y1DyMTt93LZYD8n0\\neGg/ub4vfpH6Pw7ckOGmUV11GU1DK89mNDbglVpgYMDTyAEDpD3qhoD+kJCFKnn/\\n710OxT2FgxKoV/537iufU6gi6x7Ael6v7gVLRT1tAoGAXWZ9z9DlyI430JP+hdEk\\ngsXSRDD1Z7mT5dyGEse2aS5g4mq7ntGT5qKJlzjPe1lRT88V7aMeZ7s+FWWAMN58\\n7lqwmBwatA91Jb1mrHUP9Zgy/8ngnAYif9PjOCqKNGCHifgDEadXewrMbvUwNM/S\\nD+239dORJdVYfrv5ra1IglMCgYEAi2iQa+hfc6JAL0u3OkKEDT5Z5BuopaoaJtEx\\nD4LSlpeqb9/T2v0+goXrnA+QxL6YYIOPyKt5ZegWMv0jJeqgTUhUqs5/jLwXqx73\\nhrDr1EIDoMjfJzWuEiFhBD5H2R+l8co6n4lF/g8atsfgYS6OBnu0/Ak1z/kmQQQu\\ntikyVBECgYAIGm+K2Mss31P58iQMCOkydhePkzt9f0GTFDHvM/SLPYzCI/SKpBow\\nKmkmKylqiQJaCteHg2y4TKFHKxCIvkMndIsUrzJ7bOwivxgAYb3QmK0bAjR3M9w0\\n5Ek06u54eVpOzaKO2hV3GJ/vx00Tpvf1ATkznT3n8Hbug5SnfnUi4g==\\n-----END RSA PRIVATE KEY-----'"})
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
    symmetrical = True
