from info import *
from pyrogram import Client
from subprocess import Popen
import asyncio

User = Client(name="user", session_string=SESSION)
DlBot = Client(name="auto-delete", 
               api_id=API_ID,
               api_hash=API_HASH,           
               bot_token=BOT_TOKEN)

class Bot(Client):   
    def __init__(self):
        super().__init__(   
           "bot",
            api_id=API_ID,
            api_hash=API_HASH,           
            bot_token=BOT_TOKEN,
            plugins={"root": "plugins"})
    
    async def start(self):                        
        await super().start()        
        await User.start()
        Popen("python3 -m utils.delete", shell=True)       
        print("Bot Started 👍🙂")   
        
    async def stop(self, *args):
        await super().stop()

# Check for deletion periodically
async def periodic_check():
    while True:
        Popen("python3 -m utils.delete", shell=True)
        await asyncio.sleep(60)  # Check every minute

if __name__ == "__main__":
    bot = Bot()
    
    loop = asyncio.get_event_loop()
    loop.create_task(bot.start())
    loop.create_task(periodic_check())
    loop.run_forever()
