import os
from pathlib import Path

from django.utils.translation import gettext_lazy as _

from root.ckeditor_settings import CKEDITOR_5_CONFIGS, customColorPalette

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-2i%1#ggus-iqy6j-fl1(0_qy1mc4yav68k1o78v@y)pe*760-o'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.apps.AppsConfig',
    'django_ckeditor_5',
    "debug_toolbar",
    'django.contrib.humanize',
    'rosetta'
]

INTERNAL_IPS = [
    "127.0.0.1",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'root.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.context_processors.languages'
            ],
        },
    },
]

WSGI_APPLICATION = 'root.wsgi.application'
AUTH_USER_MODEL = 'apps.User'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'alijahon_db',
        'USER': 'postgres',
        'PASSWORD': '1',
        'HOST': 'localhost',
        'PORT': '5441'
    }
}

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]

EXTRA_LANG_INFO = {
    'oz': {
        'bidi': False,
        'code': 'oz',
        'name': "O'zbek",
        'name_local': u"O'zbek",  # unicode codepoints here
    },
}
from django.conf import global_settings

gettext_noop = lambda s: s
LANGUAGE_CODE = 'en-us'

LANGUAGES = [
    ('en', _('English')),
    ('ru', _('Russia')),
    ('uz', _('Uzbek')),
    ('oz', gettext_noop("O'zbek")),
]

languages_dict = {
    "en": "English",
    "ru": "Russia",
    "uz": "Uzbek",
    "oz": "O'zbek"
}

import django.conf.locale
from django.conf import global_settings

LANG_INFO = dict(django.conf.locale.LANG_INFO, **EXTRA_LANG_INFO)
django.conf.locale.LANG_INFO = LANG_INFO

global_settings.LANGUAGES = global_settings.LANGUAGES + (["oz", "O'zbek"])
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]
TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR / 'static')

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR / 'media')

LOGOUT_REDIRECT_URL = 'main-page'
LOGIN_URL = '/login'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ROSETTA_STORAGE_CLASS = 'rosetta.storage.CacheRosettaStorage'

# LOGGING = {
#     'version': 1,
#     'filters': {
#         'require_debug_true': {
#             '()': 'django.utils.log.RequireDebugTrue',
#         }
#     },
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'filters': ['require_debug_true'],
#             'class': 'logging.StreamHandler',
#         }
#     },
#     'loggers': {
#         'django.db.backends': {
#             'level': 'DEBUG',
#             'handlers': ['console'],
#         }
#     }
# }
