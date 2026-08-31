# safe_repo
# Note if you are trying to deploy on vps then directly fill values in ("")

from os import getenv

API_ID = int(getenv("API_ID", "22470912"))
API_HASH = getenv("API_HASH", "511be78079ed5d4bd4c967bc7b5ee023")
BOT_TOKEN = getenv("BOT_TOKEN", "")
OWNER_ID = list(map(int, getenv("OWNER_ID", "7678862761").split()))
MONGO_DB = getenv("MONGO_DB", "mongodb+srv://Demo23:Demo23@cluster0.fjar36c.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
LOG_GROUP = getenv("LOG_GROUP", "-1003878357392")
CHANNEL_ID = int(getenv("CHANNEL_ID", "-1003822664020"))
