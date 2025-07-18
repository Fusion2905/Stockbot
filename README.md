# 📈 Telegram Stock Bot

A simple Telegram bot to check stock prices, 52-week highs/lows, and volume using yfinance.

## 🚀 Features

- `/stock <TICKER>`: View price, 52-week high/low, and volume.
- Hosted on Railway.

## 📦 Requirements

- Python 3.9+
- A Telegram bot token from BotFather
- Railway account

## 🧠 Setup

```bash
git clone https://github.com/YOUR_USERNAME/stockbot.git
cd stockbot
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Then paste your token in `.env`.

## 🧪 Run locally

```bash
python bot.py
```

## 🛰️ Deploy on Railway

1. Push your repo to GitHub.
2. Go to [Railway](https://railway.app/).
3. Create a new project → Deploy from GitHub.
4. Add `TELEGRAM_BOT_TOKEN` in the Railway environment variables.
5. Done! Your bot is live 🎉

## 🤖 Usage

On Telegram:

```
/start
/stock AAPL
/stock TSLA
```
