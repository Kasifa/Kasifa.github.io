# Independent analytic audit: R0.73E fixed-half-plane transfer

**Audit date:** 2026-08-30
**Revision rechecked:** 2026-08-30, after all mandatory edits
**Files audited:** `r073e_problem_freeze.md` and
`r073e_halfplane_transfer_proof.md`
**Method:** read-only adversarial check of the operator argument; no finite
Fourier calculation is used as continuum evidence

## 1. Verdict

The main theorem chain is mathematically viable.  I found no counterexample
to the fixed-positive-half-plane theorem, the top-cluster relative
dichotomy, or the logarithmic Volterra transfer under the operator structure

\[
 B_\varepsilon=M+K-\varepsilon L,
 \qquad M^*=-M,
 \qquad K\ \text{compact},
 \qquad L\ge\frac14 I.
\]

The revised proof is **FINAL PASS**.  Every mandatory item from the first
audit has been incorporated and rechecked.  No new hypothesis or numerical
claim was introduced.  The nine theorem claims listed in Section 7 are
supported as `CLOSED`, while the restored full-half-plane and moving-profile
boundaries remain `OPEN`.

## 2. Fixed-half-plane compactness and no pollution

### 2.1 Result

**PASS, revision verified.**

For a fixed \(b>0\) whose boundary line avoids \(\sigma(A_0)\), compactness
of \(\sigma(A_0)\) and analytic Fredholm theory imply that the portion in
\(\{\operatorname{Re}z>b\}\) is finite.  An infinite sequence there would
have a spectral accumulation point; the boundary condition rules out
accumulation on \(\operatorname{Re}z=b\), while compact perturbation of the
skew-adjoint multiplication operator rules out accumulation in the open
right half-plane.

The high-imaginary estimate

\[
 \|(z-H_\varepsilon)^{-1}\|
 \le (|\operatorname{Im}z|-\|M\|)^{-1}
\]

and the second Neumann factor for \(K\) control both imaginary tails.  The
dissipative estimate controls sufficiently large positive real part.  What
remains after the fixed cluster disks are removed is a compact subset of
\(\rho(A_0)\), so the compact-Fredholm argument applies uniformly.  This is
the missing noncompact-to-compact splice that the local R0.73D contour alone
could not supply.

Revised Section 4 explicitly states that disjointness of the boundary line
and the compact inviscid spectrum gives positive separation, then invokes
analytic Fredholm accumulation only at the essential spectrum on the
imaginary axis.  This closes the finiteness step.

### 2.2 Compact sandwich

**PASS, revision verified.**

The identity

\[
 G_\varepsilon-R_\varepsilon
 =G_\varepsilon K R_\varepsilon
\]

is sufficient.  On a fixed contour,
\(G_\varepsilon K=F_\varepsilon^{-1}R_\varepsilon K\) converges in norm and
has compact limit.  The adjoint strong-resolvent convergence then gives
\(G_0K(R_\varepsilon-R_0)\to0\) in norm.  This proves norm convergence of
the compact sandwich.  Writing this two-term decomposition once will make
both the Riesz-projection and the \(B_\varepsilon\Pi_\varepsilon\) arguments
auditable.  Revised equation (4.5a) contains exactly this decomposition and
records which term uses adjoint-strong convergence.

## 3. Reduced resolvent, commutation, and domains

**PASS, revision verified.**

The statement that \(G_\varepsilon(z)Q_{\varepsilon,b}\) is analytic through
the projected eigenvalues is correct when read as a meromorphic extension.
At such a point the full resolvent itself does not exist.  The revised proof
records the Riesz decomposition

\[
 H=\Pi_{\varepsilon,b}H\oplus Q_{\varepsilon,b}H,
 \qquad
 Q_{\varepsilon,b}D(B_\varepsilon)
 \subset D(B_\varepsilon),
 \qquad
 B_\varepsilon Q_{\varepsilon,b}
 =Q_{\varepsilon,b}B_\varepsilon
 \quad\text{on }D(B_\varepsilon).
\]

Let \(C_{\varepsilon,b}\) be the part of \(B_\varepsilon\) in
\(Q_{\varepsilon,b}H\).  Then the required object is

\[
 \widehat G_{\varepsilon,b}(z)
 =(z-C_{\varepsilon,b})^{-1}Q_{\varepsilon,b}.
\]

It agrees with \(G_\varepsilon(z)Q_{\varepsilon,b}\) wherever the full
resolvent is defined and is analytic across the spectrum assigned to the
finite Riesz block.  Pairing \(\widehat G\) with unit vectors and applying
the scalar maximum principle on each disk then gives the operator-norm
bound.  The uniform projection bound follows from
\(\Pi_{\varepsilon,b}\to\Pi_{0,b}\) in norm.

