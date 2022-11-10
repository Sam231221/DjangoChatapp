import os
from pathlib import Path

from .environs import Env

env = Env()
env.read_env()  # read .env file, if it exists


BASE_DIR = Path(__file__).resolve().parent.parent

DEFAULT_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
EXPLICT_APPS = [
    # 'django.contrib.sites',

    "MAuthentication.apps.MAuthenticationConfig",
        "MCore.apps.MCoreConfig",
    'MChat.apps.MChatConfig',
]
THIRDPARTY_PLUGIN = [
    'channels',
    'whitenoise',
    'social_django'
]


AUTH_USER_MODEL = "MAuthentication.User"

ROOT_URLCONF = "AConfig.urls"
INSTALLED_APPS = DEFAULT_APPS + EXPLICT_APPS + THIRDPARTY_PLUGIN

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "MAuthentication.context_processors.forms",
                
                'social_django.context_processors.backends',  # <-- Here
                'social_django.context_processors.login_redirect',  # <-- Here
            ],
        },
    },
]

WSGI_APPLICATION = 'AConfig.wsgi.application'
ASGI_APPLICATION = 'AConfig.routing.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


AUTHENTICATION_BACKENDS = (
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_FACEBOOK_KEY = '605352750442305'
SOCIAL_AUTH_FACEBOOK_SECRET = '9b701b2223914aeda73111b89cc295c4'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '848686387472-1cmojobb1oqs50591bglb73fc9rbac6e.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'FYOLzOHwhZv_GkDONcoYN3nQ'


LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = "/accounts/login/"


# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kathmandu"
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = "/staticfiles/"

STATICFILES_DIRS = [os.path.join(BASE_DIR, "staticfiles")]

STATIC_ROOT = os.path.join(BASE_DIR, "static")
MEDIA_ROOT = os.path.join(BASE_DIR, "staticfiles/mediafiles")
MEDIA_URL = "/mediafiles/"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"



'''
LOGIN_URL='accounts/login'
LOGIN_REDIRECT_URL='home'
LOGOUT_URL='accounts/logout'
LOGOUT_REDIRECT_URL='accounts/login'
'''

# SMTP CONFIGURATION
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587

EMAIL_HOST_USER = env.str("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD")
GOOGLE_RECAPTCHA_SECRET_KEY = env.str("GOOGLE_RECAPTCHA_SECRET_KEY")
