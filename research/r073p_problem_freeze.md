# R0.73P problem freeze: critical stability, frequency gates, and the early-time gap

**Status:** scope frozen; primary-source collision audit and independent
analytic readback passed; formula-diagnostic and publication gates remain

**Parent result:** R0.73O global-orbit \(H^3\) stability and the open
\(L^2\)-only/high-frequency input interface

**Equation:** unforced incompressible Navier--Stokes on the normalized standard
three-torus, viscosity one, in the mean-zero divergence-free phase space

## 0. The question that is actually being tested

Let

\[
 u\in C([0,\infty);H^3_{\sigma,0})
 \cap L^2_{\rm loc}([0,\infty);H^4_{\sigma,0})
 \tag{0.1}
\]

be an a priori global unforced strong orbit.  R0.73O proved a positive
\(H^3\) stability tube around this orbit.  R0.73P asks what remains true when
the initial difference is small only at lower regularity and may be very
large in \(H^3\).

The release must keep three different interfaces separate.

1. **Weak \(L^2\) interface.**  Compare the reference orbit with every
   Leray--Hopf solution, without claiming regularity or uniqueness of that
   comparison solution during its possible early weak phase.
2. **Critical \(H^{1/2}\) interface.**  Use the scale-critical robustness
   theorem to obtain global strong continuation and synchronization.
3. **Frequency-localized \(L^2\) interface.**  Transfer the critical radius
   to an \(L^2\) threshold under an explicit upper-frequency or tail
   hypothesis.

The forbidden inference is

\[
 \|v(t_0)-u(t_0)\|_2\ll1
 \quad\Longrightarrow\quad
 v\text{ is strong from }t_0
 \tag{0.2}
\]

with no frequency or higher-norm information.  Establishing (0.2) uniformly
even at the zero background would close a supercritical small-energy
regularity problem that remains open.

## 1. Norm convention and two finite orbit actions

Work on \([0,2\pi]^3\) with normalized Haar measure
\((2\pi)^{-3}dx\).  Let \(A=-P\Delta\) be the Stokes operator and write

\[
 |z|_s:=\|A^{s/2}z\|_2,
 \qquad s\in\mathbb R.
 \tag{1.1}
\]

The first Stokes eigenvalue is one, so \(|z|_{s+1}\ge |z|_s\).
R0.73O supplies eventual exponential decay in every Sobolev order needed
below.  In particular the following two actions are finite:

\[
 \mathcal A_{1/2}[u]
 :=\int_0^\infty |u(t)|_1^4\,dt<\infty,
 \tag{1.2}
\]

and

\[
 \mathcal L[u]
 :=\int_0^\infty\|\nabla u(t)\|_\infty\,dt<\infty.
 \tag{1.3}
\]

For (1.2), use boundedness of \(|u|_1\) and the finite energy
dissipation \(\int_0^\infty |u|_1^2\).  For (1.3), use Sobolev embedding on
the finite initial interval and the R0.73O exponential high-order tail.

## 2. Target P1: all-time weak relative-energy stability

For any \(v_0\in L^2_{\sigma,0}\) and any Leray--Hopf solution \(v\) from
\(v_0\), put \(w=v-u\).  The target relative-energy inequality is

\[
 {1\over2}{d\over dt}\|w\|_2^2+|w|_1^2
 \le \|\nabla u\|_\infty\|w\|_2^2
 \tag{2.1}
\]

in the standard integrated weak--strong sense.  It should imply, for every
\(t\ge t_0\),

\[
 \boxed{
 \|w(t)\|_2
 \le e^{\mathcal L[u]}e^{-(t-t_0)}\|w(t_0)\|_2.}
 \tag{2.2}
\]

No smallness is required.  The conclusion is weak \(L^2\) proximity and
decay only.  It does not make \(v\) regular during the early interval and
does not supply uniqueness between two arbitrary Leray--Hopf solutions.

## 3. Target P2: an all-starting-time critical stability tube

Published periodic robustness theorems in \(\dot H^{1/2}\) give, on each
finite interval, a sufficient condition of the form

\[
 |w(t_0)|_{1/2}^2
 \exp\!\left(C\int_{t_0}^{T}|u(t)|_1^4\,dt\right)<c.
 \tag{3.1}
\]

Because (1.2) is finite, the target global radius can be written

\[
 R_{1/2}[u]
 :=c_*\exp\!\left(-C_*\mathcal A_{1/2}[u]\right)>0,
 \tag{3.2}
\]

with universal or explicitly computable constants.  For every \(t_0\ge0\),

\[
 |v(t_0)-u(t_0)|_{1/2}<R_{1/2}[u]
 \tag{3.3}
\]

must imply a unique global Fujita--Kato solution

\[
 v\in C([t_0,\infty);H^{1/2}_{\sigma,0})
 \cap L^2_{\rm loc}([t_0,\infty);H^{3/2}_{\sigma,0}).
 \tag{3.4}
\]

After decreasing the radius by a universal factor, the proof should retain
Poincare damping and give

\[
 |v(t)-u(t)|_{1/2}
 \le C[u]e^{-c_*(t-t_0)}|v(t_0)-u(t_0)|_{1/2}.
 \tag{3.5}
\]

If \(v(t_0)\in H^3\), weak--strong uniqueness, Serrin regularity, and
parabolic propagation must upgrade (3.4) to a global \(H^3\) strong
solution from \(t_0\).

## 4. Target P3: exact frequency-localized consequences

