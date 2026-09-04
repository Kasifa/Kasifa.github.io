# R0.76A primary mathematical audit

- Current verdict: **PASS**
- Mathematical blocker count: **0**
- Release blocker count: **0**
- Scope: the frozen primitive, the exact two-frequency cluster, the complete-clock localized-current sign, and the stated narrow obstruction only

## 1. Primitive geometry

The profile in A.1 is nonnegative and even after composition with
`a(|z|-1)`.  Hence

\[
 W_a(z)=-2\pi az\vartheta(a(|z|-1))
\]

is odd, nonnegative on the negative half-line, and nonpositive on the
positive half-line.  Its total integral is zero, so its left primitive
`Xi_a` rises from zero, remains nonnegative, and returns to zero only after
the positive lobe.  This proves A.13 and the support statement A.14.

On the interval `I_-` from A.15, the assumptions give
`vartheta=1` and `|z|>=1-delta0/a>1/2`; the weaker bound used in the note is
therefore valid.  The negative-lobe mass is at least `2 pi delta0`.
The central plateau has length

\[
 2-\frac{2\delta}{a}\ge1.
\]

Integrating the primitive over that plateau proves A.17.  The lower bound
is deliberately non-sharp but uniform in `a`.

## 2. Exact unresolved cluster

With `q=2`, `0<ell<=1/11`, and
`N=ceil(16/ell)`, one has

\[
 16\le N\ell<16+\ell<17.
\]

Thus the carrier is in the high-carrier sector, while the only adjacent
gap has scaled size `ell<16`; it fails the separated-mode gate.  The pair
`(N,N+1)` is therefore a genuine nontrivial Z-sector cluster.  For the
finite fixture `ell=1/11`, the exact values are

\[
 N=176,\qquad \alpha=16,\qquad \beta=\frac1{11},
 \qquad R=\frac1{264},\qquad B=6336.
\]

They give `BR/a=1`, as required by the scaled complete clock.

## 3. Damping, phase, and current signs

The envelope in A.6 is the exact result of factoring the common carrier
heat and transport phase from the two diffusive modes.  Direct
differentiation gives

\[
 Z_s+Z_z-a^{-2}Z_{zz}-2i\alpha a^{-2}Z_z=0
\]

because `mu=(2 alpha beta+beta^2)/a^2`.

The estimates A.19--A.22 hold uniformly for the entire support of `Xi_a`
and all `0<=s<=4`.  In particular, `r>3/4` and the relative phase has
absolute value at most `1/2`.  Substitution into the exact identity

\[
 J=\beta r(r-2\cos(\beta(z-s)))
\]

gives `J<=-9 beta/16`.  Since `beta^2<=alpha beta/8`, the correction
density obeys

\[
 |Z_z|^2+2\alpha J
 \le \frac18\alpha\beta-\frac98\alpha\beta
 =-\alpha\beta.
\]

The sign is therefore uniform, not a one-point artifact.

## 4. Localization and exact boundary

Multiplying the pointwise inequalities by `Xi_a`, the common carrier heat,
and any nonnegative nonzero time cutoff preserves strict negativity because
`Xi_a` has positive mass.  This proves A.30 and A.31.

At the fixture point `s=z=0`,

\[
 Z=1,\qquad Z_z=-\frac{i}{11},\qquad
 J=-\frac1{11},\qquad
 |Z_z|^2+2\alpha J=-\frac{351}{121}.
\]

The complete gradient remains nonnegative because its omitted carrier
density is positive:

\[
 |i\alpha Z+Z_z|^2=\frac{30625}{121}>0.
\]

Accordingly, the result rules out only discarding the localized current or
the current-correction row by a positivity claim.  It does not rule out a
perturbative bound, a signed nonlocal estimate, or a joint multiplier that
retains the carrier-density block.  The exact two-mode collar flux was
already paid in R0.75W, so this is not a flux counterexample.

## 5. Evidence classification

| item | status | reason |
|---|---|---|
| primitive positivity and support | proved analytically | oddness, sign on the two lobes, and zero total mass |
| primitive positive mass | proved analytically | explicit negative-lobe mass and central plateau |
| high-carrier unresolved classification | proved analytically | exact ceiling and strict adjacent-gap inequalities |
| envelope PDE and current formula | proved analytically | direct differentiation and multiplication |
| complete-clock strict negativity | proved analytically | uniform phase/damping bounds and positive multiplier mass |
| finite arithmetic fixture | reproducible computation | checks constants, scaling, signs, and serialization |
| general cluster-current estimate | **OPEN** | arbitrary coefficients and cluster lengths are not controlled |
| full Z-sector flux payment | **OPEN** | no general joint multiplier or cross-cluster estimate is proved |
| Navier--Stokes regularity | **OPEN** | the calculation concerns an exact shear test family only |

The finite fixtures are not represented as proof of the continuum
identities.  The source search is contextual and is not evidence of novelty
or priority.  This gate is analytic; no simulation or formal scientific
figure is needed.  **NOT CLAY.**