Revised equations (5.2a)--(5.2b) now record domain invariance, commutation,
the part operator, and the extended reduced resolvent.  The proof applies
the scalar maximum principle after pairing with unit vectors.  No commutator
with the fixed inviscid projection is needed, and no graph-norm convergence
is being smuggled into this step.

## 4. Top cluster and relative dichotomy

### 4.1 Top set and gap

**PASS, revision verified.**

The positive spectral abscissa \(a\) is attained.  Every point of the top
set is discrete, and the top set is finite.  After removing its Riesz block,
the complementary spectrum is compact and cannot approach a top point
because every top point is isolated.  Thus its spectral abscissa
\(\beta<a\).  The revised proof states this compactness argument before
choosing

\[
 \max\{\beta,0\}<b<c<a.
\]

With this choice the line \(\operatorname{Re}z=b\) automatically avoids the
inviscid spectrum and the half-plane projection is exactly the complete top
projection.  Projecting only the certified \(\sigma_*\) would not suffice,
and the proof correctly avoids that unsupported step.  Revised Section 6
now gives this compactness/isolation argument and chooses
\(\max\{\beta,0\}<b<c<a\).

### 4.2 Bromwich shift and uniform prefactor

**PASS, revision verified.**

For each \(\varepsilon>0\), \(-\varepsilon L\) generates an analytic
semigroup and \(M+K\) is bounded, so \(B_\varepsilon\), and hence its invariant
part \(C_\varepsilon\), generate analytic semigroups.  This justifies the
initial inverse-Laplace formula for \(t>0\) on a common line
\(\operatorname{Re}z=\omega>\|K\|\).

The horizontal sides in the truncated contour are controlled by the Section 3
high-frequency estimate uniformly throughout the strip
\(b\le\operatorname{Re}z\le\omega\), together with the uniform bound on
\(Q_\varepsilon^{\rm top}\), as the revision now states.

On the new line, the exact integration-by-parts identity is

\[
 e^{tC_\varepsilon}
 =\frac{e^{bt}}{2\pi t}
  \int_{\mathbb R}e^{i\tau t}
  (b+i\tau-C_\varepsilon)^{-2}\,d\tau,
 \qquad t>0.
\]

The boundary term vanishes because the resolvent is \(O(|\tau|^{-1})\),
and the squared resolvent is uniformly integrable.  The exact sign is now
fixed in (7.5).  The common crude semigroup bound handles
\(0\le t\le1\), giving a genuinely uniform prefactor.

Revised Section 7 starts from the analytic semigroup on a common line
\(\omega>\|K\|\), uses the Section 3 estimate throughout the strip, and
gives the exact integration-by-parts identity without a sign ambiguity.
The inverse group on the finite top block is valid even for non-semisimple
eigenvalues: fixed contours lying in \(\operatorname{Re}z>c\) absorb possible
Jordan polynomial factors into the exponential slack.  It must continue to
be described as a finite-block inverse group, not a negative-time semigroup
on all of \(H\).

## 5. Bounded drift and logarithmic Volterra transfer

### 5.1 Operator typing

**PASS, revision verified.**

The proof initially defines \(A(d)\) on \(X\), whereas the perturbation in
the \(H\)-space evolution is its conjugate.  Define

\[
 \widetilde A(d)=UA(d)U^{-1},
 \qquad
 E_\varepsilon(\theta)
 =\widetilde A(\varepsilon\theta)-\widetilde A(0).
\]

Then the estimate \(\|E_\varepsilon(\theta)\|\le(49/4)\varepsilon\theta\)
has the correct source and target spaces.  The elementary Fourier bounds
and the constant \(49/4\) check correctly.  Revised equations (9.0)--(9.4)
use this typing consistently.

### 5.2 Quantifiers and error exponent

**PASS.**

For each fixed \(M>0\), set \(\delta=1/(4M)\).  The semigroup constant may
depend on \(M\), but not on \(\varepsilon\).  Weighted Gronwall gives

\[
 \|q(t)\|\le C_\delta e^{(a+\delta)t}
 \exp\!\left(\tfrac12C_\delta C_A\varepsilon t^2\right),
\]

and the Duhamel error relative to the frozen eigenmode is bounded by

\[
 C\varepsilon T_\varepsilon^2
 \exp\!\left((\delta+\eta_\varepsilon)T_\varepsilon
 +C\varepsilon T_\varepsilon^2\right).
\]

Because \(M\eta_\varepsilon<1/4\) eventually, this is
\(O_M(\varepsilon^{1/2}\log^2(1/\varepsilon))\).  The order of the quantifiers
is therefore

\[
 \forall M>0\ \exists\varepsilon_M>0\ \forall
 0<\varepsilon<\varepsilon_M.
\]

No eigenvalue convergence rate is used.

The earlier ambiguous comparison of two unspecified \(o(1)\) terms has been
replaced by the invariant statement

