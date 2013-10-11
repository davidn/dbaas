import datetime
import OpenSSL
from Crypto.PublicKey import RSA

class KeyPair(object):
    def __init__(self, key=None):
        if key is None:
            k = OpenSSL.crypto.PKey()
            k.generate_key(OpenSSL.crypto.TYPE_RSA, 2048)
            key = OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, k)
        self._private_key = RSA.importKey(key)

    @property
    def private_key(self):
        """Output PEM encoded PKCS1 Private Key"""
        return self._private_key.exportKey()

    @property
    def public_key(self):
        """Output Pem encoded X509 SubjectPublicKey"""
        return self._private_key.publickey().exportKey()

class SslPair(KeyPair):
    def __init__(self, CA, CN=None, OU=None, O=None, ST=None, C=None, *args, **kwargs):
        super(SslPair, self).__init__(*args, **kwargs)
        self._ssl_private_key = OpenSSL.crypto.load_privatekey(self.private_key)
        self._certificate = OpenSSL.crypto.X509()
        self._certificate.set_pubkey(self._ssl_private_key)
        if CN is not None:
            self._certificate.get_subject().CN = CN
        if OU is not None:
            self._certificate.get_subject().OU = OU
        if O is not None:
            self._certificate.get_subject().O = O
        if ST is not None:
            self._certificate.get_subject().ST = ST
        if C is not None:
            self._certificate.get_subject().C = C
        self._certificate.set_issuer(CA._certificate.get_subject())
        self._certificate.set_notBefore(datetime.datetime.utcnow().strftime('%Y%m%d%H%M%SZ'))
        self._certificate.set_notAfter((datetime.datetime.utcnow() + datetime.timedelta(3650)).strftime('%Y%m%d%H%M%SZ'))
        self._certificate.set_serial_number(2)
        self.certificate_hook()
        self._certificate.sign(CA._ssl_private_key, 'sha1')

    def certificate_hook(self):
        pass

    @property
    def certificate(self):
        """Output PEM encoded X509 certificate"""
        return OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, self._certificate)

class CertificateAuthority(SslPair):
    def __init__(self, *args, **kwargs):
        super(CertificateAuthority, self).__init__(self, *args, **kwargs)

    def certificate_hook(self):
        self._certificate.set_version(0x2) # version 3
        self._certificate.add_extensions([
            OpenSSL.crypto.X509Extension("basicConstraints", False, "CA:TRUE"),
            OpenSSL.crypto.X509Extension("keyUsage", False, "keyCertSign"),
            OpenSSL.crypto.X509Extension("subjectKeyIdentifier", False, "hash", subject=self._certificate)
        ])
        self._certificate.add_extensions([
            OpenSSL.crypto.X509Extension("authorityKeyIdentifier", False, "keyid:always", issuer=self._certificate),
        ])
