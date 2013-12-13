from __future__ import unicode_literals
from boto import connect_s3
from django.conf import settings
from django.dispatch.dispatcher import receiver
import south.signals
import api.models


@receiver(south.signals.post_migrate)
def on_syncdb(app, **kwargs):
    if app == 'api':
        s3 = connect_s3(aws_access_key_id=settings.AWS_ACCESS_KEY, aws_secret_access_key=settings.AWS_SECRET_KEY)
        bucket = s3.lookup(api.models.BUCKET_NAME)
        if bucket is None:
            s3.create_bucket(api.models.BUCKET_NAME)
