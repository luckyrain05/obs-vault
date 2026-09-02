- A [[financial assets#Securities|debt security]]. A ==bondholder== lends money to a ==bond issuer==. The holder is rewarded in [[interest rates|interest payments]] from the issuer in exchange for liquidity.
	- The issuer can be a corporation, municipality, or government.

- Bonds are first issued in the [[financial assets#Market Types|primary market]] as contracts.
	- Issuer demands a ==par value== for every contract from buyers, usually $1000. 
	- In exchange, the issuer pays a ==coupon== to the bondholder at a certain ==frequency==, usually annually, until a specified ==maturity date==.
- Upon maturity, the original par value is paid back in full.

- Bondholders can resell the contracts in the [[financial assets#Market Types|secondary market]] at a different price than the par value. 

- Bonds are generally lower risk than stocks since bondholders are paid before shareholders in liquidation.

# Terminology

**Par Value**

- Denoted $V_{par}$. 
- The initial value that the issuer demands from buyers.
- Paid back in full upon maturity.

**Frequency** 

- Denoted $f$. 
- Frequency of payment expressed as a fraction of a year.
- Assume $f =1$, or annual unless otherwise specified.

**Coupon Rate**

- Denoted $r$.
- $r = \frac{r}{f}$
- The stated [[interest rates|interest rate]] paid on the bond's face value.
- Bounded by contract, cannot change after issue.

**Coupon**

- Denoted $C$, also just referred to as payment.
- $C = rV_{par}$

**Maturity Date**

- The date the issuer repays the face value and the bond expires.

**Current Yield**

- Denoted $Y$, $CY$, or just $yield$.
- Coupon rate adjusted for the price of the bond.

**Yield to Maturity (YTM)**

- Denoted $YTM$.
- [[interest rates|Interest rate]] adjusted for the market price of the bond.

# [[evaluation#Future Value|Future Value]] of Bonds

- A bond's cashflow stream:
	- Coupon $C = rV_{par}$ at every period $i = 1, 2, \dots, n$.
	- Par $V_{par}$ returned at $i = n$.

- $FV$ at maturity is the value of the stream rolled forward to time $n$. Each coupon compounds at the discount rate $r_d$ from when it is received until $n$.
- The par payment is already at $n$, so it is not compounded.
$$FV_n = \sum_{i=1}^n C(1+r_d)^{n-i} + V_{par}$$

- [[series#Summation equation|Closed form:]]
$$FV_n = C\frac{(1+r_d)^n - 1}{r_d} + V_{par}$$
	- $n$     = Bond's remaining payment periods.
	- $r_d$  = Discount rate per period, equal to YTM.
	- $C$    = Coupon.
	- $V_{par}$ = Par value.

**Excel function**

- `=FV(rate, nper, pmt, pv, type)`
	- `rate` =  $r_d$
	- `nper` = $nf$
	- `pmt`   = Coupon
	- `pv`     = Present value, or market price
	- `type` 
		- `0` = payment at end of period.
		- `1` = payment at beginning of period.

# [[evaluation#Present Value|Present Value]] of Bonds

- Bonds, like all other financial assets, can be resold at ==premium== or at ==discount== in the [[financial assets#Market Types|secondary market]], we assume the market price to be its present value.

**At-premium** 

- $PV_b$ > par value.
- $YTM  < r_{coupon}$

**At-discount**

- $PV_b$ < par value.
- $YTM  > r_{coupon}$
- $PV$ of bonds follow the standard [[evaluation#Present Value|PV formula]] below.
$$PV = \sum_{i=1}^{n} \frac{{CF}_i}{{(1+r_d)}^i}$$
- Each coupon and the par are discounted from when received back to the present:
$$PV_b =\sum_{i=1}^{n} \frac{C}{{(1+r_d)}^i}+ \frac{V_{par}}{{(1+r_d)}^{n}}$$
	- $r_d$    = The [[evaluation#Present Value|discount rate]] per period.
	- $C$    = Coupon.
	- $V_{par}$ = The par value, paid at maturity.

- [[series#Summation equation|Closed form:]]
$$PV_b = C\frac{1-(1+r_d)^{-n}}{r_d} + \frac{V_{par}}{{(1+r_d)}^{n}}$$

**Excel function**

- `=PV(rate, nper, pmt, fv, type)`
	- `rate` = $r_d$
	- `nper` = $nf$
	- `pmt`   = Coupon
	- `fv`     = Future value.
	- `type` 
		- `0` = payment at end of period.
		- `1` = payment at beginning of period.

# Calculating Discount Rate

- The discount rate is the [[interest rates#Interest Rate on financial markets and assets Securities Securities|market interest rate]] of other securities with equal risk.
	- If the coupon rate of a bond exceeds the market interest rate, it will sell at a premium.
	- If the coupon rate is below the market rate, then it would sell at a discount.

- The $PV$ equation is an $n$ degree quadratic, there is no algebraic solution for $r_d$ even if all other variables are given. We must use excel functions to estimate.

**Excel function**s

- `=RATE(nper, pmt, pv, fv)`
	- `nper` = $nf$
	- `pmt`   = $C$
	- `pv`     = Present value.
	- `fv`     = Future value.

- For bonds, the discount rate is the same concept as the YTM.
	- $r_d$ is applied to the $FV$ to find the $PV$.
	- Thus, in a reverse order, $r_d$ is also the growth rate from $PV$ to $FV$. Which is the same definition as YTM.

- Putting it all together, YTM = $r_d$ = [[interest rates#Interest Rate on financial markets and assets Securities Securities|market interest rate]]. In other words, every bond of equal risk have the same yield to maturity.
- Plotted across maturities for bonds of equal credit risk (typically Treasuries), these YTMs form the [[yield curves|yield curve]]. The shape of that curve aggregates market expectations about future short rates and Fed policy.

# Treasury Securities

- Debt securities issued by the U.S. federal government.
- Considered risk-free, backed by the full faith and credit of the U.S. government.
	- Thus, zero [[interest rates#Security Premiums|default risk premium]] and [[interest rates#Security Premiums|liquidity premium]].

**Treasury Bill (T-Bill)**

- Maturity: up to 1 year.
- A ==zero-coupon bond==.

**Treasury Note (T-Note)**

- Maturity: 2 to 10 years.
- Pays a fixed coupon semiannually.

**Treasury Bond (T-Bond)**

- Maturity: 20 to 30 years.
- Pays a fixed coupon semiannually.
- Longest-duration government debt security.

# Corporate Bonds

- Debt securities issued by [[business entities#Corporation|corporations]] to raise capital.
- Higher risk than treasuries, much easier for a corporation to default than a nation.

**Investment-Grade Bond**

- Rated BBB-/Baa3 or higher by credit agencies (S&P, Moody's).
- Lower yield, lower risk.

**High-Yield Bond (Junk Bond)**

- Rated below BBB-/Baa3.
- Higher yield to compensate for higher default risk.

# Misc. Bond Types

- A bond can be multiple types at once, we won't be covering them all.
- Below are a few that doesn't warrant an entire section.

**Convertible Bonds**
- Bonds that may be exchanged for common stock of the issuing firm.
- Converted at the holder's option.

**Putable Bond**
- Bonds that allows the holder to sell back to the firm prior to maturity.

**Income Bond**
- Pays interest only when interest is earned by the firm.

**Indexed Bond**
- interest rate paid is based upon the rate of inflation.

**Zero Coupon Bond**
- Bonds that pay zero coupon.
- Instead, investors purchase these at a deep discount from the par value.

