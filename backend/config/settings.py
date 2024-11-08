import os
import sys
from datetime import timedelta
from pathlib import Path

import environ
from celery.schedules import crontab
from corsheaders.defaults import default_headers
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
    "127.0.0.1",
    "0.0.0.0",
    "luminous-begonia-9708f4.netlify.app",
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
    "rest_framework_simplejwt.token_blacklist",
)

# add our Apps here
LOCAL_APPS = ("apps.account", "apps.warehouse")

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "apps.account.middleware.CustomAdminMiddleware",
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

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DATABASE_NAME"),
        "USER": env("DATABASE_USERNAME"),
        "PASSWORD": env("DATABASE_PASSWORD"),
        "HOST": env("DATABASE_HOST"),
        "PORT": env("DATABASE_PORT"),
    }
}

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
#     }
# }

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

STATIC_URL = "/static/"
STATIC_ROOT = env("DJANGO_STATIC_ROOT")

STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)


# FRONTEND_URL = env("DJANGO_FRONTEND_URL")

# CORS

CORS_ORIGIN_WHITELIST = env.list("DJANGO_CORS_ORIGIN_WHITELIST", default=[])

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = default_headers + ("x-xsrf-token", "x-csrftoken")

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 100,
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=50),
    "REFRESH_TOKEN_LIFETIME": timedelta(minutes=50),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "VERIFYING_KEY": SECRET_KEY,
    "AUDIENCE": None,
    "ISSUER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "JTI_CLAIM": "jti",
}

# ACCOUNT_AUTHENTICATION_METHOD = "email"
# ACCOUNT_EMAIL_REQUIRED = True
# ACCOUNT_USERNAME_REQUIRED = False

# CSRF
# store csrf token in cookie instead of the session to make it possible
# see ajax howto in django docs: https://docs.djangoproject.com/en/3.2/ref/csrf/#ajax

# CSRF_USE_SESSIONS = False
# CSRF_FAILURE_VIEW = "account.views.csrf_failure"
CSRF_TRUSTED_ORIGINS = ("https://localhost:5173",)
# CSRF_COOKIE_HTTPONLY = False
# CSRF_COOKIE_SECURE = env.bool("DJANGO_SESSION_COOKIE_SECURE")
# CSRF_COOKIE_SAMESITE = "Strict"

# -------------- Prod -----------------#
# PROD ONLY
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True
# -------------- Prod -----------------#

# SESSION_COOKIE_SAMESITE = "Strict"
# SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# SESSION_COOKIE_AGE = 1209600  # 2 weeks
# SESSION_COOKIE_SECURE = env.bool('DJANGO_SESSION_COOKIE_SECURE')
# SESSION_COOKIE_HTTPONLY = True

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

# ------ Celery settings ------ #
CELERY_TIMEZONE = "Europe/Berlin"
CELERY_BROKER_URL = env("DJANGO_CELERY_BROKER_URL")
CELERY_TASK_ALWAYS_EAGER = env("DJANGO_CELERY_TASK_ALWAYS_EAGER")

CELERY_CACHE_BACKEND = "default"
CELERY_TASK_CREATE_MISSING_QUEUES = True
CELERY_RETRY_DELAY = 15
CELERY_RETRY_MAX_TIMES = 15  # 15 retries

CELERY_BEAT_SCHEDULE = {
    "check stock": {
        "task": "apps.api.tasks.check_stock",
        "schedule": crontab(hour=3, minute=0),
    },
}

# ------ Email server configuration ------ #
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_PORT = env("EMAIL_PORT")
EMAIL_USE_TLS = True

RECIPIENT_ADDRESS = env("RECIPIENT_ADDRESS")

