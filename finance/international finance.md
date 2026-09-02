- A firm operates internationally when its inputs, customers, financing, or operations cross currency boundaries.
- Cash flows in different currencies introduce risks a purely domestic firm doesn't face: exchange-rate moves, political risk, multiple legal and tax systems.
- Six interlocking topics:
	- Why firms go multinational.
	- The [[financial assets|FX market]] and how rates are quoted.
	- Exchange-rate regimes: how rates are set.
	- Interest Rate Parity: links FX rates to interest rate differentials.
	- Purchasing Power Parity: links FX rates to inflation differentials.
	- FX risk types and hedging via [[forwards futures swaps]] and [[options]].

# Why Multinational Operations

- Five drivers push firms across borders. Each is a different cost or opportunity, not interchangeable.
- ==Production efficiency==: cheaper labor or raw materials in another country lower unit costs.
- ==Market access==: selling to consumers in countries the firm can't reach from home.
- ==Resource access==: commodities, technology, IP, or talent concentrated abroad.
- ==Regulatory and tax arbitrage==: differences in regulation or tax burden across jurisdictions.
- ==Risk diversification==: economic shocks rarely hit all countries at once. A firm with revenue across regions absorbs domestic shocks better.

**What Differs from Domestic Operations**

- ==Currency denomination==: revenues and costs in different units. The home-currency value of foreign cash flows moves with the FX rate.
- ==Political risk==: expropriation, capital controls, sudden regulation in the host country. No analogue domestically.
- ==Legal and tax systems==: different contract enforcement, accounting rules, tax codes per jurisdiction.
- ==Cultural and language barriers==: friction in operations and customer relations. Not a cash flow but a cost.
- ==Government role==: in some countries the state is a major commercial actor, partner, or competitor.

# Exchange Rates

- ==Exchange rate==: the price of one currency in another.
- The FX market is the largest financial market by daily volume. Trading happens 24 hours over an OTC dealer network.

**Direct vs. Indirect Quotation**

- ==Direct quote== (from a home perspective): home currency per unit of foreign. US direct quote of EUR: $1.10/€.
- ==Indirect quote==: foreign currency per unit of home. US indirect quote of EUR: €0.91/$.
- The two are reciprocals: $\text{indirect} = 1 / \text{direct}$.

**Cross Rate**

- The exchange rate between two non-home currencies, computed via a third (typically USD).
- $\frac{\text{GBP}}{\text{JPY}} = \frac{\text{GBP}}{\text{USD}} \times \frac{\text{USD}}{\text{JPY}}$
- Mechanism: most liquidity is paired against USD. A direct GBP/JPY trade is built by chaining two USD legs at the dealer level.

**Spot Rate**

- $S$ — the rate for immediate delivery. Settled T+2 by convention.

**Forward Rate**

