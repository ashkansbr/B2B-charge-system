from .base import *

DEBUG = True


ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DATABASES = {

    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'Tabdeal',
        'HOST': 'localhost',
        'CONN_MAX_AGE': 600,
        'PORT': '5432',
    }
}
