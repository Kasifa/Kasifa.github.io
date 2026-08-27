# R0.72L strong-coupling finite-audit bundle

This bundle supports the analytic R0.72L enstrophy/action-aware ledger, its
moderate strong-coupling closure window, and the exact warning that a
three-mode Galerkin countermodel cannot be embedded as a finite-support
invariant subsystem of the full Fourier lattice.

The proof is not numerical.  The finite producer and independent routes have
four deliberately narrower jobs:

1. recompute the exponents in $U_0,W,U,V,H,Z$;
2. check the scalar optimizations from L.1 to L.2 and L.4;
3. sample the local normalized action floor and the L.5 little-o window; and
4. integrate the projected oscillator while separately checking its first
   order-one full-lattice leakage.

## Producer route

- source: `research/r072l_exact_audit.py`;
- implementation: exact `Fraction` exponent arithmetic, binary64 log grids,
  Cartesian $(U,V)$ RK4 integration, and explicit convolution dictionaries;
- no random seed and no non-standard Python dependency;
- the suppressed absolute constant in the analytic floor/window is normalized
  to one only for a scaling proxy.

## Independent route

- source: `research/r072l_independent_audit.py`;
- implementation: direct scalar maxima, separately written binary64 formulas,
  polar $(\theta,\log r)$ RK4 integration, and direct leakage coefficients;
- it neither imports nor reads the R0.72L producer source or artifacts;
- its own config, environment, progress, resource, monitor, JSON, and CSV
  records are archived here.

Both routes pass all declared checks.  The producer records 48 scalar
optimization cases, 10 local-floor cases, 12 closure-window cases, and 10
Galerkin cases.  The independent route recomputes the same grids without
reading producer artifacts.

## Galerkin/full-lattice separation

The projected three-mode ODE is audited at $R=8,16$ and
$\sigma=32,64,128,256,512$.  Its target-root mass and cubic row approach
the stated linear-in-$\sigma$ averages, while the mixed row approaches a
finite limit.  This does **not** give a full-lattice counterexample.

At $R=16,\sigma=512$, both routes find 103 target roots.  The producer
ratios to the fast-phase formulas are

- root mass: `1.0048622076667055`;
- cubic row: `0.999045860832481`;
- mixed row: `1.0016977255472364`.

Across all 10 cases, the largest producer-independent relative differences
are `7.103343240906875e-5` for root mass,
`1.986780533349326e-6` for the cubic row, and
`3.5690901492126364e-7` for the mixed row.  All root counts agree exactly.

For the unprojected single-carrier convolution, the first deleted shell is
already exact:

\[
 (I-P_{\mathcal H_R})W_R^2e_0=-a^2(e_{2R}+e_{-2R}),
 \qquad
 \frac{\|(I-P)W_R^2e_0\|}{\|PW_R^2e_0\|}=\frac1{\sqrt2}.
\]

The producer additionally evaluates three finite extremal-index examples;
the analytic maximum-index argument in the report, not those examples, proves
that no nonzero finite coordinate-support invariant subspace exists.

Along the finite declared little-o sequences, the normalized proxy decreases
from `0.27994248468276506` to `0.12232737596879091` in the coherent endpoint
$p=1$, and from `0.38806767978192336` to `0.14125307931553174` in the
worst declared endpoint $p=R^{-1/2}$, as $R$ runs from 16 to 16384.  These
are scaling diagnostics, not convergence proofs.

## Boundary

All ODE results are finite binary64 diagnostics, not interval certificates.
The local floor samples do not establish the unknown absolute constants.  The
closure sequence illustrates scaling and does not by itself prove an
asymptotic theorem.  The Galerkin oscillator omits immediate Fourier cascade
and is not DNS.  This bundle neither proves regularity for general
three-dimensional Navier--Stokes solutions nor resolves the Clay Millennium
Problem.

Run `command.txt` from the repository root.  Rebuild `SHA256SUMS` only after
every other file in this directory is final.
