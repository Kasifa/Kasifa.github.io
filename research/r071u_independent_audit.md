# R0.71U independent audit

**Date:** 2026-08-26

**Status:** independent finite reconstruction passed.  The checker imports
neither `research/r071u_exact_audit.py` nor its JSON output.

## Methods

1. Deterministic vector-valued polynomial paths with one through twelve
   prescribed common zeros were integrated exactly in the polynomial basis
   and checked against the constants (2/|I|) and (7|I|/3).
2. A (32^2) spectral grid independently reconstructed the invariant
   substitution (u=(f(y,z),0,v(y))), its zero divergence, and the nonlinear
   term ((vf_z,0,0)).
3. Response matrices for one through eight prescribed times were assembled
   from the Duhamel response functions and checked by SVD.  This is a finite
   conditioning test; the extended-Chebyshev proof in the report supplies the
   theorem for every finite size.
4. The modular lattice was enumerated independently.  With
   (K=L=1,d=8,R_*=3), only the conjugate target pair lies in the declared
   compact support.
5. The seven-parameter (N=3) example was solved directly on the Fourier
   lattice.  The remaining six shooting variables were obtained by a new
   nonlinear solve with (p_1=0.002).  Cutoffs 24, 30, and 36 were then
   integrated independently.  All three prescribed target coefficients were
   below (2.0	imes10^{-18}), every target slope was nonzero, and the maximum
   slope change between refinements was below (5.2	imes10^{-17}).
6. The forced path (N^{-1}sin Nt) and both scale-zero theorem rows were
   reconstructed without using the symbolic producer.

## Analytic boundary

The computation does not prove the Hilbert zero-sampling lemma, the
Chebyshev-system zero multiplicity theorem, the continuum implicit-function
construction, or global regularity.  Those are analytic claims and boundaries
in `research/r071u_report-source.md`.  The lattice integration is a finite
smooth ODE corroboration, not DNS and not an approximation on which the
continuum theorem depends.

The recurrence quantifier is finite: each prescribed finite time set may use
a different initial datum.  The bounded energy--enstrophy construction rules
out a uniform raw-count bound on that bounded class, not every possible
nonuniform function of the exact pair of initial norms.

## Reproduce

```text
PYTHONDONTWRITEBYTECODE=1 /Users/kasifa/Documents/Math/.codex-research-venv/bin/python \
  research/r071u_independent_audit.py \
  --output research/certificates/r071u/independent-result.json
```
