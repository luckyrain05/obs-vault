- Three [[finance/derivatives|derivative]] instruments with symmetric payoff. Both parties are obligated; gains for one side equal losses for the other.
	- ==Forward==: bilateral OTC contract to exchange an asset for a fixed price at maturity.
	- ==Future==: standardized, exchange-traded forward with daily mark-to-market and a clearinghouse.
	- ==Swap==: periodic exchange of cash flows between two parties over a stated term.
- All three lock in something today (a price, a stream of rates) about a date later. None requires an up-front premium because both sides are exposed equally — no asymmetry to pay for.

# Why Symmetric Contracts

- Both parties want certainty. The buyer locks in a buy price; the seller locks the same price. Each gives up the chance of a more favorable spot move in exchange for eliminating the risk of an adverse one.
- The contract is struck so both sides start at fair value. No money changes hands at signing — only the obligation to perform later.
- Contrast with [[options]], where one side has discretion (asymmetric) and a premium is paid up front for that discretion.

# Forward

- Customized, bilateral contract. The buyer agrees to take delivery of the asset at maturity $T$ for a price $K$ set today. The seller agrees to deliver.
- Traded OTC. Strike, maturity, asset, quantity, settlement details all negotiated privately.
- No cash flows until maturity. No exchange and no clearinghouse stand between the parties.

**Payoff at Maturity**

- ==Long== (buyer) payoff: $S_T - K$. Pays the agreed $K$, receives the asset worth $S_T$.
- ==Short== (seller) payoff: $K - S_T$. Delivers the asset worth $S_T$, receives $K$.
- Symmetric. The two payoffs sum to zero at every $S_T$ — one side's gain is the other's loss.

**Counterparty Risk**

- Bilateral with no intermediary. Each side bears the risk the other defaults at maturity.
- If $S_T$ moves far against a party, that party has incentive to walk away. Without an intermediary backing the trade, the winning side may not collect.

# Future

- A standardized forward traded on an exchange.
- Two structural changes vs. a forward eliminate counterparty risk and most operational friction:
	- A ==clearinghouse== stands between every buyer and seller, becoming the legal counterparty to both.
	- Daily ==mark-to-market== settles gains and losses each day rather than once at maturity.

**Standardization**

- Strike, maturity dates, contract size, deliverable grade — all fixed by the exchange. Trading is in identical contracts, not custom ones.
- Liquidity follows from standardization: any future can be closed out by taking the offsetting position in the same contract series at any time before maturity.

**Clearinghouse**

- After a trade is matched, the clearinghouse interposes itself: the buyer's contract is now with the clearinghouse, and the seller's contract is now with the clearinghouse. The original two parties have no direct claim on each other.
- Clearinghouse manages its own risk via margin requirements and a guarantee fund.
- For the trader, counterparty default risk is effectively eliminated. If the original counterparty defaults, the clearinghouse still performs.

**Mark-to-Market**

- At the end of each trading day the contract is repriced at the day's settlement price.
- The party that lost value pays cash to the party that gained value, routed through margin accounts.
- Effect: the contract's economic exposure is reset to zero each day. P&L is realized in cash daily, not banked until maturity.
- Net payoff over the life of the contract is the same as a forward struck at the same price, but cash-flow timing is spread across many days rather than concentrated at maturity.

**Margin**

- ==Initial margin==: cash deposited when the position is opened. A performance bond.
- ==Maintenance margin==: a floor on the margin balance.
- If a daily mark-to-market loss pushes the balance below maintenance, the trader receives a ==margin call== and must top up to the initial level by the next day.
- Failure to meet a margin call: the clearinghouse liquidates the position. Combined with daily mark-to-market, no trader can build up an unsecured loss — at most one day's adverse move is unsecured at any time.

# Forward vs. Future

```
+---------------+--------------------+----------------------+
|               | Forward            | Future               |
+---------------+--------------------+----------------------+
| Venue         | OTC, bilateral     | Exchange             |
| Standardized  | No                 | Yes                  |
| Clearinghouse | None               | Yes                  |
| Settlement    | Once at maturity   | Daily mark-to-market |
| Counterparty  | Original other side| Clearinghouse        |
| Margin        | None (typically)   | Initial + maint.     |
| Customization | Full               | None                 |
+---------------+--------------------+----------------------+
```

- Identical payoff at maturity for the same strike. Different cash-flow timing, different counterparty risk, different liquidity profile.
- Forwards are used when terms must be customized (specific delivery date, specific grade, off-market FX pairs). Futures are used when standardization is acceptable and counterparty risk is not.

# Swap

- A contract to exchange streams of cash flows between two parties at periodic intervals over a stated term.
- Mechanically equivalent to a sequence of forwards, one per payment date.
- ==Notional principal== is the reference amount on which payments are computed. Usually never exchanged — only the differential between the two legs each period.

**Fixed-for-Floating Interest Rate Swap**

- The most common swap. Two parties on a notional $N$ over a term:
	- Party A pays a fixed rate $r_{\text{fix}}$ each period; receives a floating rate.
	- Party B pays a floating rate (e.g. SOFR + spread); receives fixed.
- Floating rate is referenced to a [[interest rates|market rate]] set on each prior fixing date.
- Each period only the difference is exchanged: if $r_{\text{fix}} > r_{\text{float}}$ this period, Party A pays Party B $(r_{\text{fix}} - r_{\text{float}}) \times N \times \tau$, where $\tau$ is the period length. If reversed, Party B pays Party A.
- Use case: a firm holding floating-rate debt enters a swap as Party A. The floating receipt cancels the debt's floating coupon; the fixed leg becomes the firm's net obligation. The firm has converted floating-rate debt into fixed-rate debt without retiring the original loan.

**Currency Swap**

- Two parties exchange streams in different currencies.
- Each pays the other interest in the partner currency on a notional denominated in that currency. Notionals are typically exchanged at the start and re-exchanged at the end (unlike interest-rate swaps, where they aren't).
- Use case: a US firm borrowing in euros to fund a European subsidiary swaps its euro interest obligation for dollar interest, neutralizing FX risk on debt service.

**Payoff Structure**

- Net cash flow each period: $(r_{\text{receive}} - r_{\text{pay}}) \times N \times \tau$.
- Across the swap's life, net P&L is the sum of these periodic differentials, discounted appropriately.
- A swap is fairly priced at inception when the present value of the expected receive-leg cash flows equals the present value of the expected pay-leg cash flows. Initial value to both parties is zero.
