# R0.73P proof: weak \(L^2\) stability, a critical \(H^{1/2}\) tube, and frequency-localized strong continuation

**Status:** **FORMAL PASS after independent analytic readback**; the main
critical theorem is a classical corollary of published robustness theory
plus the finite actions of R0.73O

**Depends on:** the R0.73O global-orbit decay ladder; Leray--Hopf existence
and relative energy; periodic Fujita--Kato local theory; quantitative
\(\dot H^{1/2}\) robustness; Serrin regularity

## 1. Setting and theorem package

On the standard three-torus \([0,2\pi]^3\), equip Fourier norms with the
normalized Haar measure \((2\pi)^{-3}dx\), and let

\[
 \partial_tu+Au+B(u,u)=0,
 \qquad A=-P\Delta,
 \tag{1.1}
\]

where

\[
 \widehat z_k=\int_{\mathbb T^3}z(x)e^{-ik\cdot x}(2\pi)^{-3}dx,
 \qquad
 |z|_s^2=\sum_{k\in\mathbb Z^3\setminus\{0\}}
 |k|^{2s}|\widehat z_k|^2.
\]

and suppose

\[
 u\in C([0,\infty);H^3_{\sigma,0})
 \cap L^2_{\rm loc}([0,\infty);H^4_{\sigma,0})
 \tag{1.2}
\]

is an a priori global strong solution.  Write

\[
 |z|_s=\|A^{s/2}z\|_2.
 \tag{1.3}
\]

There are finite orbit actions

\[
 \mathcal A_c[u]=\int_0^\infty |u(t)|_1^4\,dt<\infty,
 \qquad
 \mathcal L[u]=\int_0^\infty\|\nabla u(t)\|_\infty\,dt<\infty.
 \tag{1.4}
\]

The theorem package proved below has four parts.

1. Every Leray--Hopf comparison solution is globally stable relative to
   \(u\) in \(L^2\), with no smallness assumption.
2. There is a positive \(H^{1/2}\) radius, uniform over every starting time
   along \(u\), that gives a unique global critical solution and exponential
   critical synchronization.
3. If the critical perturbation datum belongs to \(H^3\), the comparison
   solution is global in \(H^3\).
4. A Fourier cutoff \(|k|\le N\) converts the critical radius into an
   \(L^2\) sufficient threshold proportional to \(N^{-1/2}\).

## 2. Why both orbit actions are finite

The energy equality gives

\[
 {1\over2}\|u(t)\|_2^2+\int_0^t|u(s)|_1^2\,ds
 ={1\over2}\|u(0)\|_2^2.
 \tag{2.1}
\]

R0.73O proves that, after a finite time, \(|u(t)|_3\) and all lower
Sobolev norms decay exponentially.  On every finite interval, (1.2) makes
\(|u|_1\) continuous and bounded.  Consequently

\[
 \int_0^\infty |u|_1^4
 \le \left(\sup_{t\ge0}|u(t)|_1^2\right)
     \int_0^\infty |u(t)|_1^2\,dt<\infty.
 \tag{2.2}
\]

On a finite interval, \(H^3\hookrightarrow W^{1,\infty}\) gives integrability
of \(\|\nabla u\|_\infty\).  On the infinite tail, the high-order
exponential decay proved in R0.73O gives

\[
 \int_T^\infty\|\nabla u(t)\|_\infty\,dt
 \le C\int_T^\infty |u(t)|_3\,dt<\infty.
 \tag{2.3}
\]

This proves (1.4).

## 3. All-time relative \(L^2\) stability for every Leray--Hopf solution

Fix \(t_0\ge0\).  Let \(v\) be any Leray--Hopf solution with datum
\(v(t_0)\in L^2_{\sigma,0}\), and set \(w=v-u\).  The standard
weak--strong relative-energy calculation gives

\[
 {1\over2}E'(t)+D(t)
 \le a(t)E(t),
 \qquad
 E=\|w\|_2^2,\quad D=|w|_1^2,\quad
 a=\|\nabla u\|_\infty,
 \tag{3.1}
\]

in integrated form.  This is legitimate with \(v\) weak because \(u\) is
strong; it is the same relative-energy mechanism used in weak--strong
uniqueness, but the two initial data need not agree.

Let

\[
 A_{t_0}(t)=\int_{t_0}^t a(s)\,ds.
 \tag{3.2}
\]

Multiplying (3.1) by \(e^{-2A_{t_0}(t)}\) yields

\[
 e^{-2A_{t_0}(t)}E(t)
 +2\int_{t_0}^t e^{-2A_{t_0}(s)}D(s)\,ds
 \le E(t_0).
 \tag{3.3}
\]

