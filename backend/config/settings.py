import os
import sys
from datetime import timedelta
from pathlib import Path

import environ
from corsheaders.defaults import default_methods

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False),
    DJANGO_STATIC_ROOT=(str, "staticfiles"),
    DJANGO_MEDIA_ROOT=(str, "media"),
)
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))
# To make apps are findable without a prefix
sys.path.append(str(BASE_DIR / "apps"))

DEBUG = env.bool("DJANGO_DEBUG")
DEBUG_TOOLBAR = (env.bool("DJANGO_USE_DEBUG_TOOLBAR"),)

AUTH_USER_MODEL = "account.User"

BASE_URL = env("DJANGO_SERVER_URL")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("DJANGO_SECRET_KEY")

# ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")
ALLOWED_HOSTS = [
    "demo.softeis.net",
    "enchanting-baklava-c0f2a4.netlify.app",
    "127.0.0.1",
    "localhost",
]

# Application definition
DJANGO_APPS = (
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # needs for full-text search with postgres
    "django.contrib.postgres",
)

THIRD_PARTY_APPS = (
    "django_db_logger",
    "django_extensions",
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    "dj_rest_auth",
    "rest_framework_simplejwt.token_blacklist",
)

# add our Apps here
LOCAL_APPS = ("apps.account", "apps.warehouse")

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

CART_SESSION_ID = "cart"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

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

WSGI_APPLICATION = "config.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": env("DATABASE_NAME"),
#         "USER": env("DATABASE_USERNAME"),
#         "PASSWORD": env("DATABASE_PASSWORD"),
#         "HOST": env("DATABASE_HOST"),
#         "PORT": env("DATABASE_PORT"),
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "de-de"

TIME_ZONE = "Europe/Berlin"

USE_I18N = True

USE_TZ = True

MEDIA_ROOT = env("DJANGO_MEDIA_ROOT")
MEDIA_URL = "/media/"

STATIC_URL = "/static/"
STATIC_ROOT = env("DJANGO_STATIC_ROOT")

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

STATICFILES_DIRS = ("static",)

FRONTEND_URL = env("DJANGO_FRONTEND_URL")

# CORS
CORS_ORIGIN_WHITELIST = env.list("DJANGO_CORS_ORIGIN_WHITELIST")
CORS_ALLOWED_ORIGINS = (
    "https://enchanting-baklava-c0f2a4.netlify.app",
    "https://192.168.178.25:5173",
    "http://192.168.178.25:5173",
    "http://localhost:3000",
)
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = default_methods

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

CORS_EXPOSE_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
]

REST_AUTH = {
    "LOGIN_SERIALIZER": "dj_rest_auth.serializers.LoginSerializer",
    "TOKEN_SERIALIZER": "dj_rest_auth.serializers.TokenSerializer",
    "JWT_SERIALIZER": "dj_rest_auth.serializers.JWTSerializer",
    "JWT_SERIALIZER_WITH_EXPIRATION": "dj_rest_auth.serializers.JWTSerializerWithExpiration",
    "JWT_TOKEN_CLAIMS_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "USER_DETAILS_SERIALIZER": "dj_rest_auth.serializers.UserDetailsSerializer",
    "PASSWORD_RESET_SERIALIZER": "dj_rest_auth.serializers.PasswordResetSerializer",
    "PASSWORD_RESET_CONFIRM_SERIALIZER": "dj_rest_auth.serializers.PasswordResetConfirmSerializer",
    "PASSWORD_CHANGE_SERIALIZER": "dj_rest_auth.serializers.PasswordChangeSerializer",
    "REGISTER_SERIALIZER": "dj_rest_auth.registration.serializers.RegisterSerializer",
    "REGISTER_PERMISSION_CLASSES": ("rest_framework.permissions.AllowAny",),
    "TOKEN_MODEL": "rest_framework.authtoken.models.Token",
    "TOKEN_CREATOR": "dj_rest_auth.utils.default_create_token",
    "PASSWORD_RESET_USE_SITES_DOMAIN": False,
    "OLD_PASSWORD_FIELD_ENABLED": False,
    "LOGOUT_ON_PASSWORD_CHANGE": False,
    "SESSION_LOGIN": True,
    "USE_JWT": False,
    "JWT_AUTH_COOKIE": None,
    "JWT_AUTH_REFRESH_COOKIE": None,
    "JWT_AUTH_REFRESH_COOKIE_PATH": "/",
    "JWT_AUTH_SECURE": False,
    "JWT_AUTH_HTTPONLY": True,
    "JWT_AUTH_SAMESITE": "Lax",
    "JWT_AUTH_RETURN_EXPIRATION": False,
    "JWT_AUTH_COOKIE_USE_CSRF": False,
    "JWT_AUTH_COOKIE_ENFORCE_CSRF_ON_UNAUTHENTICATED": False,
}

