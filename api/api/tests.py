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

from api.models import User, Node, Cluster, Region, Flavor
class ClusterTest(TestCase):
    fixtures = ['initial_data']
    def setUp(self):
        self.user = User.objects.create(email='test@example.com')

    def test_create(self):
        """
        Tests cluster creation.
        """
        Cluster.objects.create(user=self.user)

    @patch('api.models.dbaas_resources.connect_iam', new_callable=connect_iam)
    @patch('api.models.dbaas_resources.ZabbixAPI')
    def test_launch(self, ZabbixAPI, connect_iam):

        cluster = Cluster.objects.create(user=self.user)
        cluster.launch_sync()
        self.assertEqual(Cluster.PROVISIONING, cluster.status)

        cluster.launch_async_iam()
        connect_iam.assert_called_once_with(aws_access_key_id=settings.AWS_ACCESS_KEY, aws_secret_access_key=settings.AWS_SECRET_KEY)
        connect_iam.return_value.create_user.assert_called_once_with(cluster.uuid)
        self.assertEqual(connect_iam.return_value.put_user_policy.call_count, 1)
        connect_iam.return_value.create_access_key.assert_called_once_with(cluster.uuid)
        self.assertEqual('NEW_ARN', cluster.iam_arn)
        self.assertEqual('NEW_AKI', cluster.iam_key)
        self.assertEqual('NEW_SAK', cluster.iam_secret)
        self.assertEqual(Cluster.PROVISIONING, cluster.status)

        cluster.launch_async_zabbix()
        ZabbixAPI.assert_called_once_with(settings.ZABBIX_ENDPOINT)
        ZabbixAPI.return_value.login.called_once_with(settings.ZABBIX_USER, settings.ZABBIX_PASSWORD)
        ZabbixAPI.return_value.hostgroup.create.called_once_with(name=self.user.email)
        self.assertEqual(Cluster.PROVISIONING, cluster.status)

        cluster.launch_complete()
        self.assertEqual(Cluster.RUNNING, cluster.status)

    @patch('api.models.dbaas_resources.connect_iam', new_callable=connect_iam)
    def test_launch_setpolicy_failure(self, connect_iam):
        connect_iam.return_value.put_user_policy.side_effect = Exception("Fail once")

        cluster = Cluster.objects.create(user=self.user)
        cluster.launch_sync()
        with self.assertRaises(Exception):
            cluster.launch_async()

    def test_launch_complete(self):
        cluster = Cluster.objects.create(user=self.user)
        cluster.launch_complete()
        self.assertEqual(Cluster.RUNNING, cluster.status)

    @patch('api.models.dbaas_resources.connect_iam', new_callable=connect_iam)
    def test_terminate(self, connect_iam):
        cluster = Cluster.objects.create(user=self.user)
        cluster.iam_arn = 'NEW_ARN'
        cluster.iam_key = 'NEW_AKI'
        cluster.iam_secret = 'NEW_SAK'
        cluster.on_terminate()

        connect_iam.assert_called_once_with(aws_access_key_id=settings.AWS_ACCESS_KEY, aws_secret_access_key=settings.AWS_SECRET_KEY)
        connect_iam.return_value.delete_access_key.assert_called_once_with('NEW_AKI', cluster.uuid)
        connect_iam.return_value.delete_user_policy.assert_called_once_with(cluster.uuid, cluster.uuid)
        connect_iam.return_value.delete_user.assert_called_once_with(cluster.uuid)
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
@patch('api.models.dbaas_resources.ZabbixAPI')
@patch('api.models.cloud_resources.providers.test')
@patch('api.models.dbaas_resources.connect_iam', new_callable=connect_iam)
class LaunchClusterControllerTest(TestCase):
    fixtures = ['initial_data']
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
        self.cluster.pk = cluster.pk
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
    def test_no_exceptions(self, connect_iam, Cloud, ZabbixAPI):
        ZabbixAPI.return_code.item.get.return_code=True
        for node in self.nodes:
            node.pending = lambda: Cloud.launch.called
        launch_cluster(self.cluster)
        self.assertCallCounts()

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=False)
    def test_retry_on_pending(self, connect_iam, Cloud, ZabbixAPI):
        ZabbixAPI.return_code.item.get.return_code=True
        for node in self.nodes:
            # 30 * 15s = 7m30s
            node.pending = MagicMock(side_effect=chain(repeat(True,30),repeat(False)))
        launch_cluster(self.cluster)
        self.assertCallCounts(node_update=31)

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=False)
    def test_retry_on_iam_error(self, connect_iam, Cloud, ZabbixAPI):
        errors = (BotoClientError(""), S3CreateError(400,""), S3PermissionsError(400,""), S3ResponseError(400,""))
        ZabbixAPI.return_code.item.get.return_code=True
        for node in self.nodes:
            node.pending = lambda: Cloud.launch.called
        connect_iam.return_value.create_user.side_effect=errors+(connect_iam.return_value.create_user.return_value,)
        launch_cluster(self.cluster)
        self.assertCallCounts(cluster=len(errors)+1)

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=False)
    def test_retry_on_s3_error(self, connect_iam, Cloud, ZabbixAPI):
        errors = (BotoClientError(""), BotoServerError(400,""),)
        ZabbixAPI.return_code.item.get.return_code=True
        for node in self.nodes:
            node.pending = lambda: Cloud.launch.called
        launch_cluster(self.cluster)
        self.assertCallCounts(cluster=len(errors)+1)

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=False)
    def test_retry_on_setup_dns_error(self, connect_iam, Cloud, ZabbixAPI):
        ZabbixAPI.return_code.item.get.return_code=True
        for node in self.nodes:
            node.pending = lambda: Cloud.launch.called
            node.setup_dns = MagicMock(side_effect=(DNSServerError(400,"whatever"),True))
        launch_cluster(self.cluster)
        self.assertCallCounts(node_dns=2)

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=False)
    def test_launch_error(self, connect_iam, Cloud, ZabbixAPI):
        ZabbixAPI.return_code.item.get.return_code=True
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
    def test_constant_iam_error(self, connect_iam, Cloud, ZabbixAPI):
        ZabbixAPI.return_code.item.get.return_code=True
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
    def test_constant_dns_error(self, connect_iam, Cloud, ZabbixAPI):
        ZabbixAPI.return_code.item.get.return_code=True
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

