import os
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
API_KEY = os.getenv("TWELVE_DATA_API_KEY")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Send /stock SYMBOL to get stock info.")

async def stock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("Usage: /stock SYMBOL")
        return

    symbol = context.args[0].upper()

    url = f"https://api.twelvedata.com/time_series"
    params = {
        "symbol": symbol,
        "interval": "1day",
        "apikey": API_KEY,
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
            await update.message.reply_text("No data found for this symbol.")
            return

        latest = values[0]
        close_price = float(latest["close"])
        volume = latest.get("volume", "N/A")

        closes = [float(day["close"]) for day in values]
        high_52w = max(closes)
        low_52w = min(closes)

        reply = (
            f"📈 Stock: {symbol}
"
            f"Price: ${close_price:.2f}
"
            f"52W High: ${high_52w:.2f}
"
            f"52W Low: ${low_52w:.2f}
"
            f"Volume: {volume}"
        )
        await update.message.reply_text(reply)

    except Exception as e:
        logger.error(f"Error fetching stock: {e}")
        await update.message.reply_text("Error: Couldn't fetch data. Please try again later.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stock", stock))
    print("Bot started")
    app.run_polling()

if __name__ == "__main__":
    main()
