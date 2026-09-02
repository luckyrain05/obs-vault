- A ==derivative== is a contract whose value is derived from an underlying asset.
- Underlyings include [[stocks]], [[bonds]], commodities, interest rates, foreign-exchange rates, and indexes.
- Traded on exchanges or over the counter via [[financial assets|broker-dealer networks]].
- Used to transfer risk between parties: one side wants to shed a price exposure, the other accepts it for a fee.
- Four categories — forward, future, option, swap — split along whether both parties are obligated (==symmetric==) or only one (==asymmetric==). The mechanism for each lives in [[options]] and [[forwards futures swaps]].

# Why Derivatives Exist

- Risk transfer.
- A wheat farmer in March wants certainty about his September selling price. A baker in March wants certainty about his September buying price. Each carries a price risk the other side wants to neutralize. A derivative pairs them: the farmer locks in a sell price, the baker locks in a buy price, and the spot price in September no longer matters to either.
- Without derivatives both parties self-insure: hold extra cash, store extra inventory, accept worse outcomes from price swings. With derivatives each keeps the risk it wants and sheds the rest at a price.
- Two distinct uses follow from the same instrument:
	- ==Hedging==: an existing exposure is offset.
	- ==Speculation==: a new exposure is taken on, betting on a price move. Same contract, opposite intent.

# The Four Categories

**Forward**

- Bilateral, customized contract to exchange an asset for a fixed price at a future date. OTC.
- Both sides obligated to perform at maturity. No money changes hands at signing.
- Mechanism, payoffs, counterparty risk: [[forwards futures swaps]].

**Future**

- A standardized, exchange-traded forward with daily mark-to-market and a clearinghouse standing between the two sides.
- Both sides obligated.
- Mechanism, daily settlement, margin: [[forwards futures swaps]].

**Option**

- Gives the holder the right but not the obligation to buy (call) or sell (put) the underlying at a strike price.
- Asymmetric: the holder has discretion, the writer is obligated only if the holder exercises.
- Holder pays a ==premium== up front for that asymmetry.
- Mechanism, payoffs, valuation: [[options]].

**Swap**

- Periodic exchange of cash flows between two parties — typically fixed-rate vs. floating-rate, or one currency vs. another.
- Both sides obligated to make their respective payments each period.
- Mechanism: [[forwards futures swaps]].

# Symmetric vs. Asymmetric Payoff

- The defining structural divide. It justifies splitting derivatives across two child files.

**Symmetric**

- Forwards, futures, swaps. Both parties perform regardless of where the underlying ends up.
- Gains for one side equal losses for the other. Zero-sum at every spot price.
- No premium up front (in principle): the contract is struck so both sides start at fair value.

**Asymmetric**

- Options. The holder pays a premium and then has discretion to exercise or walk away.
- Holder's payoff is bounded below by the premium paid (loss limited) and unbounded above. Writer's payoff mirrors: bounded above by the premium collected, unbounded loss below.
- The premium is the price of that asymmetry — paid up front because the cash flows are not symmetric like a forward's.

# Hedging

- Take a derivative position whose payoff moves opposite an existing exposure. The two positions sum to a near-constant outcome regardless of where the underlying ends up.
- The hedger keeps the certainty and gives up the upside that would have come if the spot price moved favorably.

**Long Hedge**

- Lock in a future buy price. The hedger will need to buy the asset later and fears the price rising.
- Take a long position in a derivative on the asset (long forward, long future, long call). If the spot price rises, the derivative pays off, offsetting the higher purchase cost.
- Examples: manufacturers needing raw materials, importers needing foreign currency in three months.

**Short Hedge**

- Lock in a future sell price. The hedger will sell the asset later and fears the price falling.
- Take a short position in a derivative (short forward, short future, long put). If the spot price falls, the derivative pays off, offsetting the lower sale price.
- Examples: farmers selling crops at harvest, oil producers, exporters expecting foreign-currency receipts.

**Hedging vs. Speculation**

- Same instrument, opposite starting position. The hedger already has spot exposure and uses the derivative to neutralize it. The speculator has no spot exposure and uses the derivative to take one.
- A long call held against an upcoming purchase is a hedge; the same long call held against nothing is a speculative bet that the underlying will rise.
