- Net income is accounting profit. It's the wrong number for asking whether a firm is genuinely creating value.
- Three metrics fix this from different angles, all derived from [[financial statements]]:
	- ==Free cash flow== (FCF): cash actually available to all investors after running and reinvesting in operations.
	- ==Economic Value Added== (EVA): profit above the dollar cost of the capital it took to generate.
	- ==Market Value Added== (MVA): cumulative wealth the market thinks the firm has created for shareholders.

# Why Net Income Misleads

- Accrual accounting books revenue when earned, not when paid. A firm can report large profit while no cash arrives — receivables grow instead.
- Depreciation reduces net income but no cash leaves. The firm holds more cash than its profit number suggests.
- Capital reinvestment — buying new equipment, expanding inventory — drains cash but is not an expense (it's a capitalized asset). Net income ignores it; the cash position takes the hit.
- Net income also ignores the cost of equity. A firm that earns $100M on $10B of equity, when shareholders demand a 15% return, is destroying value. Net income shows positive; the value scoreboard shows negative.

# Free Cash Flow

- Cash left over after operating and reinvesting, available to be paid out to all investors (debt and equity).
- $\text{FCF} = \text{NOPAT} - \text{Net Investment in Operating Capital}$

**NOPAT**

- Net Operating Profit After Taxes.
- $\text{NOPAT} = \text{EBIT} \times (1 - t)$
	- $\text{EBIT}$ = Earnings Before Interest and Taxes from the [[financial statements#Income Statement|income statement]].
	- $t$ = corporate tax rate.
- Operating profit, after the government's share, before any financing decision.
- Strips out interest deliberately. A leveraged and an unleveraged firm with identical operations have identical NOPAT and identical FCF; capital structure shows up in the discount rate, not the cash flow.

**Net Investment in Operating Capital**

- Cash tied up this period in growing the business.
- $\text{Net Investment} = \Delta(\text{Operating Working Capital}) + \Delta(\text{Net PP&E})$
	- Operating working capital = operating current assets − operating current liabilities (excludes cash and short-term debt).
	- Net PP&E = gross PP&E − accumulated depreciation.
- Growing receivables and inventory absorb cash. Growing payables release cash. Buying new equipment absorbs cash.
- Subtracting it leaves only the cash not reinvested — actually free.

**Interpretation**

- FCF > 0: the firm can pay down debt, pay dividends, buy back shares, or accumulate cash without raising capital.
- FCF < 0: the firm must raise external capital to fund operations and growth.
- A young growing firm typically has FCF < 0 (heavy reinvestment); a mature firm typically has FCF > 0.

# Economic Value Added

- Capital is not free. Debt holders demand interest; equity holders demand return. Operating profit only counts as value if it exceeds the dollar cost of the capital used.
- $\text{EVA} = \text{NOPAT} - (\text{WACC} \times \text{Invested Capital})$

**WACC**

- Weighted Average Cost of Capital. The blended required return across the firm's debt and equity, weighted by their share of total financing.
- $\text{WACC} = \frac{D}{D+E} \, r_d (1 - t) + \frac{E}{D+E} \, r_e$
	- $D, E$ = market value of debt and equity.
	- $r_d$ = pre-tax cost of debt; the $(1 - t)$ factor reflects that interest is tax-deductible, so each dollar of interest saves $t$ dollars of tax.
	- $r_e$ = cost of equity, the return shareholders require for bearing the firm's equity risk.

**Invested Capital**

- Total long-term funding tied up in the business.
- $\text{Invested Capital} = \text{Long-Term Debt} + \text{Equity}$
- Equivalently from the asset side: net operating assets.

**Interpretation**

- EVA > 0: NOPAT exceeds the dollar cost of capital. Genuine value created this period.
- EVA < 0: the firm earns less than its capital costs. Net income may still be positive, but shareholders would have done better putting their money in a similar-risk alternative.
- A unit can have rising net income and falling EVA if it's growing the asset base faster than profit. EVA exposes this; net income hides it.

# Market Value Added

- The market's cumulative verdict on value creation.
- $\text{MVA} = \text{Market Value of Equity} - \text{Book Value of Equity}$
- Market value of equity = share price $\times$ shares outstanding. The market's price for the equity claim.
- Book value of equity = the equity line on the [[financial statements#Balance Sheet|balance sheet]]. Accounting record of capital paid in plus retained earnings.

**Interpretation**

- MVA > 0: the market values the firm above what was contributed in. Cumulative value created since inception.
- MVA < 0: the firm has destroyed shareholder wealth relative to what was put in.
- EVA is a single-period flow; MVA is the present value of all future expected EVAs. They answer the same question at different time horizons.

# When Each Applies

- ==FCF==: valuing the firm. Project FCF forward, discount at WACC, sum to get enterprise value. The input to a [[evaluation|DCF]] valuation.
- ==EVA==: judging this period's operating performance for compensation, budgeting, capital-allocation decisions. Did the unit beat its cost of capital?
- ==MVA==: external benchmarking. Has the firm's cumulative decision-making created or destroyed wealth, in the market's view?
