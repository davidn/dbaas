#!/usr/bin/python
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from __future__ import unicode_literals
from django.test import TestCase
from mock import MagicMock, patch, call
from django.conf import settings
from textwrap import dedent
from itertools import chain, repeat
from boto.exception import S3CreateError, S3PermissionsError, BotoClientError,\
    S3ResponseError, BotoServerError
from boto.route53.exception import DNSServerError
from django.test.utils import override_settings

def connect_iam():
    connect_iam = MagicMock()
    connect_iam.return_value.create_user.return_value = \
        {'create_user_response':{'create_user_result':{'user':{'arn':'NEW_ARN'}}}}
    connect_iam.return_value.create_access_key.return_value = \
        {'create_access_key_response':{'create_access_key_result':{'access_key':{
            'access_key_id':'NEW_AKI',
            'secret_access_key':'NEW_SAK'}}}}
    return connect_iam

def connect_s3(empty=True):
    connect_s3 = MagicMock()
    if empty:
        connect_s3.return_value.lookup.return_value = None
    else:
        connect_s3.return_value.lookup.return_value.__iter__ = lambda _: iter(('a','b','c'))
    connect_s3.return_value.create_bucket.return_value.set_policy.return_value = True
    return connect_s3

from api.models import User, Node, Cluster, Region, Flavor
class ClusterTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@example.com')

    def test_create(self):
        """
        Tests cluster creation.
        """
        Cluster.objects.create(user=self.user)

    @patch('api.models.connect_iam', new_callable=connect_iam)
    @patch('api.models.connect_s3', new_callable=connect_s3)
    def test_launch(self, connect_s3, connect_iam):

        cluster = Cluster.objects.create(user=self.user)
        cluster.launch_sync()
        self.assertEqual(Cluster.PROVISIONING, cluster.status)

        cluster.launch_async()
        connect_iam.assert_called_once_with(aws_access_key_id=settings.AWS_ACCESS_KEY, aws_secret_access_key=settings.AWS_SECRET_KEY)
        connect_iam.return_value.create_user.assert_called_once_with(cluster.uuid)
        connect_iam.return_value.create_access_key.assert_called_once_with(cluster.uuid)
        connect_s3.assert_called_once_with(aws_access_key_id=settings.AWS_ACCESS_KEY, aws_secret_access_key=settings.AWS_SECRET_KEY)
        connect_s3.return_value.lookup.assert_called_once_with(cluster.uuid)
        self.assertEqual(connect_s3.return_value.create_bucket.return_value.set_policy.call_count,1)
        self.assertEqual('NEW_ARN', cluster.iam_arn)
        self.assertEqual('NEW_AKI', cluster.iam_key)
        self.assertEqual('NEW_SAK', cluster.iam_secret)
        self.assertEqual(Cluster.PROVISIONING, cluster.status)

    @patch('api.models.connect_iam', new_callable=connect_iam)
    @patch('api.models.connect_s3', new_callable=connect_s3)
    def test_launch_setpolicy_failure(self, connect_s3, connect_iam):
        connect_s3.return_value.create_bucket.return_value.set_policy.side_effect = Exception("Fail once")

        cluster = Cluster.objects.create(user=self.user)
        cluster.launch_sync()
        with self.assertRaises(Exception):
            cluster.launch_async()

    def test_launch_complete(self):
        cluster = Cluster.objects.create(user=self.user)
        cluster.launch_complete()
        self.assertEqual(Cluster.RUNNING, cluster.status)

    @patch('api.models.connect_iam', new_callable=connect_iam)
    @patch('api.models.connect_s3', new_callable=lambda: connect_s3(False))
    def test_terminate(self, connect_s3, connect_iam):
        cluster = Cluster.objects.create(user=self.user)
        cluster.iam_arn = 'NEW_ARN'
        cluster.iam_key = 'NEW_AKI'
        cluster.iam_secret = 'NEW_SAK'
        cluster.terminate()

        connect_iam.assert_called_once_with(aws_access_key_id=settings.AWS_ACCESS_KEY, aws_secret_access_key=settings.AWS_SECRET_KEY)
        connect_iam.return_value.delete_access_key.assert_called_once_with('NEW_AKI', cluster.uuid)
        connect_iam.return_value.delete_user.assert_called_once_with(cluster.uuid)
        connect_s3.assert_called_once_with(aws_access_key_id=settings.AWS_ACCESS_KEY, aws_secret_access_key=settings.AWS_SECRET_KEY)
        connect_s3.return_value.lookup.assert_called_once_with(cluster.uuid)
        connect_s3.return_value.lookup.return_value.delete_keys.assert_called_once_with(['a','b','c'])
        self.assertEqual(Cluster.OVER, cluster.status)

    def test_next_nid(self):
        cluster = Cluster.objects.create(user=self.user)
        nodes = [Node.objects.create(
            cluster=cluster,
            storage=10,
            region=Region.objects.get(code='test-1'),
            flavor=Flavor.objects.get(code='test-small')) for _ in xrange(4)]
        nodes[0].nid = cluster.next_nid()
        nodes[0].save()
        nodes[1].nid = cluster.next_nid()
        nodes[1].save()
        nodes[2].nid = 5 # test skips
        nodes[2].save()
        nodes[3].nid = cluster.next_nid()
        self.assertEqual(nodes[0].nid, 1)
        self.assertEqual(nodes[1].nid, 2)
        self.assertEqual(nodes[2].nid, 5)
        self.assertEqual(nodes[3].nid, 6)

