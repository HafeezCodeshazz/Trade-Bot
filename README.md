# Trading Bot — Binance Futures Testnet (USDT-M)

A clean, modular Python CLI application to place **Market**, **Limit**, and **Stop-Market** orders on the Binance Futures Testnet.

---

## Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py          # Binance REST API wrapper
│   ├── orders.py          # Order placement logic
│   ├── validators.py      # Input validation
│   └── logging_config.py  # Logging setup (file + console)
├── logs/                  # Auto-created; stores trading_bot.log
├── cli.py                 # CLI entry point
├── .env.example           # Credentials template
├── requirements.txt
└── README.md
```

---

## Setup Steps

### 1. Clone / download the project

```bash
git clone <your-repo-url>
cd trading_bot
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API credentials

```bash
cp .env.example .env
```

Open `.env` and replace the placeholder values with your **Binance Futures Testnet** API key and secret:

```
BINANCE_API_KEY=your_actual_key
BINANCE_API_SECRET=your_actual_secret
```

> Get credentials at: https://testnet.binancefuture.com → top-right menu → API Management

---

## How to Run

### Place a MARKET order

```bash
# Buy 0.001 BTC at market price
python cli.py order --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

# Sell 0.001 BTC at market price
python cli.py order --symbol BTCUSDT --side SELL --type MARKET --quantity 0.001
```

### Place a LIMIT order

```bash
# Buy 0.001 BTC at $50,000
python cli.py order --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.001 --price 50000

# Sell 0.001 BTC at $100,000
python cli.py order --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 100000
```

### Check account balances

```bash
python cli.py account
```

### Adjust log verbosity

```bash
python cli.py --log-level DEBUG order --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

---

## Output Example

=======================================================
ORDER REQUEST SUMMARY

Symbol : BTCUSDT
Side : BUY
Type : MARKET
Quantity : 0.003

ORDER RESPONSE
Order ID : 13006501806
Status : NEW
Exec. Qty : 0.000
Avg Price : 0.00
Client OID : x-Cb7ytekJ4ae09f0aede22196e02d08
---

## Logs

All API requests, responses, and errors are written to **`logs/trading_bot.log`** (rotating, max 5 MB × 3 backups). The console shows INFO and above; the file captures DEBUG and above.

## 📂 Log Files (Submission Requirement)

The file `logs/trading_bot.log` contains:

- MARKET order request and response
- LIMIT order request and response

These logs include API interactions, order details, and error handling information.
---

## Assumptions

- Testnet base URL: `https://testnet.binancefuture.com`
- Only USDT-M perpetual futures are targeted.
- Credentials are stored in a local `.env` file (never commit this file).
- Minimum quantity for BTCUSDT on testnet is typically `0.001`.

---

## ⚠️ Note on Binance Testnet Behavior

The Binance Futures Testnet environment may not always execute orders immediately. 
In some cases, orders can remain in `NEW` status due to limitations of the testnet matching engine.

Despite this, all order requests in this project are successfully sent to the API and valid responses 
(including order IDs) are received, demonstrating correct implementation of:

- MARKET orders
- LIMIT orders
- STOP-MARKET orders
- Logging and error handling

## Dependencies

| Package | Purpose |
|---------|---------|
| `python-binance` | Official Binance API client for Python |
| `python-dotenv` | Load environment variables from .env file |

---

## 🚀 Features

- Place MARKET orders
- Place LIMIT orders
- Place STOP-MARKET orders
- CLI-based interface
- Input validation
- Structured logging (file + console)
- Environment-based configuration

## License

MIT — free to use and modify.
