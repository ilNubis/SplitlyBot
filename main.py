from aiogram import Bot, Dispatcher, types, filters
from custom_aioutils.filters import UserLeftChat, UserJoinChat
from utils import JDataStore, LanguageManager
from dotenv import load_dotenv
import logging
import asyncio
import sys
import os

load_dotenv()

API_TOKEN: str | None = os.getenv("BOT_TOKEN")
print(API_TOKEN)

# Configure logging
logging.basicConfig(level=logging.INFO)


# Initialize bot and dispatcher
assert API_TOKEN != "{YOUR_TOKEN}" and isinstance(API_TOKEN, str), "ERRORE: TOKEN invalido, non sai dove si prende? Guarda dentro 'Project setup.md'"


lang_manager: LanguageManager = LanguageManager("lang")

users_id_data: JDataStore = JDataStore("data/users.json", {
    int: {
        "name"    : str,
        "language": str,
        "groups": [int],
    }
})

groups_id_data: JDataStore = JDataStore("data/groups.json", {
    int: {
        "name": str,
        "total-cost": int,
        "total-users": int,
        "events": [{
            "title": str,
            "date": int,
            "reason": str,
            "request-from": int,
            "cost": int
        }]
    }
})

bot: Bot = Bot(token=API_TOKEN) 
dp: Dispatcher = Dispatcher()


@dp.message(UserLeftChat(bot.id))
async def send_welcome(message: types.Message):
    print("Rip")
    #await message.reply("Hi!\nI'm SplitBot!")


# Dentro il gruppo starta da solo
@dp.message(UserJoinChat(bot.id))
async def join_group(message: types.Message):
    await message.reply("Test")


@dp.message(filters.Command("start"))
async def private_start(message: types.Message):
    language_pack: JDataStore = lang_manager[message.from_user.language_code]

    print(message.chat.type)
    if message.chat.type == "private":
        await message.reply(language_pack["start-priv"])

        


@dp.message()
async def foo(message: types.Message):
    await message.reply(lang_manager["it"]["hello"])

if __name__ == '__main__':


    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(dp.start_polling(bot))
