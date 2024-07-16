from starlette.config import Config
from starlette.datastructures import Secret

try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()

MAIL_USERNAME = config("MAIL_USERNAME", cast = Secret)

MAIL_PASSWORD = config("MAIL_PASSWORD", cast = Secret)

MAIL_FROM = config("MAIL_FROM", cast = Secret)

MAIL_PORT = config("MAIL_PORT", cast = int)

MAIL_SERVER = config("MAIL_SERVER", cast = Secret)

MAIL_FROM_NAME = config("MAIL_FROM_NAME", cast = Secret)