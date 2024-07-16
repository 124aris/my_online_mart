from fastapi_mail import ConnectionConfig
from app import settings

configuration = ConnectionConfig(
    MAIL_USERNAME = str(settings.MAIL_USERNAME),
    MAIL_PASSWORD = str(settings.MAIL_PASSWORD),
    MAIL_FROM = str(settings.MAIL_FROM),
    MAIL_PORT = settings.MAIL_PORT,
    MAIL_SERVER = str(settings.MAIL_SERVER),
    MAIL_FROM_NAME = str(settings.MAIL_FROM_NAME),
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)