"""
Django settings for tournament project.

Generated by 'django-admin startproject' using Django 5.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
import logging


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
# FERNET_SECRET_KEY = os.getenv("2FA_KEY")
FERNET_SECRET_KEY = os.getenv(
    "FERNET_SECRET_KEY", "2kXe3YL7r5_v69Gm4axlcNLWO4f2xAQqaqTTdLZST0A="
)


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("env", "prod") != "prod"

ALLOWED_HOSTS = ["*", f"https://{PI_DOMAIN}"]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    f"https://{PI_DOMAIN}",
]

# Application definition

INSTALLED_APPS = [
    # "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "authentication_app",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "django_otp",  # 2FA
    "django_otp.plugins.otp_totp",  # 2FA
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
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
                # Needed for allauth
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
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PWD_MODULE = "django.contrib.auth.password_validation."

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": f"{AUTH_PWD_MODULE}UserAttributeSimilarityValidator",
    },
    {
        "NAME": f"{AUTH_PWD_MODULE}MinimumLengthValidator",
    },
    {
        "NAME": f"{AUTH_PWD_MODULE}CommonPasswordValidator",
    },
    {
        "NAME": f"{AUTH_PWD_MODULE}NumericPasswordValidator",
    },
]

# AUTH_USER_MODEL = "user_management_app.Player"


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

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
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
]


class HealthCheckFilter(logging.Filter):
    def filter(self, record):
        return "/health/" not in record.getMessage()


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
