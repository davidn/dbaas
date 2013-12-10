from __future__ import unicode_literals
from logging import getLogger
from datetime import timedelta

logger = getLogger(__name__)


def disable_user(user):
    logger.info("Disabling user %s", user.email)
    user.is_active = False
    user.save()


def near_expiry_email(user):
    logger.info("Sending trial time warning to %s", user.email)
    user.email_user_template('trial_warning_email', {
        'username': str(user),
        'is_paid': user.is_paid,
        'user': user,
    })

def no_cluster_email(user, delta):
    logger.info("Sending %s day email to %s", delta.days, user.email)
    user.email_user_template('no_cluster_%sday_email' % delta.days, {
        'username': str(user),
        'is_paid': user.is_paid,
        'user': user,
        'unused_time': delta
    })


def no_cluster_email_2days(user):
    no_cluster_email(user, timedelta(days=2))


def no_cluster_email_5days(user):
    no_cluster_email(user, timedelta(days=5))


def no_cluster_email_10days(user):
    no_cluster_email(user, timedelta(days=10))
