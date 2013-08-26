# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'User.is_paid'
        db.add_column(u'api_user', 'is_paid',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

    def backwards(self, orm):
        # Deleting field 'User.is_paid'
        db.delete_column(u'api_user', 'is_paid')

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
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['api.User']"}),
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
            'tinc_private_key': ('django.db.models.fields.TextField', [], {'default': "'-----BEGIN RSA PRIVATE KEY-----\\nMIIEpAIBAAKCAQEAvE4kpji+RMa+K7TUriOvEuMlgaFysYiE0jBhD6C0j0c8aPeE\\nxxtn6L9FrQIovGOMWShYeIE9RPu0B8LQvJ/KZTBPJVzf/emyP4Mu8qdydaX5eIpD\\nct0Vblz0p9JJ+PGh+wKbLNOweETtedtUJLAfbp0XVEn3PXl9gIj5lkPEx70rYQk6\\nX0oILu5EfkQgz8X/ZpbxdmBC8yHs2Wj8u3wLptDTaiZDizYSN56kcyXzRNseHnoE\\nxjsY7h9aA7ierc/Smx1jNc6dOlyxyOX2oHz5A1+tnDQaBGYks53PxIUlBET79ULb\\n/nuQDeQJSyW8r7fNZmQWb6MyF+NzpAfgoo/8FQIDAQABAoIBADN95tWxVI44Do6j\\nDzljNp+ij4IIJPXZEADuC8ybNGStpR5K+Pr9SofBrgrmOT9ytVE4ECE7rgZsEcnB\\ngxThWRYchLgB0pp7SivF8pOWKF11emd034bMX+zi7F/ryCCT6qhaCRbT+ECbEJku\\n2a6CnsW/nT6GT153F1OLoTxu4aOAZZo5zlb259eUKPTuRFjW2Nr/U8a/c5QNuYBj\\nKXT4FOENWlbT1NTa3CTV+ZZ25O2C7Rc48ycGDFiVc9588FqcXx4TK/GiKvn17MRD\\npKIlGztmdZhiePKb+A0XEaHS+rYBWCeL1kBtykulUEvzefDqR+q4WXyxFhEW3fgO\\nl4SxBcECgYEAyfrEz0dzqv/RrgeH9ejOUbeO8MpUGXtoP8fnfIeUTrZrKhIAEdyr\\npRX+Q6JUN2SmUxV9SNLcneznu0LhdzeCI/99IGVACCVfIWDqSGvpnY8miPjxTqww\\n2qR0W5Z5PK1QbG+bI9IzJao4y0ffeEDsWb60/1wffMgshCjvkf7SdvECgYEA7qsd\\nXpyDHUCKC6CdfnBbZ+PMEPv/NxaZCpcTG/MHnB/rcs1MIBn/DGJK581ItRWtP8xC\\n8G8PLfxZVyEqmDgrAI3Z6iamizHrOeTezD/kmr5EL3fKe2QF4evcuB7WsEkvEcJd\\nvaBC8sou3UHcJW3OT6gxw/6bgqeRWdyYhTfd/2UCgYEAq0r89j1Gn1LtZIYGjEqw\\nDyV5GES/Jg0+0Dic3UOuR0L1h2xUmtFm0E7ioEFe4st9MyEaa1RIvbZYoLuLsytk\\nN1tJptu3fjETiJ9Ekb7TFUh+CdP18h6eIA8wjywCDa9+cTgFfk+aCOtf1yZRIw8M\\nYuAVaCucmJq7BiohYtOVckECgYEAgf7R0GaPQ6+TgSHKpsOsBbodvGKFcAvu78W5\\nss98pZz9MVqAzDtcn/Ipungl0fwskUNAcpULP5DjWIHIIYD2aybYOqEytT5LUQ1I\\nDRf//AkGOpSUxQCF87f0UJT7eqlh6dpkFJTl4jgdroXg0sIsTVbfRFG5gkCi+r8c\\nk/MKB8ECgYAp/+2Lzq0YgcIhjc9K/ISuPWl0E/v3cj4QDPgjaJa/gk0CD4htXTiL\\n72WRMDYaY4aiNcR+MS+kJPm5gb+AkHqtjSYM78vGwRO1pkAP8JCh3yCU5iWuFuhT\\nibFJb8RQXAiap3jQt0clMGpekQMLDqkRaVNOJ8SnkM4QZts2AzE7gQ==\\n-----END RSA PRIVATE KEY-----'"})
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
        u'api.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['api']
