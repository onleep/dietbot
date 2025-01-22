import logging

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject

logging.basicConfig(format=f'%(asctime)s | %(levelname)s: %(message)s',
                    datefmt=f"%Y-%m-%d %H:%M:%S",
                    level=logging.INFO,
                    filename="dietbot.log",
                    filemode="a")

logging.getLogger('aiogram').setLevel(logging.WARNING)


class LoggingMiddleware(BaseMiddleware):

    async def __call__(self, handler, event: TelegramObject, data: dict):
        if isinstance(event, CallbackQuery):
            if callback := event.data:
                logging.info(f'Получен callback: {callback}')
        elif isinstance(event, Message):
            if message := event.text:
                logging.info(f'Получена команда: {message}')
        return await handler(event, data)
