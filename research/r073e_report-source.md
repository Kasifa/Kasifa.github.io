# R0.73E report source: fixed-half-plane splitting and logarithmic profile transfer

**Date:** 2026-08-30
**Scope:** the periodic heat profile, the physical row
\(\beta=\xi=0\), \(\gamma=1/2\), and the singular limit
\(\varepsilon=|\Lambda|^{-1}\downarrow0\)
**Evidence:** exact operator proof, independent analytic audit, bounded
primary-source literature audit, and a separate reproducible finite diagnostic

## 0. Direct decision

R0.73E closes the complement and fast-time gates left open by R0.73D for one
exact Fourier row.  After the kinetic-space unitary transform, the frozen
family has the structure

\[
 B_\varepsilon=M+K-\varepsilon L,
 \qquad M^*=-M,
 \qquad K\text{ compact},
 \qquad L=-\partial_x^2+\frac14.
 \tag{0.1}
\]

For every fixed \(b>0\) whose boundary line avoids the inviscid spectrum,
there exists \(\varepsilon_b>0\) such that, for every
\(0<\varepsilon<\varepsilon_b\), all spectrum in
\(\operatorname{Re}z\ge b\) is captured by finitely many continued inviscid
clusters.  There is no additional viscous spectrum in that fixed half-plane,
the total Riesz projection and finite spectral block converge in operator norm,
and the extended complementary resolvent is uniformly bounded.  No constant
is uniform as \(b\downarrow0\).

Let

\[
 a=\max_{z\in\sigma(B_0)}\operatorname{Re}z.
 \tag{0.2}
\]

The certified R0.73C eigenvalue gives
\(a\ge\sigma_*>0.17035\).  Projecting the complete top cluster, rather than
only the selected \(\sigma_*\), yields a family-uniform relative exponential
dichotomy.  The exact heat-profile drift is a bounded perturbation of size
\(O(\varepsilon\theta)\) in fast time.  A fixed-generator Volterra argument
therefore transfers a viscous top eigenmode through every interval

\[
 T_\varepsilon=M\log(1/\varepsilon),
 \qquad M>0\text{ fixed}.
 \tag{0.3}
\]

Consequently, for every fixed observation window \(d_*>0\) and every
\(p>0\),

\[
 \boxed{
 \lim_{|\Lambda|\to\infty}
 \frac{G_{1/2}(\Lambda;d_*)}{|\Lambda|^p}=\infty.}
 \tag{0.4}
\]

This excludes every fixed-degree polynomial upper bound that must cover this
row.  It does not give one viscosity threshold for the entire open right
half-plane, absolute decay of the unshifted complement, a moving-profile
spectral dichotomy, a fixed-window law \(e^{c|\Lambda|}\), the complete
OS--Squire \(A_2\) direct sum, a nonlinear estimate, or a Clay-problem
conclusion.

## 1. Exact row and physical norm

The heat-decaying shear is

\[
 W(d,x)=-\frac12e^{-d}\sin x+\frac14e^{-4d}\sin2x,
 \qquad W_d=W_{xx}.
 \tag{1.1}
\]

On the two-dimensional row

\[
 \beta=\xi=0,
 \qquad \gamma=\frac12,
 \qquad \mu=\gamma^2=\frac14,
 \tag{1.2}
\]

put

\[
 L=-\partial_x^2+\frac14,
 \qquad
 A(d)=-\frac i2\left(M_{W(d)}+M_{W_{xx}(d)}L^{-1}\right).
 \tag{1.3}
\]

The physical kinetic vorticity space \(X=X_{1/4}\) has norm

\[
 \|q\|_X^2=4\langle L^{-1}q,q\rangle_{L^2}.
 \tag{1.4}
\]

The map

\[
 U=2L^{-1/2}:X\longrightarrow H=L^2(\mathbb T_{2\pi})
 \tag{1.5}
\]

is unitary.  In fast time \(\theta=|\Lambda|d\), with
\(\varepsilon=|\Lambda|^{-1}\), the positive-sign frozen generator becomes
the operator in (0.1), where

\[
 M=-\frac i2M_{W(0)}
 \tag{1.6}
\]

is bounded and skew-adjoint, and

