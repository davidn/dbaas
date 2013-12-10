from django.conf import settings
from datetime import timedelta
from django.utils.timezone import now
from ..models import Cluster


def user_expired(user):
    if user.is_paid:
        return False
    q = Cluster.history.filter(user_id=user.id, status=Cluster.PROVISIONING).order_by('-history_date')
    try:
        first_cluster = q[0]
    except IndexError:
        return False
    return first_cluster.history_date + settings.TRIAL_LENGTH < now()

def user_near_expiry(user):
    if user.is_paid:
        return False
    q = Cluster.history.filter(user_id=user.id, status=Cluster.PROVISIONING).order_by('-history_date')
    try:
        first_cluster = q[0]
    except IndexError:
        return False
    return first_cluster.history_date + settings.TRIAL_LENGTH - settings.TRIAL_WARN_PERIOD < now()


def user_launched(user):
    return Cluster.history.filter(user_id=user.id, status=Cluster.PROVISIONING).count() != 0


def user_not_launched(user):
    return not user_launched(user)


def user_not_launched_after_2days(user):
    return now() - timedelta(days=5) < user.date_joined < now() - timedelta(days=2) \
        and not user_launched(user) \
        and not user.is_paid


def user_not_launched_after_5days(user):
    return now() - timedelta(days=10) < user.date_joined < now() - timedelta(days=5) \
        and not user_launched(user)\
        and not user.is_paid


def user_not_launched_after_10days(user):
    return user.date_joined < now() - timedelta(days=10) \
        and not user_launched(user) \
        and not user.is_paid


def tables_created(user):
    # in practice this test will need to *not* fire if user_not_launched == true, otherwise the user might get two
    # emails. If you want to be fussy create an extra function so that this can be a 'pure' function. See
    # https://geniedb.atlassian.net/browse/BPB-154?focusedCommentId=20211&page=com.atlassian.jira.plugin.system.issuetabpanels:comment-tabpanel#comment-20211
    raise NotImplementedError()


def rows_created(user):
    raise NotImplementedError()
