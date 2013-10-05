# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding field 'ClusterAudit.ca_cert'
        db.add_column(u'api_cluster_audit', 'ca_cert',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'ClusterAudit.client_cert'
        db.add_column(u'api_cluster_audit', 'client_cert',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'ClusterAudit.server_cert'
        db.add_column(u'api_cluster_audit', 'server_cert',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'ClusterAudit.client_key'
        db.add_column(u'api_cluster_audit', 'client_key',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'ClusterAudit.server_key'
        db.add_column(u'api_cluster_audit', 'server_key',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'Cluster.ca_cert'
        db.add_column(u'api_cluster', 'ca_cert',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'Cluster.client_cert'
        db.add_column(u'api_cluster', 'client_cert',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'Cluster.server_cert'
        db.add_column(u'api_cluster', 'server_cert',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'Cluster.client_key'
        db.add_column(u'api_cluster', 'client_key',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'Cluster.server_key'
        db.add_column(u'api_cluster', 'server_key',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
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
            'tinc_private_key': ('django.db.models.fields.TextField', [], {'default': "'-----BEGIN RSA PRIVATE KEY-----\\nMIIEowIBAAKCAQEAhiycNqK2RfiD29ZcNzVr6fDqgDcuO/wrAzlvUw6smFOrm8hV\\nB9p+hRKDs0z6JF+wSSOuHIPyVJB6dBzstJ5QXRgDlUQEQSniqIY6rfQ0OdSlHpZF\\nvQAhxZ6JXuFhIdk7PAUaG3t7moy2nQ5At9D38hURXi169nQl5Lkrn9H5eVILw7+3\\n/qNCw+lwMh8lfF3ZcTPD7P59Nou5/G6Zc+MMh5vOohrMzrEqQMqDYehE1z8O8i00\\nVOWki3C+zW9H0WQ9+pE3chBdmlmqcVd0DthJcNcK0IzMshDweDXF4+trjiioOH3V\\npTxYoW3ywRj84YaC8lVM9rvIL4THXRarKLIgoQIDAQABAoIBAHmq0iyo92gTpl4e\\nz5gwlR6aG8sQPpieXdKarlw+njuzA5ZL3u80Li41T7+zOdDqBE0OUcAB1ijgqmnI\\nIMzYEj+YmwcrmkAM3z+6GFPNcd5O+Tv3QF3WVMmCrUagURgEiDYw2i+5lafbmWxp\\nlD4a+/tFJ26jBzGcuQ/i6bAPE43yjB6fOlk+rb8nhFjWHfSGxvniQkSicVe8a3Y2\\nC9WAITEXlV2s3Sjk1uEqB3/3Z4hC3yzztZlRoDCkyvz+WFXU9ZiMFTB1DDjdHQdU\\nE36oBjezynosqDFfTSioOqldCWilBjlTSprOljUHg2PfaK3GiWMbsb0kJtWlV+Ps\\nCbazApECgYEAt9KiCDI9DThv0sQfohmzgqyb3HNf9RL716TWzv42dn7WWSu0eSD6\\noTUaIxPjI318ZIqBMP5lF0sSES2pLKAs0PpNjkuAbeE1A+bCgKwGkzAmFtVcvCWr\\nDK0GoLtrtOhoFG+D1A87p/qEoU8LPxlSs5/kaYiK5ayTw8iW7sNDZ8cCgYEAuttx\\nN9WqQirN14fnHpKzu2Bj4iNkgbg5FAHy3WGVQtIg8cumFhrYXFKf88aW8MuYR6wn\\nB+q52vhtK8gFArk7X8dGPOdQqVgGG/N2Nz80dWnzXnFTp090UYU84ZJVJCAmfGR/\\nGSYZkTChf3ACJH2UHf3MRxLFz9e3hmRSU0r/RFcCgYABYf9ACoi1CcClmD4YrRLR\\nn9TIUsHdCRiF5cKL6hOkzo10PETuSFY6UjjxHJwvzyjZZMVWBgPiqfjn0i0cndPY\\nepmMwXqk2PXaIqlB6IlgIBOZRl+dNrdTsBWFrgNAaCMoTDJ0rOyo9dR7limifuFF\\nYqWIObO5yJOP/HlOMH/YTwKBgQCf+2gpJN+7/Qf2I96Gt5X4tONv51uTENaVwcFd\\nN8JizqP0Qac2v89E5F0ci4gKLFZ57vQP/DEaQJ6/4GYh2dPzAhup42aVRs8cOUua\\nq5vPd2IuFxtHYWi2rzvb6bzJzFkHIcgMESnMvHVZNd4vvfEF6JlwtKr2c7wm7Vfr\\nBogdywKBgGhDo3EFyxrD4tU9Z+1K5mkUI+YE845MD6lHYE0O0l9f8r4UE5LKu159\\n0FpswhBmpHOvmoCyry3XV3JM4PevZ6aHwyaUoRUkLuxwbNa6aT0a9ajb/LmWvpoD\\nwvLQza3NsfNHxsPTtCI7quOfA77UvSBo8cY/5TdYsYvzQF6uuIHV\\n-----END RSA PRIVATE KEY-----'"})
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
            'tinc_private_key': ('django.db.models.fields.TextField', [], {'default': "'-----BEGIN RSA PRIVATE KEY-----\\nMIIEpAIBAAKCAQEAppHKWc0B2pi6MkNuH13Bp7lx0XZPAy5CDgwC2QLpNWbI2B/t\\nQWNZ4jy2aq++n2ycGFwGdhnK5/lHS+ALYLNdhW534HCn4VBWUSCfFR0eQS3bj2y6\\nVNkNlhaKi3dyKPTAdyPX4UTTI6hoLQgVQ+Nz6faHyIcA2E/zKph0uT2zWmB7WsJ7\\nqSBPYpo96K5pmbfz76OlAqtvkGQbagJVFVUszYSCcp62JPqn/S43kqLJ1zH/0eP5\\nIS6U1pbdLfWu3BvTcPuYznpBggooRTydQsizp5CUYPVprOr8mxLlbs2DEEloyiTC\\nO7uwjpHmmigcoT3zIAoa9FKOG/oyWWqBsPFYjQIDAQABAoIBAGZleV97B4i6GryL\\nd0cQ+9t/xNhfQnNSHIlGGPoPMA4EAbPa7J8l1Duf1wP+xdB7k/nlmJNBh9rTA2FB\\neb0YhoVgQ5FVr95y5J060JDKNa8b4b1puaIvTIrXkJPr+eHzk92pyyxQgvuIq4ID\\nVg9F5BwP0akUVRClFXc6AYdexsLnTwfzLkVuUSakaXPE1ADjbUkhTQi6WmHAU/cz\\nPH+Jp5PplTJU/i+TX2cpxp84U1LPATwGf7U9MpDWlaA9LA1EPo9nRFxbNFBwVQUR\\noI4q4IKARARyGozm6IsqBnY1s1SEDTjSW+EvUI2BMv/KwK4aZoO666IjyD3NqHc4\\n2L6/yAECgYEAzNTkW96gYbhIKrf1Pe40ec/i/lXRzlLUhaRySInYf06h5yFSmRAE\\nTYiALzjRpqSg/JYKRGRKyd+AywvebV/7xu6FsNoh+lHFY1nPGekjTULdDNR6wzCM\\n71TP1k79OQ9tjvUHsJWj61GOqF6sjZS1loBZV3/FxS7j6hNqrkgG3H0CgYEA0C4D\\nMYc3mcH5UXX4W9MD5TPKRTaqO5jkcQWRWOFBdjQm3qXSAc5LDJzhy7MWj4E+IKW9\\nRB3mlwZ7SoP6te4X1xxZUD4ol26pyuI8RSFz5WSyRJ8LoqD1ZqCg42fRptzsT2Fr\\nBLbmCzTENKtU7ATWT9NUJeN5MtqlzDUdNUSQ+VECgYEAp1uO1c1Zh15VgKnbc+Vr\\n9Nc5ZYtjKEwfHq6VPdV7EdGCkWF1pmAi0+KisXKgQaMjch15eBXl0XmPNteUvhL9\\nmbWLgEtKFce4GovnngkR8e+ewvvc7hx+GpJWWokhdvy3DGYCCXLKgtuZTtJD9E47\\n7CMkXEymn4zHZZrFwG5TRNUCgYBfnDJFRffIOykZO5gD/Cb21lFYdmG6m16Xddoq\\nOtIIyqzrZrbLs4YOVeLx3d9HqzDwZ45EQYNM62Imd/TmJ2J1ngR68QFNgzqh/kN1\\n8IY83YFuOKlsWIY8Sxt5NY45F4/EaVZwRNvkW6idE+8dsp8G7GTiPdXFAFxTLDWs\\n6D+48QKBgQCt8fhx3mLzC3wR/qpUkJdIuVxSxpon6tA0F3lwJnjhQwrF9khcNwuN\\nvHFwkbFdnE4g5grg0f/ELrXeG1RrqWPrLz8knTSv7w9y8yUaTCPLMYBexp8roeCB\\nqB8ljgKwy+w1Vsg1KUdS0TEj/8RYobhPUO1jYDtLaiiXPrC0BhE+7w==\\n-----END RSA PRIVATE KEY-----'"})
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
