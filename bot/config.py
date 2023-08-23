import os

from environ import environ
from simpy.settings import BASE_DIR


env = environ.Env(
    DEBUG=(bool, False)
)
env.read_env(os.path.join(BASE_DIR, '.env'))

# Telegram bot API
TELEGRAM_BOT_API_KEY = env('TELEGRAM_BOT_API_KEY')