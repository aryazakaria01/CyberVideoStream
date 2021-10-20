from pyrogram import Client
from pytgcalls import PyTgCalls
from lib.config import SESSION_NAME, API_ID, API_HASH


app = Client(SESSION_NAME, API_ID, API_HASH)
call_py = PyTgCalls(app)
