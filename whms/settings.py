
"""
Django settings for whms project.

Configured for both local development and Vercel deployment.
"""

from pathlib import Path
import os
from urllib.parse import urlparse, parse_qs, unquote


BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# SECURITY
# ============================================================

# Use an environment variable in production.
# The local fallback allows development to continue normally.
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-local-development-key-change-before-deployment'
)


# Local development defaults to True.
# Vercel production environment should set DEBUG=False.
DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'


# ============================================================
# ALLOWED HOSTS
# ============================================================

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
]


# Vercel hostname.
# Example:
# VERCEL_HOST=your-project.vercel.app
vercel_host = os.environ.get('VERCEL_HOST')

if vercel_host:
    ALLOWED_HOSTS.append(vercel_host)


# Also allow additional hosts through an environment variable.
# Example:
# ALLOWED_HOSTS=example.com,www.example.com
additional_hosts = os.environ.get('ALLOWED_HOSTS')

if additional_hosts:
    ALLOWED_HOSTS.extend(
        host.strip()
        for host in additional_hosts.split(',')
        if host.strip()
    )


# ============================================================
# CSRF
# ============================================================

CSRF_TRUSTED_ORIGINS = []


if vercel_host:
    CSRF_TRUSTED_ORIGINS.append(
        f'https://{vercel_host}'
    )


# Additional trusted origins can be supplied through:
# CSRF_TRUSTED_ORIGINS=https://example.com,https://www.example.com
additional_csrf_origins = os.environ.get(
    'CSRF_TRUSTED_ORIGINS'
)

if additional_csrf_origins:
    CSRF_TRUSTED_ORIGINS.extend(
        origin.strip()
        for origin in additional_csrf_origins.split(',')
        if origin.strip()
    )


# ============================================================
# APPLICATIONS
# ============================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'livestock',
]


# ============================================================
# MIDDLEWARE
# ============================================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',

    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ============================================================
# URL CONFIGURATION
# ============================================================

ROOT_URLCONF = 'whms.urls'


# ============================================================
# TEMPLATES
# ============================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        'DIRS': [
            BASE_DIR / 'templates'
        ],

        'APP_DIRS': True,

        'OPTIONS': {
            'context_processors': [

                'django.template.context_processors.request',

                'django.contrib.auth.context_processors.auth',

                'django.contrib.messages.context_processors.messages',

                'livestock.context_processors.farm_settings',
            ],
        },
    },
]


# ============================================================
# WSGI
# ============================================================

WSGI_APPLICATION = 'whms.wsgi.application'


# ============================================================
# DATABASE
# ============================================================

# Local development:
#   SQLite is used automatically when DATABASE_URL is not set.
#
# Production:
#   PostgreSQL is used automatically when DATABASE_URL is set.
#
# Example DATABASE_URL:
#   postgresql://username:password@hostname:5432/database


DATABASE_URL = os.environ.get('DATABASE_URL')


if DATABASE_URL:

    # Support both:
    # postgres://
    # postgresql://

    if DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace(
            'postgres://',
            'postgresql://',
            1
        )

    parsed_db_url = urlparse(DATABASE_URL)

    database_name = (
        parsed_db_url.path.lstrip('/')
        if parsed_db_url.path
        else ''
    )

    database_user = (
        unquote(parsed_db_url.username)
        if parsed_db_url.username
        else ''
    )

    database_password = (
        unquote(parsed_db_url.password)
        if parsed_db_url.password
        else ''
    )

    database_host = parsed_db_url.hostname or ''

    database_port = (
        str(parsed_db_url.port)
        if parsed_db_url.port
        else '5432'
    )

    database_options = {}

    query_parameters = parse_qs(
        parsed_db_url.query
    )

    if 'sslmode' in query_parameters:
        database_options['sslmode'] = (
            query_parameters['sslmode'][0]
        )

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',

            'NAME': database_name,

            'USER': database_user,

            'PASSWORD': database_password,

            'HOST': database_host,

            'PORT': database_port,

            'OPTIONS': database_options,
        }
    }

else:

    # Local development database.
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',

            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# ============================================================
# PASSWORD VALIDATION
# ============================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
            'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },

    {
        'NAME':
            'django.contrib.auth.password_validation.MinimumLengthValidator',
    },

    {
        'NAME':
            'django.contrib.auth.password_validation.CommonPasswordValidator',
    },

    {
        'NAME':
            'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# ============================================================
# INTERNATIONALIZATION
# ============================================================

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Nairobi'

USE_I18N = True

USE_TZ = True


# ============================================================
# STATIC FILES
# ============================================================

STATIC_URL = 'static/'

STATIC_ROOT = BASE_DIR / 'staticfiles'


# ============================================================
# DEFAULT PRIMARY KEY
# ============================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ============================================================
# AUTHENTICATION
# ============================================================

LOGIN_URL = '/accounts/login/'

LOGIN_REDIRECT_URL = '/'

LOGOUT_REDIRECT_URL = '/accounts/login/'


# ============================================================
# EMAIL
# ============================================================

# Console email is suitable for local development.
# A real email service will be configured later for
# production password-reset emails.

EMAIL_BACKEND = (
    'django.core.mail.backends.console.EmailBackend'
)

DEFAULT_FROM_EMAIL = 'noreply@wahomeherd.local'


# ============================================================
# PRODUCTION SECURITY
# ============================================================

if not DEBUG:

    # Vercel terminates HTTPS before forwarding the request
    # to the Django application.
    SECURE_PROXY_SSL_HEADER = (
        'HTTP_X_FORWARDED_PROTO',
        'https'
    )

    SECURE_SSL_REDIRECT = True

    SESSION_COOKIE_SECURE = True

    CSRF_COOKIE_SECURE = True

    SECURE_BROWSER_XSS_FILTER = True

    SECURE_CONTENT_TYPE_NOSNIFF = True

    X_FRAME_OPTIONS = 'DENY'

