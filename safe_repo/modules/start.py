from pyrogram import filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ForceReply
from pyrogram.errors import UserAlreadyParticipant, InviteHashInvalid, InviteHashExpired, FloodWait
from safe_repo import app
from safe_repo.core import script
from safe_repo.core.func import subscribe
from config import OWNER_ID

# ------------------- Start-Buttons ------------------- #

buttons = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("Join Channel", url="https://t.me/safe_repo")],
        [
            InlineKeyboardButton("Buy Premium", url="https://t.me/safe_repo_bot"),
            InlineKeyboardButton("Polo 🤖", callback_data="polo_join")
        ]
    ]
)

@app.on_message(filters.command("start"))
async def start(_, message):
    join = await subscribe(_, message)
    if join == 1:
        return
    await message.reply_text(
        text=script.START_TXT.format(message.from_user.mention), 
        reply_markup=buttons
    )

# ------------------- Polo Button Callback ------------------- #

@app.on_callback_query(filters.regex("^polo_join$"))
async def polo_callback(_, query: CallbackQuery):
    await query.answer()
    await query.message.reply_text(
        "🔗 **Please send the group/channel link or username to join:**",
        reply_markup=ForceReply(selective=True)
    )

# ------------------- Handle Join Request Link ------------------- #

@app.on_message(filters.private & (filters.regex(r"t\.me/") | filters.regex(r"^@?\w+")))
async def process_join_link(client, message):
    # Ignore bot commands
    if message.text.startswith("/"):
        return

    raw_link = message.text.strip()
    
    # Cleaning the link to extract username or invite hash
    if "joinchat/" in raw_link or "+" in raw_link:
        invite_arg = raw_link.split("/")[-1].replace("+", "")
    elif "t.me/" in raw_link:
        invite_arg = raw_link.split("/")[-1].replace("@", "")
    else:
        invite_arg = raw_link.replace("@", "")

    status_msg = await message.reply_text("🔄 **Joining chat...**")

    try:
        # Pass the extracted username/hash directly as a string
        chat = await client.join_chat(str(invite_arg))
        chat_title = getattr(chat, "title", "Group/Channel")
        chat_id = getattr(chat, "id", "N/A")
        
        await status_msg.edit_text(
            f"✅ **Successfully Joined!**\n\n"
            f"📌 **Title:** `{chat_title}`\n"
            f"🆔 **ID:** `{chat_id}`"
        )

    except UserAlreadyParticipant:
        await status_msg.edit_text("⚠️ **Already a member of this chat.**")
    except (InviteHashInvalid, InviteHashExpired):
        await status_msg.edit_text("❌ **Invalid or Expired Invite Link/Username.**")
    except FloodWait as e:
        await status_msg.edit_text(f"⏳ **Telegram Rate Limit:** Wait `{e.value}` seconds.")
    except Exception as e:
        await status_msg.edit_text(f"❌ **Error:** `{str(e)}`")
