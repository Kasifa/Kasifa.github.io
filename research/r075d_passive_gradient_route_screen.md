# R0.75D -- passive outer-gradient route screen

## 0. Target and verdict

The remaining exact-family target is

\[
 D_{k,R}^{{\rm out},F}
 :=\frac{\omega}{R}\int_{I_{2R}}\int
 \eta_R\xi_k^R|\nabla_{23}F|^2
 \stackrel{?}{\le}C(P_R^M)^{2/3}.
 \tag{D.1}
\]

The present audit finds a rigorous low-frequency calculation, but no
unconditional frequency decomposition and no exact counterexample.

\[
\boxed{
\begin{gathered}
\textbf{EXACT PASSIVE CACCIOPPOLI FALLBACK: }P^{2/3}+P;\\
\textbf{SMALL-PAYMENT PASSIVE OUTER DISSIPATION: PAID;}\\
\textbf{FROZEN COMMON-SHEAR BRANCH: LARGE PAYMENT, SO NOT CLOSED;}\\
\textbf{LOW FULL-SPATIAL FREQUENCY: PAID CONDITIONALLY;}\\
\textbf{HORIZONTAL FREQUENCY ALONE: INSUFFICIENT;}\\
\textbf{HIGH-FREQUENCY LOCAL CAPTURE: OPEN;}\\
\textbf{NO EXACT COUNTEREXAMPLE CONSTRUCTED.}
\end{gathered}}
\tag{D.2}
\]

## 1. Proved scale calculation for a low-frequency piece

Let \(G\) be a component satisfying, on the enlarged outer collar,
\[
 \int|\nabla_{23}G|^2\le K^2\int|G|^2.
 \tag{D.3}
\]
The collar spacetime volume is \(O(L^2R^5)\). Hölder and the
scale-\(2R\) lower weight \(W_{2R}\ge\omega\) give
\[
\begin{aligned}
 \int_{I_{2R}}\int_{\rm out}|G|^2
 &\le CL^{2/3}R^{5/3}
       \left(\int_{I_{2R}}\int_{\rm out}|G|^3\right)^{2/3},\\
 \int_{I_{2R}}\int_{\rm out}|G|^3
 &\le CR^2\omega^{-1}P_R^M.
\end{aligned}
\tag{D.4}
\]
Therefore
\[
 \frac{\omega}{R}\int_{I_{2R}}\int_{\rm out}|\nabla G|^2
 \le
 CK^2L^{2/3}R^2\omega^{1/3}(P_R^M)^{2/3}.
 \tag{D.5}
\]
This algebra is rigorous whenever (D.3) and pointwise/cubic separation of
the chosen piece are justified. The coefficient is bounded if
\[
 K\le K_{\rm low}:=
 cR^{-1}L^{-1/3}\omega^{-1/6}.
 \tag{D.6}
\]
At exponential scale,
\[
 L^{-2}\log K_{\rm low}
 =\frac\rho4+\frac{c_\gamma}{24}+o(1).
 \tag{D.7}
\]

The qualification in (D.5) matters. For a signed decomposition
\(F=G+H\), the total cubic payment controls \(|F|^3\), not \(|G|^3\)
separately. A Littlewood--Paley projection is not pointwise dominated by
\(F\). Thus (D.5) is not yet an unconditional low-frequency lemma.

## 2. Why horizontal splitting does not close the target

Because \(b=b(t,x_3)\), horizontal modes are invariant:
\[
 \partial_tf_n-\partial_3^2f_n+(n^2+inb)f_n=0.
 \tag{D.8}
\]
Their exact energy identity gives forward damping \(e^{-n^2(t-s)}\).
However, the horizontal zero mode
\[
 F_m(t,x_3)=e^{-m^2t}\sin(mx_3)
 \tag{D.9}
\]
has arbitrarily large vertical gradient. Hence an \(x_2\)-frequency
threshold cannot imply (D.3) and cannot control (D.1).

A full \((x_2,x_3)\) projection would control both derivatives, but it is
not invariant under multiplication by \(b(x_3)\).

## 3. Gradient identity and the shear commutator

