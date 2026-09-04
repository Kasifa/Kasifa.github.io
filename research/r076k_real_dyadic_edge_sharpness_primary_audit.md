# R0.76K primary mathematical and source audit

## Verdict

**PASS -- single-slice theorem only; complete-clock flux remains open.**

The main note proves that the Chebyshev edge exponent and the linear `L2`
endpoint factor survive reality, conjugate pairing, a single dyadic band,
positive integer spatial modes, and exact heat-shear realization at one
prescribed scaled time.  It also closes the signed two-cap algebra at that
slice and proves an exact parabolic warning against a cost-free extension
to the full clock.  It does not claim a complete signed-flux lower bound
against the full physical plateau.

## Frozen dependency boundary

The upstream locally reconstructed edge theorem is bound to:

| artifact | SHA-256 |
|---|---|
| `research/r076j_local_edge_extrapolation_reconstruction.md` | `a3d67c8a27ef6ffb7068313732e8e8a08ba98931226df726ac4ee2140ab0f57f` |
| `research/r076j_local_edge_extrapolation_reconstruction_primary_audit.md` | `1b2a608c6ffe16c35489b95fd384f0f47a1d4a79b22491a7825ac53382a746d5` |

The exact upstream research commit is
`25d44e986d5283107816f910f89b94bceb1d5726`.  This is the twelve-file
R0.76J research commit, not the later publication-handoff commit.  A hash
or commit mismatch invalidates the comparison until re-audited.

## Coefficient and class audit

For a real degree-`n` polynomial, direct binomial expansion gives

\[
 b_j(\epsilon)=\sum_{r=j}^na_r(i\epsilon)^{-r}
 (-1)^{r-j}{r\choose j}.
\]

Taylor expansion at `i/epsilon` independently gives
`b_j=p^(j)(i/epsilon)/(j!(i epsilon)^j)`.  Multiplication by
`(i epsilon)^n` isolates the nonzero limit
`a_n(-1)^(n-j)C(n,j)`.  Therefore every transformed coefficient is
nonzero only for sufficiently small `epsilon`; the main note correctly
does not assert nonvanishing for every positive `epsilon`.

Realification produces `q=n+1` positive cosine frequencies and their
negative conjugates.  Hence there are `2q` complex exponential branches.
The condition `n epsilon<M` places all positive frequencies strictly
between `M` and `2M`; the closed dyadic definition also permits the upper
endpoint.  The note correctly compares this with R0.76J using `N<=2q`
and does not infer a `T_q` statement from class inclusion.

## Pointwise and integrated constants

For `p=T_n`, `M=1`, and `theta=-(1+d)`, the limiting real profile is
`2T_n(t)cos(t-(1+d))`.  Its endpoint numerator is `2T_n(1+d)`, while its
`L2` denominator is at most `2||T_n||_2`.  The standard bounds

\[
 \|T_n\|_2\le\sqrt2,\qquad
 T_n(1+d)\ge\frac12e^{n\operatorname {arcosh}(1+d)}
\]

give the exact amplitude prefactor `1/(2sqrt(2))`.  The simplification
`arcosh(1+d)>=sqrt(d)` is used only for `0<=d<=1`.

On `J_d=[1+7d/8,1+d]`, the carrier phase has absolute value at most
`d/8<=1/8`, so its square is at least `1/2`.  Chebyshev monotonicity gives
the square prefactor `1/4`, realification contributes `4`, and the interval
has length `d/8`.  Thus

\[
 4\cdot\frac14\cdot\frac12\cdot\frac d8
 =\frac d{16}
\]

is the exterior numerator coefficient.  The core `L2` square is at most
`8`, yielding `d/128`.  For the `L3` pairing, the core cube is at most
`16` and `16^(2/3)<8`, so the same displayed constant is conservative.
K.2, K.3, and K.20: **PASS**.

## Endpoint polynomial audit

For

\[
 p_n^*(t)=\sum_{m=0}^n\frac{2m+1}{2}P_m(t),
\]

Legendre orthogonality and `P_m(1)=1` give

\[
 p_n^*(1)=\|p_n^*\|_2^2=\frac{(n+1)^2}{2}=\frac{q^2}{2}.
\]

The resulting `L2` endpoint ratio is `q/sqrt(2)`.  Since
`|P_m(t)|<=1` on the interval, `||p_n^*||_infinity<=q^2/2`, and therefore
`||p_n^*||_3^3<=q^4/4`.  The `L3` endpoint ratio is at least
`2^(-1/3)q^(2/3)`, whose square is `2^(-2/3)q^(4/3)`.  The note correctly
leaves the gap to the squared `q^2` upper factor open.  K.21--K.24:
**PASS**.

## Exact integer heat-shear slice

With zero-based indices `j=0,...,q-1`, the choices

\[
 \eta_L=e_aaR,\qquad n_j=n_0+j,\qquad
 n_0\ge\max\{1,q-1\},\qquad M_L=n_0\eta_L
\]

give positive consecutive integers satisfying
`n_(q-1)<=2n_0`.  At each prescribed pair `(s_*,B)`, the exact choices

\[
 A_j=2|b_j|e^{n_j^2R^2s_*},qquad
 \phi_j\equiv-\theta-\arg b_j-n_jBR^2s_*\pmod{2\pi}
\]

obey

