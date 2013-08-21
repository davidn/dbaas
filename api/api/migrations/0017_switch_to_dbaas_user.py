# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.create_unique('auth_user',['email'])
        db.alter_column('auth_user','email', models.EmailField(unique=True))
        db.delete_column('auth_user','username')
        db.rename_table('auth_user', 'api_user')
        db.rename_table('auth_user_groups', 'api_user_groups')
        db.rename_table('auth_user_user_permissions', 'api_user_user_permissions')
        db.alter_column(u'api_cluster', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['api.User']))

    def backwards(self, orm):
        db.alter_column(u'api_cluster', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']))
        db.add_column('api_user','username', models.CharField(unique=True, max_length=30))
        db.rename_table('api_user_user_permissions', 'auth_user_user_permissions')
        db.rename_table('api_user_groups', 'auth_user_groups')
        db.rename_table('api_user', 'auth_user')

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
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['api.User']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        u'api.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'})
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
            'label': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'lbr_region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'nodes'", 'to': u"orm['api.LBRRegionNodeSet']"}),
            'nid': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'nodes'", 'to': u"orm['api.Region']"}),
            'security_group': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'storage': ('django.db.models.fields.IntegerField', [], {}),
            'tinc_private_key': ('django.db.models.fields.TextField', [], {'default': "'-----BEGIN RSA PRIVATE KEY-----\\nMIIEogIBAAKCAQEArzCtL/XseIMI3I9XnvTtZdIipWDE3WlZfHnnEq0W3ccdX/rC\\n5KKjE1H76BvlS3LHvCcVK+C/pttkZansW2tus6iujc9gu64RGCAU/gYHTSj4geYq\\nWGqoP5dNaDQWcS5FLaUxGwL7JdkrClhTfpZUUvF8IBpMssFovqzJ2Rlw9gyqlMI+\\nohcy7AlZbhZpGIobzo82vHW1Ku81D8Qi1pTEvx+HCnZVNyQaGw2z95JDhzyBYH/O\\ni48+jz4ojpnGWIzrmeWO7gagSBW1qYXh7vrlWWZS+0p6xUsF7++14baxfCCmh60R\\n6HzkE9RQHXP2ArW3a3aAuWa3EWdeLApLhI5YjwIDAQABAoIBABjFpkeY26YyySb+\\n8eHdOlBihVmjNFMmmWu7hQwkA466oBG5UKOpx6tstVUd1K91fH7De//nWNJMRYcG\\nnxBSQaYP3RbaUxBWzb3+k1lUGuYzO+iKVkSIWGAdkemBLAc3Brssl6P9KOwyKB7f\\nXHcS5LuRv/5+GYhRRvFnV2dmbI2uAmtkGJhdExuPxA/uPJ9MlxHsf9hW82mmhU9C\\nosenQJsysQS7SmzC/ruE6rWKHsL62XlOi22Wpnah4zCb7ePMXv3z8KC0veHZtP5X\\n1KS8VPRXZeXKxw/Jb4KwhwpQiCgc70+s80L3myd5HnzZUTAtZWHmSuxceijZZNnt\\nF0vc5xECgYEAuaDa8F+TGsOM8ctaJbbeb3g1hq6AM9tw6i1rdubIGnjT3QrzgM7o\\nbFgVqQtK7R9AoH1JschXk25sOydcn5eL1wI7gDTJGOlclL/wmB50scUgXKz4JxXM\\nTcTF+YD8SmNdbTKLz0Ypdc2joThnQuGfPe6qTxaviGGvIi9/yCLwytcCgYEA8ZrM\\niZzxAaBTh8WW+2BPpPmR9025EZQrsfVvyuVwci7/4gmO15w2KvGGzUd5Iwx5LCk9\\ncLYCtciaoJCP/BS6ZOObZnhW2DY1cehDE7WXMwkk/7+XuYXgzqbdxlrUBo636eTh\\n+S6GpNvaty7eZjxIPTq6U1Hm0ildTSkL397qoQkCgYBYOWdVT1dvJPncAbY6rotR\\nl2R5On6cJvOnmSa2QEFis4KeUBIjajN1KvhAe6mEwZHJtUJNSNa2r4ipJLAU+cXw\\nzpLRAEWDnYXu/Lqw0ejMhNA4u8zFZsrPO3KMfw1pnYhN2fQw8zvJTY8zlMcfNnSk\\nzsYLCNEslKDUMpcc295tyQKBgAw/JoMLO4QzlkhZka+oUCEyrV11yR3E/voEUOhd\\n/Pcsvre8eEshlfVTTNv29YL7TOEaLg0ajMSeKIhfC41hl5kpmGT3UJ+hD9B4T34e\\nRE3H9uIn2g8DZEPVXYSCciDq9xOaEIJLA3Qz2MBUVd2kzJyd73ftvN+GTT5uCDYO\\n3KHRAoGAFm9kqxGU95BExL32YRq40Eg2saZDAynhLFcUrHEG5L4IhcsL69GA3Rkr\\nL1FApAw5N5RbBSVBtHITrdyA/2qf8IVfdQNqpaMwa7sGw/wD4gv7GIRwMynyfzVj\\niQlXpTLYnee6Q5R+ixlwDows5dFkjrWONmuz527WC3cXAqZm2bg=\\n-----END RSA PRIVATE KEY-----'"})
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
