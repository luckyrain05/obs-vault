Implement a [[oop|class]] that tracks the profit and loss of a single stock position.

Implement the methods below.

```python
def add_fill(quantity, price)
```

- `quantity`: shares to be added or sold from the current position.
	- `quantity > 0` means buy, `quantity < 0` means sell.
- `price`: market price of the shares
- Returns nothing.

```python
def get_position() -> str
```

- Returns net position. Long, short, or flat.

```python
def get_realized_pnl() -> int
```

-  Returns the PnL already locked in from closed portions of the position.

```python
def get_unrealized_pnl(current_price) -> int
```

- Returns PnL yet to be realized, hypothetically realized at `current_price`.

Use **FIFO accounting** to determine which shares are closed when an opposite-side trade arrives.
For example: 

```text 
Buy 5 @ $10 
Buy 10 @ $20 
Sell 8 @ $30 
```
  
-  The sell order should offload shares starting from the oldest. Thus, it should sell the `5 @ $10` shares first, then three of the `10 @ $20` shares second. 
- Thus, our PnL is:
$$5 \times(30-10) + 3 \times(20-10) = $130$$
- The remaining position is: 

```text 
7 shares long @ $20 
```

The implementation should also correctly support **short positions**. 
Examples that should work: 

```text 
Sell 10 @ $100 
Buy 4 @ $90
Buy 4 @ $90
Sell 10 @ $100 
``` 

Please: 

1. Implement the class in Python. 
2. Use a clean FIFO-lot data structure. 
3. Explain the logic for matching incoming trades against existing lots. 
4. Walk through both long and short examples. 
5. Explain edge cases when a trade crosses through zero. 
6. Give the time and space complexity of each operation.

# Solution

```python
from collections import deque

class StockPosition:
        def __init__(self):
            self.rpnl         = 0
            self.pos          = 0
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
```

## TS Complexity

## Explanation

- [[queues]]