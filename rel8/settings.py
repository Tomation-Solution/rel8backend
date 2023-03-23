"""
Django settings for rel8 project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import os
from urllib.parse import urlparse
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
import cloudinary_storage
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['secret_key']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*',]


# Application definition

# INSTALLED_APPS = [
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
# ]


SHARED_APPS = (
    'django_tenants',  # mandatory
    "Rel8Tenant",
    "account",
    "Dueapp",
    # everything below here is optional
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'django.contrib.contenttypes',
       'corsheaders',
    
    # third party apps
    'rest_framework',
      'rest_framework.authtoken',
       "django_celery_results",
    "django_celery_beat",
    "django_tenants_celery_beat",
    "django_filters",

    #    "cloudinary_storage",
    "cloudinary",
     'channels',
     'chat',
     'meeting',
     'prospectivemember'

     # you must list the app where your tenant model resides in
    #    'mailing',

)

TENANT_APPS = (
    "account",
    
     'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    # your tenant-specific apps
    "Dueapp",
    'event',
    'news',
    "publication",
    'extras',
    "election",
    "subscription",
    "minute",
    "faq",
    'reminders',
     'chat',
    # third party apps
    'rest_framework',
      'rest_framework.authtoken',
    "django_celery_results",
    "django_filters",
       'corsheaders',
       'mailing',
     'channels',
    'anymail',
     'meeting',
     'interswitchapp',
     'LatestUpdate',
     'services',
'prospectivemember'
    # my apps

)
INSTALLED_APPS = list(SHARED_APPS) + [app for app in TENANT_APPS if app not in SHARED_APPS]


MIDDLEWARE = [
        "utils.customTenantSubFolderUrl.CustomTenantSubFolderMiddleware",
    #  'django_tenants.middleware.main.TenantMainMiddleware',
    'django.middleware.security.SecurityMiddleware',
      "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'rel8.urls_tenant'
PUBLIC_SCHEMA_URLCONF ="rel8.urls_public"
TENANT_SUBFOLDER_PREFIX = "tenant"
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'rel8.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
if os.environ.get('databaseUser',None):

    DATABASES = {
        'default': {
            'ENGINE': 'django_tenants.postgresql_backend',
            'NAME': os.environ['databaseName'], 
            'USER': os.environ['databaseUser'], 
            'PASSWORD': os.environ['databasePassword'],
            'HOST': os.environ['databaseHost'], 
            'PORT': os.environ['databasePort'],
        }
    }
else:
    db_info = urlparse(os.environ.get('DATABASE_URL',None))
    DATABASES = {
    "default": {
    "ENGINE": "django_tenants.postgresql_backend",
    "NAME": db_info.path[1:],
    "USER": db_info.username,
    "PASSWORD": db_info.password,
    "HOST": db_info.hostname,
    "PORT": db_info.port,
    "OPTIONS": {"sslmode": "require"},
    "CONN_MAX_AGE": 60,
    }
    }
DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Lagos'
CELERY_TIMEZONE=TIME_ZONE
USE_I18N = True
CELERY_ENABLE_UTC = False
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
MEDIA_URL = '/media/'
# STATIC_ROOT=Path(BASE_DIR,'static')
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
DEFAULT_FROM_EMAIL =os.environ['domain_mail']
SERVER_EMAIL=DEFAULT_FROM_EMAIL
BASE_DOMAIN=os.environ['BASE_DOMAIN']

ANYMAIL = {
    "SENDINBLUE_API_KEY": os.environ['SENDINBLUE_API_KEY'],
}
EMAIL_BACKEND = "anymail.backends.sendinblue.EmailBackend" 

TENANT_MODEL = "Rel8Tenant.Client" # app.Model

TENANT_DOMAIN_MODEL = "Rel8Tenant.Domain"  # app.Model

AUTH_USER_MODEL ="account.User"

# EXTRA REST SETTINgiGS

REST_FRAMEWORK = {
    #here am just telling django rest to use this function for my error response 
    'EXCEPTION_HANDLER': 'utils.custom_exception_response.custom_exception_handler',
    # 'DEFAULT_PARSER_CLASSES': [
    #     'rest_framework.parsers.JSONParser',
    # ],
    'DEFAULT_AUTHENTICATION_CLASSES':[
         'rest_framework.authentication.TokenAuthentication'
    ],
      "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}


PAYSTACK_SECRET=os.environ['PAYSTACK_SECRET']
PAYSTACK_PUBLICKEY=os.environ['PAYSTACK_PUBLICKEY']

if os.environ.get('REDIS_URL',None):
    "if u have a redis url u can always put it in the venv...."
    CELERY_BROKER_URL =os.environ.get('REDIS_URL')


sentry_sdk.init(
    dsn="https://a587ed04d437497199ba62aececdc5ed@o930234.ingest.sentry.io/6394255",
    integrations=[DjangoIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)






CORS_ALLOWED_ORIGINS = [
# 'ws://localhost:6000',
"http://localhost:3000",
"http://localhost:5500",
'https://spectacular-beignet-868060.netlify.app',
'https://fancy-dragon-bad276.netlify.app',
'http://members.nimn.com.ng',
'https://members.nimn.com.ng',
# "http://localhost:8000",
# 'https://guileless-stroopwafel-666090.netlify.app'
'https://cool-liger-caec7e.netlify.app',
'http://cool-liger-caec7e.netlify.app',
'https://nimn-frontend-production.up.railway.app',
'http://nimn-frontend-production.up.railway.app',
'http://rela8.tech',
'https://rela8.tech',
'https://www.rela8.tech',
'https://www.rela8.tech',
'https://rel8-man-production.up.railway.app',
'http://rel8-man-production.up.railway.app',
'https://rel8admin-production.up.railway.app',
'http://rel8admin-production.up.railway.app',
'http://man.rel8membership.com',
'https://man.rel8membership.com',
'http://www.rel8membership.com',
'https://www.rel8membership.com',
'https://rel8membership.com',
'http://rel8membership.com',
]
if os.environ.get('databaseName',None):
    CORS_ALLOWED_ORIGINS.append('http://localhost:3000')

CORS_ALLOW_METHODS = [
'DELETE',
'GET',
'OPTIONS',
'PATCH',
'POST',
'PUT',
]

CORS_ALLOW_HEADERS = [
'accept',
'accept-encoding',
'authorization',
'content-type',
'dnt',
'origin',
'user-agent',
'x-csrftoken',
'x-requested-with',
]



# cloudinary settings
"usiing cloudinary for storage"
CLOUDINARY_URL = os.environ["CLOUDINARY_URL"]
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"
ASGI_APPLICATION = "rel8.routing.application"


if os.environ.get('REDIS_URL'):
    CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [os.environ['REDIS_URL']],
        },
    },
    }

    # CACHES = {
    # "default": {
    #     "BACKEND": "django_redis.cache.RedisCache",
    #     "LOCATION": os.environ['REDIS_URL'],
    #     "OPTIONS": {
    #         "CLIENT_CLASS": "django_redis.client.DefaultClient"
    #     }
    # }
    # }
else:
    CHANNEL_LAYERS={
        'default':{
            'BACKEND':'channels.layers.InMemoryChannelLayer'
        }
    }

redis_url = os.environ.get('REDIS_URL',None)
if redis_url:
    CELERY_BROKER_URL =redis_url
PERIODIC_TASK_TENANT_LINK_MODEL ='Rel8Tenant.PeriodicTaskTenantLink'