\[
 A_je^{-n_j^2R^2s_*}=2|b_j|,qquad
 -\phi_j-n_jBR^2s_*\equiv\theta+\arg b_j.
\]

Thus K.29 follows term by term.  The heat compensation has the positive
sign and contains `n_j^2R^2`, not `kappa_j^2`; the transport term in
`phi_j` has the negative sign.  The quantifier is explicitly
`for all (s_*,B), there exist (A_j,phi_j)`, not one packet for all times.
K.25--K.30: **PASS**.

## Growing-degree audit

For `eta<=1/8` and `|x|<=2`, the exponential remainder gives
`|w_eta(x)-x|<=2eta`, and the connecting segment lies in the disk of
radius `9/4`.  The Chebyshev and Legendre coefficient recurrences obey the
`l1` majorant `(1+sqrt(2))^m`; since `(9/4)(1+sqrt(2))<6`, the derivative
bound gives `C eta q6^q` for `T_(q-1)` and `C eta q^2 6^q` for the
normalized endpoint kernel.

The normalized kernel's leading coefficient is

\[
 \frac{2q-1}{2q}2^{-(q-1)}{2q-2\choose q-1}\ge\frac34.
\]

After multiplying the transformed coefficients by `(i eta)^(q-1)`, the
lower-degree remainder is uniformly at most `C eta q5^q`.  Hence
`eta q^2 7^q->0` makes every coefficient nonzero eventually and also gives
`eta q->0`, which validates `n_0=ceil(1/eta)>=q-1`.

Since `eta=(a-delta_0)exp(-rho L^2/4)`, every `q=o(L^2)` meets this
condition.  The stronger density condition
`limsup q/L^2<rho/(4log7)` is also sufficient.  The proof does not cover
all `q=o(L^(5/2))`, and the note labels this as a proof limitation rather
than a failure example.  K.31--K.39: **PASS**.

## Signed slice and parabolic gate

Put `A=a-delta_0`.  The full shell projection has
`|x|<=(a+delta_0)/A=1+2delta_0/A`.  On the fixed positive subcap, the
smallest normalized exterior gap is
`(r_c-h+delta_0)/A`, strictly larger because `r_c-h>delta_0`.  Expanding
`arcosh(1+c/A)` gives K.43 and the positive gap
`Gamma_m` of order `m/sqrt(A)`.

For `U_m(x)=2T_m(x)cos(x-pi/4)`, parity gives exactly

\[
 U_m(x)^2-U_m(-x)^2=4\sin(2x)T_m(x)^2.
\]

On the entire fixed support of `vartheta`, `x=1+O(1/a)`, so the sine is
uniformly positive for large `a`.  With a fixed `v<0`, every paired cap term is
nonnegative; the selected subcap supplies a uniform positive weight.  The
cap square divided by the two-thirds power of the full-plateau spatial
cube therefore contains the exponent `2Gamma_m`.  K.41--K.45: **PASS**.

The normalized PDE has drift `v/e_a` and diffusion `A^(-2)`.  Conjugating
the heat semigroup past `e^(iM_Lx)` gives exactly K.46, including the
imaginary shift `2iM_Ltau/A^2` and scalar decay `exp(-M_L^2tau/A^2)`.
For fixed `m`, its confluent limit is the heat-transformed polynomial, not
a common scalar multiple.

The explicit even-Chebyshev coefficients in K.47 give the same-sign sum in
K.48.  For `j<=n/2`, its factorial coefficient is at least
`(n/2)^(2j)`.  With `X=Tn^2/A^2=o(n)`, one term near `j=X` and Stirling's
bound prove `exp(cX)`; `1+X` handles `X<1`.  Thus the backward warning
`exp(cTm^2/A^2)` is valid for `m=o(A^2)`.  In the overlapping range
`A^(3/2)<<m=o(A^2)`, that cost
exceeds `Gamma_m=O(m/sqrt(A))`.  This disproves only a cost-free
Gamma-ledger bridge from a terminal slice, not the final quotient for every
possible packet.  K.46--K.48: **PASS**.

## Source and claim audit

The v1 TeX source of Zhang places the Chebyshev lower construction in
Proposition 7.1.  The main note and source report use that number.  The
official arXiv record, the ICALP publisher record for Chen--Price, and NIST
DLMF were checked for their stated roles.  The bounded collision search
found no exact combined real/dyadic/integer-heat-shear statement, but the
report explicitly says this is not evidence of novelty or priority.

The main note separates literature architecture, local proof, finite
computation, and open claims.  It states that no simulation or formal
figure is needed.  It makes no full-clock flux, `q=o(L^(5/2))` lower-range,
arbitrary-field, regularity, singularity, novelty, priority, or Clay claim.

## Finite-certificate boundary

The finite certificate may verify exact polynomial expansions, rational
sample integrals, dyadic indices, phase residuals, constant and exponent
ledgers, dependency hashes, equation/reference inventories, and negative
controls.  It cannot prove uniform convergence, orthogonal-polynomial
facts, the continuum supremum, the semigroup theorem, or the full PDE
claim.  Those remain in the analytic proof and source audit.

The independent counterexample-first and flux-bridge rereads report no
remaining mathematical blocker after correction of the proposition
number, carrier choice, transformed-coefficient quantifier, phase sign,
normalized drift, whole-support cap pairing, and conditional slab wording.
The release is ready for dual finite certificates and clean-archive QA.
**NOT CLAY.**
