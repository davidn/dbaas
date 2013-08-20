# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Backup'
        db.create_table(u'api_backup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(related_name='backups', to=orm['api.Node'])),
            ('filename', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('time', self.gf('django.db.models.fields.DateTimeField')()),
            ('size', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'api', ['Backup'])


    def backwards(self, orm):
        # Deleting model 'Backup'
        db.delete_table(u'api_backup')


    models = {
        u'api.backup': {
            'Meta': {'object_name': 'Backup'},
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'backups'", 'to': u"orm['api.Node']"}),
            'size': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'time': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'api.cluster': {
            'Meta': {'object_name': 'Cluster'},
            'backup_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '24'}),
            'backup_schedule': ('django.db.models.fields.CharField', [], {'default': "'3 */2 * * *'", 'max_length': '255'}),
            'dbname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'dbpassword': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'dbusername': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'iam_arn': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'iam_key': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'iam_secret': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
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
            'tinc_private_key': ('django.db.models.fields.TextField', [], {'default': "'-----BEGIN RSA PRIVATE KEY-----\\nMIIEowIBAAKCAQEA687jO0LIMhKDXWEdFXZstTfQMwzyYJ985H2ZAWPtzmzo+aSk\\nzGVZih+8F2qw/bJTI1Gi02R2XPJBMMDYy61OD9BPKK8c7vG7We/hJOcV5+BSrASQ\\nIT1I4SN9weGKSE9O/TOD9EYRIKFh6CW4A0oEIHN6GuWXZv5k2PtUSTJBFkARm3Zv\\n8/qHU/fSdiTgEesWt8jBrwi8IUBVWirFypDKn09HjQjwD8Uacoodwnv+6VyAhx8n\\nR8cVKYJzvNxdu4hUXgYwuhxSre3P8iA3j2CZL8x80T4busgJFpJ59HYCg0/0FvcB\\nihfSt1C1M2TI2ZTUN/so7q7p6Sbz7/xrSsv9sQIDAQABAoIBAAGJUIuzTLCe1EJI\\nfrMEGYM4wN+ERxQAFgU7GEMdDpCYvw/ZVcWLJ4Ex4bzZUhvlDIufXYs5DVhfr7MM\\nnpz9HRQXTFy8f1jDNHBKktH1u3vOR1udj/7XcmEdJRWdTZRZB++4ZTSzPCtVQdkM\\nXd2PnuVDO1lvg4QFRkzvnkX30Nq/Pun/MAHiwmWA8mAJwnEBwaR1cBgDbRtZS5tg\\nnl3fqdJKj8A6xRF7iDCrebrMhp9/XYLUTyYLRTpDOOI/95kG9ud98CZj+3tfNHrJ\\naBHOcsQXlhK4TL166WXc+QsFkIN5CyY/3bjLwXA9n52n8+y+brwlMaIpYcsB8/Ir\\nkmb7YtECgYEA7UoelyMtgTbrwD92R+m8DsapXAVz0DYpue+H+em1gT/mOOBJU+mG\\n0zG+LaQ04j3m8mP844WRos2cWF1jIw+TQ2/KDavhEmXAFxXC0hXP4MTCKtmfn0i/\\nbwHTWgwsU5S9dHhuTqN39fqRMRZPVFJ63+esZutJMZwp3CLO7PcM8E0CgYEA/mbd\\nijuoSID2j4ZWxnYBE82zv+vRZvUKCyAopTaSU5eJaCFYT9uKnXb0d3KolSleKxkM\\nsdxWQhOvdjf+aqM6DajIpFt94CT+crh2EDa08tkkmbo+SQSHLRnri9OKHJ+zGYXx\\nolEOCRrWYl9KdxuSLFK/mjsk/2lRp52BFa00FPUCgYADucczLk03myomcZik1mmq\\nfboJBNjlqwQKtFUZOm8sIVm3COZ918vTIxPOWaau6rPmmGVPGTjJKptK0+SLl2ID\\njAzLHCjDhi927VOKwubpq4006QfVk2nWD1xHLKvBgDNdUcrBl1V52j5PW/9Q3p6p\\nR1TwpL8YdVA+8Zj4JYThfQKBgQCAEIpPju6M6Ra1c3v1Vev+6xskbvKv8ISIyzyK\\nxqjsmakbGUYalTr3P62a/8YrqHJ2IZsJYhCuHLjEOzXAusB7pc6zJjd8gULxvzf3\\nu4JlibfqBx5ZpYTiyFyRvACXnjELlSjpfAIjxTXMuYmD4gY4d8NqQYHDbWIkjZ4w\\nqktAjQKBgCunI104n+t0Q26Bzay7L5LVOeEDRYpjJ0g2ZyYb4ATvLCBGjSZRJ8Et\\njQpgQT92q0ggXbAwkc7irkaO5+XJvrR24DDYpg9iEwqWqlKWG+xNHBP/Q+obj0yh\\nnAMIKQuliWQilf1S4D6DduprUc+MLdyP6s6Lz9hKYToHMl+kX3Eu\\n-----END RSA PRIVATE KEY-----'"})
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
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'lbr_region': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
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