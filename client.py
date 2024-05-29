from info import *
from pyrogram import Client
from subprocess import Popen
from utils.helpers import (
    add_group, get_group, update_group, delete_group, delete_user, get_groups, add_user,
    get_users, save_dlt_message, get_all_dlt_data, delete_all_dlt_data, search_imdb,
    force_sub, broadcast_messages
)

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

if __name__ == "__main__":
    bot = Bot()
    bot.run()
