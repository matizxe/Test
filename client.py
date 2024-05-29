import asyncio
from pyrogram import Client, idle
from info import API_ID, API_HASH, BOT_TOKEN, SESSION
from plugins import *
from utils.helpers import run_check_up

class Bot(Client):
    def __init__(self):
        super().__init__(
            "DlBot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(root="plugins")
        )

    async def start(self):
        await super().start()
        print("Bot started.")
        asyncio.create_task(run_check_up())

    async def stop(self, *args):
        await super().stop()
        print("Bot stopped.")

if __name__ == "__main__":
    bot = Bot()
    bot.run()
