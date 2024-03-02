import os
from pathlib import Path

from ms_identity_web.configuration import AADConfig
from ms_identity_web import IdentityWebPython


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY","unset_key")

# Building a variable to pivot between prod and dev environments
stage = os.getenv("stage","predeploymigrations")

if stage == "prod":
    DEBUG = False
    SECURE_SSL_REDIRECT = True 
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    
if stage == "dev":
    DEBUG = True

# Using pipe delimeted string to allow the environment vars to separate a list of hosts. 
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS","ERROR: `ALLOWED_HOSTS` NOT FOUND IN ENVIRONMENT VARIABLES").split('|')

# Application definition
AAD_CONFIG = AADConfig.parse_json(file_path='aad.config.json')
AAD_CONFIG.client.client_id = os.getenv("AAD_CLIENT_ID","ERROR: `AAD_CLIENT_ID` NOT FOUND IN ENVIRONMENT VARIABLES")
AAD_CONFIG.client.client_credential = os.getenv("AAD_CLIENT_CREDENTIAL","ERROR: `AAD_CLIENT_CREDENTIAL` NOT FOUND IN ENVIRONMENT VARIABLES")
AAD_CONFIG.client.authority = f"https://login.microsoftonline.com/{os.getenv('AAD_TENANT_ID','ERROR: `AAD_TENANT_ID` NOT FOUND IN ENVIRONMENT VARIABLES')}"


MS_IDENTITY_WEB = IdentityWebPython(AAD_CONFIG)
ERROR_TEMPLATE = 'registration/{}.html' # for rendering 401 or other errors from msal_middleware


# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "app",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "ms_identity_web.django.middleware.MsalMiddleware"
]

ROOT_URLCONF = "web.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "web.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases


# The Game uses CosmosDB and AAD for authentication and data. The SQLite doesn't do anythign. 
# It's only here to keep the default Django functionality from crashing, but it is never used.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]
ACCOUNT_LOGOUT_REDIRECT_URL = '/'

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static and Media Files

# STATIC_URL = "/static/"
if stage == "predeploymigrations":
    log_path = "not_really_running.log"
    abs_path = os.environ.get('abspath','.')
    STATIC_ROOT = 'static'
    STATIC_URL = '/static/'
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

if stage == "prod":
    AZURE_STORAGE_KEY = os.environ.get('AZURE_STORAGE_KEY', False)+"==" # wierd env string issue
    AZURE_ACCOUNT_NAME = os.environ.get('AZURE_ACCOUNT_NAME', False)
    AZURE_STATIC_CONTAINER = os.environ.get('AZURE_STATIC_CONTAINER', 'static')
    AZURE_CUSTOM_DOMAIN = f'{AZURE_ACCOUNT_NAME}.blob.core.windows.net'  # CDN URL
    STATIC_URL = f'https://{AZURE_CUSTOM_DOMAIN}/{AZURE_STATIC_CONTAINER}/'
    STATIC_ROOT = os.path.join("app", "static")
    log_path = "prod_blog_log.log"
    DEFAULT_FILE_STORAGE = 'web.backend.AzureMediaStorage'
    STATICFILES_STORAGE  = 'web.backend.AzureStaticStorage'

if stage == "dev":
    STATIC_URL = "/static/"
    STATIC_ROOT = os.path.join(abs_path, "app", "static", "app")
    log_path = os.path.join(abs_path, "data", "non_prod_blog_log.log")


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "handlers": {
        "logfile": {
            "class": "logging.handlers.WatchedFileHandler",
            "filename": log_path,
        }
    },
    "loggers": {
        "django": {"handlers": ["logfile"], "level": "ERROR", "propagate": False,}
    },
}
