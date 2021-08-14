"""Read .env file"""
import environ
import os.path


env = environ.Env(
    DEBUG=(bool, False),
)

if os.path.exists('.env'):
    environ.Env.read_env('.env')

__all__ = [
    env,
]