class NodeTest(TestCase):
    fixtures = ['initial_data']
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

from api.models import Rule
@patch('api.models.rules.rules.actions')
@patch('api.models.rules.rules.conditions')
class RuleTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@email.com')
        self.rule = Rule.objects.create(condition='test_condition', action='test_action')

    def test_condition_true(self, conditions, actions):
        conditions.test_condition.return_value = True
        Rule.process()
        conditions.test_condition.assert_called_with(self.user)
        actions.test_action.assert_called_with(self.user)

    def test_condition_false(self, conditions, actions):
        conditions.test_condition.return_value = False
        Rule.process()
        conditions.test_condition.assert_called_with(self.user)
        self.assertFalse(actions.test_action.called)

    def test_repeat_true(self, conditions, actions):
        conditions.test_condition.return_value = True
        Rule.process()
        conditions.reset_mock()
        actions.reset_mock()
        Rule.process()
        self.assertFalse(conditions.test_condition.called)
        self.assertFalse(actions.test_action.called)

    def test_repeat_false(self, conditions, actions):
        conditions.test_condition.return_value = False
        Rule.process()
        conditions.reset_mock()
        actions.reset_mock()
        Rule.process()
        conditions.test_condition.assert_called_with(self.user)
        self.assertFalse(actions.test_action.called)

    def test_multi_user(self, conditions, actions):
        conditions.test_condition.side_effect = (True, False, True)
        user2 = User.objects.create(email='test2@email.com')
        Rule.process()
        self.assertEqual(conditions.test_condition.call_count, 2)
        self.assertEqual(actions.test_action.call_count, 1)
        conditions.reset_mock()
        actions.reset_mock()
        Rule.process()
        conditions.test_condition.assert_called_with(user2)
        actions.test_action.assert_called_with(user2)

    def test_multi_rule(self, conditions, actions):
        self.rule = Rule.objects.create(condition='test_condition2', action='test_action2')
        conditions.test_condition.return_value = True
        conditions.test_condition2.side_effect = (False, True)
        Rule.process()
        conditions.test_condition.assert_called_with(self.user)
        actions.test_action.assert_called_with(self.user)
        conditions.test_condition2.assert_called_with(self.user)
        self.assertFalse(actions.test_action2.called)
        conditions.reset_mock()
        actions.reset_mock()
        Rule.process()
        self.assertFalse(conditions.test_action.called)
        self.assertFalse(actions.test_action.called)
        conditions.test_condition2.assert_called_with(self.user)
        actions.test_action2.assert_called_with(self.user)

