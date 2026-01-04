import logging
import sys
from datetime import datetime
from typing import Optional, Dict, Any
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'trading_bot_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


class BasicBot:
    """
    A trading bot for Binance Futures Testnet supporting market, limit, and advanced order types.
    """
    
    def __init__(self, api_key: str, api_secret: str, testnet: bool = True):
        """
        Initialize the trading bot with API credentials.
        
        Args:
            api_key: Binance API key
            api_secret: Binance API secret
            testnet: Whether to use testnet (default: True)
        """
        try:
            self.client = Client(api_key, api_secret, testnet=testnet)
            if testnet:
                self.client.API_URL = 'https://testnet.binancefuture.com'
            
            logger.info("Bot initialized successfully")
            logger.info(f"Using {'TESTNET' if testnet else 'LIVE'} environment")
            
            # Test connection
            self._test_connection()
        except Exception as e:
            logger.error(f"Failed to initialize bot: {str(e)}")
            raise
    
    def _test_connection(self):
        """Test API connection and log account info."""
        try:
            account = self.client.futures_account()
            logger.info("Connection successful")
            logger.info(f"Account balance: {account.get('totalWalletBalance', 'N/A')} USDT")
        except Exception as e:
            logger.error(f"Connection test failed: {str(e)}")
            raise
    
    def _validate_symbol(self, symbol: str) -> bool:
        """Validate if symbol exists on Binance Futures."""
        try:
            exchange_info = self.client.futures_exchange_info()
            symbols = [s['symbol'] for s in exchange_info['symbols']]
            return symbol.upper() in symbols
        except Exception as e:
            logger.error(f"Symbol validation failed: {str(e)}")
            return False
    
    def _log_order_details(self, order: Dict[str, Any]):
        """Log order details in a readable format."""
        logger.info("="*50)
        logger.info("ORDER EXECUTED SUCCESSFULLY")
        logger.info("="*50)
        logger.info(f"Order ID: {order.get('orderId')}")
        logger.info(f"Symbol: {order.get('symbol')}")
        logger.info(f"Side: {order.get('side')}")
        logger.info(f"Type: {order.get('type')}")
        logger.info(f"Quantity: {order.get('origQty')}")
        logger.info(f"Price: {order.get('price', 'MARKET')}")
        logger.info(f"Status: {order.get('status')}")
        logger.info(f"Time: {datetime.fromtimestamp(order.get('updateTime', 0)/1000)}")
        logger.info("="*50)
    
    def place_market_order(self, symbol: str, side: str, quantity: float) -> Optional[Dict]:
        """
        Place a market order.
        
        Args:
            symbol: Trading pair (e.g., 'BTCUSDT')
            side: 'BUY' or 'SELL'
            quantity: Order quantity
            
        Returns:
            Order response dict or None if failed
        """
        try:
            symbol = symbol.upper()
            side = side.upper()
            
            # Validate inputs
            if not self._validate_symbol(symbol):
                raise ValueError(f"Invalid symbol: {symbol}")
            
            if side not in ['BUY', 'SELL']:
                raise ValueError("Side must be 'BUY' or 'SELL'")
            
            if quantity <= 0:
                raise ValueError("Quantity must be positive")
            
            logger.info(f"Placing MARKET {side} order for {quantity} {symbol}")
            
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='MARKET',
                quantity=quantity
            )
            
            self._log_order_details(order)
            return order
            
        except BinanceAPIException as e:
            logger.error(f"Binance API Error: {e.status_code} - {e.message}")
            return None
        except BinanceOrderException as e:
            logger.error(f"Order Error: {e.status_code} - {e.message}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error placing market order: {str(e)}")
            return None
    
    def place_limit_order(self, symbol: str, side: str, quantity: float, price: float) -> Optional[Dict]:
        """
        Place a limit order.
        
        Args:
            symbol: Trading pair (e.g., 'BTCUSDT')
            side: 'BUY' or 'SELL'
            quantity: Order quantity
            price: Limit price
            
        Returns:
            Order response dict or None if failed
        """
        try:
            symbol = symbol.upper()
            side = side.upper()
            
            # Validate inputs
            if not self._validate_symbol(symbol):
                raise ValueError(f"Invalid symbol: {symbol}")
            
            if side not in ['BUY', 'SELL']:
                raise ValueError("Side must be 'BUY' or 'SELL'")
            
            if quantity <= 0 or price <= 0:
                raise ValueError("Quantity and price must be positive")
            
            logger.info(f"Placing LIMIT {side} order for {quantity} {symbol} at {price}")
            
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='LIMIT',
                timeInForce='GTC',
                quantity=quantity,
                price=price
            )
            
            self._log_order_details(order)
            return order
            
        except BinanceAPIException as e:
            logger.error(f"Binance API Error: {e.status_code} - {e.message}")
            return None
        except BinanceOrderException as e:
            logger.error(f"Order Error: {e.status_code} - {e.message}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error placing limit order: {str(e)}")
            return None
    
    def place_stop_limit_order(self, symbol: str, side: str, quantity: float, 
                               stop_price: float, limit_price: float) -> Optional[Dict]:
        """
        Place a stop-limit order (BONUS feature).
        
        Args:
            symbol: Trading pair (e.g., 'BTCUSDT')
            side: 'BUY' or 'SELL'
            quantity: Order quantity
            stop_price: Stop/trigger price
            limit_price: Limit price after trigger
            
        Returns:
            Order response dict or None if failed
        """
        try:
            symbol = symbol.upper()
            side = side.upper()
            
            # Validate inputs
            if not self._validate_symbol(symbol):
                raise ValueError(f"Invalid symbol: {symbol}")
            
            if side not in ['BUY', 'SELL']:
                raise ValueError("Side must be 'BUY' or 'SELL'")
            
            if quantity <= 0 or stop_price <= 0 or limit_price <= 0:
                raise ValueError("Quantity, stop price, and limit price must be positive")
            
            logger.info(f"Placing STOP_LIMIT {side} order for {quantity} {symbol}")
            logger.info(f"Stop Price: {stop_price}, Limit Price: {limit_price}")
            
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='STOP',
                timeInForce='GTC',
                quantity=quantity,
                price=limit_price,
                stopPrice=stop_price
            )
            
            self._log_order_details(order)
            return order
            
        except BinanceAPIException as e:
            logger.error(f"Binance API Error: {e.status_code} - {e.message}")
            return None
        except BinanceOrderException as e:
            logger.error(f"Order Error: {e.status_code} - {e.message}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error placing stop-limit order: {str(e)}")
            return None
    
    def get_open_orders(self, symbol: Optional[str] = None) -> list:
        """Get all open orders."""
        try:
            if symbol:
                orders = self.client.futures_get_open_orders(symbol=symbol.upper())
            else:
                orders = self.client.futures_get_open_orders()
            
            logger.info(f"Retrieved {len(orders)} open orders")
            return orders
        except Exception as e:
            logger.error(f"Error getting open orders: {str(e)}")
            return []
    
    def cancel_order(self, symbol: str, order_id: int) -> bool:
        """Cancel an open order."""
        try:
            result = self.client.futures_cancel_order(
                symbol=symbol.upper(),
                orderId=order_id
            )
            logger.info(f"Order {order_id} cancelled successfully")
            return True
        except Exception as e:
            logger.error(f"Error cancelling order: {str(e)}")
            return False


