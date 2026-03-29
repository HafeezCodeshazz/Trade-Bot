"""
Input validation helpers for CLI arguments.
"""

VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT", "STOP_MARKET", "STOP_LIMIT"}
VALID_TIF = {"GTC", "IOC", "FOK", "GTX"}


class ValidationError(ValueError):
    """Raised when user input is invalid."""


def validate_symbol(symbol: str) -> str:
    s = symbol.strip().upper()
    if not s:
        raise ValidationError("Symbol cannot be empty.")
    return s


def validate_side(side: str) -> str:
    s = side.strip().upper()
    if s not in VALID_SIDES:
        raise ValidationError(f"Side must be one of {VALID_SIDES}. Got: '{side}'")
    return s


def validate_order_type(order_type: str) -> str:
    t = order_type.strip().upper()
    if t not in VALID_ORDER_TYPES:
        raise ValidationError(
            f"Order type must be one of {VALID_ORDER_TYPES}. Got: '{order_type}'"
        )
    return t


def validate_quantity(quantity: str) -> float:
    try:
        q = float(quantity)
    except (ValueError, TypeError):
        raise ValidationError(f"Quantity must be a number. Got: '{quantity}'")
    if q <= 0:
        raise ValidationError(f"Quantity must be positive. Got: {q}")
    return q


def validate_price(price: str) -> float:
    try:
        p = float(price)
    except (ValueError, TypeError):
        raise ValidationError(f"Price must be a number. Got: '{price}'")
    if p <= 0:
        raise ValidationError(f"Price must be positive. Got: {p}")
    return p
