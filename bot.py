import os
import yfinance as yf
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv
import logging

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Use /stock <TICKER> to get stock data.")

async def stock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("Usage: /stock <TICKER>")
        return

    ticker = context.args[0].upper()
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        if not info or 'regularMarketPrice' not in info:
            raise ValueError("Invalid ticker or data not available")

        current_price = info.get("regularMarketPrice", "N/A")
        high_52w = info.get("fiftyTwoWeekHigh", "N/A")
        low_52w = info.get("fiftyTwoWeekLow", "N/A")
        volume = info.get("volume", "N/A")
        currency = info.get("currency", "USD")

        reply = (
            f"📈 *{ticker}* Stock Info\n"
            f"💵 Price: {current_price} {currency}\n"
            f"📈 52W High: {high_52w} {currency}\n"
            f"📉 52W Low: {low_52w} {currency}\n"
            f"🔁 Volume: {volume:,}\n"
        )
        await update.message.reply_text(reply, parse_mode="Markdown")
    except Exception as e:
        logging.error(f"Error fetching stock: {e}")
        await update.message.reply_text("Error: Couldn't fetch data. Please try again.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stock", stock))
    app.run_polling()