from controller import launch_cluster
@patch('api.models.ZabbixAPI')
@patch('api.tasks.ZabbixAPI')
@patch('api.models.Cloud')
@patch('api.models.connect_iam', new_callable=connect_iam)
@patch('api.models.connect_s3', new_callable=connect_s3)
class LaunchClusterControllerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@example.com')
        cluster = Cluster.objects.create(user=self.user,
                                              dbname='db',
                                              dbusername='user',
                                              dbpassword='dbpass')
        self.nodes = [Node.objects.create(
            cluster=cluster,
            storage=10,
            region=Region.objects.get(code='test-1'),
            flavor=Flavor.objects.get(code='test-small')) for _ in xrange(3)]
        for node in self.nodes:
            node.launch_sync = MagicMock(wraps=node.launch_sync)
            node.launch_async_provision = MagicMock(wraps=node.launch_async_provision)
            node.launch_async_update = MagicMock(wraps=node.launch_async_update)
            node.launch_async_dns = MagicMock(wraps=node.launch_async_dns)
            node.launch_async_zabbix = MagicMock(wraps=node.launch_async_zabbix)
            node.launch_complete = MagicMock(wraps=node.launch_complete)
        self.cluster = MagicMock(wraps=cluster)
        def get_status(self):
            return cluster.status
        def set_status(self,status):
            cluster.status = status
        type(self.cluster).status = property(get_status, set_status)
        self.cluster.uuid = cluster.uuid
        self.cluster.nodes.all.return_value = self.nodes
        self.cluster.nodes.filter.return_value = self.nodes
    
    def assertCallCounts(self, node_update=1, node_dns=1, cluster=1):
        self.assertEquals(1, self.cluster.launch_sync.call_count)
        self.assertEquals(cluster, self.cluster.launch_async.call_count)
        self.assertEquals(1, self.cluster.launch_complete.call_count)
        self.assertItemsEqual([1,2,3], [node.nid for node in self.cluster.nodes.all()])
        for node in self.nodes:
            self.assertEquals(1, node.launch_sync.call_count)
            self.assertEquals(1, node.launch_async_provision.call_count)
            self.assertEquals(node_update, node.launch_async_update.call_count)
            self.assertEquals(node_dns, node.launch_async_dns.call_count)
            self.assertEquals(1, node.launch_async_zabbix.call_count)
            self.assertEquals(1, node.launch_complete.call_count)

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=False)
    def test_no_exceptions(self, connect_s3, connect_iam, Cloud, ZabbixAPI, ZabbixAPI2):
        ZabbixAPI.return_code.item.get.return_code=True
        ZabbixAPI2.return_code.item.get.return_code=True
        for node in self.nodes:
            node.pending = lambda: Cloud.launch.called
        launch_cluster(self.cluster)
        self.assertCallCounts()

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=False)
    def test_retry_on_pending(self, connect_s3, connect_iam, Cloud, ZabbixAPI, ZabbixAPI2):
        ZabbixAPI.return_code.item.get.return_code=True
        ZabbixAPI2.return_code.item.get.return_code=True
        for node in self.nodes:
            # 30 * 15s = 7m30s
            node.pending = MagicMock(side_effect=chain(repeat(True,30),repeat(False)))
        launch_cluster(self.cluster)
        self.assertCallCounts(node_update=31)

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=False)
    def test_retry_on_iam_error(self, connect_s3, connect_iam, Cloud, ZabbixAPI, ZabbixAPI2):
        errors = (BotoClientError(""), S3CreateError(400,""), S3PermissionsError(400,""), S3ResponseError(400,""))
        ZabbixAPI.return_code.item.get.return_code=True
        ZabbixAPI2.return_code.item.get.return_code=True
        for node in self.nodes:
            node.pending = lambda: Cloud.launch.called
        connect_iam.return_value.create_user.side_effect=errors+(connect_iam.return_value.create_user.return_value,)
        launch_cluster(self.cluster)
        self.assertCallCounts(cluster=len(errors)+1)

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=False)
    def test_retry_on_s3_error(self, connect_s3, connect_iam, Cloud, ZabbixAPI, ZabbixAPI2):
        errors = (BotoClientError(""), BotoServerError(400,""),)
        ZabbixAPI.return_code.item.get.return_code=True
        ZabbixAPI2.return_code.item.get.return_code=True
        for node in self.nodes:
            node.pending = lambda: Cloud.launch.called
        connect_s3.return_value.lookup.side_effect=errors+(connect_s3.return_value.lookup.return_value,)
        launch_cluster(self.cluster)
        self.assertCallCounts(cluster=len(errors)+1)

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=False)
    def test_retry_on_setup_dns_error(self, connect_s3, connect_iam, Cloud, ZabbixAPI, ZabbixAPI2):
        ZabbixAPI.return_code.item.get.return_code=True
        ZabbixAPI2.return_code.item.get.return_code=True
        for node in self.nodes:
            node.pending = lambda: Cloud.launch.called
            node.setup_dns = MagicMock(side_effect=(DNSServerError(400,"whatever"),True))
        launch_cluster(self.cluster)
        self.assertCallCounts(node_dns=2)

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=False)
    def test_launch_error(self, connect_s3, connect_iam, Cloud, ZabbixAPI, ZabbixAPI2):
        ZabbixAPI.return_code.item.get.return_code=True
        ZabbixAPI2.return_code.item.get.return_code=True
        for node in self.nodes:
            node.pending = lambda: False
            node.region.connection.launch = MagicMock(side_effect=Exception("whatever"))
        with self.assertRaisesMessage(Exception, "whatever"):
            launch_cluster(self.cluster)
        self.assertEqual(Cluster.objects.get(uuid=self.cluster.uuid).status, Cluster.ERROR)
        for node in self.nodes:
            self.assertEqual(node.region.connection.launch.call_count, 3)
            self.assertEqual(node.launch_async_update.call_count, 0)
            self.assertEqual(Node.objects.get(pk=node.pk).status, Node.ERROR)

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=False)
    def test_constant_iam_error(self, connect_s3, connect_iam, Cloud, ZabbixAPI, ZabbixAPI2):
        ZabbixAPI.return_code.item.get.return_code=True
        ZabbixAPI2.return_code.item.get.return_code=True
        for node in self.nodes:
            node.pending = lambda: Cloud.launch.called
        connect_iam.return_value.create_user.side_effect = BotoClientError("whatever")
        with self.assertRaisesMessage(BotoClientError, "whatever"):
            launch_cluster(self.cluster)
        self.assertEqual(Cluster.objects.get(uuid=self.cluster.uuid).status, Cluster.ERROR)
        self.assertGreater(self.cluster.launch_async.call_count, 1)
        for node in self.nodes:
            self.assertEqual(node.launch_async_provision.call_count, 0)
            self.assertEqual(node.launch_async_update.call_count, 0)

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=False)
    def test_constant_dns_error(self, connect_s3, connect_iam, Cloud, ZabbixAPI, ZabbixAPI2):
        ZabbixAPI.return_code.item.get.return_code=True
        ZabbixAPI2.return_code.item.get.return_code=True
        for node in self.nodes:
            node.pending = lambda: Cloud.launch.called
            node.setup_dns = MagicMock(side_effect=DNSServerError(400,"whatever"))
        with self.assertRaisesMessage(DNSServerError, "whatever"):
            launch_cluster(self.cluster)
        self.assertEqual(Cluster.objects.get(uuid=self.cluster.uuid).status, Cluster.ERROR)
        self.assertEqual(self.cluster.launch_async.call_count, 1)
        for node in self.nodes:
            self.assertEqual(node.launch_async_provision.call_count, 1)
            self.assertEqual(node.launch_async_update.call_count, 1)
            self.assertGreater(node.launch_async_dns.call_count, 1)
            self.assertEqual(Node.objects.get(pk=node.pk).status, Node.ERROR)

