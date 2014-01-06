from __future__ import unicode_literals
import yaml
from django.db import models
from south.modelsinspector import add_introspection_rules
from salt.client import LocalClient
from .exceptions import check_highstate_error

def send_salt_cmd(ids, cmd, **kwargs):
        client = LocalClient()
        return client.cmd_async(ids, cmd, expr_form='list', **kwargs)

def get_salt_result(**kwargs):
    return SaltReturn.objects.filter(**kwargs)

def get_highstate_result(**kwargs):
    return check_highstate_error(yaml.load(SaltReturn.objects.get(**kwargs).full_ret)['return'])

class MediumText(models.TextField):
    def db_type(self, connection):
        if connection.settings_dict['ENGINE'] == 'django.db.backends.mysql':
            return 'mediumtext'
        else:
            return super(MediumText, self).db_type(connection)
add_introspection_rules([], ["^salt_jobs.models.MediumText"])

class SaltJob(models.Model):
    jid = models.CharField(max_length=255, primary_key=True)
    load = MediumText()
    class Meta:
        db_table = 'jids'

class SaltReturn(models.Model):
    prim = models.AutoField(primary_key=True)
    fun = models.CharField(max_length=50, db_index=True)
    jid = models.CharField(max_length=255, db_index=True)
    s_return = MediumText(db_column='return')
    id = models.CharField(max_length=255, db_index=True)
    success = models.CharField(max_length=10)
    full_ret = MediumText()
    class Meta:
        db_table = 'salt_returns'
        get_latest_by = 'pk'
