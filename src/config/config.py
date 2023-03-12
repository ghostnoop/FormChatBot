import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Config:
    TOKEN = os.environ.get('TOKEN')
    CHANNEL_ID = os.environ.get('CHANNEL_ID')
    CHANNEL_ADMIN_ID = os.environ.get('CHANNEL_ADMIN_ID')

    DB_NAME = os.environ.get('DB_NAME')
    DB_USER = os.environ.get('DB_USER')
    DB_HOST = os.environ.get('DB_HOST')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_PORT = os.environ.get('DB_PORT')


config = Config()
