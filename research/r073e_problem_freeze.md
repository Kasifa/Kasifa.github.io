# R0.73E problem freeze: fixed-half-plane splitting and logarithmic transfer

**Frozen:** 2026-08-30
**Parent release:** R0.73D
**One permitted row:** \(d=0\), \(\gamma=1/2\), \(s=+1\), followed by
the exact heat-profile drift \(d=\varepsilon\theta\)
**Evidence target:** an exact operator theorem; finite Fourier calculations
remain diagnostic only

## 1. Input inherited from R0.73D

On the physical kinetic space \(X=X_{1/4}\), R0.73D proved static
small-viscosity persistence for at least one certified inviscid eigenvalue

\[
 \sigma_*\in(0.17035,0.17050).
 \tag{1.1}
\]

After the fixed unitary map \(U=2L^{-1/2}:X\to L^2\), the complete frozen
family is

\[
 \widetilde B_\varepsilon=M+K-\varepsilon L,
 \qquad
 M=-\frac i2M_{W_0},
 \qquad
 L=-\partial_x^2+\frac14,
 \tag{1.2}
\]

where \(M\) is bounded and skew-adjoint, \(K\) is fixed and compact, and

\[
 D(\widetilde B_\varepsilon)=H^2_{\rm per}\quad(\varepsilon>0),
 \qquad
 \widetilde B_0=A=M+K\in\mathcal B(L^2).
 \tag{1.3}
\]

R0.73D controls one fixed small contour.  That local statement by itself
does not control the rest of the spectrum or the complementary semigroup.
R0.73E is allowed to use the full structure (1.2), not only the local
projection conclusion.

## 2. The right spectral object

The certified \(\sigma_*\) is not known to be the rightmost inviscid
eigenvalue.  Define instead

\[
 a:=\max_{z\in\sigma(A)}\operatorname{Re}z.
 \tag{2.1}
\]

Since \(A\) is bounded, its spectrum is compact.  Since \(K\) is compact and
\(\sigma(M)\subset i\mathbb R\), every point with positive real part is an
isolated eigenvalue of finite algebraic multiplicity.  Equation (1.1) gives

\[
 a\ge\sigma_*>0.17035.
 \tag{2.2}
\]

The top set

\[
 \Sigma_{\rm top}:={z\in\sigma(A):\operatorname{Re}z=a}
 \tag{2.3}
\]

is therefore nonempty and finite.  All top points must be projected
together.  A complement theorem for the one selected \(\sigma_*\) is not
permitted unless \(\sigma_*\) is separately proved rightmost.

## 3. Exact theorem contract E1: every fixed positive half-plane

Fix \(b>0\) with

\[
 \sigma(A)\cap\{\operatorname{Re}z=b\}=\varnothing,
 \qquad
 \Sigma_b:=\sigma(A)\cap\{\operatorname{Re}z>b\}.
 \tag{3.1}
\]

The section must prove all of the following for sufficiently small positive
\(\varepsilon\):

1. \(\Sigma_b\) is finite and is surrounded by finitely many fixed disjoint
   contours \(\Gamma_{b,j}\subset\{\operatorname{Re}z>b\}\);
2. the corresponding viscous contours remain in the resolvent set and the
   total Riesz projections satisfy

   \[
    \|\Pi_{\varepsilon,b}-\Pi_{0,b}\|\longrightarrow0;
    \tag{3.2}
   \]

3. every viscous spectral point in \(\{\operatorname{Re}z\ge b\}\) lies
   inside those fixed contours; there is no additional spectrum in that
   fixed half-plane;
4. with \(Q_{\varepsilon,b}=I-\Pi_{\varepsilon,b}\) and
   \(C_{\varepsilon,b}\) the part of \(\widetilde B_\varepsilon\) in
   \(Q_{\varepsilon,b}L^2\), the extended reduced resolvent is uniformly
   bounded:

   \[
    \sup_{0<\varepsilon<\varepsilon_b}
    \sup_{\operatorname{Re}z\ge b}
    \|(z-C_{\varepsilon,b})^{-1}Q_{\varepsilon,b}\|<\infty;
    \tag{3.3}
   \]

5. the finite spectral blocks also converge in operator norm:

   \[
    \|\widetilde B_\varepsilon\Pi_{\varepsilon,b}
      -A\Pi_{0,b}\|\longrightarrow0.
    \tag{3.4}
   \]

