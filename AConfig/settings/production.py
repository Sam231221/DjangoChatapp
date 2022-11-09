from AConfig.base import *

from AConfig.environs import Env

env = Env()
env.read_env()  # read .env file, if it exists

DEBUG = True
SECRET_KEY = env.str("SECRET_KEY")

ALLOWED_HOSTS = ["chitchat129.herokuapp.com",]

# Order matters
MIDDLEWARE = [
    #'django.middleware.cache.UpdateCacheMiddleware',         #Explict middleware
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',             #Explict middleware
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    #'django.middleware.cache.FetchFromCacheMiddleware',      #Explict middleware
    # 'csp.middleware.CSPMiddleware',                           #Explict middleware
]


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}



"""
import dj_database_url
db_from_env=dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)
"""


STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [os.environ.get('REDIS_URL', 'redis://localhost:6379')],
        },
    },
}

CSRF_TRUSTED_ORIGINS = [
    'https://chitchat129.herokuapp.com'
]