"""
Order placement logic — sits between CLI and BinanceClient.
"""

import logging
from bot.client import BinanceClient
from bot.validators import (
    validate_symbol,
    validate_side,
    validate_order_type,
    validate_quantity,
    validate_price,
    ValidationError,
)

logger = logging.getLogger(__name__)


def _print_order_summary(params: dict, response: dict):
    """Pretty-print the request and response."""
    print("\n" + "=" * 55)
    print("  ORDER REQUEST SUMMARY")
    print("=" * 55)
    print(f"  Symbol     : {params.get('symbol')}")
    print(f"  Side       : {params.get('side')}")
    print(f"  Type       : {params.get('type')}")
    print(f"  Quantity   : {params.get('quantity')}")
    if params.get("price"):
        print(f"  Price      : {params.get('price')}")
    if params.get("stopPrice"):
        print(f"  Stop Price : {params.get('stopPrice')}")

    print("\n  ORDER RESPONSE")
    print("-" * 55)
    print(f"  Order ID   : {response.get('orderId')}")
    print(f"  Status     : {response.get('status')}")
    print(f"  Exec. Qty  : {response.get('executedQty')}")
    avg = response.get("avgPrice") or response.get("price", "N/A")
    print(f"  Avg Price  : {avg}")
    print(f"  Client OID : {response.get('clientOrderId')}")
    print("=" * 55 + "\n")


def place_market_order(
    client: BinanceClient,
    symbol: str,
    side: str,
    quantity: str,
) -> dict:
    """Place a MARKET order."""
    sym = validate_symbol(symbol)
    sid = validate_side(side)
    qty = validate_quantity(quantity)

    params = dict(symbol=sym, side=sid, type="MARKET", quantity=qty)
    logger.info("Market order request: %s", params)

    response = client.place_order(**params)
    logger.info("Market order response: %s", response)
    _print_order_summary(params, response)
    return response


def place_limit_order(
    client: BinanceClient,
    symbol: str,
    side: str,
    quantity: str,
    price: str,
    time_in_force: str = "GTC",
) -> dict:
    """Place a LIMIT order."""
    sym = validate_symbol(symbol)
    sid = validate_side(side)
    qty = validate_quantity(quantity)
    prc = validate_price(price)

    params = dict(
        symbol=sym,
        side=sid,
        type="LIMIT",
        quantity=qty,
        price=prc,
        timeInForce=time_in_force,
    )
    logger.info("Limit order request: %s", params)

    response = client.place_order(**params)
    logger.info("Limit order response: %s", response)
    _print_order_summary(params, response)
    return response


def place_stop_market_order(
    client: BinanceClient,
    symbol: str,
    side: str,
    quantity: str,
    stop_price: str,
) -> dict:
    """Place a STOP_MARKET order (bonus order type)."""
    sym = validate_symbol(symbol)
    sid = validate_side(side)
    qty = validate_quantity(quantity)
    sp = validate_price(stop_price)

    params = dict(
        symbol=sym,
        side=sid,
        type="STOP_MARKET",
        quantity=qty,
        stopPrice=sp,
    )
    logger.info("Stop-Market order request: %s", params)

    response = client.place_order(**params)
    logger.info("Stop-Market order response: %s", response)
    _print_order_summary(params, response)
    return response
