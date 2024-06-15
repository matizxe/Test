from pyrogram import Client, filters, enums
from pyrogram.types import Message
from info import ADMIN
import re
from datetime import datetime, timedelta
from time import time
import asyncio
from utils.helpers import save_dlt_message, get_all_dlt_data, delete_all_dlt_data
from client import DlBot

DELETE_REGEX = r"(\d+yrs)?\s*(\d+mon)?\s*(\d+wks)?\s*(\d+day)?\s*(\d+hrs)?\s*(\d+min)?"


def parse_time(duration: str):
    matches = re.match(DELETE_REGEX, duration)
    if not matches:
        return None
    time_params = {
        "years": int(matches.group(1)[:-3]) if matches.group(1) else 0,
        "months": int(matches.group(2)[:-3]) if matches.group(2) else 0,
        "weeks": int(matches.group(3)[:-3]) if matches.group(3) else 0,
        "days": int(matches.group(4)[:-3]) if matches.group(4) else 0,
        "hours": int(matches.group(5)[:-3]) if matches.group(5) else 0,
        "minutes": int(matches.group(6)[:-3]) if matches.group(6) else 0,
    }
    return timedelta(
        days=time_params["years"] * 365
        + time_params["months"] * 30
        + time_params["weeks"] * 7
        + time_params["days"],
        hours=time_params["hours"],
        minutes=time_params["minutes"],
    )


@Client.on_message(filters.command("delete") & (filters.user(ADMIN) | filters.group))
async def delete_messages(client: Client, message: Message):
    print(
        f"Received /delete command in chat {message.chat.id}, chat type: {message.chat.type}"
    )

    if message.chat.type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        await message.reply_text("This command can only be used in groups.")
        return

    user_status = await client.get_chat_member(message.chat.id, message.from_user.id)
    print(f"User {message.from_user.id} status: {user_status.status}")

    if (
        user_status.status not in ["administrator", "creator"]
        and message.from_user.id != ADMIN
    ):
        await message.reply_text(
            "You need to be a group admin or bot admin to use this command."
        )
        return

    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        text = """How to use this command 👇👇
Follow this... 

min = minutes
hrs = hours
day = days
wks = weeks
mon = months
yrs = years

👉 Ex:- 1day 2hrs 5min [ 1 day and 2 hours and five minutes ]"""
        await message.reply_text(text)
        return

    time_str = args[1]
    time_delta = parse_time(time_str)
    print(f"Parsed time: {time_delta}")

    if not time_delta:
        await message.reply_text(
            "Invalid time format. Use /delete 1yrs 2mon 4wks 4day 1hrs 3min"
        )
        return

    deletion_time = datetime.now() + time_delta

    await save_dlt_message(message.chat.id, message, deletion_time)
    await message.reply_text(f"Messages will be deleted after {time_str} from now.")


async def check_up(bot):
    _time = int(time())
    all_data = await get_all_dlt_data(_time)
    for data in all_data:
        try:
            await bot.delete_messages(
                chat_id=data["chat_id"], message_ids=data["message_id"]
            )
        except Exception as e:
            err = data
            err["❌ Error"] = str(e)
            print(err)
    await delete_all_dlt_data(_time)


async def run_check_up():
    async with DlBot as bot:
        while True:
            await check_up(bot)
            await asyncio.sleep(60)


if __name__ == "__main__":
    asyncio.run(run_check_up())
