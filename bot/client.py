"""
Binance Futures Testnet - API Client Wrapper using python-binance
"""

import logging
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException

logger = logging.getLogger(__name__)


class BinanceClient:
    """Wrapper around Binance Futures Testnet REST API using python-binance."""

    def __init__(self, api_key: str, api_secret: str):
        self.client = Client(api_key, api_secret, testnet=True)
        logger.info("Binance Futures Testnet client initialized")

    def place_order(self, **kwargs):
        """Place an order on Binance Futures Testnet."""
        try:
            order = self.client.futures_create_order(**kwargs)
            logger.info(f"Order placed: {order}")
            return order
        except (BinanceAPIException, BinanceRequestException) as e:
            logger.error(f"API Error: {e}")
            raise

    def get_account_info(self):
        """Get account information."""
        try:
            account = self.client.futures_account()
            logger.info("Account info retrieved")
            return account
        except (BinanceAPIException, BinanceRequestException) as e:
            logger.error(f"API Error: {e}")
            raise
