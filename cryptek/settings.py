"""
Django settings for cryptek project.

Generated by 'django-admin startproject' using Django 5.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import logging
import os
from pathlib import Path

import environ
from django.contrib import messages
from django_filters import rest_framework

logger = logging.getLogger(__name__)

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False),
    LOCAL=(bool, False),
    PERMISSIONS=(bool, False),
    ALLOWED_HOSTS=(list, ""),
    SECRET_KEY=(str, ""),
    ADMINS=(
        list,
        [
            "admin_is",
        ],
    ),
)

# CORE SETTINGS. https://docs.djangoproject.com/es/5.1/ref/settings/#core-settings =====================================

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

ADMINS = env.list(
    "ADMINS"
)  # https://docs.djangoproject.com/es/5.1/ref/settings/#admins.
MANAGERS = ADMINS  # https://docs.djangoproject.com/es/5.1/ref/settings/#managers.

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/.

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG")  # https://docs.djangoproject.com/es/5.1/ref/settings/#debug.
LOCAL = env.bool("LOCAL")
PERMISSIONS = env.bool("PERMISSIONS")

ALLOWED_HOSTS = env.list(
    "ALLOWED_HOSTS"
)  # https://docs.djangoproject.com/es/5.1/ref/settings/#allowed-hosts.
APPEND_SLASH = True  # https://docs.djangoproject.com/es/5.1/ref/settings/#append-slash.

# APPLICATION DEFINITION. https://docs.djangoproject.com/es/5.1/ref/settings/#installed-apps ===========================
DJANGO_DEFAULT_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
]
THIRD_PARTY_APPS = [
    "csp",
    "rest_framework",
    "django_filters",
    "markdownx",
]
CUSTOM_APPS = [
    "library_tomb.apps.LibraryTombConfig",
    "message_app.apps.MessageAppConfig",
    "log_recorder_app.apps.LogRecorderAppConfig",
    "conscious_element.apps.ConsciousElementConfig",
]
INSTALLED_APPS = DJANGO_DEFAULT_APPS + THIRD_PARTY_APPS + CUSTOM_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    # "django.contrib.sessions.middleware.SessionMiddleware",
    "conscious_element.session_middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "csp.middleware.CSPMiddleware",
]  # https://docs.djangoproject.com/es/5.1/ref/settings/#middleware.

ROOT_URLCONF = "cryptek.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "cryptek/templates"],
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
]  # https://docs.djangoproject.com/es/5.1/ref/settings/#templates.

WSGI_APPLICATION = "cryptek.wsgi.application"  # https://docs.djangoproject.com/es/5.1/ref/settings/#wsgi-application.

# DATABASES. https://docs.djangoproject.com/en/5.1/ref/settings/#databases =============================================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
        "ATOMIC_REQUESTS": True,  # https://docs.djangoproject.com/es/5.1/ref/settings/#atomic-requests.
        "AUTOCOMMIT": True,  # https://docs.djangoproject.com/es/5.1/ref/settings/#autocommit.
    }
}

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": env.str("POSTGRES_DB"),
#         "USER": env.str("POSTGRES_USER"),  # Matches .env
#         "PASSWORD": env.str("POSTGRES_PASSWORD"),
#         # "HOST": env.str("POSTGRES_HOST", default="localhost"),
#         "HOST": "localhost",
#         "PORT": env.int("POSTGRES_PORT", default=5432),
#         "ATOMIC_REQUESTS": True,  # https://docs.djangoproject.com/es/5.1/ref/settings/#atomic-requests.
#         "AUTOCOMMIT": True,  # https://docs.djangoproject.com/es/5.1/ref/settings/#autocommit.
#     }
# }

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#     },
#     'cache-for-ratelimiting': {},
# }

# AUTHENTICATION. https://docs.djangoproject.com/es/5.1/ref/settings/#auth =============================================
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]  # https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators
AUTHENTICATION_BACKENDS = (
    # "django.contrib.auth.backends.ModelBackend",
    "cryptek.backends.EmailOrUsernameAuthenticationBackend",
)
AUTH_USER_MODEL = "conscious_element.CryptekUser"  # https://docs.djangoproject.com/es/5.1/ref/settings/#auth-user-model.
LOGIN_URL = "/login/"  # https://docs.djangoproject.com/es/5.1/ref/settings/#login-url.
LOGIN_REDIRECT_URL = (
    "/blog/"  # https://docs.djangoproject.com/es/5.1/ref/settings/#login-redirect-url.
)
LOGOUT_REDIRECT_URL = "/login/"  # https://docs.djangoproject.com/es/5.1/ref/settings/#logout-redirect-url.
PASSWORD_RESET_TIMEOUT = 259200  # https://docs.djangoproject.com/es/5.1/ref/settings/#password-reset-timeout.
PASSWORD_HASHERS = (
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.ScryptPasswordHasher",
)  # https://docs.djangoproject.com/es/5.1/ref/settings/#password-hashers.

# SECURITY =============================================================================================================
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = ()
X_FRAME_OPTIONS = "DENY"

# CSP - CONTENT SECURITY POLICY.
CSP_REPORT_ONLY = True
CSP_REPORT_URI = "/csp-violations/"
CCONTENT_SECURITY_POLICY = {
    "EXCLUDE_URL_PREFIXES": ["/admin/"],
    "directives": {
        # General content
        "default-src": (
            "'self'",
            "'unsafe-inline'",  # Temporarily allow inline styling
            "http://localhost:8000/*",
            "https://fonts.googleapis.com",
            "https://maxcdn.bootstrapcdn.com",
        ),
        "base-uri": ("'self'",),
        "form-action": ("'self'",),
        "child-src": ("'self'",),
        "connect-src": ("'self'",),
        # Allow image and media sources
        "img-src": ("'self'", "data:"),
        "media-src": ("'self'",),
        "disposition": ("'self'",),
        # Fonts and Styles Configuration
        "font-src": (
            "'self'",
            "http://localhost:8000/*",
            "https://fonts.gstatic.com",  # Required for Google Fonts
            "data:",  # To allow inline base64 fonts if used
        ),
        "style-src": (
            "'self'",
            "'unsafe-inline'",  # Needed if you can't avoid inline styles
            "http://localhost:8000/*",
            "https://fonts.googleapis.com",  # Google Fonts stylesheets
            "https://maxcdn.bootstrapcdn.com",  # Bootstrap stylesheets
        ),
        "style-src-elem": (
            "'self'",
            "'unsafe-inline'",  # Temporarily allow inline styling
            "http://localhost:8000/*",
            "https://fonts.googleapis.com",
            "https://maxcdn.bootstrapcdn.com",
        ),
        "effective-directive": (
            "style-src-elem",
            "http://localhost:8000/*",
        ),
        "original-policy": (
            "'self'",
            "'unsafe-inline'",  # Temporarily allow inline styling
            "http://localhost:8000/*",
            "https://fonts.googleapis.com",
            "https://maxcdn.bootstrapcdn.com",
        ),
        # Scripts
        "script-src": ("'self'",),
    },
}

# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https") # https://docs.djangoproject.com/en/dev/ref/settings/#secure-proxy-ssl-header.
# automatically redirects requests over HTTP to HTTPS.
# SECURE_SSL_REDIRECT = True # https://docs.djangoproject.com/en/5.1/ref/settings/#secure-ssl-redirect.

SECURE_HSTS_INCLUDE_SUBDOMAINS = True  # https://docs.djangoproject.com/en/5.1/ref/settings/#secure-hsts-include-subdomains.
SECURE_HSTS_PRELOAD = (
    True  # https://docs.djangoproject.com/en/5.1/ref/settings/#secure-hsts-preload.
)
SECURE_HSTS_SECONDS = "2,592,000"  # https://docs.djangoproject.com/en/5.1/ref/settings/#secure-hsts-seconds

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = False if DEBUG else True


# INTERNATIONALIZATION =================================================================================================
LANGUAGE_CODE = (
    "en-us"  # https://docs.djangoproject.com/es/5.1/ref/settings/#language-code.
)
LANGUAGES = (
    ("en", "English"),
    ("es", "Spanish"),
)
TIME_ZONE = "UTC"
USE_I18N = True  # https://docs.djangoproject.com/en/5.1/topics/i18n/.
USE_TZ = True  # https://docs.djangoproject.com/es/5.1/ref/settings/#use-tz.


# STATIC & MEDIA FILES (CSS, JavaScript, Images) https://docs.djangoproject.com/es/5.1/ref/settings/#static-files ======
# https://docs.djangoproject.com/en/5.1/howto/static-files/.
STATIC_URL = (
    "/static/"  # https://docs.djangoproject.com/es/5.1/ref/settings/#static-url.
)
MEDIA_URL = "/media/"
STATIC_ROOT = os.path.join(BASE_DIR, "cryptek/static")
MEDIA_ROOT = "cryptek/media"
# STATICFILES_DIRS = [
#     BASE_DIR / "/static/",
# ]
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
        "LOCATION": BASE_DIR
        / "media",  # This is the directory where all uploaded files will be stored
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
# STATICFILES_FINDERS = (
#     "django.contrib.staticfiles.finders.FileSystemFinder",
#     "django.contrib.staticfiles.finders.AppDirectoriesFinder",
# )
# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field.
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
DEFAULT_CHARSET = (
    "utf-8"  # https://docs.djangoproject.com/es/5.1/ref/settings/#default-charset.
)

# LOGGING CONFIGURATION. https://docs.djangoproject.com/es/5.1/ref/settings/#logging ===================================
# https://docs.djangoproject.com/es/5.1/topics/logging/#configuring-logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "WARNING",
            "class": "logging.FileHandler",
            "filename": "csp_violations.log",
        },
        "console": {
            "level": "WARNING",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django_csp": {
            "handlers": ["file", "console"],
            "level": "WARNING",
            "propagate": False,
        },
    },
}

# EMAIL CONFIGURATION. https://docs.djangoproject.com/es/5.1/ref/settings/#default-from-email. =========================
DEV_EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
PROD_EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_BACKEND = DEV_EMAIL_BACKEND if DEBUG else PROD_EMAIL_BACKEND
EMAIL_HOST = env.str("EMAIL_HOST")
EMAIL_PORT = env.int("EMAIL_PORT")
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env.str("EMAIL_USERNAME")
EMAIL_HOST_PASSWORD = env.str("EMAIL_PASSWORD")

# MESSAGES. https://docs.djangoproject.com/es/5.1/ref/settings/#messages. ==============================================
MESSAGE_TAGS = {
    messages.DEBUG: "debug",
    messages.INFO: "info",
    messages.SUCCESS: "success",
    messages.WARNING: "warning",
    messages.ERROR: "error",
}

# SESSIONS. https://docs.djangoproject.com/es/5.1/ref/settings/#sessions. ==============================================
SESSION_ENGINE = "conscious_element.backends"
