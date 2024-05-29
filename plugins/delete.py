from pyrogram import Client, filters
from pyrogram.types import Message
from info import ADMIN
import re
from datetime import datetime, timedelta

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
        days=time_params["years"] * 365 + time_params["months"] * 30 + time_params["weeks"] * 7 + time_params["days"],
        hours=time_params["hours"],
        minutes=time_params["minutes"]
    )

@Client.on_message(filters.command("delete") & (filters.user(ADMIN) | filters.group))
async def delete_messages(client: Client, message: Message):
    if message.chat.type not in ["group", "supergroup"]:
        await message.reply_text("This command can only be used in groups.")
        return

    if not message.from_user:
        return

    user_status = await client.get_chat_member(message.chat.id, message.from_user.id)
    if user_status.status not in ["administrator", "creator"] and message.from_user.id != ADMIN:
        await message.reply_text("You need to be a group admin or bot admin to use this command.")
        return

    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.reply_text("Usage: /delete <time>")
        return

    time_str = args[1]
    time_delta = parse_time(time_str)

    if not time_delta:
        await message.reply_text("Invalid time format. Use /delete 1yrs 2mon 4wks 4day 1hrs 3min")
        return

    deletion_time = datetime.now() + time_delta

    # Store deletion schedule in your database here, using `message.chat.id` and `deletion_time`

    await message.reply_text(f"Messages will be deleted after {time_str} from now.")

    # Add code to perform the actual message deletion as per your requirements
