# Django settings for dbaas_api project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

EC2_REGIONS = {
    'us-west-1': {
        'AMI': 'ami-58664d1d',
        'KEY_NAME': 'dbaas',
        'SECURITY_GROUPS': ['dbaas'],
        'name': 'EC2 US West (Northern California)',
    },
    'us-west-2': {
        'AMI': 'ami-b3e57783',
        'KEY_NAME': 'dbaas',
        'SECURITY_GROUPS': ['dbaas'],
        'name': 'EC2 US West (Oregon)',
    },
    'us-east-1': {
        'AMI': 'ami-cdb0c8a4',
        'KEY_NAME': 'dbaas',
        'SECURITY_GROUPS': ['dbaas'],
        'name': 'EC2 US East (Northern Virginia)',
    },
    'eu-west-1': {
        'AMI': 'ami-a1f8e6d5',
        'KEY_NAME': 'dbaas',
        'SECURITY_GROUPS': ['dbaas'],
        'name': 'EC2 EU (Ireland)',
    },
    'ap-northeast-1': {
        'AMI': 'ami-c16bfdc0',
        'KEY_NAME': 'dbaas',
        'SECURITY_GROUPS': ['dbaas'],
        'name': 'EC2 Asia Pacific (Tokyo)',
    },
    'ap-southeast-1': {
        'AMI': 'ami-7a0f4728',
        'KEY_NAME': 'dbaas',
        'SECURITY_GROUPS': ['dbaas'],
        'name': 'EC2 Asia Pacific (Singapore)',
    },
    'ap-southeast-2': {
        'AMI': 'ami-1d851727',
        'KEY_NAME': 'dbaas',
        'SECURITY_GROUPS': ['dbaas'],
        'name': 'EC2 Asia Pacific (Sydney)',
    },
    'sa-east-1': {
        'AMI': 'ami-6fdb7f72',
        'KEY_NAME': 'dbaas',
        'SECURITY_GROUPS': ['dbaas'],
        'name': 'EC2 South America (Sao Paulo)',
    },
}

INSTANCE_TYPES = {
    "t1.micro": {"cpus": 1, "ram": 0.615, "approx_ram": 1},
    "m1.small": {"cpus": 1, "ram": 1.7, "approx_ram": 2},
    "m1.medium": {"cpus": 1, "ram": 3.75, "approx_ram": 4},
    "m1.large": {"cpus": 2, "ram": 7.5, "approx_ram": 8},
    "m1.xlarge": {"cpus": 4, "ram": 15, "approx_ram": 16},
    "m3.xlarge": {"cpus": 4, "ram": 15, "approx_ram": 16},
    "m3.2xlarge": {"cpus": 8, "ram": 30, "approx_ram": 32},
    "c1.medium": {"cpus": 2, "ram": 1.7, "approx_ram": 2},
    "c1.xlarge": {"cpus": 8, "ram": 7, "approx_ram": 8},
    "cc2.8xlarge": {"cpus": 32, "ram": 60.5, "approx_ram": 64},
    "m2.xlarge": {"cpus": 2, "ram": 17.1, "approx_ram": 16},
    "m2.2xlarge": {"cpus": 4, "ram": 34.2, "approx_ram": 32},
    "m2.4xlarge": {"cpus": 8, "ram": 68.4, "approx_ram": 64},
    "cr1.8xlarge": {"cpus": 32, "ram": 244, "approx_ram": 244},
    "hi1.4xlarge": {"cpus": 16, "ram": 60.5, "approx_ram": 64},
    "hs1.8xlarge": {"cpus": 16, "ram": 117, "approx_ram": 117},
    "cg1.4xlarge": {"cpus": 32, "ram": 22.5, "approx_ram": 16}
}


AWS_ACCESS_KEY=""
AWS_SECRET_KEY=""

