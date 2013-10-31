
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
            errors.append("The following nodes did not respond: %s." % ", ".join(self.missing))
        if self.failed:
            errors.append("The following errors occurred: %s." % ", ".join("node %s - %s" % (n,f["comment"]) for n,f in self.failed.iteritems()))
        return " ".join(errors)

def check_for_salt_error(result, node_dns_names):
    missing = list(set(node_dns_names) - set(result.iterkeys()))
    failed = (
        (dns_name, dict((p,c) for p,c in d['ret'].iteritems() if not c['result']))
        for dns_name,d in result.iteritems())
    failed = dict(f for f in failed if f[1])
    if missing or failed:
        raise SaltError(missing=missing, failed=failed)
