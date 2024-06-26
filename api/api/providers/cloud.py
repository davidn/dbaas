#!/usr/bin/python
from __future__ import unicode_literals
from logging import getLogger
from textwrap import dedent
from django.conf import settings
from django.db import connection

logger = getLogger(__name__)


class Cloud(object):
    def __init__(self, region):
        self.region = region

    def launch(self, node):
        pass

    def pending(self, node):
        return False

    def shutting_down(self, node):
        return False

    def get_ip(self, node):
        return "192.0.2.%d" % node.nid

    def update(self, node, tags={}):
        pass

    def terminate(self, node):
        pass

    def reinstantiate_setup(self, node):
        pass

    def reinstantiate(self, node):
        # Note: this command can be re-tried
        pass

    def reinstantiation_complete(self, node):
        # Allow for any clean up now that the reinstantiation is complete
        pass

    @staticmethod
    def cloud_init(node):
        return dedent("""\
            #!/bin/sh
            cat >>/etc/salt/minion <<END
            master: {salt_master}
            id: {dns_name}
            mysql.host: '{salt_master}'
            mysql.port: 3306
            mysql.user: '{salt_minion_sql_user}'
            mysql.pass: '{salt_minion_sql_pass}'
            mysql.db: '{mysql_db}'
            startup_states: highstate
            ext_job_cache: mysql
            END
            """.format(
            dns_name=node.dns_name,
            salt_master=settings.SALT_MASTER,
            mysql_db=getattr(settings, 'SALT_MINION_SQL_DB', connection.settings_dict['NAME']),
            salt_minion_sql_user=getattr(settings, 'SALT_MINION_SQL_USER', connection.settings_dict['USER']),
            salt_minion_sql_pass=getattr(settings, 'SALT_MINION_SQL_PASSWORD', connection.settings_dict['PASSWORD'])))
