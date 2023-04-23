# Every setting in base.py can be overloaded by redefining it here.
from .base import *

SECRET_KEY = os.environ.get("AA_SECRET_KEY")
SITE_NAME = os.environ.get("AA_SITENAME")
SITE_URL = (
    f"{os.environ.get('PROTOCOL')}"
    f"{os.environ.get('AUTH_SUBDOMAIN')}."
    f"{os.environ.get('DOMAIN')}"
)
CSRF_TRUSTED_ORIGINS = [SITE_URL]
DEBUG = os.environ.get("AA_DEBUG", False)
DATABASES["default"] = {
    "ENGINE": "django.db.backends.mysql",
    "NAME": os.environ.get("AA_DB_NAME"),
    "USER": os.environ.get("AA_DB_USER"),
    "PASSWORD": os.environ.get("AA_DB_PASSWORD"),
    "HOST": os.environ.get("AA_DB_HOST"),
    "PORT": os.environ.get("AA_DB_PORT", "3306"),
}

# Register an application at https://developers.eveonline.com for Authentication
# & API Access and fill out these settings. Be sure to set the callback URL
# to https://example.com/sso/callback substituting your domain for example.com
# Logging in to auth requires the publicData scope (can be overridden through the
# LOGIN_TOKEN_SCOPES setting). Other apps may require more (see their docs).

ESI_SSO_CLIENT_ID = os.environ.get("ESI_SSO_CLIENT_ID")
ESI_SSO_CLIENT_SECRET = os.environ.get("ESI_SSO_CLIENT_SECRET")
ESI_SSO_CALLBACK_URL = f"{SITE_URL}/sso/callback"
ESI_USER_CONTACT_EMAIL = os.environ.get(
    "ESI_USER_CONTACT_EMAIL"
)  # A server maintainer that CCP can contact in case of issues.

# By default emails are validated before new users can log in.
# It's recommended to use a free service like SparkPost or Elastic Email to send email.
# https://www.sparkpost.com/docs/integrations/django/
# https://elasticemail.com/resources/settings/smtp-api/
# Set the default from email to something like 'noreply@example.com'
# Email validation can be turned off by uncommenting the line below. This can break some services.
REGISTRATION_VERIFY_EMAIL = False
EMAIL_HOST = os.environ.get("AA_EMAIL_HOST", "")
EMAIL_PORT = os.environ.get("AA_EMAIL_PORT", 587)
EMAIL_HOST_USER = os.environ.get("AA_EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("AA_EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = os.environ.get("AA_EMAIL_USE_TLS", True)
DEFAULT_FROM_EMAIL = os.environ.get("AA_DEFAULT_FROM_EMAIL", "")

ROOT_URLCONF = "myauth.urls"
WSGI_APPLICATION = "myauth.wsgi.application"
PROMETHEUS_REDIS_URI = os.environ.get("PROMETHEUS_REDIS_URI", "redis://redis:6379/1")
STATIC_ROOT = "/var/www/myauth/static/"
BROKER_URL = f"redis://{os.environ.get('AA_REDIS', 'redis:6379')}/0"
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{os.environ.get('AA_REDIS', 'redis:6379')}/1",  # change the 1 here to change the database used
    }
}

# Add any additional apps to this list.
INSTALLED_APPS += [
    # https://allianceauth.readthedocs.io/en/latest/features/apps/index.html
    # 'allianceauth.corputils',
    # 'allianceauth.fleetactivitytracking',
    # 'allianceauth.optimer',
    #'invoices',

    # Corp Tools Preloaded
    'corptools',
    'securegroups',

    'allianceauth.permissions_tool',
    'allianceauth.srp',
    #'allianceauth.timerboard',
    #'allianceauth.hrapplications',

    # https://allianceauth.readthedocs.io/en/latest/features/services/index.html
    'allianceauth.services.modules.discord',
    #'allianceauth.services.modules.discourse',
    # 'allianceauth.services.modules.ips4',
    # 'allianceauth.services.modules.openfire',
    'allianceauth.services.modules.mumble',
    # An example of running mumble with authenticator in docker can be found here
    # https://github.com/Solar-Helix-Independent-Transport/allianceauth-docker-mumble
    # 'allianceauth.services.modules.phpbb3',
    # 'allianceauth.services.modules.smf',
    #'allianceauth.services.modules.teamspeak3',
    # 'allianceauth.services.modules.xenforo',
    #'allianceauth.eveonline.autogroups',
    
    # Proms Client
    'aaprom',
]