\[
 K=-\frac i2\left(
 L^{-1/2}[M_{W(0)},L^{1/2}]
 +L^{-1/2}M_{W_{xx}(0)}L^{-1/2}
 \right)
 \tag{1.7}
\]

is compact.  The singular domain jump remains visible:

\[
 D(B_\varepsilon)=H^2_{\rm per}\quad(\varepsilon>0),
 \qquad
 B_0=M+K\in\mathcal B(H).
 \tag{1.8}
\]

No bounded-operator norm perturbation theorem is applied to
\(-\varepsilon L\).

## 2. Fixed-positive-half-plane theorem

Fix \(b>0\) such that

\[
 \sigma(B_0)\cap\{\operatorname{Re}z=b\}=\varnothing.
 \tag{2.1}
\]

The spectrum of the bounded inviscid operator is compact.  Since \(B_0\) is
a compact perturbation of skew-adjoint multiplication, its spectrum in the
open right half-plane consists of isolated eigenvalues of finite algebraic
multiplicity, with no accumulation away from the imaginary axis.  Therefore

\[
 \Sigma_b=\sigma(B_0)\cap\{\operatorname{Re}z>b\}
 \tag{2.2}
\]

is finite.  Surround these points by finitely many disjoint fixed contours
\(\Gamma_{b,j}\subset\{\operatorname{Re}z>b\}\).

### Theorem 2.1

For all sufficiently small positive \(\varepsilon\):

1. every \(\Gamma_{b,j}\) lies in \(\rho(B_\varepsilon)\) with a common
   contour-resolvent bound;
2. the total Riesz projections

   \[
    \Pi_{\varepsilon,b}
    =\frac1{2\pi i}\sum_j\int_{\Gamma_{b,j}}
      (z-B_\varepsilon)^{-1}\,dz
   \]

   obey

   \[
    \|\Pi_{\varepsilon,b}-\Pi_{0,b}\|\longrightarrow0;
    \tag{2.3}
   \]

3. all viscous spectrum in \(\operatorname{Re}z\ge b\) lies inside the
   selected contours;
4. if \(Q_{\varepsilon,b}=I-\Pi_{\varepsilon,b}\) and
   \(C_{\varepsilon,b}\) is the part of \(B_\varepsilon\) in
   \(Q_{\varepsilon,b}H\), then

   \[
    \sup_{0<\varepsilon<\varepsilon_b}
    \sup_{\operatorname{Re}z\ge b}
    \|(z-C_{\varepsilon,b})^{-1}Q_{\varepsilon,b}\|<\infty;
    \tag{2.4}
   \]

5. the finite blocks converge:

   \[
    \|B_\varepsilon\Pi_{\varepsilon,b}
      -B_0\Pi_{0,b}\|\longrightarrow0.
    \tag{2.5}
   \]

At a projected eigenvalue, (2.4) denotes the analytic complement-part
resolvent.  The full resolvent does not exist there.  Every constant in the
theorem may depend on the fixed \(b\).

## 3. The noncompact resolvent splice

The local R0.73D contour theorem cannot by itself prove Theorem 2.1.  Put

\[
 H_\varepsilon=M-\varepsilon L,
 \qquad R_\varepsilon(z)=(z-H_\varepsilon)^{-1}.
 \tag{3.1}
\]

For \(z=x+i\tau\), \(x>0\), dissipativity gives

\[
 \|R_\varepsilon(z)\|\le x^{-1}.
 \tag{3.2}
\]

The exact factorization

\[
 z-H_\varepsilon=(z+\varepsilon L)
 \left[I-(z+\varepsilon L)^{-1}M\right]
 \tag{3.3}
\]

and positivity of \(L\) give

\[
 \|R_\varepsilon(x+i\tau)\|
 \le\frac1{|\tau|-\|M\|},
 \qquad |\tau|>\|M\|.
 \tag{3.4}
\]

A second Neumann factor for \(K\) yields

\[
 \|(z-B_\varepsilon)^{-1}\|
 \le\frac2{|\tau|-\|M\|}
 \tag{3.5}
\]

when \(|\tau|\) exceeds a fixed bound.  Large positive real part follows
from (3.2).  Only a fixed compact rectangle remains, where strong and
adjoint-strong base-resolvent convergence, compactness of \(K\), and analytic
Fredholm theory apply uniformly.