This extended object agrees with
\((z-\widetilde B_\varepsilon)^{-1}Q_{\varepsilon,b}\) wherever the full
resolvent exists and remains analytic across the finite projected block.
The constants may depend on the fixed \(b\).  Nothing in E1 is uniform as
\(b\downarrow0\).

## 4. Mandatory noncompact resolvent step

The compact-contour proof from R0.73D is insufficient until the unbounded
half-plane is controlled.  The proof must establish uniform high-frequency
bounds directly.  For \(z=x+i\tau\), \(x>0\),

\[
 z-(M-\varepsilon L)=(z+\varepsilon L)
 \bigl[I-(z+\varepsilon L)^{-1}M\bigr].
 \tag{4.1}
\]

Since \(L\) is positive self-adjoint,

\[
 \|(z+\varepsilon L)^{-1}\|\le |\tau|^{-1}.
 \tag{4.2}
\]

Thus the base resolvent is \(O(|\tau|^{-1})\), uniformly in
\(\varepsilon\), once \(|\tau|>\|M\|\).  A second Neumann factor gives the
same decay for the full resolvent once \(|\tau|\) exceeds a fixed bound
depending only on \(\|M\|+\|K\|\).  High positive real part is controlled
by the accretive base estimate and the bounded compact term.  The remaining
region is a compact rectangle, where the R0.73D compact-Fredholm convergence
applies.

No finite Fourier truncation may replace this step.

## 5. Exact theorem contract E2: top-cluster relative dichotomy

Let \(\Pi_\varepsilon^{\rm top}\) be the viscous continuation of all points
in \(\Sigma_{\rm top}\), and set
\(Q_\varepsilon^{\rm top}=I-\Pi_\varepsilon^{\rm top}\).  The inviscid
complement has a strictly smaller spectral bound.  R0.73E must prove that
there are numbers

\[
 0<b<c<a
 \tag{5.1}
\]

and constants independent of sufficiently small \(\varepsilon\) such that

\[
 \|e^{t\widetilde B_\varepsilon}Q_\varepsilon^{\rm top}\|
 \le C_b e^{bt},
 \qquad t\ge0,
 \tag{5.2}
\]

and, on the finite-dimensional top block,

\[
 \|e^{-t\widetilde B_\varepsilon}
       \Pi_\varepsilon^{\rm top}\|
 \le C_c e^{-ct},
 \qquad t\ge0.
 \tag{5.3}
\]

The negative-time expression in (5.3) is only the inverse group on the
finite-dimensional top spectral block.  Equations (5.2)--(5.3) give a
uniform relative exponential dichotomy after a shift between \(b\) and
\(c\).  They do not give absolute uniform decay of the unshifted complement.

The implication from (3.3) to (5.2) must retain a uniform prefactor.  A
permitted self-contained route is:

1. start the Bromwich formula on a common line to the right of the crude
   growth bound;
2. move it to \(\operatorname{Re}z=b\) using the uniform
   \(O(|\operatorname{Im}z|^{-1})\) resolvent bound;
3. integrate once by parts, so the integrand contains the square resolvent
   and is absolutely integrable;
4. use the common short-time semigroup bound for \(0\le t\le1\).

Writing only “analytic semigroup” or only “Gearhart--Prüss” is not enough.

## 6. Exact theorem contract E3: fixed-generator Volterra transfer

In fast time \(\theta=|\Lambda|d\), put
\(\varepsilon=|\Lambda|^{-1}\).  For \(s=+1\), the exact moving generator
is

\[
 \widetilde B_\varepsilon
 +E_\varepsilon(\theta),
 \qquad
 E_\varepsilon(\theta)
 =\widetilde A(\varepsilon\theta)-\widetilde A(0),
 \qquad
 \widetilde A(d)=UA(d)U^{-1}.
 \tag{6.1}
\]

The explicit heat profile must be used to prove

\[
 \|E_\varepsilon(\theta)\|
 \le C_A\varepsilon\theta
 \tag{6.2}
\]

on every required interval.  This is a bounded perturbation; the unbounded
term \(-\varepsilon L\) remains inside the frozen generator.

For every fixed \(M>0\), set

\[
 T_\varepsilon=M\log(1/\varepsilon).
 \tag{6.3}
\]

The section must select a unit viscous top eigenvector

\[
 \widetilde B_\varepsilon v_\varepsilon
 =\lambda_\varepsilon v_\varepsilon,
 \qquad
 \operatorname{Re}\lambda_\varepsilon\longrightarrow a,
 \tag{6.4}
\]

