# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from django.core.management import call_command

def load_fixture(file_name, orm):
    original_get_model = models.get_model
    
    def get_model_southern_style(*args):
        try:
            return orm['.'.join(args)]
        except:
            return original_get_model(*args)
    
    models.get_model = get_model_southern_style
    
    call_command('loaddata', file_name)
    
    models.get_model = original_get_model


class Migration(DataMigration):

    def forwards(self, orm):
        load_fixture("initial_data.json", orm)

    def backwards(self, orm):
        pass

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
            'health_check': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'iops': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'default': "''", 'max_length': '15', 'blank': 'True'}),
            'lbr_region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'nodes'", 'to': u"orm['api.LBRRegionNodeSet']"}),
            'nid': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'security_group': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'storage': ('django.db.models.fields.IntegerField', [], {}),
            'tinc_private_key': ('django.db.models.fields.TextField', [], {'default': "'-----BEGIN RSA PRIVATE KEY-----\\nMIIEpAIBAAKCAQEAs5vs5XkzVrUxZDS1CoDo2kD+8FMdb8W+1AAFer0F2sUY4Z1K\\no4/MugndAa/a/aP4KqKjHoZiPvXxx9j/uYkE4e8c3uw09IFI90bWq61Hh0j3GqLV\\nnQtw2670ra/csjmOirXjFHkS2FAAG+/qTKoLm08qBI8vnapG/YIFcg3F96pd0837\\njbsor3l7go/Bio3siOulWj53PCyjoHfJIeXPur3UEKvHj8HUj5dar+O5fG3OH+7U\\n2uEI8FrFpt+JiV0Z4kzXXRFcfuRlQSIT1dpVoJHYDF7z/dnl+iHgDsj5EeYuUM3g\\n+lSf8WtYuDCj0z7DinjyNwLLsvyY2hv8IB9rgwIDAQABAoIBAQCxLlGtMjomAEsA\\nKkqqWO7cV5/nXma8m5ubsYW2RgAfh63661r1LWdt40sFXgCvlHC9RoGaHEGRELh6\\nSKRE2FlbtLGLbAL1bRCY92XQJ/lXCPDTcu09pkqoPNic+s7BdqwaREIGMUYY5Bqn\\ndK5zAJDAnoC5zLLRW2f6r6hFkjbIELrvAFwKZzjHJEBM3wlsC3KacvCBkPBzKQso\\nUvsrXPjrYr3Nxr3lSKu0M7fMHZtVxEaBmCqacz/aQJkz3T8FqpDXQPnCMrhe9zqN\\nbjNi7NEj/8Ry7Hj/Qy3fEWiAOKQKm8v9rg57dil1/Bz6W2aPxbNuVgzEPuS5IBAD\\n0JmrI6DJAoGBALuOEaqjKsFu2+nnMp83Et719hpytY1MIVl2YBoITOBjQ3Dcvvpg\\n1rUN4JoqcBnhmSxjyMMuDUfJ1vmBaVB0kpnCmzb/p8FYE5GhLCm/yJvFFXc3M779\\nLqJi19XKMTJ3vvLjqVCGKW3jsmUnPxyFbM4QYBEdCLOY3DG5BlU60jVlAoGBAPUn\\nh5miL+6RCY9+8YwaEbXAdUqUqPe7op39g28aAjcD5clLVzRZiujoFjydncHPtdP4\\n85f7g+3jrUkeBxLzDkn2o+LaFiD/2IGn7rhmLHIp0kdYXdcfY0iebGyQyAUfCMSC\\nkZYvdwpUPy6ktHdKSXt4RxvQp/Yy50V75PgdVqLHAoGAR9w5HJ4DxbVKASaaGLKr\\nQk4PCzckJI0kwfg+/fpsKhUeQ+HwMlJkMV6tzaOw69mqLH3W8CF26SiGe3Z/+VmQ\\nyeTsP3hYuBWc+dE88IoQvM4YWWMHKogrFAC3HayoiOOkf7+GodmlifsR4PvWjID6\\nnUFc7XGoYdeRlmOD76fn3pkCgYEAh4h7JyzLYxE8P+DmmZYwBFOKhNj7MTrDBKWL\\nbHjskI3PFCJa6841Rd5JrOlWtjenRrFzuqqKnZIp0yqOrqNBWxLIODpp0YSgpc25\\n5KhYGiWU42yvNKddtGAhgUPp0Sr/JeUpp+ZF4agB5j+Ypfqj9WbhqTcKJMqvoXKF\\ne8Z8hzECgYA/YMhGwmc1j0e9xYXbWE5Y4in912GAhcPYPLSPA/d7rreADirIQxG7\\nJ6/IwvBR4tvSc6OOUifCeW/lWbmlhteqEHTo066EvGVMUsBPqArhF3neeYfpzFUc\\n2ZkUZPigCp3oU7OGXsTtfyQjph+s5QWvCr4w2MBjueL/IbSHeVIxww==\\n-----END RSA PRIVATE KEY-----'"})
        },
        u'api.provider': {
            'Meta': {'object_name': 'Provider'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
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
    symmetrical = True
