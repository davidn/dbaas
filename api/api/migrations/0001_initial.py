# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Cluster'
        db.create_table(u'api_cluster', (
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
        ))
        db.send_create_signal(u'api', ['Cluster'])

        # Adding model 'RegionNodeSet'
        db.create_table(u'api_regionnodeset', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cluster', self.gf('django.db.models.fields.related.ForeignKey')(related_name='regions', to=orm['api.Cluster'])),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('launched', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'api', ['RegionNodeSet'])

        # Adding model 'Node'
        db.create_table(u'api_node', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('instance_id', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True)),
            ('security_group', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True)),
            ('health_check', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True)),
            ('nid', self.gf('django.db.models.fields.IntegerField')(default=None, null=True, blank=True)),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(related_name='nodes', to=orm['api.RegionNodeSet'])),
            ('size', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('storage', self.gf('django.db.models.fields.IntegerField')()),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(default='', max_length=15, blank=True)),
            ('port', self.gf('django.db.models.fields.PositiveIntegerField')(default=3306)),
            ('iops', self.gf('django.db.models.fields.IntegerField')(default=None, null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('tinc_private_key', self.gf('django.db.models.fields.TextField')(default='-----BEGIN RSA PRIVATE KEY-----\nMIIEowIBAAKCAQEA26jiLSz3FwTyp+hwBfz1IpotVIG94i/KwJ2ZaMd17dldJtHt\nd39n0x7Fw4FfROH7+BgjvDiGnjGt0c6TdvGe0qfUrhQ6pnxkM+HNnVFCQWN4ccgv\nN2VmRUkH/EoLJ3DmhSH9y6Yo4SB2Uyvckrjw3Sn+QnkJOVaqRaz/CBJnY5KbMhel\nUvhtgYyLIVGet0XdJQORjj2qstta8c2BBLz/OTbohlJyD6ppRM/hHRx0tKkQkfcF\nWJN8bz1RJ3ubhtn1BWutvAsWZLR7duY/BjLnbvYfmImOY4+BHWpQ5Eg6XD5C/UTd\ny9SrKx6nwWhZodUK5m3eTdvp1L5OL5jcEMofXwIDAQABAoIBAGzQB2LboHdtwwr8\ncOn2ejSu7X+sWbT/ec/bAlDOZhPyFlwRqDIHEhaaattDbj9AN0KaKrGlysH42CNT\n0uccIFI4Q3oMmVU5z6WH2QRyaYDc1qB+yy0E9RmjaOpIf6gFHJyczw2f/SYwn4zp\n8HVaWi8lC0hAjxoxXV3wqdGE1GSVIz1DF4+UeDSeAcvSxLmG9K45TJixWHa0Rg1R\n82fyWU4dE7ZHBywD4KJs9Ju9M0zE7jMQvFROKXg/ZmlkU3i0XU9gJGYw9mq8/wXI\nnnjjEgJaloi2RtBxsMP34KNX7j/vDs3spJJx9z1YlMlhmaHM03OADG1zBXQjXdh2\n8EzC8IkCgYEA4TqxGZe1gBJsC9iGWYbZ4hf3b8NdUMQcORnHe23lW4Jzq0bJojzI\nW1cNFNg202MCs/r2IcvD020M4StPo61PeDk2sP4Z5iNy3YNV6kJgr5tFHwzjyk8t\nQymfKmanmWr4e1dvkYEuobB7UgbC4xZ+nxxUBNp4aNCFvhUfT8YPELMCgYEA+atl\n+LnttiQQYlCOhEcsek/whMk6kS1sBZf2XxbpSv/VcrNbga3QNGAqb4f6z2C9n7fq\n7slT7pIJNc7fQopJNDryOSZFbnUZg39iBqPfgX03GjXM7buK7djaFqOphtG0cB6s\ndJ3uGrTLXDYQ2LbsrvyEMVRrS6eVonRAf7eQNKUCgYAAxtUJg45qrKWWvN5pvJ9P\nukluJzxRJPv77mzTriNWV3LSqmHTn2YJeple8wftXrAJstnab/ty5TNgK2gQ5m4Z\nugjIP3gTZRfmT6eiMSxoLp7kZoT6k59SVfhoiwYU71uAAWMvG0Tv5c3nEILniZJS\nNiTMB3zWz7FGYIhFHCe9JQKBgQDC/Yn2Z7+vsRrare+gf7XNEQHXsxF6sO7cr4JL\nYalyWbxqiIm/DfC99x0tXhYUQInYY9uoArT6bjOjQp47aaUilab321v+mJYEjUgR\nx4qXpyOR5NLYGNC4UdSCOe/8y2sQ5ePqcC21zd3FdrRRjQvs3mqf3D6wJ4JGDmUR\nWlvVwQKBgA2g4xnyTn2NWKiAxW+G+1AwpNqoH+Pcl3SdaF3Mhr6bQDktDbF7lBR+\n3H9HtjGTnrdg1yO5MyE5MbJ0pX/8xgnv4BHWcFhgE3w4+HFJNi/7adRTjhC8MWjO\nJrqUnW4WSyYnZoaWqF/nisqFWcGOHoaPSYunwRIeOrvnyrDzMy1O\n-----END RSA PRIVATE KEY-----')),
            ('mysql_setup', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('cluster', self.gf('django.db.models.fields.related.ForeignKey')(related_name='nodes', to=orm['api.Cluster'])),
        ))
        db.send_create_signal(u'api', ['Node'])


    def backwards(self, orm):
        # Deleting model 'Cluster'
        db.delete_table(u'api_cluster')

        # Deleting model 'RegionNodeSet'
        db.delete_table(u'api_regionnodeset')

        # Deleting model 'Node'
        db.delete_table(u'api_node')


    models = {
        u'api.cluster': {
            'Meta': {'object_name': 'Cluster'},
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        u'api.node': {
            'Meta': {'object_name': 'Node'},
            'cluster': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'nodes'", 'to': u"orm['api.Cluster']"}),
            'health_check': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'iops': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'default': "''", 'max_length': '15', 'blank': 'True'}),
            'mysql_setup': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'nid': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'port': ('django.db.models.fields.PositiveIntegerField', [], {'default': '3306'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'nodes'", 'to': u"orm['api.RegionNodeSet']"}),
            'security_group': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'storage': ('django.db.models.fields.IntegerField', [], {}),
            'tinc_private_key': ('django.db.models.fields.TextField', [], {'default': "'-----BEGIN RSA PRIVATE KEY-----\\nMIIEogIBAAKCAQEAxNPty0J+2Dum2q+a2DqQ/thbSuFYv61sRfaI4WXkojBGHMBE\\nVck8hJp7Fh4BsmRZY8M6vdaboHYtUP4vWEgiXe856I62BT2ML9tWK21mNeRV90Kz\\n0qOhAWJtcZH7n1Bj2NMB2wl+teFRED4MGJDqc0nOatHc2W0ojtygoDC5pXb+tNlV\\nCgN4Grrq/JxdKGfp9QW+VDtMWVo6ECvx79p7ch3lfVmMXOzXHH9ytKreOuXd312y\\nPDLjE0U/vURlM/c3Wt5xU6SKUcap79iQBMAwyl9U8f7BfH/BRg0gHBkmMxDSayJq\\nHPBkiNvO1FNnaBbh6T5esjboePuSgJyFjxWuUQIDAQABAoIBAFDfg2Vw/Q179SMF\\n5GnUJp+P5nLuBLk9WK+mjLeQVlEN5MELfwiAlw0lLE36JlhWQyRqo0g9VdSouhX9\\nWxa7DOPr169mdAPTNjazuMQ/PzAFkgz2q0xxT0ZyWuW/RdRAA8ajbK/DRv0Uh2pV\\nFENDyBF20gmyETyFTZTlslofqygA9DfPEsZUNWDjPX7mJnSEmIO6fvptdRYplPnm\\n/Ug3fydJMgNWtUFEzwnb/Qz/I03bXUXi5/3kmhWqe+kTVJSS4HarNAosQRfWyzxv\\nbLw2VQvzFwMsLOo6Ejf2ozJboxSg6NeyU+0qUKht+lpkPh/EBi1x1CD7wF9m71LJ\\nAWH8nAECgYEA2XbhTMGl8gVcMhm/uwEP0BzckTk8CRAgdqTyPlm81x/F6BFGiOnG\\nPSAjFJpCOgraZoO+B6u9BBlWMEAFam1F/EdrkjYSYsLIqBQw+AZtyE0SOeloeAuT\\n4PbmaqmAjMQlTNAQsWwk6egytpuGuLzYhNELWz2i3rjjss5y5GewdHkCgYEA57Tj\\nF78YqLdI1XZfjHPm9bcf3y29jmTFJEeEn4P4JyWyQSTN38fHrq9w1i8hwWvWH0ZT\\nobv+/24aF6tXpMJcwx+BrSwrrYco33NbwY+Ooaku9bUMeZlQ6Ry4BOpRNVfC7siY\\niCwsFtFZNfSq/DTh0x4OMCYXS6jnNgBrdAZoIpkCgYBzvsSYGBH9SUETIYVdQWlr\\nOZFkcnQz1rOQsqaE7TqHvc+Wf2ttgBAVhL9nPdu2DQTFv6UrbAtE3T90mv7G8LZp\\nWpI01jbe/hHS9DxEJxfTnsHutP73tiHVgVSOvP1A7z1zLuNTq93R6dbkPs9sEIel\\n2aYTwDCqHvqCt0OLsmzG8QKBgDUSTo2q3JgQWyNhmKMQDQ+s4ST6UheiZzFXHD55\\nOMamsLyRFIK0PL17O8ojQ4UNER9auV8rM04IRvuy6EE5r4uV1Nr4agy2D5uWzaZ5\\nHj9TBAmNbY0Qm+K5DEE79lvUfTa6RY2zKGoVi2x7XQqlhjAYC0HmB6Hxzvukfvg1\\nW3bJAoGAabiiRRZR5JfHpoBamz0zair3lM/azqWTQ9ws0vXwYWXcgcohFYj9GWDY\\ny7XTQZnFFuweYNRwHPNEvkzTK9jhcCcXwD3SAVhkuhfnlhkO9EO5mM1nFJHbGbtP\\neRmNdAGsRL7rnppnso+CQFxi4J4zxa6pv6DDxYYIgzKYBNEQYyI=\\n-----END RSA PRIVATE KEY-----'"})
        },
        u'api.regionnodeset': {
            'Meta': {'object_name': 'RegionNodeSet'},
            'cluster': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'regions'", 'to': u"orm['api.Cluster']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'launched': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '20'})
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