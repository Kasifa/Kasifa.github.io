# R0.73X Gaussian velocity-tail scalar certificate

**Status:** `PASS`

**Scope:** scalar Gaussian kernel domination, scale integration, NSE degree
bookkeeping, and translated-packet concentration powers.  This is not a PDE
simulation, regularity theorem, or Clay conclusion.

## Reproduction

```bash
python3 scripts/r073x_gaussian_tail_certificate.py --check-only
```

## Certified rows

- Kernel ratio maximum: `q=2.0` with constant
  `3.4310555398428275`; the deterministic grid maximum is
  `3.4310555398428275`.
- A fully explicit admissible pointwise constant in
  `|S_s| <= C s^(-1/2) P_(2s)(|u|^3)` is
  `9.8141320262657512`.
- Direct quadrature versus the closed scale-integral formula has maximum
  relative error `3.067e-14` on the declared
  48-case grid.
- Annular distance, heat-ball coefficient
  `0.033245190033452721`, and final coefficient
  `1.0638460810704871` are assembled independently.
- Both the absolute tent and exact exterior-tail functionals have NSE scaling
  degree zero.
- A shrinking remote packet has derived `L3` power `3` and
  weighted-`L2`-to-`3/2` power
  `9/2`; their ratio has power
  `-3/2`.  Direct packet quadrature
  recovers final consecutive slopes
  `2.999857066`,
  `4.499782070`, and
  `-1.499925004`.
- The energy interpolation independently gives viscosity power
  `-3/4` and radius power
  `2`; the lifted polynomial tail is bounded by
  a geometric super-exponential majorant.

`payload_sha256=fcac97440dde87d00103f3a09b346bdd918c9fbb7360ee792edc2c8d0357e3b7`

NOT CLAY.
