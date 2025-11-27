from dotenv import load_dotenv
import os
import alpaca_trade_api as tradeapi

load_dotenv()

API_KEY = os.getenv("ALPACA_API_KEY")
SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
BASE_URL = os.getenv("ALPACA_BASE_URL")

api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL, api_version='v2')

def get_account_info():
    return api.get_account()

def submit_order(symbol, qty, side, type='market'):
    return api.submit_order(
        symbol=symbol,
        qty=qty,
        side=side,
        type=type,
        time_in_force='gtc'
    )
