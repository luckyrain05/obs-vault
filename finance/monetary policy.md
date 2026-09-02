- ==Monetary policy== is the process by which a central bank controls the [[supply and demand|supply]] of money to influence [[interest rates]] and the broader economy.
- In the U.S., the central bank is the ==Federal Reserve (the Fed)==.

# Money Market

- The [[supply and demand]] model applied to money.
	- Y-axis: [[interest rates|interest rate]] $r$. 
	- X-axis: quantity of money $M$.

- We define two curves, money supply and money demand.
**Money Supply (MS)**
	- Money does not respond to the interest rate, thus it is perfectly [[supply and demand#Elasticity|inelastic]] and vertical in shape.
	- Set directly by the Fed.

- **Money Demand (MD)**
	- Downward sloping.
	- Higher $r$ increases the opportunity cost of holding cast.
	- Lower $r$ makes holding cash less costly.

# Equilibrium

```desmos-graph
left=0; right=10; bottom=0; top=10; grid=true
---
x=4|y>0|blue
y=\frac{24}{x+2}|x>0|blue
x=4|0<y<4|dashed|red
y=4|0<x<4|dashed|red
(4,4)|red|label:r*
(4,9)|blue|label:MS
(9,2.2)|blue|label:MD
```

- The equilibrium [[interest rates|interest rate]] $r^*$ is where $MS$ and $MD$ intersect.
- $r > r^*$: surplus of money
	- People buy [[bonds]] and bond yields fall, pushing $r$ down.
- $r < r^*$: shortage of money
	- People sell bonds, bond prices fall, yields rise, pushing $r$ up.

# Fed Tools

**Open Market Operations (OMO)**

- The Fed buys or sells [[bonds#Treasury Securities|Treasury securities]].
- Buy → injects money into the economy → $MS$ shifts right.
- Sell → pulls money from the economy → $MS$ shifts left.
- Most commonly used tool.

**Discount Rate**

- The [[interest rates|interest rate]] the Fed charges banks for short-term loans.
- Lower → banks borrow more → $MS$ shifts right.
- Raise → banks borrow less → $MS$ shifts left.

**Reserve Requirements**

- The fraction of deposits banks must hold in reserve rather than lend out.
- Lower → banks can lend more → $MS$ shifts right.
- Raise → banks can lend less → $MS$ shifts left.

# Expansionary Policy

```desmos-graph
left=0; right=10; bottom=0; top=10; grid=true
---
x=4|y>0|blue
x=6|y>0|blue
y=\frac{24}{x+2}|x>0|blue
y=4|0<x<4|dashed|red
y=3|0<x<6|dashed|red
(4,9)|blue|label:MS0
(6,9)|blue|label:MS1
(9,2.2)|blue|label:MD
```

- The Fed increases $MS$ → shifts right → $r$ falls.
- Lower $r$ → cheaper borrowing → more spending and investment → economic growth.
- Risk: inflation if pushed too far.

# Contractionary Policy

```desmos-graph
left=0; right=10; bottom=0; top=10; grid=true
---
x=4|y>0|blue
x=2|y>0|blue
y=\frac{24}{x+2}|x>0|blue
y=4|0<x<4|dashed|red
y=6|0<x<2|dashed|red
(4,9)|blue|label:MS0
(2,9)|blue|label:MS1
(9,2.2)|blue|label:MD
```

- The Fed decreases $MS$ → shifts left → $r$ rises.
- Higher $r$ → expensive borrowing → less spending and investment → slows inflation.
- Risk: recession if pushed too far.

# Transmission to the Yield Curve

- The Fed's tools move $r^*$, which is the very-short-end rate (overnight to ~1 year). Long-term rates are set by the bond market, not directly by the Fed.
- The market sets long rates by averaging its expectations of future short rates over the bond's life, plus a maturity premium. So today's long yield reflects today's $r^*$ plus the market's forecast of the Fed's next moves.
- Mechanism, shapes, and the inverted-curve recession signal: [[yield curves]].
