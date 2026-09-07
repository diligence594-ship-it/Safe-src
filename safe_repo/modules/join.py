import re
from pyrogram import Client, filters
from pyrogram.errors import (
    UserAlreadyParticipant,
    InviteHashInvalid,
    InviteHashExpired,
    FloodWait,
    ChatAdminRequired
)

@Client.on_message(filters.command("join") & filters.private)
async def join_chat_handler(client: Client, message):
    # Check if link parameter is provided
    if len(message.command) < 2:
        await message.reply_text(
            "❌ **Please provide a join link or username!**\n\n"
            "**Usage:** `/join https://t.me/+AbCdEf12345` or `/join https://t.me/group_username`"
        )
        return

    raw_link = message.command[1].strip()
    
    # Process link to extract hash or username
    if "joinchat/" in raw_link or "+" in raw_link:
        invite_arg = raw_link.split("/")[-1].replace("+", "")
    elif "t.me/" in raw_link:
        invite_arg = raw_link.split("/")[-1]
    else:
        invite_arg = raw_link

    status_msg = await message.reply_text("🔄 **Joining chat...**")

    try:
        chat = await client.join_chat(invite_arg)
        chat_title = getattr(chat, "title", "Private Group/Channel")
        chat_id = getattr(chat, "id", "N/A")
        
        await status_msg.edit_text(
            f"✅ **Successfully Joined!**\n\n"
            f"📌 **Title:** `{chat_title}`\n"
            f"🆔 **ID:** `{chat_id}`"
        )

    except UserAlreadyParticipant:
        await status_msg.edit_text("⚠️ **Already a member of this chat.**")
    except (InviteHashInvalid, InviteHashExpired):
        await status_msg.edit_text("❌ **Invalid or Expired Invite Link.**")
    except FloodWait as e:
        await status_msg.edit_text(f"⏳ **Telegram Rate Limit:** Please wait `{e.value}` seconds.")
    except Exception as e:
        await status_msg.edit_text(f"❌ **Error:** `{str(e)}`")
