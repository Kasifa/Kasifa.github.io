# Figure R0.74A-1: localized K_D payments and function-level obstructions

This package is source-bound to research commit
`391debac9d48158ab4b0f90edf873150849e6e57`.

It visualizes normalized exponent factors from the frozen R0.74A analytic
size lemma and its two function-level obstruction ledgers. The plotted rows
are deterministic evaluations of closed formulas. They are not simulation,
DNS, fitted data, or numerical evidence for the analytic quantifiers.

The high-frequency and time-spike packets are function-level fields. They
are not unforced Navier--Stokes trajectories. Every displayed positive
parameter gives a separate finite energy-class field; the time-spike family
has no uniform global `L_t^infinity L_x^2` bound.

## Reproduction

Run from this directory with the repository checkout at the bound commit:

```text
python producer.py --render
python validate.py --write-baseline .determinism-baseline.json
python producer.py --render
python validate.py --determinism-baseline .determinism-baseline.json --consume-baseline --write-metadata --confirm-visual-qa
python validate.py --verify-only --confirm-visual-qa
```

The runtime must expose Python 3.12, NumPy, Pillow, ReportLab, pypdf, and
Poppler's `pdftoppm`. No network, DGX, random sampling, or equation solver is
used.

## Claim boundary

- Panel A suppresses the theorem constant `C` and plots only the exact
  `theta` weights after setting the four nonnegative payments to one.
- Panel B suppresses the positive packet constant `c` and plots only the
  exact powers of `N`.
- Panel C plots only the exact powers of `delta`; each row denotes a separate
  finite field, not one uniformly energy-bounded family.
- Finite rows do not prove quantifiers, produce an NSE counterexample, or
  establish compactness, epsilon regularity, or global regularity.

**NOT CLAY.**