from controller import add_database
class AddDatabaseControllerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@example.com')
        self.cluster = Cluster.objects.create(user=self.user,
                                              dbname='db',
                                              dbusername='user',
                                              dbpassword='dbpass')
        self.nodes = [Node.objects.create(
            cluster=self.cluster,
            storage=10,
            region=Region.objects.get(code='test-1'),
            flavor=Flavor.objects.get(code='test-small')) for _ in xrange(3)]

    @patch('MySQLdb.connect')
    def test_add_database(self, connect):
        self.nodes[0].status = Node.PROVISIONING
        self.nodes[0].nid = self.cluster.next_nid()
        self.nodes[0].save()
        self.nodes[1].nid = self.cluster.next_nid()
        self.nodes[1].status = Node.RUNNING
        self.nodes[1].save()
        self.nodes[2].nid = self.cluster.next_nid()
        self.nodes[2].status = Node.RUNNING
        self.nodes[2].save()
        add_database(self.cluster, 'db2')
        self.assertItemsEqual(
            [call(host=self.nodes[1].dns_name,
                  user=settings.MYSQL_USER,
                  passwd=settings.MYSQL_PASSWORD,
                  port=self.cluster.port),
             call(host=self.nodes[2].dns_name,
                  user=settings.MYSQL_USER,
                  passwd=settings.MYSQL_PASSWORD,
                  port=self.cluster.port)],
            connect.call_args_list)
        self.assertItemsEqual(
            [call("CREATE DATABASE IF NOT EXISTS db2;"),
             call("CREATE DATABASE IF NOT EXISTS db2;"),
             call("GRANT ALL ON db2.* to %s@'%%';",('user',)),
             call("GRANT ALL ON db2.* to %s@'%%';",('user',))],
            connect.return_value.cursor.return_value.execute.call_args_list
        )

