"""
Django settings for databaseapi project.

Generated by 'django-admin startproject' using Django 3.2.12.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
import logging
from datetime import timedelta

NAME = os.getenv("name")

PI_DOMAIN = os.getenv("pi_domain")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-\
    8to7%ajqsxrgsbr5asn@mzimmxx9-t^4&356adt680x(v^34kt"

# SECURITY WARNING: keep the secret key used in production secret!
FERNET_SECRET_KEY = os.getenv(
    "FERNET_SECRET_KEY", "2kXe3YL7r5_v69Gm4axlcNLWO4f2xAQqaqTTdLZST0A="
)


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("env", "prod") != "prod"

ALLOWED_HOSTS = ["*", f"https://{PI_DOMAIN}"]

CSRF_TRUSTED_ORIGINS = [
    "https://localhost:8443",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    f"https://{PI_DOMAIN}",
]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    f"{NAME}_app",
    "rest_framework",
    "django_filters",
    "corsheaders",
    'django_extensions', # For CSV init players
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",  # This must be BEFORE CommonMiddleware
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = f"{NAME}.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = f"{NAME}.wsgi.application"
ASGI_APPLICATION = f"{NAME}.asgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB"),  # Name of the Database
        "USER": os.getenv("POSTGRES_USER"),  # Username for accessing the database
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),  # Password for the database user.
        "HOST": os.getenv("POSTGRES_HOST"),
        "PORT": os.getenv("POSTGRES_PORT"),
    }
}

AUTH_USER_MODEL = "databaseapi_app.Player"


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Paris"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = f"/static/{NAME}/" if DEBUG else "/static/"

# Répertoire où collecter les fichiers statiques (après collectstatic)
STATIC_ROOT = "/app/staticfiles"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    # "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    # "PAGE_SIZE": 10  # Number of items per page
}


# Healthcheck filter
class HealthCheckFilter(logging.Filter):
    def filter(self, record):
        return "/health/" not in record.getMessage()


# Logging configuration for healthcheck
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "healthcheck_filter": {
            "()": HealthCheckFilter,
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "filters": ["healthcheck_filter"],  # Apply filter here
        },
    },
    "loggers": {
        "django.server": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

CORS_ALLOW_CREDENTIALS = True  # 🔥 Allow cookies in requests
CORS_ALLOW_ALL_ORIGINS = True  # Allow all origins for development
CORS_ALLOW_ORIGINS = [
    "http://localhost:8000",  # Basic
    "http://localhost:8001",  # Tournament
    "http://localhost:8002",  # Match
    "http://localhost:8003",  # Static files
    "http://localhost:8004",  # User
    "http://localhost:8005",  # FastAPI
    "http://localhost:8006",  # Authentication
    "http://localhost:8007",  # DatabaseAPI
    f"https://{PI_DOMAIN}",  # Production
]
CORS_ALLOW_METHODS = ["GET", "POST", "OPTIONS", "PUT", "DELETE"]
CORS_ALLOW_HEADERS = ["*"]
CORS_EXPOSE_HEADERS = ["Content-Type", "X-CSRFToken", "Set-Cookie"]

# JWT settings
JWT_AUTH = {
    "JWT_SECRET_KEY": SECRET_KEY,
    "JWT_ALGORITHM": "HS256",
    "JWT_ALLOW_REFRESH": True,
    "JWT_EXPIRATION_DELTA": timedelta(minutes=15),
    "JWT_REFRESH_EXPIRATION_DELTA": timedelta(days=7),
}

CORS_ALLOW_CREDENTIALS = True  # 🔥 Allow cookies in requests
CORS_ALLOW_ORIGINS = [
    "http://localhost:8000",  # Basic
    "http://localhost:8001",  # Tournament
    "http://localhost:8002",  # Match
    "http://localhost:8003",  # Static files
    "http://localhost:8004",  # User
    "http://localhost:8005",  # FastAPI
    "http://localhost:8006",  # Authentication
    "http://localhost:8007",  # DatabaseAPI
    "https://localhost:8443"  # For secure HTTPS access
    f"https://{PI_DOMAIN}",  # Production
]
CORS_ALLOW_METHODS = ["GET", "POST", "OPTIONS", "PUT", "DELETE"]
CORS_ALLOW_HEADERS = ["*"]

# Cookie settings
SESSION_COOKIE_SECURE = True  # Ensures session cookies are only sent over HTTPS
SESSION_COOKIE_HTTPONLY = True  # Prevents JavaScript access (for security)
SESSION_COOKIE_SAMESITE = "Lax"  # Allows cookies on same-site navigation, blocks cross-site

CSRF_COOKIE_SECURE = True  # Ensures CSRF cookie is only sent over HTTPS
CSRF_COOKIE_HTTPONLY = False  # JavaScript needs access to CSRF token
CSRF_COOKIE_SAMESITE = "Lax"  # Allows CSRF cookie on same-site requests

# CSRF Middleware settings
CSRF_TRUSTED_ORIGINS = ["https://localhost:8443"]  # Add your domain(s) here