import datetime
class ConditionsTest(TestCase):
    from rules import conditions

    def setUp(self):
        self.user = User.objects.create(email='test@email.com')
        self.user2 = User.objects.create(email='test2@email.com')

    def test_user_launched(self):
        self.assertFalse(self.conditions.user_launched(self.user))
        c = Cluster.objects.create(user=self.user)
        self.assertFalse(self.conditions.user_launched(self.user))
        Cluster.objects.create(user=self.user2, status=Cluster.PROVISIONING)
        self.assertFalse(self.conditions.user_launched(self.user))
        c.status = Cluster.PROVISIONING
        c.save()
        self.assertTrue(self.conditions.user_launched(self.user))
        c.status = Cluster.RUNNING
        c.save()
        self.assertTrue(self.conditions.user_launched(self.user))
        c.status = Cluster.OVER
        c.save()
        self.assertTrue(self.conditions.user_launched(self.user))
        c.delete()
        self.assertTrue(self.conditions.user_launched(self.user))

    def test_user_not_launched_after_2days(self, paid=False):
        self.assertFalse(self.conditions.user_not_launched_after_2days(self.user))
        c = Cluster.objects.create(user=self.user)
        self.assertFalse(self.conditions.user_not_launched_after_2days(self.user))
        c.status = Cluster.PROVISIONING
        c.save()
        self.assertFalse(self.conditions.user_not_launched_after_2days(self.user))
        c.delete()
        self.assertFalse(self.conditions.user_not_launched_after_2days(self.user))
        self.user.date_joined -= datetime.timedelta(days=2)
        self.assertFalse(self.conditions.user_not_launched_after_2days(self.user))

        self.assertFalse(self.conditions.user_not_launched_after_2days(self.user2))
        self.user2.date_joined -= datetime.timedelta(days=2)
        self.assertEqual(self.conditions.user_not_launched_after_2days(self.user2), not paid)
        c2 = Cluster.objects.create(user=self.user2)
        self.assertEqual(self.conditions.user_not_launched_after_2days(self.user2), not paid)
        c2.status = Cluster.PROVISIONING
        c2.save()
        self.assertFalse(self.conditions.user_not_launched_after_2days(self.user2))

    def test_paid_user_not_launched_after_2days(self):
        self.user.is_paid = True
        self.user.save()
        self.user2.is_paid = True
        self.user2.save()
        self.test_user_not_launched_after_2days(True)

    @override_settings(TRIAL_LENGTH=datetime.timedelta(days=1))
    def test_user_expired(self):
        self.assertFalse(self.conditions.user_expired(self.user))
        c = Cluster.objects.create(user=self.user)
        self.assertFalse(self.conditions.user_expired(self.user))
        c.status = Cluster.PROVISIONING
        c.save()
        self.assertFalse(self.conditions.user_expired(self.user))
        h = c.history.all().update(history_date=datetime.datetime.utcnow() - datetime.timedelta(days=2))
        self.assertTrue(self.conditions.user_expired(self.user))
        c.status = Cluster.OVER
        c.save()
        self.assertTrue(self.conditions.user_expired(self.user))
        c.delete()
        self.assertTrue(self.conditions.user_expired(self.user))


class ActionsTest(TestCase):
    from rules import actions
    import django.core.mail as mail

    def setUp(self):
        self.user = User.objects.create(email='test@email.com')
        self.user2 = User.objects.create(email='test2@email.com')

    def test_disable_user(self):
        self.user.is_active = True
        self.user.save()
        self.actions.disable_user(self.user)
        self.assertFalse(User.objects.get(pk=self.user.pk).is_active)

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_no_cluster_email_2days(self):
        self.actions.no_cluster_email_2days(self.user)
        self.assertEquals(len(self.mail.outbox), 1)
        self.assertSequenceEqual(self.mail.outbox[0].to, (self.user.email,))