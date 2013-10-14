import re
from time import sleep
from logging import getLogger
from itertools import islice
from django.core.exceptions import ValidationError

logger = getLogger(__name__)

def retry(func, initialDelay=50, maxRetries=12):
    delay = initialDelay
    for retry in range(maxRetries-1):
        try:
            result = func()
            if result:
                break
        except:
            #Logging for this can be captured from Boto
            pass
        sleep(delay / 1000.0)
        delay *= 2
    else:
        # Final attempt, don't catch exception
        result = func()
    return result

cronvalidators = (
    lambda x, allowtext: (re.match(r'^\d+$', x) and 0 <= int(x, 10) <= 59) or allowtext and x == '*',
    lambda x, allowtext: (re.match(r'^\d+$', x) and 0 <= int(x, 10) <= 23) or allowtext and x == '*',
    lambda x, allowtext: (re.match(r'^\d+$', x) and 1 <= int(x, 10) <= 31) or allowtext and x == '*',
    lambda x, allowtext: (re.match(r'^\d+$', x) and 1 <= int(x, 10) <= 12) or allowtext and x.lower() in (
        '*', 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'),
    lambda x, allowtext: (re.match(r'^\d+$', x) and 0 <= int(x, 10) <= 07) or allowtext and x.lower() in (
        '*', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun')
)
"""Functions for validating each field of a cron schedule"""


def cron_validator(value):
    """Raise an error if :param value: is not a valid cron schedule."""
    if "\n" in value or "\r" in value:
        raise ValidationError("No new lines allowed in schedule")
    values = value.split()
    if len(values) != 5:
        raise ValidationError("Schedule must have exactly 5 whitespace separated fields")
    for period, field in enumerate(values):
        for part in field.split(","):
            part_step = part.split("/")
            if not 0 < len(part_step) <= 2:
                raise ValidationError("Invalid schedule step: %s" % part)
            part_range = part_step[0].split("-")
            if not 0 < len(part_range) <= 2:
                raise ValidationError("Invalid schedule range: %s" % part_step[0])
            if len(part_range) == 2:
                if not cronvalidators[period](part_range[0], False):
                    raise ValidationError("Invalid range part: %s" % part_range[0])
                if not cronvalidators[period](part_range[1], False):
                    raise ValidationError("Invalid range part: %s" % part_range[1])
            elif not cronvalidators[period](part_range[0], True):
                raise ValidationError("Invalid range part: %s" % part_range[0])
            if len(part_step) > 1:
                if len(part_range) == 1 and part_range[0] != '*':
                    raise ValidationError("Schedule step requires a range to step over")
                if not re.match(r'^\d+$', part_step[1]):
                    raise ValidationError("Invalid step: %s" % part_step[1])


def split_every(n, iterable):
    """"Given an iterable, return slices of the iterable in separate lists."""
    i = iter(iterable)
    piece = list(islice(i, n))
    while piece:
        yield piece
        piece = list(islice(i, n))
