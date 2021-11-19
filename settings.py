import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'w)a#gfta0hqw@k2!+yl=4t4ltxvm!mj6t_d3beajjd&iyw!9c@'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django_crontab',    # As we want to call API in every 5 min we are using cron tab 
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',    # django rest-framework for creating REST Api
    'api',               # microservice for fetching youtube api
    'django_filters',    # for applying filter for sorting in reverse chronological order of their publishing date-time
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

ROOT_URLCONF = 'backendTaskFetchYoutubeApi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'backendTaskFetchYoutubeApi.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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


APP_LOG_FILENAME = os.path.join(BASE_DIR,'log/app.log')  # to record the logs from scheduled jobs
ERROR_LOG_FILENAME = os.path.join(BASE_DIR,'log/error.log')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(name)-12s %(levelname)-8s %(message)s',
        },
        'file': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': APP_LOG_FILENAME
        }
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        }
    }
}

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],  # Django filter backend
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',      # Django pagination backend
    'PAGE_SIZE': 10                                                                    # Setting paging size of 10
}


# These jobs run after specfic time
CRONJOBS = [
    ('*/2 * * * *', 'api.cron.callAPI'),           # runs every 2 min (fetch youtube api and record data to the database)
    ('*/5 * * * *', 'api.cron.deleteCache'),       # runs every 5 min and clear the cache (database entery to prevent our database to get overflow)
]

API_KEYS = ['AIzaSyARvQQ64xbZHzhi-lz7i1a1CP8mR7M-KF4']     # list of apiKeys for calling youtube api, a certain api can request for limited number of time so if one doesn;t work then we call api through next key

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
