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
import sys
from pathlib import Path

import cloudinary
import dj_database_url
import environ
from django.contrib import messages

logger = logging.getLogger(__name__)

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False),
    DEVELOPMENT_MODE=(bool, False),
    ALLOWED_HOSTS=(list, ""),
    SECRET_KEY=(str, ""),
)

# CORE SETTINGS. https://docs.djangoproject.com/es/5.1/ref/settings/#core-settings =====================================

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/.

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG")  # https://docs.djangoproject.com/es/5.1/ref/settings/#debug.
DEVELOPMENT_MODE = env.bool("DEVELOPMENT_MODE")

SITE_ID = 1  # https://docs.djangoproject.com/es/5.1/ref/settings/#site-id.

ADMINS = env.list("ADMINS")  # https://docs.djangoproject.com/es/5.1/ref/settings/#admins.
MANAGERS = ADMINS  # https://docs.djangoproject.com/es/5.1/ref/settings/#managers.

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")  # https://docs.djangoproject.com/es/5.1/ref/settings/#allowed-hosts.
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
    "django.contrib.sites",  # https://docs.djangoproject.com/es/5.1/ref/contrib/sites/
]
THIRD_PARTY_APPS = [
    "csp",
    "rest_framework",
    "markdownx",
    "debug_toolbar",
    "widget_tweaks",
    # django-allauth.
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    # django-allauth providers.
    "allauth.socialaccount.providers.github",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.linkedin_oauth2",
    "allauth.socialaccount.providers.digitalocean",
]
CUSTOM_APPS = [
    "blog_app.apps.BlogAppConfig",
    "message_app.apps.MessageAppConfig",
    "log_recorder_app.apps.LogRecorderAppConfig",
    "user_app.apps.UserAppConfig",
]
INSTALLED_APPS = DJANGO_DEFAULT_APPS + THIRD_PARTY_APPS + CUSTOM_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "csp.middleware.CSPMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    # "django.contrib.sessions.middleware.SessionMiddleware",
    "user_app.session_middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # # Allauth middleware.
    "allauth.account.middleware.AccountMiddleware",
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
DATABASE = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
        "ATOMIC_REQUESTS": True,  # https://docs.djangoproject.com/es/5.1/ref/settings/#atomic-requests.
        "AUTOCOMMIT": True,  # https://docs.djangoproject.com/es/5.1/ref/settings/#autocommit.
    },
}
TEST_DATABASE = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "test_db.sqlite3",
        "ATOMIC_REQUESTS": True,  # https://docs.djangoproject.com/es/5.1/ref/settings/#atomic-requests.
        "AUTOCOMMIT": True,  # https://docs.djangoproject.com/es/5.1/ref/settings/#autocommit.
    },
}

if "test" in sys.argv:
    DATABASES = TEST_DATABASE
elif DEVELOPMENT_MODE:
    DATABASES = DATABASE
else:
    DATABASES = {"default": dj_database_url.config(env.str("POSTGRES_URL"))}

# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": "redis://127.0.0.1:6379/1",
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#         },
#     }
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
    "allauth.account.auth_backends.AuthenticationBackend",
)
AUTH_USER_MODEL = "user_app.CryptekUser"  # https://docs.djangoproject.com/es/5.1/ref/settings/#auth-user-model.

