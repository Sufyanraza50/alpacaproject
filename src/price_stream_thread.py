import os
import asyncio
from PyQt6.QtCore import QThread, pyqtSignal
import alpaca_trade_api as tradeapi

class PriceStreamThread(QThread):
    price_update = pyqtSignal(dict)  # Emits {symbol: price}

    def __init__(self, symbols):
        super().__init__()
        self.symbols = symbols

    def run(self):
        asyncio.run(self.stream_prices())

    async def stream_prices(self):
        stream = tradeapi.Stream(
            key_id=os.getenv("ALPACA_API_KEY"),
            secret_key=os.getenv("ALPACA_SECRET_KEY"),
            base_url=os.getenv("ALPACA_BASE_URL"),
            data_feed='iex'
        )

        async def on_trade(trade):
            self.price_update.emit({trade.symbol: trade.price})

        for symbol in self.symbols:
            stream.subscribe_trades(on_trade, symbol)

        try:
            await stream._run_forever()
        except Exception as e:
            print("WebSocket error:", e)
