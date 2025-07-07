import os
import discord
import asyncio
import requests
from discord.ext import tasks, commands
from pymongo import MongoClient
from utils.alert_builder import build_alert_embed
from utils.token_filter import is_strong_token
from utils.update_checker import check_for_updates
from utils.cleanup import clean_old_tokens
from keep_alive import keep_alive

# Secrets from Render
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))
MONGO_URI = os.getenv("MONGODB_URI")
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
    clean_stale.start()

@tasks.loop(seconds=30)
async def scan_tokens():
    try:
        response = requests.get(f"{DEX_API_URL}/solana")
        data = response.json().get("pairs", [])
        for token in data[:10]:
            address = token['pairAddress']
            if collection.find_one({"address": address}):
                continue

            if not is_strong_token(token):
                continue

            embed = build_alert_embed(token)
            channel = bot.get_channel(CHANNEL_ID)
            await channel.send(embed=embed)

            collection.insert_one({
                "address": address,
                "cap": float(token.get("fdv", 0)),
                "created_at": token.get("pairCreatedAt", 0),
                "last_updated": token.get("pairCreatedAt", 0),
                "update_count": 0
            })
    except Exception as e:
        print("Error in scan_tokens:", e)

@tasks.loop(seconds=60)
async def check_updates():
    await check_for_updates(bot, collection, CHANNEL_ID)

@tasks.loop(minutes=5)
async def clean_stale():
    clean_old_tokens(collection)

keep_alive()
bot.run(TOKEN)