This high-frequency step is analytic and infinite-dimensional.  No Fourier
truncation replaces it.

## 4. Projection norm and reduced resolvent

The full and base resolvents obey

\[
 G_\varepsilon-R_\varepsilon
 =G_\varepsilon K R_\varepsilon.
 \tag{4.1}
\]

On every fixed contour,
\(G_\varepsilon K=F_\varepsilon^{-1}R_\varepsilon K\) converges in norm,
and the compact-sandwich difference splits as

\[
 G_\varepsilon K R_\varepsilon-G_0KR_0
 =(G_\varepsilon K-G_0K)R_\varepsilon
 +G_0K(R_\varepsilon-R_0).
 \tag{4.2}
\]

The first term uses the uniform base-resolvent bound; the second uses
adjoint-strong convergence against the compact operator \(G_0K\).  The base
resolvent is analytic inside every right-half-plane cluster contour, so its
contour integral, and the contour integral of \(zR_\varepsilon(z)\), vanish.
Equations (2.3) and (2.5) follow.

The Riesz splitting satisfies

\[
 H=\Pi_{\varepsilon,b}H\oplus Q_{\varepsilon,b}H,
 \qquad
 Q_{\varepsilon,b}D(B_\varepsilon)\subset D(B_\varepsilon),
 \qquad
 [B_\varepsilon,Q_{\varepsilon,b}]=0
 \quad\text{on }D(B_\varepsilon).
 \tag{4.3}
\]

The complement-part resolvent agrees with
\(G_\varepsilon Q_{\varepsilon,b}\) off the finite block and extends
analytically across it.  Its boundary values are uniformly bounded, and the
maximum principle on the finitely many disks proves (2.4).

## 5. The complete top cluster

Define the spectral abscissa

\[
 a=\max_{z\in\sigma(B_0)}\operatorname{Re}z.
 \tag{5.1}
\]

R0.73C--D supply

\[
 \sigma_*\in(0.17035,0.17050)\cap\sigma_p(B_0),
 \qquad a\ge\sigma_*>0.17035.
 \tag{5.2}
\]

The top set

\[
 \Sigma_{\rm top}
 =\{z\in\sigma(B_0):\operatorname{Re}z=a\}
 \tag{5.3}
\]

is nonempty and finite.  It is essential to project all of it.  The certified
\(\sigma_*\) is not known to be rightmost.

Let \(\Pi_0^{\rm top}\) be the total top Riesz projection.  The complementary
spectrum is compact and cannot approach the isolated finite top set, so its
spectral abscissa \(\beta_{\rm top}\) satisfies

\[
 \beta_{\rm top}<a.
 \tag{5.4}
\]

Choose

\[
 \max\{\beta_{\rm top},0\}<b<c<a.
 \tag{5.5}
\]

Theorem 2.1 then selects exactly the top cluster.  Its viscous continuation
\(\Pi_\varepsilon^{\rm top}\) converges in norm, and one can choose unit
eigenvectors

\[
 B_\varepsilon v_\varepsilon
 =\lambda_\varepsilon v_\varepsilon,
 \qquad
 \operatorname{Re}\lambda_\varepsilon\longrightarrow a.
 \tag{5.6}
\]

No simplicity, common eigenvector, or explicit gap is asserted.

## 6. Uniform relative dichotomy

Let \(C_\varepsilon\) be the part of \(B_\varepsilon\) on the top
complement.  The base semigroup is contractive, and bounded perturbation by
\(K\) gives the common crude estimate

\[
 \|e^{tB_\varepsilon}\|\le e^{\|K\|t}.
 \tag{6.1}
\]

Theorem 2.1 and the high-frequency estimate give

\[
 \|(b+i\tau-C_\varepsilon)^{-1}\|
 \le\frac{C}{1+|\tau|}.
 \tag{6.2}
\]

For every \(\varepsilon>0\), \(B_\varepsilon\) generates an analytic
semigroup.  Start the inverse-Laplace formula on a common line
\(\operatorname{Re}z=\omega>\|K\|\), move it across the strip to
\(\operatorname{Re}z=b\), and use the high-frequency bound to remove the
horizontal sides.  Integration by parts gives the exact identity

