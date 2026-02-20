import os
import dj_database_url
from pathlib import Path

import os
from pathlib import Path
from dotenv import load_dotenv # Add this import
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent
# This loads the variables from .env if the file exists
load_dotenv(os.path.join(BASE_DIR, '.env'))

# Now you can use os.environ.get() safely
SECRET_KEY = os.environ.get('SECRET_KEY', 'default-unsafe-key')
# Build paths inside the project


# SECURITY WARNING: keep the secret key used in production secret
# DEBUG should be True locally and False on Render
DEBUG = 'RENDER' not in os.environ

# Allow local connections and your future Render URL
ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    "daphne",
    "channels",
    "accounts",
    "chat",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Added for static files on Render
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
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

ASGI_APPLICATION = "config.asgi.application"
WSGI_APPLICATION = 'config.wsgi.application'

# Database Configuration
# Uses PostgreSQL on Render (via DATABASE_URL variable) and SQLite locally
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600
    )
}

# Channel Layers (WebSockets)
# Uses Redis on Render and InMemory locally
if 'REDIS_URL' in os.environ:
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [os.environ.get('REDIS_URL')],
            },
        },
    }
else:
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels.layers.InMemoryChannelLayer",
        }
    }

# Auth Settings
AUTH_USER_MODEL = "accounts.User"
LOGIN_REDIRECT_URL = 'user_list'
LOGOUT_REDIRECT_URL = 'login'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
# This allows WhiteNoise to compress static files for faster loading
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CSRF Settings for Render
CSRF_TRUSTED_ORIGINS = ['https://*.onrender.com']