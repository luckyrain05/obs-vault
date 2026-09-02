- The standardized window into a [[business entities|corporation's]] financial state.
- Required reading for investors deciding whether to hold equity or debt, creditors deciding whether to lend, and regulators enforcing disclosure law.
- Three views of the same firm at the same time, plus a bridge:
	- ==Balance sheet==: stock of value, at one instant.
	- ==Income statement==: flow of accounting profit, over a period.
	- ==Cash flow statement==: flow of actual cash, over the same period.
	- ==Statement of stockholders' equity==: bridge from net income to ending equity.

# Why Statements Exist

- A firm is opaque from the outside. Outsiders cannot inspect operations, contracts, or asset condition directly.
- Without a standardized disclosure, every investor would need a private audit to value the firm. The cost of capital would explode.
- ==GAAP== in the US and ==IFRS== internationally are accounting standards that fix what the statements contain and how items are measured. A line that says "Revenue: $100M" under GAAP means the same thing across firms.
- Each statement answers a distinct question:
	- Balance sheet: what does the firm own, what does it owe, right now?
	- Income statement: how much did the firm earn this period?
	- Cash flow statement: how much cash actually moved in and out?
	- Statement of stockholders' equity: how did equity change between periods?

# Balance Sheet

- A snapshot at one instant. Dated, not period-based.
- The ==accounting identity==: $A = L + E$. Every dollar of asset is funded by either a liability (creditor's claim) or equity (shareholder's claim).
- This is identity by construction, not approximation. Every transaction touches both sides:
	- Buy a $100 machine with cash: PP&E up $100, cash down $100. Both sides unchanged.
	- Borrow $100: cash up $100, long-term debt up $100. Both sides up by $100.

**Assets**

- Resources controlled by the firm with future economic benefit.
- Listed top-down in order of liquidity.

**Current Assets**

- Convertible to cash within one year.
- ==Cash and equivalents==: physical cash plus money-market instruments (T-bills, commercial paper) maturing in 90 days or less.
- ==Accounts receivable==: amounts owed by customers from credit sales not yet collected.
- ==Inventory==: raw materials, work in progress, finished goods awaiting sale.

**Fixed Assets**

- Held more than one year. Also called non-current assets.
- ==Property, plant, equipment== (PP&E): land, buildings, machinery, vehicles, less accumulated ==depreciation==.
- Depreciation: each period a fraction of the asset's cost is moved from the balance sheet to the income statement as expense, reflecting use-up. Net PP&E on the balance sheet equals original cost minus all depreciation taken so far.
- ==Intangibles==: patents, trademarks, goodwill (excess paid in an acquisition over fair value of net assets).

**Liabilities**

- External claims on the firm's assets.

**Current Liabilities**

- Due within one year.
- ==Accounts payable==: amounts owed to suppliers from credit purchases.
- ==Short-term debt==: notes and loans due within a year.
- ==Accrued expenses==: obligations recognized but not yet paid (wages, taxes, interest).

**Long-Term Liabilities**

- Due after one year.
- Bonds payable, long-term loans, lease obligations, deferred tax liabilities.

**Equity**

- The residual claim: $E = A - L$. Everything left after liabilities are settled belongs to shareholders.
- ==Common stock== plus ==additional paid-in capital==: cash received from issuing shares, split between par value and the excess paid above par.
- ==Retained earnings==: cumulative net income minus cumulative dividends since inception. Earnings the firm reinvested rather than paid out.
- ==Treasury stock==: shares the firm repurchased. A contra-equity account, subtracted from equity.

# Income Statement

- A flow over a period (quarter, year). The date alone says nothing.
- Revenue minus expenses, walked in a specific order to expose intermediate profitability subtotals. Each subtotal isolates one decision domain (operations, financing, taxation).

**Revenue**

- Sales of goods or services, recognized when ==earned==, not when cash arrives.
- Earned means: goods delivered or service performed, payment expected. A sale on credit produces revenue today and a receivable on the balance sheet, no cash movement.

**Cost of Goods Sold**

- Direct costs of producing what was sold: raw materials, direct labor, factory overhead.
- Scales with units produced and sold.

**Gross Profit**

- $\text{Revenue} - \text{COGS}$.
- Tests core production economics. Negative gross profit means the firm loses money on every unit before any overhead is paid.

**Operating Expenses**

- Costs of running the firm not tied directly to production.
- Selling, general, and administrative expenses (SG&A): salaries for non-production staff, rent, marketing.
- Research and development.
- Depreciation and amortization on operating assets.

**EBIT**

- Earnings Before Interest and Taxes, also called operating income.
- $\text{EBIT} = \text{Gross Profit} - \text{Operating Expenses}$.
- Captures operating performance before any financing decision (interest) or jurisdiction effect (taxes). Lets analysts compare firms with different capital structures or tax situations on equal terms.

**Interest Expense**

- Cost of debt financing. Coupon paid on bonds, interest on loans.
- Subtracted from EBIT to get pre-tax income.

**Taxes**

- Income tax owed: tax rate times pre-tax income, after deductions.

**Net Income**

- The bottom line. $\text{NI} = \text{EBIT} - \text{Interest} - \text{Taxes}$.
- Goes either to ==dividends== or to ==retained earnings==. The split is set by the board.

# Statement of Stockholders' Equity

- Bridges the income statement to the equity section of the balance sheet.
- $\text{End Equity} = \text{Beg Equity} + \text{NI} - \text{Dividends} + \text{New Stock Issued} - \text{Treasury Stock Repurchased}$
- Equity changes from sources other than just net income (issuing shares, buying back shares, paying dividends). Without this statement, two consecutive balance sheets would not reconcile.

# Cash Flow Statement

- A flow over a period. Tracks actual cash movement, ignoring accruals.
- The income statement uses ==accrual accounting==: revenue when earned, expense when incurred, regardless of cash. The cash flow statement undoes accruals to show the real cash movement.
- Three categories. The sum equals total change in cash, which must match the change in the cash line on the balance sheet.

**Operating Activities**

- Cash generated by running the business.
- ==Indirect method== (the standard): start from net income, then adjust to convert accrual profit into cash.
	- Add back non-cash expenses: depreciation, amortization. These reduced net income but no cash left the firm.
	- Adjust for working capital changes:
		- Receivables up: revenue was booked but cash not received. Subtract.
		- Inventory up: cash was spent on stock not yet sold. Subtract.
		- Payables up: expense was booked but cash not paid. Add.
- Positive net income with negative operating cash flow is a red flag. Earnings exist on paper but no cash is materializing — usually because receivables or inventory ballooned.

**Investing Activities**

- Cash from buying or selling long-term assets.
- ==Capital expenditure== (capex): cash spent on PP&E. Negative for a growing firm.
- Acquisitions or divestitures of other businesses.
- Purchase or sale of marketable securities held as investments.

**Financing Activities**

- Cash from raising or paying back capital.
- Issuing stock: cash in. Repurchasing stock: cash out.
- Issuing debt: cash in. Repaying principal: cash out.
- Paying dividends: cash out. Note interest payments are in operating, not financing — an accounting convention.

# Articulation

- The four statements are not independent. They tie together through three specific bridges.

```
+----------------------------+
|  Income Statement          |
|  Revenue - Expenses        |
|  = Net Income              |
+--------------+-------------+
               |
               | (NI - Dividends)
               v
+----------------------------+      +----------------------------+
|  Stmt of Stockholders' Eq  |      |  Cash Flow Statement       |
|  Beg Equity                |      |  Operating CF              |
|  + NI                      |      |  + Investing CF            |
|  - Dividends               |      |  + Financing CF            |
|  + Issue / - Repurchase    |      |  = Change in Cash          |
|  = End Equity              |      +--------------+-------------+
+--------------+-------------+                     |
               |                                   |
               v                                   v
+--------------------------------------------------------------+
|             Balance Sheet (period end)                        |
|                                                               |
|  Assets:                                                      |
|    Cash <------------------------------- (+ Change in Cash)   |
|    Receivables, Inventory, PP&E, ...                          |
|                                                               |
|  = Liabilities                                                |
|  + Equity (Retained Earnings) <-------- (End Equity)          |
+--------------------------------------------------------------+
```

- ==Net income== flows into ==retained earnings== on the balance sheet, routed through the statement of stockholders' equity.
- ==Change in cash== from the cash flow statement equals the change in the cash line between two consecutive balance sheets.
- Period-end balance sheet = period-start balance sheet plus all changes accumulated across the other three statements.
