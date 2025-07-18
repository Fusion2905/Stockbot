import logging
import yfinance as yf
import time
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Retry logic for fetching stock info
def get_stock_info(ticker_symbol):
    for attempt in range(3):
        try:
            ticker = yf.Ticker(ticker_symbol)
            info = ticker.info

            if not info or "shortName" not in info:
                raise ValueError("Invalid or missing stock info")

            return {
                "name": info.get("shortName", "N/A"),
                "price": info.get("regularMarketPrice", "N/A"),
                "currency": info.get("currency", "N/A")
            }

        except Exception as e:
            logging.error(f"Error fetching stock: {e}")
            time.sleep(1.5)  # Wait before retrying
    return None

# Command handler for /stock
async def stock_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Please provide a stock symbol. Usage: /stock AAPL")
        return

    symbol = context.args[0].upper()
    stock_data = get_stock_info(symbol)

    if stock_data:
        reply = f"📈