import yaml
from hashlib import sha1
class NodeTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@example.com')
        self.cluster = Cluster.objects.create(user=self.user)

    def test_create(self):
        """
        Tests node creation.
        """
        Node.objects.create(
            cluster=self.cluster,
            storage=10,
            region=Region.objects.get(code='test-1'),
            flavor=Flavor.objects.get(code='test-small')
        )

    def test_cloud_config(self):
        self.cluster.uuid='15bbb7df-8d4b-49f4-9210-418bb80235e5'
        self.cluster.ca_cert = 'CA_CERT'
        self.cluster.server_cert = 'SERVER_CERT'
        self.cluster.server_key = 'SERVER_KEY'
        node = Node.objects.create(
            cluster=self.cluster,
            storage=10,
            region=Region.objects.get(code='test-1'),
            flavor=Flavor.objects.get(code='test-small')
        )
        node.tinc_private_key = "-----BEGIN RSA PRIVATE KEY-----\nMIIEowIBAAKCAQEA34jp0sVa9rX0/aqJEjeQy1Z0Kd8WGtN81MxHlXGN86zBqlQU\n11qTE+TzSVR0YwzJANLAATwVFpknUuiIH04ad5Fc754rLAnQz8SobJWH4S0lLF72\nvmk9j3AsdaC7GcO3mTYc0s/F8eLLBahTq0glHQfKOqMG3LnTgoeNPxGbRDDqH7aI\nN6rJCTYk/d5MbAiu+F1ZxwJPpcjT9AhTSpv5P2iFXOVe1DzvxqMFMjrN65duJdGw\nwabep9Sa02oX063bvulCircrhuNfS2aJZ2tyIcQl0ZowHDHipx00INq7efKi2n0y\npJbnXr9zTwoFcaO4J9mW1c7U5fADyAtswFuyPQIDAQABAoIBAA/nlvN3NVSud6MA\n2kXgjD3bheJgzBrWh2BAtKsubDI1TYZH+z+jYymcNa83Ahz2EOstE5pC4yE7fm/I\nub64eOue/STTdTDp9eCClpU7QnLEGowAqb+8jzPAgHlSGV3o7gxJrF1XiTb/swBR\nDLr4JCPfpQTtCpTz59e2u1cMcqa0TjAjfbd2AaavT0WGHOoodycpQwPuRXUZrWi0\nypvWnsCsw7wJGMpEOup+SmkC3PpTb1I323DXKLKb76vTJxZh7x2E89EAwjMANzIf\n1FKsJ9Hx+BaNRgWUA7LlvDB2u79PaXlzk1OD9kGzj56uKvI1fiDL8dmtgpU6mBX2\nsbwfqgECgYEA+qKfj6KM2rBuWwCXdR/6dYb0+IKg8cVbPnyoOWnXqgfqq2VzCP+j\nyDPBeTE5xFm+46WMVTcM6LLasmQ3aXK1/tD7+H+zSidRJxkbZR0BQ07XiAJQYGBi\nZIzUMrDjS6TkpQUsgtrcW4XSLn4jBg72t/L1xXxPkshaGawR1lKUHb0CgYEA5FHK\ngLzhQpStxMhxCQWY/sZs7U6hhhkh9U0XV0beaNbIqHUfY/mLh3/t2Y+60g4eEGwA\nwD7ATngLE4tRC7wZ+9A43lTFAil4vCh3CZTjYCx6bAqdnNlmV+WcqzumnK7x8waA\nyqEWL/Z5IxgQk9658FMUwNhoIYTl8RsbzpoP7oECgYAPnWAZf8QMv98wNjo5ZtOg\nzNaoQOMsDOKhYvzMDucLxdB9+yUOk3atu2O7XDDAJeM5pY+3o2Vfff0YDhxRqn7i\nMDzyf2o5HXf12p+VThhNDDVrWNGPH5Iht5Bk1BZlGRHRoh/iyyXdYdn1YZBnCTmf\nvjhHpHYErAzI+qpl0uE9dQKBgEPh4YBHJ/4gsE1qftj81hEhs68WisWQ4VzKT98+\nDdBD06LqN6wEvKxLp87ggd4EHoIpaku+HHT4Eer8p9sCUQNiVBYeQ/ixldjzevjZ\nUIT+lGNdAKFqrZgCh4MNmCrLhNoJm+8i17Lo5/k8JWmhdczzFp+Dd+pHVgpKUgkq\nGwSBAoGBAObzpgXyXyOM+A8mmoJwMG4st2Hov2EMzyF737QT+vGRwf3kElj4JRiQ\ncrG3Bn4qOURCEzeHHhewYZNFsODaw0sWBO/fkINuBq/MHNWQESt9tFSeaSaf07vW\ndSgc64TgukO28KabJEgjVJd0C89MjxndouR50emloKyGN6Fsl7KS\n-----END RSA PRIVATE KEY-----"
        node.save()
        yml = yaml.load(node.cloud_config)
        with open('test_cc.json') as test_cc:
            comp = yaml.load(test_cc.read())
        for key in comp.keys():
            self.assertItemsEqual(yml[key], comp[key])
        self.assertEqual(len(comp), len(yml))

    def test_cloud_config_multi_db(self):
        self.cluster.dbname = "first_database,second_database"
        self.cluster.dbusername = "dbuser"
        self.cluster.dbpassword = "dbpw"
        node = Node.objects.create(
            cluster=self.cluster,
            storage=10,
            region=Region.objects.get(code='test-1'),
            flavor=Flavor.objects.get(code='test-small')
        )
        yml = yaml.load(node.cloud_config)
        for f in yml['write_files']:
            if f['path'] == '/etc/mysqld-grants':
                self.assertMultiLineEqual(f['content'], dedent("""\
                    CREATE USER 'dbuser'@'%' IDENTIFIED BY PASSWORD '*5D8437CCDC45A2E565B0561CBB441CF1371202C8';
                    CREATE USER '{mysql_user}'@'%' IDENTIFIED BY PASSWORD '{mysql_password}';
                    GRANT ALL ON *.* to '{mysql_user}'@'%' WITH GRANT OPTION;
                    CREATE DATABASE first_database;
                    GRANT ALL ON first_database.* to 'dbuser'@'%';
                    CREATE DATABASE second_database;
                    GRANT ALL ON second_database.* to 'dbuser'@'%';
                    """).format(mysql_user=settings.MYSQL_USER, mysql_password='*' + sha1(sha1(settings.MYSQL_PASSWORD).digest()).hexdigest().upper()))
                break
        else:
            raise self.failureException('/etc/mysqld-grants not found in cloud_config')

