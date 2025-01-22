from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.config import START_TEXT, HELP_TEXT, ACCEPTED_TEXT, START_BUTTONS, HELP_BUTTONS, START_IMAGE, HELP_IMAGE, ACCEPTED_IMAGE
from app.database import Data


async def start_handler(client: Client, message):
    """Handles the /start command."""
    user_id = message.from_user.id
    if not await Data.find_one({"id": user_id}):
        await Data.insert_one({"id": user_id})
    
    buttons = [[InlineKeyboardButton(**btn) for btn in row] for row in START_BUTTONS]
    await message.reply_photo(
        photo=START_IMAGE,
        caption=START_TEXT.format(user=message.from_user.mention),
        reply_markup=InlineKeyboardMarkup(buttons)
    )


async def callback_handler(client: Client, callback_query):
    """Handles button presses."""
    data = callback_query.data
    if data == "help":
        buttons = [[InlineKeyboardButton(**btn) for btn in row] for row in HELP_BUTTONS]
        await callback_query.message.edit_media(
            media=HELP_IMAGE,
            caption=HELP_TEXT,
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    elif data == "start":
        buttons = [[InlineKeyboardButton(**btn) for btn in row] for row in START_BUTTONS]
        await callback_query.message.edit_media(
            media=START_IMAGE,
            caption=START_TEXT.format(user=callback_query.from_user.mention),
            reply_markup=InlineKeyboardMarkup(buttons)
        )


async def req_accept(client: Client, message):
    """Handles join requests."""
    user_id = message.from_user.id
    chat_id = message.chat.id
    if not await Data.find_one({"id": user_id}):
        await Data.insert_one({"id": user_id})
    
    await client.approve_chat_join_request(chat_id, user_id)
    await client.send_photo(
        chat_id=user_id,
        photo=ACCEPTED_IMAGE,
        caption=ACCEPTED_TEXT.format(user=message.from_user.mention, chat=message.chat.title)
    )