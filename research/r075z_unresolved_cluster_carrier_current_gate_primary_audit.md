# R0.75Z primary mathematical audit

- Current verdict: **PASS**
- Mathematical blocker count: **0**
- Release blocker count: **0**
- Scope: the exact X/Y/Z spectral trichotomy, maximal cluster normal form,
  carrier-current identities, and the stated pointwise obstruction only

## 1. Parameter partition

For fixed `q`, R0.75X permits the choice `C_0=8q`, so
`n_1 ell<8q` is covered.  In the complementary branch,
`n_1 ell>=8q`.  The minimum gap of
`{-n_q,...,-n_1,n_1,...,n_q}` is

\[
 \min\left(2n_1,\min_j(n_{j+1}-n_j)\right).
\]

If every adjacent scaled gap is at least `8q`, this minimum has scaled
value at least `8q`, including the equality case, and R0.75Y applies.
Otherwise at least one adjacent gap is smaller and the family belongs to
the Z-sector.  The branches are disjoint and exhaustive.

Cutting at gaps greater than or equal to `8q/ell` is important: equality
must be a separator.  Summing strict internal inequalities gives the
strict cluster-width bound in Z.4.  The dyadic hypothesis gives
`n_s-N<=2n_1-N<=n_1<=N`.

## 2. Normal form and signs

For an offset mode

\[
 Z_j=A_je^{-(2Nd_j+d_j^2)t}e^{i(d_j(y-Bt)-\phi_j)},
\]

the four coefficients in
`Z_t+B Z_y-Z_yy-2iN Z_y` are

\[
 -(2Nd_j+d_j^2)-iBd_j,
 \quad iBd_j,
 \quad d_j^2,
 \quad 2Nd_j.
\]

They sum to zero.  Expanding `(H+conj(H))^2/4` gives one half of
`|H|^2` plus one half of `Re(H^2)`, proving Z.18 and its flux split.

Twice the real part of `conj(Z) Z_t` gives

\[
 Q_t+BQ_y-Q_{yy}=-2|Z_y|^2-4N\operatorname {Im}(\overline Z Z_y).
\]

Fourier orthogonality gives the nonnegative full-period current in Z.26.
That sign is not a pointwise sign and cannot be moved through an arbitrary
local collar weight.

## 3. Counterexample boundary

At `t=0`, take the envelope `Z=2-e^{iy}`.  At `y=0`,

\[
 Z=1,\qquad Z_y=-i,\qquad
 \operatorname {Im}(\overline Z Z_y)=-1.
\]

Hence `2N|J|=2N` while `|Z|^2+|Z_y|^2=2`; no constant independent of the
carrier can absorb the `N`-weighted absolute current into that unweighted
quantity.  Also `|Z_y|^2+2NJ=1-2N<0`.

This does not deny the elementary estimate
`|J|<=|Z||Z_y|`, an estimate carrying an `N^2|Z|^2` price after Young's
inequality, a nonlocal signed estimate, or cancellation with the carrier
block.  The main note states only the narrower obstruction.

## 4. Evidence classification

| item | status | reason |
|---|---|---|
| X/Y/Z partition | proved analytically | direct comparison with the exact X and Y hypotheses |
| cluster-width bounds | proved analytically | telescoping adjacent gaps and the dyadic band |
| carrier-envelope PDE | proved analytically | termwise differentiation |
| density/carrier split | proved analytically | exact complex square identity |
| local and global current formulas | proved analytically | product rule and Fourier orthogonality |
| pointwise carrier-loss example | proved analytically | exact evaluation at one point |
| full clustered-sector flux payment | **OPEN** | no localized signed-current or joint multiplier inequality is proved |
| cross-cluster aggregation | **OPEN** | the one-cluster square split omits full-field cross products |
| Navier--Stokes regularity | **OPEN** | the calculation concerns an exact shear test class only |

The finite fixtures check arithmetic, equality conventions, signs, and
serialization.  They are not represented as proof of the parameter
partition or continuum identities.  The source search is contextual and
does not support a novelty claim.  No simulation or formal scientific
figure is needed for this analytic gate.  **NOT CLAY.**
