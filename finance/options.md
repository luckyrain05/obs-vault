- A [[finance/derivatives|derivative]] giving the holder the right, but not the obligation, to buy or sell an underlying at a fixed price by an expiration date.
- Defining feature: asymmetric payoff. Holder pays a premium up front; downside is bounded by the premium, upside is unbounded.
- Underlying is typically a [[stocks|stock]], but options also exist on indexes, commodities, currencies, and futures.

# Terminology

**Strike Price**

- Denoted $K$.
- The price at which the holder buys (call) or sells (put) if exercised.

**Expiration**

- Denoted $T$.
- The date past which the contract is dead. No exercise after $T$.

**Premium**

- The price the holder pays the writer at contract creation. Non-refundable.
- Denoted $c$ for a call, $p$ for a put.

**Spot Price**

- Denoted $S$ now, $S_T$ at expiration.
- The current market price of the underlying.

**Moneyness**

- ==In-the-money== (ITM): exercising is profitable right now (ignoring premium). Call: $S > K$. Put: $S < K$.
- ==At-the-money== (ATM): $S = K$.
- ==Out-of-the-money== (OTM): exercising would lose money. Call: $S < K$. Put: $S > K$.
- ITM options have positive intrinsic value. OTM options have zero intrinsic value, only time value.

**American vs. European**

- ==American==: exercisable any time up to expiration.
- ==European==: exercisable only at expiration.
- American options are weakly more valuable. Any exercise an American holder could take, a European holder cannot — the early-exercise right is a strict superset, never negative.

# Calls and Puts

**Call**

- The right to buy at strike $K$ by expiration.
- Holder is bullish — wants the price to rise.
- Payoff at expiration: $\max(S_T - K, 0)$.
	- $S_T > K$: holder exercises, buys at $K$, sells in market at $S_T$, gross profit $S_T - K$.
	- $S_T \le K$: holder walks away, payoff zero.
- Net profit, accounting for premium paid: $\max(S_T - K, 0) - c$.

**Put**

- The right to sell at strike $K$ by expiration.
- Holder is bearish — wants the price to fall.
- Payoff at expiration: $\max(K - S_T, 0)$.
	- $S_T < K$: holder exercises, sells at $K$, buys in market at $S_T$, gross profit $K - S_T$.
	- $S_T \ge K$: holder walks away, payoff zero.
- Net profit, accounting for premium paid: $\max(K - S_T, 0) - p$.

# Payoff Diagrams

- The asymmetric payoff is most visible as a graph of net profit vs. spot price at expiration. The kink at $K$ is the option's defining feature: linear above (or below) $K$, flat at the premium loss otherwise.

**Long Call**

```
  Profit
    ^
    |                          /
    |                         /
    |                        /
    |                       /
   0+----------------------+--------> S_T
    |                      K
   -c+======================+
    |
```

- Below $K$: flat at $-c$. Holder walks away, loss = premium.
- Above $K$: 45° rising. Profit = $(S_T - K) - c$. Crosses zero at $S_T = K + c$ (==break-even==).
- Max loss: $c$. Max profit: unbounded.

**Long Put**

```
  Profit
    ^
    |\
    | \
    |  \
    |   \
   0+----+------------------+------> S_T
    |    K
   -p+    ==================+
    |
```

- Above $K$: flat at $-p$.
- Below $K$: rises as $S_T$ falls. Profit = $(K - S_T) - p$. Crosses zero at $S_T = K - p$.
- Max loss: $p$. Max profit: $K - p$ (when $S_T = 0$).

**Short Call**

- Exact mirror of long call across the horizontal axis.
- Max profit: $c$ (premium collected). Max loss: unbounded.
- Writer obligated to deliver at $K$ if exercised.

**Short Put**

- Exact mirror of long put.
- Max profit: $p$. Max loss: $K - p$ (when $S_T = 0$).
- Writer obligated to buy at $K$ if exercised.

# Intrinsic vs. Time Value

- The premium decomposes into two non-negative parts.
- $\text{Premium} = \text{Intrinsic Value} + \text{Time Value}$

**Intrinsic Value**

- What the option would be worth if exercised right now.
- Call: $\max(S - K, 0)$.
- Put: $\max(K - S, 0)$.
- Always non-negative. Zero for OTM options.

**Time Value**

- Premium minus intrinsic value. The remaining portion of the price.
- Captures the chance the underlying moves further into the money before expiration.
- Drivers:
	- Time to expiration: longer time = more chance of favorable movement = higher time value.
	- Volatility of the underlying: higher σ = wider distribution of $S_T$ = larger probability of a big favorable move = higher time value.
	- Interest rate: discounts the strike. Calls more valuable when $r$ is higher; puts less.
- Time value approaches zero as $T$ approaches. At expiration $\text{Premium} = \text{Intrinsic Value}$ exactly — there is no future left in which the underlying could still move.

# Valuation Frameworks

- Two standard models price options. This file flags them by name; derivation lives elsewhere.

**Black-Scholes**

- Continuous-time model. Assumes the underlying follows a log-normal price process with constant volatility, no dividends, frictionless trading.
- Yields a closed-form formula for European call and put prices in terms of $S, K, T, r, \sigma$.
- Foundational. Turned options from exotic instruments into mainstream by giving traders a single number to anchor on.

**Binomial Model**

- Discrete-time. The underlying moves up by factor $u$ or down by factor $d$ each period. Build a tree to expiration; value the option backward by replication or risk-neutral expectation.
- Handles American options naturally — early exercise can be checked at every node.
- Converges to Black-Scholes as the time step shrinks toward zero.
