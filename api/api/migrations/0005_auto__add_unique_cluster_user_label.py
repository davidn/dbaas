# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'Cluster', fields ['user', 'label']
        db.create_unique(u'api_cluster', ['user_id', 'label'])


    def backwards(self, orm):
        # Removing unique constraint on 'Cluster', fields ['user', 'label']
        db.delete_unique(u'api_cluster', ['user_id', 'label'])


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
            'Meta': {'unique_together': "(('user', 'label'),)", 'object_name': 'Cluster'},
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
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
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
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
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
            'tinc_private_key': ('django.db.models.fields.TextField', [], {'default': "'-----BEGIN RSA PRIVATE KEY-----\\nMIIEowIBAAKCAQEAuxWDUFUlLZ2tYIohPkiGdl+Stl0rrpn/z+bGu0Zmq1Atdme4\\nQqCZvQEWRp06pl/yEAt5UgzCIX9EcVPdCRsB/YBLKmfDBEmILclQuev11TVFjK55\\nKBo7R8kXYV7j2Vtr04Z5Iz74NWLgsfLMSujiTRLOIEOV5iA6dLHGXQsRKdKtlc/s\\n3lsCndc+AuqI1yf9/jyifWuBehpMkZMmXIDdrKDNjFCnTRZwzIhagR1QCCzE1Hyv\\n5zO9VbhafRKxw2ZZDisEFNI2mFi6sFvysDU1qgRIvvco4u6jE7nm3drh16ZFCdS/\\n0hm5imso2ZiyR0KotDQdwFhRl5jqcjn8syCVrwIDAQABAoIBAEGNCSS1oMA59kzU\\nOU+sc8i4NhzFyo90ECkVcF6gDUtLXZKWRv65bQTHg7mcT7eJ+LPcgVbZd4/rGt0m\\niFUvbGQZdrzV/IPdC+UXG7z5S3q4HrVrULJXdpvxfsq0R9uZ588G2B0cbDWwfpB7\\nRU+eB+T/iM/PPo+SjUjkHV/uh8YCHS+QH5jEiG0VUZ3fdHWB0HEmgIDMTm/k9mrT\\nLuaNTCYfGlevzg3kLJPwoW1eNoNcUd+TbTpSmgVuftPKqa7vB9yExxdf9liB9jzs\\nhVel0HqXqGJNJROoqww9TAA1I+Qdndm3mBsKvRqRy5RRsfXLMpiuHLno0rUTdCeE\\n5divbEECgYEA4vv2fgxxi8bclwzGbWLrM2Qk8FvQfl2hBuzxjUsGtVwRBEWCqNbm\\ngCjhdZwmieVzAK2zOxOBs2SEVTGj/3yGvV02dAbjERP4+S1eP5wZrHPnCxGVZUo3\\n2amk6X1P2Oby5MpkjqUKSvLwwWfF7C7Y+rEUmcj7k47O6DME6zFyv6ECgYEA0v/R\\n7aJGBuc8fJWbRLnKAiS7+2f55K9h6akHNQxNWCioqgqLzEC3lo8l00qHlNp8b7ng\\nC45BEY5g2GtVZTwm5KPZTy4stgF/+j874dU6oJt2Z+WHw75gRH5P+/eAaNA4Rqtz\\nKNdR5Z6R0zynWQlcWmO/0DiKaQpQi3M/T0Xuk08CgYBAMQ2GnDJIW1brCNvc94qY\\noAuqRezyr7voX334fW1KQN03HglTgmLxf54zSpPDj7Y0TOtRG7UkbJrYFQ/SIv9f\\n8kqCCaiRndpdba0nxBemo6iFgtWDLbgZwFY5Cg1YxAeRGIPTq2z7wTTBHX3ly2Hl\\nk8rFqwcqtcph9HvBn9xZwQKBgQCNGzAVL5SNQU8eMh7oUydZT5+3fc2Mtg1Q6g07\\n2MJQ1sAVF4BuVElyksDFEO6jCYp2XWQL1lKFnyX9FarCTPvlo/3MCiE0hsRDYs51\\nNNhEWDNTQBkPOt2+cIqlAtwJPFamTDpzcav/V5BGKCXyUWRFvrekVGub254J5ETO\\niwIF2QKBgDQGVw+bbj11fSod5/qJBhCH+2iMuKFU/CWF7D+Am0T05LjabFSxUS1V\\nsjdo8pqYAbvlemblrN5H5Sw7ktKj6yMa5IcV3iakHL1vTFj64CIaWYJQCbYChTPS\\nqVpUlZwu/i75DBROAHFE1uLnUKcpbxvcpGQ9E1A4dOzhUpfeW4Fx\\n-----END RSA PRIVATE KEY-----'"})
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
            'tinc_private_key': ('django.db.models.fields.TextField', [], {'default': "'-----BEGIN RSA PRIVATE KEY-----\\nMIIEpAIBAAKCAQEAk4jno7LwXHCGSPKK5Rn4mRqHizDdE6Td0lC7WUt02xLPeeC7\\nXkwVjPyhdrSMZNtLPg3tAlb/itTG8X8tHY0W43k9Gb8utJ8GMw0agudM1DwXcnM3\\nzCrEQ6HtN1r5DYMBjUYn7FaYy2KEG59v4IXnE0AxnaGLLhwu2v/d3CsmhvGM8I+4\\n+hdiUOi8BvFcDJ/urHHZBNfJKY49vhqvBDiyZ3+D+2lWz/vUo2cX3XnsMU+VBamu\\ntt0aTUo0iTWg+5dGRilwfc9Y2gWtYrygxqRkGm86NNHiOBdlL2ZgLDfuW/Hm9xLo\\nOZx85TioHPzvJF/y0CtdLx0zdSmEGuCk3pWybQIDAQABAoIBAAUPhSKQWL5S/cgy\\nyaDiKyzVRCD6JBswZIt6SXLeq7t4AbXkh4jMg1C6ua8gslAjVYljYOXbphhVBB30\\nhs+kr0xONFJVxHxdmBDYOjiTRodhKEy8twVB0kmfnEtxy2kzPTJjXas1rTgMwQtR\\nhLzm2u5GHW2SxPtn7BOHA00yDbhDM4VI/oHXc1Eo7nlYxXCO69crHQiwdDkkchgq\\nXgYQP6p7/sGis/WNSQ1LO8vTfVqr7A459dIMocTIDVU/ybDXVE0QopbSLWp+Ny3F\\nTufIELAuWlIzkKc1nvlCD3GGxEF2JdD0j5rpgayDN2SNqiGE39TANtJWtzklFKhL\\nappzZgECgYEAwqrVSweyhwF21WCs2vd9vRNcDRUknzvkERGxW87hNn7gaE4FRUPO\\ne5Qzf4rvZybVGr5m563nzUqRpBmO/2zZmQv0q2YtSW28apsXqS0bYe/z0/UGKt5p\\nVevjNi/7q73CWyAUWYPRmBKNGZx3bnhUVRQsjuOCZfMlQNAI4TwPzN0CgYEAwgSH\\n5A7eWPaXS4O7/NTdXYuJ7h9cDmpmY7ioZHgLN0UhPpD7kuKVXVIhQA80v45ux3iu\\nurwm+QjkDY4K9x96lfN+mlXzkhRp3hzFO1j4GdMh1VT9f3YeUs7IUpLCbzuFQ/hu\\njPK0gb77SGD4cUcIurPKeF4bFJWRuR1IZvPVGtECgYEAqQfBUPcME6I31yusrC0+\\nZxEKWunC9OkCLbgZMsi+UZ11qdwlQ3GPN0sGNHclTYIwhJpTrFQa9O0M7VqsCiov\\n/26cMr/0DtBUTJUCxIlAP5glNiSKCGs7N7otfn3Hn+aTfqCqStflBJEHJ/fu1GNz\\nhrSPxDrUnUW1UUPSkhCe/5kCgYEAgqZSa/ynNfk4AJ4BJUyilK+2fieX8g0sTdK3\\ncpBz3RAsRtmSz2LNej4oLd8Pgj8D0kcuQokZJXIbQBV6xNbp0bhadMuUbbZZZDyz\\nhDdxOtK2YdYNrpt36ANfWluBmy3Vm+PbbgayDvzwcdj69C0Fb9RKb6vPSJk/vAxA\\nCTQBOUECgYAv6rCLvTA4zZYscqjHEiYUTVR6ywrn6j39XtRrTPGLuEJD8yaGEZTE\\ndfdSIEo0b0aSr+gou8p5RywxnWF9cmI9VcsZTvGbW/xZQ/c2EykWSr0Lqb78+2jO\\nMmyfsL5McNwCycEQdWRBgZDaaTAAMG32BzfrZHqNTax2zDNX1AQLWg==\\n-----END RSA PRIVATE KEY-----'"})
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
            'key_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'lbr_region': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'provider': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'regions'", 'to': u"orm['api.Provider']"}),
            'security_group': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
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