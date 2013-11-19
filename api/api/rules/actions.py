from __future__ import unicode_literals
from datetime import timedelta


def disable_account(user):
    user.is_active = False
    user.save()


def no_cluster_email(user, delta):
    user.email_user_template('no_cluster_%sday' % timedelta.days, {
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
