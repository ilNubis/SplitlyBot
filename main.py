from aiogram import Bot, Dispatcher, types, filters
from dotenv import load_dotenv
import logging
import asyncio
import sys
import os

load_dotenv()

API_TOKEN: str = os.getenv("BOT_TOKEN")

# Configure logging
logging.basicConfig(level=logging.INFO)


# Initialize bot and dispatcher
bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher()


@dp.message(filters.Command("start"))
async def send_welcome(message: types.Message):

    """

    This handler will be called when user sends `/start` command

    """

    await message.reply("Hi!\nI'm SplitBot!")



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(dp.start_polling(bot))
