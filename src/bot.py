import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.fsm.storage.memory import MemoryStorage

from config import config
from db import db
from db.models import User
from misc import bot
from routers import form_router
from routers.form_router import create_form_start
from services.form_services import form_channel_send
from utils import consts

logging.basicConfig(level=logging.INFO)

dp = Dispatcher(storage=MemoryStorage())


# Хэндлер на команду /start
@dp.message(Command(commands=["start"]))
async def cmd_start(message: types.Message, state):
    await User.get_or_create(id=message.from_user.id, nickname=message.from_user.username)

    await message.answer(consts.START_MESSAGE, parse_mode='HTML')
    await create_form_start(message, state)


# Запуск процесса поллинга новых апдейтов
async def main():
    await db.init()
    dp.include_router(form_router.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
