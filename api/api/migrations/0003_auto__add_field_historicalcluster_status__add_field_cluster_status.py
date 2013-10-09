# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'HistoricalCluster.status'
        db.add_column(u'api_historicalcluster', 'status',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Cluster.status'
        db.add_column(u'api_cluster', 'status',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'HistoricalCluster.status'
        db.delete_column(u'api_historicalcluster', 'status')

        # Deleting field 'Cluster.status'
        db.delete_column(u'api_cluster', 'status')


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
            'tinc_private_key': ('django.db.models.fields.TextField', [], {'default': "'-----BEGIN RSA PRIVATE KEY-----\\nMIIEowIBAAKCAQEAwwghvuF4fEOJ5x1GdiDTUKl6b8xVQkGaBHWI6LWrO1FiiSjw\\nGvyMmLnLJYITmtbhFaYKOlURHseKzOfnDQ+UReb62IunmligV2bw/LjF5mJg2vr8\\nZNr8HWZZXUK3JkF4MhNP2Mzq89TnojFW6kmadqYvna6+vQRwQEu6+0YRrX5veiJA\\nbkNBnggwjbEerDG8fsIzMK3URNP+6UMk47nIzQCzy4BUPBimRiA9rTR+FHWvS1Mt\\n6yoNKdxCAmhW6IvrYHxZXGKlY/nnUnu4iK3tKq5upW6R5ftkVRmrsLliN7RNqXZk\\nIFhYUPyBpyLGDJ6K+GeY/kG2bbAIrh4X3hJ41QIDAQABAoIBAQClvW1gF6AaihLR\\nUzGkBbVO4Rfplk4GJlXK4E9e47QGjt0cDqwtYt3glFOtJmOevGk/yoD6nXwVGiI8\\ni/7wPIMW/HnEOLpQEm0AmbzGKAgWBxikP5Lp6qdCHM5o0N9wJUcN1xeN+Gbam93V\\nGfTw2Wfo2MWyTORPIUx7d2AJVbyEIGY5PCkQayUzC0q6oiKwkPF468ToFpOxjHFR\\nuALYLn946BV8U6+HHolRiACQTeps+Q5fgsXmuUINRgVNE45f1PdX7yhHPbt5RHbV\\nMdLYyZLcqF8wy80VjVjX/ZNlKIcP+fUGW/ZzAZ2fA1dyBQNVLIIIBAODyIdRRBh4\\n/dijThLpAoGBAPqUvRTWdGI+fm+oE4go0LissPe8540z+5AzyWSIq8f6L/Fq8g5l\\nxDk9out1rHFD/x8kByQtmniMDWLzvtmPumWMKfbMR+mvEMLM0B2w1mxFpl3iyQmp\\nAx4QDSWq7Dn/jJPqQCydH31oQvFImpWOiVRFdfLFSicjtMVfYiRFzI3PAoGBAMc/\\n3NXbBupW9WyM+MlZBzBmA+TTj0kYzlf5QAjZ/JovdM7lchi9zWVR4Y/rZrjEWVm3\\n9qMOU3ad77vl2Zl/vroIZfvUCpPjBgbinAW6d8u8CwRj6EGVQh7qygq7EjSU7Vqi\\nPWSXTwalnGIJ/X8JlF3xIDSNB0i27nejifrHTTwbAoGAV94yU41D8HNjmLnCZ5uQ\\nXUHJKIYoWB5jV1ShiUxXmF9F0o0i5iOPZFcVuyVfW7RxULUsf+Yx5ZWO2CUKxnWc\\n8iDtUiqeCPanlPeG/vJUrlDaHs/4mReYDUGpqoy+GzReUjvxVvOd6DbYSo2gD1OV\\nGmTlEEVYVFMz/4YL/xYuvYcCgYBMXkbnVNbWtNPGclXc3pmpzEAL0aamrrJP98G6\\nYsq10iCkOD8+CmmSPwsEXYZ2pRNWFvOaVaBZ43kCfLulYNgad6OXHROc0TP7KZoB\\nfBH0bbOPUDeyA2JfdUBRUphMvRQoW+zKBFCOzKUe0pNtwJ80Tno4iiFTloHaKz10\\neDU7JwKBgGA/WC+5Tm5Hwe9S8oPc8DhVgPa6O9Y8zusdHlxmlIxhMISM4CRyJF4M\\nAcJ1G08HIa9nriHtVcNvPme5ZzIdp/P9uZPbrTLkmNFH9TN9yQUciWuhegIOtkcc\\nNOKynsOsAYblaC0yM9ZL3MHELbttJHkyTG1srPmDqRI3I9VxkOCL\\n-----END RSA PRIVATE KEY-----\\n'"})
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
            'tinc_private_key': ('django.db.models.fields.TextField', [], {'default': "'-----BEGIN RSA PRIVATE KEY-----\\nMIIEpQIBAAKCAQEAtw9FTsRxcNftTICKAVKIOcLX4pr1PkIwYEYq/51/Qu9oSewz\\nHun8v1iFb4bIbonneceMKYQSU2MUQv4y2OcEPNElxLuQYV8XWHvGoVd+9FeO97vC\\nKlbDxWH7aSetSJWYHCRJg57nH19Vto97AfKpDIHdvN8ZELgWWuDbdVH85z7kd2wD\\nvilUGKJvAt08XMM7+3VaKa4agFU/XDva5jZQH4lq8bz0AxpxxA1RpT7gBLW9JBNd\\nRSazMLMTcatYYyVxCezBhPGTiM+CAsgkGG2Q7nlvII0XIggHeSwGZctBlRF7PLbH\\nQIR/J3c8Atf1og9Pyi/xqOAMXWz6zpua5p9JOQIDAQABAoIBAGfNRvW1OsZMCok4\\n0giR7iEitRwP1kSpb5kH8NXlTwZ7jt1sDEjZUbKG1ZM6EGlt1U4eswHPnDygkBq0\\n3cxUoviBeDMoUGSGcUyBU06luJ2BENa1JxKvBG/mcZNdJktkWE6M3Qq/jjsh6g6N\\nKakfGnC3Ky8wKpxqZnK90nOiPBA7iESbCOvKxtWya502ZThQ49oC2cWW+INnfX3/\\nM7ordqu37NWYyf2fSpTGkKFh7cUdSSaaw9J+vVALWVTklC34xmxdVDA5nGOg6xq7\\nQhTgzIIykPuTe+1K2bL8HGaIhHWrUlkQef19najLp94c6uqB75ggyQg/kt8s1B0C\\noPry1aECgYEA858WhoF64gCEQJt9KT4gZIdEsj8waBDmtv74dtOUoosko7xs++fx\\nIXIHrf/BonkFTN9jYAYuEv8pA1qJZX+ZlF0Kztf8oJZbj58XBgXjTYG4UoQevOly\\n7dNuHkvO+Zao756yhsjcFBGIe/p8w5jTihnrwlAfRUJp1X9zQqIx0TUCgYEAwFxs\\nfLUyB8ic7OTuAfY2TRuN8el3Yt4Xve9QW4HrCZr2IIuB0a2C1rEpYdhrvCronxXG\\njcp+AdfX11pXBrJ22Tyjjz8Rmh1qfYtzhsDHO6zMcUlkCVd3XInUc23XxxqVvEph\\npG/x9/Gz1TlbgVfpN3Z7GBjOsviuR/l74MARfHUCgYEAhMk8lNm0KcUQUMqvYLBt\\nJX4ZMnKApug3aJz2voW6aRIgSWKloHQemRU3HF7fovgFrI3B84/Kwy3yo9JQO1Ne\\nWWCRSIavOrRZeaHEAdNpvlArMEa1HlC8BOcOCVNWn/G/aMP+GLsYQZQA6VpxcIc3\\nHfnc58+WC8EUQHs0TqhrMNUCgYEAilAqhYT341bhVwjJBkoWA12Ds+UOPd25ro1r\\n91A0QyTUQtRs1OpxAJREUCGAXb1wpCrRKNTnw8WCYkuH9b3O7SbH6FEOBAWQs5LY\\nz5S/7O2z1uVRc9IbdkN4qkLZ+0TnU4scKFOB5ak6iF+Epz0h6QpdOhdkUJW1IvWF\\nmDYinJ0CgYEA8DqngjrUqF3Pzkots8v34PCgksVblLZz9HM8b4u3TiJQVvfCuvUW\\n5nii5UnDfHhaun6aDAAm5HS04GAR/gzH4AyWnDJ7iafQw+5USp/NXPalaLIvHpfz\\naD9qRRLiuHO6q5YDD1gZumSbOCvoVkeNWq/ducn6T91VHDSWw+RoQZI=\\n-----END RSA PRIVATE KEY-----\\n'"})
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