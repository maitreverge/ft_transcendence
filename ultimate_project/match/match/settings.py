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

NAME = os.getenv("name")

PI_DOMAIN = os.getenv("pi_domain")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-\
    8to7%ajqsxrgsbr5asn@mzimmxx9-t^4&356adt680x(v^34kt"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("env", "prod") != "prod"

ALLOWED_HOSTS = ["*", f"{PI_DOMAIN}"]

CSRF_TRUSTED_ORIGINS = [
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
    "channels",
    f"{NAME}_app",
    # f"{NAME}_app.services.testapp.TonAppConfig",
]

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
        # Utilise la mémoire pour les messages #! prod: redis
    },
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # ! static files with daphne
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
# ! for static file with daphne

ROOT_URLCONF = f"{NAME}.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": not DEBUG,
        "OPTIONS": {
            "debug": DEBUG,  # ✅ Forcer le rechargement des templates
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

if DEBUG:  # ✅ Forcer le rechargement des templates
    TEMPLATES[0]["OPTIONS"]["loaders"] = [
        "django.template.loaders.filesystem.Loader",
        "django.template.loaders.app_directories.Loader",
    ]

WSGI_APPLICATION = f"{NAME}.wsgi.application"
ASGI_APPLICATION = f"{NAME}.asgi.application"

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('MATCH_POSTGRES_DB'), # Name of the Database
        'USER': os.getenv('MATCH_POSTGRES_USER'), # Username for accessing the database
        'PASSWORD': os.getenv('MATCH_POSTGRES_PASSWORD'), # Password for the database user.
        'HOST': os.getenv('MATCH_POSTGRES_HOST'), # Hostname where the database server is running == compose service == Name of the db
        'PORT': os.getenv('MATCH_POSTGRES_PORT'), # Port number on which the database server is listening.
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.\
            password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.\
            password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.\
            password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.\
            password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

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
