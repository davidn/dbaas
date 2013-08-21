# -*- coding: utf-8 -*-
import datetime
import re
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        for cluster in orm.Cluster.objects.all():
            cluster.dbusername = cluster.user.username
            try:
                n = cluster.nodes.all()[0]
                cluster.port = n.port
                m = re.search(r"CREATE DATABASE (\w*);",n.mysql_setup)
                if m:
                    cluster.dbname = m.group(1)
                m = re.search(r"CREATE USER '(\w*)'@'%' IDENTIFIED BY '(\w*)';",n.mysql_setup)
                if m:
                    cluster.dbusername, cluster.dbpassword = m.group(1,2)
            except:
                pass
            cluster.save()

    def backwards(self, orm):
        for node in orm.Node.objects.all():
            node.port = node.cluster.port
            node.mysql_setup = """CREATE DATABASE {dbname};
CREATE USER '{dbusername}'@'%' IDENTIFIED BY '{dbpassword}';
GRANT ALL ON {dbname}.* to '{dbusername}'@'%';""".format(
                dbname = node.cluster.dbname,
                dbusername = node.cluster.dbusername,
                dbpassword = node.cluster.dbpassword,
            )
            node.save()

    models = {
        u'api.cluster': {
            'Meta': {'object_name': 'Cluster'},
            'dbname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'dbpassword': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'dbusername': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'port': ('django.db.models.fields.PositiveIntegerField', [], {'default': '3306'}),
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
            'tinc_private_key': ('django.db.models.fields.TextField', [], {'default': "'-----BEGIN RSA PRIVATE KEY-----\\nMIIEowIBAAKCAQEA1qAL7ouie71rLYkVyCHA9XoaDhAVGNMxWdBIytQ9ZDSaz92y\\nsW7mIVGLYCOLsH2YRKkA9+L3X6rbkjM/Qn0gjyYkeZd0YFEBu68A9g4k7ojTpUnU\\nJLOXA6yX/6hDKt+fH6RLtF3SvPJzKmnex3GcqEYOBv6ov2K8+GmSpOHtAOgFGdgu\\nnoG3Op70lSmlMOAL/2hTyYws9kho7XqY5y8+CwTh0acE3il6az8BVflFgIHqy1ik\\nPfSL5hjx/+W2159LruFId/b35INlGOT9gGB8GdElyimOVBXf7rDRnOizcZDMH8bV\\ndR07EVYw6YE3LdnstC2yCv3ADGMZwDzNovb3+wIDAQABAoIBAH5jF0OtZMybef8B\\nqBsHjXrBIZDAdbv9uiUam5Mdst1MgRIBitYj6U8blwjRRdRz0XQ1VcWkGWpz0gNh\\nPFJqHv9NRdN4leaWLYAZiWZcY/E4D/JY7J2ESFy4iXXa31ri/vCCLraTPaNY3urO\\nF4u5YrhRMLd7xWGWwpNCkEGabZfG9eo5DzLoNCzj3VXvlsc0tJS4lbxTt8GV/UM4\\nmCmMipLzXCzJlDoWl0FaOMKIsnqNzLwA/oTa3O8vn1z1AFdbLfLQAPlTD1GED/7D\\ncX/t/jz84vbu2xUNZdCp+EOUIBJ7nFgc1gez0gI/6ZiCynidCV6wPRRHQEIMObaQ\\nFITD7XkCgYEA4tiuP+u5TKpZKaCnS/Caa2dO24Aa4jm4yoSC1e4kEYUs5P/Xg2qw\\n/Crtz6I0xZiQ/Z99G8M8IFfvy6wyQjF0nMQK5GCLsM7LdBzdBUAI3Yb41kPc5QdF\\n9RQdOMu7AuRXKIsKUO7ETzy3zuJgUd1Ptg5Uc41bzlrVeXjBka/hhL8CgYEA8jVI\\nnzzrU7D0a5bOqr4rWPVADYtBYq//yhNpgDACZa+CELSPKYxkrwve9EkuJFTOMUOD\\niCzczHfIZ9cqHFLvVum8lQX61PYU528EVu0k0EwSuw1ScFjPBdTGGNEYpqusmjJZ\\nhV0Yfl3t2DYGB+lPBj8MQzeF1BmuE/IqNtRjb8UCgYEAs0GekIxppReH1clJ6kx6\\n+hxsyC93DwWl7QLBkOPaRK4ESAGUABkzOlGCEu2O3gYtrP13E5U30icrKrssC/qg\\nt7CDGuzf9huz0lFsplVvq/6YbFi8GY+hzITUgqkbYrGl3jfhMws6vZKxfR6OFqLX\\n9nlkatttjKdiwdaWv9VIVGkCgYA/3rEx3JypyyYJIRGKkO9ZXALyD2DEp2iqXwgZ\\nF4/qRKflw9dku3LpfhXjEVErn3loIEeVJ09qU8PzLhgas/wNTUG/gn4snl/Qz8Oz\\nMIHes9DUpqSwn5qoDP3YGXuIqAix+MkGlBAbcqV/uG9Kssl1+jY/m2qdDdCLzfY3\\n0zYNiQKBgEMoqRUR8MMbSuK5an0Gi2attp41Aerg8HJd8BqPCthlKmAJqeJsiCKC\\nA29296UVoq47ER/aCx19MCjMx1s8Fo8NhysfmjagghaHB3LaQ4/gEf+xwdB19aSJ\\nFP67e6/QSik0T+tUacuZIQ0FhQN35YR5T+M8LF59ypND3JR9UGbL\\n-----END RSA PRIVATE KEY-----'"})
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
    symmetrical = True
