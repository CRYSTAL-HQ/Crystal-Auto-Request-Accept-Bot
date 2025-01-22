from aiohttp import web

# Web route for checking the bot's status
async def index(request):
    return web.Response(text="The Telegram bot is running!", content_type="text/html")

def run_webserver():
    app = web.Application()
    app.router.add_get("/", index)
    web.run_app(app, port=int(os.getenv("PORT", 8080)))