from tortoise import Tortoise

from config import config
from db.services import load_fixtures


async def init():
    # Here we connect to a SQLite DB file.
    # also specify the app name of "models"
    # which contain models from "app.models"
    await Tortoise.init(
        db_url=f'asyncpg://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}',
        modules={'models': ['db.models']}
    )
    # Generate the schema
    await Tortoise.generate_schemas()
    await load_fixtures()
