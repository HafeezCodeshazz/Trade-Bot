#!/usr/bin/env python3
"""
cli.py  —  Command-line interface for the Binance Futures Testnet trading bot.

Usage examples
--------------
  # Market BUY
  python cli.py order --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

  # Limit SELL
  python cli.py order --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 100000

  # Stop-Market BUY (bonus)
  python cli.py order --symbol BTCUSDT --side BUY --type STOP_MARKET --quantity 0.001 --stop-price 80000

  # Check account balances
  python cli.py account
"""

import argparse
import os
import sys

from dotenv import load_dotenv

from bot.client import BinanceClient
from bot.logging_config import setup_logging
from bot.orders import place_limit_order, place_market_order
from bot.validators import ValidationError

load_dotenv()


# ------------------------------------------------------------------ #
#  Helpers                                                            #
# ------------------------------------------------------------------ #

def get_client() -> BinanceClient:
    api_key = os.getenv("BINANCE_API_KEY", "").strip()
    api_secret = os.getenv("BINANCE_API_SECRET", "").strip()
    if not api_key or not api_secret:
        print(
            "[ERROR] BINANCE_API_KEY and BINANCE_API_SECRET must be set in your .env file."
        )
        sys.exit(1)
    return BinanceClient(api_key=api_key, api_secret=api_secret)


# ------------------------------------------------------------------ #
#  Sub-command handlers                                               #
# ------------------------------------------------------------------ #

def cmd_order(args):
    client = get_client()
    order_type = args.type.upper()

    try:
        if order_type == "MARKET":
            place_market_order(
                client=client,
                symbol=args.symbol,
                side=args.side,
                quantity=args.quantity,
            )

        elif order_type == "LIMIT":
            if not args.price:
                print("[ERROR] --price is required for LIMIT orders.")
                sys.exit(1)
            place_limit_order(
                client=client,
                symbol=args.symbol,
                side=args.side,
                quantity=args.quantity,
                price=args.price,
            )

        else:
            print(f"[ERROR] Unsupported order type: {order_type}")
            sys.exit(1)

    except ValidationError as exc:
        print(f"[VALIDATION ERROR] {exc}")
        sys.exit(1)
    except Exception as exc:
        print(f"[API ERROR] {exc}")
        sys.exit(1)


def cmd_account(args):
    client = get_client()
    try:
        data = client.get_account_info()
        print("\n" + "=" * 55)
        print("  ACCOUNT BALANCES")
        print("=" * 55)
        for asset in data.get("assets", []):
            wb = float(asset.get("walletBalance", 0))
            if wb != 0:
                print(f"  {asset['asset']:<10} wallet: {wb:.4f}  "
                      f"unrealised PnL: {float(asset.get('unrealizedProfit', 0)):.4f}")
        print("=" * 55 + "\n")
    except Exception as exc:
        print(f"[ERROR] {exc}")
        sys.exit(1)


# ------------------------------------------------------------------ #
#  Argument parser                                                    #
# ------------------------------------------------------------------ #

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="trading_bot",
        description="Binance Futures Testnet Trading Bot (USDT-M)",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging verbosity (default: INFO)",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- order sub-command ---
    order_parser = subparsers.add_parser("order", help="Place a futures order")
    order_parser.add_argument("--symbol", required=True, help="Trading pair, e.g. BTCUSDT")
    order_parser.add_argument("--side", required=True, choices=["BUY", "SELL", "buy", "sell"])
    order_parser.add_argument(
        "--type", required=True,
        choices=["MARKET", "LIMIT", "market", "limit"],
        dest="type",
    )
    order_parser.add_argument("--quantity", required=True, help="Order quantity")
    order_parser.add_argument("--price", default=None, help="Limit price (required for LIMIT)")
    order_parser.set_defaults(func=cmd_order)

    # --- account sub-command ---
    account_parser = subparsers.add_parser("account", help="Show account balances")
    account_parser.set_defaults(func=cmd_account)

    return parser


# ------------------------------------------------------------------ #
#  Entry point                                                        #
# ------------------------------------------------------------------ #

def main():
    parser = build_parser()
    args = parser.parse_args()
    setup_logging(args.log_level)
    args.func(args)


if __name__ == "__main__":
    main()
