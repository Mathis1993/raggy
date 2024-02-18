import environ
import os


env = environ.Env(
    DEBUG=(bool, False)
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

DEBUG = env('DEBUG')

SECRET_KEY = env('SECRET_KEY')

DATABASES = {
    'default': env.db(),
}

# CACHES = {
#     'default': env.cache(),
#     'redis': env.cache_url('REDIS_URL')
# }

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = env.str('MEDIA_URL', default='media/')
STATIC_URL = env.str('STATIC_URL', default='static/')


WSGI_APPLICATION = "config.wsgi.application"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

ROOT_URLCONF = "config.urls"

TEST_USER_PASSWORD = "password1"