```python
from pyrogram import filters
from safe_repo import app
from safe_repo.core import script
from safe_repo.core.func import subscribe
from config import OWNER_ID
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton


# ------------------- Start-Buttons ------------------- #

buttons = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                "Join Channel",
                url="https://t.me/safe_repo"
            )
        ],
        [
            InlineKeyboardButton(
                "Buy Premium",
                url="https://t.me/safe_repo_bot"
            )
        ]
    ]
)


# ------------------- /start Command ------------------- #

@app.on_message(filters.command("start"))
async def start(_, message):
    join = await subscribe(_, message)

    if join == 1:
        return

    await message.reply_text(
        text=script.START_TXT.format(
            message.from_user.mention
        ),
        reply_markup=buttons
    )


# ------------------- /join Command ------------------- #
# Public groups/channels only
#
# Usage:
# /join https://t.me/username
# /join https://t.me/username/
# /join @username
#
# This uses the bot account itself, so the bot must be
# allowed to join the public chat.


@app.on_message(
    filters.command("join") & filters.private
)
async def join_public_chat(_, message):

    if len(message.command) < 2:
        await message.reply_text(
            "❌ Please send a public group/channel link.\n\n"
            "Example:\n"
            "`/join https://t.me/username`"
        )
        return

    link = message.command[1].strip()

    # Remove trailing slash
    link = link.rstrip("/")

    # Convert @username to username
    if link.startswith("@"):
        username = link[1:]

    elif link.startswith("https://t.me/"):
        username = link.split("https://t.me/", 1)[1].split("/", 1)[0]

    elif link.startswith("http://t.me/"):
        username = link.split("http://t.me/", 1)[1].split("/", 1)[0]

    else:
        await message.reply_text(
            "❌ Invalid public Telegram link.\n\n"
            "Use:\n"
            "`/join https://t.me/username`\n"
            "or\n"
            "`/join @username`"
        )
        return

    # Reject invite/private links
    if (
        not username
        or username.startswith("+")
        or username.startswith("joinchat")
        or "joinchat" in username
    ):
        await message.reply_text(
            "❌ Private invite links are not supported.\n"
            "Please provide a public `t.me/username` link."
        )
        return

    # Basic username validation
    if not username.replace("_", "").isalnum():
        await message.reply_text(
            "❌ Invalid public username."
        )
        return

    status = await message.reply_text(
        "⏳ Trying to join the public chat..."
    )

    try:
        # Resolve the public chat
        chat = await app.get_chat(username)

        # Join public group/channel
        await app.join_chat(chat.id)

        await status.edit_text(
            "✅ Successfully joined!\n\n"
            f"**Chat:** {chat.title or username}\n"
            f"**Username:** @{username}"
        )

    except Exception as e:

        error = str(e)

        # Already joined
        if (
            "USER_ALREADY_PARTICIPANT" in error
            or "USER_ALREADY_IN_CHAT" in error
            or "already a participant" in error.lower()
        ):
            await status.edit_text(
                "ℹ️ Already joined this group/channel.\n\n"
                f"**Chat:** @{username}"
            )
            return

        # Username not found
        if (
            "USERNAME_NOT_OCCUPIED" in error
            or "USERNAME_INVALID" in error
            or "PEER_ID_INVALID" in error
        ):
            await status.edit_text(
                "❌ Public group/channel not found.\n\n"
                f"`@{username}`"
            )
            return

        # Bot cannot join
        if (
            "CHANNELS_TOO_MUCH" in error
            or "CHANNEL_PRIVATE" in error
            or "INVITE_REQUEST_SENT" in error
        ):
            await status.edit_text(
                "❌ The bot could not join this public chat.\n\n"
                f"**Error:** `{error}`"
            )
            return

        await status.edit_text(
            "❌ Failed to join the public chat.\n\n"
            f"**Error:** `{error}`"
        )
```
    
