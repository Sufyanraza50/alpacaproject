import sys
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QSizePolicy
from alpaca_client import get_account_info, get_stock_price, get_positions

stock_symbols = [
    "AAPL","MSFT","GOOG","GOOGL","AMZN","NVDA","AVGO","META","TSLA","NFLX",
    "ADBE","AMD","ABNB","AMGN","ADI","AMAT","ASML","ARM","AZN","TEAM",
    "ADSK","ADP","AXON","BKR","BIIB","BKNG","CDNS","CDW","CHTR","CSCO",
    "CCEP","CTAS","CSGP","COST","CPRT","CRWD","CSX","DDOG","DXCM","EA",
    "EXC","FAST","FTNT","GILD","GEHC","HON","IDXX","INTC","INTU","ISRG",
    "KDP","KLAC","LRCX","LIN","LULU","MAR","MRVL","MELI","MCHP","MDLZ",
    "MNST","MU","NFLX","NXPI","ODFL","ON","ORLY","PCAR","PDD","PEP",
    "QCOM","REGN","ROP","ROST","SBUX","SHOP","SNPS","TTD","TMUS","TTWO",
    "TXN","VRSK","VRTX","WBD","WDAY","XEL","ZS"
]

class TradingBotGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AlgoAI Trading Bot")
        self.setGeometry(100, 100, 1200, 600)

        # Main horizontal layout
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        # -------------------------------
        # Left panel: Account Info + Stock Prices
        # -------------------------------
        left_panel = QVBoxLayout()
        main_layout.addLayout(left_panel, stretch=1)

        # Account Info (top-left)
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

        # Stock Prices table (beneath Account Info)
        self.stock_table = QTableWidget()
        self.stock_table.setColumnCount(2)
        self.stock_table.setHorizontalHeaderLabels(["Symbol", "Price"])
        self.stock_table.setRowCount(len(stock_symbols))
        self.stock_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        left_panel.addWidget(QLabel("<b>Stock Prices</b>"))
        left_panel.addWidget(self.stock_table)

        # -------------------------------
        # Right panel: Positions Table
        # -------------------------------
        right_panel = QVBoxLayout()
        main_layout.addLayout(right_panel, stretch=2)

        self.positions_table = QTableWidget()
        self.positions_table.setColumnCount(7)
        self.positions_table.setHorizontalHeaderLabels([
            "Symbol", "Qty", "Entry Price", "Current Price", 
            "Market Value", "Unrealized P/L", "Status"
        ])
        self.positions_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        right_panel.addWidget(QLabel("<b>Open Positions</b>"))
        right_panel.addWidget(self.positions_table)

        # -------------------------------
        # Timer for updates
        # -------------------------------
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(5000)  # every 5 seconds

        # Initial data load
        self.update_data()

    def update_data(self):
        # -------------------------------
        # Update Account Info
        # -------------------------------
        try:
            acc = get_account_info()
            self.status_label.setText(f"Status: {acc.status}")
            self.equity_label.setText(f"Equity: ${float(acc.equity):,.2f}")
            self.buying_power_label.setText(f"Buying Power: ${float(acc.buying_power):,.2f}")
            self.cash_label.setText(f"Cash: ${float(acc.cash):,.2f}")
        except Exception as e:
            print("Account error:", e)

        # -------------------------------
        # Update Stock Prices
        # -------------------------------
        try:
            for row, symbol in enumerate(stock_symbols):
                price = get_stock_price(symbol)
                self.stock_table.setItem(row, 0, QTableWidgetItem(symbol))
                self.stock_table.setItem(row, 1, QTableWidgetItem(f"${price:.2f}" if price else "---"))

            # Resize columns and rows to fit content
            self.stock_table.resizeColumnsToContents()
            self.stock_table.resizeRowsToContents()
        except Exception as e:
            print("Stock prices error:", e)

        # -------------------------------
        # Update Positions
        # -------------------------------
        try:
            positions = get_positions()
            self.positions_table.setRowCount(len(positions) if positions else 1)

            if not positions:
                for col in range(7):
                    self.positions_table.setItem(0, col, QTableWidgetItem("---"))
            else:
                for row, p in enumerate(positions):
                    pl = float(p.unrealized_pl)
                    pl_text = f"${pl:,.2f}"

                    self.positions_table.setItem(row, 0, QTableWidgetItem(p.symbol))
                    self.positions_table.setItem(row, 1, QTableWidgetItem(str(p.qty)))
                    self.positions_table.setItem(row, 2, QTableWidgetItem(f"${float(p.avg_entry_price):.2f}"))
                    self.positions_table.setItem(row, 3, QTableWidgetItem(f"${float(p.current_price):.2f}"))
                    self.positions_table.setItem(row, 4, QTableWidgetItem(f"${float(p.market_value):,.2f}"))

                    pl_item = QTableWidgetItem(pl_text)
                    pl_item.setForeground(Qt.GlobalColor.green if pl >= 0 else Qt.GlobalColor.red)
                    self.positions_table.setItem(row, 5, pl_item)

                    status_item = QTableWidgetItem("OPEN")
                    status_item.setForeground(Qt.GlobalColor.green)
                    self.positions_table.setItem(row, 6, status_item)

            # Resize columns and rows to fit content
            self.positions_table.resizeColumnsToContents()
            self.positions_table.resizeRowsToContents()

        except Exception as e:
            print("Positions error:", e)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TradingBotGUI()
    window.show()
    sys.exit(app.exec())
