import base64
import textwrap
import datetime
import OpenSSL

def asn1_to_pem(s, header='RSA PRIVATE KEY'):
    return "-----BEGIN {0}-----\n{1}\n-----END {0}-----\n".format(header, textwrap.fill(base64.standard_b64encode(s), 64))

class KeyPair(object):
    def __init__(self, key=None):
        if key is None:
            self._private_key = OpenSSL.crypto.PKey()
            self._private_key.generate_key(OpenSSL.crypto.TYPE_RSA, 2048)
        else:
            self._private_key = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, key)

    @property
    def private_key(self):
        return asn1_to_pem(OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_ASN1, self._private_key))

    @property
    def public_key(self):
        # this is ridiculous
        if not hasattr(self,'_public_key'):
            x = OpenSSL.crypto.X509()
            x.set_pubkey(self._private_key)
            self._public_key = x.get_pubkey()
        return asn1_to_pem(OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_ASN1, self._public_key), 'PUBLIC KEY')

class SslPair(KeyPair):
    def __init__(self, CA, CN=None, OU=None, O=None, ST=None, C=None, *args, **kwargs):
        super(self,SslPair).__init__(self, *args, **kwargs)
        self._certificate = OpenSSL.crypto.X509()
        self._certificate.set_pubkey(self.private)
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
        self._certificate.sign(CA._private_key, 'sha1')

    def certificate_hook(self):
        pass

    @property
    def certificate(self):
        return OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, self._certificate)

class CertificateAuthority(SslPair):
    def __init__(self, *args, **kwargs):
        super(self,CertificateAuthority).__init__(self, *args, **kwargs)

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
