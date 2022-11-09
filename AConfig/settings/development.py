from AConfig.base import *

from AConfig.environs import Env

env = Env()
env.read_env()  # read .env file, if it exists

ALLOWED_HOSTS = ["127.0.0.1", "localhost",]
DEBUG = True

SECRET_KEY = env.str("SECRET_KEY")


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

"""
#POSTGRES DATABASE
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env.str("DATABASE_NAME"),  
        'USER': env.str("DATABASE_USER"),    
        'PASSWORD': env.str("DATABASE_PASSWORD"),  
        'HOST': env.str("DATABASE_HOST"),
        'PORT': env.str("DATABASE_PORT"),
    }
}

"""


CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
        # 'CONFIG': {
        #     'hosts': [('127.0.0.1', 6379)],
        # }
    }
}