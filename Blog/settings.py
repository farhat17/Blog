"""
Django settings for Blog project.

Generated by 'django-admin startproject' using Django 4.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-x)#ex5=i0bwr61(%x#nu%25^b$1^m&qhbgt!2zx8yldf)gv3q3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['192.168.20.7']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myblogs',
     'tinymce',
    #  'crispy_forms',
     
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
]

# Use a session engine if not already configured
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

ROOT_URLCONF = 'Blog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR,'templates'],
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
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'myblog',
        'USER': 'root',
        'PASSWORD': '123',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'), 
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') 


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

CRISPY_TEMPLATE_PACK = 'bootstrap4'
# TINYMCE_JS_URL = 'https://cdn.tiny.cloud/1/no-api-key/tinymce/7/tinymce.min.js'
# TINYMCE_COMPRESSOR = False


TINYMCE_DEFAULT_CONFIG = {
    'height': 400,
    'width': '100%',
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 20,
    'selector': 'textarea',
    'plugins': '''
        textpattern advlist autolink lists link image charmap print preview hr anchor
        searchreplace wordcount visualblocks visualchars code fullscreen insertdatetime media nonbreaking
        table emoticons template paste help
    ''',
    'toolbar': '''
        undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify |
        bullist numlist outdent indent | link image | charmap | preview code | forecolor backcolor
    ''',
    'content_css': '/path/to/your/custom.css', 
}



LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # Don't disable existing loggers

    'handlers': {
        'file': {
            'level': 'DEBUG',  # Capture all levels from DEBUG and above
            'class': 'logging.FileHandler',
            'filename': 'django_output.log',  # Path to the log file for regular output logs
        },
        'error_file': {
            'level': 'ERROR',  # Capture only ERROR and CRITICAL logs
            'class': 'logging.FileHandler',
            'filename': 'django_error.log',  # Path to the log file for error logs
        },
    },

    'loggers': {
        'django': {
            'handlers': ['file', 'error_file'],  # Send logs to both files
            'level': 'DEBUG',  # Capture all logs from DEBUG and above
            'propagate': True,
        },
    },
}
