import asyncio
import logging
import sys
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.utils.i18n import FSMI18nMiddleware

from app.bot.dispatcher import TOKEN
from app.bot.handlers import *


async def main() -> None:
    i18n = I18n(path="locales", default_locale="en", domain="messages")
    middleware = FSMI18nMiddleware(i18n=i18n)
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.update.outer_middleware(middleware)
    await dp.start_polling(bot)


print("Hello world")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

