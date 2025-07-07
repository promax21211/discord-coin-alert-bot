import os
import discord
import asyncio
import requests
from discord.ext import tasks, commands
from pymongo import MongoClient
from utils.alert_builder import build_alert_embed
from utils.token_filter import is_strong_token
from utils.update_checker import check_for_updates
from keep_alive import keep_alive

# Secrets from Render
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))
MONGO_URI = os.getenv("MONGODB_URI")
PUMP_API_URL = os.getenv("PUMPFUN_API_URL")
DEX_API_URL = os.getenv("DEX_SCREENER_URL")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

mongo = MongoClient(MONGO_URI)
db = mongo['coin_alerts']
collection = db['tokens']

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    scan_tokens.start()
    check_updates.start()

@tasks.loop(seconds=30)
async def scan_tokens():
    try:
        response = requests.get(PUMP_API_URL)
        data = response.json()
        for token in data[:5]:
            address = token['address']
            if collection.find_one({"address": address}):
                continue

            screener = requests.get(f"{DEX_API_URL}{address}").json()
            screener_data = screener.get("pair")
            if not screener_data or not is_strong_token(screener_data):
                continue

            embed = build_alert_embed(token, screener_data)
            channel = bot.get_channel(CHANNEL_ID)
            await channel.send(embed=embed)

            collection.insert_one({
                "address": address,
                "cap": float(screener_data.get("fdv", 0)),
                "timestamp": token.get("launchedAt", 0)
            })
    except Exception as e:
        print("Error in scan_tokens:", e)

@tasks.loop(seconds=60)
async def check_updates():
    await check_for_updates(bot, collection, CHANNEL_ID)

keep_alive()
bot.run(TOKEN)
