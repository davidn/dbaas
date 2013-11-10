from __future__ import unicode_literals
import collections

class SaltError(Exception):
    def __init__(self, failures):
        self.failures = failures

    def __repr__(self):
        return "SaltError(failures=%r)" % (self.failures)

    def __str__(self):
        return " ".join("Failed to configure %s: %s." % failure
                        for failure in self.failures)

def check_highstate_error(result):
    if isinstance(result, collections.Mapping):
        failures = [(formula_name, salt_output) for formula_name, salt_output in
                     result.iteritems() if not salt_output['result']]
    elif isinstance(result, collections.Sequence):
        failures = [('', sls_failure) for sls_failure in result]
    else
        raise TypeError('Expected Mapping or Sequence got %s', result.__class__)
    if failures:
        raise SaltError(failures=failures)
