- Raw line items from [[financial statements]] don't compare across firms or industries. A $1M profit means very different things for a corner shop and a multinational.
- Ratios normalize. They strip out scale and expose the economics — efficiency, leverage, profitability, the market's view.
- Five categories, each isolating one question about the firm. The DuPont identity then shows how the categories interact to produce shareholder return.

# Why Ratios

- Comparability is the entire point.
	- Same firm over time: did debt grow faster than assets?
	- Firm vs. industry: is this firm's gross margin above or below peers?
	- Segment vs. segment within one firm: which division generates return on its asset base?
- Absolute numbers can't answer any of these — scale dominates. Ratios can, because they cancel scale.
- Every input comes from the balance sheet, the income statement, or the market price of the firm's [[stocks|shares]].

# Liquidity Ratios

- Test whether the firm can pay short-term obligations as they come due.
- All compare current assets (or a stricter subset) to current liabilities. They differ in how strict the asset definition is.

**Current Ratio**

- $\text{Current} = \frac{\text{Current Assets}}{\text{Current Liabilities}}$
- Loosest measure. Includes inventory.
- $> 1$: current assets exceed current obligations. $< 1$: short-term insolvency risk if cash flow stalls.
- Industry-dependent. A grocer with fast-turning inventory runs $< 1$ safely; a manufacturer can't.

**Quick Ratio**

- Also called acid test.
- $\text{Quick} = \frac{\text{Current Assets} - \text{Inventory}}{\text{Current Liabilities}}$
- Excludes inventory. Tests whether the firm could pay obligations without selling stock — relevant when inventory is illiquid, slow, or potentially stale.

**Cash Ratio**

- $\text{Cash Ratio} = \frac{\text{Cash} + \text{Equivalents}}{\text{Current Liabilities}}$
- Strictest. Only counts what is already cash. Tests immediate solvency under a stress scenario where receivables stop collecting and inventory can't be sold.

# Asset Management Ratios

- Test how efficiently the firm converts its asset base into sales.
- High = efficient (many sales dollars per asset dollar). Low = bloated (idle assets, slow inventory, slow collections).

**Inventory Turnover**

- $\text{Inv Turnover} = \frac{\text{COGS}}{\text{Inventory}}$
- Number of times the firm cycles through its stock per year.
- Low: stock sitting unsold, capital tied up, obsolescence risk.
- High: rapid turnover; but very high may mean stockouts and lost sales.

**Days Sales Outstanding**

- $\text{DSO} = \frac{\text{Receivables}}{\text{Sales} / 365}$
- Average days from credit sale to cash collection.
- Long DSO: cash tied in receivables, exposure to bad debt, working capital strain.

**Fixed Assets Turnover**

- $\text{FAT} = \frac{\text{Sales}}{\text{Net Fixed Assets}}$
- Sales generated per dollar of plant and equipment specifically.
- Excludes current assets, isolating how productively the long-term operating assets are used.
- Low: too much fixed-asset capacity relative to demand. High: capacity-constrained or running lean.

**Total Asset Turnover**

- $\text{TAT} = \frac{\text{Sales}}{\text{Total Assets}}$
- Sales generated per dollar of all assets.
- Low: the firm has more assets than its sales support — underutilization, or recent capital expenditure yet to pay off.

# Debt Management Ratios

- Test leverage and solvency.
- Higher leverage amplifies equity returns in good times and equity losses in bad. These ratios quantify the trade-off.

**Debt Ratio**

- $\text{Debt Ratio} = \frac{\text{Total Debt}}{\text{Total Assets}}$
- Share of assets funded by debt.
- High: more fixed interest obligation, more vulnerability in a downturn.

**Debt-to-Equity**

- $\text{D/E} = \frac{\text{Total Debt}}{\text{Equity}}$
- Same information as debt ratio, expressed against the equity base. Useful for the DuPont decomposition below.

**Debt-to-Capital**

- $\text{Debt/Capital} = \frac{\text{Total Debt}}{\text{Total Debt} + \text{Equity}}$
- Share of long-term financing supplied by debt rather than equity. Equivalent to a normalized debt ratio that excludes operating liabilities (payables, accruals) from the denominator.
- Used when "capital" specifically means long-term funding sources, as in WACC computation.

**Times Interest Earned**

- $\text{TIE} = \frac{\text{EBIT}}{\text{Interest Expense}}$
- How many times operating profit covers the year's interest bill.
- $< 1$: operating profit can't cover interest. Imminent default risk.
- High: ample cushion; the firm can absorb a profit drop without missing payments.

# Profitability Ratios

- Test how much profit the firm extracts per dollar of sales, asset, equity, or invested capital.

**Operating Margin**

- $\text{Operating Margin} = \frac{\text{EBIT}}{\text{Sales}}$
- Operating profit per dollar of sales, before interest and taxes.
- Isolates operating performance from financing and tax decisions. A firm with weak operating margin and a strong profit margin is propping up the bottom line with non-operating items.

**Profit Margin**

- $\text{Profit Margin} = \frac{\text{Net Income}}{\text{Sales}}$
- Bottom-line profit per dollar of revenue, after interest and taxes.
- Industry-bound. Software firms run high; commodity producers run low.

**Basic Earning Power**

- $\text{BEP} = \frac{\text{EBIT}}{\text{Total Assets}}$
- Operating return on the asset base, independent of financing structure or tax rate.
- Lets analysts compare operating efficiency across firms with very different capital structures or jurisdictions. ROA mixes operating performance with financing decisions; BEP doesn't.

**Return on Assets**

- $\text{ROA} = \frac{\text{Net Income}}{\text{Total Assets}}$
- Profit per dollar of asset, regardless of how the asset was funded.
- Captures operating efficiency, mostly independent of capital-structure choice.

