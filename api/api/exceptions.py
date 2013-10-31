
class BackendNotReady(Exception):
    pass

class SaltError(Exception):
    def __init__(self, missing, failed):
        self.missing = missing
        self.failed = failed

    def __repr__(self):
        return "SaltError(missing=%r, failed=%r)" % (self.missing, self.failed)

    def __str__(self):
        errors = []
        if self.missing:
            errors.extend("Node %s did not reply." % n for n in self.missing)
        if self.failed:
            errors.extend(
                "Node %s failed to configure %s: %s." % (dns, name, s_o['comment'])
                    for dns,fail in self.failed.iteritems()
                    for name,s_o in fail.iteritems())
        return " ".join(errors)

def check_for_salt_error(result, node_dns_names):
    missing = list(set(node_dns_names) - set(result.iterkeys()))
    failed = (
        (dns_name, dict((p,c) for p,c in d['ret'].iteritems() if not c['result']))
        for dns_name,d in result.iteritems())
    failed = dict(f for f in failed if f[1])
    if missing or failed:
        raise SaltError(missing=missing, failed=failed)
