# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        for cluster in orm.Cluster.objects.all():
		if cluster.nodes.filter(status=1000).count() > 0:
			cluster.status = 1000
		elif cluster.nodes.filter(status=3).count() > 0:
			cluster.status = 3
		elif cluster.nodes.filter(status=7).count() > 0:
			cluster.status = 7
		elif cluster.nodes.filter(status=8).count() > 0:
			cluster.status = 8
		elif cluster.nodes.filter(status__in=[6, 9, 10, 11]).count() > 0:
			cluster.status = 6

    def backwards(self, orm):
        pass

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
            'tinc_private_key': ('django.db.models.fields.TextField', [], {'default': "'-----BEGIN RSA PRIVATE KEY-----\\nMIIEpAIBAAKCAQEAzk6XpzmpiHs3LhjO01gRiYPNyxgF8stxWwutE3WIbnBJWLlC\\n+iaZLN/Xo7DhIv4knuroJLg9by9hRQ8ZCPG53mxsH0wnFdGi9eXBs4StVBc5RjR9\\nkWzZ4C6P/hzV4GicZA8I4OQfz6WsU53ZhbOWVS/BAJEzivHuT3lxiT/AC63l5VuF\\nbLereLEk77vrGx8LRG5cea5J+t8PGLmPxhF+F/uU3Nfmo4/l7L5Tu1A3lJI5myNR\\nKIOC9/86+B3sR1kn2JZsoFLiKvU7JQvQsQ8F5Yi3BVkFzw/8hWciU1TTH1WceOTM\\nbc23sIyg5AL7+o54bVtKaBOpKNoGTtfsVzK3KwIDAQABAoIBAQCqKydp9uUAv2l3\\na10F9GmavQ39TFZzux1IFOxw1YxwU8wcE8vMHBRScFwlF9vMCkbYkjhjOVjrIfCg\\njuB+gSxn65SPiDfhBmbdXuMUGQcDCpjicJ92WYupH58D4nMDxCXjXodbQK+Ajk4D\\nNntajhQdNeODfUE/hWilQy3EIMJenlhrYjQp8+ZdEyVza7c9zgNSRbTmyPTtC2KT\\nmpxU3NFpLAAyc4ouPNScevbIzITUBkvhNR2JbxdAUhTZkUyMHUGmLw5vRrmPjL1E\\nFhu+0l496KoLTOChYKjxo130Y4utcGjDd+49Im6n0bnCZKg0pA6AhQs163rvKOg/\\noXm4ZlLhAoGBAPijJqv/kdcG57OEVe/w0FLM4/fI/pCc4hiO3npYr5aP+EGwVBT/\\nt1xoGYtIovh5MUtDStd6r6YvOm7MBDAsNizqoDtUhegYGq/w/1sFf0xQuW26Rp+9\\nGan0WzYAZtsC8wzmp+Lga8bV0C/rOTOFi6pr4BD+8eXC9BP2FCqetYObAoGBANRq\\njBpPXUitu/ZvMhVulNxtx7TGI9dTT/MBdMEMXrwjQ0smPvyUfhXRWIRxnoZc8voe\\nWVc+KlCdIwOq16zlx6vlu3xBrzQ6LYill07C+qhdlPmvgzktyb0dWKAJewcV2qAI\\ng7j2l+fWHfAhc7oe3ddw/vqGYZx6B9aj3YlT+juxAoGBAOrT5K1j9pD4w5Mn9KZm\\nccsSGmknW06n7V62aOdypXv1Q8p+yBsBHWPYKfADzXARvn3P83qqNAUn6+9DHt2E\\nlDI98tG2VbZMNcBgRDzqZz1jrI429Ybe6cM7t328SWimU3mmy3+a6A/mVvc7GU5Q\\n3gU6V2iV8U9Ino/PxWIvfU3rAoGAcl4jrQ7KNRWFvHvGRY/SipR5EDYWmhr7UuWX\\nzVExuK5rzwx6oVf6QxkCRd0+8y0cjdrFU5nfAqR4c8MKeMcHKOB6f76F7OLeHVK7\\nEuccOoaYbY84YhLrKe2hCBnSqc/0dHHhKjdrNqIsYFxCiRWRcCwgvRaZe7ygd8qm\\nvwf+FSECgYBm+6qBnMYq8hpkx6DMLneNZpYpqgIlfJ4MausW81D638Zckltz7WE/\\nOsEbEguDKc/tfHkpXkV9g5iXqnN+gKqv/HuX8wIOHfTAAakRTW6aGqNHhKAFy8Qj\\n2hOqQQzNHCZGujHx13mw18xyS5jweX5pWhPwmDcAk5133C+fDWmZtQ==\\n-----END RSA PRIVATE KEY-----\\n'"})
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
            'tinc_private_key': ('django.db.models.fields.TextField', [], {'default': "'-----BEGIN RSA PRIVATE KEY-----\\nMIIEogIBAAKCAQEAyxQ6LpVYyy5aX0muER3gsIrOsWS9V2fDvbwoWj1SaDqyQYJ4\\n39hlyMEYfBBurGxMv81hmerS7jYSEt/im4iAZZnnEYSKfrFPUdCDO6xlYwD9gGz7\\nYpGdq9WN1BG5l8mZkkz2Yc5oYJRlwqYU18CB8iE1rPupf11s4EEuwDBjHEJNk1yf\\nZt2/werJSPd5a/1/W1eDlPpa4W7J9DqjOtrJaW2QX9raxml+G7FI+swXr6U6WHUa\\npbSFtVZgX9ZgyoJ4VwM749uYV9NI2nqVzuiyZAH2GbEqTylbdSWhUB4SviyTjujZ\\noxW9Ra2gGsFMRRbvkniuoI/Otpm6GqgDwYygRQIDAQABAoIBAAShI2pocSvAlMLT\\nVSqCudqMb4XPvBk//lBW97yG5VgG7oVbyhGgR0G6VSqO3VcE6QL+VZlCpyhTBzpy\\n7CGLjRHD3mah1N5qgFpnHHbByVXmceD5mwl2NFf0eFU7SjXRnLSfGIbGQ87f0yoK\\nyzLX6p5wb17QJd8HbDH4im5LLBc6yU7Zb3uDG7QpcqXK4Mva57libaB/6LvevB+M\\nxHilgnb9RlQZR5SR8v0TxAAvpVgNYyiF1XAOddwsK3fZPN/55vt2LrgFDq1QbKXR\\nPLxQHNXwOb6/JemwnYsJYLz6c0XTX82A1g2WHuMvQPjEZQ/8c8mEUlGkDSgF7MCW\\nh1ngI4kCgYEA7IoGUxEx9kLrclrdq7t22oPb3x2HqbaZEk3Elz+/56Gh3w8mKIha\\n3/mjZUSKflEvVEDh6vuufuvOq3022NNjf+YIl+FQzl7AuNKWgecC2NF78fNAGFmu\\n4aABYw4yob+QRdVOAiv8yPpVjUmzzJ/9fi42+hJ+2zl6Kkl8edOXe0sCgYEA28l3\\ne87jGMkquWqVazU0H9KotMHk8aIv2Yd3Ej/954VbD1LUR6/qXd8ZA5d5MpwFoIne\\nPsMO83zCXt0E2PpqM37Ukc/cO6/jRqaVKTsHlK4ZxqO35ZtBt+vx534IL32kl5lH\\n+7gudqQUiLQIC2cnMKA2FNx7ZUD2/WT/rt9PCK8CgYBMSArYGRCCuXwSqekY6+Dd\\ngW6T2oMYoTFmLLw8hquNuJtqQwlsQuUDnA8splj/eZEI28+/pyDT/5nrxfq9HBbX\\ndUjKKjiUBQyjzg4JoIVThOMy2N6Pu8RhMOehmT+M2Clfy/VXT/Y6njie0ujwEZx/\\nZ8oFBZfxfOy/3GkPJMSSVwKBgC38KROuZbV54YaJ1lln+E/wM3weVVh5JqnMvg0D\\ndoxKSpMaMXAOTmr1krY9qw37tvGv5uAaz7YCFGjktW7wdefwUWlwpBOY6WSO1gaa\\nYyuogZweBQv1P/rLUwGsTOoiz50oZPc1wgLwsZsoj8ZS/tAdtTMILokw3nyF9TkR\\nX+fhAoGAf9UU2sTrzSZdLzZ5XDe0IXhNLDMGgzfUMLk8cmRZzS9xPahcrCayOUzt\\nCDZSQ9YB+x1RmaoXon5XHyED37g2g+p/+cwwkYeioOftBDRLQrqE87wKBbvRQ7YR\\nRfYx92R2CPm0yMDN/i8fLWMen2qGb2MCEuJ9iPNNllbB/1AfgCA=\\n-----END RSA PRIVATE KEY-----\\n'"})
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
    symmetrical = True