LOGIN_URL = "login"  # https://docs.djangoproject.com/es/5.1/ref/settings/#login-url.
LOGIN_REDIRECT_URL = "home"  # https://docs.djangoproject.com/es/5.1/ref/settings/#login-redirect-url.
LOGOUT_REDIRECT_URL = "login"  # https://docs.djangoproject.com/es/5.1/ref/settings/#logout-redirect-url.

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
CONTENT_SECURITY_POLICY = {
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
SECURE_SSL_REDIRECT = (
    False if DEVELOPMENT_MODE else True
)  # https://docs.djangoproject.com/en/5.1/ref/settings/#secure-ssl-redirect.

SECURE_HSTS_INCLUDE_SUBDOMAINS = (
    True  # https://docs.djangoproject.com/en/5.1/ref/settings/#secure-hsts-include-subdomains.
)
SECURE_HSTS_PRELOAD = True  # https://docs.djangoproject.com/en/5.1/ref/settings/#secure-hsts-preload.
SECURE_HSTS_SECONDS = "2,592,000"  # https://docs.djangoproject.com/en/5.1/ref/settings/#secure-hsts-seconds

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = False if DEBUG else True

# Email verification settings.
EMAIL_TOKEN_TIMEOUT = 86400  # 24 hours

SOCIALACCOUNT_FORMS = {
    "disconnect": "allauth.socialaccount.forms.DisconnectForm",
    "signup": "allauth.socialaccount.forms.SignupForm",
}

# INTERNATIONALIZATION =================================================================================================
LANGUAGE_CODE = "en-us"  # https://docs.djangoproject.com/es/5.1/ref/settings/#language-code.
LANGUAGES = (
    ("en", "English"),
    ("es", "Spanish"),
)
TIME_ZONE = "UTC"
USE_I18N = True  # https://docs.djangoproject.com/en/5.1/topics/i18n/.
USE_TZ = True  # https://docs.djangoproject.com/es/5.1/ref/settings/#use-tz.

# STATIC & MEDIA FILES (CSS, JavaScript, Images) https://docs.djangoproject.com/es/5.1/ref/settings/#static-files ======
# https://docs.djangoproject.com/en/5.1/howto/static-files/.
STATIC_URL = "/static/"  # https://docs.djangoproject.com/es/5.1/ref/settings/#static-url.
MEDIA_URL = "/media/"
STATIC_ROOT = os.path.join(BASE_DIR, "cryptek/staticfiles")
MEDIA_ROOT = os.path.join(BASE_DIR, "cryptek/media")

cloudinary.config(
    cloud_name=env.str("CLOUDINARY_CLOUD_NAME"),
    api_key=env.str("CLOUDINARY_API_KEY"),
    api_secret=env.str("CLOUDINARY_API_SECRET"),
    secure=True,
)

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field.
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
DEFAULT_CHARSET = "utf-8"  # https://docs.djangoproject.com/es/5.1/ref/settings/#default-charset.

# LOGGING CONFIGURATION. https://docs.djangoproject.com/es/5.1/ref/settings/#logging ===================================
# https://docs.djangoproject.com/es/5.1/topics/logging/#configuring-logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "mail_log": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "email_debug.log",
        },
        "file": {
            "level": "WARNING",
            "class": "logging.FileHandler",
            "filename": "csp_violations.log",
        },
        "console": {
            "level": "WARNING",
            "class": "logging.StreamHandler",
        },
        "null": {
            "class": "logging.NullHandler",
        },
    },
    "loggers": {
        "django_csp": {
            "handlers": ["file", "console", "mail_log"],
            "level": "WARNING",
            "propagate": True,
        },
        "django.security.DisallowedHost": {
            # https://docs.djangoproject.com/es/5.1/ref/logging/#django-security
            "handlers": ["file", "console"],
            "level": "WARNING",
            "propagate": False,
        },
    },
}

# EMAIL CONFIGURATION. https://docs.djangoproject.com/es/5.1/ref/settings/#default-from-email. =========================
DEV_EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
PROD_EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_BACKEND = DEV_EMAIL_BACKEND if DEVELOPMENT_MODE else PROD_EMAIL_BACKEND
EMAIL_HOST = env.str("EMAIL_HOST")
EMAIL_PORT = env.int("EMAIL_PORT")
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env.str("EMAIL_USERNAME")
EMAIL_HOST_PASSWORD = env.str("EMAIL_PASSWORD")
DEFAULT_FROM_EMAIL = env.str("DEFAULT_FROM_EMAIL")
# MESSAGES. https://docs.djangoproject.com/es/5.1/ref/settings/#messages. ==============================================
MESSAGE_TAGS = {
    messages.DEBUG: "debug",
    messages.INFO: "info",
    messages.SUCCESS: "success",
    messages.WARNING: "warning",
    messages.ERROR: "error",
}

