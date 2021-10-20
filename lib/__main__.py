from lib.tg_stream import app
from pyrogram import Client, idle
from lib.config import API_HASH, API_ID, BOT_TOKEN
from lib.tg_stream import call_py

bot = Client(
    ":memory:",
    API_ID,
    API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="lib.driver"),
)

bot.start()
app.start()
call_py.start()
idle()
