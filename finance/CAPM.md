- ==Capital Asset Pricing Model== prices the compensation investors demand for bearing the market risk that [[risk analysis#Diversifiable vs. Market Risk|cannot be diversified away]].
- Builds directly on [[risk analysis]]. The diversifiable/market split is the foundation; CAPM provides the per-asset price.
- Output: a single linear equation giving the required return on any asset, given its sensitivity to market movements.

# Why CAPM

- [[risk analysis]] established that in equilibrium only market risk earns return — diversifiable risk vanishes in a broad portfolio, so investors who could have diversified but chose not to are not compensated for the avoidable risk.
- The remaining question: how much return per unit of market-risk exposure?
- The answer requires a per-asset measure of "exposure to market movements." Total σ won't do — it includes the diversifiable component. The right measure is ==beta==.

# Beta

- The asset's covariance with the market, normalized by market variance.
- $\beta_i = \frac{\text{Cov}(r_i, r_m)}{\sigma_m^2}$
- Equivalently: the slope when asset returns are regressed on market returns.
- Mechanism: β isolates the part of the asset's variability that moves with the market (the priced part) from the part that doesn't (the diversifiable noise).

**Interpretation by Range**

- $\beta = 1$: asset moves one-for-one with the market on average. The market itself has $\beta = 1$ by construction.
- $\beta > 1$: amplifies the market. A 10% market swing produces roughly a $\beta \times 10\%$ swing in the asset. Cyclicals, leveraged firms, high-growth tech.
- $0 < \beta < 1$: dampens the market. Utilities, consumer staples, regulated industries.
- $\beta = 0$: uncorrelated with the market. The risk-free asset is here by construction.
- $\beta < 0$: moves opposite the market on average. Requires negative correlation with the market. Rare in practice — some hedges, gold in certain regimes.

**Portfolio Beta**

- The β of a portfolio is the weighted average of its constituents' βs.
- $\beta_p = \sum_i w_i \beta_i$
- Mechanism: covariance is linear in either argument, so the covariance of a weighted sum with the market is the weighted sum of covariances. Dividing by $\sigma_m^2$ preserves the linearity.
- Implication: portfolio required return can be computed two equivalent ways:
	- Weighted average of each asset's CAPM-required return.
	- CAPM applied directly to the portfolio's β.
	- Both yield the same number.

**Estimation**

- β is not observed. Standard estimate: regress historical asset returns on historical market returns (typically 5 years of monthly data); the slope is the estimated β.
- Estimates are noisy and unstable across windows. The β a firm exhibits over the next year may differ from the historical slope, especially when the firm's leverage or business mix has changed.

# Market Risk Premium

- The extra return investors demand for holding the market portfolio rather than the risk-free asset.
- $\text{MRP} = E[r_m] - r_f$
- $r_f$ is the [[interest rates|risk-free rate]] (T-bill yield, conventionally).
- $E[r_m]$ is the expected return on the broad market portfolio (typically proxied by a broad index like the S&P 500).
- Mechanism: the market price of one unit of market-risk exposure. Empirically positive on the order of 4–8% over long horizons; the exact value is debated, the sign is not.

# The CAPM Equation

- $E[r_i] = r_f + \beta_i \, (E[r_m] - r_f)$
- Read as: required return = compensation for time + compensation for market risk borne.
- Three pieces:
	- $r_f$: payment for deferring consumption, no risk involved.
	- $E[r_m] - r_f$: per-unit price of market-risk exposure.
	- $\beta_i$: quantity of market-risk exposure carried by asset $i$.
- Linear in β. Geometrically a line.

# Security Market Line

- The geometric expression of the CAPM equation. Plot $E[r]$ vertically and $\beta$ horizontally.
- Every correctly-priced asset lies on a single straight line — the ==SML==.
	- Intercept at $\beta = 0$: $r_f$.
	- Slope: MRP.

```
 E[r] |
      |                                  . SML
      |                              .
      |                          .
 E[rm]|----------------------*               (asset with beta = 1)
      |                  .   |
      |              .       |
      |          .           |
   rf |------*               |               (beta = 0, risk-free)
      |  .                   |
      +----------------------+----------- beta
         0                   1
```

**Underpricing**

- An asset above the SML offers more return than its β justifies. Buying it is profitable until demand drives the price up and the expected return falls back onto the line.

**Overpricing**

- An asset below the SML offers less return than its β requires. Holders sell until the price drops and the expected return rises back to the line.

**Equilibrium**

- In equilibrium every asset lies on the SML. Deviations are arbitrage opportunities that close as investors trade.

# Factors That Shift the SML

- The SML is defined by two parameters: intercept $r_f$ and slope MRP. A change in either moves the line, and the two move it in geometrically different ways.

**Inflation Shift**

- Rising inflation expectations push the risk-free nominal rate up: investors demand the same real return plus the higher expected inflation.
- $r_f$ rises by the change in expected inflation; MRP is unchanged.
- The SML shifts up in parallel. Required return rises by the same amount at every β.

**Risk-Aversion Shift**

- Increased investor risk aversion pushes up the MRP: investors demand more extra return per unit of market risk.
- $r_f$ unchanged; slope steepens.
- The SML rotates upward, pivoting around the intercept at $\beta = 0$. Required return rises more for high-β assets than for low-β ones — high-β assets fall in price more in a risk-aversion shock.

# Required Return as Discount Rate

- For valuation, $E[r_i]$ from CAPM is the discount rate applied to the asset's expected future cash flows.
- Higher β → higher required return → lower [[evaluation|present value]] for the same cash flows.
- This is the channel by which market risk reduces an asset's price: not directly through the cash flows, but through the rate at which they're discounted.

# Assumptions and Limits

- ==Single period==: CAPM is a one-period model. Multi-period extensions (intertemporal CAPM) exist but don't fit here.
- ==Homogeneous expectations==: all investors agree on means, variances, covariances. In reality they don't.
- ==Everyone holds the market portfolio==: in reality investors deviate (home bias, sector bets, illiquid assets they can't trade).
- ==β is estimated from historical regression==: estimates are noisy. The β measured this year may not be the β next year, especially for firms whose business mix is changing.
- ==Empirical fit is mixed==: realized average returns line up with β only loosely. Size and value factors explain return variation CAPM doesn't capture. Multi-factor models (Fama-French) extend the framework but stay outside this file.