from api.crypto import KeyPair
from Crypto.PublicKey.RSA import importKey, generate
from Crypto import Random
class KeyPairTest(TestCase):
    def test_generate(self):
        kp = KeyPair()
        self.assertNotEqual(kp.private_key, kp.public_key)
        priv = importKey(kp.private_key)
        self.assertTrue(priv.has_private)
        self.assertGreaterEqual(priv.size(), 1024)

    def test_import(self):
        key = generate(2048, Random.new().read)
        kp= KeyPair(key.exportKey(pkcs=1))
        self.assertEqual(kp.private_key.strip(), key.exportKey(pkcs=1))
        kp= KeyPair(key.exportKey(pkcs=8))
        self.assertEqual(kp.private_key.strip(), key.exportKey(pkcs=1))

    def test_private(self):
        kp = KeyPair()
        self.assertTrue(kp.private_key.strip().startswith('-----BEGIN RSA PRIVATE KEY-----'))
        self.assertTrue(kp.private_key.strip().endswith('-----END RSA PRIVATE KEY-----'))
        priv8 = importKey(kp.private_key)
        self.assertTrue(priv8.has_private())

    def test_public(self):
        kp = KeyPair()
        self.assertTrue(kp.public_key.strip().startswith('-----BEGIN PUBLIC KEY-----'))
        self.assertTrue(kp.public_key.strip().endswith('-----END PUBLIC KEY-----'))
        pub8 = importKey(kp.public_key)
        self.assertFalse(pub8.has_private())

