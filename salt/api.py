# -*- coding: utf-8 -*-
'''
Generate pillar data from DBaaS API

:maintainer: David Newgas <dnewgas@geniedb.com>
:maturity: new


Configuring the dbaas_api ext_pillar
=====================================

.. code-block:: yaml

    ext_pillar:
      - api:
          pillar_name: my_application
          env: /srv/dbaas/env/
          project_path: /srv/dbaas/api/
          env_file: /path/to/env/file.sh
          settings_module: dbaas_api.settings
          django_app: api

This would return pillar data that would look like

.. code-block:: yaml

    dbaas_api:
        cluster-nid:
          field: value


Module Documentation
====================
'''

import logging
import os
import sys
import re


HAS_VIRTUALENV = False

try:
    import virtualenv
    HAS_VIRTUALENV = True
except ImportError:
    pass

log = logging.getLogger(__name__)


def __virtual__():
    if not HAS_VIRTUALENV:
        log.warn('virtualenv not installed, please install first')
        return False
    return 'api'

def node_dict(node):
    return dict((field, getattr(node, field)) for field in
        ('id','nid','dns_name', 'buffer_pool_size', 'tinc_private_key', 'public_key', 'set_backup_url', 'status'))

def cluster_dict(cluster):
    ret = dict((field, getattr(cluster, field)) for field in
               ('uuid','port','dbname', 'dbusername', 'dbpassword','ca_cert', 'server_cert', 'server_key', 'subscriptions', 'backup_count', 'backup_schedule', 'iam_key','iam_secret'))
    ret['nodes'] = [node_dict(node) for node in cluster.nodes.all()]
    ret['backup_parts'] = cluster.backup_schedule.split()
    ret['dbname_parts'] = cluster.dbname.split(',')
    return ret

def ext_pillar(minion_id,
               pillar,
               pillar_name,
               env,
               project_path,
               settings_module,
               django_app,
               env_file=None,
               *args,
               **kwargs):
    '''
    Connect to a Django database through the ORM and retrieve model fields

    Parameters:
        * `pillar_name`: The name of the pillar to be returned
        * `env`: The full path to the virtualenv for your Django project
        * `project_path`: The full path to your Django project (the directory
          manage.py is in.)
        * `settings_module`: The settings module for your project. This can be
          found in your manage.py file.
        * `django_app`: The name of your app.
        * `env_file`: A bash file that sets up your environment. The file is
          run in a subprocess and the changed variables are then added.
    '''

    if not os.path.isdir(project_path):
        log.error('Django project dir: \'{}\' not a directory!'.format(env))
        return {}
    for path in virtualenv.path_locations(env):
        if not os.path.isdir(path):
            log.error('Virtualenv {} not a directory!'.format(path))
            return {}

    # load the virtualenv
    sys.path[0:0]=(virtualenv.path_locations(env)[1] + '/site-packages/',)
    # load the django project
    sys.path.append(project_path)

    os.environ['DJANGO_SETTINGS_MODULE'] = settings_module

    if env_file is not None:
        import subprocess

        base_env = {}
        proc = subprocess.Popen(['bash', '-c', 'env'], stdout=subprocess.PIPE)
        for line in proc.stdout:
            (key, _, value) = line.partition('=')
            base_env[key] = value

        command = ['bash', '-c', 'source {0} && env'.format(env_file)]
        proc = subprocess.Popen(command, stdout=subprocess.PIPE)

        for line in proc.stdout:
            (key, _, value) = line.partition('=')
            # only add a key if it is different or doesn't already exist
            if key not in base_env or base_env[key] != value:
                os.environ[key] = value.rstrip('\n')
                log.debug('Adding {} = {} to Django environment'.format(
                            key,
                            value.rstrip('\n')))

    try:
        import importlib

        models = importlib.import_module(django_app + '.models')
        from django.conf import settings
        from django.db.transaction import commit_on_success
        r = re.match(settings.CLUSTER_NID_TEMPLATE, __grains__['id'])
        with commit_on_success():
            node = models.Node.objects.get(cluster_id=r.group('cluster'), nid=r.group('nid'))
            return {pillar_name: {
                'node': node_dict(node),
                'cluster': cluster_dict(node.cluster),
                'settings': {
                    'BUCKET_NAME': models.BUCKET_NAME,
                    'zabbix_server':settings.ZABBIX_SERVER,
            }}}
    except ImportError, e:
        log.error('Failed to import library: {}'.format(e.message))
        return {}
    except Exception, e:
        log.error('Failed on Error: {}'.format(e.message))
        return {}
