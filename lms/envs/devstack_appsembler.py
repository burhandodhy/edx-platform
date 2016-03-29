from .devstack import *

APPSEMBLER_SECRET_KEY = "secret_key"
# the following ip should work for all dev setups....
APPSEMBLER_AMC_API_BASE = 'http://10.0.2.2:8080/api'
APPSEMBLER_FIRST_LOGIN_API = '/logged_into_edx'

FEATURES["ENABLE_SYSADMIN_DASHBOARD"] = True

# needed to show only users and appsembler courses
FEATURES["ENABLE_COURSE_DISCOVERY"] = True
FEATURES["SHOW_ONLY_APPSEMBLER_AND_OWNED_COURSES"] = False
OAUTH_ENFORCE_SECURE = False

# disable caching in dev environment
CACHES['general']['BACKEND'] = 'django.core.cache.backends.dummy.DummyCache'
CACHES['default']['BACKEND'] = 'django.core.cache.backends.dummy.DummyCache'
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

MICROSITE_BACKEND = 'microsite_configuration.backends.database.DatabaseMicrositeBackend'

INSTALLED_APPS += ('appsembler_lms',)