JAZZMIN_SETTINGS = {
    "site_title": "Stocky",
    "site_header": "Zarg Lagerverwaltung",
    "site_brand": "Lagerverwaltung",
    "site_logo": "image/logo256x256.png",
    "welcome_sign": "Zarg Lagerverwaltung",
    "hide_apps": ["django_db_logger", "auth", "token_blacklist"],
    # "hide_models": ["account.user"],
    "related_modal_active": True,
    "icons": {
        "account.user": "fas fa-id-card",
        "account.employee": "fas fa-users",
        "warehouse.stock": "fas fa-cubes",
        "warehouse.category": "fas fa-globe-europe",
        "warehouse.item": "fas fa-store",
        "warehouse.order": "fas fa-shipping-fast",
        "warehouse.returnrequest": "fas fa-exchange-alt",
    },
    "order_with_respect_to": [
        "account.user",
        "account.employee",
        "warehouse.stock",
        "warehouse.item",
        "warehouse.category",
        "warehouse.order",
    ],
    "show_ui_builder": False,
    # "custom_css": custom_css,
    # "changeform_format": "horizontal_tabs",
    # "custom_links": {
    #     "account": [
    #         {
    #             "name": "Benutzer",
    #             "url": "admin:user",
    #             # "icon": "fas fa-exchange-alt",
    #             # # TODO: Refine custom permissions
    #             "permissions": [
    #                 "user.is_staff",
    #             ],
    #         }
    #     ]
    # },
}

ZARG_JAZZMIN_SETTINGS = {
    "site_title": "Stocky - Zarg",
    "site_header": "Zarg Lagerverwaltung",
    "site_brand": "Zarg Lagerverwaltung",
    "site_logo": "image/logo256x256.png",
    "welcome_sign": "Willkommen bei Zarg Lagerverwaltung",
    "hide_apps": ["django_db_logger", "auth", "token_blacklist"],
    "related_modal_active": True,
    "icons": {
        "account.user": "fas fa-id-card",
        "account.employee": "fas fa-users",
        "warehouse.stock": "fas fa-cubes",
        "warehouse.category": "fas fa-globe-europe",
        "warehouse.item": "fas fa-store",
        "warehouse.order": "fas fa-shipping-fast",
        "warehouse.returnrequest": "fas fa-exchange-alt",
    },
    "order_with_respect_to": [
        "account.user",
        "account.employee",
        "warehouse.stock",
        "warehouse.item",
        "warehouse.category",
        "warehouse.order",
    ],
    "show_ui_builder": False,
}

ENERGIEVERSUM_JAZZMIN_SETTINGS = {
    "site_title": "Stocky - Energieversum",
    "site_header": "Lager Energieversum",
    "site_brand": "Energieversum Lager",
    "site_logo": "image/energieversum.png",
    "welcome_sign": "Willkommen bei Energieversum Lager",
    "hide_apps": ["django_db_logger", "auth", "token_blacklist"],
    "related_modal_active": True,
    "icons": {
        "account.user": "fas fa-id-card",
        "account.employee": "fas fa-users",
        "warehouse.stock": "fas fa-cubes",
        "warehouse.category": "fas fa-globe-europe",
        "warehouse.item": "fas fa-store",
        "warehouse.order": "fas fa-shipping-fast",
        "warehouse.returnrequest": "fas fa-exchange-alt",
    },
    "order_with_respect_to": [
        "account.user",
        "account.employee",
        "warehouse.stock",
        "warehouse.item",
        "warehouse.category",
        "warehouse.order",
    ],
    "show_ui_builder": False,
}

SENEC_JAZZMIN_SETTINGS = {
    "site_title": "Stocky - Senec",
    "site_header": "Lager Senec",
    "site_brand": "Senec Lager",
    "site_logo": "image/senec_logo.png",
    "welcome_sign": "Willkommen bei Senec Lager",
    "hide_apps": ["django_db_logger", "auth", "token_blacklist"],
    "related_modal_active": True,
    "icons": {
        "account.user": "fas fa-id-card",
        "account.employee": "fas fa-users",
        "warehouse.stock": "fas fa-cubes",
        "warehouse.category": "fas fa-globe-europe",
        "warehouse.item": "fas fa-store",
        "warehouse.order": "fas fa-shipping-fast",
        "warehouse.returnrequest": "fas fa-exchange-alt",
    },
    "order_with_respect_to": [
        "account.user",
        "account.employee",
        "warehouse.stock",
        "warehouse.item",
        "warehouse.category",
        "warehouse.order",
    ],
    "show_ui_builder": False,
    "custom_links": {
        "warehouse": [
            {
                "name": "Retoure",
                "url": "https://academy.senec.com/totara/catalog/index.php",
                "icon": "fas fa-exchange-alt",
                # TODO: Refine custom permissions
                # "permissions": [
                #     "user.is_staff",
                # ],
            }
        ]
    },
}
