"""Read .env file"""
import environ
import os.path


env = environ.Env(
    DEBUG=(bool, False),
    DEBUG_SQL=(bool, False),
    ACCESS_TOKEN_LIFETIME_MINUTES=(int, 10),
    REFRESH_TOKEN_LIFETIME_DAYS=(int, 60),
    HTTP_PORT=(int, 8000),
)

if os.path.exists('.env'):
    environ.Env.read_env('.env')
elif os.path.exists('../.env'):
    environ.Env.read_env('../.env')

__all__ = [
    env,
]
