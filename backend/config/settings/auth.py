from .base import *

CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOW_CREDENTIALS = True
ALLOWED_HOSTS = ["*"]
CSRF_TRUSTED_ORIGINS = env.str("DJANGO_CSRF_TRUSTED_ORIGINS", "").split(",")
CORS_ORIGIN_WHITELIST = env.str("DJANGO_CORS_ORIGIN_WHITELIST", "").split(",")


AUTH_USER_MODEL = "users.User"
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
    {
        "NAME": "users.utils.password_validators.ContainsUppercaseValidator",
    },
    {
        "NAME": "users.utils.password_validators.ContainsLowercaseValidator",
    },
    {
        "NAME": "users.utils.password_validators.SpecialCharacterValidator",
    },
]