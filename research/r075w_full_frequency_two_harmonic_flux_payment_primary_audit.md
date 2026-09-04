# R0.75W primary mathematical audit

## Verdict

- Current verdict: **PASS**.
- Mathematical blocker count: **0**.
- Release blocker count: **0**.
- Scope: analytic proof and claim boundary for one exact diffusive dyadic
  two-harmonic shear.

## 1. Statement audit

The theorem quantifies over `A,C>=0`, every integer pair
`1<=m<k<=2m`, both phases, and every real constant `B`.  The low/high split
is exhaustive: R0.75W proves `maR<C_0`, while the byte-bound R0.75V theorem
proves `maR>=C_0`.  No frequency endpoint is omitted.

The output is the same physical estimate and normalization as R0.75V.  The
claim is limited to the exact field W.1 and does not assert a projection,
packet, Version-M extraction, suitable-weak, or regularity theorem.

## 2. Scaling audit

With `ell=aR`, `t=R^2s`, `x_2=ell z`, and `v=BR/a`, direct substitution
gives

`G_s+vG_z-a^(-2)G_zz=0`.

The cross-sectional derivative obeys

`D_R(ell z) ell dz = a R^2 W_a(z) dz`.

Since `B R^2=a v R`, the flux prefactor is exactly `a^2 R^3 v/2`.
The plateau fibre has area `4 pi a delta_0 R^2`; multiplication by
`dt=R^2 ds` and `dx_2=aR dz` gives the mass prefactor
`4 pi delta_0 a^2 R^5`.  Hence

`a^2 R^3 (M/(a^2 R^5))^(2/3)
 =a^(2/3) R^(-1/3) M^(2/3)`.

The normalization cancels every power of `R` and leaves
`a^(2/3) omega^(1/3) p^(2/3)` with rate `-2/11907`.

## 3. Spatial observation audit

At fixed time the scaled pair solves the fourth-order ODE W.12.  Its state
matrix coefficients are continuous on the compact square
`[0,2C_0]^2`.  The contradiction argument normalizes the complete initial
jet, not the two original Fourier coefficients.  Consequently it includes
the confluent limits `alpha=beta`, generalized sine/cosine solutions, and
the cubic-polynomial limit `alpha=beta=0`.  This is the correct closure of
near-colliding two-frequency spaces.

The lemma controls both `G` and `G_z` on the support of `Xi_a` by the
observed `L^3` norm on `[-1/2,1/2]`.  No inverse frequency gap occurs.

## 4. Temporal endpoint audit

For fixed `z`, W.9 has at most four complex exponential terms.  Their real
parts are `-alpha^2/a^2` and `-beta^2/a^2`; their imaginary parts may be
arbitrarily large because `v` is unrestricted.  Nazarov's theorem has
exactly the required independence from imaginary frequencies and gaps.

Choosing the half-measure `L^3` sublevel set in W.17 gives W.16.  Pointwise
application followed by integration in `z` gives `h(4)<=CH`.  Coincident
exponents only reduce the number of distinct terms and create no singular
constant.

## 5. Kernel and sign audit

The scaled kernel `W_a` is odd and has zero integral.  Its primitive
`Xi_a` is compactly supported, uniformly bounded in `L^1` and `L^infinity`,
and has `||Xi_a''||_1<=Ca`.  The factor `a^(-2)` in the heat rows therefore
absorbs the only growing derivative norm.

For `Q=G^2`, the audited equation is

`Q_s+vQ_z-a^(-2)Q_zz=-2a^(-2)|G_z|^2`.

Since `W_a=Xi_a'`, the signs in W.25--W.26 are:

- terminal energy: plus;
- cutoff derivative: minus;
- `Xi_a'' G^2` heat row: minus;
- localized dissipation: plus.

All terms are bounded in absolute value after the exact identity is formed.
No invalid sign discard is used.

## 6. Degeneracy audit

- `B=0`: the original flux vanishes; W.26 remains an exact cancelling
  identity and its right side is controlled.
- `|B|` large: the temporal trace is independent of imaginary frequency.
- `k-m` small: the spatial ODE compactness includes repeated roots.
- `maR` small: the cubic-polynomial confluent limit is included.
- third-order centre node: `A sin(2my)-2A sin(my)` has leading term
  `-A(my)^3`; it disproves a uniform low-frequency use of the old T defect
  but is covered by the complete four-jet compactness argument.
- common-phase node: the full local energy identity retains the endpoint,
  cutoff, heat, and dissipation cancellation; the four Fourier rows are not
  bounded separately.
- one zero amplitude: the argument reduces without division by an
  amplitude.

## 7. Evidence boundary

The source report checks Nazarov's primary theorem, an accessible primary
restatement, and the official Clay problem statement.  The analytic
continuum lemmas are proved in the main note.  Finite algebra and numerical
stress tests are not represented as proof of those lemmas.

No formal figure is required for this analytic identity: a plot would not
verify compact ODE observability or the exponential-polynomial trace.  This
decision does not waive the source, certificate, independent-audit, or
publication gates.

## 8. Final boundary

R0.75W closes the carrier-frequency gap for one exact dyadic two-harmonic
shear.  Three or more modes, arbitrary packets, projection from a larger
field, arbitrary-field E.24, Version-M extraction, suitable-weak transfer,
regularity, and singularity remain open.  **NOT CLAY.**
