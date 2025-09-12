import tkinter as tk
from tkinter import ttk, messagebox
import requests

FEE_PERCENT_PER_SIDE = 0.04
ROUND_TRIP_FEE_PCT = FEE_PERCENT_PER_SIDE * 2

SYMBOLS = {
    "BTC": "BTCUSDT",
    "ETH": "ETHUSDT",
    "SOL": "SOLUSDT",
    "XRP": "XRPUSDT",
}

def get_price(symbol):
    try:
        resp = requests.get(f"https://api.delta.exchange/v2/tickers/{symbol}")
        resp.raise_for_status()
        return float(resp.json()['result']['close'])
    except Exception as e:
        messagebox.showerror("Error", f"Error fetching price for {symbol}:\n{e}")
        return None

def convert_currency(amount, from_cur, to_cur):
    if from_cur == to_cur:
        return amount
    try:
        resp = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        resp.raise_for_status()
        rate = resp.json()['rates']['INR']
        return amount * rate if from_cur == 'USD' else amount / rate
    except Exception as e:
        messagebox.showerror("Error", f"Currency conversion error:\n{e}")
        return None

class CryptoCalcApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Crypto Leverage Trading Calculator")
        self.geometry("950x600")
        self.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        # Input frame
        inp_frame = ttk.LabelFrame(self, text="Inputs")
        inp_frame.pack(fill='x', padx=10, pady=5)

        ttk.Label(inp_frame, text="Cryptocurrency:").grid(row=0, column=0, padx=5, pady=5)
        self.crypto_var = tk.StringVar(value="BTC")
        crypto_options = list(SYMBOLS.keys())
        crypto_menu = ttk.OptionMenu(inp_frame, self.crypto_var, crypto_options[0], *crypto_options)
        crypto_menu.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(inp_frame, text="Capital currency:").grid(row=0, column=2, padx=5, pady=5)
        self.cap_cur_var = tk.StringVar(value="INR")
        cur_menu = ttk.OptionMenu(inp_frame, self.cap_cur_var, "INR", "USD", "INR")
        cur_menu.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(inp_frame, text="Capital amount:").grid(row=1, column=0, padx=5, pady=5)
        self.cap_entry = ttk.Entry(inp_frame)
        self.cap_entry.grid(row=1, column=1, padx=5, pady=5)
        self.cap_entry.insert(0, "5000")

        ttk.Label(inp_frame, text="Leverage:").grid(row=1, column=2, padx=5, pady=5)
        self.lev_entry = ttk.Entry(inp_frame)
        self.lev_entry.grid(row=1, column=3, padx=5, pady=5)
        self.lev_entry.insert(0, "15")

        ttk.Label(inp_frame, text="Trade side:").grid(row=2, column=0, padx=5, pady=5)
        self.side_var = tk.StringVar(value="LONG")
        side_menu = ttk.OptionMenu(inp_frame, self.side_var, "LONG", "LONG", "SHORT")
        side_menu.grid(row=2, column=1, padx=5, pady=5)

        calc_btn = ttk.Button(inp_frame, text="Calculate", command=self.calculate)
        calc_btn.grid(row=2, column=3, padx=5, pady=5)

        # Output frame
        out_frame = ttk.LabelFrame(self, text="Results")
        out_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Current price label
        self.price_lbl = ttk.Label(out_frame, text="Current Price: N/A")
        self.price_lbl.pack(pady=5)

        # Treeviews for PnL and Stop loss
        pnl_label = ttk.Label(out_frame, text="Profit & Loss Scenarios")
        pnl_label.pack()
        columns = ["Move", "Target Price", "PnL (USD)", "Fee (USD)", "Net USD", "PnL (INR)", "Fee (INR)", "Net INR"]
        self.pnl_tree = ttk.Treeview(out_frame, columns=columns, show="headings", height=10)
        for col in columns:
            self.pnl_tree.heading(col, text=col)
            self.pnl_tree.column(col, width=100, anchor='center')
        self.pnl_tree.pack(pady=5)

        sl_label = ttk.Label(out_frame, text="Stop Loss Scenarios")
        sl_label.pack()
        sl_columns = ["Risk %", "SL Price", "Loss (USD)", "Fee (USD)", "Total USD", "Loss (INR)", "Fee (INR)", "Total INR"]
        self.sl_tree = ttk.Treeview(out_frame, columns=sl_columns, show="headings", height=10)
        for col in sl_columns:
            self.sl_tree.heading(col, text=col)
            self.sl_tree.column(col, width=100, anchor='center')
        self.sl_tree.pack(pady=5)

    def calculate(self):
        # Clear old results
        for i in self.pnl_tree.get_children():
            self.pnl_tree.delete(i)
        for i in self.sl_tree.get_children():
            self.sl_tree.delete(i)

        # Fetch inputs
        crypto = self.crypto_var.get()
        symbol = SYMBOLS[crypto]
        cap_cur = self.cap_cur_var.get()
        try:
            cap = float(self.cap_entry.get())
            lev = int(self.lev_entry.get())
        except:
            messagebox.showerror("Input Error", "Please enter valid numeric capital and leverage")
            return
        side = self.side_var.get()

        price = get_price(symbol)
        if price is None:
            return

        self.price_lbl.config(text=f"Current {symbol} Price: ${price:.2f}")

        cap_usd = cap if cap_cur == "USD" else convert_currency(cap, "INR", "USD")
        cap_inr = cap if cap_cur == "INR" else convert_currency(cap_usd, "USD", "INR")

        pos_usd = cap_usd * lev
        contracts = pos_usd / price
        fee_usd = pos_usd * (ROUND_TRIP_FEE_PCT / 100)
        fee_inr = fee_usd * (cap_inr / cap_usd)

        # Populate PnL scenarios
        for pct in range(1, 11):
            pnl_usd = cap_usd * pct / 100
            price_move = pnl_usd / contracts
            if side == "LONG":
                target_price = price + price_move
            else:
                target_price = price - price_move
            net_usd = pnl_usd - fee_usd
            pnl_inr = pnl_usd * (cap_inr / cap_usd)
            net_inr = pnl_inr - fee_inr
            self.pnl_tree.insert("", "end", values=(
                f"+{pct}%",
                f"{target_price:.2f}",
                f"{pnl_usd:.2f}",
                f"{fee_usd:.2f}",
                f"{net_usd:.2f}",
                f"{int(round(pnl_inr))}",
                f"{int(round(fee_inr))}",
                f"{int(round(net_inr))}",
            ))

        # Populate Stop Loss scenarios
        for pct in range(1, 11):
            loss_usd = cap_usd * pct / 100
            price_move = loss_usd / contracts
            if side == "LONG":
                sl_price = price - price_move
            else:
                sl_price = price + price_move
            total_usd = loss_usd + fee_usd
            loss_inr = loss_usd * (cap_inr / cap_usd)
            total_inr = loss_inr + fee_inr
            self.sl_tree.insert("", "end", values=(
                f"{pct}%",
                f"{sl_price:.2f}",
                f"{loss_usd:.2f}",
                f"{fee_usd:.2f}",
                f"{total_usd:.2f}",
                f"{int(round(loss_inr))}",
                f"{int(round(fee_inr))}",
                f"{int(round(total_inr))}",
            ))

if __name__ == "__main__":
    app = CryptoCalcApp()
    app.mainloop()
