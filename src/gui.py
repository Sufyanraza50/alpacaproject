import tkinter as tk
from tkinter import messagebox
from alpaca_client import get_account_info

def create_gui():
    window = tk.Tk()
    window.title("AlgoAI Trading Bot")
    window.geometry("400x300")

    tk.Label(window, text="AlgoAI Trading Bot", font=("Arial", 16)).pack(pady=10)

    def check_account():
        try:
            acc = get_account_info()
            messagebox.showinfo("Alpaca", f"Account Status: {acc.status}\nBuying Power: {acc.buying_power}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(window, text="Check Alpaca Account", command=check_account).pack(pady=20)

    window.mainloop()

if __name__ == "__main__":
    create_gui()
