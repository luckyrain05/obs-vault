- Investors require return for bearing risk on holding [[financial assets]]. This file builds the measure of risk and the diversification mechanism that lets risk be reduced.
- Every asset pricing model follows the two questions: 
	- How risky is one asset on its own?
	- How risky is an asset as an addition to an existing portfolio?

# Utility Curves

- $U(W)$, the ==utility function==, maps wealth as the x-axis and utility as the y-axis. Utility represents what the individual can do with the money. 
- This function describes the psychological relationship of an individual with money. We assume higher utility to be higher satisfaction and happiness levels.

```desmos-graph
left=0; right=10; bottom=-3; top=7; grid=true
---
y=2\sqrt{x}|x>0|#5da5da
(9,6)|#5da5da|label:U(W)
```

- The second [[math/calculus/derivatives]], or $U''(W)$, then, would give us the acceleration of satisfaction with respect to the change in wealth.

```desmos-graph
left=0; right=10; bottom=-3; top=7; grid=true
---
y=-0.5/x^{1.5}|x>0|#5da5da
(1,-0.5)|#5da5da|label:U''(W)
```

# Investor Attitudes

**Risk Averse**

-  $U$ is concave, or formally $U''(W) < 0\ \ \forall \ W \in \mathbb{R}$.
- Each additional dollar adds less utility than the previous. Losing $x$ dollars would reduce more utility than the utility gained from an additional $x$ dollars. 
- We describe these investors to be ==risk averse==, they require higher returns on riskier investments to gain the same utility that they risk losing.

```desmos-graph
left=0; right=10; bottom=-3; top=7; grid=true
---
y=2\sqrt{x}|x>0|#5da5da
y=-0.5/x^{1.5}|x>0|#60bd68
(9,6)|#5da5da|label:U(W)
(1,-0.5)|#60bd68|label:U''(W)
```

**Risk Neutral**

- $U$ is linear, or $U''(W) = 0\ \ \forall \ W \in \mathbb{R}$. 
- Every dollar provides the same utility as the previous and the next.

```desmos-graph
left=0; right=10; bottom=-3; top=7; grid=true
---
y=0.5x|x>0|#5da5da
y=0|x>0|#60bd68
(10,5)|#5da5da|label:U(W)
(2,0)|#60bd68|label:U''(W)
```

**Risk Seeking**

- $U$ is convex, or $U''(W) > 0\ \ \forall \ W \in \mathbb{R}$. 
- Each additional dollar provides more utility than the previous. 
- Risk seeking investors requires less returns on riskier investments, for they need to make less additional money to match the utility they risk.

```desmos-graph
left=0; right=10; bottom=-3; top=7; grid=true
---
y=0.05x^{2}|x>0|#5da5da
y=0.1|x>0|#60bd68
(10,5)|#5da5da|label:U(W)
(2,0.1)|#60bd68|label:U''(W)
```

- Every risk model assumes risk aversion, or at least risk neutral investors.

# Expected Return

- The probability-weighted average of outcomes.
$$E[r] = \sum_{i=1}^n p_i \, r_i$$
- For every outcome $i$, its probability $p$, and its returns $r$. 
- An investment that would either return $\$100$ or nothing has a expected return of $0.5\times0+0.5\times100=\$50$ 

# Probability Distribution of Returns

- Discrete framing: the future is one of $n$ mutually exclusive states. State $i$ has probability $p_i$ and produces return $r_i$.
- $\sum_{i=1}^n p_i = 1$
- Continuous framings exist (e.g. log-normal price assumption used in [[evaluation|DCF]] extensions and Black-Scholes), but discrete is enough for the mechanics here.

# [[standard deviation]]

- The measure of how far returns spread around the expected value.
- $\sigma = \sqrt{\sum_{i=1}^n p_i \, (r_i - E[r])^2}$
- Mechanism, in three steps:
	- For each state, compute the deviation from the expected value: $r_i - E[r]$.
	- Square it. Negative and positive deviations both contribute equally; large deviations are penalized more than proportionally.
	- Probability-weight the squared deviations and sum. This is the ==variance== $\sigma^2$. The square root brings the units back to return units.
- Why squared rather than absolute deviation:
	- Smooth (differentiable), so optimization works.
	- Additive across independent variables: $\text{Var}(X + Y) = \text{Var}(X) + \text{Var}(Y)$ when $X, Y$ are independent. This makes portfolio variance computable from pairwise covariances.
	- Connects directly to the normal distribution and to most parametric statistics.

**Historical Estimation**

