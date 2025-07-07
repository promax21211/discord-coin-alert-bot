import discord

def build_alert_embed(pump, screener):
    symbol = screener.get("baseToken", {}).get("symbol", "???")
    cap = screener.get("fdv", 0)
    volume = screener.get("volume", 0)
    buys = screener.get("txCount", {}).get("buys", 0)
    sells = screener.get("txCount", {}).get("sells", 0)
    holders = screener.get("holders", 0)
    top10_percent = screener.get("topTenHoldersPercent", "N/A")
    address = screener.get("pairAddress")

    embed = discord.Embed(
        title=f"📡 New Token Alert — {symbol}",
        description=f"""
💠 `{symbol}` launched on Pump.fun  
Cap: {cap} | Vol: {volume}  
🅑 {buys} buys | 🅢 {sells} sells  
Top Holders: {holders} | Top 10: {top10_percent}%

📊 [Chart](https://dexscreener.com/solana/{address})  
🔗 [Pump.fun](https://pump.fun/{address})  
👑 [VIP Tools](https://axiom.trade/@promax21)
""",
        color=discord.Color.green()
    )
    return embed
