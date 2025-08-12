import discord
from discord.ext import commands
import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler

CHANNEL_ID = 718948680467742783  # zmień na swój
MESSAGE = "nigger!"
TOKEN = os.environ["TOKEN"]

intents = discord.Intents.default()
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

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    scheduler.start()

TIMES = [(3, 0), (3, 10), (3, 15), (3, 20), (3, 30), (10, 0)]
for hour, minute in TIMES:
    scheduler.add_job(send_scheduled_message, "cron", hour=hour, minute=minute)

bot.run(TOKEN)
