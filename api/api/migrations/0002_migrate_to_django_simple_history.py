# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'LBRRegionNodeSetAudit'
        db.delete_table(u'api_lbrregionnodeset_audit')

        # Deleting model 'NodeAudit'
        db.delete_table(u'api_node_audit')

        # Deleting model 'ClusterAudit'
        db.delete_table(u'api_cluster_audit')

        # Adding model 'HistoricalLBRRegionNodeSet'
        db.create_table(u'api_historicallbrregionnodeset', (
            (u'id', self.gf('django.db.models.fields.IntegerField')(db_index=True, blank=True)),
            ('cluster_id', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=36, null=True, blank=True)),
            ('lbr_region', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('launched', self.gf('django.db.models.fields.BooleanField')(default=False)),
            (u'history_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            (u'history_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            (u'history_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['api.User'], null=True)),
            (u'history_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'api', ['HistoricalLBRRegionNodeSet'])

        # Adding model 'HistoricalNode'
        db.create_table(u'api_historicalnode', (
            (u'id', self.gf('django.db.models.fields.IntegerField')(db_index=True, blank=True)),
            ('label', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('cluster_id', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=36, null=True, blank=True)),
            ('region_id', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            ('flavor_id', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            ('lbr_region_id', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            ('instance_id', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True)),
            ('security_group', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True)),
            ('health_check', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True)),
            ('nid', self.gf('django.db.models.fields.IntegerField')(default=None, null=True, blank=True)),
            ('storage', self.gf('django.db.models.fields.IntegerField')()),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(default='', max_length=15, blank=True)),
            ('iops', self.gf('django.db.models.fields.IntegerField')(default=None, null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('tinc_private_key', self.gf('django.db.models.fields.TextField')(default='-----BEGIN RSA PRIVATE KEY-----\nMIIEowIBAAKCAQEAoZ9GC0wI0MCTovMHoq3TNbW1go7Tm2E9Mk6fxogtF81IG6OO\nCtNuOWcYcws5wTOgXW9WG164ogjAm/22blrx9px7q2uO4jBhdAKWvclHQrlRrWXO\nXfGgZkOlTS2CMOQKfXUc1AGh0XWg1Oul3TftXWMdSEB1ROAgppv5yVz8FkYkmcE2\nicfmyxvTBP1L/2kPMMFIzhNEY6frjZNKM052mFAUH5KdvRvS2prAPDCQMfGk9qLy\nDJCnsO2x/eMXADYiWTOm210lI+Et3b8uw5JPP6RXqIC3NTKa6sU2sb+pv4h5VHje\nUQ/qCRIKq4OGnUXhi6+TiUJZGTiZ8w2FzD3ngQIDAQABAoIBAEOl7eR2m838fQ8c\nWBrQVPJLL0EJVSrZJYsz+45Wm0E2LDNdXuvLGXyvWT11+mOSn1Hccxcbq34u2aex\nJzXDnTlSwDS83V5xT6kGGGAxqkEUXkqMrTcHFtMXB05peO/L01Q1u65FTJzmdj4I\nsDEK4rBO9wex6yO8CA6UhJWy9NTBNuIsoiIJZ/0eA2xuPH7V9yoR6lKADR17aMd2\noFWv0L5zAcGd3cRDQ4rC/JHfDqMNEZ0BozKSbDJvKvBG3tjBz5v+4eJOuiicU4TJ\nSOCEPQz0gqVRNgW3QSZfDeJ+/fWAOLtHhhd8QWo+dQ5VK+V2DswpwwimU/abzNQa\nDVxNAZ0CgYEAxdHdgfxPycitaIZCA3EuA4ngR8XmOrcZrLGeIi3RneaiHoLsJ+sX\nJAeaSbn8pvWPw6znnX2whORWmoTYc2hukmIOHmlj5zCNLlW7P19mYbfjGBzJlEqq\nlLHnK+BlQtPtU6rukeIbJQo8Qvoctnvd3c9eFXXlpcO4/NQWiBKlNZ8CgYEA0SgJ\nl6clsDmTu00TlDarNB4Gu1BxgTDDrli198KXQ0TRcvN0lXAN/6JYtUCbqkcbrx2i\nIXEnsL95gRDkfvT6JoTr5YQ7Swp1eQCOTVDEqu6E6tOt/yeXYwmT39rpKDqyhdtp\nJ8Z2vCTBFksWU8wDqOQUND4JSkmx8JxIZ1Gqjt8CgYEAs0iUvK3zkilyH/0t7viw\nfzyCLApLsoMnncAMVWW5SKYx3/1AEp2aB2lsh80sEhUUCn+2GqJDTO21H62ujknj\njH+Z1C4oAOubyJaicbkAjSefhcbxWpihKMpjfPyOSZbQzLdqKIUHnPY9z2Xmh+yT\nE+hQmJqVWzqbeWiuUvyzBnkCgYA6UsLSAi8VRAj5CtYx10jIYLMZ2qW8E8ANRvl/\nHEkX3gHV3yOcZEHTDg9Ug66kve1vWIEUeDxMIiicn/xHlsKGqTwqpUPvefwmAMyt\nrJ8a1yZDYUG8y+qAGHSe0KmBqVSM1REuoT4M2ubo84lHVrWSi/9CTiZDC+fNo5bh\nELnR2wKBgA/VOlTXfZTHUEUzLIlvVmBFy9Kmf1F6c78Msf1K56Uh17d/HClkYpBE\nUSXJ53NmX1qMOVR3nMQQBDLk7cC8NmfaNTUnJDXgvcVhNTKLwUFfi1I29yw0ezMI\nE08xcQAIXSFF2ccm+CJLFlIY9ZXp/dQt7rcJGyNaIL8mxofgJp4s\n-----END RSA PRIVATE KEY-----')),
            (u'history_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            (u'history_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            (u'history_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['api.User'], null=True)),
            (u'history_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'api', ['HistoricalNode'])

        # Adding model 'HistoricalCluster'
        db.create_table(u'api_historicalcluster', (
            ('user_id', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=36, blank=True)),
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
            ('ca_cert', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('client_cert', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('server_cert', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('client_key', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('server_key', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            (u'history_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            (u'history_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            (u'history_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['api.User'], null=True)),
            (u'history_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'api', ['HistoricalCluster'])


    def backwards(self, orm):
        # Adding model 'LBRRegionNodeSetAudit'
        db.create_table(u'api_lbrregionnodeset_audit', (
            ('_audit_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cluster', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_lbr_regions', on_delete=models.DO_NOTHING, to=orm['api.Cluster'])),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True, db_index=True)),
            (u'id', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('launched', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('lbr_region', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'api', ['LBRRegionNodeSetAudit'])

        # Adding model 'NodeAudit'
        db.create_table(u'api_node_audit', (
            ('iops', self.gf('django.db.models.fields.IntegerField')(default=None, null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('health_check', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True)),
            ('tinc_private_key', self.gf('django.db.models.fields.TextField')(default='-----BEGIN RSA PRIVATE KEY-----\nMIIEpQIBAAKCAQEAstQmA4zUmnv/Ie9/c/FByeQ8VcaGJXFoCI2KkYPdJoisYPGE\nA/bQ4MNIxcRpj+mwLaLWPqTn03FR1jftUOyeC+XCH0CSKflIpZHnIPvMSa3WcEpy\nP9H+MAmeulfQ1SW3whjXmxqraLfhCI+9yvAXg7/rw9JoEc6donBhWiUpBcOPmKcs\nHwZ2H8gRJjebfY14srNQqC65Sy6HZHt8Roy9EBGadiikFbYd5GeickVut2PWGn9Y\nnPYoSVGEQq6VxhZNB+jPtTbR+aqrRkNCrQ1VckbXdJc3u8KMmd85o1f58UIny4uy\nRHkaracNmkR3/WGSWddnGOZPe1KVOu6/OWOO8wIDAQABAoIBADbbbW3ZXb6mGvXG\nCkr+zzenk/qcE7qYt1koUkGhOc4ATyDN9blhlWHdhg1k2x0SisD1GtPMsnDiakBU\nl7AjZbgwmwQLQsstdWOVBlnP5DMV6Jo5vCJnwJnr2Y1AMwevslcQV9N0svBEt/tw\nXMBMNmpsDV7cxJ/xydlyr+p/S75AYuLfb/HNjJRng5FpeBVp+Gd9aWhZdTtLOKWv\nGgkO+2by71p1W+xsl1BH6hRXlHN97/mBsvy5iERYtUN3t58sImYVkUhvmzxCTsNg\nDNLRtOXUZ0b4e8M/JxiVv2Z5tk2xMTPLwzXJUQVX5+JjadgJ11uKmyn8X0qQOVdi\nKiubyUECgYEAupCN7ZK8bfq9yrvrMaw/6ZRSWwrEyEq61XBiwIgHHtGRZ1QFPXyL\ntwN7jr0YaZtds0rs9cDrSiufYkzEV/CJluT5PdOC07WGVPCKoMli5/dfHkTt3SUt\ntU088ZRn3CIa1pT5Skm/HZq87tYPpjDcc/OeLYZHVhYratFGokLF8+0CgYEA9WKH\nosXGo8cQSSdoTofUDjvy7Zh80XadnZFjNEE1Y7Hw489B+4KLO5+iFs++LMy9DQSF\n5pkOXpn3FA2WXOszP9Y6WcbMSyEHKfLsEwfZMJFM0MbxIzmjewIa5WTm/Tfh9Skp\n5mF0u2J2onSaiLbGUstA+8fnsXz/LsxTCBu48l8CgYEAtx98sFz/p9Qexwh9a1xv\nv45e6A5B6XewvCB8Tg83LgD2gD3whtHhMdqxRQJHHCHsbzh0LyUVzs/SumIvt0Hb\nS8mk/BLIr5XWLTmOWRRTiO0+6C8wa4k6vGL8FwRcja7MOSQxLcIFXcGtAaIL6ky7\nlvThpj3Pd6h7JXYVpt9z/mECgYEApKrBEIcd/MvZ7u1l/sUBlae/Jpgcssehj5p/\n8xILTOKdH5L22VvKKXG/aQVxvkiKWRD+9jchwHQbrTZM///JvX36XEKe14/Laegd\nacvrgL8QyE2ohhXo0eQgvm2O4MA+frFn77TYi+LQb8ZF6ZaV0fuZmRyWK7IQ4Iu2\n8IsB+osCgYEAh40y62xhfPfq73q3etcKZBtmPxz0/6B/w2BF1BkW/on5TbshZpaO\nhGVR8z/zazJRRpyuYrhTf4w04DCtGzl+MLN0na9TKuqQaaaNFlC4v1dVayuyEise\nFPqM/R7/Oi+rp0meFQGh2R2pIsHHpH4/0z2g3OS+RbBjjYdUr0cu+jg=\n-----END RSA PRIVATE KEY-----')),
            ('cluster', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_nodes', on_delete=models.DO_NOTHING, to=orm['api.Cluster'])),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(default='', max_length=15, blank=True)),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_nodes', on_delete=models.DO_NOTHING, to=orm['api.Region'])),
            ('storage', self.gf('django.db.models.fields.IntegerField')()),
            ('nid', self.gf('django.db.models.fields.IntegerField')(default=None, null=True, blank=True)),
            ('label', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('instance_id', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True)),
            ('_audit_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lbr_region', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_nodes', on_delete=models.DO_NOTHING, to=orm['api.LBRRegionNodeSet'])),
            ('security_group', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True, db_index=True)),
            ('flavor', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_nodes', on_delete=models.DO_NOTHING, to=orm['api.Flavor'])),
            (u'id', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
        ))
        db.send_create_signal(u'api', ['NodeAudit'])

        # Adding model 'ClusterAudit'
        db.create_table(u'api_cluster_audit', (
            ('dbusername', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('server_cert', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('server_key', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('iam_key', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('ca_cert', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('backup_schedule', self.gf('django.db.models.fields.CharField')(default='3 */2 * * *', max_length=255)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('dbname', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('port', self.gf('django.db.models.fields.PositiveIntegerField')(default=3306)),
            ('_audit_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_clusters', on_delete=models.DO_NOTHING, to=orm['api.User'])),
            ('dbpassword', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('iam_arn', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True, db_index=True)),
            ('backup_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=24)),
            ('label', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('iam_secret', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('client_cert', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('client_key', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
        ))
        db.send_create_signal(u'api', ['ClusterAudit'])

        # Deleting model 'HistoricalLBRRegionNodeSet'
        db.delete_table(u'api_historicallbrregionnodeset')

        # Deleting model 'HistoricalNode'
        db.delete_table(u'api_historicalnode')

        # Deleting model 'HistoricalCluster'
        db.delete_table(u'api_historicalcluster')


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
        u'api.historicalcluster': {
            'Meta': {'ordering': "(u'-history_date', u'-history_id')", 'object_name': 'HistoricalCluster'},
            'backup_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '24'}),
            'backup_schedule': ('django.db.models.fields.CharField', [], {'default': "'3 */2 * * *'", 'max_length': '255'}),
            'ca_cert': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'client_cert': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'client_key': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'dbname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'dbpassword': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'dbusername': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'history_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'history_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'history_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'history_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['api.User']", 'null': 'True'}),
            'iam_arn': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'iam_key': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'iam_secret': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'port': ('django.db.models.fields.PositiveIntegerField', [], {'default': '3306'}),
            'server_cert': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'server_key': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'user_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '36', 'blank': 'True'})
        },
        u'api.historicallbrregionnodeset': {
            'Meta': {'ordering': "(u'-history_date', u'-history_id')", 'object_name': 'HistoricalLBRRegionNodeSet'},
            'cluster_id': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '36', 'null': 'True', 'blank': 'True'}),
            u'history_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'history_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'history_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'history_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['api.User']", 'null': 'True'}),
            u'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'launched': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lbr_region': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'api.historicalnode': {
            'Meta': {'ordering': "(u'-history_date', u'-history_id')", 'object_name': 'HistoricalNode'},
            'cluster_id': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '36', 'null': 'True', 'blank': 'True'}),
            'flavor_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'health_check': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            u'history_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'history_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'history_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'history_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['api.User']", 'null': 'True'}),
            u'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'instance_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'iops': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'default': "''", 'max_length': '15', 'blank': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'lbr_region_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'nid': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'region_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'security_group': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'storage': ('django.db.models.fields.IntegerField', [], {}),
            'tinc_private_key': ('django.db.models.fields.TextField', [], {'default': "'-----BEGIN RSA PRIVATE KEY-----\\nMIIEpAIBAAKCAQEAquGCMNE6a2Nlms0XhkDEhLzqlN8XLYQ8xS345eOLHCOXdIk2\\nNDihAYHEYCAeZ+3dQnujEj2meiItV1MqNALr5Dy/IR3qogciO7xiMFJD6R2sJUfK\\nIpyf6CMawQJxkGjnHbHJf9aUh0pdhniLLotDejIG1OSZBfdlwtuoASR70Zd4JUnT\\neImCVmxbZ9QGxUyvv95gv7wmgc5okLui/BNFGF1WhxNSvoCQwE/MT4BiHWXryp2v\\n54VJSwMuZk0Z8Sc69dpPNxZFiaW9WIDzY7juUUL3OGcbgSlE3rWzXBp2RntqFDm8\\n+6mBDVtd0w1iO9Q+q4JrzASObCrCDzg71wuEkQIDAQABAoIBAQCGRecQRwgZpCQN\\nrMSkaLZC+1N1IYvL51H9Oq+OrOr9dHYpSzw9cpYJYheV1QcvcThgalhsF+d9pudr\\n69yIvBbx5E3nTuO059gdily5TZsxTXCcZrnN0rbQKO135lyoNdYNfkswWcOiP2wY\\nIxZyv1mJZk/575rSlmDu6b0tEKb+vDTlkKiS+WbaUBuRbN/4kJ/X6lqPKOtDlUMF\\n4asZZcfL7Bqj1Xnq1Asalg9dKuHZwASGUSfnnHYhFDCQ2HINLIguXs3AbrBWA6aW\\nL6DDoWXFbd04wqJdTRa2HuJhwDxCMAWgCcb9zlRJ/TCUaYVnG88tNH77XBi3Lk2Q\\nyNlTveBBAoGBALoFNEFOhzF7e1mAUOqVUEie93clwXDOvqfxeo7rsgNjSprTEc4U\\nFjZNTHrlO2C5Cqb4aSDdbmUfRHVi2KI42MV4d29KnJntj/MENvtXGjdO+kodNCnT\\nuVNH4L48LQKZ7aqmKzGipwfqKv++1ZB4F3h8PDFEMCVtUAgTnqWNhRVpAoGBAOsq\\nStJE4h5Uar8xk0eCSmDkWi0v1nAj9DvpRDSQq9uiyivbnZbRoNAQWXasQCYFePro\\nf2IzX4Qszqg0sHXNj24nIG31aUbPl2aHa9e7AKtuk9jN/NPNFh/qF0Z6yE1jlegI\\nuP2OqW3i2YnP8Y7R3Ui+BJfraWP7s9z6t85jicjpAoGAXCBBreo/SEFYaI4FBPin\\nxx97fXWkZMLvZ2tPgEK4abcd9ql70uzdx0znCKJIkvFxlhnGrvEbQFeI5v3qPgUb\\nTkkIFYUFI7KkrP00YavUnvmtOVFXSTPDP7yEUJKq0/P54Z7kG3Prdx8A5qHTUPY4\\n4YHdqaSUl6SYkzdsRZ9d/qkCgYEAnBydQuz7dsrvejD85nG10pCE1I53OkaD8emu\\nn36St+FfeLH38ZEDwlu4KDG8/ACSCW6icZxNAj+EiOFBa1KkrqlGu/g4hQt2JFgt\\n3S6FCUkE2N4VwrzYvSL3hJApvEYp07lGpPw5uXrokrX6U6c50Ppjrj5W3krPYhkG\\nP/qQE1ECgYApB7LUoQGAZYHGj761gYeNJoonplusIGhid31+yaxyZ7S0MgrBY3+B\\nrRWPKOo60R/bWEnksssXfk6ZisrQPPYbnKfs0CuD5uc/THTr2MKYL0rXOlaXGUhO\\nUOL3SASNn2c+uaHXMsx2j/Lm6iXwucGRaALmHgrFNdQ0GLsAOAUtkg==\\n-----END RSA PRIVATE KEY-----'"})
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
            'tinc_private_key': ('django.db.models.fields.TextField', [], {'default': "'-----BEGIN RSA PRIVATE KEY-----\\nMIIEpAIBAAKCAQEA4Vuy/rHmPqfg2/FurUin9Q0WbyNXTXksd+Qpv6p6Vkmy74P7\\nWXyJyMbNeV3ryZ27XsXJ+LjR8/fbfJQzTFExGHeQnddTntOm0QNw6U8E5BsJYwoo\\n35FnE4DJHIN+HBPeK+QJgmmOyINch/BaCWFvFh9re6DuaLmnmrGXEkrGHb4NJXsJ\\n2qY+tUR6wYujvqNXRIje/LIc8SrripodFw5cRWHNyOICoUWKVHXBhkBUaIFvMUGG\\ny9pi5skWkm24+TEer0p1hUpiDc0fle0XiSI0twCz8ld7HPN48kWVmJo0W98xTZyw\\nOi0zjEQXKY6QUIFq7zxAGmdOI/2mM8msjtUvAwIDAQABAoIBAB6I/kfkcv4qYR1s\\nKULxhVB+5XtJnpqwwIW+NKnzv3/RnJ03lOcbKNA7n7vCLiCzbp/4zNUWtdwIyYSn\\n0AuXNL/L85xvgLUUmJXZkYMLYe5Ge48f4Unpub26xYVHi97iEkiALYmuI9qncfI5\\nbvm2agblWvr1Y1htT3h2d7HSz+VXifORpkxA7BLfQ/V8K2dOcCa1/BlNfKLluXNj\\nuB8L7/IfSi9S3wBBstS5m3t6kNIleuUkn6wiAk2D2xnsiW7FAwa7HCENOagzmv4q\\n6+9+8P2GasA/TM8A6h23/mXaykIm0F5Ye4hXpk7shny4gtyFYEg4/HmsmJnHRMFW\\nqZ05DIECgYEA6gL3nYyFxINoU2WGy/+yEHaQJ7MxA4bwqADU3EJV0MLpCYbkjlju\\nyVFAe0L7wFNYIiHdN/EDRvJPlBpwPORwAtaQHinZtjCB/m8hC81KrFs6bYthGmh4\\nFw06mxptVaZaHvlJC0oyzOJDG1PlnauDgWQJPMXWe8WlVRicFjnXWscCgYEA9oiU\\nNI2SoUrnBu8oVZHqmpsOUHJHu0573kJbSuYhvdfTvdcP8/Y21oGyRTGQyxFKIsdy\\n7ffZ6/9eC/0TETQqOX1zr5GZajV5Kd1JN7bqbisg56bJuGS/2PCDeskYkjpVBxxC\\nSve6UxoCNiXywv1RCA5kO4cK/YsXUj3nnvvkLeUCgYEAjHA5cJjb0sLWQm6Exjru\\n/0hYXSsCOE6scPcGyCUbYU0IFAqbcf5XWARmQVNCyPp7wwg1vhPrVpGnRofTYgfq\\nXRmtphyRpvBXo33IBFAxB108pG9oWDPoFlV/HYRvp15NaZdLyfW+pQ0JHwZroANF\\nycpibNGCVgeYoIhDbGdMIhMCgYEA3FNPcHAd3TwdoFrYRzEy450ze73GUaVgmk/f\\nWt60xP8/4udzAGrIs4gRlDkp1/HJua9aDUZ2Ya1FlZ1FDxj5q4tsejm7S+oiMMHt\\nD3fPp0mwDJdIrByOQAki1/ckmHq9Rq+Ap5Mh1+bklxPvE0hkxLhn57NWpSVLYFqm\\nx7UCRekCgYB3auqvB95bxnlzqySxOs7qfuO0i491R3sftueAEfxbH3g2hPMAyASC\\nmAdE9ReUqhNPFDQ3p+b2UcK8JjIcCir/CQC2B4dO7oYGSj3fd9OJdbcpsgJZS3lw\\n9BAu1swaLobplTtAgXY9rrF6n2t3z2CIKqqYOhJYjn8cjSPoIoHbeQ==\\n-----END RSA PRIVATE KEY-----'"})
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