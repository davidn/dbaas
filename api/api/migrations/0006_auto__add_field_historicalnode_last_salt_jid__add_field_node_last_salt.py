# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'HistoricalNode.last_salt_jid'
        db.add_column(u'api_historicalnode', 'last_salt_jid',
                      self.gf('django.db.models.fields.CharField')(default=u'', max_length=255, blank=True),
                      keep_default=False)

        # Adding field 'Node.last_salt_jid'
        db.add_column(u'api_node', 'last_salt_jid',
                      self.gf('django.db.models.fields.CharField')(default=u'', max_length=255, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'HistoricalNode.last_salt_jid'
        db.delete_column(u'api_historicalnode', 'last_salt_jid')

        # Deleting field 'Node.last_salt_jid'
        db.delete_column(u'api_node', 'last_salt_jid')


    models = {
        u'api.backup': {
            'Meta': {'object_name': 'Backup'},
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'backups'", 'to': u"orm['api.Node']"}),
            'size': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'time': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'api.cluster': {
            'Meta': {'unique_together': "((u'user', u'label'),)", 'object_name': 'Cluster'},
            'backup_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '24'}),
            'backup_schedule': ('django.db.models.fields.CharField', [], {'default': "u'3 */2 * * *'", 'max_length': '255'}),
            'ca_cert': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'client_cert': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'client_key': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'dbname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'dbpassword': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'dbusername': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'iam_arn': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255', 'blank': 'True'}),
            'iam_key': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255', 'blank': 'True'}),
            'iam_secret': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255', 'blank': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255', 'blank': 'True'}),
            'port': ('django.db.models.fields.PositiveIntegerField', [], {'default': '3306'}),
            'server_cert': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'server_key': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'clusters'", 'to': u"orm['api.User']"}),
            'uuid': (u'django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        u'api.flavor': {
            'Meta': {'object_name': 'Flavor'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'cpus': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'free_allowed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'provider': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'flavors'", 'to': u"orm['api.Provider']"}),
            'ram': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'api.historicalcluster': {
            'Meta': {'ordering': "(u'-history_date', u'-history_id')", 'object_name': 'HistoricalCluster'},
            'backup_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '24'}),
            'backup_schedule': ('django.db.models.fields.CharField', [], {'default': "u'3 */2 * * *'", 'max_length': '255'}),
            'ca_cert': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'client_cert': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'client_key': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'dbname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'dbpassword': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'dbusername': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'history_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'history_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'history_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'history_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['api.User']", 'null': 'True'}),
            'iam_arn': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255', 'blank': 'True'}),
            'iam_key': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255', 'blank': 'True'}),
            'iam_secret': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255', 'blank': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255', 'blank': 'True'}),
            'port': ('django.db.models.fields.PositiveIntegerField', [], {'default': '3306'}),
            'server_cert': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'server_key': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'uuid': (u'django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '36', 'blank': 'True'})
        },
        u'api.historicallbrregionnodeset': {
            'Meta': {'ordering': "(u'-history_date', u'-history_id')", 'object_name': 'HistoricalLBRRegionNodeSet'},
            'cluster_id': (u'django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '36', 'null': 'True', 'blank': 'True'}),
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
            'cluster_id': (u'django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '36', 'null': 'True', 'blank': 'True'}),
            'flavor_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'health_check': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '200', 'blank': 'True'}),
            u'history_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'history_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'history_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'history_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['api.User']", 'null': 'True'}),
            u'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'instance_id': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '200', 'blank': 'True'}),
            'iops': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'default': "u''", 'max_length': '15', 'blank': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255', 'blank': 'True'}),
            'last_salt_jid': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255', 'blank': 'True'}),
            'lbr_region_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'nid': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'region_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'security_group': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '200', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'storage': ('django.db.models.fields.IntegerField', [], {}),
            'tinc_private_key': ('django.db.models.fields.TextField', [], {'default': "'-----BEGIN RSA PRIVATE KEY-----\\nMIIEpAIBAAKCAQEA1k5mcPJjlhKd36eAbUr4qX9bpclenjfLxVDmKzbxjsvrJQFQ\\n1gkifizcQN3DxvgJWvA3fV+YWtArwuRPxvzVSNrB6lslS6c4JefWGNwhykzRG/Sp\\nVGsEgSCmRZNgRrsNXQ15or8j+pQcD0EkgwzfwNIDWb80I4PVxRQ9sHrR6qdqEHxx\\nyan2Z0kysX1mcpkWC4GatAw45ydXtMpQJKMyXBkSnbls8amJIgCVgw3LDFCtLxGk\\nfwXMji7XfeHwEwqyQ+/AsSSAOz+DLNxIf7NKN3nSWDHciLdEzk+m6pr2RLCS7sXZ\\nogNwgo8k/cNTWVY8ABrMl+JpzcvA5/nhRjpSqwIDAQABAoIBAQCMnDQqt18QAHcF\\nX+mrzB0LWTzQsicauJFCjan3gL1NbA6E4TAgvy2ai+SXyunBiszYlfRSln5oV13f\\nKd4OOaXXf3DsS5FU6gq1FEAtX4HsMiqhpQ3VDcKO1tVBoUjyH5jNDSJZ3f/FUZh3\\nic5jDfdhlGoOYJ3dD4sbHAS93lgNFUeER9b/J5zjpFWSMoGoZjCiNrRr8Fc/Lcyt\\n8qL5hXXKfoD9KYgTjz65mNvktyIXL/puNQ28sZWbdWAnbfyapVWbKFjOaMsoCc4p\\n7CoPrQxyb4E2yXzJbdK+VAQfcgWRgFr/o8SzE2HkR+cEMTOdvyZOKwcyPvjKBf0K\\naOVRqXNBAoGBAPaY9PTRh5XeHkgR+2pHKSFqJRwU42TBEtgIgqdokZQ0QQFfoMiC\\nSC2VgezOssCHue6/hL3TmYal3f6zca+4BEjtvxH7Rgja799MDAeH4p28CpE1IoWQ\\nlb1dzbcGxX/FpXq3gNVNRChnY4+IRDrwqlLD6OtefxlnM80lJ9zJUx11AoGBAN56\\nP3SLjQoekbC3Xm6ByaH+Vb1U+Xe0shOVO2nLHdy9LfelAVIy8cyo+o3bWEkom2bb\\n2/zOYsgLZlpnw7gWnq0n6HR4CdiUbyIFthUUcd6jLixJPc2kASo0+uW5gPDtOBOA\\nMfzQDivplDPkhAy/DVVqAURzB1OV/ZiA6meWGwufAoGAAaymNSdbEVRxxjGBEIat\\nK9HpsJgftyZsd1UPdg2Kt4PnURgSImpoDQ8v06jPo+kIBSv9vcA7EaP8rucPBY9t\\nUAV1P60CG7tI165PgpmUm1eUhsnikx+ZNLD3XZ/JJYX1CrFGSax9ovyYu3fEZtYN\\nggRch4SbvlNqEaGH9MLVMqUCgYEA26ZWf/pHhXYo4RApa3E4YXd5rzP2GPmN10e/\\nIPQox4b/m0CNzVn+4ND0jpnA0HoG88adqzsYy+h1ZUyNL3Mltk9wcY0SK4JhNnXt\\nD2LgCa+SJqcpHZ6Oh91G2QgNBdEvTBGFSNUhKLm0WIeE2BDIWUwPdEUdNqkfdzHQ\\nO/U3PoECgYB1hplCBiGJ6iP2PInjTnhI1MpvkWuk/sOxpFAHwjYNNw3jSh/7yEK0\\n7CE86MhM6Dp0hqURa27yqPVmJ4DNRkYsVyE/9Y6d/EHR4hG3//NmMefkEfJsHZeS\\nXjiXEsN1r5UB2+N9iMphM41DU3v3v+evEnzyOlZ3ooh7iffT/q0mHQ==\\n-----END RSA PRIVATE KEY-----'"})
        },
        u'api.lbrregionnodeset': {
            'Meta': {'object_name': 'LBRRegionNodeSet'},
            'cluster': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'lbr_regions'", 'to': u"orm['api.Cluster']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'launched': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lbr_region': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'api.node': {
            'Meta': {'object_name': 'Node'},
            'cluster': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'nodes'", 'to': u"orm['api.Cluster']"}),
            'flavor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'nodes'", 'to': u"orm['api.Flavor']"}),
            'health_check': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance_id': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '200', 'blank': 'True'}),
            'iops': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'default': "u''", 'max_length': '15', 'blank': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255', 'blank': 'True'}),
            'last_salt_jid': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255', 'blank': 'True'}),
            'lbr_region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'nodes'", 'to': u"orm['api.LBRRegionNodeSet']"}),
            'nid': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'nodes'", 'to': u"orm['api.Region']"}),
            'security_group': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '200', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'storage': ('django.db.models.fields.IntegerField', [], {}),
            'tinc_private_key': ('django.db.models.fields.TextField', [], {'default': "'-----BEGIN RSA PRIVATE KEY-----\\nMIIEpQIBAAKCAQEAtluw0QxJWSC3F8j2q+5XzZYeq+gclbdeLTyfJcb8lUivwOQe\\nk7aDmIwi2fsgab63rBsHNNWOTCJE8MclwiSs4hsbJgB14lBYIw3b625igdkkoonj\\nnNao6Lx1udiP8iCWsVgRdTGTOYTjjuinz/RKXHkD+H+CchWpdUAjY8OkA46YBelt\\n5Gq5Jt4GjCuOYN+avxhSExxdLu1a7L7ZX54dSNHjzsZfO4DYLT9pGDgAF7OWwfW3\\n14Op5gkSz02by41wW7gaFe7aaD+NZfS6gCun8OQH+hhZhPBGsg1WbFGwvXQOPuz7\\nhpZGP9HVOQa7yI7So5SguOq3/CVSETYGttvgawIDAQABAoIBADpB9q4CV9hyfCvM\\nFwn8Xe6e+/N9dsxZxWt8R3ehJ4Zlr0hXWHFmSIpOkr/C26sMs87234mAhDJMbGvj\\no2tvng+qCzVLxl1jv5SLU+vV2wCSp4KJvL6ZUWLw+kdCKVJ4GMxVT1Z6XQduLei0\\n6Q+lgrAiNSOJUNozk2yS7ftsQBSmSgivBOPM+xRpW2dJTBcRFdZKEyIoM8BknTmu\\nT2B6512no4jEW+t7+KUN8o4cmekFagh0u+oKQ8Ad4C7RfkdBAaMmApVdLpiqPaat\\n50Asj0V+ja0Egja0/t03xmS9X1BfYE+XW8kTN83h474Q2rqOAU1ZJCpSE97ggz+1\\n4f6EcmkCgYEA51lLRh+1biGHPg7U/7nVBajV30aiGJXgEaeBk9ST0wjdnZIHdlTC\\nOAjJNNarrIU80BYDg/6+tEio1rzNVUxYUfOmP1/ZhGNoYygjc9Cl2P6/hqxQrbkU\\nwbf8VvCQWaZPt9cgIFZwllocI+Sk/+ORLqjaZcamb5NLqzXAnfo2CacCgYEAycoJ\\nIs5uK0x+5xk5znxtc8zP5jVCn4+FwLnngnk/CjWZBVF/HL8UwIgnnNvQ+C3B02CU\\nrCcLoo0OpsIJwaCiEGePfd2qX5H35KuAIza1XdgQcDDozckBifaAH4ZGARNRkdRx\\nS22WsSSrzjXw6p8nCx+WQG5CZcR88aXm7f7tA50CgYEAwD//AqYFAiEQnyx6KoyG\\nDm7wU9wBhga+Lk2Rq4SC12NNrsyUMOxcfW4nriYagYIzOASjJURDu9OJovFAfPq1\\nhlzAMXf4bUCilYvccjjYKUwBYuu9G7BrJFQ9eQ3uFuHS60X1J4pNg1QcgGNYDmFQ\\n24JsAxmiY6P2xK8lguJTl48CgYEAqX5SfjH2x9fRIDxIGfDZ3tLCLhO+ilf7eQ6u\\nLyG4mdK7XYQ+yN6Xh8DVxSO+Ozfz/qC5QIDrfPYOwHNrzoAmoLDcDlUKrovlNOX5\\nE5r4bIL4C8SJR5D3AfNTWydl1bFsapmPMFQ0p0auKN+WJPzZxrYZdrUmgGSyricz\\n+eSPIOECgYEAvNqCFb6Ox1tC7iovt0/DkxJLkTTiDDo+KirchsbZLfvaQNm76w/2\\ngM8F3uKCRKrPOP4JM44VGV6ZMoct4GS7kPn/mXIUmdqNL7entRW07fTIdqCb9UvH\\n7Vmbf3luSXTtRlaKmXOFa8x2pWTMLvD++uDmx9fnS/tD7VVcx39OAV4=\\n-----END RSA PRIVATE KEY-----'"})
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
            'provider': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'regions'", 'to': u"orm['api.Provider']"}),
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