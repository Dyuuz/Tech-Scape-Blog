"""
Django settings for Blog project.

Generated by 'django-admin startproject' using Django 5.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
import environ
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', default=os.getenv('SECRET_KEY'))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'techscape-swlm.onrender.com',
    'localhost',
    '127.0.0.1',
    '192.168.76.169',
    '192.168.91.198',
    '192.168.0.169',
    '192.168.52.198',
    '192.168.161.198',
    '192.168.163.198',
]


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'App',
    'cachebuster',
]

# INSTALLED_APPS += ['admin_tools_stats']

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]



ROOT_URLCONF = 'Blog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'Blog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': env('PGS_ENGINE', default=os.getenv('PGS_ENGINE')) ,
        'NAME': env('PGS_NAME', default=os.getenv('PGS_NAME')),      
        'USER': env('PGS_USER', default=os.getenv('PGS_USER')),            
        'PASSWORD':env('PGS_PASSWORD', default=os.getenv('PGS_PASSWORD')) ,   
        'HOST': env('PGS_HOST', default=os.getenv('PGS_HOST')),    
        'PORT': env.int('PGS_PORT', default=os.getenv('PGS_PORT')),
    }
}

JAZZMIN_SETTINGS = {
    "site_title": "Tech Scape",
    "site_header": "Tech Scape Admin",
    "site_brand": "Tech Scape",
    "welcome_sign": "Welcome to Tech Scape",
    "copyright": "Tech Scape",
    "search_model": "auth.User",
    "user_avatar": None,
}

SUIT_CONFIG = {
    'ADMIN_NAME': 'My Custom Admin',
    'SHOW_REQUIRED_ASTERISK': True,
    'CONFIRM_UNSAVED_CHANGES': True,
    'MENU_OPEN_FIRST_CHILD': True,
    'SEARCH_URL': '',
    'LIST_PER_PAGE': 20,
    'MENU': (
        {'label': 'Users', 'icon': 'icon-user', 'models': ('auth.user', 'auth.group')},
        {'label': 'Content Management', 'icon': 'icon-folder-open', 'models': ('App.Category', 'myapp.Blog')},
        {'label': 'Subscriptions', 'icon': 'icon-envelope', 'models': ('App.Newsletter',)},
        {'label': 'Security', 'icon': 'icon-lock', 'models': ('App.PasswordReset',)},
    ),
}

SUIT_CONFIG['DASHBOARD'] = 'App.dashboard.CustomDashboard'

ADMIN_TOOLS_INDEX_DASHBOARD = 'myapp.dashboard.CustomIndexDashboard'

import time
STATIC_VERSION = str(int(time.time()))  # Generates a new version each time the server restarts

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

CACHEBUSTER_URL = '/static/'

AUTH_USER_MODEL = 'App.Client'

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIR = [os.path.join('BASE_DIR', 'App/static'), ]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = 'media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'App/media/')

SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 3600
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'App/cache'),
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' 
EMAIL_HOST =  env('EMAIL_HOST', default=os.getenv('EMAIL_HOST'))
EMAIL_PORT = env.int('EMAIL_PORT', default=int(os.getenv('EMAIL_PORT')))
EMAIL_USE_TLS =  env.bool('EMAIL_USE_TLS', default=os.getenv('EMAIL_USE_TLS', 'True').lower() == 'true')
EMAIL_HOST_USER =  env('EMAIL_HOST_USER', default=os.getenv('EMAIL_HOST_USER'))
EMAIL_HOST_PASSWORD =  env('EMAIL_HOST_PASSWORD', default=os.getenv('EMAIL_HOST_PASSWORD'))