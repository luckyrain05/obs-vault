- Interest rates are the price of borrowing money. the lender earns interest, the borrower pays it. It is set by the lender.
- Thus, interest rates directly represent the value of liquidity in the [[monetary policy#Money Market|money market]].

# Interest Rate For [[financial assets#Securities|Securities]]

$$r = r^* + IP + LP + DRP + MRP$$
 
**Definitions**
- $r$ 
	- Market interest rate of a security.
	- It is what investors collectively demand from said security accounting for all risks and $r^*$, the time value of their investment.
- $r^*$ 
	- Equilibrium in the [[monetary policy#Money Market|money market]].
	- The base rate that investors charge for loosing access to the cash that is used to purchase the security. Represents the actual [[supply and demand|demand]] for liquidity.
- $IP$
	- Inflation premium.
	- Compensates for value loss due to inflation.
- $LP$
	- Liquidity premium.
	- Compensates for value loss when liquidating.
- $DRP$
	- Default risk premium
	- Compensates for the default risk of the borrower.
- $MRP$
	- Maturity risk premium.
	- Compensates for interest rate risk on longer maturities.

# Security Premiums

$$premiums = IP + LP + DRP + MRP$$

- ==Security premiums== is the monetary compensation for additional risk factors that could decrease the [[bonds|yield to maturity]] of said security.

**Formula**
- $IP = \bar{\pi}_e$ 
	- $\pi$ is the symbol for inflation in economics.
- $LP = r_{illiquid} - r_{liquid}$
	- Yield spread between two instruments identical in all ways except marketability. Hard to isolate precisely
	- Usually estimated by comparing corporate vs Treasury yields after stripping out DRP.
- $DRP = r_{risky} - r_{rf}$
	- Spread between a risky bond's yield and a risk-free bond of identical maturity.
	- Credit rating agencies quantify this more empirically.
- $MRP = 0.1\% \times{(t − 1)}$
	- $t$ = years to maturity
	- Typical textbook form assuming the maturity risk increases by $0.1\%$ yearly.
	- Otherwise the formula is: $MRP = r_{long} - r_{short}$ and observed directly from the yield curve, the spread between long and short-term Treasuries.

- For [[bonds#Treasury Securities|Treasury Securities]], $DRP = LP = 0$. Essentially 0 default risk and is highly liquid.

# Yield Curve

- The plot of [[bonds#Treasury Securities|Treasury]] yield against time-to-maturity. Aggregates how each rate component above (especially $MRP$ and expectations of future $r^*$) varies across maturities.
- Mechanism, shapes, and theories of why the curve takes a given shape: [[yield curves]].
