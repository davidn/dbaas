# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Node.old_region'
        db.delete_column(u'api_node', 'old_region')

        # Deleting field 'Node.size'
        db.delete_column(u'api_node', 'size')


    def backwards(self, orm):
        # Adding field 'Node.old_region'
        db.add_column(u'api_node', 'old_region',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20),
                      keep_default=False)

        # Adding field 'Node.size'
        db.add_column(u'api_node', 'size',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20),
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
            'region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'nodes'", 'to': u"orm['api.Region']"}),
            'security_group': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'storage': ('django.db.models.fields.IntegerField', [], {}),
            'tinc_private_key': ('django.db.models.fields.TextField', [], {'default': "'-----BEGIN RSA PRIVATE KEY-----\\nMIIEpAIBAAKCAQEAprtgAU2B/eZJlJL32dY/wxwqtY+NuDIaiLkyY3BKawOpgxM/\\n3ThT87p5FEmtJerZfYPPN38m1rp3IsNASY4io5Gd9z5M2hKiJ3I2o3IG1BrtNXbY\\naLZA6HwPG4y9Kv7CQv2V4xYzATVl3ORSuVHBbgbFV35kAfonEg2tEkxK1gw2/cIl\\nPLOkhR9csJkxlnVHxxnBe3R3FGH/t3ZzltK5y0KmPadNoCCMHn8xOJgi2qYsI8aK\\nF9dMsdGkpmus7F/ojsvJqrzPcK087l5ykk0DA1lBjZ4NC+NMATp6RpH1czJ+aMys\\n1ZM5BS9Nul3RkWUppD/3ftU5uQtYqgs5L91rBwIDAQABAoIBADITRpM9lxQNbP3t\\nYfkPytirhfw/oB25FpUHoiWRXRhk4i1Ww7CKMVSbJbA9LH6d2TJEOyD81EpbeFp9\\nb7pnsOmVW28dS/GW9RKJz/Uo0vozGBkdl4NjcX0hfVwV2d6m4utBxBmO2kS7p9s+\\ny8WS01hbOju73wdk/QUEDH3ZYgSE667VOAEzI0IUX8ta6gAoXUYkeLP+ZSSHEHUp\\n6/hkf4y7p7VtZwdde3PTh8TS1Gke3Dv1KBtb+ibuultRBiIyahlQ7ze+s10Bg2vE\\nR3LPU9dcfwanlxga2ggdU/v8CeaGWYkKXFLJAtSL87ggbHPdx/l2G49JhM/5qxrq\\n7tRKYzECgYEAt7uE4yBDpwkZoWQIqWQem8m/BhOhlM7kDikFMCeSuCqRTYtP/jfM\\nxTSu5k2pJq4tsTLkZ+x61g+sOLuw/VBNJZR8WRtq9rGoBHGR8cSLGm1zWMeVTOje\\niCaugRqGhhYhIvq+6G47KZYlQfFEGBGu3ujIVCr9msWWt9oVISjHFnkCgYEA6FAG\\n7wW6FIqiETH4hkinAVRUcGfz2klkIGbOyfP8E3TEsaGxFe+28DDae1JtvWtxX8//\\nq2qij1VOswVcYrORegegz+zSbI1GAwCouG4MUj0PzAqA55NNJ85u8Tv2wblh1qHO\\nfNDicAyV5c57sT/L/P3MMND12+DdEQWSeFXWLX8CgYEArOQyKiAkSTxQ+APP+sYR\\n33s63BcBB6ygAYssLKIweEjmLlgX0Brl//SRWHpf39wrdwFy2TA4btKUt1Y3OEem\\nMOTHFnqsbrPCbVwJf735P8cascIthg/jx67OqwIw8GBGkknt934zAfEd4i2MbDHH\\nok7epAVIW6nvJ9Z555gdr9ECgYEA2qImRGFRZO+r4x7yU/6gHeItrbRHjRIxB0V6\\nLBpRDEaCruILdSerNZXkqNdErFYn1xI7/ilXYCna7SSIc+Onb/8p20V4K+0xDLZc\\nE2aOdf89lLv14PuCS4o+Yw4aBuvfJk4VtOYplWZi1GplgsUVx71bpD2khRC1PMXP\\nuSyfayUCgYB0M+vu8zlK6IaE25i5GQXZ7F9uJG5Q9jzrFMIe7h4FyhMYsrJLJl4Y\\ngQvtu3PZDBGI9Ugo1MDL9uMNYoUmVWqBTvul7gBjG41SR+s0+/d2mK0CyLC+EE5f\\nCYxKx4sd5wWC40u7du9K6alhxjRbCWEaBEdagiLJxi7W7vQBT9ph7A==\\n-----END RSA PRIVATE KEY-----'"})
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