In particular,

\[
 \sup_{t\ge t_0}\|w(t)\|_2
 \le e^{\mathcal L[u]}\|w(t_0)\|_2,
 \tag{3.4}
\]

and

\[
 \int_{t_0}^\infty |w(t)|_1^2\,dt
 \le {1\over2}e^{2\mathcal L[u]}\|w(t_0)\|_2^2.
 \tag{3.5}
\]

Since \(D\ge E\) by Poincare, (3.1) also gives the sharper decay formula

\[
 \boxed{
 \|v(t)-u(t)\|_2
 \le
 e^{\int_{t_0}^t\|\nabla u(s)\|_\infty ds}
 e^{-(t-t_0)}\|v(t_0)-u(t_0)\|_2.}
 \tag{3.6}
\]

This theorem says nothing about regularity of \(v\) before its eventual
regular time.  In particular it cannot be used to test (1.1) with
\(A^{1/2}v\) at the starting time when only \(L^2\) data are known.

## 4. The finite-time published critical robustness estimate

Burczak--Zaj\k{a}czkowski prove quantitative robustness in a periodic cube
for \(\dot H^\alpha\), \(\alpha\in[1/2,1]\).  At \(\alpha=1/2\), equal
forcing, and viscosity one, their Theorem 1 has the following consequence.
Here is the exact normalization used in this release.  Fix positive margins
\(\bar\nu,\varepsilon_1,\varepsilon_2\) with

\[
 \bar\nu+\varepsilon_1+\varepsilon_2<1.
 \tag{4.1}
\]

Let \(C_S(\beta)\) denote the paper's Sobolev--Poincare constant on
\(Q_{2\pi}\).  Specializing the constants printed immediately before its
Theorem 1 to \(L=2\pi\) and \(\alpha=1/2\) gives

\[
 \begin{aligned}
 K_2^c&=\sqrt2\,C_S(1/2)C_S(1)C_S(0),\\
 K_3^c&=\varepsilon_1^{-3}{27\over128}(2\pi)^{-12}
 C_S(1/2)^4C_S(1)^4
 \left[1+C_S(0)(2\pi)^{-3/2}\right]^4,\\
 K_4^c&=(4\varepsilon_2)^{-1}.
 \end{aligned}
 \tag{4.2}
\]

The paper's Fourier coefficient norm \(|\cdot|_{s,2\pi}\) is exactly our
normalized-Haar Stokes norm \(|\cdot|_s\).  Its Lebesgue gradient norm is
unnormalized, however, so its identity (1.1) yields

\[
 \|\nabla z\|_{L^2(dx)}=(2\pi)^{3/2}|z|_1.
 \tag{4.3}
\]

Consequently put

\[
 K_3'=(2\pi)^6K_3^c.
 \tag{4.4}
\]

At equal forcing and viscosity one, Theorem 1 says that if \(u\) is critical
strong on \([t_0,T]\) and

\[
 |w(t_0)|_{1/2}^2
 \exp\!\left(
 K_3^c\int_{t_0}^{T}\|\nabla u(t)\|_{L^2(dx)}^4\,dt
 \right)
 <\left({\bar\nu\over K_2^c}\right)^2,
 \tag{4.5}
\]

then every Leray--Hopf solution from the perturbed datum is critical strong
on \([t_0,T]\), with the quantitative estimate

\[
 \sup_{t_0\le t\le T}|w(t)|_{1/2}^2
 +(1-\bar\nu-\varepsilon_1-\varepsilon_2)
 \int_{t_0}^{T}|w(t)|_{3/2}^2dt
 \le\left({\bar\nu\over K_2^c}\right)^2.
 \tag{4.6}
\]

Critical uniqueness follows separately from the paper's local uniqueness
theorem, equivalently from Serrin weak--strong uniqueness.  The robustness
theorem is stated from time zero; applying it to the time-translated
autonomous equation gives the form above for every \(t_0\).  The
force-difference term carrying \(K_4^c\) vanishes here because both
equations are unforced.

Define