from api.crypto import CertificateAuthority
from OpenSSL.crypto import load_certificate, FILETYPE_PEM, X509Extension
class CertificateAuthorityTest(TestCase):
    def test_X509(self):
        cert = load_certificate(FILETYPE_PEM, CertificateAuthority().certificate)
        self.assertEqual(cert.get_version(), 0x2)
        self.assertEqual(cert.get_issuer(), cert.get_subject())
        self.assertFalse(cert.has_expired())
        extensions = dict((cert.get_extension(i).get_short_name(), cert.get_extension(i).get_data()) for i in range(cert.get_extension_count()))
        self.assertEqual(len(extensions), cert.get_extension_count(), 'An X509v3 extension appeared twice.')
        self.assertEqual(extensions["basicConstraints"], X509Extension("basicConstraints", False, "CA:TRUE").get_data())
        self.assertEqual(extensions["keyUsage"], X509Extension("keyUsage", False, "keyCertSign").get_data())
        self.assertEqual(extensions["subjectKeyIdentifier"], X509Extension("subjectKeyIdentifier", False, 'hash', subject=cert).get_data())
        self.assertEqual(extensions["authorityKeyIdentifier"], X509Extension("authorityKeyIdentifier", False, "keyid:always", issuer=cert).get_data())
        # test sig?

from api.crypto import SslPair
class SslPairTest(TestCase):
    def setUp(self):
        self.ca = CertificateAuthority()

    def runTest(self):
        cert = load_certificate(FILETYPE_PEM, SslPair(self.ca).certificate)
        ca = load_certificate(FILETYPE_PEM, self.ca.certificate)
        self.assertEqual(cert.get_subject(), ca.get_subject())
        self.assertFalse(cert.has_expired())
        extensions = dict((cert.get_extension(i).get_short_name(), cert.get_extension(i).get_data()) for i in range(cert.get_extension_count()))
        if extensions.has_key('basicConstraints'):
            self.assertEqual(extensions["basicConstraints"], X509Extension("basicConstraints", False, "CA:FALSE").get_data())
        # test sig?