Differentiating the passive equation shows that the vertical derivative
obeys
\[
 (\partial_t+b\partial_2-\Delta_{23})\partial_3F
 =-b_3\partial_2F.
 \tag{D.10}
\]
Globally,
\[
 \frac12\frac d{dt}\|\nabla_{23}F\|_2^2
 +\|\Delta_{23}F\|_2^2
 =-\int b_3\,\partial_2F\,\partial_3F.
 \tag{D.11}
\]
The sign is indefinite. A crude
\(\|b_3\|_\infty\) bound is too expensive: near a saturation transition it
can have scale \(B/R=O(R^{-3})\).

There is useful geometry not yet converted into a theorem. The large
\(b_3\) region is confined to \(O(R)\)-thick horizontal transition bands.
Their intersection with the spherical outer collar has volume
\(O(LR^3)\), one factor \(L^{-1}\) smaller than the full
\(O(L^2R^3)\) collar. R0.75C also proves that the background shear's own
gradient row is paid. What is missing is a mixed estimate for
\(b_3\partial_2F\) that uses this smaller volume without demanding an
unavailable \(L^\infty\) bound on \(F\).

## 4. Short-block damping and the \(R^{-1}\) loss

The full window has length \(O(R^2)\), while a natural transport block has
length \(O(R^3)\); hence there are \(O(R^{-1})\) blocks. Standard
Caccioppoli on the full window sums this count and produces the adverse
\(R^{-1}\) in B.38.

On one \(R^3\) block, a heat frequency \(K\) is strongly damped if
\[
 K^2R^3\gg1,\qquad\text{i.e.}\qquad K\gg R^{-3/2}.
 \tag{D.12}
\]
But the low-frequency payment threshold (D.6) has exponential rate
\(\rho/4+c_\gamma/24\), whereas \(R^{-3/2}\) has rate \(3\rho/8\).
For the frozen constants,
\[
 \frac{3\rho}{8}
 -\left(\frac\rho4+\frac{c_\gamma}{24}\right)
 =\frac\rho8-\frac{c_\gamma}{24}>0.
 \tag{D.13}
\]
Thus there is an intermediate band
\[
 K_{\rm low}\ll K\lesssim R^{-3/2}
 \tag{D.14}
\]
which is neither paid by the coarse low-frequency calculation nor strongly
damped within one block. Any successful split must address this band.

Backward amplification of \(K\gg R^{-3/2}\) is global. It becomes local
payment only after proving that the amplified energy stays in a region
where the central or exterior Version-M weight is bounded below.

## 5. Localization and periodic-weight blockers

Three noncommuting operations must be handled simultaneously:

1. spatial frequency projection and multiplication by \(b(x_3)\);
2. frequency projection and the moving collar cutoff \(\xi_k^R\);
3. projection tails and the periodic shell weight \(W_{2R}\).

The commutators have schematic form
\[
 [P_{\le K},b]\partial_2F,\qquad
 [P_{\le K},\xi_k^R]F.
 \tag{D.15}
\]
The first depends on derivatives of \(b\); the second has size involving
\((KR)^{-1}\) only when \(KR\gg1\). Nonlocal projection tails can leave the
physical shell, where the lower weight \(W_{2R}\ge\omega\) is no longer
available. Periodization must be retained before using any kernel estimate.

These are analytic blockers, not finite-arithmetic issues.

## 6. Exact transport/payment fallback and why it does not close the branch

The crude replacement \(|b|\le CR^{-2}\) in R0.75B is not needed for a
two-regime estimate. Apply (B.14) with \(\chi=\xi_k^R\), keep the
transport term separate, discard the nonnegative endpoint term, and put

\[
 \begin{aligned}
 p_F&:=R^{-2}\omega
   \int_{I_{2R}}\int_{\operatorname {supp}\xi_k^R}|F|^3,\\
 p_b&:=R^{-2}\omega
   \int_{I_{2R}}\int_{\operatorname {supp}\xi_k^R}|b|^3.
 \end{aligned}
 \tag{D.16}
\]

The scale-\(2R\) exterior velocity row and
\((F^2+b^2)^{3/2}\ge\max\{|F|^3,|b|^3\}\) imply

\[
 p_F+p_b\le CP_R^M.
 \tag{D.17}
\]

The time and Laplacian cutoff rows satisfy

\[
 \begin{aligned}
 \omega R^{-3}\int_{I_{2R}}\int_{\rm out}|F|^2
 &\le C\omega R^{-3}(L^2R^5)^{1/3}
       (R^2\omega^{-1}p_F)^{2/3}\\
 &\le CL^{2/3}\omega^{1/3}p_F^{2/3}.
 \end{aligned}
 \tag{D.18}
\]

