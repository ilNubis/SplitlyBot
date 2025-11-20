from aiogram import Bot, Dispatcher, types, filters
from custom_aioutils.filters import UserLeftChat, UserJoinChat
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


@dp.message(UserLeftChat(bot.id))
async def send_welcome(message: types.Message):

    """

    This handler will be called when user sends `/start` command

    """
    print("Rip")
    #await message.reply("Hi!\nI'm SplitBot!")

# Dentro il gruppo starta da solo
@dp.message(UserJoinChat(bot.id))
async def join_group(message: types.Message):
    await message.reply("Test")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(dp.start_polling(bot))
