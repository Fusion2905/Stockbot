import os
import logging
import yfinance as yf
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

# Logging for debugging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Your bot token from environment variables
TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.environ.get("PORT", 8443))
WEBHOOK_HOST = os.getenv("RAILWAY_STATIC_URL")  # e.g. mybot.up.railway.app

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Send /stock <symbol> to get stock price.")

# /stock command handler
async def stock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("Usage: /stock <symbol>")
        return

    symbol = context.args[0].upper()
    try:
        data = yf.Ticker(symbol)
        price = data.info.get("currentPrice")

        if price:
            await update.message.reply_text(f"{symbol} current price: ${price}")
        else:
            await update.message.reply_text("Couldn't fetch price. Try another symbol.")
    except Exception as e:
        logging.error(f"Error fetching stock: {e}")
        await update.message.reply_text("Error: Couldn't fetch data. Please try again.")

# Main app
if __name__ == "__main__":
    if not TOKEN:
        raise Exception("BOT_TOKEN is not set in environment variables.")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stock", stock))

    webhook_url = f"https://{WEBHOOK_HOST}/{TOKEN}"
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=webhook_url
    )