- $F$ — the rate set today for a delivery at a specified future date.
- ==Forward premium==: $F > S$. The forward currency is more expensive than the spot.
- ==Forward discount==: $F < S$.
- Forwards trade for standard tenors (1M, 3M, 6M, 12M) and as customized OTC contracts. See [[forwards futures swaps#Forward|forward mechanics]].

**Appreciation vs. Depreciation**

- ==Appreciation==: a currency's market value rises against another. The home currency now buys more foreign currency.
- ==Depreciation==: the opposite.
- Floating-regime moves; no government action involved.

**Devaluation vs. Revaluation**

- Official changes set by a government in a fixed or managed regime.
- ==Devaluation==: lowering the official rate (the home currency now buys less foreign).
- ==Revaluation==: raising it.

# Exchange Rate Regimes

- A country's regime is the rule that determines its rate. Regimes sit on a spectrum from full market clearing to full government control.

**Freely Floating**

- Rate set entirely by FX market supply and demand. No government intervention.
- Mechanism: the central bank lets the rate clear at whatever level matches order flow.
- USD, EUR, JPY, GBP.

**Managed Floating**

- Mostly market-driven, but the central bank intervenes when moves are deemed disruptive.
- Mechanism: the central bank buys or sells reserves to lean against extreme moves without committing to a level.
- Most emerging-market currencies.

**Fixed Peg**

- The central bank commits to a fixed rate against another currency or a basket.
- Mechanism: defended by FX-market intervention. If demand pushes the home currency below the peg, the central bank sells foreign reserves and buys home currency. If above, it sells home currency and buys reserves.
- Risk: if reserves run out under sustained pressure, the peg breaks. Currency crises (Asia 1997, GBP 1992) followed this pattern.

**Currency Board**

- Fixed peg backed by 100% foreign-reserve coverage of the local monetary base.
- Mechanism: the board only issues local currency in exchange for foreign currency at the fixed rate, and only retires it by exchanging back. No discretion.
- More credible than a soft peg because no fiat issuance can undermine the rate.

**No Local Currency**

- The country adopts another nation's currency outright (==dollarization==) or joins a monetary union (==Eurozone==).
- Eliminates FX risk against the adopted currency.
- Cost: surrenders independent [[monetary policy]]. The adopting country can no longer set its own interest rates or print money in response to local shocks.

# Interest Rate Parity

- A no-arbitrage relationship linking spot rate, forward rate, and the [[interest rates|interest rates]] in two currencies.
- An investor must earn the same return investing at home or abroad with the FX risk fully hedged via a forward. Otherwise free money exists.

**Two-Route Mechanism**

- Investor with 1 unit of home currency, one period horizon. Two routes:
	- Route A: invest at home rate $r_h$. End with $1 + r_h$.
	- Route B: convert to foreign at spot $S$ (foreign per home), invest at $r_f$, lock in conversion back at forward $F$. End with $\frac{1}{S}(1 + r_f) \cdot F$.
- For no arbitrage, the two must be equal:
- $1 + r_h = \frac{F}{S}(1 + r_f)$
- Rearranging:
- $\frac{F}{S} = \frac{1 + r_h}{1 + r_f}$
- Approximation for small rates: $F \approx S \times (1 + r_h - r_f)$.

**Implication**

- The currency with the higher interest rate trades at a ==forward discount== (its forward rate is below its spot).
- The forward locks away the rate differential. A "high-yield" currency offers no extra return when fully hedged — the forward conversion gives back exactly the rate advantage gained on the deposit.
- Carry trades (borrow low-yield, invest high-yield without hedging) earn the differential by accepting unhedged FX risk. They are not free returns; they are paid for bearing the risk that IRP locks away.

# Purchasing Power Parity

- A long-run relationship linking spot rates to inflation differentials.
- Identical traded goods should cost the same in every country, once prices are converted to a common currency. If not, arbitrage moves goods until prices equalize.

**Absolute PPP**

- $S = \frac{P_h}{P_f}$
- Spot rate (foreign per home) equals the ratio of price levels.
- Strong assumption: holds for a basket of identical traded goods, frictionless transport, no tariffs. Real-world deviations are large.

**Relative PPP**

- $\frac{S_t}{S_0} = \frac{1 + \pi_h}{1 + \pi_f}$
- The change in the spot rate equals the inflation differential.
- Mechanism: a country with higher inflation has its currency lose purchasing power faster. To keep traded-goods prices in line internationally, the high-inflation currency must depreciate against the low-inflation currency.
- Example: 5% home inflation, 2% foreign inflation. Home currency depreciates roughly 3% per year against foreign in equilibrium.

**Why PPP Deviates Short-Run**

- Transport costs and tariffs prevent goods arbitrage on the margin.
- Non-traded goods (services, real estate) don't arbitrage at all.
- Sticky prices: contracts and menu costs delay price adjustment.
- Capital flows dominate goods flows in the short run, moving FX rates faster than prices can adjust.
- PPP holds on average over long horizons (decades), poorly over short ones (months to years).

# FX Risk and Hedging

- Three types of FX exposure, each with a different cash-flow consequence and a different hedging fit.

**Transaction Risk**

- A specific contracted future cash flow in foreign currency. The home-currency value depends on the spot rate at the cash-flow date.
- Example: a US firm sells goods to a German buyer for €1M, payable in 90 days. The dollar value of that €1M depends on the EUR/USD spot rate in 90 days.
- Hedge: a [[forwards futures swaps#Forward|forward]] locks in the rate today (eliminates uncertainty, gives up favorable moves). A [[options#Put|put option on the foreign currency]] locks in a worst case and preserves upside, paying a premium.

**Translation Risk**

- Foreign-subsidiary [[financial statements]] must be converted to home currency for consolidation. Reported earnings and equity move with FX rates even if no cash flow occurs.
- Largely an accounting concern. Affects reported ratios and can affect debt covenants, but not cash directly.
- Hedging is partial; some firms use balance-sheet hedges (matching foreign assets with foreign liabilities) rather than derivatives.

**Economic Risk**

- The firm's long-run competitive position depends on FX rates. A persistently strong home currency raises the foreign-currency price of home-produced exports, shrinking foreign demand.
- Hardest to hedge — the exposure is to long-run business fundamentals, not a specific contracted cash flow.
- Mitigation is operational: produce where you sell, diversify across currencies, build pricing flexibility into contracts.

**Hedging Instruments**

- ==FX forwards==: lock in a future rate. Symmetric payoff. See [[forwards futures swaps#Forward]].
- ==FX futures==: same payoff, exchange-traded with daily mark-to-market. See [[forwards futures swaps#Future]].
- ==Currency options==: lock in a worst-case rate while preserving favorable upside. See [[options]].
- ==Currency swaps==: exchange streams of cash flows in two currencies, used for long-dated debt-service hedging. See [[forwards futures swaps#Currency Swap]].
