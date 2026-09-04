# R0.75S primary analytic audit

## Audit object

- Main note: `research/r075s_full_frequency_single_harmonic_clock_payment.md`
- Audit type: exact radial reduction, phase--node lemma, scale ledger, and
  claim-boundary audit
- Current verdict: **PASS**
- Mathematical blocker count: **0**
- Release blocker count: **0**

The finite certificate will bind the final main-note SHA-256 after independent
review.  This author-side audit does not authorize publication.

## 1. Exact radial reduction

The cross-sectional identity `D_R(y)=-2pi y vartheta(|y|/R-a)` is odd.
In the square of one real harmonic, the constant row and the cosine row are
even in `y`, so both vanish against `D_R`.  The remaining sine row gives
exactly S.13, including the factor `A^2B/4` and the phase
`2phi+2kBt`.  No absolute value is taken before these cancellations.

For `g_a(z)=z vartheta(|z|-a)`, support has fixed width around `+/-a` and
all fixed derivative `L^1` norms are `O_N(a)`.  Direct `L^1`, the low-
frequency inequality `|sin(2qz)|<=2q|z|`, and `N` integrations by parts
give the three simultaneous rows

\[
 |S_{k,R}|\le C_NaR^2\min\{\varepsilon,1,q^{-N}\},
 \qquad q=kR,\quad\varepsilon=kaR.
\]

The small row is `q a^2 R^2=aR^2 epsilon`; no power of `R` is missing.

## 2. Plateau node geometry

The rectangular subcollar has `x_1` fibre at least `4delta_0R`, `x_3`
length `aR/2`, and `x_2=aRz` with `|z|<=1/4`.  Its volume factor is
therefore `2delta_0 a^2R^3` times the normalized `z` integral.

The only degeneracy of that integral occurs when `epsilon` and the distance
from `phi` to a cosine node are both small.  After translating the nearest
node, the elementary lower bound for `|sin r|` reduces the claim to

\[
 \int_{-1/4}^{1/4}|\varepsilon z-r_0|^3dz
 \ge c(\varepsilon+|r_0|)^3.
\]

Outside a fixed neighborhood of this degeneracy, compactness on one phase
period gives a uniform positive lower bound.  This verifies S.20--S.21,
including the endpoint `epsilon=2pi`.

## 3. Moving-phase lemma

Let `J=int_0^1 Q_epsilon(phi+sigma s)^3 ds`.  For `|sigma|<=1`, the phase
interval has length `|sigma|`; minimizing its third distance moment by
centering it at a node gives

\[
 J^{1/3}\ge c\min\{1,\varepsilon+|\sigma|\}.
\]

Together with `|sin(2psi)|<=2Q_epsilon(psi)` and Holder, this gives
`|sigma| int |sin| <= C J^(2/3)`.

For `|sigma|>=1`, the same distance moment is bounded below by a positive
constant.  The weight `w=eta exp(-2lambda s)` satisfies
`Var(w)<=2` for every `lambda>=0`: the increasing eta row contributes at
most one and the exponential row contributes at most one.  BV integration
by parts bounds `sigma int w sin` by a constant.  This verifies S.22 for
arbitrary phase speed, including arbitrary constant `B`.

A direct fixed-grid quadrature is not a valid certificate in the fast-phase
regime: it can alias the oscillation.  The release certificate must use the
exact endpoint/BV identity there rather than claim a sampled numerical
proof.

## 4. Low-frequency power ledger

When `epsilon<=2pi`, sufficiently large `a` gives
`lambda=k^2T_R=4q^2<=16pi^2/a^2<=1`.  The low radial row gives
`|S|/k<=Ca^2R^3`.  After `sigma=kBT_R`, S.22 therefore bounds the flux by
`CA^2a^2R^3J^(2/3)`.  The plateau mass is at least
`cA^3a^2R^3T_RJ`.  Hence

\[
 a^{2/3}R^{-1/3}M^{2/3}
 \asymp A^2a^2R^3J^{2/3}
\]

because `T_R=4R^2`.  This confirms S.30.

## 5. High-frequency power ledger

When `epsilon>=2pi`, the Q phase-uniform subcollar gives
`M>=cA^3a^2R^3 min(T_R,k^(-2))`.  BV phase integration gives
`|T|<=CA^2|S|/k`.

- If `q<=1`, then `q>=2pi/a`, so `|S|/k<=CaR^3/q<=Ca^2R^3`, while the
  target lower scale is `a^2R^3`.
- If `q>=1`, one radial integration by parts gives
  `|S|/k<=CaR^3q^(-2)`.  The target lower scale is
  `a^2R^3q^(-4/3)`, which is larger because
  `q^(-2)<=q^(-4/3)` and `a<=a^2`.

The low/high split overlaps at `epsilon=2pi`; the two high-frequency
subcases overlap at `q=1`.  Thus every integer `k>=1` is covered.

## 6. Normalization and scope

Using `p=R^(-2)omega M` and `X=(omega/R)[T]_+`, S.4 leaves exactly

\[
 X\le Ca^{2/3}\omega^{1/3}p^{2/3}.
\]

All powers of `R` cancel.  Its logarithmic `L^2` rate is
`-c_gamma/12`; the polynomial `a^(2/3)` is harmless.

The exact velocity `u=(0,B,F)` has zero divergence,
`(u dot grad)u=(0,0,B partial_2F)`, and solves the unforced equation with
constant pressure.  Its constant background is not asserted to satisfy the
frozen mean-zero, inversion-paired Version-M conditions.  S.39 additionally
requires the entire time window and spacetime tube to be aligned with the
same exterior measurement row and the same actual velocity component.

Multimode interference, projections of larger fields, nonconstant shear,
vertical structure, E.24, complete Version-M extraction, suitable-weak
transfer, regularity, and singularity remain open.  No novelty or priority
claim is made.  **NOT CLAY.**

## Audit conclusion

The exact reduction, radial coefficient bounds, node geometry, phase lemma,
two scale ledgers, normalization, exact-solution status, and claim boundaries
are internally consistent.  The draft is ready for independent finite-
certificate construction.