**Return on Equity**

- $\text{ROE} = \frac{\text{Net Income}}{\text{Equity}}$
- Profit per dollar of shareholder capital.
- The shareholder's headline number. Decomposed in the DuPont section below.

**Return on Invested Capital**

- $\text{ROIC} = \frac{\text{EBIT}(1 - t)}{\text{Debt} + \text{Equity}} = \frac{\text{NOPAT}}{\text{Invested Capital}}$
- After-tax operating return on the long-term capital tied up in the business. See [[free cash flow]] for NOPAT and invested capital.
- The metric for value creation. ROIC > WACC: the firm earns more on each dollar of capital than that capital costs — value created. ROIC < WACC: each dollar of growth destroys value.
- ROE alone can rise from leverage; ROIC strips that out, exposing operating return cleanly.

# Market Value Ratios

- Bring market price into the picture. Compare what the market pays to what the books say.

**Price-to-Earnings**

- $\text{P/E} = \frac{\text{Share Price}}{\text{EPS}}$
- Where $\text{EPS} = \text{Net Income} / \text{Shares Outstanding}$.
- Years of current earnings the market is willing to pay for one share.
- High P/E: market expects fast earnings growth or perceives low risk. Low P/E: weak growth expectations or distress.

**Book Value per Share**

- $\text{BVPS} = \frac{\text{Common Equity}}{\text{Shares Outstanding}}$
- Accounting equity divided by share count. The per-share counterpart to the equity line on the [[financial statements#Balance Sheet|balance sheet]].
- The denominator of the per-share P/B ratio.

**Price-to-Book**

- $\text{P/B} = \frac{\text{Price per Share}}{\text{BVPS}}$
- Market's premium (or discount) over accounting equity, on a per-share basis.
- $> 1$: the market values intangibles (brand, growth options, management) the books don't capture.
- $< 1$: the market thinks the recorded assets aren't worth their book value.

**Market-to-Book**

- Same ratio as P/B, expressed firm-wide rather than per-share.

**Enterprise Value / EBITDA**

- $\text{EV} = \text{MV(Equity)} + \text{MV(Debt)} + \text{MV(Preferred)} - \text{Cash}$
- $\text{EV/EBITDA} = \frac{\text{EV}}{\text{EBITDA}}$
- EBITDA = EBIT + Depreciation + Amortization. Operating profit before interest, taxes, and the two main non-cash charges.
- EV is the cost of acquiring the entire firm — paying off both equity and debt holders, less the cash that comes with the firm.
- The numerator (EV) and denominator (EBITDA) are both capital-structure-neutral: leverage shows up in both equally and cancels. Lets two firms with very different debt loads be compared on operating valuation.
- Used heavily in M&A and credit analysis where P/E breaks down for highly leveraged or unprofitable firms.

# DuPont Identity

- ROE alone doesn't reveal how it was achieved. Two firms with 15% ROE can have completely different operating profiles. Decomposition shows which lever is doing the work.
- $\text{ROE} = \frac{\text{NI}}{\text{Sales}} \times \frac{\text{Sales}}{\text{Assets}} \times \frac{\text{Assets}}{\text{Equity}}$
- The middle ratios cancel algebraically; the identity is a tautology. Its value is interpretive: each factor isolates one driver.

**Profit Margin**

- $\text{NI}/\text{Sales}$.
- Operating efficiency: how much profit per dollar of sales.

**Asset Turnover**

- $\text{Sales}/\text{Assets}$.
- Asset efficiency: how many sales dollars each asset dollar produces.

**Equity Multiplier**

- $\text{Assets}/\text{Equity} = 1 + D/E$.
- Leverage: how much asset is financed per dollar of equity.

**Reading the Decomposition**

- The same 15% ROE arises from very different profiles:
	- High margin, low turnover, low leverage: a luxury boutique.
	- Low margin, high turnover, low leverage: a supermarket.
	- Mid margin, mid turnover, high leverage: a bank.
- A jump in ROE driven by rising equity multiplier is risk-laden — leverage cuts both ways. A jump from rising margin or turnover is genuine operational improvement.

# Problems with ROE

- ROE is the headline shareholder ratio, but it has two structural blind spots that motivate the value-creation metrics in [[free cash flow]].
- ==Ignores risk==: a high ROE achieved by taking on more leverage or riskier investments looks identical to a high ROE from genuinely better operations. ROE doesn't price the risk taken to produce it.
- ==Ignores amount of capital invested==: a unit can grow ROE by shrinking the equity base (buybacks) without any operating improvement. ROE rises mechanically.
- These gaps are why EVA and MVA exist: they bring in the cost of capital and the size of the capital base directly.

# Limitations

- ==Industry dependence==: a 1.2 current ratio is alarming for a manufacturer, fine for a grocer. Compare within an industry, not across.
- ==Accounting-policy distortion==: depreciation method (straight-line vs. accelerated), inventory method (FIFO vs. LIFO), and revenue-recognition timing alter ratio inputs without any operating change. Cross-firm comparison breaks if methods differ.
- ==Window dressing==: management can time year-end transactions (paying down short-term debt the day before reporting, accelerating receivables collection) to make ratios look better than they are at the snapshot date.
- ==Seasonal distortion==: ratios computed at quarter-end can swing significantly across seasons for cyclical businesses (retail at year-end, agriculture at harvest). A single snapshot misleads.
- ==Inflation==: book values reflect historical cost; inflation makes old assets look cheap and depreciation understated, distorting ratios that use book values.
- ==Trend and benchmark over level==: a ratio's direction over time and relative position vs. industry peers carry more information than the absolute number. ==Benchmarking== compares against a chosen peer set; ==trend analysis== looks at the firm's own ratio history.
