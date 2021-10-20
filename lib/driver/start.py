"""
tg-stream-video, An Telegram Bot Project
Copyright (c) 2021 GalihMrd <https://github.com/Imszy17>
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.
You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>
"""

from time import time
from datetime import datetime
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram import Client, filters
from lib.config import USERNAME_BOT
from lib.helpers.decorators import sudo_users_only
from lib.helpers.filters import command


START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ("week", 60 * 60 * 24 * 7),
    ("days", 60 * 60 * 24),
    ("h", 60 * 60),
    ("m", 60),
    ("s", 1)
)

async def _human_time_duration(seconds):
    if seconds == 0:
        return 'inf'
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append('{} {}{}'
                         .format(amount, unit, "" if amount == 1 else "s"))
    return ', '.join(parts)


BOKEP = "https://telegra.ph/file/1e78b509a59fe6c04362a.mp4"


@Client.on_message(
    command(["start", f"start@{USERNAME_BOT}"]) & filters.private & ~filters.edited
)
async def start_(client, message):
    coli = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("📚 Commands", callback_data="cbcmds"),
            ]
        ]
    )
    await client.send_video(message.chat.id, BOKEP, caption=START_MESSAGE, reply_markup=coli)


@Client.on_message(command(["start", f"start@{USERNAME_BOT}"]) & filters.group & ~filters.edited)
async def start(client, message):
    START_MESSAGE = f"""✨ **Welcome {message.from_user.mention} !**

    ❍ I'm online and ready for playing video on your Group video chat.

    ❍ To see all my **feature list and the information**, Click on the » 📚 **Commands button** below
    """

    START_EWE = f"""✨ **Hello {message.from_user.mention} !**

    ❍ I'm online and ready for playing video on your Group video chat.

    ❍ To see all my **feature list and the information**, Click on the » ❓ **Basic Guide button** below
    """

    asu = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("❓ Basic Guide", callback_data="cbhelp"),
            ]
        ]
    )
    await client.send_video(message.chat.id, BOKEP, caption=START_EWE, reply_markup=asu)


@Client.on_message(filters.command(["uptime", f"uptime@{USERNAME_BOT}"]) & ~filters.edited)
@sudo_users_only
async def get_uptime(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply_text(
        "🥵 **Bot Status:\n"
        f"• **uptime:** `{uptime}`\n"
        f"• **start time:** `{START_TIME_ISO}`"
    )