# SIMPLE_JWT = {
#     "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
#     "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
#     "ROTATE_REFRESH_TOKENS": True,
#     "BLACKLIST_AFTER_ROTATION": True,
#     "UPDATE_LAST_LOGIN": False,
#     "ALGORITHM": "HS256",
#     "SIGNING_KEY": SECRET_KEY,
#     "VERIFYING_KEY": "",
#     "AUDIENCE": None,
#     "ISSUER": None,
#     "JSON_ENCODER": None,
#     "JWK_URL": None,
#     "LEEWAY": 0,
#     "AUTH_HEADER_TYPES": ("Bearer",),
#     "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
#     "USER_ID_FIELD": "id",
#     "USER_ID_CLAIM": "user_id",
#     "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
#     "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
#     "TOKEN_TYPE_CLAIM": "token_type",
#     "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
#     "JTI_CLAIM": "jti",
#     "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
#     "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
#     "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
#     "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
#     "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
#     "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
#     "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
#     "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
#     "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
# }

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "dj_rest_auth.jwt_auth.JWTCookieAuthentication",
    ),
}

ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False

# CSRF
# store csrf token in cookie instead of the session to make it possible
# see ajax howto in django docs: https://docs.djangoproject.com/en/3.2/ref/csrf/#ajax

# CSRF_USE_SESSIONS = False
# CSRF_FAILURE_VIEW = "account.views.csrf_failure"
# CSRF_TRUSTED_ORIGINS = env.list("DJANGO_CSRF_TRUSTED_ORIGINS")
# CSRF_COOKIE_HTTPONLY = env.bool("DJANGO_CSRF_COOKIE_HTTPONLY")
# CSRF_COOKIE_SECURE = env.bool("DJANGO_SESSION_COOKIE_SECURE")
# CSRF_COOKIE_SAMESITE = env.str("DJANGO_SESSION_COOKIE_SAMESITE")

# SESSION_COOKIE_SAMESITE = env.str('DJANGO_SESSION_COOKIE_SAMESITE')
# SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# SESSION_COOKIE_AGE = 1209600  # 2 weeks
# SESSION_COOKIE_SECURE = env.bool('DJANGO_SESSION_COOKIE_SECURE')
# SESSION_COOKIE_HTTPONLY = env.bool('DJANGO_CSRF_COOKIE_HTTPONLY')

# CSRF_COOKIE_DOMAIN = env.str('DJANGO_COOKIE_DOMAIN')
# SESSION_COOKIE_DOMAIN = env.str('DJANGO_COOKIE_DOMAIN')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Logging
DB_LOGGER_ENTRY_LIFETIME = 30
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"},
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
            "%(process)d %(thread)d %(message)s"
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "db_handler": {
            "level": "DEBUG",
            "class": "django_db_logger.db_log_handler.DatabaseLogHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "default": {
            "level": "DEBUG",
            "handlers": ["console", "db_handler"],
            "propagate": True,
        }
    },
}

# Celery settings
CELERY_TIMEZONE = "Europe/Berlin"
# CELERY_BROKER_URL = env("DJANGO_CELERY_BROKER_URL")
# CELERY_TASK_ALWAYS_EAGER = env("DJANGO_CELERY_TASK_ALWAYS_EAGER")

CELERY_RESULT_BACKEND = "rpc://"
CELERY_TASK_CREATE_MISSING_QUEUES = True
CELERY_RETRY_DELAY = 15
CELERY_RETRY_MAX_TIMES = 15  # 15 retries

# Email server configuration
# EMAIL_HOST = env("EMAIL_HOST")
# EMAIL_HOST_USER = env("EMAIL_HOST_USER")
# EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
# EMAIL_PORT = env("EMAIL_PORT")
# EMAIL_USE_TLS = True