# SESSIONS. https://docs.djangoproject.com/es/5.1/ref/settings/#sessions. ==============================================
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# DJANGO DEBUG TOOLBAR. https://django-debug-toolbar.readthedocs.io/en/latest/installation.html ========================
INTERNAL_IPS = [
    "127.0.0.1",
]  # https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#configure-internal-ips.
DEBUG_TOOLBAR_PANELS = [
    "debug_toolbar.panels.history.HistoryPanel",
    "debug_toolbar.panels.versions.VersionsPanel",
    "debug_toolbar.panels.timer.TimerPanel",
    "debug_toolbar.panels.settings.SettingsPanel",
    "debug_toolbar.panels.headers.HeadersPanel",
    "debug_toolbar.panels.request.RequestPanel",
    "debug_toolbar.panels.sql.SQLPanel",
    "debug_toolbar.panels.staticfiles.StaticFilesPanel",
    "debug_toolbar.panels.templates.TemplatesPanel",
    "debug_toolbar.panels.alerts.AlertsPanel",
    "debug_toolbar.panels.cache.CachePanel",
    "debug_toolbar.panels.signals.SignalsPanel",
    # 'debug_toolbar.panels.redirects.RedirectsPanel',
    # "debug_toolbar.panels.profiling.ProfilingPanel",
]

# Django RateLimit. https://django-ratelimit.readthedocs.io/en/stable/ =================================================
RATELIMIT_HASH_ALGORITHM = "hashlib.sha256"
RATELIMIT_ENABLE = False if DEBUG else True

# Django Allauth. https://django-allauth.readthedocs.io/en/latest/installation.html ====================================
SOCIALACCOUNT_PROVIDERS = {
    "github": {
        "SCOPE": [
            "user",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
    },
    "google": {
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
    },
    "linkedin_oauth2": {
        "SCOPE": [
            "r_liteprofile",
            "r_emailaddress",
        ],
        "AUTH_PARAMS": {
            "access_type": "offline",
        },
    },
    "digitalocean": {
        "SCOPE": [
            "read",
            "write",
        ],
        "AUTH_PARAMS": {
            "access_type": "offline",
        },
    },
}
ACCOUNT_ADAPTER = "user_app.adapters.CustomAccountAdapter"
# ACCOUNT_CHANGE_EMAIL = True
# ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = "home"
# ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
# ACCOUNT_EMAIL_NOTIFICATIONS = True
# ACCOUNT_EMAIL_UNKNOWN_ACCOUNTS = True
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"
ACCOUNT_SIGNUP_FIELDS = ["username", "email*", "password1", "password2"]
ACCOUNT_LOGIN_METHODS = ["username", "email"]
ACCOUNT_EMAIL_VERIFICATION = "optional"  # mandatory
ACCOUNT_RATE_LIMITS = {
    "change_password": "5/m/user",
    "manage_email": "10/m/user",
    "reset_password": "20/m/ip,5/m/key",
    "reauthenticate": "10/m/user",
    "reset_password_from_key": "20/m/ip",
    "signup": "20/m/ip",
    "login": "30/m/ip",
    "login_failed": "10/m/ip,5/5m/key",
    "confirm_email": "1/3m/key",
}
# ACCOUNT_REAUTHENTICATION_REQUIRED = True
# ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True
# ACCOUNT_UNIQUE_EMAIL = True
# ACCOUNT_USER_MODEL_EMAIL_FIELD = "email"
# ACCOUNT_USER_MODEL_USERNAME_FIELD = "username"
# ACCOUNT_USERNAME_MIN_LENGTH = 6
# ACCOUNT_USERNAME_REQUIRED = True