ROUTE53_ZONE=""
CLUSTER_DNS_TEMPLATE="{cluster}.dbaas.example.com"
REGION_DNS_TEMPLATE="{cluster}-{region}.dbaas.example.com"
NODE_DNS_TEMPLATE="{cluster}-{node}.dbaas.example.com"
EMAIL_SUBJECT="Your GenieDB cluster is ready!"
PLAINTEXT_EMAIL_TEMPLATE="""
Hi {username}, please find the information for your cluster below. I wanted to
point out a few things that you will need.

1. There is a default database '{db}' created.
2. To create any table that you want replicated, you should add
   'ENGINE=GenieDB' to the end of the SQL statement.
   E.g. CREATE TABLE {db}.foo(a INT PRIMARY KEY, b INT) ENGINE=GenieDB;
3. To create any non-replicated table, you can use ENGINE=MyISAM or
   ENGINE=InnoDB.
4. You should set up application servers close to the individual servers.
5. The common DNS name {cluster_dns} will automatically find the
   nearest database
6. The nodes can be directly accessed using specific domain name (notice the
   -1, -2 etc) or IP addresses.

This cluster will be available for your use until {trial_end:%d}{ord}
{trial_end:%B}, at which point we can discuss the results of your trial and
whether or not you want to move forward. Please don't hesitate to let me know
if you have any questions or issues. We are happy to help with your testing or
answer any questions you may have regarding distributed system architecture.

Cluster Details
username: {dbusername}
password: {dbpassword}   <-- Change the password at your earliest convenience
database: {db}
port: {port}

LBR DNS: {cluster_dns}

{node_text}
"""
HTML_EMAIL_TEMPLATE="""
<p>
    Hi {username}, please find the information for your cluster below. I wanted
    to point out a few things that you will need.
</p>
<ol>
    <li>There is a default database &quot;{db}&quot; created.</li>
    <li>To create any table that you want replicated, you should add
        &quot;ENGINE=GenieDB&quot; to the end of the SQL statement. E.g.
        <code>CREATE TABLE {db}.foo(a INT PRIMARY KEY, b INT) ENGINE=GenieDB;
        </code>
    </li>
    <li>To create any non-replicated table, you can use
        <code>ENGINE=MyISAM</code> or <code>ENGINE=InnoDB</code>.</li>
    <li>You should set up application servers close to the individual servers.
    </li>
    <li>The common DNS name <b>{cluster_dns}</b> will automatically find the
        nearest database</li>
    <li>The nodes can be directly accessed using specific domain name (notice
        the -1, -2 etc) or IP addresses.</li>
</ol>
<p>
    This cluster will be available for your use until {trial_end}, at which
    point we can discuss the results of your trial and whether or not you want
    to move forward. Please don't hesitate to let me know if you have any
    questions or issues. We are happy to help with your testing or answer any
    questions you may have regarding distributed system architecture.
</p>
<p>
<b>Cluster Details</b>
    username: {dbusername}<br />
    password: {dbpassword}   <-- Please change the password at your earliest
    convenience :-)<br />
    database: {db}<br />
    port: {port}
</p>
<p>
    LBR DNS: {cluster_dns}
</p>
{node_html}
"""
PLAINTEXT_PER_NODE="""
Node {nid}
Location: {region}
DNS: {node_dns}
IP: {node_ip}
"""
HTML_PER_NODE="""
<p>
    Node {nid}<br />
    Location: {region}<br />
    DNS: {node_dns}<br />
    IP: {node_ip}<br />
</p>
"""
import datetime
TRIAL_LENGTH=datetime.timedelta(weeks=1)
EMAIL_SENDER="newcustomer@geniedb.com"
EMAIL_RECIPIENTS=["newcustomer@geniedb.com"]

DEFAULT_PORT = 3306

HOSTS_DIR='/tmp/hosts'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAdminUser',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    )
}

BROKER_URL = 'amqp://guest:guest@localhost:5672/'

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

TEMPLATE_DIRS = (
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
    'api'
)

CORS_ORIGIN_ALLOW_ALL=True

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

