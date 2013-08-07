# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Provider.enabled'
        db.add_column(u'api_provider', 'enabled',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Provider.enabled'
        db.delete_column(u'api_provider', 'enabled')


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
            'lbr_region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'nodes'", 'to': u"orm['api.LBRRegionNodeSet']"}),
            'nid': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'nodes'", 'to': u"orm['api.Region']"}),
            'security_group': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'storage': ('django.db.models.fields.IntegerField', [], {}),
            'tinc_private_key': ('django.db.models.fields.TextField', [], {'default': "'-----BEGIN RSA PRIVATE KEY-----\\nMIIEpAIBAAKCAQEAqKjHqGeX78JY7msDZXAAx05lGfqxmMnqSwmv5o4xrYZtN75D\\n9W7yIRcDu5YyIhuRGx8jsZU2B2jt5eFx8w5AMLnJlVP04xTvQb/XPWirBjTNJ4Xp\\nOBwyyHnUgGm3TnAnbc8mUpUqOipPGD6lV95ltU8fHKF1exspz5JAaDzGXSTPyc7t\\nchtZbxUecubkStUSNF5nA8WmSZSa66JwZOLvU/5oAPBC+Rdi9ycJoXogrOXNBXKI\\nD1OnlhqtTJ7aZvqFgOJhFZ9glfn98yD0oau13bxhyar/gMAmzFXrJtGe+la3up4Q\\nTHQ6EPR6vFdOQck6PToCybJttWqb81dYlrhCAQIDAQABAoIBAQCRy91UkcDA7SNN\\nbsqvzIOPxxAUxibyKlHT7hrV1kPRemw9jMdYikDbI/cBGRRbcbMdW+zSHWdoPmew\\nmhOUBdStil1dLgd6qeUt1DWviySUp95U9SinbZDkxpRRMZHZR5B+F11MdE/dmidn\\nkPgDnmgTtMLzUAurkM6y9f2hXjAn4TwCkRqJTu90gIyjfKQ1p9Hj6eY0HzyYCIvB\\nyfCqvYzVFXhZFpAht4gLrYvI/wrGew8p3js2JaOLiQHmOKd7Y+huEkV6wGAgGdgu\\niRAvP71YrA5D7OaVp635UoPKSjVGj8bIVL04gZYMCW28xmfNEYNMfoIhZfPkjXIS\\nHUZktJFxAoGBAMdSOF3Quk5n7bnouDXKyqDDZD9szB2pktBP1oBAAEu9yIHzldss\\nUWLpVQibMWI1Iirjpfs6Eq25Y3crS2oSSA4b0vZi9PWru9udxhiZWRYHLmjCl/fv\\ndt3J2feeDjMoFyebEA8Z0fpmBXvCrJAB90kbWuatd509ahg4U8zmXaxNAoGBANie\\nf5r77rO4Lg1+xEoTDHleToOwx31uTy4me4i79roKwaXNX2y/JFWdhcQsO7jYGrqk\\nWRrmgKRTgsGIPNeIuV8wH+O9wDUhf3pxSwy5mihloSjbyeHpDpj213pR62HgZ78e\\nHYo0bJBIny2UocMHKamZxcZiv6+8vVBJZKapS7aFAoGARXYizJbsBlzznME8SQrF\\n+KZ/LhdFPuUUk+Hu17z2HW8jDB6OT9Yu+rBkAN7Mo/PuV1IESvve/InJ3wLIgkui\\nrsAFkfXEdkUF77AZFAOE50dTZhDCkxXxr7Mjcca0HiHPh+7i9tBBu+iH6qxaJMl6\\nmxCcah1zvOllKtGeap6xcFUCgYEAu9zx4/Kb+OdBoViQWYGdruB4DUPSLtjs+KRN\\nPK9u8bgEa4vqN0Cp/UpIyXJnNQ7OV5HS6T6A0ILQgpFp2q7rvT7aWUOmHy33BbSd\\nluKcbG5/TxUWR8M8crKY+69yCQd6UkiG6+Y9RQCGdBxUEfTzT/BZkozvmzR/ptKP\\n5O4sCJUCgYAcJ6rYAez38Ntj8Q+sd7PzwHbcw9cawb+8U36oppf78BEF7GPGaXlM\\nb4IQ59yR9PDxqFQQmzJfB1Lg7Z/BTg0rdSvT8k05/zvoEHUmGGUb2lkTra0Q4Ukl\\nutuOIJJBmQFjXrpDKg9EzR9bzAhbb4dRnVFqf75sFfe4M2fpmnw5Iw==\\n-----END RSA PRIVATE KEY-----'"})
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
            'lbr_region': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
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