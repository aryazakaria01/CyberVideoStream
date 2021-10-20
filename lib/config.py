import os

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
SESSION_NAME = os.getenv("SESSION_NAME")
USERNAME_BOT = os.getenv("USERNAME_BOT", "YuiiDev_bot")
OWNER_NAME = os.getenv("OWNER_NAME", "Badboyanim")
COMMAND_PREFIXES = os.getenv("COMMAND_PREFIXES", "!")
SUDO_USERS = list(map(int, os.getenv("SUDO_USERS").split()))
