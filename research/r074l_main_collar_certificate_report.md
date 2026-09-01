# R0.74L finite main-collar certificate report

## Result

The primary exact-arithmetic producer
scripts/r074l_main_collar_certificate.py returns

\[
 \boxed{\text{PASS }24/24.}
\]

Its stdout is byte-identical to
research/r074l_main_collar_certificate.json.  The independent Ruby
reconstruction also returns PASS 24/24 with zero discrepancies.

## Certified finite comparisons

The certificate checks:

- the first discrete threshold
  \(L_{14}=32256\ge262144/15\);
- the bad-path reflection exponent
  \[
  A=\frac{4876875}{1476395008};
  \]
- its strict reserve
  \[
  A-\rho=\frac{1315703}{7381975040}>0;
  \]
- the exact fourth Taylor lower bound at \(256/65\), which proves
  \(4e^{-256/65}<1/8\);
- the calibrated interval
  \[
  \frac1{128}\le BR^2\le\frac1{64};
  \]
- the clock length \(65/64<2\), projection coefficient \(65/63\),
  physical-duration coefficient \(66560/189\), and positive modulus
  exponent coefficient \(189/68157440\); and
- both exact \(R\)-power ledgers:
  \[
  R^6R^2R^{-1}R^{-3}(LR)=LR^5,
  \]
  \[
  R^6R^{-1}LR^{-3}R^2R=LR^5.
  \]

## Boundary

This is a **FINITE** certificate only.  It does not prove bridge reversal,
the reflection principle, stopping-time measurability, thickened-slice
geometry, the short-clock BV lemma, the nearest inward collar, or any
universal Navier--Stokes conclusion.  Those analytic statements have
separate proof and audit records.  **NOT CLAY.**
