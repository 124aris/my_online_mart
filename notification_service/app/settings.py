from starlette.config import Config
from starlette.datastructures import Secret

try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()

#DATABASE_URL = config("DATABASE_URL", cast = Secret)
KAFKA_NOTIFICATION_TOPIC = config("KAFKA_NOTIFICATION_TOPIC", cast = str)
BOOTSTRAP_SERVER = config("BOOTSTRAP_SERVER", cast = str)
KAFKA_CONSUMER_GROUP_ID_FOR_PRODUCT = config("KAFKA_CONSUMER_GROUP_ID_FOR_PRODUCT", cast = str)
#TEST_DATABASE_URL = config("TEST_DATABASE_URL", cast = Secret)
MAIL_USERNAME = config("MAIL_USERNAME", cast = Secret)
MAIL_PASSWORD = config("MAIL_PASSWORD", cast = Secret)
MAIL_FROM = config("MAIL_FROM", cast = Secret)
MAIL_PORT = config("MAIL_PORT", cast = int)
MAIL_SERVER = config("MAIL_SERVER", cast = Secret)
MAIL_FROM_NAME = config("MAIL_FROM_NAME", cast = Secret)