\[
 R_{\rm pub}[u]
 ={\bar\nu\over K_2^c}
 \exp\!\left(-{K_3'\over2}\mathcal A_c[u]\right)>0.
 \tag{4.7}
\]

Then (4.5) holds on every finite interval \([t_0,T]\) whenever
\(|w(t_0)|_{1/2}<R_{\rm pub}[u]\).  Applying the theorem for arbitrary
finite \(T\) and using critical uniqueness patches the finite solutions into
a global one:

\[
 v\in C([t_0,\infty);H^{1/2}_{\sigma,0})
 \cap L^2_{\rm loc}([t_0,\infty);H^{3/2}_{\sigma,0}).
 \tag{4.8}
\]

The same radius works for every \(t_0\) because the tail action never
exceeds \(\mathcal A_c[u]\).

## 5. Retaining Poincare damping: exponential critical synchronization

The finite-time robustness proof is based on the critical difference
inequality

\[
 X'(t)+c_0Y(t)
 \le C_0|u(t)|_1^4X(t)+C_1X(t)Y(t),
 \quad
 X=|w|_{1/2}^2,\quad Y=|w|_{3/2}^2.
 \tag{5.1}
\]

This is also the explicit inequality in the proof of
Mar\'in-Rubio--Robinson--Sadowski Theorem 3, up to fixed norm constants.
Choose \(\eta>0\) so that \(C_1\eta\le c_0/2\).  On an interval where
\(X\le\eta\),

\[
 X'+{c_0\over2}Y\le C_0|u|_1^4X.
 \tag{5.2}
\]

Since \(Y\ge X\), Gronwall gives

\[
 X(t)
 \le X(t_0)
 \exp\!\left(
 C_0\int_{t_0}^t|u(s)|_1^4\,ds
 -{c_0\over2}(t-t_0)
 \right).
 \tag{5.3}
\]

If

\[
 X(t_0)<{\eta\over2}e^{-C_0\mathcal A_c[u]},
 \tag{5.4}
\]

the usual first-exit bootstrap keeps \(X<\eta\) for all time.  Define the
released critical radius by

\[
 R_{1/2}[u]
 :=\min\left\{
 R_{\rm pub}[u],
 \sqrt{\eta/2}\,e^{-C_0\mathcal A_c[u]/2}
 \right\}>0.
 \tag{5.5}
\]

Then every datum inside this radius has the global critical solution (4.8)
and

\[
 \boxed{
 |v(t)-u(t)|_{1/2}
 \le e^{C_0\mathcal A_c[u]/2}
 e^{-c_0(t-t_0)/4}|v(t_0)-u(t_0)|_{1/2}.}
 \tag{5.6}
\]

Only the existence of positive computable constants is used later.  No
numerical value is assigned without fixing every Sobolev constant and norm
normalization.

## 6. Propagation from a critical solution to a global \(H^3\) solution

Suppose now that the perturbed datum belongs to \(H^3\).  Standard local
\(H^3\) theory gives a maximal local \(H^3\) solution.  It coincides with
the global critical solution by weak--strong uniqueness.

The critical class satisfies

\[
 L^\infty_tH^{1/2}_x\cap L^2_tH^{3/2}_x
 \hookrightarrow L^4_tH^1_x
 \hookrightarrow L^4_tL^6_x,
 \tag{6.1}
\]

which is the Serrin pair \((p,q)=(4,6)\).  Hence no finite endpoint of the
local \(H^3\) solution can be singular.  Equivalently, the regularity upgrade
in Mar\'in-Rubio--Robinson--Sadowski Theorem 2 first yields
\(L^\infty H^1\cap L^2H^2\), after which standard parabolic bootstrapping
propagates the initial \(H^3\) regularity on every finite interval.
Therefore

\[
 v\in C([t_0,\infty);H^3_{\sigma,0})
 \cap L^2_{\rm loc}([t_0,\infty);H^4_{\sigma,0}).
 \tag{6.2}
\]

## 7. Fourier cutoff: the \(N^{-1/2}\) gate

Let \(P_{\le N}\) be the orthogonal Fourier projector onto
\(0<|k|\le N\), let \(Q_{>N}=I-P_{\le N}\), and let \(R_3[u]=R_A[u]\) denote
the homogeneous Stokes \(H^3\) stability radius constructed in R0.73O.

Assume

\[
 \operatorname{supp}\widehat w_0\subset\{k\in\mathbb Z^3:0<|k|\le N\}.
 \tag{7.1}
\]

Then Parseval gives

\[
 |w_0|_{1/2}^2
 =\sum_{0<|k|\le N}|k||\widehat w_0(k)|^2
 \le N\sum_{0<|k|\le N}|\widehat w_0(k)|^2
 =N\|w_0\|_2^2.
 \tag{7.2}
\]

Thus

\[
 \boxed{
 \|w_0\|_2<R_{1/2}[u]N^{-1/2}}
 \tag{7.3}
\]

implies the global \(H^3\) continuation (6.2) and the critical
synchronization (5.6).  The direct \(H^3\) tube would use

\[
 |w_0|_3\le N^3\|w_0\|_2
 \tag{7.4}
\]

and therefore only the sufficient threshold

\[
 \|w_0\|_2<R_3[u]N^{-3}.
 \tag{7.5}
\]

The critical route changes the high-frequency exponent by \(5/2\).

For a normalized divergence-free single Fourier mode \(\phi_N\),

\[
 \|\phi_N\|_2=1,
 \qquad
 |\phi_N|_s=N^s.
 \tag{7.6}
\]

At \(w_N=rN^{-1/2}\phi_N\),

\[
 \|w_N\|_2=rN^{-1/2}\to0,
 \qquad
 |w_N|_{1/2}=r,
 \qquad
 |w_N|_3=rN^{5/2}\to\infty.
 \tag{7.7}
\]

This proves that the exponent in (7.2) is attained.  It does not show that
any Navier--Stokes solution at a larger amplitude is singular or unstable.

## 8. Mixed higher-norm and tail gates

Logarithmic convexity of homogeneous Sobolev norms gives, for
\(s>1/2\),

\[
 |w_0|_{1/2}
 \le \|w_0\|_2^{1-1/(2s)}|w_0|_s^{1/(2s)}.
 \tag{8.1}
\]

If \(|w_0|_s\le M\), the sufficient condition

\[
 \boxed{
 \|w_0\|_2
 <R_{1/2}[u]^{\frac{2s}{2s-1}}
 M^{-\frac1{2s-1}}}
 \tag{8.2}
\]

places the datum in the critical tube.  For \(s=3\), this is

\[
 \|w_0\|_2<R_{1/2}[u]^{6/5}M^{-1/5}.
 \tag{8.3}
\]

For a low/high split,

\[
 |w_0|_{1/2}^2
 \le N\|P_{\le N}w_0\|_2^2
 +|Q_{>N}w_0|_{1/2}^2
 \le N\|w_0\|_2^2+|Q_{>N}w_0|_{1/2}^2.
 \tag{8.4}
\]

Hence

\[
 N\|w_0\|_2^2+|Q_{>N}w_0|_{1/2}^2<R_{1/2}[u]^2
 \tag{8.5}
\]

is another auditable sufficient gate.  A lower-frequency bound alone gives
no such estimate; an upper cutoff, a critical tail, or a higher-norm
envelope is essential to this method.

## 9. Exact obstruction and exact non-obstruction

There is no constant \(C\) such that

\[
 |z|_{1/2}\le C\|z\|_2
 \tag{9.1}
\]

for all smooth periodic divergence-free fields.  Equation (7.6) makes the
ratio equal to \(N^{1/2}\).  Therefore the critical robustness theorem
cannot, by norm transfer alone, produce a frequency-independent \(L^2\)
radius.

This is a **methodological no-go**, not a dynamical counterexample.  The
single modes used to saturate (9.1) may themselves generate globally smooth
flows.  Consequently R0.73P leaves the following question open:

\[
 \exists\delta[u]>0\ \forall t_0\ge0\ \forall w_0\in H^3_{\sigma,0},
 \quad
 \|w_0\|_2<\delta[u]
 \Longrightarrow u(t_0)+w_0\text{ generates a global forward strong solution}.
 \tag{9.2}
\]

At \(u\equiv0\), (9.2) is the fixed-torus, small-\(L^2\), arbitrary-high-
frequency regularity problem.  The present proof neither proves nor
disproves it.

## 10. Release boundary

The continuum results in Sections 2--9 are analytic.  Any plotted values of
\(N^{-3}\), \(N^{-1/2}\), or \(N^{5/2}\) are exact finite diagnostics of
these formulas only.  They are not simulations of (1.1), do not test
singularity formation, and add no strength to the proof.

```text
allTimeWeakL2RelativeStability=CLOSED_AFTER_AUDIT
globalCriticalH12OrbitStability=CLOSED_AS_CLASSICAL_COROLLARY
criticalH12Synchronization=CLOSED_AFTER_AUDIT
criticalToGlobalH3Propagation=CLOSED_AS_CLASSICAL_COROLLARY
bandLimitedL2ThresholdNMinusHalf=CLOSED_AS_COROLLARY
mixedL2HsThreshold=CLOSED_AS_COROLLARY
lowHighCriticalTailCertificate=CLOSED_AS_COROLLARY
normTransferNMinusHalfSharp=CLOSED
PDEDynamicalNMinusHalfSharp=NOT_CLAIMED
uniformL2OnlyStrongThreshold=OPEN_COLLISION_SENSITIVE
earlyWeakIntervalRegularity=OPEN
backwardRegularityInference=NOT_AVAILABLE
arbitraryThreeDimensionalGlobalRegularity=OPEN
clayConclusion=OPEN
noveltyOrPriorityClaim=FORBIDDEN
```

The exact public label is **NOT CLAY**.
