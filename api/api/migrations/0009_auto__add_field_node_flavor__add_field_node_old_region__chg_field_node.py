# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Node.flavor'
        db.add_column(u'api_node', 'flavor',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='nodes', to=orm['api.Flavor']),
                      keep_default=False)

        # Adding field 'Node.region'
        db.add_column(u'api_node', 'region',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='nodes', to=orm['api.Region']),
                      keep_default=False)

        # Renaming column for 'Node.old_region'
        db.rename_column(u'api_node', 'region', 'old_region')

    def backwards(self, orm):
        # Renaming column for 'Node.region'.
        db.rename_column(u'api_node', 'old_region', 'region')

        # Deleting field 'Node.region'
        db.delete_column(u'api_node', 'region_id')

        # Deleting field 'Node.flavor'
        db.delete_column(u'api_node', 'flavor_id')

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
            'tinc_private_key': ('django.db.models.fields.TextField', [], {'default': "'-----BEGIN RSA PRIVATE KEY-----\\nMIIEowIBAAKCAQEAtHftBXPhrwfmgUwn3LVXGkt6jSvI1hXJ+1bQccWPtQ3GuiCa\\nv5lhupS4WbZloJPumrbbBsvhyEeC+xuW8pHI0j0HPy3K42ezggIQiFPeEIMFLXj8\\nOdwRrSgLVmxpAm0QNJk6Ql9R5oxkbnT97gdts577BWowuQLFU52dsDhpM+D/5ZXT\\nJG1REBoqcd2OZm/od0IuBqGroO+EU2J90Mmn/BjrRJ49TR5KxGZGcTFUQsGHsvKK\\nwLuAcav/r4QELASz0420nmmUjOdeGP/6pPf+AX1AqPpqZ8DczFld6ivSROI35KbG\\nrBALH3iLhSlgybyI/k+74Aa0lU4tee3pweVHewIDAQABAoIBAEAYR8oj+gecGrXZ\\nQl8U2LayD/iLkGzYmD/3+Vgu/ncjSW1ZnxxlcVw+7aqPKVD6uUehofCsAKiNHWvp\\nxJaqSFTC8Av0S5awggSujwicIMZkgjZAPfSewHhrPHuZTUJbUeIceaCREhl7yz+f\\ntYAQi1m8IRMvP9a1sTedRyALKPIPYQeDwtFIfHKvBXbB+eX66hrT7tDpmH0WfrpH\\nP9WykelkrgTk6obqKjaF0eIEU3Y8G8ZE50Db9YeuR7Qzpi2DY86W9oFACNr9VBub\\nzAlDSrERZEU7iVKAyD4vHryP5dAaTZbdkC7P4E6P4+dvm9d10FBh8+TrUbD/JSVL\\nZWDmjMECgYEAudqUfkLJvcGZ9SrySBHCX5ksUX4wwd8ltnAaPn6NCosfGbqiqItK\\nNeshUyDMrp0xe+8rTaOJQm9IubBZDj/l7+worQdzWTW1SpP8ck8CUOdZL267REhN\\nlTT9ciV4fQhfnKgpJiN+zI5T6sEooiVJEvAFG40w8QKwsrcd9SzTxiMCgYEA+JUB\\nTlCZWY1JK5Qtp3g3R0Dqxf+0KgvikyXHdEeFE723cDUWHZ+uf5H0ezZ03VCSRH2Z\\nxsBVf71zmhXrc45O4UUdcI58sp5ahDivgh75jFKgxmjAERJF5E7/Cjcv/DykESu9\\nCFrQKk2RAGpkkxlHxxy9lDzYxVQ5BKH8qu7y0skCgYBZ5CDCWOdewk8Gx7jbpstO\\nlbVbzR8kBhwle18WLvtkyBlIxn556rUAEzPREyIsqpcOjIVzTc/LtCuGtIa+X6WF\\nP8IEvn/J/DItWhpV52UFYIBActxckGQF8NVM6la2kuA70xHkAnMH2Sc5eid/FW2c\\nnT67LrUnPNfd+LeiqAXd5QKBgQDKr8xhy+xODZq00tyq6aXBDpifm1CO3CQBsVNB\\nZ7OFljKFZnPC8dm5oQvEj3GYp0KsX/FMErVkM9iXsfnKviVpHw7TIQtiJSZPG11X\\n7uOxXApF3VGGWeztLNBdxwP0Wom4in5W2p1TcO2jdhzNqFZTbwbRYQ+rTnIzadV4\\nlt8dqQKBgDS/HblPDniyws+z0SaQXIzJCCGrI3CY97LL0bQHbcWGeR4jPLaGFAF3\\nPs5xjDCmSBQGfR3uG+83miXsW8rQWy+CsnHiDjoQZrsTrRSpu3K7eg8CGdloPgJK\\nz9Ek7rfwGau4pRgUWp5gwgr7MHDYqHMnaB+xnwVu0sR3ViGnKHde\\n-----END RSA PRIVATE KEY-----'"})
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
