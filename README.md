📈 Telegram Stock Bot

This bot allows you to get real-time stock data (price, volume, 52-week high/low) directly in Telegram by sending:

/stock SYMBOL

Example:

/stock AAPL

🚀 Features

    Current stock price

    52-week high and low

    Daily volume

    Supports any stock supported by Twelve Data

🧩 Tech Stack

    Python 3

    python-telegram-bot

    Twelve Data API

    Railway (for deployment)

📦 Setup Instructions (Local or GitHub)

    Clone the repo or upload the files to GitHub:

git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO

    Install dependencies

pip install -r requirements.txt

    Create a .env file

cp .env.example .env

Fill in your keys:

TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TWELVE_DATA_API_KEY=your-twelve-data-api-key

    Run the bot locally

python bot.py

☁️ Deployment with Railway

    Go to https://railway.app and create a new project.

    Link your GitHub repo containing the bot files.

    Set up Environment Variables in the Railway dashboard:

TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TWELVE_DATA_API_KEY=your-twelve-data-api-key

    Railway should auto-detect Python and deploy the bot.

    Monitor logs to ensure it's working correctly.

🧪 Testing the Bot

    Open Telegram

    Start a chat with your bot (created via @BotFather)

    Send a message like:

/stock TSLA

If everything is set up, you should get real-time data.
🔧 Debugging Tips

    Use Railway Logs to monitor activity.

    In case of errors, check .env variables and Twelve Data API usage.

    For debugging, inspect print statements in bot.py.

📄 License

MIT — feel free to fork and modify.
