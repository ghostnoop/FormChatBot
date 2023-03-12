import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command

from config import config

from aiogram import F, Router, Bot

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.TOKEN)
dp = Dispatcher()




@dp.channel_post()
async def cmd_start(message: types.Message):
    print(message.json())
    print('ewew')


async def main():
    w = await bot.get_me()
    print(w)
    # dp.include_routers(router)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
