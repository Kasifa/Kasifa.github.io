# Chart contract and source-data specification

## Analytical question

How do the four positive R0.74A payments split into two heat-scale powers,
and why do the two function-level examples require gradient and essential-time
exterior payments absent from the older integrated cubic package?

## Supported takeaway

The closed exponent ledgers separate `theta^(1/4)` from `theta`, a fixed
`K_D` lower-bound factor from a vanishing old payment and growing gradient
energy, and a bounded cubic time payment from a growing essential-time
velocity endpoint.

## Surface and visual family

- Surface: static double-column journal figure.
- Physical size: 178 mm by 74 mm.
- Renderer: one dependency-light producer with a shared vector drawing model
  for SVG and ReportLab PDF; the archival PNG is a 600 dpi PDF render.
- Family: three aligned closed-form line panels on honest logarithmic scales.
- Palette: hard two-root cap (blue and amber) plus charcoal/grey neutrals.
- Non-color distinctions: solid/dashed/dotted strokes and circle/square/
  triangle markers.
- Background: near-white; no gradients or decorative chart fills.

## Panel contract

### A | Four-block heat-scale weights

- Grain: 121 logarithmically spaced `theta` values in `[10^-4,1]`.
- Normalization: `A_c=B_c=U_ext=D_ext=1`.
- Series 1: `cc=ec=theta^(1/4)`.
- Series 2: `ce=ee=theta`.
- Both axes are logarithmic.
- Prohibited reading: the theorem constant `C` is not one and is not plotted.

### B | Exterior high-frequency packet

- Grain: `j=1,...,24`, `N=2^j`, `epsilon_N=N^(-2/3)`.
- Series 1: displayed lower-bound exponent factor `N^0=1`.
- Series 2: old cubic payment exponent factor `N^(-2)`.
- Series 3: gradient-energy exponent factor `N^(2/3)`.
- X is base-2 logarithmic in `N`; Y is logarithmic.
- Prohibited reading: the unknown positive lower-bound constant `c` is not
  one and is not plotted.

### C | Exterior time spike

- Grain: 121 logarithmically spaced `delta` values in `[10^-6,1]`.
- Series 1: old cubic payment exponent factor `delta^0=1`.
- Series 2: essential-time velocity endpoint factor `delta^(-2/3)`.
- Both axes are logarithmic.
- Every row is a separate finite energy-class field; there is no uniform
  global `L_t^infinity L_x^2` bound across the displayed family.

## Evidence boundary

`source-data.csv` is reconstructed independently from exact exponent formulas
by `validate.py`. Panels B and C are function-level packets, not unforced NSE
trajectories. No finite row carries a universal quantifier. No simulation or
DNS is used. **NOT CLAY.**
