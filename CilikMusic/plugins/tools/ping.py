#
# Copyright (C) 2021-2022 by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/YukkiMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiMusicBot/blob/master/LICENSE >
#
# All rights reserved.
import asyncio
from random import shuffle
from datetime import datetime

from pyrogram import filters
from pyrogram.types import Message

from config import BANNED_USERS, MUSIC_BOT_NAME, PING_IMG_URL
from strings import get_command
from CilikMusic import app
from CilikMusic.core.call import Cilik
from CilikMusic.utils import bot_sys_stats
from CilikMusic.utils.decorators.language import language

### Commands
PING_COMMAND = get_command("PING_COMMAND")


@app.on_message(
    filters.command(PING_COMMAND)
    & filters.group
    & ~filters.edited
    & ~BANNED_USERS
)
@language
async def ping_com(client, message: Message, _):
    response = await message.reply_photo(
        photo=PING_IMG_URL,
        caption=_["ping_1"],
    )
    start = datetime.now()
    pytgping = await Cilik.ping()
    UP, CPU, RAM, DISK = await bot_sys_stats()
    resp = (datetime.now() - start).microseconds / 1000
    await response.edit_text(
        _["ping_2"].format(
            MUSIC_BOT_NAME, resp, UP, DISK, CPU, RAM, pytgping
        )
    )



   
tagallgcid = []


@app.on_message(
    filters.command(["all", "cancel"], ["/"])
    & filters.group
    & ~filters.edited
    & ~BANNED_USERS
)
async def tagcom(client, message: Message):
    if message.command[0] == "all":
        if message.chat.id in tagallgcid:
            return
        tagallgcid.append(message.chat.id)
        text = message.text.split(None, 1)[1] if len(message.text.split()) != 1 else ""
        users = [
            member.user.mention
            async for member in message.chat.get_members()
            if not (member.user.is_bot or member.user.is_deleted)
        ]
        shuffle(users)
        m = message.reply_to_message or message
        for output in [users[i : i + 5] for i in range(0, len(users), 5)]:
            if message.chat.id not in tagallgcid:
                break
            await asyncio.sleep(1.5)
            await m.reply_text(
                ", ".join(output) + "\n\n" + text, quote=bool(message.reply_to_message)
            )
        try:
            tagallgcid.remove(message.chat.id)
        except Exception:
            pass
    elif message.command[0] == "cancel":
        if message.chat.id not in tagallgcid:
            return await message.reply_text(
                "Tidak ada mentions"
            )
        try:
            tagallgcid.remove(message.chat.id)
        except Exception:
            pass
        await message.reply_text("<b>Stoped.</b>")