\[
 e^{tC_\varepsilon}
 =\frac{e^{bt}}{2\pi t}
 \int_{\mathbb R}e^{i\tau t}
 (b+i\tau-C_\varepsilon)^{-2}\,d\tau,
 \qquad t>0.
 \tag{6.3}
\]

The squared resolvent is uniformly integrable.  Combining (6.3) for
\(t\ge1\) with (6.1) for short time proves

\[
 \|e^{tB_\varepsilon}Q_\varepsilon^{\rm top}\|
 \le C_b e^{bt},
 \qquad t\ge0.
 \tag{6.4}
\]

Fixed top contours in \(\operatorname{Re}z>c\) give the inverse group on the
finite block:

\[
 \|e^{-tB_\varepsilon}\Pi_\varepsilon^{\rm top}\|
 \le C_c e^{-ct},
 \qquad t\ge0.
 \tag{6.5}
\]

After any shift between \(b\) and \(c\), (6.4)--(6.5) form a uniform
relative exponential dichotomy.  The unshifted complement need not decay.

For every fixed \(\delta>0\), the same splitting yields

\[
 \|e^{tB_\varepsilon}\|
 \le C_\delta e^{(a+\delta)t},
 \qquad t\ge0,
 \tag{6.6}
\]

uniformly for sufficiently small \(\varepsilon\).

## 7. Exact heat-profile drift

On \(H\), define

\[
 \widetilde A(d)=UA(d)U^{-1}.
 \tag{7.1}
\]

For \(\Delta W=W(d)-W(0)\), the Fourier commutator estimate gives

\[
 \|\widetilde A(d)-\widetilde A(0)\|
 \le\frac12\left(
 \|\Delta W\|_\infty
 +2\sum_k|k||\widehat{\Delta W}(k)|
 +4\|\Delta W_{xx}\|_\infty\right).
 \tag{7.2}
\]

The explicit profile obeys

\[
 \|\Delta W\|_\infty\le\frac32d,
 \qquad
 \sum_k|k||\widehat{\Delta W}(k)|\le\frac52d,
 \qquad
 \|\Delta W_{xx}\|_\infty\le\frac92d.
 \tag{7.3}
\]

Therefore

\[
 \boxed{
 \|\widetilde A(d)-\widetilde A(0)\|
 \le\frac{49}{4}d.}
 \tag{7.4}
\]

In fast time the exact moving generator is

\[
 B_\varepsilon+E_\varepsilon(\theta),
 \qquad
 E_\varepsilon(\theta)
 =\widetilde A(\varepsilon\theta)-\widetilde A(0),
 \qquad
 \|E_\varepsilon(\theta)\|
 \le\frac{49}{4}\varepsilon\theta.
 \tag{7.5}
\]

The unbounded term \(-\varepsilon L\) stays inside the frozen generator; it
is never treated as bounded forcing.

## 8. Logarithmic Volterra transfer

Fix \(M>0\), set

\[
 T_\varepsilon=M\log(1/\varepsilon),
 \qquad \delta=\frac1{4M},
 \tag{8.1}
\]

and start the moving equation from the top viscous eigenvector in (5.6):

\[
 q'(t)=[B_\varepsilon+E_\varepsilon(t)]q(t),
 \qquad q(0)=v_\varepsilon.
 \tag{8.2}
\]

The bounded-perturbation theorem gives a unique evolution family.  Duhamel's
formula, (6.6), and weighted Gronwall yield

\[
 \|q(t)\|
 \le C_\delta e^{(a+\delta)t}
 \exp\left(\frac12C_\delta C_A\varepsilon t^2\right),
 \qquad C_A=\frac{49}{4}.
 \tag{8.3}
\]

The difference from the frozen eigenmode satisfies

\[
 \|q(t)-e^{\lambda_\varepsilon t}v_\varepsilon\|
 \le\frac12C_\delta^2C_A\varepsilon t^2
 \exp\left((a+\delta)t
 +\frac12C_\delta C_A\varepsilon t^2\right).
 \tag{8.4}
\]

Let
\(\eta_\varepsilon=|\operatorname{Re}\lambda_\varepsilon-a|\to0\).
At \(T_\varepsilon\), the error divided by the frozen eigenmode is bounded
by

