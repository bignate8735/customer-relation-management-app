# settings.py
from decouple import config, UndefinedValueError
import os
from decouple import config
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Helper to get config from decouple or fallback to os.environ
def env(key, default=None, cast=None):
    try:
        # decouple will fail if cast is None and default is also None
        if cast is None:
            return config(key, default=default)
        return config(key, default=default, cast=cast)
    except (UndefinedValueError, TypeError):
        val = os.environ.get(key, default)
        if cast and val is not None:
            return cast(val)
        return val
       
# Now use `env()` everywhere
SECRET_KEY = env('SECRET_KEY')
if not SECRET_KEY:
    raise RuntimeError(" SECRET_KEY is not set. Please define it in your environment or .env file.")

DEBUG = env('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = env('DJANGO_ALLOWED_HOSTS', default='localhost', cast=lambda v: v.split(','))

REQUIRED_DB_KEYS = ['DB_NAME', 'DB_USER', 'DB_PASSWORD']
for key in REQUIRED_DB_KEYS:
    if not env(key):
        raise RuntimeError(f" {key} is not set. Please define it in your environment or .env file.")
    

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST', default='127.0.0.1'),
        'PORT': env('DB_PORT', default='3306', cast=int),
    }
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'website'
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

ROOT_URLCONF = 'CRM.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'CRM.wsgi.application'



# https://docs.djangoproject.com/en/5.2/ref/settings/#databases


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
import os

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

#Redirections
LOGIN_URL = '/login/'

LOGIN_REDIRECT_URL = '/dashboard/'  # or wherever makes sense in your app
#LOGIN_REDIRECT_URL = '/'