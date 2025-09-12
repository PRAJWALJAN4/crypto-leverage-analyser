import requests

FEE_PERCENT_PER_SIDE = 0.04  # 0.04% per side
ROUND_TRIP_FEE_PCT = FEE_PERCENT_PER_SIDE * 2

def get_eth_price(symbol):
    try:
        resp = requests.get(f"https://api.delta.exchange/v2/tickers/{symbol}")
        resp.raise_for_status()
        return float(resp.json()['result']['close'])
    except Exception as e:
        print(f"Error fetching {symbol} price: {e}")
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
        print(f"Currency conversion error: {e}")
        return None

def trading_calculator():
    print("📊 Multi-Crypto Leverage Trading Calculator (Delta Exchange)\n")

    SYMBOLS = {"1": "BTCUSDT", "2": "ETHUSDT", "3": "SOLUSDT", "4": "XRPUSDT", "5": "Others"}
    choice = input("Select crypto (1: BTC, 2: ETH, 3: SOL, 4: XRP, 5: Others): ").strip()
    if choice in SYMBOLS and choice != "5":
        symbol = SYMBOLS[choice]
    elif choice == "5":
        symbol = input("Enter trading pair symbol (e.g. BTCUSDT): ").strip().upper()
    else:
        print("Invalid crypto choice.")
        return

    cur_choice = input("Select capital currency (1: USD, 2: INR): ").strip()
    cur = "USD" if cur_choice == "1" else "INR"

    cap = float(input("Capital amount: "))

    # Display equivalent capital in other currency
    if cur == "INR":
        cap_usd = convert_currency(cap, "INR", "USD")
        print(f"Capital entered: ₹{cap:.2f} ≈ ${cap_usd:.2f}")
    else:
        cap_usd = cap
        cap_inr = convert_currency(cap, "USD", "INR")
        print(f"Capital entered: ${cap:.2f} ≈ ₹{cap_inr:.2f}")

    lev = int(input("Leverage (e.g. 10, 25, 50): "))
    side_choice = input("Trade side (1: LONG, 2: SHORT): ").strip()
    trade_side = "LONG" if side_choice == "1" else "SHORT"

    cap_inr = cap if cur == "INR" else convert_currency(cap_usd, "USD", "INR")

    price = get_eth_price(symbol)
    if price is None:
        return

    print(f"\n✅ Current {symbol} Price: ${price:.2f}\n")

    pos_usd = cap_usd * lev
    contracts = pos_usd / price
    fee_usd = pos_usd * (ROUND_TRIP_FEE_PCT / 100)
    fee_inr = fee_usd * (cap_inr / cap_usd)

    # Profit & Loss Scenarios
    print("💰 PROFIT & LOSS SCENARIOS")
    print(f"{'Move':<5} {'Target Price':<14} {'PnL (USD)':<10} {'Fee (USD)':<10} {'Net USD':<9} "
          f"{'PnL (INR)':<10} {'Fee (INR)':<10} {'Net INR':<9}")
    print("-" * 90)
    for pct in range(1, 11):
        pnl_usd = cap_usd * pct / 100
        price_move = pnl_usd / contracts
        target_price = price + price_move if trade_side == "LONG" else price - price_move
        net_usd = pnl_usd - fee_usd
        pnl_inr = pnl_usd * (cap_inr / cap_usd)
        net_inr = pnl_inr - fee_inr
        print(f"+{pct}%   ${target_price:<12.2f} ${pnl_usd:<9.2f} ${fee_usd:<9.2f} "
              f"${net_usd:<8.2f} ₹{pnl_inr:<9.0f} ₹{fee_inr:<9.0f} ₹{net_inr:<8.0f}")

    # Stop-Loss Scenarios
    print("\n🛑 STOP-LOSS SCENARIOS")
    print(f"{'Risk%':<5} {'SL Price':<12} {'Loss (USD)':<11} {'Fee (USD)':<10} {'Total USD':<10} "
          f"{'Loss (INR)':<10} {'Fee (INR)':<10} {'Total INR':<10}")
    print("-" * 95)
    for pct in range(1, 11):
        loss_usd = cap_usd * pct / 100
        price_move = loss_usd / contracts
        sl_price = price - price_move if trade_side == "LONG" else price + price_move
        total_usd = loss_usd + fee_usd
        loss_inr = loss_usd * (cap_inr / cap_usd)
        total_inr = -(loss_inr + fee_inr)  # Negative to indicate loss
        print(f"{pct}%   ${sl_price:<11.2f} ${loss_usd:<10.2f} ${fee_usd:<9.2f} "
              f"${total_usd:<9.2f} ₹{loss_inr:<9.0f} ₹{fee_inr:<9.0f} ₹{total_inr:<9.0f}")

if __name__ == "__main__":
    trading_calculator()
