from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserIsBlocked, InputUserDeactivated, FloodWait
from motor.motor_asyncio import AsyncIOMotorClient
from os import environ as env
import asyncio

# Environment Variables (Render Deployment)
API_ID = int(env.get("API_ID"))  # Telegram API ID
API_HASH = env.get("API_HASH")  # Telegram API Hash
BOT_TOKEN = env.get("BOT_TOKEN")  # Bot token from BotFather
DB_URL = env.get("DB_URL")  # MongoDB connection URL
ADMINS = [int(admin_id) for admin_id in env.get("ADMINS", "").split()]  # List of Admin user IDs

# Database Setup (MongoDB)
Dbclient = AsyncIOMotorClient(DB_URL)
Cluster = Dbclient["Cluster0"]
Data = Cluster["users"]

# Initialize the Bot
Bot = Client(
    "AutoAcceptBot",  # Optional name (can be removed if unused)
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Start Command
@Bot.on_message(filters.command("start") & filters.private)
async def start_handler(c: Client, m: Message):
    user_id = m.from_user.id
    if not await Data.find_one({"id": user_id}):  # Add user to database if not already present
        await Data.insert_one({"id": user_id})
    buttons = [
        [
            InlineKeyboardButton("Updates", url="https://t.me/mkn_bots_updates"),
            InlineKeyboardButton("Support", url="https://t.me/MKN_BOTZ_DISCUSSION_GROUP"),
        ]
    ]
    await m.reply_text(
        text=f"Welcome {m.from_user.mention}!\n\nI am an Auto Request Accept Bot. Add me to your channel to use my features.",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# Broadcast Command (Admin Only)
@Bot.on_message(filters.private & filters.command('broadcast') & filters.user(ADMINS))
async def broadcast_handler(client: Client, message: Message):
    if not message.reply_to_message:
        return await message.reply("Please use this command as a reply to a message you want to broadcast.")
    
    query = Data.find({})
    broadcast_msg = message.reply_to_message
    total, successful, blocked, deleted, unsuccessful = 0, 0, 0, 0, 0
    pls_wait = await message.reply("<i>Broadcasting Message... This may take some time.</i>")
    
    async for user in query:
        chat_id = user["id"]
        try:
            await broadcast_msg.copy(chat_id)
            successful += 1
        except FloodWait as e:
            await asyncio.sleep(e.x)
            await broadcast_msg.copy(chat_id)
            successful += 1
        except UserIsBlocked:
            await Data.delete_one({"id": chat_id})
            blocked += 1
        except InputUserDeactivated:
            await Data.delete_one({"id": chat_id})
            deleted += 1
        except Exception:
            unsuccessful += 1
        total += 1
    
    status = f"""<b><u>Broadcast Completed</u></b>

<b>Total Users:</b> <code>{total}</code>
<b>Successful:</b> <code>{successful}</code>
<b>Blocked:</b> <code>{blocked}</code>
<b>Deleted:</b> <code>{deleted}</code>
<b>Unsuccessful:</b> <code>{unsuccessful}</code>"""
    await pls_wait.edit(status)

# Auto Accept Join Requests
@Bot.on_chat_join_request()
async def auto_accept(c: Client, m):
    user_id = m.from_user.id
    chat_id = m.chat.id
    if not await Data.find_one({"id": user_id}):
        await Data.insert_one({"id": user_id})
    await c.approve_chat_join_request(chat_id, user_id)
    try:
        await c.send_message(user_id, f"Hi {m.from_user.mention}, your request to join {m.chat.title} has been accepted!")
    except Exception:
        pass

Bot.run()
