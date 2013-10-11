"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from .models import User, Node, Cluster, Region, Flavor
class ClusterTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@example.com')

    def test_create(self):
        """
        Tests cluster creation.
        """
        cluster = Cluster.objects.create(user=self.user)

class NodeTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@example.com')
        self.cluster = Cluster.objects.create(user=self.user)

    def test_create(self):
        """
        Tests node creation.
        """
        node = Node.objects.create(
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
from hashlib import sha1
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