from api.utils import cron_validator
from django.core.exceptions import ValidationError
class CronValidatorTest(TestCase):
    valid = (
        "* * * * *",
        "* * *\t* *",
        "* *  * * *",
        "* * *\t  * *",
        "* * * 1 *",
        "* 0,2,4,6,8,10,12,14,16,18,20,22 * * *",
        "0 0 1 1 0",
        "59 23 31 12 7",
        "* * * jan fri",
        "* * * Feb Sat",
        "* * * MAR WED",
    )
    invalid = (
        "* * * *",
        "* * * * * *",
        "-1 * * * * *",
        "* -1 * * *",
        "* * 0 * *",
        "* * * 0 *",
        "* * * * -1",
        "60 * * * *",
        "* 24 * * *",
        "* * 32 * *",
        "* * * 13 *",
        "* * * * 8",
        "* * *\r* *",
        "*\n* * * *",
        "a * * * *",
        "* b * * *",
        "* * c * *",
        "* * * d *",
        "* * * * e",
        "* * * * sam",
    )
    def test_valid(self):
        for i in self.valid:
            cron_validator(i)
    def test_invalid(self):
        for i in self.invalid:
            try:
                with self.assertRaises(ValidationError):
                    cron_validator(i)
            except AssertionError, e:
                e.args += (i,)
                raise

from api.utils import mysql_database_validator
class MysqlDatabaseValidatorTest(TestCase):
    valid = (
        "db",
        "db_asdf",
        "d0023432",
        "324d3242",
        "234d",
        "a$",
        "a$",
        "_a",
        "a234567890123456789012345678901234567890123456789012345678901234",
    )
    invalid = (
        "a b",
        "a,b",
        "a.b",
        "a/b",
        "a\\b",
        "a-b",
        "",
        "\n",
        "\r",
        "(",
        "_",
        "321",
        "$",
        'CREATE',
        'create',
        "a2345678901234567890123456789012345678901234567890123456789012345",
)
    def test_valid(self):
        for i in self.valid:
            mysql_database_validator(i)
    def test_invalid(self):
        for i in self.invalid:
            try:
                with self.assertRaises(ValidationError):
                    mysql_database_validator(i)
            except AssertionError, e:
                e.args += (i,)
                raise

from api.utils import split_every
class SplitEveryTest(TestCase):
    def test_divisable(self):
        self.assertListEqual(
            list(split_every(2, (1,2,3,4))),
            [[1,2],[3,4]])
    def test_remainder(self):
        self.assertListEqual(
            list(split_every(2, (1,2,3,4,5))),
            [[1,2],[3,4],[5]])
    def test_empty(self):
        self.assertListEqual(
            list(split_every(2, ())),
            [])
    def test_generator(self):
        self.assertListEqual(
            list(split_every(2, xrange(4))),
            [[0,1],[2,3]])
    def test_read_out_of_order(self):
        se = split_every(2, (1,2,3,4))
        first = se.next()
        second = se.next()
        self.assertListEqual([3,4], second)
        self.assertListEqual([1,2], first)
        self.assertRaises(StopIteration, se.next)

from api.utils import retry
class RetryTest(TestCase):
    def setUp(self):
        self.retry_func = MagicMock(name='retry_func')
        self.retry_func.return_value=1
    def test_success(self):
        self.assertEqual(self.retry_func.return_value,
            retry(self.retry_func, initialDelay=1, maxRetries=3)
        )
        self.assertEqual(1, len(self.retry_func.mock_calls))
    def test_fail(self):
        self.retry_func.side_effect=Exception('asdf')
        with self.assertRaisesRegexp(Exception, 'asdf'):
            self.assertEqual(self.retry_func.return_value,
                retry(self.retry_func, initialDelay=1, maxRetries=3)
            )
        self.assertEqual(3, len(self.retry_func.mock_calls))
    def test_fail_once(self):
        self.retry_func.side_effect=(Exception(),1)
        self.assertEqual(self.retry_func.return_value,
            retry(self.retry_func, initialDelay=1, maxRetries=3)
        )
        self.assertEqual(2, len(self.retry_func.mock_calls))
