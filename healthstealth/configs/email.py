from decouple import config




EMAIL_BACKEND = config("EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend")
SMTP_HOST = config("SMTP_HOST", default=None)
SMTP_USE_TLS = config("SMTP_USE_TLS", cast=bool, default=False)
SMTP_PORT = config("SMTP_PORT", cast=int, default=None)
SMTP_USERNAME = config("SMTP_USERNAME", default=None)
SMTP_PASSWORD = config("SMTP_PASSWORD", default=None)

if not all([SMTP_HOST, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD]):
    raise ValueError("Missing required SMTP configuration values in the .env file")
