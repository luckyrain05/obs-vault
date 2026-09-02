# Demand

-  The quantity of a good or service that consumers are willing and able to buy at each price level.

**Law of Demand**
- All else held equal, as price increases, demand decreases. As price decreases, demand increases.

**Demand Curve**
- $x$ : Quantity demanded.
- $y$ : Price of product.
- Slopes downward left to right. Higher price, lower demand.

```desmos-graph
left=0; right=10; bottom=0; top=10; grid=true
---
y=\frac{8}{\sqrt{x}}|x>0|blue
(9,2.7)|blue|label:D
```

# Supply

**Supply**
- The quantity of a good or service that producers are willing and able to sell at each price level.

**Law of Supply**
- All else held equal, as price increases, quantity supplied increases. As price decreases, quantity supplied decreases.

**Supply Curve**
- $x$ : Quantity supplied.
- $y$ : Price
- Slopes upward left to right. Higher the price, higher the demand.

```desmos-graph
left=0; right=10; bottom=0; top=10; grid=true
---
y=2\sqrt{x}|x>0|blue
(9,6)|blue|label:S
```

# Supply and Demand Model

- Plotting both the supply and demand curves together forms the complete supply and demand model.

**Equilibrium Price (P*)**
- The price where quantity demanded equals quantity supplied.

**Equilibrium Quantity (Q*)**
- The quantity bought and sold at the equilibrium price.

```desmos-graph
left=0; right=10; bottom=0; top=10; grid=true
---
y=\frac{8}{\sqrt{x}}|x>0|blue
y=2\sqrt{x}|x>0|blue
x=4|0<y<4|dashed|red
y=4|0<x<4|dashed|red
(4,4)|red|label:P* Q*
(9,2.7)|blue|label:D
(9,6)|blue|label:S
```

**Surplus**
- Occurs when actual price is above equilibrium.
- Quantity supplied > quantity demanded.
- Sellers lower prices to clear excess inventory, pushing price back toward equilibrium.

**Shortage**
- Occurs when price is below equilibrium.
- Quantity demanded > quantity supplied.
- Buyers bid prices up, pushing price back toward equilibrium.

# Elasticity

- ==Elasticity== measures how responsive quantity is to a change in price.
- Formally, the ratio of the proportional change in quantity to the proportional change in price.
$$E = \frac{dQ}{dP} \cdot \frac{P}{Q}$$
- $\frac{dQ}{dP}$ is the [[finance/derivatives|derivative]] of quantity with respect to price.
-  $\frac{P}{Q}$ scales it into a dimensionless ratio.
- Thus, elasticity directly influences the shape of the curves.

**Price Elasticity of Demand (PED)**
- $E_d = \frac{dQ_d}{dP} \cdot \frac{P}{Q_d}$
- Always negative (law of demand), typically expressed as $|E_d|$.

**Price Elasticity of Supply (PES)**
- $E_s = \frac{dQ_s}{dP} \cdot \frac{P}{Q_s}$
- Always positive (law of supply).

**Arc Elasticity (Midpoint Method)**
- Discrete approximation when the demand function is unknown — uses two observed points.
$$E = \frac{Q_2 - Q_1}{P_2 - P_1} \times \frac{P_1 + P_2}{Q_1 + Q_2}$$

**Perfectly Elastic**
- $|E| = \infty$
- Horizontal line, price does not fluctuate at any quantity.
- Consumers will only buy at one exact price.

**Perfectly Inelastic**
- $|E| = 0$
- Vertical curve, quantity does not respond to price.
- Consumers buy the same quantity regardless of price.

```desmos-graph
left=0; right=10; bottom=0; top=10; grid=true
---
y=5|x>0|blue
x=5|y>0|blue
(8,5)|blue|label:Perfectly Elastic
(5,9)|blue|label:Perfectly Inelastic
```