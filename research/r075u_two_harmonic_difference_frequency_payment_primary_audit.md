# R0.75U primary audit -- complete-clock difference-frequency payment

## 0. Frozen objects and verdict

- Main note: `research/r075u_two_harmonic_difference_frequency_payment.md`
- Audited main SHA-256:
  `f9fb331cf880b20f3b407fe66453bce71517ac1ef2af4fa0863c00325c1022a4`
- Source report: `research/r075u_report-source.md`
- Audited source SHA-256:
  `d0e9356a162b683a33c5b4c49692a62962d2a9c63cccba9eb9d84040aaf4a01f`
- Current verdict: **PASS**
- Mathematical blocker count: **0**
- Release blocker count: **0**

The audit certifies U.4 only for the difference-frequency component U.2 of
one exact two-harmonic dyadic pair.  It does not certify the remaining two
self-frequency rows, the sum-frequency row, or a complete two-mode theorem.

## 1. Radial quotient audit

For every integer `n>=1`, the frozen radial coefficient satisfies

\[
 |J_{n,R}|\le CaR^2\min\{naR,1\}.
\]

If `naR<=1`, division by `n` gives `Ca^2R^3`.  If `naR>=1`, then
`n^(-1)<=aR`, and the direct `CaR^2` row gives the same bound.  Thus U.10 is
uniform and introduces no unrecorded difference-frequency threshold.

## 2. Phase-distance moment audit

Let `tau=min{1,Lambda^(-1)}`, with `tau=1` when `Lambda<=1`, and let
`P=|sigma|tau`.  The function in U.12 is the distance to one periodic
lattice, clipped at one.  On a phase interval of length below one, it is
piecewise affine with slopes `+/-1`; an interval that crosses a node has
cubic mean equal to a fixed fraction of the cube of its endpoint scale.  On
a phase interval of length at least one, either the clipped region itself or
one complete affine portion supplies a fixed positive mean.  Rescaling the
time interval therefore gives

\[
 \int_0^\tau h(s)^3\,ds
 \ge c\tau\min\{1,h(0)+P\}^3.
\]

The exponential factor is at least `e^(-3/2)` on `[0,tau]`.  Raising the
last lower bound to the power `2/3` proves U.16 with the correct
`tau^(2/3)q^2` scale.

## 3. Slow- and fast-phase audit

### Slow phase, `Lambda<=1`

Here `tau=1` and `|sigma|<=1`.  On the full interval `[0,4]`, Lipschitz
continuity of the lattice distance gives

\[
 |\sin(\alpha+\sigma s)|\le Cq,
 \qquad q=\min\{1,h(0)+|\sigma|\}.
\]

The weighted integral is therefore at most `C|sigma|q`.  Since
`q>=|sigma|`, this is at most `Cq^2`, matching U.16.

### Slow phase, `Lambda>=1`

The cutoff onset and derivative bound imply `zeta(s)<=C_eta s`.  The exact
Laplace moments are

\[
 \int_0^\infty se^{-\Lambda s}\,ds=\Lambda^{-2},
 \qquad
 \int_0^\infty s^2e^{-\Lambda s}\,ds=2\Lambda^{-3}.
\]

Using `|sigma|tau<=1` gives the U.18 upper bound
`C|sigma|tau^2q`.  Because `q>=|sigma|tau`, this is at most
`C tau q^2<=C tau^(2/3)q^2`.

### Fast phase

For `w=zeta e^(-Lambda s)`, one integration by parts is legitimate because
`w(0)=0`.  If `Lambda<=1`, the endpoint and total variation are uniformly
bounded.  If `Lambda>=1`,

\[
 \int|\zeta'|e^{-\Lambda s}\,ds\le C\Lambda^{-1},
 \qquad
 \Lambda\int\zeta e^{-\Lambda s}\,ds\le C\Lambda^{-1}.
\]

Thus the fast-phase row is `O(tau)`.  In this case `q=1`, and
`tau<=tau^(2/3)`, so U.16 again closes the estimate.  These three cases cover
all `Lambda>=0`, `sigma in R`, and `alpha in R`.

## 4. Scaling and amplitude audit

If `AC=0`, U.2 vanishes.  Otherwise set

\[
 \Lambda=(k^2+m^2)R^2,\qquad\sigma=dBR^2,
 \qquad t=R^2s.
\]

The original time integral is `AC/d` times the left side of U.13.  From
U.23,

\[
 R^{-2}\int_0^{T_R}H(t)^3\,dt
 \ge(AC)^{3/2}\int_0^4e^{-3\Lambda s/2}h(s)^3\,ds.
\]

Taking the `2/3` power cancels `AC` exactly and produces
`d^(-1)R^(-4/3)`, as stated in U.24.  Multiplication by U.10 gives
`a^2R^(5/3)`.  Finally, U.26 has coefficient `a^2R^3`; solving it for the
defect integral and taking the `2/3` power gives

\[
 a^2R^{5/3}(a^2R^3)^{-2/3}
 =a^{2/3}R^{-1/3}.
\]

This proves the scaling in U.4.  Substituting
`M=R^2omega^(-1)p` into `(omega/R)U.4` cancels every power of `R` and leaves
`a^(2/3)omega^(1/3)p^(2/3)`.  The frozen value
`c_gamma=8/3969` gives `-c_gamma/12=-2/11907`.

## 5. PDE, source, and claim audit

Each harmonic in U.1 solves the transported heat equation, so their finite
sum does as well.  For `u=(0,B,F(t,x_2))`, divergence vanishes,
`(u dot grad)u=(0,0,B partial_2F)`, and
`Delta u=(0,0,partial_2^2F)`.  The exact shear embedding is therefore
correct.  The nonzero constant background is expressly not claimed to lie
in the frozen mean-zero, inversion-paired Version-M subclass.

The conditional Version-M row retains the same complete clock, plateau tube,
row weight, and actual-component requirements as R0.75S.  It is not applied
to a Fourier projection and does not convert the component estimate into a
bound for the complete flux.

The source report binds primary neighboring records on shear mixing, torus
spectral observability, heat observability, and the official Clay problem.
None is imported into the proof of U.13.  The search is explicitly bounded
and establishes no novelty, completeness, or priority claim.

The open boundary is accurate: the combined self/sum block, complete
two-mode payment, low carriers, three or more modes, arbitrary packets,
arbitrary-field E.24, Version-M extraction, suitable-weak transfer,
regularity, and singularity remain open.  **NOT CLAY.**

## 6. Finite-check boundary

A coarse fixed-grid scan can alias the fast phase in U.13 and report a false
large ratio.  It is therefore excluded from proof evidence.  The finite
certificate may verify exact rational scale ledgers, regime fixtures,
bindings, tags, and mutation rejection; only the analytic argument above
certifies the continuum phase lemma.
