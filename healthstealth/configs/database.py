from decouple import config
from datetime import timedelta
from pathlib import Path

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

is_production = config("ISPRODUCTION", default=False, cast=bool)
BASE_DIR = Path(__file__).resolve().parent.parent

if not is_production:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": config("DATABASE_NAME"),
            "USER": config("DATABASE_USER"),
            "PASSWORD": config("DATABASE_PASSWORD"),
            "HOST": config("DATABASE_HOST"),
            "PORT": config("DATABASE_PORT"),
        }
    }
