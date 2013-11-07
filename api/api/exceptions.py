#!/usr/bin/python
from __future__ import unicode_literals
import collections

class BackendNotReady(Exception):
    pass

class DiskNotAvailableException(Exception):
    pass

SaltFailure = collections.namedtuple('SaltFailure', ['dns_name','forumla_name','formula_error'])

class SaltError(Exception):
    def __init__(self, missing, failures):
        self.missing = missing
        self.failures = failures

    def __repr__(self):
        return "SaltError(missing=%r, failures=%r)" % (self.missing, self.failures)

    def __str__(self):
        errors = []
        if self.missing:
            errors.extend("Node %s did not reply." % n for n in self.missing)
        if self.failures:
            errors.extend(
                "Node %s failed to configure %s: %s." % failure
                    for failure in self.failures)
        return " ".join(errors)

def check_for_salt_error(result, node_dns_names):
    missing = list(set(node_dns_names) - set(result.iterkeys()))
    failures=[]
    failures.extend(
        SaltFailure(dns_name, formula_name, salt_output['comment'])
        for dns_name, sls_formulas in
            filter(lambda x: isinstance(x[1], collections.Mapping), result.iteritems())
        for formula_name, salt_output in sls_formulas.iteritems()
        if not salt_output['result']
    )
    failures.extend(
        SaltFailure(dns_name, '', sls_failure)
        for dns_name, sls_failure_list in
            filter(lambda x: isinstance(x[1], collections.Sequence), result.iteritems())
        for sls_failure in sls_failure_list
    )
    if missing or failures:
        raise SaltError(missing=missing, failures=failures)
