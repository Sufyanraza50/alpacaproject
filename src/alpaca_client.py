from dotenv import load_dotenv
import os
import alpaca_trade_api as tradeapi

load_dotenv()

API_KEY = os.getenv("ALPACA_API_KEY")
SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
BASE_URL = os.getenv("ALPACA_BASE_URL")

# Create Alpaca REST API client
api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL, api_version='v2')


# ---------------------------------------------------------
# GET ACCOUNT INFO
# ---------------------------------------------------------
def get_account_info():
    return api.get_account()


# ---------------------------------------------------------
# SUBMIT ORDER
# ---------------------------------------------------------
def submit_order(symbol, qty, side, type='market'):
    return api.submit_order(
        symbol=symbol,
        qty=qty,
        side=side,
        type=type,
        time_in_force='gtc'
    )


# ---------------------------------------------------------
# NEW: GET LATEST STOCK PRICE
# ---------------------------------------------------------
def get_stock_price(symbol):
    """
    Fetches the latest price for a given stock symbol.
    Returns float price or None if data unavailable.
    """
    try:
        bar = api.get_latest_bar(symbol)
        return float(bar.close)
    except Exception as e:
        print(f"Error fetching price for {symbol}:", e)
        return None


def get_positions():
    """
    Returns list of open positions from Alpaca.
    """
    try:
        return api.list_positions()
    except Exception as e:
        print("Error fetching positions:", e)
        return []
