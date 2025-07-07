import discord

def build_alert_embed(data):
    symbol = data.get("baseToken", {}).get("symbol", "???")
    cap = data.get("fdv", 0)
    volume = data.get("volume", 0)
    buys = data.get("txCount", {}).get("buys", 0)
    sells = data.get("txCount", {}).get("sells", 0)
    address = data.get("pairAddress")

    embed = discord.Embed(
        title=f"🚨 New Coin Alert — {symbol}",
        description=f"""
CA: `{address}`  
Cap: ${int(cap):,} | Vol: ${int(volume):,}  
🅑 {buys} Buys | 🅢 {sells} Sells  
Chart: [DEX Screener](https://dexscreener.com/solana/{address})
""",
        color=discord.Color.green()
    )
    return embed
