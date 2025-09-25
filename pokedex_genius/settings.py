# ============================================================
# DEBUG OVERRIDE FOR HEROKU
# ============================================================
import os
if os.getenv("HEROKU_DEBUG", "") == "1":
    DEBUG = True
    print("⚠️ HEROKU_DEBUG=1: DEBUG MODE IS ENABLED ON HEROKU ⚠️")


from pathlib import Path
import environ

# ============================================================
# PATHS & ENVIRONMENT
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


# ============================================================
# SECURITY
# ============================================================

SECRET_KEY = env('SECRET_KEY')
DEBUG = env.bool('DEBUG', default=False)

ALLOWED_HOSTS = [
    'pokedex-genius-9617911b5f35.herokuapp.com',
    '127.0.0.1',
    'localhost',
]

X_FRAME_OPTIONS = 'SAMEORIGIN'


# ============================================================
# APPLICATION DEFINITION
# ============================================================

INSTALLED_APPS = [
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',

    # Third-party apps
    'django_extensions',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'crispy_forms',
    'crispy_bootstrap5',
    'widget_tweaks',

    # Local apps
    'users',
    'pokedex',
    'core',
]

SITE_ID = 1
AUTH_USER_MODEL = 'users.pokedexUser'

LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'


# ============================================================
# AUTHENTICATION / DJANGO-ALLAUTH
# ============================================================

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

ACCOUNT_FORMS = {}
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True
ACCOUNT_EMAIL_VERIFICATION = 'none'


# ============================================================
# EMAIL
# ============================================================

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# ============================================================
# MIDDLEWARE
# ============================================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]


# ============================================================
# URLS & WSGI
# ============================================================

ROOT_URLCONF = 'pokedex_genius.urls'
WSGI_APPLICATION = 'pokedex_genius.wsgi.application'


# ============================================================
# TEMPLATES
# ============================================================

TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'pokedex.context_processors.user_pokedexes',
            ],
        },
    },
]


# ============================================================
# DATABASE
# ============================================================

DATABASES = {
    'default': env.db(),
}


# ============================================================
# PASSWORD VALIDATION
# ============================================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ============================================================
# INTERNATIONALIZATION
# ============================================================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# ============================================================
# STATIC & MEDIA FILES
# ============================================================

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# ============================================================
# DJANGO CRISPY FORMS
# ============================================================

CRISPY_ALLOWED_TEMPLATE_PACKS = ['bootstrap5']
CRISPY_TEMPLATE_PACK = 'bootstrap5'


# ============================================================
# MESSAGES
# ============================================================

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'


# ============================================================
# DEFAULT PRIMARY KEY FIELD TYPE
# ============================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



import sys

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": True,
        },
        "django.template": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}
