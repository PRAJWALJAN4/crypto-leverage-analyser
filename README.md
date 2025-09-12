# crypto-Trade-analyser

# Crypto Leverage Trading Calculator

A Python-based leveraged crypto trading calculator with a graphical user interface (GUI) to help traders estimate profit, loss, and stop-loss scenarios including fees. Supports multiple cryptocurrencies (BTC, ETH, SOL, XRP, and more) and capital currencies (USD and INR) with live price and currency conversion.

---

## Features

- Calculate leveraged position details based on capital, leverage, and trade side (Long/Short)
- Supports USD and INR capital with live currency conversion rates
- Fetch live prices for cryptocurrencies via Delta Exchange API
- Display profit & loss and stop-loss scenarios including fees in both USD and INR
- Interactive Tkinter GUI for easy input and output viewing
- Supports BTC, ETH, SOL, XRP by default and custom trading pairs
- Simple double-click desktop shortcut friendly for quick launch

---

## Getting Started

### Prerequisites

- Python 3.7 or newer installed on your system
- Internet connection for API requests (crypto prices and exchange rates)
- Required Python packages:
  - `requests` (install with `pip install requests`)
- `tkinter` (usually included with Python; no extra install needed)

### Installation

1. Clone or download the repository.
2. In your command line, navigate to the project folder containing `crypto_calc_gui.py`.
3. Install required dependencies:


A window will open allowing you to select cryptocurrency, capital currency, input capital and leverage, and choose trade side. Press **Calculate** to view detailed profit/loss and stop-loss scenarios.

---

## Usage

1. Select cryptocurrency from dropdown menu.
2. Choose capital currency (USD or INR).
3. Enter your capital amount.
4. Enter the leverage multiplier (e.g., 15).
5. Choose trade side: LONG or SHORT.
6. Click **Calculate** to generate scenarios.
7. Review the profit & loss and stop-loss tables, including fees and net results in both USD and INR.

---

## Technologies Used

- Python 3  
- Tkinter for GUI  
- Requests library for API calls  
- Delta Exchange API for live cryptocurrency prices  
- ExchangeRate-API for USD-INR currency conversion  

---

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to fork the repo and submit pull requests.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contact

Created by [Your Name]. For questions or collaboration, reach out at [your-email@example.com].

---

## Acknowledgments

- Delta Exchange for providing market APIs  
- ExchangeRate-API for currency exchange data  
- Tkinter community for GUI support  
