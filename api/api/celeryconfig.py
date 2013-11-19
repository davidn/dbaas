from __future__ import unicode_literals
from datetime import timedelta

BROKER_URL = 'amqp://guest:guest@localhost:5672/'

CELERY_EAGER_PROPAGATES_EXCEPTIONS = False
CELERY_CHORD_PROPAGATES = True
CELERY_SEND_TASK_ERROR_EMAILS = True

CELERYBEAT_SCHEDULE = {
    'rules': {
        'task': 'tasks.rules_process',
        'schedule': timedelta(hours=1)
    }
}