\[
 C\varepsilon T_\varepsilon^2
 \exp\left((\delta+\eta_\varepsilon)T_\varepsilon
 +C\varepsilon T_\varepsilon^2\right).
 \tag{8.5}
\]

For each fixed \(M\), eventually \(M\eta_\varepsilon<1/4\).  Since
\(M\delta=1/4\), the right side is
\(O_M(\varepsilon^{1/2}\log^2(1/\varepsilon))\).  Hence

\[
 \|q(T_\varepsilon)\|
 \ge\frac12e^{\operatorname{Re}\lambda_\varepsilon T_\varepsilon}
 \tag{8.6}
\]

for all sufficiently small \(\varepsilon\), with the exact quantifier order

\[
 \forall M>0\ \exists\varepsilon_M>0\ \forall
 0<\varepsilon<\varepsilon_M.
 \tag{8.7}
\]

Equivalently,

\[
 \liminf_{\varepsilon\downarrow0}
 \frac{\log\|U_\varepsilon(T_\varepsilon,0)\|}
      {\log(1/\varepsilon)}
 \ge Ma\ge M\sigma_*>0.17035M.
 \tag{8.8}
\]

No convergence rate for \(\lambda_\varepsilon\) is used.

## 9. Physical-time and complete-row consequence

The physical time corresponding to (8.1) is

\[
 d_\Lambda=M\frac{\log|\Lambda|}{|\Lambda|}\longrightarrow0.
 \tag{9.1}
\]

The exact row gain is

\[
 G_{1/2}(\Lambda;d_*)
 =\sup_{0\le d\le d_*}
 \|U_{1/2,\Lambda}(d,0)\|_{\mathcal K_{1/4}\to\mathcal K_{1/4}}.
 \tag{9.2}
\]

For any fixed \(d_*>0\), eventually \(d_\Lambda<d_*\).  Given \(p>0\),
choose \(M>p/0.17035\).  Equations (8.8)--(9.2) prove (0.4).  Complex
conjugation gives the same conclusion for both signs of \(\Lambda\), because
\(W\) and \(L\) are real.

The exact Orr--Sommerfeld--Squire system on (1.2) has Squire forcing
coefficient \(i\xi\Lambda=0\).  Initial Squire vorticity \(\eta(0)=0\)
therefore remains zero.  The kinetic identity is

\[
 \|u\|_2^2
 =\mu^{-1}\left(\|L^{-1/2}q\|_2^2+\|\eta\|_2^2\right).
 \tag{9.3}
\]

The map (1.5) is exactly the OS part of this norm.  The lower bound therefore
embeds isometrically into a complete Fourier row.  Any complete-row
polynomial upper bound that is required to cover all rows must dominate this
one and is excluded.

This embedding does not prove a uniform estimate across all rows or close the
complete OS--Squire \(A_2\) direct sum.

## 10. Why local R0.73D data were insufficient

The matrices

\[
 D_N=
 \begin{pmatrix}
 a&0&0\\
 0&-N&N^2\\
 0&0&-N
 \end{pmatrix}
 \tag{10.1}
\]

have a constant Riesz projection around \(a\), a uniform local contour
resolvent, and complement spectrum \(\{-N\}\).  Yet at \(t=N^{-1}\),

\[
 e^{tD_N}|_{\rm complement}
 =e^{-Nt}\begin{pmatrix}1&N^2t\\0&1\end{pmatrix}
 \tag{10.2}
\]

has norm at least \(N/e\).  Local Riesz convergence, a spectral gap, and
memberwise analyticity do not imply a family-uniform complementary semigroup
bound.  Theorem 2.1 succeeds only because (0.1) supplies the additional
high-frequency and compact-Fredholm structure.

## 11. Finite diagnostic

The reproducible finite experiment uses kinetic-isometric dense Fourier
compressions on modes \(-N,\ldots,N\), with
\(N=24,48,96\), and viscosities \(10^{-2},\ldots,10^{-6}\).  It asks what
remains after removing only the selected leading finite cluster.

At \(N=96\), \(\varepsilon=10^{-6}\), the leading finite eigenvalue is

\[
 \lambda_{\rm lead}=0.170406506600201,
 \tag{11.1}
\]

while the finite complement still contains

