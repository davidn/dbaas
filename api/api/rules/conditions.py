from django.conf import settings
from datetime import datetime, timedelta
from django.utils.timezone import utc
from ..models import Cluster


def user_expired(user):
    if user.is_paid:
        return False
    q = Cluster.history.filter(user_id=user.id, status=Cluster.PROVISIONING).order_by('-history_date')
    try:
        first_cluster = q[0]
    except IndexError:
        return False
    return first_cluster.history_date + settings.TRIAL_LENGTH < datetime.utcnow().replace(tzinfo=utc)


def user_launched(user):
    return Cluster.history.filter(user_id=user.id, status=Cluster.PROVISIONING).count() != 0


def user_not_launched(user):
    return not user_launched(user)


def user_not_launched_after_2days(user):
    return user.date_joined + timedelta(days=2) < datetime.utcnow().replace(tzinfo=utc) and not user_launched(user)


def user_not_launched_after_5days(user):
    return user.date_joined + timedelta(days=5) < datetime.utcnow().replace(tzinfo=utc) and not user_launched(user)


def user_not_launched_after_10days(user):
    return user.date_joined + timedelta(days=10) < datetime.utcnow().replace(tzinfo=utc) and not user_launched(user)


def tables_created(user):
    return False


def rows_created(user):
    return False