Let \(P_{\le N}\) denote the orthogonal Fourier projection to
\(0<|k|\le N\), let \(Q_{>N}=I-P_{\le N}\), and let \(R_3[u]\) be the
homogeneous Stokes \(H^3\) radius from R0.73O.
For a band-limited difference \(w_0=P_{\le N}w_0\),

\[
 |w_0|_{1/2}\le N^{1/2}\|w_0\|_2.
 \tag{4.1}
\]

Hence the critical tube gives the sufficient condition

\[
 \boxed{\|w_0\|_2<R_{1/2}[u]N^{-1/2}.}
 \tag{4.2}
\]

The direct R0.73O \(H^3\) transfer would require

\[
 \|w_0\|_2<R_3[u]N^{-3}.
 \tag{4.3}
\]

Thus the critical route improves the frequency exponent from \(-3\) to
\(-1/2\).  At the critical boundary, a single normalized Fourier mode has

\[
 \|w_N\|_2\asymp R_{1/2}[u]N^{-1/2},
 \qquad
 |w_N|_3\asymp R_{1/2}[u]N^{5/2},
 \tag{4.4}
\]

so the new tube includes smooth perturbations whose \(H^3\) size diverges.
The exponent \(-1/2\) is sharp for the norm-transfer inequality (4.1), not
for the Navier--Stokes dynamics.

The release should also record two more sufficient interfaces:

\[
 |w_0|_{1/2}
 \le \|w_0\|_2^{1-1/(2s)}|w_0|_s^{1/(2s)},
 \qquad s>{1\over2},
 \tag{4.5}
\]

and

\[
 |w_0|_{1/2}^2
 \le N\|w_0\|_2^2+|Q_{>N}w_0|_{1/2}^2.
 \tag{4.6}
\]

If \(|w_0|_s\le M\), (4.5) yields

\[
 \|w_0\|_2
 <R_{1/2}[u]^{\frac{2s}{2s-1}}
 M^{-\frac1{2s-1}}.
 \tag{4.7}
\]

These are mixed or localized criteria, not \(L^2\)-only criteria.

## 5. Target P4: eventual regularity and the early-time gap

Every unforced periodic Leray--Hopf solution eventually becomes Gevrey
regular and decays exponentially.  The primary-source audit must verify a
time \(T(M)\) and bounds uniform over the energy ball
\(\|v_0\|_2\le M\).

The strongest admissible internal corollary is a delayed smoothing estimate
of the form

\[
 \|v(t)-u(t)\|_{H^3}
 \le C(u,M)e^{-c(t-T(M))}\|v_0-u_0\|_2,
 \qquad t\ge T(M)+\tau_*,
 \tag{5.1}
\]

for a fixed positive smoothing delay \(\tau_*\).  This claim may enter the
release only after an independent proof checks uniformity over every
Leray--Hopf selection.

Even if (5.1) passes, it deliberately permits an earlier weak interval.
Eventual smoothness by itself supplies no backward regularity implication
and therefore does not close the Clay problem.

## 6. Literature and priority boundary

The following are expected collision sources and must be treated as primary
inputs rather than novelty support:

- Mar\'in-Rubio--Robinson--Sadowski: periodic \(\dot H^{1/2}\) robustness;
- Burczak--Zaj\k{a}czkowski: quantitative periodic
  \(\dot H^\alpha\), \(\alpha\in[1/2,1]\), robustness;
- Fujita--Kato and standard Serrin theory: critical local theory and
  regularity propagation;
- Hoang--Martinez: eventual Gevrey regularity for all periodic
  Leray--Hopf solutions;
- Mucha 2001 and 2008: the closest \(L^2\)-small/high-norm-large collision
  claims.

R0.73P may claim a topology-matched synthesis and a sharper frequency
transfer relative to R0.73O.  It must not claim the critical robustness
theorem itself as new.  Mucha 2001 cannot be used beyond its verified
quantifiers; Mucha 2008 explicitly makes its \(L^2\) smallness relative to a
higher Besov trace norm.

## 7. Exact machine-readable boundary

```text
allTimeWeakL2RelativeStability=CLOSED_AFTER_AUDIT
globalCriticalH12OrbitStability=CLOSED_AS_CLASSICAL_COROLLARY
criticalH12Synchronization=CLOSED_AFTER_AUDIT
criticalToGlobalH3Propagation=CLOSED_AS_CLASSICAL_COROLLARY
bandLimitedL2ThresholdNMinusHalf=CLOSED_AS_COROLLARY
mixedL2HsThreshold=CLOSED_AS_COROLLARY
lowHighCriticalTailCertificate=CLOSED_AS_COROLLARY
uniformEventualRegularityOnL2Ball=CLOSED_AFTER_AUDIT
uniformEventualSmallH3Entry=CLOSED_AFTER_AUDIT
oneSidedDelayedL2ToH3Synchronization=CLOSED_AFTER_AUDIT
uniformL2OnlyStrongThreshold=OPEN_COLLISION_SENSITIVE
normTransferNMinusHalfSharp=CLOSED
PDEDynamicalNMinusHalfSharp=NOT_CLAIMED
arbitraryLerayPairLipschitzSemigroup=NOT_PROVED
earlyWeakIntervalRegularity=OPEN
backwardRegularityInference=NOT_AVAILABLE
arbitraryThreeDimensionalGlobalRegularity=OPEN
clayConclusion=OPEN
noveltyOrPriorityClaim=FORBIDDEN
```

The public label remains **NOT CLAY**.