def get_user_input() -> Dict[str, Any]:
    """Get order details from user via CLI."""
    print("\n" + "="*60)
    print("BINANCE FUTURES TRADING BOT - TESTNET")
    print("="*60)
    
    # Order type
    print("\nSelect Order Type:")
    print("1. Market Order")
    print("2. Limit Order")
    print("3. Stop-Limit Order (Bonus)")
    
    order_type = input("\nEnter choice (1-3): ").strip()
    
    # Symbol
    symbol = input("Enter symbol (e.g., BTCUSDT): ").strip().upper()
    
    # Side
    print("\nSelect Side:")
    print("1. BUY")
    print("2. SELL")
    side_choice = input("Enter choice (1-2): ").strip()
    side = "BUY" if side_choice == "1" else "SELL"
    
    # Quantity
    quantity = float(input("Enter quantity: ").strip())
    
    # Price details based on order type
    price = None
    stop_price = None
    limit_price = None
    
    if order_type == "2":  # Limit order
        price = float(input("Enter limit price: ").strip())
    elif order_type == "3":  # Stop-limit order
        stop_price = float(input("Enter stop price: ").strip())
        limit_price = float(input("Enter limit price: ").strip())
    
    return {
        'order_type': order_type,
        'symbol': symbol,
        'side': side,
        'quantity': quantity,
        'price': price,
        'stop_price': stop_price,
        'limit_price': limit_price
    }


def main():
    """Main function to run the trading bot."""
    print("Binance Futures Trading Bot - Testnet")
    print("="*60)
    
    # Get API credentials
    api_key = "TSnFKBzElWEqE923PO7lzM0SzUnMYmDw6liFlHHtIXfISSBp3dIneW8W8Tn51ROH"
    api_secret = "cKbBUvB7cV7zyFGuHlRND63lN5kuDMqjNJh9AXhyDcH1AW8CFGQE9yeSGY2FlY7I"
    
    try:
        # Initialize bot
        bot = BasicBot(api_key, api_secret, testnet=True)
        
        while True:
            # Get user input
            order_params = get_user_input()
            
            # Execute order based on type
            if order_params['order_type'] == '1':
                bot.place_market_order(
                    order_params['symbol'],
                    order_params['side'],
                    order_params['quantity']
                )
            elif order_params['order_type'] == '2':
                bot.place_limit_order(
                    order_params['symbol'],
                    order_params['side'],
                    order_params['quantity'],
                    order_params['price']
                )
            elif order_params['order_type'] == '3':
                bot.place_stop_limit_order(
                    order_params['symbol'],
                    order_params['side'],
                    order_params['quantity'],
                    order_params['stop_price'],
                    order_params['limit_price']
                )
            else:
                logger.error("Invalid order type selected")
            
            # Continue or exit
            continue_trading = input("\nPlace another order? (y/n): ").strip().lower()
            if continue_trading != 'y':
                print("\nThank you for using the Trading Bot!")
                break
                
    except KeyboardInterrupt:
        print("\n\nBot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()