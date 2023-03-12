import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.fsm.storage.memory import MemoryStorage

from config import config
from db import db
from misc import bot
# from routers import form_router

logging.basicConfig(level=logging.INFO)

dp = Dispatcher(storage=MemoryStorage())


# Хэндлер на команду /start
@dp.message(Command(commands=["start"]))
async def cmd_start(message: types.Message):
    await message.answer("Hello!")


# Запуск процесса поллинга новых апдейтов
async def main():
    # await db.init()
    # dp.include_router(form_router.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
