
class BackendNotReady(Exception):
    pass

class SaltError(Exception):
    pass

def check_for_salt_error(result, node_dns_names):
    missing = set(node_dns_names) - set(result.iterkeys())
    failed = [(dns_name, (change for change in d['ret'] if not change['result'])) for dns_name,d in result.iteritems()]
    failed = dict(f for f in failed if f[1])
    if missing or failed:
        raise SaltError(missing=missing, failed=failed)
