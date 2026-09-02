An extension of [[citadel's pnl tracking 1]].

Design a system that tracks buy and sell trades for multiple ticker symbols and computes the profit/loss for each symbol over time.

Requirements

- Support adding **buy and sell trades** for different ticker symbols.
- Track each ticker symbol independently.
- Track the current **net position** for each symbol.

The class should support the following methods:

```python
class PnlTracker:
	def add_trade(trade): pass
	
	def update_market_price(symbol, price): pass
	
	def get_position(symbol): pass
	
	def get_realized_pnl(symbol): pass
	
	def get_unrealized_pnl(symbol): pass
	
	def get_total_pnl(symbol): pass
	
```

- Every method here has the same requirements as [[citadel's pnl tracking 1]], except `get_unrealized_pnl()`, which should calculate unrealized pnl using the market price.

A trade should contain the following:

- symbol
- side
- quantity
- price

Test Cases:

```python

if __name__ == "__main__":
    tracker = PnlTracker()
    trades = [
        Trade("AAPL", Side.BUY,  100, 10.0),
        Trade("AAPL", Side.BUY,  100, 11.0),
        Trade("AAPL", Side.SELL, 150, 12.0),
        Trade("TSLA", Side.SELL,  10, 50.0),
        Trade("TSLA", Side.BUY,   10, 45.0),
    ]
    
    for t in trades:
        print(f"\n>>> {t.side.value} {t.quantity} {t.symbol} @ {t.price}")
        tracker.add_trade(t)
        print(f"    position:   {tracker.get_position(t.symbol)}")
        print(f"    realized:   {tracker.get_realized_pnl(t.symbol)}")
        print(f"    unrealized: {tracker.get_unrealized_pnl(t.symbol)}")
        print(f"    total:      {tracker.get_total_pnl(t.symbol)}")
    
    print("\n>>> mark AAPL to 13.0")
    tracker.update_market_price("AAPL", 13.0)
    print(f"    unrealized: {tracker.get_unrealized_pnl('AAPL')}")
    print(f"    total:      {tracker.get_total_pnl('AAPL')}")
```

# Solution

```python
from enum import Enum
from collections import deque
from dataclasses import dataclass

class Side(str, Enum):
    BUY = "BUY"
    SELL = "SELL"

@dataclass
class Trade:
    symbol   : int
    side     : Side
    quantity : int
    price    : int

class PnlTracker:
    class StockPosition:
        def __init__(self):
            self.rpnl         = 0
            self.pos          = 0
            self.market_price = 0
            self.buys         = deque()
            self.sells        = deque()
		
        def add_fill(self, quantity, price):
            if quantity == 0:
                raise ValueError("Cannot process 0 shares.")
            elif quantity < 0:
                self.sells.append([-quantity, price])
            else:
                self.buys.append([quantity, price])
			
			self.pos += quantity * price
			
            while self.buys and self.sells:
                buy = self.buys[0]
                sell = self.sells[0]
                shares_exec = min(buy[0], sell[0])
                self.rpnl += sell[1] - buy[1]
                self.pos  -= shares_exec * (buy[1] + sell[1])
				
                buy[0] -= shares_exec
                sell[0] -= shares_exec
                if buy[0] == 0:
                    self.buys.popleft()
                if sell[0] == 0:
                    self.sells.popleft()
		
        def get_position(self) -> str:
            if self.pos == 0:
                return "Flat"
            elif self.pos > 0:
                return "Long"
            else:
                return "Short"
		
        def get_realized_pnl(self) -> int:
            return self.rpnl
		
        def get_unrealized_pnl(self, current_price) -> int:
            if self.buys:
                return sum(
	                shares * (current_price - price) \
	                for shares, price in self.buys
	            )
            elif self.sells:
                return sum(
	                shares * (price - current_price) \ 
	                for shares, price in self.sells
	            )
            else:
                return 0
	
    def __init__(self):
        self.portfolio = {}
	
    def add_trade(self, trade):
        if trade.side is Side.BUY:
            quantity = trade.quantity
        else:
            quantity = -trade.quantity
		
        if trade.symbol not in self.portfolio:
            self.portfolio[trade.symbol] = self.StockPosition()
		
		self.update_market_price(trade.symbol, trade.price)	
        self.portfolio[trade.symbol].add_fill(quantity, trade.price)
	
	def _lookup(self, symbol):
		if symbol not in self.portfolio:
            raise KeyError("ticker not in portfolio")
        return self.portfolio[symbol]
    
    def get_position(self, symbol):
        return self.portfolio[symbol].get_position()
	
    def update_market_price(self, symbol, price):
        self._lookup(symbol).market_price = price
	
    def get_realized_pnl(self, symbol):
        return self._lookup(symbol).get_realized_pnl()
	
    def get_unrealized_pnl(self, symbol):
        return self._lookup(symbol).get_unrealized_pnl(
	        self._lookup(symbol).market_price
	    )
	
    def get_total_pnl(self, symbol):
        return (
            self.get_realized_pnl(symbol) +
            self.get_unrealized_pnl(symbol)
        )
```

- [[oop#Encapsulation|Encapsulate]] the class from [[citadel's pnl tracking 1]], represent a portfolio of stocks using a [[hashs#Dictionary|dictionary]].