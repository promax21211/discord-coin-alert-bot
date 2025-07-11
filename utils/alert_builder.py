import discord
from datetime import datetime

def build_alert_embed(data):
    name = data.get("baseToken", {}).get("name", "Unknown")
    symbol = data.get("baseToken", {}).get("symbol", "???")
    cap = float(data.get("fdv", 0))
    volume = float(data.get("volume", 0))
    buys = data.get("txCount", {}).get("buys", 0)
    sells = data.get("txCount", {}).get("sells", 0)
    address = data.get("pairAddress", "N/A")
    icon = data.get("icon", "")
    price = float(data.get("priceUsd", 0))
    created_at = data.get("pairCreatedAt", 0)
    chart_url = f"https://dexscreener.com/solana/{address}"

    launch_time = (
        datetime.utcfromtimestamp(created_at // 1000).strftime("%Y-%m-%d %H:%M:%S UTC")
        if created_at else "Unknown"
    )

    embed = discord.Embed(
        title=f"🚀 {name} ({symbol})",
        description="**Trending Solana Meme Coin Detected**",
        color=discord.Color.green()
    )

    embed.set_thumbnail(url=icon or "https://cryptologos.cc/logos/solana-sol-logo.png")

    embed.add_field(name="💰 Price", value=f"${price:.6f}", inline=True)
    embed.add_field(name="📊 Market Cap", value=f"${int(cap):,}", inline=True)
    embed.add_field(name="📈 Volume", value=f"${int(volume):,}", inline=True)

    embed.add_field(name="🟢 Buys", value=str(buys), inline=True)
    embed.add_field(name="🔴 Sells", value=str(sells), inline=True)
    embed.add_field(name="📅 Launch Time", value=launch_time, inline=True)

    embed.add_field(name="🔗 Chart", value=f"[View Chart]({chart_url})", inline=False)
    embed.add_field(name="🧬 Token Address", value=f"`{address}`", inline=False)

    embed.set_footer(text="📡 Powered by DEX Screener | Solana Bot")

    return embed
