import re
import boto
from boto.route53 import *
from boto.resultset import ResultSet

# If need to bump connection version
_connect_route53 = boto.connect_route53
def connect_route53(*args, **kwargs):
        route53 = _connect_route53(*args, **kwargs)
        route53.Version = '2012-12-12'
        return route53
boto.connect_route53 = connect_route53

class RecordWithTargetHealthCheck(record.Record):
    def to_xml(self):
        out = super(RecordWithTargetHealthCheck,self).to_xml()
        return re.sub('</AliasTarget>',
                      '<EvaluateTargetHealth>true</EvaluateTargetHealth></AliasTarget>',
                      out)

class RecordWithHealthCheck(record.Record):
    def __init__(self, health_check_id, *args, **kwargs):
        super(RecordWithHealthCheck,self).__init__( *args, **kwargs)
        self.health_check_id = health_check_id

    def to_xml(self):
        out = super(RecordWithHealthCheck,self).to_xml()
        return re.sub('</ResourceRecordSet>',
                      '<HealthCheckId>%(health_check_id)s</HealthCheckId></ResourceRecordSet>' % {'health_check_id':self.health_check_id},
                      out)

# If you need to change the version number
record.ResourceRecordSets.ChangeResourceRecordSetsBody = re.sub(
    'https://route53.amazonaws.com/doc/\d\d\d\d-\d\d?-\d\d?/',
    'https://route53.amazonaws.com/doc/2012-12-12/',
    record.ResourceRecordSets.ChangeResourceRecordSetsBody)


def r53_create_heath_check(self, xml_body):
    uri = '/%s/healthcheck' % self.Version
    response = self.make_request('POST', uri, {'Content-Type' : 'text/xml'}, xml_body)
    body = response.read()
    boto.log.debug(body)
    if response.status >= 300:
        raise exception.DNSServerError(response.status,
                                       response.reason,
                                       body)
    e = boto.jsonresponse.Element()
    h = boto.jsonresponse.XmlHandler(e, None)
    h.parse(body)
    return e

connection.Route53Connection.create_health_check = r53_create_heath_check

def r53_delete_heath_check(self, health_check_id):
    uri = '/%s/healthcheck/%s' % (self.Version, health_check_id)
    response = self.make_request('DELETE', uri)
    body = response.read()
    boto.log.debug(body)
    if response.status not in (200, 204):
        raise exception.DNSServerError(response.status,
                                       response.reason,
                                       body)

connection.Route53Connection.delete_health_check = r53_delete_heath_check

class HealthCheck(ResultSet):
    CreateHealthCheckBody = """<?xml version="1.0" encoding="UTF-8"?>
    <CreateHealthCheckRequest xmlns="https://route53.amazonaws.com/doc/2012-12-12/">
        <CallerReference>%(caller_reference)s</CallerReference>
        <HealthCheckConfig>
            <IPAddress>%(ip_address)s</IPAddress>
            %(port_body)s
            <Type>%(type)s</Type>
            %(resource_path_body)s
            %(fqdn_body)s
        </HealthCheckConfig>
    </CreateHealthCheckRequest>"""

    PortBody = """<Port>%(port)s</Port>"""
    ResoucePathBody = """<ResourcePath>%(resouce_path)s</ResourcePath>"""
    FQDNBody = """<FullyQualifiedDomainName>%(fqdn)s</FullyQualifiedDomainName>"""

    def __init__(self, connection=None, caller_reference=None, ip_address=None, port=None, health_check_type=None, resource_path=None, fqdn=None):
        self.connection = connection
        self.caller_reference = caller_reference
        self.ip_address = ip_address
        self.port = port
        self.type = health_check_type
        self.resource_path = resource_path
        self.fqdn = fqdn
        ResultSet.__init__(self, [('HealthCheck', HealthCheck)])
    
    def to_xml(self):
        return self.CreateHealthCheckBody % {
            'caller_reference': self.caller_reference,
            'ip_address': self.ip_address,
            'type': self.type,
            'port_body': self.PortBody % {'port':self.port} if self.port is not None else '',
            'resource_path_body': self.ResoucePathBody % {'resouce_path':self.resouce_path} if self.resource_path is not None else '',
            'fqdn_body': self.FQDNBody % {'fqdn':self.fqdn} if self.fqdn is not None else ''
        }

    def commit(self):
        """Commit this change"""
        if not self.connection:
            self.connection = boto.connect_route53()
        return self.connection.create_health_check(self.to_xml())

def catch_dns_exists(rrs):
    try:
        rrs.commit()
    except exception.DNSServerError, e:
        if re.search('but it already exists', e.body) is None:
            raise

def catch_dns_not_found(rrs):
    try:
        rrs.commit()
    except exception.DNSServerError, e:
        if re.search('but it was not found', e.body) is None:
            raise
