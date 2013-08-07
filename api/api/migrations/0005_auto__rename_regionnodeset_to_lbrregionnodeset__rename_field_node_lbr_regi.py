# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Rename model 'RegionNodeSet' to 'LBRRegionNodeSet'
        db.rename_table(u'api_regionnodeset', u'api_lbrregionnodeset')

        # Rename field 'LBRRegionNodeSet.region' to 'LBRRegionNodeSet.lbr_region'
        db.rename_column(u'api_lbrregionnodeset', 'region', 'lbr_region')

        # Rename field 'Node.region' to 'Node.lbr_region'
        db.rename_column(u'api_node', 'region_id', 'lbr_region_id')

        # Add field 'Node.region'
        db.add_column(u'api_node', 'region', self.gf('django.db.models.fields.CharField')(max_length=20))

    def backwards(self, orm):
        # Remove field 'Node.region'
        db.remove_column(u'api_node', 'region')
        # Rename field 'Node.lbr_region' to 'Node.region'
        db.rename_column(u'api_node', 'lbr_region_id', 'region_id')

        # Rename field 'LBRRegionNodeSet.lbr_region' to 'LBRRegionNodeSet.region'
        db.rename_column(u'api_lbrregionnodeset', 'lbr_region', 'region')

        # Rename model 'LBRRegionNodeSet' to 'RegionNodeSet'
        db.rename_table(u'api_lbrregionnodeset', u'api_regionnodeset')

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
            'tinc_private_key': ('django.db.models.fields.TextField', [], {'default': "'-----BEGIN RSA PRIVATE KEY-----\\nMIIEpQIBAAKCAQEAlMYdvxuQJ39HESLAGQKeXnf41Yk2+1KCxGFw1a+KJehgNTZl\\nhw/y8/h1JBF6xunqV9hQegjEClAaAlHW/uSgtSuWrqqneYuS3zELNttewpbGICPC\\nHsbw31zFCr2iW9SHDvImCL0auWUop9RId65nXVLklCU13mnTOcJckVmyQPEeHBDA\\n5Y2+xNS9mxkU/wRvkUkeFzcGLL0rxadkemAL9LYMLHeBezY/UNQ/V9jatWB/KPtn\\nZVfX3CE68yIfD7VTvSsAfsQ7huREpf0xDNXDAvea+rZ76o9G+JhkI0aMTy/YFl2X\\nPdwtAGH5Z7Oj4NSYdotpNIqh4JEQEa28QySrSwIDAQABAoIBAAxSbFxLuCDNVeGB\\nc0+e++bvINjuyHMAXnxNZb8NDvAc0vsVSktpcsHqLimSmQyoixRDgkbZOwNvpvfS\\nN3BdF0JqHczRrZVPjhaWRUuB19NeEYLP82ABMioN0PQWyL+6VoVSYPwQTYpVaoyb\\n9HSVKVJ9bxkmC9QkB66c/nW7bBwcu/6ynmsfkytXPKxH2M4TxGVCC2ktdm9L4HWQ\\noEEjSwGoc4WY0dxrtDCEtDhvEQlyd6N0d8tllQGilNDISlYR5bQnljTUvZqRvVHA\\nqzSlfDqOvdRmO9/bmZPJedAUgYqgw+emktJ9H5OrAgnh7WetcoEL3VZkQuBbR5fJ\\nnyXMMUECgYEAvd3ycnXeN0TgqMBEk2r2/eAiiQSjhmXeCaLnct5Kh0dBUlo1ungR\\ncmuWPd274DSS2NGXp0VYSlPMZSQN8XmZXLeihQS+5TlCAXbOR6uuBb2aVpjwwUlc\\n/vFb75XY7ME256en7DFkL2vVyuj/Oje1cV5XzIQMwgXaI81LsL/aMbMCgYEAyJf7\\nWm2EOFE+OIhdanjcFub9bLzjINlwaA6zmHuoSEOl6IKhQrWIwcEq6skAzNNEcvAA\\n7rpwWO+LDR0g2/pFquX3rOI0wzAL6ZlM3K2Gx0R4OdujYa0bMr1UVqwRrGx46f+q\\na8zlT5s3ldV8areDaZIlumPS5XwZNnN9EoU1ZAkCgYEAhqX5A31dixqYrHQ17cnk\\nwaSLOVqF0ZE6huD1fLvyZL9+rrV09vmhfeCYmuU+EMGYBpWVFDYUaBnHkU6haMeQ\\noHVGl0kHTC5wBfPIVIGHF2EgLBuoWZr6jX6DcYR2Y2ie1GhMqS9Z2luCMbVNE29g\\niLacU1iuZ4aY7dzwubdFOQsCgYEAtPoqFJPqTsU91dNyNLWGHEObMZfZc7G58KgS\\n8OfgFBK0hOoWhBE0qVqWVe2zgxi5ENnofXpIEnVMhzBYjR9n66A/rQMJh3C5zrA4\\n4IDOsMndjpXS+jUr7MNUbD4iU+Yp0TSRlWDvIrtvkwdhkQaw0XbCA0A87j7goHfh\\nx+vXF8ECgYEAlHFOfAd9l0KUIIo82NdKyQ1ubKp+56vZefZX5Bz8Tr8LGF3ohiTf\\nP1iJVjahkWUjlcQq8DI3+3CYbRM0+QbfUrjf30Y1f5zJmAmG9fI/ikvNpPigRcaw\\n1S53US9c7/zsWzul+13Gm9cQnCYSZW91HbWpNsG7b2Y5vij9mtqTDNk=\\n-----END RSA PRIVATE KEY-----'"})
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
