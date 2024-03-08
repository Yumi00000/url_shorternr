import asyncio
import logging
import sys
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import motor.motor_asyncio
import os
import random
import string

load_dotenv()
API_TOKEN = os.getenv("TELEGRAM_TOKEN")
dp = Dispatcher()
client = motor.motor_asyncio.AsyncIOMotorClient(
    f"mongodb://root:example@{os.environ.get('MOGO_HOST', 'localhost')}:27017/")


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer("Hello! I am a bot that can shorted your url")


@dp.message(Command("my_urls"))
async def my_urls_handler(message: Message) -> None:
    db = client["shortener"]
    url_collection = db["urls"]
    await message.answer('Your shortened')
    user_urls = url_collection.find({'user_id': message.from_user.id})
    async for url_data in user_urls:
        await message.answer(f"{url_data['short_url']}>>> {url_data['long_url']} | {url_data['count']} hits")
    await message.answer("That's all your urls")


@dp.message()
async def url_handler(message: Message) -> None:
    try:

        db = client["shortener"]
        url_collection = db["urls"]
        bot_answer = "invalid url"
        if message.text.startswith('https://' or 'http://'):
            shor_url = ''.join(random.choice(string.ascii_letters + string.digits))

            doc = {'short_url': shor_url, 'long_url': message.text, 'user_id': message.from_user.id}
            await url_collection.insert_one(doc)
            bot_answer = shor_url
        else:
            # long_url = await get_long_url_from_json_file(short_url)
            doc_url = await url_collection.find_one({"short_url": message.text})
            if doc_url is not None:
                long_url = doc_url["long_url"]
                bot_answer = long_url
        await message.answer(bot_answer)

    except TypeError:
        await message.answer("Nice try")


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(API_TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
