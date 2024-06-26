# Django settings for dbaas_api project.

from __future__ import unicode_literals
import datetime

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
# ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '', # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '', # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '', # Set to empty string for default.
    }
}

ZABBIX_SERVER = "zabbix.example.com"
ZABBIX_ENDPOINT = "http://%s/zabbix/" % ZABBIX_SERVER
ZABBIX_USER = ""
ZABBIX_PASSWORD = ""

SALT_MASTER="salt.example.com"
SALT_IPC_PATH='/var/run/salt/master'
# These should only have INSERT perms on the salt_returns table.
SALT_MINION_SQL_USER=''
SALT_MINION_SQL_PASSWORD=''

AWS_ACCESS_KEY = ""
AWS_SECRET_KEY = ""

GCE_PROJECT_ID = ""
GCE_SERVICE_ACCOUNT_EMAIL = ""
GCE_PRIVATE_KEY = ""

RACKSPACE_USER = ""
RACKSPACE_PASS = ""
RACKSPACE_TENANT = ""
RACKSPACE_AUTH_URL = "https://identity.api.rackspacecloud.com/v2.0"

RACKSPACELONDON_USER = ""
RACKSPACELONDON_PASS = ""
RACKSPACELONDON_TENANT = ""
RACKSPACELONDON_AUTH_URL = "https://lon.identity.api.rackspacecloud.com/v2.0/"

PROFITBRICK_USER = ""
PROFITBRICK_PASS = ""

ROUTE53_ZONE = ""
CLUSTER_DNS_TEMPLATE = "{cluster}.dbaas.example.com"
REGION_DNS_TEMPLATE = "{cluster}-{lbr_region}.dbaas.example.com"
NODE_DNS_TEMPLATE = "{cluster}-{node}.dbaas.example.com"
CLUSTER_NID_TEMPLATE = "^(?P<cluster>[-a-f0-9A-F]+)-(?P<nid>\d+)(?:.*)"

BUFFER_POOL_PROPORTION = 0.5

TRIAL_LENGTH = datetime.timedelta(weeks=1)
TRIAL_WARN_PERIOD = datetime.timedelta(days=-1)

DEFAULT_PORT = 3306

HOSTS_DIR = '/tmp/hosts'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAdminUser',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    )
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
# Put strings here, like "/home/html/static" or "C:/www/django/static".
# Always use forward slashes, even on Windows.
# Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'mfv4^l$w==@%xbnr-45+k^e1av3=%(l(g&@syg^e+czl348l$w'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'dbaas_api.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'dbaas_api.wsgi.application'

import os.path

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), '../rest_registration/templates').replace('\\', '/'),
    os.path.join(os.path.dirname(__file__), '../api/templates').replace('\\', '/'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'south',
    'djcelery',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'registration',
    'rest_registration',
    'simple_history',
    'salt_jobs',
    'unbounce_hook',
    'api'
)

ACCOUNT_ACTIVATION_DAYS = 7

AUTH_USER_MODEL = 'api.User'

CORS_ORIGIN_ALLOW_ALL = True

TEST_RUNNER = 'djcelery.contrib.test_runner.CeleryTestSuiteRunnerStoringResult'
BROKER_URL = 'amqp://guest:guest@localhost:5672/'

CELERY_EAGER_PROPAGATES_EXCEPTIONS = False
CELERY_CHORD_PROPAGATES = True
CELERY_SEND_TASK_ERROR_EMAILS = True

CELERYBEAT_SCHEDULE = {
    'rules': {
        'task': 'api.tasks.rules_process',
        'schedule': datetime.timedelta(hours=1)
    }
}
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

try:
    from local_settings import *
except:
    pass


