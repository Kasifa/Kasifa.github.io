# R0.20 certificate archive

This directory contains the machine-readable evidence used by research note
R0.20.  The scope is the selected finite fifth-order quotient in the positive
three-parameter family.  It is not a certificate for the Navier-Stokes PDE.

## Certificate chain

1. `compactification.json` records the exact quotient, stationary-system
   profiles, factor removals, and projective boundary limits.
2. `exact-polynomials.json.gz` contains the three exact saturated stationary
   polynomials used by every interior calculation.
3. `interior-root-certificates.json` gives radius `1e-6` exact-rational
   Krawczyk boxes for the two positive stationary roots and their Hessian
   classifications.
4. `boundary-resultants-*.json*` and the four compressed `*-rur.json.gz`
   files give exact elimination and rational-univariate pairing evidence for
   all four finite faces.
5. `boundary-face-certificates.json` and
   `boundary-edge-certificates.json` certify the retained positive boundary
   stationary points and all four codimension-two edge maxima.
6. `boundary-blowup.json` records the two weighted exceptional-divisor sign
   calculations.  `boundary-strips.json` strengthens them to explicit exact
   finite-width Bernstein strips.
7. `global-bernstein-depth2.json` is the complete outward-rounded global
   subdivision.  `global-bernstein-depth3.json` repeats it from an independent
   512-seed partition.  Both finish with zero unresolved boxes.

Exact algebra on the finite faces was run in the pinned
`navier-stokes-r020-flint:py312-flint090` image with image ID
`sha256:02b6a51168a1bc9b15aca05889d5ca95fa729b36298ec4faa73c08af63f013a5`.
The global Bernstein runs used Python 3.12.13 and NumPy 2.3.5 on macOS arm64.

The SHA-256 list in `SHA256SUMS` is part of the archive.  Recompute it before
using copied files as evidence.
