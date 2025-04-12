from decouple import config
from datetime import timedelta
from .throttling import throttle_classes

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

    
    'DEFAULT_THROTTLE_CLASSES': throttle_classes['DEFAULT_THROTTLE_CLASSES'],
    'DEFAULT_THROTTLE_RATES': throttle_classes['DEFAULT_THROTTLE_RATES'],
}