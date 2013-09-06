# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'LBRRegionNodeSetAudit'
        db.create_table(u'api_lbrregionnodeset_audit', (
            ('cluster', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_lbr_regions', to=orm['api.Cluster'])),
            ('lbr_region', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('launched', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('_audit_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            (u'id', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
        ))
        db.send_create_signal(u'api', ['LBRRegionNodeSetAudit'])

        # Adding model 'NodeAudit'
        db.create_table(u'api_node_audit', (
            ('label', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('cluster', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_nodes', to=orm['api.Cluster'])),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_nodes', to=orm['api.Region'])),
            ('flavor', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_nodes', to=orm['api.Flavor'])),
            ('lbr_region', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_nodes', to=orm['api.LBRRegionNodeSet'])),
            ('instance_id', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True)),
            ('security_group', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True)),
            ('health_check', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True)),
            ('nid', self.gf('django.db.models.fields.IntegerField')(default=None, null=True, blank=True)),
            ('storage', self.gf('django.db.models.fields.IntegerField')()),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(default='', max_length=15, blank=True)),
            ('iops', self.gf('django.db.models.fields.IntegerField')(default=None, null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('tinc_private_key', self.gf('django.db.models.fields.TextField')(default='-----BEGIN RSA PRIVATE KEY-----\nMIIEpAIBAAKCAQEAwDEkX/+vcI1Svrn3y8xulRjkcCeSdFuUm580Qdg0Zzh7BUIR\n4H5CmCKQnHX4+hOLwLSrRIDsihKAj+ETF6Zl0HNbYltOYAyBBb6A+tWmlrR+vAKT\n4HFvJXfSUYi8aXO9vDn8SnPTiLm3scAJVJEvZ/hNWZBuaeNkjyjX+nl2pBAzKZ6f\njpV/YYI5ojpxEWgA0IpX/G+yljsqNppZfDl9WQxyyEZU+A+ePZFKg5/DMB36p/Gy\n6PIVpW4gV/L+OXRUSV3gYUFx/uxYdjL34hoo0BqjUT/Jyh+iH9jpjedPGhgs/qGe\nLOnURmDI/3V0yBvjeLLjMfHWfa2XS5t0CYfhEwIDAQABAoIBAQCK1vVgJGWo+W79\nOXs5TsXUD9d27h9uz3nbsncd2gKBTtwQQFqJwqx5Gv89CDyE6/nZjKrtIfW/CP62\n8fHI8/w5ShyKQUutN1s9uxGSIyXlWR700yfgzBFvD9Bv9kemJma6w2juoB4Ad6ms\nTv5uiTOl+EpomV4qQIs0oFzmJTj/6zIUrgv+pgQBeh6Behr9W5JUBuMns2kp528G\nwVhqQ021AiZMFU11Uo+w2Pct9qfVTfBYMUvynNW3jG8yjfWheB2lSYh37fYVkFia\n5BLFhnh0sQ7RXoL7RUjsZvfRLDBPXeV5z8GKippDwj9Gsw2o9WNztWIHHi4SIyPO\nItj+G2UBAoGBAMl/YzEJ/J4qb7Ciy3/K1bGKHKwxIop3ufRnAHp3+kDyZI4QyjA2\niaFO7vGlrZHgU6ypsRFC/1yMmy9+miMvEXeuCEy9SM/qWbAOdL1WvUmPEqy2bvfm\n6TcllyI1BoklBjNu22MwZrxNsv1pFNzXVLuEsSjPCXAy3wNp911oe2xrAoGBAPQt\nY6hqMvMrfUuulMTaTgzrc1efOrlkwJPzKDGpsC6vwyvXmyawOFs3QrQwqrMFRN3s\nE0ZaX1d7yU0UignvZ8xE8+mhFNkV1foaEebrFfCrewKeB/5NwVbllI0qI0u8EOkU\n+vGQu/63uXVej+Tf5BJcjnVHezBOAGDqsGvtrYf5AoGAfIqTCY1tqWj7TcbhVuRM\nvoZqAHgCLGmh8xDy979OW3Q2eKSiA7jByoUaJRvNMzvfG/pqagvqAA8cH/f1V0fR\nWRKlKKFZ7sCfnLTirOB+8IdQ+JVt8yWzAhXm2wrBNmU+9u1PBni1FzBDMGQRtAoX\n4is6wMluwP2AYADQFtjsaG8CgYEAgXEGYaNauxoU4+f6qZhow+SVUp/wi5Njm4rN\nhfZElZtLRZSYhRvp5EEZNViPRTPH3DVnymXiIQhYIGqA+t9VES6EdxeTa7lto5Xq\nY5XAHcNqBGsuJZumoKA37dWmvGFIPaeHmEN3xYIz6IpmkZg22Z0DUBzCq0rOXJJN\nUAnBclECgYBTyDfLe6Pa2/oeyS11wBGNPN2h8+tvWBqQIScb1X22AXNwl8Wwc55L\n54OtEp/kvxd64abDtqf7M8VodEp5aVNd4ukTV0zIAWb+2JxoNC94ldliarD9OpcR\n9Flh45goi9pYFtBbDE/RuSgm3MtoBLjBgy3mBqBw+lf+CSi5nO29Jg==\n-----END RSA PRIVATE KEY-----')),
            ('_audit_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            (u'id', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
        ))
        db.send_create_signal(u'api', ['NodeAudit'])

        # Adding model 'ClusterAudit'
        db.create_table(u'api_cluster_audit', (
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_clusters', to=orm['api.User'])),
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('label', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('port', self.gf('django.db.models.fields.PositiveIntegerField')(default=3306)),
            ('dbname', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('dbusername', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('dbpassword', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('backup_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=24)),
            ('backup_schedule', self.gf('django.db.models.fields.CharField')(default='3 */2 * * *', max_length=255)),
            ('iam_arn', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('iam_key', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('iam_secret', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('_audit_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'api', ['ClusterAudit'])


    def backwards(self, orm):
        # Deleting model 'LBRRegionNodeSetAudit'
        db.delete_table(u'api_lbrregionnodeset_audit')

        # Deleting model 'NodeAudit'
        db.delete_table(u'api_node_audit')

        # Deleting model 'ClusterAudit'
        db.delete_table(u'api_cluster_audit')


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
            'dbname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'dbpassword': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'dbusername': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'iam_arn': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'iam_key': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'iam_secret': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'port': ('django.db.models.fields.PositiveIntegerField', [], {'default': '3306'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_clusters'", 'to': u"orm['api.User']"}),
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
            'cluster': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_lbr_regions'", 'to': u"orm['api.Cluster']"}),
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
            'tinc_private_key': ('django.db.models.fields.TextField', [], {'default': "'-----BEGIN RSA PRIVATE KEY-----\\nMIIEowIBAAKCAQEAwRfXZNv/5LEx9Hn44t6dAYY8cSYn7qZCcGWIgFi4GuldO9mS\\n1/lbTz75m2ol1Y99STdNFACIlmNghETMzLDbHu6Y0uKa152ZWf1OcKSk2Ze7cziy\\n4OzBNh9jqtHjPeg5unseu34ZUrH0SywpEd56n/Okpwhv8DpWGeDgwtvhkgTyirB1\\nvREmUm37B7KLqw+XPSKWKT9icRdSKR1wJiEHwqOkEgdLBEEQ3vd9qms43EhwCItR\\nsXgZ/mq+AIophz1aBBnh4rniNyl8QnjtzrWxAZ+L41oOIsAMdPvfHSHISpO16hdP\\na05WJEEnbj1oD0rsl/PLPtoTVaASoQRmBBGPlwIDAQABAoIBAD3LEG5BjWG1ZyQy\\nyHhp/1rWh486Q7s2z7pCc+2G9tv95I1bsoeVUChLIfwfex4d/l0o6mzFQvDFusR5\\ndATpcCY0+wk55Y2s7L+Etc6MkgjkauOTuIMMoURdxTqMUqmkIJ1R+2LLFvWE54YL\\nCtWiGiIICaA+rfv130oG0kbpsQVWKxzwg6CBqv87JUMJjrRQhTs9kDGgM3m5/crp\\ns4aguIJPPXtaGZ1IH/y9ISYltDUbFs8/AzvTXTWY5lfx1Y5BlH6SUynl3bPNP7TV\\nJJL3UMp2LAXCtzkPbBqXlpMo0rAKZG7gO/HeMGKx8cMpUDlx5DjbAAkDVi/54GM/\\n2SbATnECgYEAy1BsBeEbWWGV7bAZOHJWCRmM97H23pOsSQNyV5slIVgo71uFLkgJ\\nLjkj8wK6/fNygA3RspfPwxZg6SduucrYbaTP/qxnbzBkSbk8z9KGL7pSPwYyPhq5\\nxv7WjnNPadjiH4ve2Ky2sQT2/gI2bvphfyi6fqGHTD1Lw10gIqrrOH8CgYEA8yFf\\nDTutZkzjkZgDWd0BQoMyqIWCxh7yhJO80FoCg55rbSQTcHcDM0JLuZWZxDTzIrdi\\nxMt7Yjv0WWvSuvxgl9rXeFtOcDkb8MGLMikbCchoNX1p3EPA7ROSjur8Usn0ni09\\nw3WDLBM2uVf4uUIx/0oBJvh2WBN7kotIXGmS3OkCgYALGMuckonEmh/txjPKMeti\\nOcPI7Sy1P0gjAA4om+4t4LrzPYKKYSInJLVCmT6Nh9ETDi4I2mJbmogVkbJob5ra\\neSllFBHdLr36jCK2kR4D0t6UVAk//INxSg153u9RrqXA5Qh3uQ2LoeK9QG+qJP5X\\nS2jKapSQ47OT6SxM2BlYjwKBgDHM9BtRzgLWXQbFjGorysZE+WtrbY4HaMWfPV2w\\nEjPDj12bth+jQRSOz9QDwKtf7S1/QsvsoilM/pASdee3KlHwkZIlobt69y4pdsmf\\ngdpPIolSVwy3FB17lNmRaH3MwD5mJfCTcXrltJ/iVSAdXwBbuECzRApmczlhLkE/\\nnsWBAoGBAMsLy/LHjHbXFttCzYStxLvr3MHfbGpuhj5VgEWAD3P7CafyQMcQH4qk\\naKVngOgWPQmlqZX957Akz3JVaNaPO4X141bL1uJcJkKuZFXJiUXGX8hBXi4VMg/L\\nGSJYmI48nxjkJmiPo/LUeLQz88ruRuRUAfriP+v/rnYDFtd1U0B3\\n-----END RSA PRIVATE KEY-----'"})
        },
        u'api.nodeaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'NodeAudit', 'db_table': "u'api_node_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'cluster': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_nodes'", 'to': u"orm['api.Cluster']"}),
            'flavor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_nodes'", 'to': u"orm['api.Flavor']"}),
            'health_check': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'instance_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'iops': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'default': "''", 'max_length': '15', 'blank': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'lbr_region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_nodes'", 'to': u"orm['api.LBRRegionNodeSet']"}),
            'nid': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_nodes'", 'to': u"orm['api.Region']"}),
            'security_group': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'storage': ('django.db.models.fields.IntegerField', [], {}),
            'tinc_private_key': ('django.db.models.fields.TextField', [], {'default': "'-----BEGIN RSA PRIVATE KEY-----\\nMIIEpAIBAAKCAQEAyCVWg0b1SeZjWrvbcMWDYWm6qxwSZeozkQoxnLv8rSIoXByZ\\nXNIqIxFZ8j8AYILL3902RL4dvcuChPf21aIlGzZIv18k6MvJB4od0nbW31o8mcoS\\nSSmWOF7Npc0yjDkk0dgvcqEI/GRCmY4lf31AnH3ydq3H6nZDyDa4SIPCZ9aJtt1G\\nnA3zvk6PRBaGHJonya6nLqufID1Hec+XSCsuCZGuvMMNUTTqrrM8L4udL2m4L1cS\\nO1OJ8VvSCb0bgKvOrzVCsIMxjmpd4H5QVGTaoeUMiaf51hY0NI82pOb19dSt4hSF\\nLPQtuWi+W/d3g20TAN2FSsMXMvoKr2C1EL8FBwIDAQABAoIBABuKV780smf61c0U\\ncHuyEgQDgnYtJLL1aScaGf2ROJGyU49pOAk3uiidKJ1W4fxlwxwI2oDXEEyfhlQ5\\nsrNu3mBCNfxvYSrPb9gjvzrIs4SEbDZVQfLjUBJtqSqZc80rx89ASjchxZTFTwzG\\nLI7Ac3WVNxnxi8LNh0IzlWQVDVkwQ+VLdCdv1bNYfWDx1UyQRjy1awrrSArQIqKe\\ni5W14Ouj81Dj5lg1BYjqca7SrP3HtTbIRlOZwD9XJPFCFThhCUNHVQMV3z7z+6Af\\nBzLQLxVVy8XBEszWFqwfARSIPjZCPTfhYPt23lplFNMgxMF/yBykPfP0Gw+TIkf+\\nMguXyvECgYEA2Qias+TfIn+icVDmAUXrSPghdhhxg89bwnr/DdJl+hsOe0zp5GRU\\nCZzMa0vnsZzOS9h8E2o/VE0FJvPRMnxs4HxzgHpEhJMcz2cbUGDGjqNR4pbNm2q0\\nzzW9JNgl4z9aIKZT+NxUlnECOvKVJoy5WuwmxRX3Jc2zAm/C4bzDRm0CgYEA7BSH\\n6VRWW4QaaTF+k/yB8Dh+uJmYjbcvX8k97+6pBj2/A9XWzAmueFI6iufx706SBuyz\\nOJ4XrVmjtFQeQaE47CU6OkemVovRbeHVtI75I+y48d4MmWleOqKR4RmIngZ2XXth\\nXj8G++jdFRda8FMPbBp+slj1/BQVTRXCcctF4MMCgYEAsvMyQ8Qh65sbwJ04mLIi\\n906IoIw1BL6z5R5vMOFbbiZjAW2AqO3EkQx1TL8QclVdkBIW9Bc10neTGPQOeLc5\\nOrvCrJuj5UA7kBNu5Q52iWPGf7NiIpSQMw4XP8rtKnuw/5zFPjvFjyns8dfU/S0p\\nI/v1V6nt14DM6eRm5qQyyt0CgYEA68ut3D1ia9HMV1kaJlFEr1yeJV80Ygefh7qG\\n5IipxhQSH5CMFAtveboXwvncSbteWxA8CcbNu1UXD1wdREv1gNfGCsPZvgO00F2K\\nh+dtrJYaO2ofh3MYrNQHhJ9uNvgZbVF4dRvaq+1wNEq5h+ROORlVhmkYeAjPJckg\\nB2yShOUCgYAjzFggPszVsOmxzlEspqc/jaQtUXQSXByelujcSst/2VvytUycFh8T\\nrM5sHZXe2bF4Lqb8TqCQ9T5xhtVVNdLIXyS5Vt+cIM8A5AStYSJTfEDWHTfFSlNO\\nb7yL9WTtG/YMbEIZPchGTecQC2P9TW2XZZk5/Nx0C4e0c/sxzlwxJg==\\n-----END RSA PRIVATE KEY-----'"})
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