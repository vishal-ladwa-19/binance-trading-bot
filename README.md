# Binance Futures Trading Bot

> **Junior Python Developer Application - Trading Bot Assignment**

A professional-grade trading bot for Binance Futures Testnet supporting market orders, limit orders, and stop-limit orders with comprehensive logging and error handling.

---

## 📋 Assignment Completion Status

✅ **All Core Requirements Implemented**
- Market orders (BUY/SELL)
- Limit orders (BUY/SELL)
- Command-line interface with validation
- Comprehensive logging system
- Error handling and order status output
- Binance Futures Testnet integration

✅ **Bonus Features Included**
- Stop-Limit orders (advanced order type)
- Enhanced menu-driven CLI
- Account balance checking
- View/manage open orders

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the bot
python trading_bot.py

# 3. Enter your Binance Testnet API credentials when prompted
```

---

## ✨ Key Features

- **Market Orders** - Instant execution at current market price
- **Limit Orders** - Execute at your specified price target
- **Stop-Limit Orders** - Advanced risk management (BONUS)
- **Input Validation** - Prevents invalid symbols, quantities, prices
- **Error Handling** - Graceful handling of API errors and edge cases
- **Comprehensive Logging** - All actions logged to timestamped files
- **User-Friendly CLI** - Clear prompts and detailed feedback

---

## 💻 Technology Stack

```
Language:     Python 3.7+
Library:      python-binance 1.0.19
API:          Binance Futures REST API
Environment:  Testnet (https://testnet.binancefuture.com)
Architecture: Object-oriented with clean separation of concerns
```

---

## 📖 Usage Example

```
BINANCE FUTURES TRADING BOT - TESTNET

1. Market Order
2. Limit Order  
3. Stop-Limit Order (BONUS)
4. View Open Orders
5. Check Account Balance
6. Exit

Enter your choice: 1
Enter symbol: BTCUSDT
Select Side: 1 (BUY)
Enter quantity: 0.001

✓ ORDER EXECUTED SUCCESSFULLY
  Order ID: 12345678
  Symbol: BTCUSDT
  Side: BUY
  Type: MARKET
  Status: FILLED
```


