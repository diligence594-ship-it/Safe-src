# safe_repo

import asyncio
import importlib
import os
import threading

import pyrogram.utils
from pyrogram import idle
from flask import Flask

from safe_repo.modules import ALL_MODULES
from aiojobs import create_scheduler
from safe_repo.core.mongo.plans_db import check_and_remove_expired_users

pyrogram.utils.MIN_CHANNEL_ID = -1009999999999


# =========================
# WEB SERVER FOR RENDER
# =========================

web = Flask(__name__)


@web.route("/")
def home():
    return "Safe Repo Bot is Running!"


@web.route("/health")
def health():
    return "OK"


def run_web_server():
    port = int(os.getenv("PORT", "10000"))

    print(f"Web server starting on port {port}")

    web.run(
        host="0.0.0.0",
        port=port,
        debug=False,
        use_reloader=False
    )


# =========================
# EXPIRY CHECK
# =========================

async def schedule_expiry_check():
    scheduler = await create_scheduler()

    while True:
        try:
            await scheduler.spawn(
                check_and_remove_expired_users()
            )
        except Exception as e:
            print(f"Expiry check error: {e}")

        await asyncio.sleep(3600)


# =========================
# BOT START
# =========================

async def safe_repo_boot():

    print("Loading bot modules...")

    for all_module in ALL_MODULES:
        print(f"Loading module: {all_module}")

        try:
            importlib.import_module(
                "safe_repo.modules." + all_module
            )
        except Exception as e:
            print(
                f"ERROR loading module {all_module}: {e}"
            )

    print("All modules loaded!")
    print("»»»» ʙᴏᴛ ᴅᴇᴘʟᴏʏ sᴜᴄᴄᴇssғᴜʟʟʏ ✨ 🎉")

    asyncio.create_task(
        schedule_expiry_check()
    )

    print("Bot is now waiting for messages...")

    await idle()

    print(
        "»» ɢᴏᴏᴅ ʙʏᴇ ! sᴛᴏᴘᴘɪɴɢ ʙᴏᴛ."
    )


# =========================
# START
# =========================

if __name__ == "__main__":

    # Render health server
    threading.Thread(
        target=run_web_server,
        daemon=True
    ).start()

    # Use existing event loop
    loop = asyncio.get_event_loop()

    loop.run_until_complete(
        safe_repo_boot()
        )