#######################################
# Add any custom settings below here. #
#######################################

# Mumble Configuration
MUMBLE_URL = os.environ.get("MUMBLE_URL")

## Custom Edit Middleware for Prom Client
MIDDLEWARE = [
    'aaprom.middleware.PrometheusBeforeMiddleware',  # First'
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'allianceauth.authentication.middleware.UserSettingsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allianceauth.analytics.middleware.AnalyticsMiddleware',
    'aaprom.middleware.PrometheusAfterMiddleware',   # Last
]


## CORP TOOLS API
## IF CCP STOP AN ENDPOINT FOR  >3 DAYS UNCOMMENT
## OR IF CCP JUST BAN AUTH ESI AGAIN

#CT_CHAR_ACTIVE_IGNORE_ASSETS_MODULE=True
#CT_CHAR_ACTIVE_IGNORE_STANDINGS_MODULE=True
#CT_CHAR_ACTIVE_IGNORE_KILLMAILS_MODULE=True
#CT_CHAR_ACTIVE_IGNORE_FITTINGS_MODULE=True
#CT_CHAR_ACTIVE_IGNORE_CALLENDAR_MODULE=True
#CT_CHAR_ACTIVE_IGNORE_CONTACTS_MODULE=True
#CT_CHAR_ACTIVE_IGNORE_NOTIFICATIONS_MODULE=True
#CT_CHAR_ACTIVE_IGNORE_ROLES_MODULE=True
#CT_CHAR_ACTIVE_IGNORE_INDUSTRY_MODULE=True
#CT_CHAR_ACTIVE_IGNORE_MINING_MODULE=True
#CT_CHAR_ACTIVE_IGNORE_WALLET_MODULE=True
#CT_CHAR_ACTIVE_IGNORE_SKILLS_MODULE=True
#CT_CHAR_ACTIVE_IGNORE_CLONES_MODULE=True
#CT_CHAR_ACTIVE_IGNORE_LOCATIONS_MODULE=True
#CT_CHAR_ACTIVE_IGNORE_MAIL_MODULE=True
#CT_CHAR_ACTIVE_IGNORE_HELPER_MODULE=True
CT_CHAR_PAUSE_CONTRACTS = True



## LOKI STUFF

### Override the defaults from base.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'extension_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'log/extensions.log'),
            'formatter': 'verbose',
            'maxBytes': 1024 * 1024 * 5,  # edit this line to change max log file size
            'backupCount': 5,  # edit this line to change number of log backups
        },
        'console': {
            'level': 'DEBUG',  # edit this line to change logging level to console
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'notifications': {  # creates notifications for users with logging_notifications permission
            'level': 'ERROR',  # edit this line to change logging level to notifications
            'class': 'allianceauth.notifications.handlers.NotificationHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'allianceauth': {
            'handlers': ['notifications'], ## untested need to test what this does
            'level': 'DEBUG',
        },
        'extensions': {
            'handlers': ['extension_file'], ## untested need to test what this does
            'level': 'DEBUG',
        }
    }
}

###  LOKI Specific settings
LOGGING['formatters']['loki'] = {
    'class': 'allianceauth-loki-logging.LokiFormatter'  # required
}

print(f"Configuring Loki Log job to: {os.path.basename(os.sys.argv[0])}")

LOGGING['handlers']['loki'] = {
    'level': 'DEBUG' if DEBUG else 'INFO',  # Required # We are auto setting the log level to only record debug when in debug.
    'class': 'allianceauth-loki-logging.LokiHandler',  # Required
    'formatter': 'loki',  #Required
    'timeout': 1,  # Post request timeout, default is 0.5. Optional
    # Loki url. Defaults to localhost. Optional.
    'url': 'http://loki:3100/loki/api/v1/push',
    # Extra tags / labels to attach to the log. Optional, but usefull to differentiate instances.
    'tags': {"job":os.path.basename(os.sys.argv[0])}, # Auto set the job to differentiate between celery, gunicorn, manage.py etc.
    # Push mode. Can be 'sync' or 'thread'. Sync is blocking, thread is non-blocking. Defaults to sync. Optional.
    'mode': 'thread',
}

LOGGING['root'] = { # Set the root logger
    'handlers': ['loki', 'console'],
    'level': 'DEBUG' if DEBUG else 'INFO', # Auto set the log level to only record debug when in debug
}

WORKER_HIJACK_ROOT_LOGGER = False  # Do not overide with celery logging.