#!/usr/bin/python
from __future__ import unicode_literals
import re
from time import sleep
from logging import getLogger
from itertools import islice
from django.core.exceptions import ValidationError

logger = getLogger(__name__)


def retry(func, initial_delay=50, max_retries=12):
    """func must return truthy value"""
    delay = initial_delay
    for _ in range(max_retries-1):
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

cron_validators = (
    lambda x, allow_text: (re.match(r'^\d+$', x) and 0 <= int(x, 10) <= 59) or allow_text and x == '*',
    lambda x, allow_text: (re.match(r'^\d+$', x) and 0 <= int(x, 10) <= 23) or allow_text and x == '*',
    lambda x, allow_text: (re.match(r'^\d+$', x) and 1 <= int(x, 10) <= 31) or allow_text and x == '*',
    lambda x, allow_text: (re.match(r'^\d+$', x) and 1 <= int(x, 10) <= 12) or allow_text and x.lower() in (
        '*', 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'),
    lambda x, allow_text: (re.match(r'^\d+$', x) and 0 <= int(x, 10) <= 07) or allow_text and x.lower() in (
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
                if not cron_validators[period](part_range[0], False):
                    raise ValidationError("Invalid range part: %s" % part_range[0])
                if not cron_validators[period](part_range[1], False):
                    raise ValidationError("Invalid range part: %s" % part_range[1])
            elif not cron_validators[period](part_range[0], True):
                raise ValidationError("Invalid range part: %s" % part_range[0])
            if len(part_step) > 1:
                if len(part_range) == 1 and part_range[0] != '*':
                    raise ValidationError("Schedule step requires a range to step over")
                if not re.match(r'^\d+$', part_step[1]):
                    raise ValidationError("Invalid step: %s" % part_step[1])


def mysql_database_validator(value):
    if len(value) > 64:
        raise ValidationError("Database name too long: %s." % value)
    if len(value) == 0:
        raise ValidationError("Cannot create database with blank name.")
    if not re.match(r'^[\w$]*[A-Za-z][\w$]*$', value):
        raise ValidationError("Database name must consist of at least one letter and numbers only: %s." % value)
    if value.upper() in ('MYSQL', 'PERFORMANCE_SCHEMA', 'INFORMATION_SCHEMA'):
        raise ValidationError("Database name prohibited: %s" % value)
    if value.upper() in ('ACCESSIBLE', 'ADD', 'ALL', 'ALTER', 'ANALYZE', 'AND', 'AS', 'ASC', 'ASENSITIVE', 'BEFORE',
                         'BETWEEN', 'BIGINT', 'BINARY', 'BLOB', 'BOTH', 'BY', 'CALL', 'CASCADE', 'CASE', 'CHANGE',
                         'CHAR', 'CHARACTER', 'CHECK', 'COLLATE', 'COLUMN', 'CONDITION', 'CONSTRAINT', 'CONTINUE',
                         'CONVERT', 'CREATE', 'CROSS', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP',
                         'CURRENT_USER', 'CURSOR', 'DATABASE', 'DATABASES', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE',
                         'DAY_SECOND', 'DEC', 'DECIMAL', 'DECLARE', 'DEFAULT', 'DELAYED', 'DELETE', 'DESC', 'DESCRIBE',
                         'DETERMINISTIC', 'DISTINCT', 'DISTINCTROW', 'DIV', 'DOUBLE', 'DROP', 'DUAL', 'EACH', 'ELSE',
                         'ELSEIF', 'ENCLOSED', 'ESCAPED', 'EXISTS', 'EXIT', 'EXPLAIN', 'FALSE', 'FETCH', 'FLOAT',
                         'FLOAT4', 'FLOAT8', 'FOR', 'FORCE', 'FOREIGN', 'FROM', 'FULLTEXT', 'GET', 'GRANT', 'GROUP',
                         'HAVING', 'HIGH_PRIORITY', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'IF', 'IGNORE',
                         'IN', 'INDEX', 'INFILE', 'INNER', 'INOUT', 'INSENSITIVE', 'INSERT', 'INT', 'INT1', 'INT2',
                         'INT3', 'INT4', 'INT8', 'INTEGER', 'INTERVAL', 'INTO', 'IO_AFTER_GTIDS', 'IO_BEFORE_GTIDS',
                         'IS', 'ITERATE', 'JOIN', 'KEY', 'KEYS', 'KILL', 'LEADING', 'LEAVE', 'LEFT', 'LIKE', 'LIMIT',
                         'LINEAR', 'LINES', 'LOAD', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCK', 'LONG', 'LONGBLOB',
                         'LONGTEXT', 'LOOP', 'LOW_PRIORITY', 'MASTER_BIND', 'MASTER_SSL_VERIFY_SERVER_CERT', 'MATCH',
                         'MAXVALUE', 'MEDIUMBLOB', 'MEDIUMINT', 'MEDIUMTEXT', 'MIDDLEINT', 'MINUTE_MICROSECOND',
                         'MINUTE_SECOND', 'MOD', 'MODIFIES', 'NATURAL', 'NOT', 'NO_WRITE_TO_BINLOG', 'NULL', 'NUMERIC',
                         'ON', 'OPTIMIZE', 'OPTION', 'OPTIONALLY', 'OR', 'ORDER', 'OUT', 'OUTER', 'OUTFILE',
                         'PARTITION', 'PRECISION', 'PRIMARY', 'PROCEDURE', 'PURGE', 'RANGE', 'READ', 'READS',
                         'READ_WRITE', 'REAL', 'REFERENCES', 'REGEXP', 'RELEASE', 'RENAME', 'REPEAT', 'REPLACE',
                         'REQUIRE', 'RESIGNAL', 'RESTRICT', 'RETURN', 'REVOKE', 'RIGHT', 'RLIKE', 'SCHEMA', 'SCHEMAS',
                         'SECOND_MICROSECOND', 'SELECT', 'SENSITIVE', 'SEPARATOR', 'SET', 'SHOW', 'SIGNAL', 'SMALLINT',
                         'SPATIAL', 'SPECIFIC', 'SQL', 'SQLEXCEPTION', 'SQLSTATE', 'SQLWARNING', 'SQL_BIG_RESULT',
                         'SQL_CALC_FOUND_ROWS', 'SQL_SMALL_RESULT', 'SSL', 'STARTING', 'STRAIGHT_JOIN', 'TABLE',
                         'TERMINATED', 'THEN', 'TINYBLOB', 'TINYINT', 'TINYTEXT', 'TO', 'TRAILING', 'TRIGGER', 'TRUE',
                         'UNDO', 'UNION', 'UNIQUE', 'UNLOCK', 'UNSIGNED', 'UPDATE', 'USAGE', 'USE', 'USING', 'UTC_DATE',
                         'UTC_TIME', 'UTC_TIMESTAMP', 'VALUES', 'VARBINARY', 'VARCHAR', 'VARCHARACTER', 'VARYING',
                         'WHEN', 'WHERE', 'WHILE', 'WITH', 'WRITE', 'XOR', 'YEAR_MONTH', 'ZEROFILL', 'GET',
                         'IO_AFTER_GTIDS', 'IO_BEFORE_GTIDS', 'MASTER_BIND', 'ONE_SHOT', 'PARTITION', 'SQL_AFTER_GTIDS',
                         'SQL_BEFORE_GTIDS'):
        raise ValidationError("Database name is a reserved word: %s." % value)


def comma_separated_mysql_database_validator(value):
    errors = []
    for db in value.split(','):
        try:
            mysql_database_validator(db)
        except ValidationError as e:
            errors.append(e)
    if len(errors) > 0:
        raise ValidationError(" ".join(str(e) for e in errors))


def split_every(n, iterable):
    """"Given an iterable, return slices of the iterable in separate lists."""
    i = iter(iterable)
    piece = list(islice(i, n))
    while piece:
        yield piece
        piece = list(islice(i, n))
