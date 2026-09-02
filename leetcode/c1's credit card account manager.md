You're building a [[oop|class]] for Capital One to manage credit card accounts.

# Step by Step Solution

**Part A:** Create a `CreditCard` class. It should store a card number, cardholder name, credit limit, and current balance (starts at 0). 

Implement `charge(amount)` — which increases the balance if the charge doesn't exceed the credit limit, and `payment(amount)` — which decreases the balance. Return `True` if the operation succeeds, `False` otherwise.

```python
class CreditCard:
	def __init__(self, cardNumber, cardHolder, creditLimit):
		self.card_numer = cardNumber
		self.card_holder = cardHolder
		self.credit_limit = creditLimit
		self.balance = 0
	
	def charge(self, amount):
		if self.balance + amount > limit:
			return False
		else:
			self.balance += amount
			return True
	
	def payment(self, amount):
		self.balance -= amount
		return True	
```

**Part B:** Track every charge and payment as a transaction with a unique id, a type ("charge" or "payment"), amount, and date. Implement  `get_transactions_by_type()` that filters by transaction type and `get_transactions_by_id` that filters by id. Use any data structure of your choosing.

```python
def get_transactions_by_type(self, txType):
	if txType != 'charge' or txType != 'payment':
		return False
	# Python3 dictionaries are iterable
	return [tx for tx in self.transactions if tx[0] == txType]

def get_transactions_by_id(self, txid):
	if not transactions[txid]:
		return False
	return transactions[txid]
```

**Part C:** In this scenario, Capital One keeps the data for transactions in two separate [[arrays|array]] of arrays. `txDates` includes transaction date data, `txVals` includes other info. The two arrays are not guaranteed to be in any order, but the same transactions exist in both arrays. The schema is as follows:

```python
txDates = [
[1, '000000'],
[312, '102934']
]

txVals = [
[312, 'payment', 52.13],
[1, 'charge', 123.45]
]
```

Create a method `read_transactions` that reads these two separate arrays into your class.

```python
def read_transactions(self, txDates, txVals):
	# sort to minimize TC
	txDates.sort(key = lambda x : x[0])
	txVals.sort(key = lambda x : x[0])
	
	for i in range(len(txVals)):
		self.transactions[txVals[i][0]] = (txVals[i][1], txVals[i][2], txDates[1])
```

## Notes

- Without sorting, `read_transactions()` would have `O(n^2)` TC, since it needs to traverse through an entire array for every index of another array, their sizes being `n`.
- [[array sorting]] costs `O(n*logn)`, much cheaper. 

**Part D:** Write a method `top_transactions` that takes in an integer `n`, and returns `n` most expensive transactions in the class.

```python
import heapq

def top_transactions(self, n):
	heap = list(self.transactions)[:n]
	heapq.heapify(heap)
	
	for tx in self.transactions:
		if self.transactions[tx][1] > heap[0][1]:
			heap.heapreplace[self.transactions[tx]]
	
	return heap
```

## Notes

- Essentially [[array searching#Top K Search|Top K Search]]. But utilizes the heapq library and forgiveness of python more.
- `heapq.heapify()` uses the first comparable value in the tuple as it's value, dictionaries are also iterable in Python. This allows us to perform top k sort with the transaction tuples we have created in `self.transactions`.

# Complete Solution:

```python
import heapq

class CreditCard:
	def __init__(self, cardNumber, cardHolder, creditLimit):
		self.card_numer = cardNumber
		self.card_holder = cardHolder
		self.credit_limit = creditLimit
		self.balance = 0
		self.transactions = {}
	
	def charge(self, txid, amount, date):
		if self.balance + amount > limit:
			return False
		# store transactions as a tuple
		self.transactions[txid] = ('charge', amount, date)
		self.balance += amount
		return True
	
	def payment(self, txid, amount, date):
		self.transactions[txid] = ('payment', amount, date)
		self.balance -= amount
		return True	
	
	def get_transactions_by_type(self, txType):
		if txType != 'charge' or txType != 'payment':
			return False
		# Python3 dictionaries are iterable
		return [self.transactions[tx] for tx in self.transactions if self.transactions[tx][0] == txType]
	
	def get_transactions_by_id(self, txid):
		if not transactions[txid]:
			return False
		return transactions[txid]
	
	def read_transactions(self, txDates, txVals):
		# sort to minimize TC
		txDates.sort(key = lambda x : x[0])
		txVals.sort(key = lambda x : x[0])
		
		for i in range(len(txVals)):
			self.transactions[txVals[i][0]] = (txVals[i][1], txVals[i][2], txDates[1])
	
	def top_transactions(self, n):
		heap = list(self.transactions)[:n]
		heapq.heapify(heap)

		for tx in self.transactions:
			if self.transactions[tx][1] > heap[0][1]:
				heap.heapreplace[self.transactions[tx]]

		return heap
```