For the drift row, spacetime Hölder gives the exact mixed-cubic
homogeneity

\[
 \begin{aligned}
 \omega R^{-2}\int_{I_{2R}}\int_{\rm out}|b||F|^2
 &\le
 \omega R^{-2}
 \left(\int_{I_{2R}}\int_{\rm out}|b|^3\right)^{1/3}
 \left(\int_{I_{2R}}\int_{\rm out}|F|^3\right)^{2/3}\\
 &=p_b^{1/3}p_F^{2/3}.
 \end{aligned}
 \tag{D.19}
\]

Consequently the passive outer dissipation obeys the unconditional
two-regime estimate

\[
 \boxed{
 D_{k,R}^{{\rm out},F}
 \le CL^{2/3}\omega^{1/3}p_F^{2/3}
      +Cp_b^{1/3}p_F^{2/3}
 \le CL^{2/3}\omega^{1/3}(P_R^M)^{2/3}+CP_R^M.}
 \tag{D.20}
\]

In particular,

\[
 P_R^M\le1
 \quad\Longrightarrow\quad
 D_{k,R}^{{\rm out},F}\le C(P_R^M)^{2/3},
 \tag{D.21}
\]

because \(L^{2/3}\omega^{1/3}\to0\) and
\(P_R^M\le(P_R^M)^{2/3}\). This is the outer-padding analogue of the
R0.74H small-payment fallback, not a new regularity statement.

It does not close the frozen common-shear branch. R0.75C (C.13)--(C.15)
and the calibration \(B\asymp R^{-2}\) give

\[
 p_b\asymp L^2\omega R^{-3},
 \qquad
 \lim_{L\to\infty}\frac1{L^2}\log p_b
 =\frac{3\rho}{4}-\frac{c_\gamma}{4}
 =\frac{27163}{158760000}>0.
 \tag{D.22}
\]

Thus \(P_R^M\ge c p_b\to\infty\); the linear term in (D.20) cannot be
absorbed by the small-payment implication. More precisely, the mixed
term has the desired quadratic scale exactly under the additional
condition

\[
 p_bp_F^2\le C(P_R^M)^2.
 \tag{D.23}
\]

No such uniform interaction bound is presently proved. Equation (D.19)
also identifies what a successful argument must improve: it must exploit
the sign of the localized transport flux, the shear dynamics, or spatial
separation. Reapplying absolute Hölder/Young inequalities cannot change
the linear homogeneity.

## 7. Two viable next lemmas

### Route I: localized parabolic frequency dichotomy

Prove a decomposition intrinsic to the cutoff cylinder, not a global
Fourier split:

- low local Rayleigh quotient implies (D.5);
- high local Rayleigh quotient yields blockwise dissipation or backward
  energy captured by a nonnegative Version-M row;
- the transition-band commutator is absorbed using its
  \(O(LR^3)\) spatial volume and the already-paid shear estimates.

This is the most direct proof route, but every commutator and shell-weight
tail remains OPEN.

### Route II: exact counterexample search

An exact counterexample must be re-evolved forward from admissible initial
data under the same shear and must simultaneously:

- concentrate passive gradient in the outer collar for many blocks;
- avoid the safe inward weight and central-energy row;
- retain all periodic copies and cutoff-flux terms;
- make \(D_{k,R}^{{\rm out},F}/(P_R^M)^{2/3}\to\infty\).

A narrow high-frequency packet alone is not enough: its backward heat cost
or cubic residence may enter other payment rows. No family satisfying all
four conditions is constructed here.

## 8. Status boundary

**Proved calculations:** (D.4)--(D.7), horizontal modal invariance,
(D.10)--(D.13), the stated geometric volumes, and the exact
two-regime/mixed-payment estimates (D.16)--(D.22).

**Conditional lemmas:** low-frequency payment under a localized Rayleigh
bound plus cubic comparability; high-frequency capture under a localized
observability-to-payment inequality.

**Open steps:** proving the interaction condition (D.23) or replacing it
by a signed transport argument, controlling the intermediate band, the
\(b_3\partial_2F\) commutator, cutoff/projection leakage, periodic weights,
and constructing or excluding an exact counterexample.

This route screen proves neither complete-clock extraction nor a
Navier--Stokes regularity or singularity result. \(\mathbf{NOT\ CLAY}\).
