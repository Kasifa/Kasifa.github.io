# Chart contract and source-data specification

## Analytical question

How do the R0.73Z endpoint obstruction, exact lacunary arithmetic, and
pressure-active production kernel separate signed production from positive
heat covariances?

## Supported takeaway

The original \(D^{3/2}\) observable has an initial-endpoint frequency
obstruction despite fixed energy; the lacunary exact shear packages that
obstruction into one finite-energy solution; and the crossed exact family
has zero production while positive gradient and pressure covariances remain.

## Surface and visual family

- Surface: static double-column journal figure.
- Physical size: 178 mm by 74 mm.
- Renderer: one dependency-light producer with a shared vector drawing model
  for SVG and ReportLab PDF; the archival PNG is a 600 dpi PDF render.
- Family: three aligned analytic line panels.
- Palette: hard two-root cap (blue and amber) plus charcoal/grey neutrals.
- Non-color distinctions: solid/dashed/dotted strokes and circle/square/
  triangle markers.
- Background: near-white; no gradients or decorative chart fills.

## Panel contract

### A | Initial-endpoint frequency test

- Grain: integer frequency \(n=1,\ldots,64\).
- X: frequency \(n\), displayed on a base-2 logarithmic axis.
- Series 1: exact lower-bound factor \(n\) in \(c n\).
- Series 2: exact normalized energy \(6\).
- Prohibited reading: the first series is not the integral and suppresses the
  fixed positive constant \(c\).

### B | Exact lacunary arithmetic

- Grain: partial-sum index \(J=1,\ldots,16\).
- Left series: \(S_J=(1-4^{-J})/3\), with reference \(1/3\).
- Right series: \(\sum_{j\le J}a_j^3N_j=J\).
- Exact fraction text is retained in the CSV.

### C | Crossed exact family

- Grain: 121 logarithmically spaced heat scales
  \(s\in[0.005,3]\).
- Normalization: \(A=B=n=1\), \(t=t_*\),
  \(x_1=x_2=\pi/3\).
- Left series: \(D_s\).
- Right series: \(|Q_s|\) and \(\nabla\cdot Q_s\).
- Exact zero reference: \(\Pi_s=\mathscr S_s=0\).

## Evidence boundary

`source-data.csv` is reconstructed from explicit formulas by `validate.py`.
No finite row carries a universal quantifier.  The bound, divergence, and
strict-positivity proofs remain in the source-bound analytic notes.