and prove for all sufficiently small \(\varepsilon\)

\[
 \|U_\varepsilon(T_\varepsilon,0)v_\varepsilon\|
 \ge\frac12
 \exp\bigl(\operatorname{Re}\lambda_\varepsilon T_\varepsilon\bigr).
 \tag{6.5}
\]

Consequently the logarithmic growth rate satisfies

\[
 \liminf_{\varepsilon\downarrow0}
 \frac{\log\|U_\varepsilon(T_\varepsilon,0)\|}
      {\log(1/\varepsilon)}
 \ge Ma\ge M\sigma_*>0.17035M.
 \tag{6.6}
\]

For \(s=-1\), the eigenvalue and initial vector are obtained by complex
conjugation.  The initial vector may depend on \(\varepsilon\) and on the
sign.  This is an operator-norm lower bound, not a single fixed-orbit
statement.

In physical time,

\[
 d_\varepsilon=M\varepsilon\log(1/\varepsilon)\longrightarrow0.
 \tag{6.7}
\]

Thus for every fixed \(d_*>0\) and every \(p>0\), the exact row gain from
R0.73C must satisfy

\[
 \lim_{|\Lambda|\to\infty}
 \frac{G_{1/2}(\Lambda;d_*)}{|\Lambda|^p}=\infty.
 \tag{6.8}
\]

Equation (6.8) excludes every fixed-degree polynomial upper bound for this
one row.  For the complete Fourier-row implication the proof must explicitly
use \(\beta=\xi=0\), \(\gamma=1/2\), vanishing initial Squire component,
the zero Squire forcing coefficient \(i\xi\Lambda\), and the exact kinetic
norm identity.  Only then does the OS lower bound embed isometrically into a
complete row, excluding every complete-row polynomial bound required to
cover it.  This does not prove the still-open complete OS--Squire
\(A_2\) direct sum or a fixed-window lower law \(e^{c|\Lambda|}\).

## 7. Local-data no-go that must remain visible

The family

\[
 C_N=
 \begin{pmatrix}
  a&0&0\\
  0&-N&N^2\\
  0&0&-N
 \end{pmatrix},
 \qquad a>0,
 \tag{7.1}
\]

has a constant Riesz projection around \(a\), a uniform local contour
resolvent, and complement spectrum at \(-N\).  Nevertheless, at \(t=N^{-1}\)
its complementary semigroup contains the factor \(N/e\).  Hence local Riesz
convergence, a spectral gap, and memberwise analyticity do not by themselves
give a family-uniform complement bound.  E1--E2 are allowed only because
the present family has the additional compact-Fredholm and uniform
high-frequency structure in (1.2) and Section 4.

## 8. Claim ledger after independent audit

The corrected proof passed an independent adversarial analytic audit.  The
following theorem claims are closed:

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

The following are not changed by favorable finite diagnostics:

```text
certifiedSigmaStarIsRightmost=OPEN
selectedSigmaStarComplementDichotomy=OPEN
uniformHalfPlaneBoundAtBEqualsZero=OPEN
globalRightHalfPlaneNoPollution=OPEN
absoluteUniformComplementDecay=OPEN
explicitHalfPlaneGap=OPEN
explicitViscosityThreshold=OPEN
quantitativeEigenvalueRate=OPEN
movingProfileUniformContour=OPEN
graphDomainKatoTransport=OPEN
movingProfileEvolutionDichotomy=OPEN
inviscidRootUnique=OPEN
inviscidEigenvalueSimple=OPEN
completeOSSquireA2DirectSum=OPEN
fixedWindowExponentialLowerLaw=OPEN
nonlinearNavierStokes=OPEN
Clay=OPEN
```

The moving-profile contour and graph-domain Kato statements are not needed
for E3, but they remain open as separate operator claims.

## 9. Publication gate

R0.73E counts as complete only after all of the following pass:

1. a full proof of E1--E3 and an independent analytic audit;
2. a primary-source literature audit with no priority claim;
3. a reproducible finite complement-resolvent/semigroup diagnostic with
   progress monitoring and an independent recomputation;
4. a formal SVG/PDF/600-dpi PNG figure package;
5. synchronized Chinese/English HTML and PDF;
6. cumulative R0.61--R0.73E recap, homepage, literature and note index;
7. deterministic certificate and release tests;
8. GitHub Pages deployment and live byte/behavior parity checks.
