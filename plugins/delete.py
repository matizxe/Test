import re
from pyrogram import Client, filters
from pyrogram.types import Message
from utils.helpers import save_dlt_message
from time import time

async def is_admin(bot, chat_id, user_id):
    member = await bot.get_chat_member(chat_id, user_id)
    return member.status in ["administrator", "creator"]

@Client.on_message(filters.command("delete", prefixes="/") & filters.group)
async def set_delete_time(bot: Client, message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    # Check if the user is an admin of the group or the bot admin
    group = await get_group(chat_id)
    bot_admin_id = ADMIN
    if not (user_id == bot_admin_id or await is_admin(bot, chat_id, user_id)):
        return await message.reply("You don't have the permission to use this command.")

    # Parse the command
    command = message.command
    if len(command) < 2:
        return await message.reply("Usage: /delete <time>")
    
    time_str = " ".join(command[1:])
    time_pattern = r'(?P<years>\d+yrs)?\s*(?P<months>\d+mon)?\s*(?P<weeks>\d+wks)?\s*(?P<days>\d+day)?\s*(?P<hours>\d+hrs)?\s*(?P<minutes>\d+min)?'
    match = re.match(time_pattern, time_str)
    
    if not match:
        return await message.reply("Invalid time format. Use like /delete 1yrs 2mon 4wks 4day 1hrs 3min")

    time_data = match.groupdict()
    time_seconds = 0
    time_seconds += int(time_data['years'][:-3]) * 31536000 if time_data['years'] else 0
    time_seconds += int(time_data['months'][:-3]) * 2592000 if time_data['months'] else 0
    time_seconds += int(time_data['weeks'][:-3]) * 604800 if time_data['weeks'] else 0
    time_seconds += int(time_data['days'][:-3]) * 86400 if time_data['days'] else 0
    time_seconds += int(time_data['hours'][:-3]) * 3600 if time_data['hours'] else 0
    time_seconds += int(time_data['minutes'][:-3]) * 60 if time_data['minutes'] else 0
    
    if time_seconds <= 0:
        return await message.reply("Invalid time duration. Please provide a valid time duration.")

    deletion_time = int(time()) + time_seconds

    await save_dlt_message(chat_id, message.reply_to_message, deletion_time)
    await message.reply(f"Messages will be deleted after {time_str}.")

async def check_up(bot):   
    _time = int(time()) 
    all_data = await get_all_dlt_data(_time)
    for data in all_data:
        try:
           await bot.delete_messages(chat_id=data["chat_id"],
                                     message_ids=data["message_id"])           
        except Exception as e:
           err=data
           err["❌ Error"]=str(e)
           print(err)
    await delete_all_dlt_data(_time)

async def run_check_up():
    async with DlBot as bot: 
        while True:  
           await check_up(bot)
           await asyncio.sleep(1)
    
if __name__=="__main__":   
   asyncio.run(run_check_up())