\[
 \liminf_{\varepsilon\downarrow0}
 \frac{\log\|U_\varepsilon(T_\varepsilon,0)\|}
      {\log(1/\varepsilon)}
 \ge Ma\ge M\sigma_*>0.17035M.
\]

This is exactly what is needed for the polynomial no-go.  Revised Section 10
also preserves the order
\(\forall M\,\exists\varepsilon_M\,\forall\varepsilon<\varepsilon_M\);
no quantitative eigenvalue rate is assumed.

## 6. Exact row and complete-row consequence

**PASS, revision verified.**

The earlier definition is

\[
 G_{1/2}(\Lambda;d_*)
 =\sup_{0\le d\le d_*}
 \|U_{1/2,\Lambda}(d,0)\|_{\mathcal K_{1/4}\to\mathcal K_{1/4}}.
\]

This supremum is why a lower bound at
\(d_\Lambda=M\log|\Lambda|/|\Lambda|<d_*\) implies a lower bound for the
fixed observation window.  Revised Section 11 now restates this definition
before using it.

For the chosen row

\[
 \beta=\xi=0,
 \qquad \gamma=\tfrac12,
 \qquad \mu=\tfrac14,
\]

the exact OS--Squire system is triangular and the Squire forcing coefficient
\(i\xi\Lambda\) vanishes.  Zero initial Squire data therefore stay zero.  The
kinetic identity is

\[
 \|u\|_2^2
 =\mu^{-1}\bigl(\|L^{-1/2}q\|_2^2+\|\eta\|_2^2\bigr),
\]

and \(U=2L^{-1/2}\) is unitary from the OS kinetic space to \(H\).  Thus the
OS lower bound embeds isometrically into this complete Fourier row.  A
complete-row upper bound that covers all rows must dominate this row.  This
closes the fixed-degree polynomial no-go without claiming the still-open
complete OS--Squire \(A_2\) direct-sum estimate.

Complex conjugation maps the \(s=+1\) moving equation to the \(s=-1\)
equation because \(W\) and \(L\) are real.  Hence the limit is for both signs,
not merely along a subsequence.

Revised Section 11 writes the selected row, records that zero Squire data
remain zero, includes the exact kinetic identity, and replaces the former
incorrect cross-reference with the spectral-abscissa lower bound
\(a\ge\sigma_*>0.17035\).

## 7. Claim-boundary audit

The rechecked proof supports the following final states:

```text
fixedPositiveHalfPlaneNoPollution=CLOSED
allModesRightOfBProjectionNormPersistence=CLOSED
topInviscidClusterExists=CLOSED
topViscousClusterPersistence=CLOSED
topReducedHalfPlaneResolventUniform=CLOSED
frozenTopClusterRelativeDichotomy=CLOSED
fixedFrozenGeneratorVolterraTransfer=CLOSED
logFastTimeTransfer=CLOSED
superPolynomialCompleteRowNoGo=CLOSED
```

The stated open claims are correctly not inferred from this theorem.  The
revised proof and problem freeze have restored the inherited boundary:

```text
globalRightHalfPlaneNoPollution=OPEN
```

The theorem proves
\(\forall b>0\ \exists\varepsilon_b>0\) control of
\(\operatorname{Re}z\ge b\).  It does not prove one viscosity threshold
that controls the entire open half-plane \(\operatorname{Re}z>0\); spectral
points could in principle approach the imaginary axis as
\(\varepsilon\downarrow0\).  This is distinct from, and is listed beside,
`uniformHalfPlaneBoundAtBEqualsZero=OPEN`.

For the same reason, no moving-profile exponential dichotomy is proved.
The Volterra argument proves a selected lower bound without a moving Riesz
projection.  The revised ledgers now explicitly retain
`movingProfileEvolutionDichotomy=OPEN`.

## 8. Source-integrity recheck

**PASS.**  The missing backslashes, malformed `\max`, unmatched display
delimiters, form-feed character, and wrong cross-reference identified in the
first audit have all been repaired.  The recheck found:

- 80 opening and 80 closing display delimiters in the proof;
- 24 opening and 24 closing display delimiters in the problem freeze;
- zero form-feed characters and zero tab characters in both files;
- no `git diff --check` errors.

## 9. Final audit conclusion

The corrected analytic proof is sufficient for the stated
fixed-positive-half-plane splitting, top-cluster relative dichotomy,
logarithmic moving-profile transfer, and fixed-degree polynomial no-go for
every complete-row bound that must cover the selected row.  The argument is
operator-theoretic; finite diagnostics are not used to prove continuum
spectrum, resolvent bounds, or moving transfer.

Final status:

```text
r073eIndependentAnalyticAudit=PASS
```

This result does not identify the rightmost eigenvalue, control the whole
open right half-plane with one viscosity threshold, prove a moving-profile
dichotomy, establish a fixed-window exponential law, or address nonlinear
Navier--Stokes regularity or the Clay problem.
