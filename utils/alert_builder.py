import discord
from datetime import datetime, timezone

def build_alert_embed(data):
    name = data.get("baseToken", {}).get("name", "Unknown")
    symbol = data.get("baseToken", {}).get("symbol", "???")
    cap = float(data.get("fdv", 0))
    volume = float(data.get("volume", 0))
    buys = data.get("txCount", {}).get("buys", 0)
    sells = data.get("txCount", {}).get("sells", 0)
    price = float(data.get("priceUsd", 0))
    address = data.get("pairAddress", "N/A")
    icon = data.get("icon", "")
    chart_url = f"https://dexscreener.com/solana/{address}"

    # Launch time formatting
    created_at = data.get("pairCreatedAt", 0)
    if created_at:
        launch_time = datetime.utcfromtimestamp(created_at // 1000).replace(tzinfo=timezone.utc)
        now = datetime.utcnow().replace(tzinfo=timezone.utc)
        age_minutes = int((now - launch_time).total_seconds() // 60)
        launch_str = launch_time.strftime("%Y-%m-%d %H:%M:%S UTC")
        launch_note = "🆕 Just Launched!" if age_minutes <= 60 else f"{age_minutes} mins ago"
    else:
        launch_str = "Unknown"
        launch_note = ""

    # Emojis based on condition
    trending = "🔥" if volume >= 10_000 and buys > sells else ""
    rug_risk = "🛑" if sells > buys * 2 else ""

    # Social links if available
    socials = []
    for field in ["twitter", "telegram", "website", "discord", "youtube", "instagram"]:
        link = data.get("socials", {}).get(field)
        if link:
            socials.append(f"[{field.title()}]({link})")
    social_text = " | ".join(socials) if socials else "Not Detected"

    # Build embed
    embed = discord.Embed(
        title=f"{trending}{rug_risk} {name} ({symbol})",
        description="**Trending Solana Meme Coin Detected**",
        color=discord.Color.orange() if rug_risk else discord.Color.green()
    )

    embed.set_thumbnail(url=icon or "https://cryptologos.cc/logos/solana-sol-logo.png")

    embed.add_field(name="💰 Price", value=f"${price:.6f}", inline=True)
    embed.add_field(name="📊 Market Cap", value=f"${int(cap):,}", inline=True)
    embed.add_field(name="📈 Volume", value=f"${int(volume):,}", inline=True)

    embed.add_field(name="🟢 Buys", value=str(buys), inline=True)
    embed.add_field(name="🔴 Sells", value=str(sells), inline=True)
    embed.add_field(name="⏰ Launched", value=f"{launch_str}\n{launch_note}", inline=True)

    embed.add_field(name="🔗 Chart", value=f"[View on DEX Screener]({chart_url})", inline=False)
    embed.add_field(name="📢 Socials", value=social_text, inline=False)
    embed.add_field(name="🧬 Token Address", value=f"`{address}`", inline=False)

    embed.set_footer(text="📡 Powered by DEX Screener | Solana Bot")
    return embed
