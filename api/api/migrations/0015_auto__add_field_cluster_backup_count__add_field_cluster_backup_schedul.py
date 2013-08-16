# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Cluster.backup_count'
        db.add_column(u'api_cluster', 'backup_count',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=24),
                      keep_default=False)

        # Adding field 'Cluster.backup_schedule'
        db.add_column(u'api_cluster', 'backup_schedule',
                      self.gf('django.db.models.fields.CharField')(default='3 */2 * * *', max_length=255),
                      keep_default=False)

        # Adding field 'Cluster.iam_arn'
        db.add_column(u'api_cluster', 'iam_arn',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True),
                      keep_default=False)

        # Adding field 'Cluster.iam_key'
        db.add_column(u'api_cluster', 'iam_key',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True),
                      keep_default=False)

        # Adding field 'Cluster.iam_secret'
        db.add_column(u'api_cluster', 'iam_secret',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Cluster.backup_count'
        db.delete_column(u'api_cluster', 'backup_count')

        # Deleting field 'Cluster.backup_schedule'
        db.delete_column(u'api_cluster', 'backup_schedule')

        # Deleting field 'Cluster.iam_arn'
        db.delete_column(u'api_cluster', 'iam_arn')

        # Deleting field 'Cluster.iam_key'
        db.delete_column(u'api_cluster', 'iam_key')

        # Deleting field 'Cluster.iam_secret'
        db.delete_column(u'api_cluster', 'iam_secret')


    models = {
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
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
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
            'tinc_private_key': ('django.db.models.fields.TextField', [], {'default': "'-----BEGIN RSA PRIVATE KEY-----\\nMIIEogIBAAKCAQEAniXJj/j7Ft9DAgLps9JDvEa8hXLHkb+uwiWt6xc5uWTOU8mJ\\n7bJjo4BULCUHdy9pyVVJPZOmUwqWgMUySy5LdkxtR6LSfhms8eDqypWc9huIbknL\\nEeObEq9jeFBKQuHQ6mGoOvzqxhwOsRBZPSTf1lYSECMukkgxEBeKf6P6xCMDRuhQ\\n+v443h2VPHPVYYvP6I7lREbcNZFG67mPQjj+Unlyv6iAmq+9+jU4QqD819XU+qY6\\noiEsFLa3Tx3UwMswkUbgC0IE1Lgzu5RDtTn/IChCPJrRzB4yNLP1VVzJqqi1jO62\\nP4E5qWKrukiw0hSf3eorWhF3NZwJ+s7LKPVoaQIDAQABAoIBAC9VQfmsXIJg+i48\\n7vOaKBnO1hfe3apaw5RqMJ6fSfCaIkLjnDufW8EQ5KB9yLk8YJ4Yv54Fdg9+qMML\\nwlzME1vpzf9V1UhWqPOQDNXrZ5olbXUM8xF8nOo/wja9WSyhZ6Tu66oUDrSSqzcF\\nnJ/3TGNbSXa5APRZVQ3q7dH8I07Wb1XtLGk8KPie+704Fah5WHhteMYqBs7VrWrX\\nhZQP2mI1wWwfmog1twUVV0fkC1XIJWlFgEMX8MWxrA0ICSMXOsYMPzu/SWhNvSrZ\\nSBzGwuPOjfwwzRdgg6fcLPMr87Og/DBIt4OsnimA9353gybC8PW713EhDNqROrKQ\\n22iTMj0CgYEAwSfDDp9ms+tNQfFOFYo+m0XbJSZlF/jtzLviV6pUOm/hv/LnkjyR\\n0aiTpWOrLD3ItgudY9gLA+5BXqj7HXkTsWoPTTTT53Gv+LWa/tvnwNp7XMfzyihO\\n8ooYd1x7aO/LpRU7PXC+33EA5NEGGM+w0xNupMBePtgjpDLP1bu3cmMCgYEA0Zos\\nQ2jbhtFTLB/HzuUVaYxYnG0lCHHG4cs6wOJ9JUXLD1JVK+tyDGNtprFXhslHA3tF\\nbc+ACxOr/sGEFsmVuMwAcQWd2qyc9NAlAQ9eOog3w6FUYr+McGG+mjXlbOYvRsUv\\n/xLb2071elV7HFG2y+GwsbjY0i3OXNSsq8XgzcMCgYAHSSCqZIjTMITxf9CaL2S9\\nJp1lgVU+2jzeBBg9hkc3DRFO1DK36WD2r40iJ+hE+u+fLkD5iySfOVVt5KHUMsTz\\nZDS/jMaRbFBe6Tq3ckQDmjoc/c3MSkjwDRVvKyXch27/AxYA80e/1dtaxiect/jL\\nfWgm/rqPVEfD4cbFIReCUQKBgDzwZBodLGYgCdx0SPVgKT+MrF6eZPv1iGsxWR2n\\nO9dQWV9VAqpIQ9pSNhkWymnHrzvV5TOt9n5B8+mXfb3aUgtuVFqH1YM0WFXdBkUu\\noKjH3d6k0xH6uuwZnv7a2J82tVwQDIpOg1lZtYkhvS9YmprgPS0OnwtMggj/VEyE\\ntX1dAoGAWv7n8CpTUim/KT3v0fmKsdsygwyQeqMADFRQvGB2R28ESY4Q4h8n5hZQ\\n34gZexYYCofoqImeDqog+8dwZIhZZa1axvRR+8fS/LhWp0qSlK+HtqvRjpyqn8BE\\nChxJYkvUOzs2SeCbYfC9Hu1+uabE0y+uaR8nbTY03AohiqqQOFI=\\n-----END RSA PRIVATE KEY-----'"})
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