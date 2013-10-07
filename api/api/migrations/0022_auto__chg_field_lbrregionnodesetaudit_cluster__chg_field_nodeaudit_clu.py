# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Changing field 'LBRRegionNodeSetAudit.cluster'
        db.alter_column(u'api_lbrregionnodeset_audit', 'cluster_id', self.gf('django.db.models.fields.related.ForeignKey')(on_delete=models.DO_NOTHING, to=orm['api.Cluster']))

        # Changing field 'NodeAudit.cluster'
        db.alter_column(u'api_node_audit', 'cluster_id', self.gf('django.db.models.fields.related.ForeignKey')(on_delete=models.DO_NOTHING, to=orm['api.Cluster']))

        # Changing field 'NodeAudit.region'
        db.alter_column(u'api_node_audit', 'region_id', self.gf('django.db.models.fields.related.ForeignKey')(on_delete=models.DO_NOTHING, to=orm['api.Region']))

        # Changing field 'NodeAudit.lbr_region'
        db.alter_column(u'api_node_audit', 'lbr_region_id', self.gf('django.db.models.fields.related.ForeignKey')(on_delete=models.DO_NOTHING, to=orm['api.LBRRegionNodeSet']))

        # Changing field 'NodeAudit.flavor'
        db.alter_column(u'api_node_audit', 'flavor_id', self.gf('django.db.models.fields.related.ForeignKey')(on_delete=models.DO_NOTHING, to=orm['api.Flavor']))

        # Changing field 'ClusterAudit.user'
        db.alter_column(u'api_cluster_audit', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(on_delete=models.DO_NOTHING, to=orm['api.User']))

    def backwards(self, orm):

        # Changing field 'LBRRegionNodeSetAudit.cluster'
        db.alter_column(u'api_lbrregionnodeset_audit', 'cluster_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['api.Cluster']))

        # Changing field 'NodeAudit.cluster'
        db.alter_column(u'api_node_audit', 'cluster_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['api.Cluster']))

        # Changing field 'NodeAudit.region'
        db.alter_column(u'api_node_audit', 'region_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['api.Region']))

        # Changing field 'NodeAudit.lbr_region'
        db.alter_column(u'api_node_audit', 'lbr_region_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['api.LBRRegionNodeSet']))

        # Changing field 'NodeAudit.flavor'
        db.alter_column(u'api_node_audit', 'flavor_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['api.Flavor']))

        # Changing field 'ClusterAudit.user'
        db.alter_column(u'api_cluster_audit', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['api.User']))

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
            'ca_cert': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'client_cert': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'client_key': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'dbname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'dbpassword': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'dbusername': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'iam_arn': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'iam_key': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'iam_secret': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'port': ('django.db.models.fields.PositiveIntegerField', [], {'default': '3306'}),
            'server_cert': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'server_key': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'clusters'", 'to': u"orm['api.User']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        u'api.clusteraudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'ClusterAudit', 'db_table': "u'api_cluster_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'backup_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '24'}),
            'backup_schedule': ('django.db.models.fields.CharField', [], {'default': "'3 */2 * * *'", 'max_length': '255'}),
            'ca_cert': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'client_cert': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'client_key': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'dbname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'dbpassword': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'dbusername': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'iam_arn': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'iam_key': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'iam_secret': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'port': ('django.db.models.fields.PositiveIntegerField', [], {'default': '3306'}),
            'server_cert': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'server_key': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_clusters'", 'on_delete': 'models.DO_NOTHING', 'to': u"orm['api.User']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'})
        },
        u'api.flavor': {
            'Meta': {'object_name': 'Flavor'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'cpus': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'free_allowed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
        u'api.lbrregionnodesetaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'LBRRegionNodeSetAudit', 'db_table': "u'api_lbrregionnodeset_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'cluster': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_lbr_regions'", 'on_delete': 'models.DO_NOTHING', 'to': u"orm['api.Cluster']"}),
            u'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
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
            'tinc_private_key': ('django.db.models.fields.TextField', [], {'default': "'-----BEGIN RSA PRIVATE KEY-----\\nMIIEpAIBAAKCAQEAmjVmzhStov47gcOQ4iAQm0SaY6tFd/ZOdhSpocD8Xyov/zgg\\nlqQR/fQYSRIIArMd4YKx8cYOJ3IL/iWP8KOQWgSWdo4eYQTm6j5kANCWH74G4Av6\\nBNzP09iuMRTd8gl2G4IrHjUK63cF6XzcM560Axwbz4RqgUXJqG/32j6qW7roe1h3\\nDmpgOL+i736QtovZ5505zdPVmBSICE7P81jZiDQAn0im+10hkbItMoXVU6wy4MjE\\nmgR0EPFmGNSuRTKZ5owZRNC3SSof2i3x6S1moBl628dSXWR8K6nsEXyp3xhbLaQL\\nqYm5hwb0km6LXRBWN+xMjhHiyKaRI/9TuMyycQIDAQABAoIBAEpLxj8tuUaZRGRN\\nq8U2e6nDELtKbkrQ0ZaUd/Hlv/G9qqhFC3Zoj/6Rlw3FcTSTxaa7yC3bJUCd8uc8\\ng7AFreug4Dk4WayWpwZejuHRnTKn5DoXqxqipELF147wJcqSAmRYf5urJJqzmpaW\\nwKTiJoqFBWUiwAmObQ0I/RoaLQvKLvb6aVV70Nko4lP8AMWJLPr58lUiYvZy8bs9\\nCP1xOWMfEfPqa1v6lSHSntvg5LJeKwt6qfuzsjZz3JuhiZ3O+mjgePaoa5EQsjsO\\n6Myyfy3AuSDXXbpuS+NG0sEtuzf54UrNVY+efVF+DS4z+VjBFH6JDqvEaUxWRcNO\\nlyFzNRECgYEAxK98mnej+5d3UMFmFfYY2evgM+Jw7N/OVCnyNY2OEulXB4dvjLX9\\ncFvgR7wqP4nYVdj3zNKpUeouIVgQeLVZskZhbOYlPzRMjRLDHS+uQRQf2gyFh58R\\n3dNHWdyiPhco4CYxtYql0Xeof4BHbSXE3AYZ8Bw1wXFRGNfUM5Q7bjUCgYEAyLad\\nGPvid6BifRhXDGbgQT2nhvPaYg+Jtrux948hpJb+uYVdE8Pxebv0k1HC/nCxXrc6\\nce8mrWp0A/f4b9hfr2JD+HeppJzxVFHEABiEKpRiMaHsRpDKMCIGgANHZrdQXXy+\\nU6XwgZ6g8WRa9lH/gZ/Wpf2vLDD2tN+YfIu16s0CgYEAkTEmX3TwRZqjhqat8IpS\\nABTi1gpT6FiynGi2lxffCFDeYP12uD3kUBxSrUHXQj5Ex+K50qa0PXcNBKpYxnLB\\nOxw/cT9XwZee5wkxpYr8LKhpdvKFY/9mFgWQh2KbFhDMqOMpEOW/0KhvZ2fP0l/u\\nOan7XcfFWv6GqjsxN742PP0CgYAkHgA8665/2kN+wS+A0s5NzxtjRGQquyML19CZ\\nfI8QP/+MQLxT/zFnt3O2QsM05/By28PPlro+AGbqA+gXsDbfp24Vuuqy7W7bvm7n\\nmYHG67aTudB7jjhj2uuSg4SIrjnu6LCS+sxBdtr9NRLNOkog+DM24WRxLkpml8mn\\nt7g/jQKBgQCtpEIQDo1c2riLnCbdMJehlblb0zOfZDzXENkulC4F+j8XdsLfmGLD\\nEBGr7T+9BiSPsTJI/9/9loU93AdTygGqhvuxMoJafRkM1LZrlIaKgcXQhbjXETJX\\nSzk3z1zhoZj/CQRdX9b03S8ctsTMMmTcG0wmKCSwibp0DfV4PoGMGQ==\\n-----END RSA PRIVATE KEY-----'"})
        },
        u'api.nodeaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'NodeAudit', 'db_table': "u'api_node_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'cluster': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_nodes'", 'on_delete': 'models.DO_NOTHING', 'to': u"orm['api.Cluster']"}),
            'flavor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_nodes'", 'on_delete': 'models.DO_NOTHING', 'to': u"orm['api.Flavor']"}),
            'health_check': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'instance_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'iops': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'default': "''", 'max_length': '15', 'blank': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'lbr_region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_nodes'", 'on_delete': 'models.DO_NOTHING', 'to': u"orm['api.LBRRegionNodeSet']"}),
            'nid': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_nodes'", 'on_delete': 'models.DO_NOTHING', 'to': u"orm['api.Region']"}),
            'security_group': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'storage': ('django.db.models.fields.IntegerField', [], {}),
            'tinc_private_key': ('django.db.models.fields.TextField', [], {'default': "'-----BEGIN RSA PRIVATE KEY-----\\nMIIEowIBAAKCAQEAlCttWbDdvJwHzWvmW6ev6/1spTtyN26KihD9AKgzVvLkhesc\\nvnTMXUoIavukeEN/IH79wCY1o83SnU5QH6LHCCrox84nVA/0mdosFRyNvOjehlgM\\n5M7Ev+SgYyFMES9nJ5/LFDR0IU8L6vogRVix/pjTiub5rNDWzrEwF1Uknz9v7t14\\nLXuGUQOa1E+LT9OOKUTA8s5t/THO98yClWnLtNFq/NZj9YxGZEOdzAj5p93s25Nj\\nPFabMKwWBVGvBeAGmQXyItCnw5s/TgnaVYKs4oXnefpEPS3qpkuQPy94KbLQji+y\\n/+T87QdIZ9gzsGCSW5AE9IthkrPpoQ1WdHgt3QIDAQABAoIBAGF+GZt0ZtIdkHy3\\nzIDuWzDaNUybStHyaDHkb7So9+70Ly12wBkJXRbdCaDrJxMCxnkpVenCunSnjzd2\\nOf426uMS6Mvfd702Kmm5Rlw1x4VPbGvVL9a1vnvNAUN4u0ZrfGJ0H/mRcgAgtOTN\\n48H9VFEDWd4BkLMHTu/9YnlXypsE8F8x+5Bu2XgrtYuzgmJQE8BXwM2FMhXTZiWY\\nIQ8MRZAMLKLudq7e6zEPowYNuXy+jNtJHTL5yg8lRVISD6ILPB8AaYfj5ev5Mz76\\nO9Vsq1gRk7Tztuklkhv9QUt2D+JMIr9V1G9kbgXjbohBpLIa8bK83eokuY5DlTQx\\nXI1yj/kCgYEAwLWpquwoqWYJl75bLO0a7wdGkEtTUj/g4oO6Zl4RHilieoluZgHg\\n3UaYJMDuzzs8XsuyX12RnnMM9tGwV34JoPJTsS4B7FIoFd8Xq+0YDaHiXRiKu5fN\\nlpxv40AQY4jN/CUUuT6NfQ71IQe8sRyvqZjb1j3li9fl1N936BEXPvsCgYEAxNUA\\nZdYa/OL3jlPL2Dr6gZDYS6uWzJkU9rS+L5kpm8rNe3HhQZYG/SoAUaA57fNtpbPl\\nklNMya4VWnQL6A06jyWbUsCmza5pm8Wo5P9SsV3jnz0keL4X9wmi49vZhNQ1yZje\\nQciCFKBDBZLypf8WS+Fzyi0jsYvBmvwsz6xSTwcCgYBTXwR9VtgsmWFzDb6iTB4H\\n5Uzo5j2w6sPfG4BMA0xCkULyonxpk0x2TrFJzVJDw2vV0yhjS7bRJxMnwQYahAOk\\nZtJAaBga5lxDQhYaomNymmO1RQXYLM+b5igd17x/Y1NCT8SMc/yAazUvygofUbrJ\\nk8EgCf1CJ/BdzSQx+RrmewKBgQCisVTE1/YytP/eOtExB37r/WdrFIdu0dGMIdVZ\\nzoWf6j9yG60O4w0f0Mm2rnNzhVRKNKo7CnNb+HJZ87WrttOCYplCC09UjydnxDdY\\nINqfFHYCty0gSC/S17o2ERB4RFe5LIv5X9x1ZApB3zaFkpVBXzawFCN+q3/5tRrt\\nBQh7nQKBgEC8BODV1f0jWbNiuVxAyBadUG5pkuxFajNhwAU4HnaQbKn7m6uTMfu/\\nsNn/7tzNSqdNa5T0MJe7wdq9cuBqrxSmjQL8DZtkYKsXmfmrGZ4rUXAhNvKN/43r\\n9Lgh6WvDaBYCkoJFk0Qcezv89rOWnWZY/v5HZQ21P4rqPOmQV8YX\\n-----END RSA PRIVATE KEY-----'"})
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
