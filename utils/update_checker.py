import requests
import os
from discord import Embed

DEX_API_URL = os.getenv("DEX_SCREENER_URL")

async def check_for_updates(bot, collection, channel_id):
    try:
        tokens = list(collection.find())
        for token in tokens:
            address = token['address']
            old_cap = float(token.get("cap", 0))

            response = requests.get(f"{DEX_API_URL}/solana/{address}")
            data = response.json().get("pair")
            if not data:
                continue

            new_cap = float(data.get("fdv", 0))
            if new_cap > 1.5 * old_cap:
                embed = Embed(
                    title=f"🎉 Update: {data['baseToken']['symbol']} 1.5x+",
                    description=f"CA: `{address}`\n💹 ${int(old_cap):,} → ${int(new_cap):,}\n[Chart](https://dexscreener.com/solana/{address})",
                    color=0xFFD700
                )
                await bot.get_channel(channel_id).send(embed=embed)

                collection.update_one(
                    {"address": address},
                    {"$set": {
                        "cap": new_cap,
                        "last_updated": data.get("pairCreatedAt", 0)
                    }, "$inc": {"update_count": 1}}
                )
    except Exception as e:
        print("Error in check_updates:", e)
