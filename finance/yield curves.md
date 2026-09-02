- The relationship between [[bonds|bond]] yields and time to maturity, for bonds of identical credit quality.
- Plotted: yield on the y-axis, time-to-maturity on the x-axis. Each point is a bond at that maturity, its [[bonds#Yield to Maturity (YTM)|YTM]].
- Typically drawn from [[bonds#Treasury Securities|Treasury securities]] to strip out default and liquidity effects ($DRP$ and $LP$ both $\approx 0$). What remains drives the shape.
- The shape shifts over time and carries the market's expectations of future short-term [[interest rates]] and [[monetary policy|Fed]] policy.

# Why the Curve Exists

- A 1-year and a 10-year Treasury both pay a fixed yield, but those yields differ. The difference is information.
- Both bonds have negligible $DRP$ and $LP$. Per the [[interest rates|rate decomposition]] $r = r^* + IP + LP + DRP + MRP$, only $r^*$, $IP$, and $MRP$ vary meaningfully across Treasury maturities.
- Differences in market expectations about each component over different horizons produce different yields at different maturities. The curve aggregates those expectations.

# Shapes

```desmos-graph
left=0; right=10; bottom=0; top=10; grid=true
---
y=2\ln(x+1)+2|x>0|blue
y=-2\ln(x+1)+8|x>0|red
y=5|x>0|green
(9,6.6)|blue|label:Normal
(9,3.4)|red|label:Inverted
(9,5)|green|label:Flat
```

**Normal**

- Upward sloping. Long yields > short yields.
- The default state. Two reinforcing reasons:
	- ==Maturity risk premium== ($MRP$, owned by [[interest rates#Security Premiums|interest rates]]) compensates for interest-rate risk on long bonds. Bond prices fall when rates rise; longer duration means larger price loss from a given rate change. Investors demand more yield to bear that.
	- Expectations: investors typically expect short rates to rise over the long run as the economy grows.

**Inverted**

- Downward sloping. Short yields > long yields.
- Rare. Mechanism: investors expect the [[monetary policy#Fed Tools|Fed]] to cut short rates significantly in the future, usually because they expect a recession.
- When investors expect future short rates to fall, they bid up long bonds today to lock in current high yields. Long-bond prices rise, long yields fall — and can fall below short yields.
- Historically has preceded every U.S. recession in the post-WWII period.

**Flat**

- Long $\approx$ short across all maturities.
- Transitional. The curve passes through flat as it inverts or un-inverts.

**Humped**

- Medium-term yields higher than both short and long.
- Rare. Indicates the market expects a near-term tightening cycle followed by long-run cuts.

# Theories of Shape

- Three theories explain why the curve takes the shape it does. They are not mutually exclusive — real curves blend all three.

**Pure Expectations**

- Long-term rates equal the geometric average of expected future short-term rates over the same period.
- $(1 + r_n)^n = \prod_{t=1}^{n}(1 + E[r_{1,t}])$
	- $r_n$ = the n-period yield observed today.
	- $E[r_{1,t}]$ = expected one-period short rate starting at time $t$.
- Mechanism: an investor with a 5-year horizon can buy a 5-year bond, or roll over five 1-year bonds. Arbitrage forces the expected return to be equal across the two routes, so the 5-year yield must equal the average of expected 1-year yields.
- Predicts: curve slopes up only when expected future short rates exceed today's short rate. Slopes down when investors expect cuts.

**Liquidity Preference**

- Investors prefer short bonds (less price risk) and demand a maturity premium to hold long bonds.
- Long yield = average expected future short rate + $MRP$.
- Mechanism: the same arbitrage argument as pure expectations, but with a wedge. The wedge is $MRP$, which grows roughly linearly with maturity (textbook approximation: $MRP \approx 0.1\% \times (t-1)$ years).
- Predicts: curve has an upward bias even when expected future short rates are flat. Pure-expectations slope plus a maturity wedge.

**Market Segmentation**

- Different investor groups have preferred maturity ranges and don't substitute freely across them.
	- Insurance companies and pension funds want long-dated assets to match long-dated liabilities.
	- Banks want short-dated assets for liquidity.
	- Money-market funds are constrained to very short maturities by regulation.
- Mechanism: yield at each maturity is set by [[supply and demand]] within that bucket, not by arbitrage with adjacent maturities.
- Predicts: curve shape can be irregular, with kinks where supply or demand spikes at a particular maturity.

# Recession Indicator

- Inversion of the 10-year vs. 2-year (or 10-year vs. 3-month) Treasury spread has preceded every U.S. recession in the post-WWII period.
- Mechanism, in three steps:
	- Investors collectively expect the economy to weaken.
	- They expect the [[monetary policy#Expansionary Policy|Fed]] to respond by cutting short rates aggressively.
	- They buy long-term Treasuries today to lock in current yields before those cuts. Long-bond prices rise, long yields fall below short yields.
- The curve does not cause recessions. It reports the market's collective forecast that one is coming, by aggregating bets on future Fed policy.
- Lead time: typically 6 to 24 months between inversion and recession onset. The curve identifies the direction, not the date.
