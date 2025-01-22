from pyrogram import Client
from threading import Thread
from app.handlers import start_handler, callback_handler, req_accept
from app.webserver import run_webserver
from os import environ as env

API_ID = int(env.get("API_ID"))
API_HASH = env.get("API_HASH")
BOT_TOKEN = env.get("BOT_TOKEN")

# Initialize the bot
Bot = Client(
    name="AutoAcceptBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Add handlers
Bot.add_handler(filters.command("start") & filters.private, start_handler)
Bot.add_handler(filters.callback_query, callback_handler)
Bot.add_handler(filters.chat_join_request, req_accept)

if __name__ == "__main__":
    # Start the web server in a separate thread
    Thread(target=run_webserver).start()
    
    # Run the bot
    Bot.run()