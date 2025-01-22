import asyncio

from aiogram import Bot, Dispatcher
from buttons import bot_commands
from dotenv import dotenv_values
from routers.activity import activity
from routers.mainpage import mainpage
from routers.profiles import profiles
from tools.logger import LoggingMiddleware


async def main():
    TG_TOKEN = dotenv_values().get('TG_TOKEN')
    if not TG_TOKEN: return 'TG_TOKEN не указан'

    bot = Bot(token=TG_TOKEN)
    await bot.get_updates(offset=-1)
    commands = await bot.set_my_commands(bot_commands)

    dp = Dispatcher()
    dp.include_router(mainpage)
    dp.include_router(profiles)
    dp.include_router(activity)
    dp.message.middleware(LoggingMiddleware())
    dp.callback_query.middleware(LoggingMiddleware())
    await dp.start_polling(bot, on_startup=commands)


if __name__ == "__main__":
    asyncio.run(main())