\[
 0.040536174080661\pm0.176136754131770i.
 \tag{11.2}
\]

Thus the finite complement obtained after removing the rank-one leading
cluster is not stable.  This is why the analytic theorem selects the complete
top cluster and proves a relative, not absolute, dichotomy.

For the same largest-cutoff, smallest-viscosity case, the sampled
complement-resolvent peaks are:

| \(\operatorname{Re}z\) | maximum sampled/refined norm | peak \(|\operatorname{Im}z|\) |
|---:|---:|---:|
| 0.05 | 378.4782 | 0.1758830 |
| 0.08 | 56.2998 | 0.1730535 |
| 0.12 | 21.2573 | 0.1677321 |

The intrinsic finite complementary semigroup has

\[
 \|e^{200B_{\varepsilon,Q}}\|_2=1.68367\times10^4,
 \tag{11.3}
\]

and a peak normalized transient of 5.07968 on the sampled grid.  Its fitted
late-time slope, 0.0405522, is close to the finite spectral abscissa.

The fixed inviscid complement illustrates long-time leakage:

\[
 \|P_\varepsilon-P_0\|_2=3.09050\times10^{-4},
 \qquad
 \|e^{200B_\varepsilon}Q_0\|_2\approx1.94966\times10^{11}.
 \tag{11.4}
\]

All 15 primary rows and the independently coded contour, inverse-resolvent,
and semigroup recomputations pass.  The maximum primary algebraic residual is
\(6.2430\times10^{-14}\).  The largest independent resolvent relative error
is below \(1.71\times10^{-13}\); the intrinsic and moving-complement
semigroup sentinels are reproduced within \(2.38\times10^{-13}\), while the
fixed-complement endpoint comparisons are reproduced within
\(1.74\times10^{-11}\).

These are IEEE-754 binary64 finite observations.  They do not prove an
additional continuum eigenpair, a continuum resolvent bound, a continuous-
time semigroup estimate, or the logarithmic transfer theorem.

## 12. Literature boundary

The primary-source audit records the following distinctions.

- Shvydkoy--Friedlander give the broad inviscid-to-viscous unstable-spectrum
  precedent, including spectral-subspace and multiplicity persistence.  Their
  theorem does not explicitly label the projection convergence as operator
  norm; R0.73E proves its model-specific norm statement directly.
- Kato supplies the general separated-spectrum framework once a suitable
  convergence hypothesis is verified.  The singular domain jump here makes
  that verification substantive.
- Engel--Nagel, Gearhart, and Prüss explain why memberwise analytic semigroups
  and a local spectral gap do not supply a family-uniform prefactor.  R0.73E
  proves the whole-line bound and performs the Bromwich argument explicitly.
- Li--Lin connect oscillatory shears, frozen Orr--Sommerfeld instability, and
  slow viscous drift, but do not supply this exact moving-profile evolution
  lower bound.
- Grenier--Nguyen obtain genuine uniform semigroup estimates in a different
  no-slip half-space setting and different norms.
- Kato's and Schmid's adiabatic theories and the
  Latushkin--Schnaubelt/Popescu
  dichotomy literature require regularity, domain, gap, or pre-existing
  evolution-family hypotheses that are not imported here.

No originality or priority claim is made.  Full DOI links and source-level
scope checks are in `research/r073e_literature_audit.md`.

## 13. What this section changes

R0.73D proved static persistence of one certified inviscid cluster but left
the rest of the right half-plane and the complementary semigroup uncontrolled.
R0.73E replaces that conditional gate with the exact chain

```text
every fixed positive half-plane is spectrally complete
+ total Riesz projection converges in norm
+ reduced half-plane resolvent is uniform
+ complete top cluster has a relative dichotomy
+ bounded exact profile drift transfers a top mode through M log(1/epsilon)
+ every fixed-degree polynomial row upper bound is excluded.
```

This is a linear-instability theorem for one exact row.  Its direct value for
the Clay problem remains limited because no nonlinear
frequency interaction, energy closure, continuation criterion, or blow-up
construction has been obtained.

## 14. Exact final boundary

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

No finite Fourier calculation, frozen one-row theorem, or super-polynomial
linear gain is presented as a solution of three-dimensional Navier--Stokes
regularity.
