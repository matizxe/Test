import asyncio
from info import *
from utils import *
from time import time
from client import User
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_message(filters.text & filters.group & filters.incoming & ~filters.command(["verify", "connect", "id"]))
async def search(bot, message):
    f_sub = await force_sub(bot, message)
    if f_sub == False:
        return
    channels = (await get_group(message.chat.id))["channels"]
    if not channels:
        return
    if message.text.startswith("/"):
        return
    query = message.text
    head = "<u>Here is the results 👇\n\nPowered By </u> <b><I>@Matiz_Techz</I></b>\n\n"
    results = ""
    try:
        for channel in channels:
            async for msg in User.search_messages(chat_id=channel, query=query):
                name = (msg.text or msg.caption).split("\n")[0]
                if name in results:
                    continue
                results += f"<b><I>♻️ {name}\n🔗 {msg.link}</I></b>\n\n"
        if not results:
            msg = await message.reply_text(
                "I couldn't find anything related to your query. Do you want to request this to the admin?",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("🎯 Request To Admin 🎯", callback_data=f"request_{message.from_user.id}")]]
                ),
            )
        else:
            msg = await message.reply_text(text=head + results, disable_web_page_preview=True)
        _time = int(time()) + (15 * 60)
        await save_dlt_message(msg, _time)
    except Exception as e:
        print(e)

@Client.on_callback_query(filters.regex(r"^request"))
async def request(bot, update):
    clicked = update.from_user.id
    try:
        typed = update.message.reply_to_message.from_user.id
    except:
        return await update.message.delete()
    if clicked != typed:
        return await update.answer("That's not for you! 👀", show_alert=True)

    admin = (await get_group(update.message.chat.id))["user_id"]
    query = update.message.reply_to_message.text
    text = f"#RequestFromYourGroup\n\nQuery: {query}"
    await bot.send_message(chat_id=admin, text=text, disable_web_page_preview=True)
    await update.answer("✅ Request Sent To Admin", show_alert=True)
    await update.message.delete(60)
