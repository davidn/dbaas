# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

# This migration migrates from a amazon only system to a multi-cloud
# system, including separationg lbr_region from region.

# Specifically, we take value from what was RegionNodeSet.region and
# use that as LBRRegionNodeSet.lbr_region, and prepend it with 'az-'
# and use it for Node.region

class Migration(DataMigration):

    def forwards(self, orm):
        for node in orm.Node.objects.all():
            node.region = 'az-' + node.lbr_region.lbr_region
            node.save()

    def backwards(self, orm):
        for node in orm.Node.objects.all():
            assert node.region[:3] == 'az-', 'Cannot migrate non-amazon instance to amazon only code: %s' % str(node)
        for node in orm.Node.objects.all():
            node.region = node.region[3:]
            lbr_region.save()

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
            'tinc_private_key': ('django.db.models.fields.TextField', [], {'default': "'-----BEGIN RSA PRIVATE KEY-----\\nMIIEogIBAAKCAQEAnYxcGaboJBgYNPZfuM9171tEu9XUMbACcUoQEX+6//zd3Ex5\\nwE0DUvQ2nDrIXlen07h1eJsVyznaIfpJF2w/pyzyHmZDQ/h7RPknX4VYs4hu7Y4q\\nVWko6hHhw2sKMKHcSXlBfJrahQLDkYhirgLpl+OTe3+apatXUIE2Kk7Ft3RUJPtE\\njmNXVkybZPPUqzwqjxyl4T+X14aI4JfoHsr2Z2a5tPlgcq10c3oB5IKDDyCJX4GF\\nmE8WJ5QM8JW1TDIz2W2diFG5hjtzR/ESuPW/reqJSifXIaKcuS9tykHGg6CiGrsu\\nVh318RfwKpxG4KSUHOVHw6BEdMwEr7jEZKd/0QIDAQABAoIBACsOrDEai4Ep0JvQ\\n5bJFiK7E29EWDGsT9mbt3dxac0n42s2VXQTwR0NJmQ8zhYU7IZPcasZuZBNpmTMG\\nCynKnM7cmsMyIZoW8+GS0m7pq6dNVzu3SdyT4+msv22/+EX4RpMR/5LFY4lMixRg\\nGNAD3cF0Id9zrVkvrapD1gDUDHcpdvWTRBXxBa6+LdDVh2lVQrIt+xHdah0lbS8/\\nOfavHvAQa9hr1ggDm3GrWu2pecqEQZQQ+DdOABYPitv7V74dmmPHpjTNu0QMqE3S\\neK4RH9KFylxVdu0wrGOFaluA69t4aHsVDLagiQ3+bPs0YBg8hW/Lk40KVwI9qtKO\\nnlyX060CgYEAxKvne6utSEE/6fDKMRy4pxlNGNf2QcN4N2P+gHnFhLflEVxStRwg\\naprrAIkfTr7Gc5XANE/lYhqNY0he9wfm2DExxSMrnZqY0NoL5vAgkDu+9vpEukgi\\nGjMUcelJw1Y8QBMTIm1zd+5n6paFjL+rYODgozkxerLMcc9/WKl6sJMCgYEAzRMj\\nHI2fwMoDjVI2TIPTy9jvw3c/wqOezOkXOOEqIANqN/MBKljM0jMisxMWmi3vFk/1\\nI7aUVVwOhmOXPQ1u7QKqEoDoE7DdL/qu828pdTNJeVOIysyO7/ndyJGGYPYwbdCF\\navJpAbnqZPIo1PZM48LttkT4itUKhWxNeZPz4IsCgYAtBFArDaPPSygvCy+syC84\\nCGGOUziJ2w00WI4TqEve0hz7uU8xJ2wAGs+5wqlI5AAWyutAzhzqNLuyQwmBr+xW\\nBgSnZCKCo7Vg8NgSl1pMyXAvph9/KC2uI40FeempbZ7C59rUYYsxo39jwep1yhWX\\nSkIA+oFp3W1Qi7dRexGbQwKBgDmQUZ7GMj2PdwfIN+2qY10o+8RGSON9wimKlDYn\\nHgf2bW5fC8izPGsUZ30Uspd8pUwCDbGEooaDXKBkfCNrDeQBh3PCM2KzlqLNHya9\\n4UlAqDMiO5eRa934qUSPdMTq1hU9HvYyLT+KzDyhrMx6hoK4SLmNCqcNvfJNwEGM\\nQjyZAoGAHOr+8yMC98qY3W/sfSRoNFv35OUoca8wosavELizl+EttUBkCQlUkhbf\\nOpJuB4f43ZQDuB3Cfx+68mDtXYnAEzUObLK8lyDYcj6M/j/lpX2r6/uclU3nUf8u\\n8i7pskZ7i4SDA4qA/M0TKHjy89Uv53Di4uG9wd3FJDYgtXstBm8=\\n-----END RSA PRIVATE KEY-----'"})
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
