# Discord Coin Alert Bot 💰🚨

A powerful, real-time Discord bot that tracks new meme coins on Solana from Pump.fun and DEX Screener.

## ⚙️ Features

- Alerts on trending Solana tokens in real-time
- Updates when market cap grows (e.g., 1.5x or more)
- Clean, premium-style embeds
- Smart filtering logic (volume, liquidity, snipers, etc.)
- MongoDB tracking to avoid duplicate alerts
- Render-compatible Flask server for 24/7 uptime

## 🛠 Secrets to Set in Render

| Key                   | Description                         |
|------------------------|-------------------------------------|
| DISCORD_BOT_TOKEN      | From Discord Developer Portal       |
| DISCORD_CHANNEL_ID     | Channel ID for posting alerts       |
| MONGODB_URI            | MongoDB Atlas URI                   |
| PORT                   | `8080` (Always for Flask on Render) |
| COINGECKO_API_KEY      | Optional (for future price logic)   |
| DEX_SCREENER_URL       | `https://api.dexscreener.com/latest/dex/pairs/solana/` |
| PUMPFUN_API_URL        | `https://pump.fun/api/trending`     |
| TRADINGVIEW_API_URL    | Placeholder or real TradingView API |

## 🚀 Deploy on Render

1. Fork or clone this repo.
2. Go to [Render](https://render.com) → Create New Web Service.
3. Connect this GitHub repo.
4. Set `Start Command` to:
