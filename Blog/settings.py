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
import dj_database_url
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', default=os.getenv('SECRET_KEY'))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    'techscape-swlm.onrender.com',
    'localhost',
    '127.0.0.1',
    '192.168.240.42',
    '192.168.177.42',
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
    'cloudinary',
    'cloudinary_storage',
    'django_ckeditor_5',
]
INSTALLED_APPS += ['csp']

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
MIDDLEWARE += ['csp.middleware.CSPMiddleware']


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
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600
    )
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

#CSP HEADS
CSP_DEFAULT_SRC = ("'self'", "https://pagead2.googlesyndication.com")

CSP_SCRIPT_SRC = (
    "'self'",
    "https://pagead2.googlesyndication.com",
    "https://www.googletagservices.com",
    "https://adservice.google.com",
    "'unsafe-inline'"
)

CSP_IMG_SRC = (
    "'self'",
    "https://www.google.com",
    "https://tpc.googlesyndication.com",
    "https://res.cloudinary.com",  # Allow Cloudinary images
    "data:"  # Allow base64 images
)

CSP_FRAME_SRC = (
    "'self'",
    "https://googleads.g.doubleclick.net",
    "https://tpc.googlesyndication.com"
)

CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")
CSP_REPORT_ONLY = True

ADMIN_TOOLS_INDEX_DASHBOARD = 'myapp.dashboard.CustomIndexDashboard'

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

AUTH_USER_MODEL = 'App.Client'

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_5_CONFIGS = {
    "default": {
        "toolbar": [
            "undo", "redo", "|",
            "heading", "|",
            "bold", "italic", "underline", "strikethrough", "|",
            "subscript", "superscript", "|",
            "fontColor", "fontBackgroundColor", "highlight", "|",
            "link", "imageUpload", "mediaEmbed", "blockQuote", "|",
            "bulletedList", "numberedList", "todoList", "|",
            "alignment", "indent", "outdent", "|",
            "insertTable", "horizontalLine", "|",
            "code", "codeBlock", "sourceEditing", "|",
            "findAndReplace", "removeFormat", "|",
            "specialCharacters", "pageBreak", "|",
            "ckbox", "mention"
        ],
        "image": {
            "toolbar": [
                "imageTextAlternative", "imageStyle:full", "imageStyle:side",
                "linkImage", "toggleImageCaption", "resizeImage"
            ],
        },
        "table": {
            "contentToolbar": [
                "tableColumn", "tableRow", "mergeTableCells",
                "tableProperties", "tableCellProperties"
            ],
        },
        "simpleUpload": {
            "uploadUrl": "/ckeditor5/image_upload/",
        },
        "extraPlugins": ["MediaEmbed"],
        "extraAllowedContent": "iframe[*]",
        "mediaEmbed": {
            "previewsInData": True,
            "providers": [
                {
                    "name": "iframe.ly",
                    "url": "https://ckeditor.iframe.ly/api/oembed?url={url}&callback={callback}",
                },
                {
                    "name": "youtube",
                    "url": [
                        "^(https?:)?//(www.)?youtube\\.com/watch",
                        "^(https?:)?//(www.)?youtube\\.com/v/",
                        "^(https?:)?//(www.)?youtu\\.be/"
                    ]
                }
            ],
        },
        "removePlugins": ["Markdown"],
        "allowedContent": True,
    }
}

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
CKEDITOR_5_FILE_UPLOAD_PERMISSION = "staff"
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
EMAIL_PORT = env('EMAIL_PORT', default=os.getenv('EMAIL_PORT'))
EMAIL_USE_TLS =  env.bool('EMAIL_USE_TLS', default=os.getenv('EMAIL_USE_TLS', 'True').lower() == 'true')
EMAIL_HOST_USER =  env('EMAIL_HOST_USER', default=os.getenv('EMAIL_HOST_USER'))
EMAIL_HOST_PASSWORD =  env('EMAIL_HOST_PASSWORD', default=os.getenv('EMAIL_HOST_PASSWORD'))
