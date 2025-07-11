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

# Load secrets from Render environment
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))
MONGO_URI = os.getenv("MONGODB_URI")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# MongoDB setup
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
        response = requests.get("https://api.dexscreener.com/token-boosts/latest/v1", timeout=10)

        if response.status_code != 200:
            print(f"❌ DEX Boost API Error: Status {response.status_code}")
            return

        try:
            all_tokens = response.json()  # ✅ FIXED: API returns a list, not a dict
        except Exception as e:
            print("❌ JSON Decode Error:", e)
            print("Raw Response:", response.text[:200])
            return

        solana_tokens = [
            token for token in all_tokens
            if token.get("chainId") == "solana"
            and token.get("baseToken", {}).get("name")
            and is_strong_token(token)
        ]

        for token in solana_tokens[:10]:
            address = token.get('pairAddress')
            if not address or collection.find_one({"address": address}):
                continue

            embed = build_alert_embed(token)
            channel = bot.get_channel(CHANNEL_ID)
            if channel:
                await channel.send(embed=embed)

            collection.insert_one({
                "address": address,
                "cap": float(token.get("fdv", 0)),
                "created_at": token.get("pairCreatedAt", 0),
                "last_updated": token.get("pairCreatedAt", 0),
                "update_count": 0
            })

    except Exception as e:
        print("❌ scan_tokens crashed:", e)

@tasks.loop(seconds=60)
async def check_updates():
    await check_for_updates(bot, collection, CHANNEL_ID)

@tasks.loop(minutes=5)
async def clean_stale():
    clean_old_tokens(collection)

# Keep Flask server alive (Render or Replit)
keep_alive()

# Run the Discord bot
bot.run(TOKEN)
