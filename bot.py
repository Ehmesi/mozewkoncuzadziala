import discord
from discord.ext import commands
import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiohttp import web
import asyncio

# === CONFIGURATION ===
CHANNEL_ID = 718948680467742783  # Twój kanał
MESSAGE = "Hello from bot!"  # Zmień na coś odpowiedniego :)
TOKEN = os.environ["TOKEN"]  # Token z Railway env variables

# === BOT SETUP ===
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
bot = commands.Bot(command_prefix="!", intents=intents)

scheduler = AsyncIOScheduler()

async def send_scheduled_message():
    channel = bot.get_channel(CHANNEL_ID)
    if channel is None:
        channel = await bot.fetch_channel(CHANNEL_ID)
    if channel:
        await channel.send(MESSAGE)
    else:
        print("⚠ Channel not found!")

# Serwer HTTP dla Render
async def handle(request):
    return web.Response(text="Bot działa!")

async def start_webserver():
    app = web.Application()
    app.add_routes([web.get('/', handle)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', int(os.environ.get("PORT", 8000)))
    await site.start()

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    scheduler.start()
    asyncio.create_task(start_webserver())

TIMES = [(3, 40), (3, 42), (3, 45), (3, 47), (3, 50), (10, 0)]
for hour, minute in TIMES:
    scheduler.add_job(send_scheduled_message, "cron", hour=hour, minute=minute)

bot.run(TOKEN)
