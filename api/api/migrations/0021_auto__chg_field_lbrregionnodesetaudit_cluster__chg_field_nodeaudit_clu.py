# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):


        # Adding field 'ClusterAudit.ca_cert'
        db.add_column(u'api_cluster_audit', 'ca_cert',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

        # Adding field 'ClusterAudit.client_cert'
        db.add_column(u'api_cluster_audit', 'client_cert',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

        # Adding field 'ClusterAudit.server_cert'
        db.add_column(u'api_cluster_audit', 'server_cert',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

        # Adding field 'ClusterAudit.client_key'
        db.add_column(u'api_cluster_audit', 'client_key',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

        # Adding field 'ClusterAudit.server_key'
        db.add_column(u'api_cluster_audit', 'server_key',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

        # Adding field 'Cluster.ca_cert'
        db.add_column(u'api_cluster', 'ca_cert',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

        # Adding field 'Cluster.client_cert'
        db.add_column(u'api_cluster', 'client_cert',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

        # Adding field 'Cluster.server_cert'
        db.add_column(u'api_cluster', 'server_cert',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

        # Adding field 'Cluster.client_key'
        db.add_column(u'api_cluster', 'client_key',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

        # Adding field 'Cluster.server_key'
        db.add_column(u'api_cluster', 'server_key',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'ClusterAudit.ca_cert'
        db.delete_column(u'api_cluster_audit', 'ca_cert')

        # Deleting field 'ClusterAudit.client_cert'
        db.delete_column(u'api_cluster_audit', 'client_cert')

        # Deleting field 'ClusterAudit.server_cert'
        db.delete_column(u'api_cluster_audit', 'server_cert')

        # Deleting field 'ClusterAudit.client_key'
        db.delete_column(u'api_cluster_audit', 'client_key')

        # Deleting field 'ClusterAudit.server_key'
        db.delete_column(u'api_cluster_audit', 'server_key')

        # Deleting field 'Cluster.ca_cert'
        db.delete_column(u'api_cluster', 'ca_cert')

        # Deleting field 'Cluster.client_cert'
        db.delete_column(u'api_cluster', 'client_cert')

        # Deleting field 'Cluster.server_cert'
        db.delete_column(u'api_cluster', 'server_cert')

        # Deleting field 'Cluster.client_key'
        db.delete_column(u'api_cluster', 'client_key')

        # Deleting field 'Cluster.server_key'
        db.delete_column(u'api_cluster', 'server_key')


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
            'ca_cert': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'client_cert': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'client_key': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'dbname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'dbpassword': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'dbusername': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'iam_arn': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'iam_key': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'iam_secret': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'port': ('django.db.models.fields.PositiveIntegerField', [], {'default': '3306'}),
            'server_cert': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'server_key': ('django.db.models.fields.TextField', [], {'default': "''"}),
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
            'ca_cert': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'client_cert': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'client_key': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'dbname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'dbpassword': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'dbusername': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'iam_arn': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'iam_key': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'iam_secret': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'port': ('django.db.models.fields.PositiveIntegerField', [], {'default': '3306'}),
            'server_cert': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'server_key': ('django.db.models.fields.TextField', [], {'default': "''"}),
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
            'tinc_private_key': ('django.db.models.fields.TextField', [], {'default': "'-----BEGIN RSA PRIVATE KEY-----\\nMIIEowIBAAKCAQEAtf6wGtHlJnBQrBQvScXl55sbZXYtUILVJbR5wKQx35t+0Kf8\\n80Kouda6bVZyqBG0IWk3m9A4gENQgHQff7qj4uD5+JloPMsr4jy3078e5VGeXg/u\\nzFuNAphfi3LNCugzUR73bLwvYPv+Qba42aUpQYR8dh+rED91LCS6DmtcqPMTPaZy\\nXZI4uB4+mVxYWzmrqmENCDmZOarcVATPX9xFFUE+jAu2E+ywLvTRzb70TzBr+PLP\\nh6Wtc5jyWP9xrELoaQKA0ma0ztX5jqjIZsStjU1nPTGpPntn0rsrmOYuPXE61NZv\\nWgz3TkCPbc/KRfhCD0d+vi/NLuJyzLqyxNXJUQIDAQABAoIBAHdZWF+eOiolCaJv\\ncjts/kIOY7776uebhPA/FIESrGo5bMalA6r7ke6dNJCzWmmBgqFOgNs7h3IFsusq\\nO+XlncgRRZyT7dnAWzz4GI1SDo7QIY0J4c4+U5DaH/4xAOogMFcIebXjCycM2kZ5\\n72s7dnyyx3QnfGUhWFPkmecO3SslcK5QfdXnBtLxT4rnrnhT3irAMEnWZ/Z1l8gJ\\n4uXckMagH15AkxRn0/oqA0xnipWuYZ2I9FSD02yR6xWq2Hs4aHAtBl0OhyIKR9MH\\nuL50gm0aab8NTI1qXwoZoJ9BVt+hN/6Und138UbIEzFUo0suUKzw9jA5jY/5JRux\\n3y00GAECgYEAxMptruZTpBZu+LQ5WVWS+uxQJdepkpqAAx2O90Dbenb++e9Wso7d\\nuskkkRWE+nGpSM13W0dgcbmHHtAtZjjMKU5vp5iSfhRJ9N0nHQeYpjENmQnyxtS5\\niV8oGIQKLiIWIJaEF68Q6UQFIDMd+K8L2fdWWeehReI6YyoNNVhLxpECgYEA7MCg\\nOkjQZ3gkmht3BdYXlm9IY1LhST8URZOD635GbnanioQMIEizjyjm6igiA1EpjW9Y\\n/YpbXj+hiSbV/LC6PHAQpbmmohwYPGo4reuMVCqOCJbeUcWyZy/YP9uClIOeV5XF\\nmUjbllhTgs5VlYBHb2yrfkxXw/CWitv5RpTqtsECgYBeMvP787733dEy9bo5/A+G\\nU1YuNySxy4kZdK25x28IGSwGYb3jbSXQQnZhiKaF56B7+/Z1WB5fccqvQkFpHCkG\\nYMhrtknxVi7sqmwNplQ4wWRb7HotGSjTDBy6V4I0ARcMdGA4ohF7R5cYib+ACfKn\\nXJEWKh11wUvnqfp2nZRwMQKBgQC/tySIzhnlD8cj/AWf9kRXj3ng5GaGd8wko1X6\\nRuEl5nO5mUBwjC7LSOXky+bvJLQvUfGQLo/afFCEzawO2dWVx3HTocisEXAWzDVl\\nsQ6LwYIOto0FTsAvCvFklI7jUMnSRvgiLnuS/adyjz+CtsQiGK+usIeJpbNicssj\\nOsfugQKBgEn6mzJxjxWva+SHlk8CFjb4JhlLvkK6SlTGflOXiUr7EYfoee+qXeK6\\njIfyhT3F2zdN9NGz7IJhulQIbALuYKWTtSDkfhV7AL1L61zPnHlMzyBwSuU72+U8\\nsLw29iosfjOM2MxlCMnwkvLwiB+OfUrmOJ3ZRoVMKoyVC9TUsyYz\\n-----END RSA PRIVATE KEY-----'"})
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
            'tinc_private_key': ('django.db.models.fields.TextField', [], {'default': "'-----BEGIN RSA PRIVATE KEY-----\\nMIIEowIBAAKCAQEA3vU77V5Dxy6jpAiWVb4W5Wl7TKewYgl3p/nndj2GVQiPnypl\\nLUY2tg0QwwIWIsQMqzJwxjuvt1HQfBE+2sQjN43yItKAHKXX2Oo2GvZjGTIkJSZG\\np2IDCCkuNtLo4nQEtQ7j02/8ZR3yZg8HlQHHnoDNvuTswBQ/eg8YFXwbeE9HpxZu\\npBq9K/zSkHpKWYYivc7vcYbwptD7OKZJ8myq/mU22o+IJ6Iy9hqYBbbn6ui2c7eQ\\n79Ll3Z1atw9xAe1s2Hh+CaCM09CPzr//v0Vv/DI80rHavRF6/ZHxHA3SVX5hjm81\\nfBpvT49Oj+RhUS3adEtf2WAeq2RwZFsunGpzUQIDAQABAoIBAQCndfp05wBxco5m\\nfiysagI4fWmmwayxdfrxp7o6DSwAYlW9btJflwUw589XKRIHOslpLJGX0uy//Ctj\\nhHB5UChDadIcZY7j9YyR2BibV8RHAGo1nPIkdnFgh822T+Orcwi2FWD5RnuEV2Hh\\nVhiTyqpsWsIuRzOrcYnb28pzGKxpR3tp+4LmYURcJfr3NQFEvcyWq6s3GrpwBFCH\\nO2pGwbRWzagGGrl1y4lEWRjfrOPYlp4a/6qa6QJirjFEn69PylXMyCdmGgXpfE+n\\nhDprJxXpOrf+ucxcPWSpcWvZYnX641CiViu85d/HUzi1ypbOJ12Ilf7OMPnyAv7B\\nwFHZAGABAoGBAOMpk7ZNd2HvckoPRobZHitnM8Pfv5fE7+tLDaywJ+YkyRvd7e75\\nlfzCMBMqwjXTbBPgI7KxdpBE5NGln9wsEZnkRxhBTbL26XW5YbChUXWR9/9Ik8nU\\n3tprV5PGWVRVFtATpocraxarHJxDx5lZnkEB0lWsvw+9l/xIYd76QubBAoGBAPtD\\nBMEQ1/kvbFUC7dJt0C5793vFVsEMfWnnIHL55USJDPzi55TZpTNqcuq+YmRCs8+g\\nh1DP9j98F9VmY8lYM2qnJlmvL7cFSlNaycQ9hiIwOdFmE9tJlm9GRBKjTvpAA1Jg\\nPuSNllvHAbycOlbBBn1HxFlpVUCB46phSzbJtcCRAoGAOcxjZBgzzvxgxQ078aWe\\nsoZwul7c3d3i+ahAE3dCv6EOdoOyPYLNseEq4EWZ4p4nuqrmClpzA2Q0IE+W7Cte\\nUxytJjO/dFC0uBpyC8IP+u0n/5FU4R7DkSmMv/HQ2s9HnavSTEQ03DCvd+cbCx6t\\nUHcJMHlip7uixzMXi+d7TEECgYBs4uk/hb4ipdOLr75CkAZE7sIcaDOla3U6HMhq\\nKzOZFM+FFAwJ7Jv0ATCV3DWlf2aPFuEtO0Ja1rs5ZqrdyZRWpuMuwIWsCeXg45pG\\nqebkEAQuY889G9HOnSPI8+648l6+Jyl6QIWldkOhag66I+JdDmnf2Y7xapiv8IP4\\n1UcnkQKBgCUXRz0+qpd1/1gZcLaLHqiTMgLBvorQSO9N/aobYF/ddloblwFSGVaI\\nZJHgnE9cW4kKuHunMg3YkliKlKAS3kgs3dXveZXKhvvDvUpG6zzrB5Zw2+SGs2yo\\noHLPAaTNkbo6ULj3kyyuzjZntlct8gyWD+SIGexVOKh24hUO+RRf\\n-----END RSA PRIVATE KEY-----'"})
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
