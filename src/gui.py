import sys
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QSizePolicy
from alpaca_client import get_account_info, get_positions
from price_stream_thread import PriceStreamThread

# ONLY FIRST 10 SYMBOLS
stock_symbols = ["AAPL","MSFT","GOOG","GOOGL","AMZN","NVDA","AVGO","META","TSLA","NFLX"]

class TradingBotGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AlgoAI Trading Bot")
        self.setGeometry(100, 100, 1200, 600)

        # Main layout
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        # Left panel: Account + Stock Prices
        left_panel = QVBoxLayout()
        main_layout.addLayout(left_panel, stretch=1)

        # Account info
        self.account_layout = QVBoxLayout()
        left_panel.addLayout(self.account_layout)
        self.account_layout.addWidget(QLabel("<b>Account Info</b>"))

        self.status_label = QLabel("Status: ----")
        self.equity_label = QLabel("Equity: ----")
        self.buying_power_label = QLabel("Buying Power: ----")
        self.cash_label = QLabel("Cash: ----")

        self.account_layout.addWidget(self.status_label)
        self.account_layout.addWidget(self.equity_label)
        self.account_layout.addWidget(self.buying_power_label)
        self.account_layout.addWidget(self.cash_label)

        # Stock Prices table
        self.stock_table = QTableWidget()
        self.stock_table.setColumnCount(2)
        self.stock_table.setHorizontalHeaderLabels(["Symbol","Price"])
        self.stock_table.setRowCount(len(stock_symbols))
        self.stock_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        left_panel.addWidget(QLabel("<b>Stock Prices</b>"))
        left_panel.addWidget(self.stock_table)

        for row, symbol in enumerate(stock_symbols):
            self.stock_table.setItem(row, 0, QTableWidgetItem(symbol))
            self.stock_table.setItem(row, 1, QTableWidgetItem("---"))

        # Right panel: Positions
        right_panel = QVBoxLayout()
        main_layout.addLayout(right_panel, stretch=2)

        self.positions_table = QTableWidget()
        self.positions_table.setColumnCount(7)
        self.positions_table.setHorizontalHeaderLabels([
            "Symbol","Qty","Entry Price","Current Price","Market Value","Unrealized P/L","Status"
        ])
        self.positions_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        right_panel.addWidget(QLabel("<b>Open Positions</b>"))
        right_panel.addWidget(self.positions_table)

        # Start WebSocket for live prices
        self.stream_thread = PriceStreamThread(stock_symbols)
        self.stream_thread.price_update.connect(self.update_stock_table_live)
        self.stream_thread.start()

        # Timer for account info & positions
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_rest_data)
        self.timer.start(5000)
        self.update_rest_data()

    # WebSocket updates
    def update_stock_table_live(self, data):
        for symbol, price in data.items():
            for row in range(self.stock_table.rowCount()):
                if self.stock_table.item(row,0).text() == symbol:
                    self.stock_table.setItem(row,1,QTableWidgetItem(f"${price:.2f}"))
                    break
        self.stock_table.resizeColumnsToContents()

    # REST updates
    def update_rest_data(self):
        try:
            acc = get_account_info()
            self.status_label.setText(f"Status: {acc.status}")
            self.equity_label.setText(f"Equity: ${float(acc.equity):,.2f}")
            self.buying_power_label.setText(f"Buying Power: ${float(acc.buying_power):,.2f}")
            self.cash_label.setText(f"Cash: ${float(acc.cash):,.2f}")
        except Exception as e:
            print("Account error:", e)

        try:
            positions = get_positions()
            self.positions_table.setRowCount(len(positions) if positions else 1)
            if not positions:
                for col in range(7):
                    self.positions_table.setItem(0,col,QTableWidgetItem("---"))
            else:
                for row,p in enumerate(positions):
                    pl = float(p.unrealized_pl)
                    self.positions_table.setItem(row,0,QTableWidgetItem(p.symbol))
                    self.positions_table.setItem(row,1,QTableWidgetItem(str(p.qty)))
                    self.positions_table.setItem(row,2,QTableWidgetItem(f"${float(p.avg_entry_price):.2f}"))
                    self.positions_table.setItem(row,3,QTableWidgetItem(f"${float(p.current_price):.2f}"))
                    self.positions_table.setItem(row,4,QTableWidgetItem(f"${float(p.market_value):,.2f}"))
                    pl_item = QTableWidgetItem(f"${pl:,.2f}")
                    pl_item.setForeground(Qt.GlobalColor.green if pl >= 0 else Qt.GlobalColor.red)
                    self.positions_table.setItem(row,5,pl_item)
                    status_item = QTableWidgetItem("OPEN")
                    status_item.setForeground(Qt.GlobalColor.green)
                    self.positions_table.setItem(row,6,status_item)
            self.positions_table.resizeColumnsToContents()
        except Exception as e:
            print("Positions error:", e)
