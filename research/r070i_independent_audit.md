# R0.70I adversarial internal audit

**Release:** R0.70I
**Date:** 2026-08-24
**Final status:** PASS after correction
**Boundary:** this is an adversarial internal review by separate research
lanes.  It is not external peer review and does not certify a Millennium
claim.

## 1. Audited package

- `research/r070i_report-source.md`;
- `research/r070i_literature_audit.md`;
- `research/r070i_temporal_hardy_audit.py` and its finite certificate;
- `figures/r070i-temporal-hardy/fig-r070i-temporal-hardy/`.

The audit was split into three independent mathematical lanes: bounded
primary-literature scope, temporal-kernel/scaling counterexamples, and
LP/tensor-symmetry bookkeeping.  Each lane was asked to return `PASS` or
concrete `MUST-FIX` items rather than to improve the narrative.

## 2. Temporal kernel and scaling lane

The first review rejected the draft for three reasons:

1. the finite-chain interior sum did not explicitly stop at
   `k=K-1`, so the notation could be read as using an undefined
   `m_{K+1}`;
2. the proposed pressure-family pairing omitted the compact-support,
   nonnegativity, nondegeneracy, and admissible-coefficient hypotheses needed
   for a strict positive lower bound;
3. the heat scaling asserted a nonzero target without fixing a nondegenerate
   base profile and without scaling the chain, cutoff, filter, and top time
   together.

Corrections now present in the report:

- (2.6a) defines `T_{n,K}` with `k=0,...,K-1`, while (3.6a) defines the
  complete finite kernel including the fine Abel endpoint;
- Section 9 is restricted to a degree-zero abstract coordinate comparator,
  with explicit `U`, nonnegative `theta`, `Q_0`, `C_0`, the critical source
  norm, and a strictly positive contraction;
- Section 10 defines `E` and windowed `D`, fixes a base object with
  `T_n[v]>0`, scales the full geometry, and distinguishes the linear
  fixed-energy amplitude from exact NSE scaling;
- the small-NSE family records
  `D[v^a]=a^2 D_lin+O(a^3)` and makes clear that its tops tend to the initial
  face and its members are different solutions.

The lane's final verdict was `PASS`: the finite kernel, fine endpoint,
`alpha=1/4` threshold, heat/NSE exponents, strict degree-zero pairing, and
common-positive-top boundary were all rechecked.

## 3. LP and tensor-symmetry lane

The first review also rejected the draft for three independent reasons:

1. an arbitrary smooth `L^1` filter does not imply the annular Bernstein and
   square-function estimates used by the positive paraproduct theorem;
2. the same-index estimate did not yet cover the lower-triangular
   physical-cutoff and discarded-slab arrays;
3. a freely chosen coefficient had not been realized as an admissible
   exterior harmonic jet.

Corrections now present in the report:

- Sections 5--8 explicitly specialize to a standard LP or finite-overlap
  multiplier family satisfying (5.0);
- the filter increment and annular packets use distinct notation;
- (6.3)--(6.5) prove the complete frozen-low lower-triangular estimate via

  \[
  r_k^{-1}r_k^{3/2}\|B_j\|_2
  \lesssim r_k^{-1/2}\frac{r_k}{r_j}\|V_j\|_2,
  \qquad
  \frac{r_k}{r_j}\le\rho_+^{k-j},
  \]

  followed by the discrete `ell^1*ell^2` Young inequality;
- Section 8 is explicitly a list of representative obstructions for the
  direct termwise-absolute route, not an exhaustive signed Bony identity;
- Section 9 no longer claims exterior-source realization or degree-one
  admissibility.

The lane's final verdict was `PASS`: the complete frozen-low triangular
array closes with no scale-count or time-length loss, the low--low exponent
is unchanged, and the isotropic contraction vanishes pointwise against the
trace-free source tensor.

## 4. Literature-scope lane

The bounded audit checked the theorem statements and hypotheses of eight new
primary sources against the report's table.  Earlier wording was corrected
to preserve the input spaces, tent-space integration order, local-data
hypotheses, and the distinction between a bounded negative search finding
and theorem nonexistence.  A final source-by-source reread returned `PASS`.

The literature result is deliberately narrow: no audited theorem directly
controls the changing-cutoff, nested-time, negative-weight quadratic
vorticity-moment square from Leray energy and dissipation alone.  This is not
a proof that no such theorem exists.

## 5. Computational and figure boundary

The exact producer has twelve top-level checks.  It regresses 162 rational
finite-kernel regions, the scalar exponent threshold, heat and NSE scale
ledgers, homogeneous right-side exponents, the same-index frozen-low ledger,
the low--low ledger, and the isotropic trace-free contraction.  The analytic
all-chain geometric sum, the complete lower-triangular Young step, the
small-data expansion, and the nondegenerate moment lower bound remain
mathematical arguments rather than computer proofs.

The figure package has twenty passed validation checks and presents only
closed-form analytic curves and scaling ledgers.  It is not a simulation, a
numerical PDE proof, an NSE trajectory, or a fixed-positive-top
counterexample.

## 6. Final verdict

`PASS after correction` means the following limited conclusions are
internally consistent and auditable:

- the actual core dual norm reduces to the stated temporal Hardy kernel,
  with the exact finite-chain saturation;
- under the stated LP hypotheses, the complete frozen outer-low/annular
  triangular sector and the frozen low--low sector close at the energy level;
- the isotropic high--high contraction vanishes exactly;
- the moving-low and deviatoric high--high mechanisms remain open for this
  route;
- initial-boundary scaling forces the reported outer-scale dependence but
  does not produce a singularity or one-solution fixed-positive-time
  concentration.

No global regularity theorem, blow-up construction, no-go theorem for all
possible arguments, or solution of the Navier--Stokes Millennium problem is
claimed.
