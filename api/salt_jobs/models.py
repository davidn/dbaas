from __future__ import unicode_literals
from django.db import models
from salt.client import LocalClient
from .exceptions import check_highstate_error

def send_salt_cmd(ids, cmd, timeout=20):
        client = LocalClient()
        return client.cmd_async(ids, cmd, expr_form='list')

def get_salt_result(**kwargs):
    return SaltReturn.objects.filter(**kwargs)

def get_highstate_result(**kwargs):
    return check_highstate_error(SaltReturn.objects.get(**kwargs))

class MediumText(models.TextField):
    def db_type(self, connection):
        if connection.settings_dict['ENGINE'] == 'django.db.backends.mysql':
            return 'mediumtext'
        else:
            return super(MediumText, self).db_type(connection)

class SaltJob(models.Model):
    jid = models.CharField(max_length=255, primary_key=True)
    load = MediumText()
    class Meta:
        db_table = 'jids'

class SaltReturn(models.Model):
    pk = models.AutoField(primary_key=True)
    fun = models.CharField(max_length=50, db_index=True)
    jid = models.CharField(max_length=255, db_index=True)
    s_return = MediumText(db_column='return')
    id = models.CharField(max_length=255, db_index=True)
    sucess = models.CharField(max_length=10)
    full_ret = MediumText()
    class Meta:
        db_table = 'salt_returns'
        get_latest_by = 'pk'