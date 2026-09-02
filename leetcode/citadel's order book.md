An exchange matches buyers and sellers of a security. Orders arrive one at a time and are represented with [[oop|classes]] as such:

```python
class Side(Enum):
	BUY = 0
	SELL = 1

class Order:
	def __init__(self, order_id, side, shares, limit_price):
		...
```

You will receive an [[arrays|array]]  of `Order` objects.

```python
orders = [
	Order(1, Side.BUY, 100, 10.0),
	Order(2, Side.BUY, 200, 9.0),
	Order(3, Side.SELL, 300, 11.0),
	Order(4, Side.SELL, 400, 12.0),
	Order(5, Side.SELL, 150, 9.5),
]
```

These are limit orders. A buy order will not execute unless a sell order is available at or below its limit price, and a sell order will not execute unless a buy order is available at or above its limit price. An order that cannot execute rests in the book and waits for a later order to cross it.

Implement `class OrderBook` and the `.fill()` method to simulate such a limit market.

# [[heaps|Heap]] Solution

```python
import heapq
from enum import Enum

class Side(Enum):
    BUY = 0
    SELL = 1

class Order:
    def __init__(self, order_id, side, shares, limit_price):
        self.order_id = order_id
        self.side = side
        self.shares = shares
        self.limit_price = limit_price

class OrderBook:
    def __init__(self, orders):
        self.orders = orders
        self.bids = []
        self.asks = []
	
    def fill(self):
        trades = []
        
        for count, o in enumerate(self.orders):
            if o.shares <= 0:
                continue
                
            # must first push into heap
            if o.side is Side.BUY:
                heapq.heappush(self.bids, (-o.limit_price, count, o))
            else:
                heapq.heappush(self.asks, (o.limit_price, count, o))
            
			# one order can sweep multiple orders 
            while \
	            self.bids and \
	            self.asks and \
	            -self.bids[0][0] >= self.asks[0][0]:
	            
	            # execute trade
                bid = self.bids[0]
                ask = self.asks[0]
                shares_exec = min(bid[2].shares, ask[2].shares)
                price = ask[0] if ask[1] < bid[1] else -bid[0]
                trades.append((
	                ask[2].order_id, 
	                bid[2].order_id, 
	                shares_exec, 
	                price))
	            
	            # kill dead order, wound surviving order
                bid[2].shares -= shares_exec
                ask[2].shares -= shares_exec
                if bid[2].shares == 0:
                    heapq.heappop(self.bids)
                if ask[2].shares == 0:
                    heapq.heappop(self.asks)
        
        return trades
```

## TS Complexity

- `O(nlogk)` TC, `O(k)` SC
	- `k` == the number of orders in order book, `n` ==  all orders.
	- `k` <= `n`
	- Heap operations are `O(logk)`, and we operate `n` times.

## Explanation

1. Use two [[heaps]] to represent our order books. Tracking the highest bid price, and the lowest ask price. 
2. For every new order, push into their respective heaps. Use price to sort, and their temporal order `count` as a tie breaker.
3. Begin checking for possible trades.
	1. Use a while loop to exhaust all possible trades.
	2. Each iteration is a trade. Record them as our answer, and remove traded shares from our heaps. 


# [[array searching#Binary Search|Binary Insert]] Solution

```python

import heapq
from enum import Enum

class Side(Enum):
    BUY = 0
    SELL = 1

class Order:
    def __init__(self, order_id, side, shares, limit_price):
        self.order_id = order_id
        self.side = side
        self.shares = shares
        self.limit_price = limit_price

class OrderBook:
    def __init__(self, orders):
        self.orders = orders
        self.bids = []
        self.asks = []
	
    def fill(self):
        trades = []
        
        for count, o in enumerate(self.orders):
            if o.side is Side.SELL:
	            price = -o.limit_price 
	            book = self.asks
	        else:
	            price = o.limit_price
	            book = self.bids
	            
            left, right = 0, len(book)
            while left < right:
                mid = left + (right - left) // 2
                if book[mid][0] < price:
                    left = mid + 1
                else:
                    right = mid
            book.insert(left, (price, count, o))
            
            while \
	            self.bids and \
                self.asks and \
	            self.bids[-1][0] > -self.asks[-1][0]:
	            
                bid = self.bids[-1][2]
                ask = self.asks[-1][2]
                shares_exec = min(bid.shares, ask.shares)
                
                if self.bids[-1][1] < self.asks[-1][1]:
	                price_exec = bid.limit_price  
                else: 
	                price_exec = ask.limit_price
		        
                trades.append((
	                bid.order_id, 
	                ask.order_id, 
	                shares_exec,      
	                price_exec
				))
	            
                bid.shares -= shares_exec
                ask.shares -= shares_exec
                
                if bid.shares == 0:
                    self.bids.pop()
                if ask.shares == 0:
                    self.asks.pop()
                    
        return trades
```

## TS Complexity

- `O(nk)` TC, `O(k)` SC
	- `O(logk)` to find the index to insert, but inserts are `O(k)`, and we must perform insertions every order `n`. 

## Explanation

1. The same flow as the heaps solution. However, we use two sorted [[arrays]] instead for our order books.
2. Instead of resorting the entire array for each new element, we use [[array searching#Binary Search|binary search]] to find the appropriate index for each new element. This drops the TC from `O(klogk)` to  `O(logk)` + `O(k)`, the price for searching and inserting.
3. Keep the biggest bid and the smallest ask at the end, cheap to `.pop()`.

## Notes

- Slower than hash in notation, but much faster in practice given a reasonable input size due to [[cache#Cache Localities|cache locality]], `.insert()` is very optimized on modern languages.