- The probability-weighted formula assumes the distribution is known. In practice it isn't; σ is estimated from past returns.
- $\sigma = \sqrt{\frac{1}{N-1} \sum_{t=1}^N (r_t - \bar{r})^2}$
	- $r_t$ = return in period $t$ (e.g. monthly).
	- $\bar{r}$ = sample mean of returns.
	- $N - 1$ in the denominator (==Bessel's correction==) instead of $N$, because using the sample mean to compute deviations costs one degree of freedom.
- Assumes the future distribution resembles the past. Reasonable over short horizons in stable regimes; fails when business mix or risk profile has shifted.

# Coefficient of Variation

- Risk per unit of expected return.
- $\text{CV} = \frac{\sigma}{E[r]}$
- When two assets differ in $E[r]$, σ alone is misleading. A 5% σ on a 4% expected return is much riskier per unit than a 5% σ on a 20% expected return. CV normalizes.
- Use CV to rank assets that have very different expected returns.

# Sharpe Ratio

- Excess return per unit of risk.
- $S = \frac{E[r] - r_f}{\sigma}$
- $r_f$ = the [[interest rates|risk-free rate]] (e.g. T-bill yield).
- Mechanism: how much extra return — above the riskless alternative — is earned per unit of standard deviation taken. Geometrically, $S$ is the slope of the line from $(0, r_f)$ on a $(\sigma, E[r])$ plot to the asset's point at $(\sigma, E[r])$.
- Higher Sharpe = better risk-adjusted return. It is the standard ranking criterion when comparing portfolios with different risk levels.

# Portfolio Risk

- A portfolio holds multiple assets in weights $w_i$ summing to 1.

**Portfolio Return**

- $E[r_p] = \sum_i w_i \, E[r_i]$
- The expected return of a portfolio is a simple weighted average of individual expected returns.

**Portfolio Variance**

- For two assets:
- $\sigma_p^2 = w_1^2 \sigma_1^2 + w_2^2 \sigma_2^2 + 2 \, w_1 w_2 \, \sigma_{12}$
	- $\sigma_{12} = \rho_{12} \, \sigma_1 \, \sigma_2$ is the covariance.
	- $\rho_{12} \in [-1, 1]$ is the correlation coefficient.
- This is NOT a weighted average. The cross term depends on how the two assets move together. If they move in the same direction, the cross term is large and positive — risk adds. If they move oppositely, the cross term is negative — risk cancels.
- For $n$ assets:
- $\sigma_p^2 = \sum_i \sum_j w_i w_j \, \sigma_{ij}$
- Built from every pair's covariance, weighted by the product of the pair's weights.

# Diversification

- When $\rho < 1$, portfolio σ is less than the weighted average of the individual σ's. Mechanism: opposing deviations cancel.
- Take two assets with $\sigma_1 = \sigma_2$ and $\rho = 0$. State A: asset 1 is $+5\%$, asset 2 is $+5\%$. State B: asset 1 is $+5\%$, asset 2 is $-5\%$. The 50/50 portfolio is $+5\%$ in A, $0\%$ in B. Each individual asset is more variable than the mix.
- Boundary cases:

```
+--------+-----------------------------------------+
| rho    | Portfolio sigma vs. weighted average    |
+--------+-----------------------------------------+
|  +1    | Equal. Lockstep movement. No benefit.   |
|   0    | Below. Independent. Real benefit.       |
|  -1    | Can reach 0 with right weights.         |
+--------+-----------------------------------------+
```

- Real-world correlations across stocks are positive but well below 1 (typically 0.2–0.6), so diversification works in practice.

# Diversifiable vs. Market Risk

- As $n$ assets are added to a portfolio (equal weights $w_i = 1/n$), the variance terms split into two groups with very different fates:
- ==Own-variance terms== ($w_i^2 \sigma_i^2$): there are $n$ of them. Each scales as $1/n^2$. Sum is $O(1/n)$ — vanishes as $n$ grows.
- ==Cross-covariance terms== ($w_i w_j \sigma_{ij}$ for $i \ne j$): there are $n(n-1)$ of them. Each scales as $1/n^2$. Sum approaches the average covariance — does not vanish.
- The conclusion:

**Diversifiable Risk**

- Also called idiosyncratic or firm-specific risk.
- The component of σ that comes from individual-asset noise — earnings surprises, lawsuits, supply shocks specific to one firm.
- Diluted to zero as $n$ grows. Investors holding broad portfolios bear none of it.

**Market Risk**

- Also called systematic or non-diversifiable risk.
- The component that comes from common movement across all assets — recessions, rate moves, broad shocks.
- Survives no matter how many assets are added. The floor below which σ cannot be reduced.

**The Seam**

- Stand-alone σ measures total risk: diversifiable + market.
- In equilibrium, only market risk earns return. Investors who could have diversified but didn't are not compensated for the avoidable risk they chose to bear.
- Pricing return therefore requires a measure of an asset's exposure to market movements specifically — not its total σ.
- That measure is ==beta==. The model that uses beta to price required return is [[CAPM]].
