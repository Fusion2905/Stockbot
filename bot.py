import os
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TWELVE_DATA_API_KEY = os.getenv("TWELVE_DATA_API_KEY")

# Logging setup
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! Use /stock SYMBOL to get stock info. Example: /stock AAPL")

# Command: /stock
async def stock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /stock SYMBOL (e.g., /stock AAPL)")
        return

    symbol = context.args[0].upper()
    url = "https://api.twelvedata.com/time_series"
    params = {
        "symbol": symbol,
        "interval": "1day",
        "apikey": TWELVE_DATA_API_KEY,
        "format": "json",
        "outputsize": 365
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if "status" in data and data["status"] == "error":
            await update.message.reply_text(f"Error: {data.get('message', 'Unknown error')}")
            return

        values = data.get("values", [])
        if not values:
            await update.message.reply_text("No data available for that symbol.")
            return

        latest = values[0]
        close_price = float(latest.get("close", 0))
        volume = latest.get("volume", "N/A")
        closes = [float(day["close"]) for day in values if "close" in day]

        reply = (
            f"📈 Stock: {symbol}
"
            f"Price: ${close_price:.2f}
"
            f"52W High: ${max(closes):.2f}
"
            f"52W Low: ${min(closes):.2f}
"
            f"Volume: {volume}"
        )
        await update.message.reply_text(reply)

    except Exception as e:
        logger.error(f"Failed to fetch stock data: {e}")
        await update.message.reply_text("Error fetching stock data. Try again later.")

# Main entry point
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stock", stock))
    logger.info("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
