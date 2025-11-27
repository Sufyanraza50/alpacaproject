import tkinter as tk
from tkinter import ttk
from alpaca_client import get_account_info, get_stock_price, get_positions


def create_gui():
    window = tk.Tk()
    window.title("AlgoAI Trading Bot")
    window.geometry("850x500")
    

    # ---------------------------------------------------------
    # ACCOUNT INFO FRAME (TOP-LEFT)
    # ---------------------------------------------------------
    account_frame = tk.Frame(window, bg="#f0f0f0", bd=2, relief="groove")
    account_frame.place(x=10, y=10, width=250, height=120)

    title_label = tk.Label(account_frame, text="Account Info", font=("Arial", 12, "bold"), bg="#f0f0f0")
    title_label.pack(pady=5)

    status_label = tk.Label(account_frame, text="Status: ----", font=("Arial", 10), bg="#f0f0f0")
    status_label.pack(anchor="w", padx=10)

    equity_label = tk.Label(account_frame, text="Equity: ----", font=("Arial", 10), bg="#f0f0f0")
    equity_label.pack(anchor="w", padx=10)

    buying_power_label = tk.Label(account_frame, text="Buying Power: ----", font=("Arial", 10), bg="#f0f0f0")
    buying_power_label.pack(anchor="w", padx=10)

    cash_label = tk.Label(account_frame, text="Cash: ----", font=("Arial", 10), bg="#f0f0f0")
    cash_label.pack(anchor="w", padx=10)


    # ---------------------------------------------------------
    # STOCK LIST FRAME (LEFT SIDE)
    # ---------------------------------------------------------
    stocks_frame = tk.Frame(window, bg="#f8f8f8", bd=2, relief="groove")
    stocks_frame.place(x=10, y=140, width=250, height=340)

    stock_title = tk.Label(stocks_frame, text="Stock Prices", font=("Arial", 12, "bold"), bg="#f8f8f8")
    stock_title.pack(pady=5)

    columns = ("Symbol", "Price")
    stock_table = ttk.Treeview(stocks_frame, columns=columns, show="headings", height=15)
    stock_table.heading("Symbol", text="Symbol")
    stock_table.heading("Price", text="Price")

    stock_table.column("Symbol", width=80)
    stock_table.column("Price", width=120)

    stock_table.pack(padx=5, pady=5)

    stock_symbols = ["AAPL", "MSFT", "TSLA", "AMZN", "NVDA", "META"]


    # ---------------------------------------------------------
    # POSITIONS FRAME (CENTER)
    # ---------------------------------------------------------
    positions_frame = tk.Frame(window, bg="#f8f8f8", bd=2, relief="groove")
    positions_frame.place(x=280, y=10, width=550, height=470)

    pos_title = tk.Label(positions_frame, text="Open Positions", font=("Arial", 14, "bold"), bg="#f8f8f8")
    pos_title.pack(pady=5)

    pos_columns = ("Symbol", "Qty", "Entry Price", "Current Price", "Market Value", "Unrealized P/L", "Status")
    positions_table = ttk.Treeview(positions_frame, columns=pos_columns, show="headings", height=22)

    # Define column headings and proportional widths
    positions_table.heading("Symbol", text="Symbol")
    positions_table.heading("Qty", text="Qty")
    positions_table.heading("Entry Price", text="Entry Price")
    positions_table.heading("Current Price", text="Current Price")
    positions_table.heading("Market Value", text="Market Value")
    positions_table.heading("Unrealized P/L", text="Unrealized P/L")
    positions_table.heading("Status", text="Status")

    # Set column widths so all fit nicely in 550px
    positions_table.column("Symbol", width=70, anchor="center")
    positions_table.column("Qty", width=50, anchor="center")
    positions_table.column("Entry Price", width=80, anchor="center")
    positions_table.column("Current Price", width=90, anchor="center")
    positions_table.column("Market Value", width=100, anchor="center")
    positions_table.column("Unrealized P/L", width=90, anchor="center")
    positions_table.column("Status", width=70, anchor="center")

    positions_table.pack(padx=5, pady=5, fill="x")



    # ---------------------------------------------------------
    # AUTO FUNCTIONS
    # ---------------------------------------------------------

    def load_account_info():
        try:
            acc = get_account_info()

            status_label.config(text=f"Status: {acc.status}")
            equity_label.config(text=f"Equity: {float(acc.equity):,.2f}")
            buying_power_label.config(text=f"Buying Power: {float(acc.buying_power):,.2f}")
            cash_label.config(text=f"Cash: {float(acc.cash):,.2f}")
        except Exception as e:
            print("Account error:", e)

        window.after(5000, load_account_info)


    def load_stock_prices():
        try:
            stock_table.delete(*stock_table.get_children())

            for symbol in stock_symbols:
                price = get_stock_price(symbol)
                price_text = f"${price:.2f}" if price else "---"
                stock_table.insert("", "end", values=(symbol, price_text))
        except Exception as e:
            print("Price error:", e)

        window.after(5000, load_stock_prices)


    # ---------------------------------------------------------
    # LOAD POSITIONS
    # ---------------------------------------------------------
    def load_positions():
        try:
            positions_table.delete(*positions_table.get_children())

            pos = get_positions()

            for p in pos if pos else [None]:
                if p is None:  # No positions
                    values = ("---", "---", "---", "---", "---", "---", "CLOSED")
                    # Tag the Status column only (simulate)
                    tag = "closed"
                    positions_table.insert("", "end", values=values, tags=(tag,))
                else:
                    pl = float(p.unrealized_pl)
                    pl_text = f"${pl:,.2f}"
                    pl_tag = "profit" if pl >= 0 else "loss"

                    status = "OPEN"
                    status_tag = "open" if status == "OPEN" else "closed"

                    values = (
                        p.symbol,
                        p.qty,
                        f"${float(p.avg_entry_price):.2f}",
                        f"${float(p.current_price):.2f}",
                        f"${float(p.market_value):,.2f}",
                        pl_text,
                        status
                    )

                    # Insert the row with a dummy tag
                    positions_table.insert("", "end", values=values, tags=("normal",))

            # After insertion, loop through items and color **only two columns**
            for iid in positions_table.get_children():
                vals = positions_table.item(iid)["values"]
                # Color Unrealized P/L
                pl_val = vals[5]
                pl_num = float(pl_val.replace("$", "").replace(",", "")) if pl_val != "---" else 0
                pl_color = "green" if pl_num >= 0 else "red"
                positions_table.tag_configure(f"pl_{iid}", foreground=pl_color)
                # Color Status
                status_val = vals[6]
                status_color = "green" if status_val == "OPEN" else "red"
                positions_table.tag_configure(f"status_{iid}", foreground=status_color)

                # Assign tag
                positions_table.item(iid, tags=(f"pl_{iid}", f"status_{iid}"))

        except Exception as e:
            print("Positions error:", e)

        window.after(5000, load_positions)

    # Initial Loads
    load_account_info()
    load_stock_prices()
    load_positions()

    window.mainloop()



if __name__ == "__main__":
    create_gui()
