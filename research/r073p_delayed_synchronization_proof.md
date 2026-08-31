# R0.73P proof: uniform eventual regularity on energy balls and one-sided delayed \(L^2\to H^3\) synchronization

**Status:** **FORMAL PASS after independent analytic readback**; the
quantifiers were checked against Hoang--Martinez Theorem 2.4

**Claim boundary:** the Lipschitz estimate compares every Leray--Hopf
solution with one fixed a priori global strong reference orbit.  It is not a
Lipschitz semigroup theorem between two arbitrary Leray--Hopf selections.

Throughout this proof the domain is the standard torus \([0,2\pi]^3\), the
viscosity is one, the Haar measure is normalized, and the first positive
Stokes eigenvalue is one.  The explicit exponential rates and the constants
in the common entry times use this normalization.

## 1. Uniform eventual regularity for an \(L^2\) energy ball

Write

\[
 E_m[z](t)=|z(t)|_m^2=\|A^{m/2}z(t)\|_2^2,
 \qquad E_{m+1}\ge E_m.
 \tag{1.1}
\]

There are universal constants \(K_1,C_2,C_3\) such that every strong
solution satisfies

\[
 {1\over2}E_1'+{1\over2}E_2\le K_1E_1^3,
 \tag{1.2}
\]

\[
 {1\over2}E_2'+E_3\le C_2E_1^{1/2}E_3,
 \tag{1.3}
\]

and

\[
 {1\over2}E_3'+E_4\le C_3E_2^{1/2}E_4.
 \tag{1.4}
\]

Fix a universal \(\eta_*>0\), small enough that

\[
 K_1\eta_*^4\le{1\over4},
 \qquad
 C_2\eta_*\le{1\over2},
 \qquad
 C_3\sqrt2\,\eta_*\le{1\over2}.
 \tag{1.5}
\]

It will be decreased once more in Section 3 to absorb the difference
equation.

Let \(v\) be any Leray--Hopf solution with \(\|v_0\|_2\le M\).  If
\(M=0\), the energy inequality forces \(v\equiv0\), so every conclusion
below is immediate.  Assume henceforth that \(M>0\).  Energy and Poincare
give

\[
 E_0(t)\le e^{-2t}M^2
 \tag{1.6}
\]

and, for every admissible energy starting time \(T_0\),

\[
 \int_{T_0}^{T_0+1}E_1(t)\,dt
 \le {1\over2}E_0(T_0)
 \le {1\over2}e^{-2T_0}M^2.
 \tag{1.7}
\]

Define

\[
 L(M)=\bigl(\log(M/\eta_*)\bigr)_+,
 \qquad L(0)=0.
 \tag{1.8}
\]

For each Leray--Hopf selection choose an energy-admissible
\(T_0\in(L(M),L(M)+1)\).  Intersecting the full-measure set on which
\(v(t)\in H^1\) and the strong energy inequality can restart with the
positive-measure sublevel set supplied by (1.7), choose
\(t_*\in(T_0,T_0+1)\) such that

\[
 |v(t_*)|_1<e^{-T_0}M<\eta_*.
 \tag{1.9}
\]

At this time, local \(H^1\) theory starts a strong solution.  On the ball
\(|v|_1\le\eta_*\), (1.2) and (1.5) give

\[
 E_1'+{1\over2}E_2\le0.
 \tag{1.10}
\]

The ball is forward invariant, so the strong solution is global.  By
weak--strong uniqueness, the original Leray--Hopf selection coincides with
it for every \(t\ge t_*\).  Although \(t_*\) can depend on the selected weak
solution, it always satisfies

\[
 t_*<T_{\rm reg}(M):=L(M)+2.
 \tag{1.11}
\]

Thus every Leray--Hopf selection in the energy ball is regular after the
same deterministic upper time \(T_{\rm reg}(M)\).

## 2. Uniform entry into a small \(H^3\) ball

From (1.10),

\[
 \int_{T_{\rm reg}}^{T_{\rm reg}+1}E_2(t)\,dt
 \le2E_1(T_{\rm reg})\le2\eta_*^2.
 \tag{2.1}
\]

There is a time \(s_2\in[T_{\rm reg},T_{\rm reg}+1]\) such that
\(E_2(s_2)\le2\eta_*^2\).  Since \(|v|_1\le\eta_*\), (1.3) gives

\[
 E_2'+E_3\le0.
 \tag{2.2}
\]

Hence, at the common time

\[
 T_2(M)=T_{\rm reg}(M)+1,
 \tag{2.3}
\]

one has \(E_2(T_2)\le2\eta_*^2\).  From \(s_2\) onward,
\(|v|_2\le\sqrt2\eta_*\), and (1.4) gives

\[
 E_3'+E_4\le0.
 \tag{2.4}
\]

Moreover,

\[
 \int_{T_2}^{T_2+1}E_3(t)\,dt
 \le E_2(T_2)\le2\eta_*^2.
 \tag{2.5}
\]

Choose \(s_3\in[T_2,T_2+1]\) with
\(E_3(s_3)\le2\eta_*^2\).  Monotonicity in (2.4) proves that at the common
time

\[
 \boxed{T_3(M)=L(M)+4}
 \tag{2.6}
\]

every Leray--Hopf selection with \(\|v_0\|_2\le M\) satisfies

\[
 \boxed{|v(t)|_3\le\sqrt2\,\eta_*,
 \qquad t\ge T_3(M).}
 \tag{2.7}
\]

The result is uniform over the energy ball and over the choice of
Leray--Hopf solution.  The selection-dependent times \(t_*,s_2,s_3\) have
only been used inside fixed windows with common upper endpoints.

This self-contained Sobolev argument is compatible with the same
uniform-over-selection quantifier in Hoang--Martinez Theorem 2.4.  That
theorem proves the stronger Gevrey estimate with its own explicit common
starting time depending on \(\sigma\) and \(\|v_0\|_2\); the two numerical
starting times are not identified.

## 3. Difference energy after the common entry time

Fix the a priori global strong reference orbit \(u\), and let

\[
 \mathcal L[u]=\int_0^\infty\|\nabla u(t)\|_\infty\,dt,
 \qquad K_u=e^{\mathcal L[u]}.
 \tag{3.1}
\]

Assume

\[
 \|u_0\|_2\le M,
 \qquad
 \|v_0\|_2\le M,
 \tag{3.2}
\]

and let \(v\) be any Leray--Hopf solution from \(v_0\).  Put \(w=v-u\).
The relative-energy estimate from the critical-frequency proof gives

\[
 |w(t)|_0\le K_u|w(0)|_0,
 \qquad t\ge0.
 \tag{3.3}
\]

Set \(T=T_3(M)\).  By (2.7),

\[
 |u(t)|_3+|v(t)|_3\le2\sqrt2\,\eta_*,
 \qquad t\ge T.
 \tag{3.4}
\]

Write the difference equation as

\[
 w_t+Aw+B(v,w)+B(w,u)=0.
 \tag{3.5}
\]

Decrease \(\eta_*\), depending only on the universal periodic product
constants, so that all terms in (3.5) can be absorbed at levels zero through
three.  Standard Sobolev multiplication and Poincare then give

\[
 F_m'(t)+F_{m+1}(t)\le0,
 \qquad F_m=|w|_m^2,
 \qquad m=0,1,2,3,
 \quad t\ge T.
 \tag{3.6}
\]

For completeness, cancellation of \(\langle B(v,w),w\rangle\) at level zero
and the four product estimates give

\[
 {1\over2}F_0'+F_1
 \le C|u|_3F_0\le C\eta_*F_1,
 \tag{3.7}
\]

\[
 {1\over2}F_1'+F_2
 \le C(|u|_2+|v|_2)|w|_1|w|_2
 \le C\eta_*F_2,
 \tag{3.8}
\]

\[
 {1\over2}F_2'+F_3
 \le C(|u|_2+|v|_2)|w|_2|w|_3
 \le C\eta_*F_3,
 \tag{3.9}
\]

and

\[
 {1\over2}F_3'+F_4
 \le C(|u|_3+|v|_3)|w|_3|w|_4
 \le C\eta_*F_4.
 \tag{3.10}
\]

The second line uses the displayed \(L^2\) product estimate; the third uses
\(\|B(a,b)\|_{H^1}\le C\|a\|_{H^2}\|b\|_{H^2}\); the last uses
\(\|B(a,b)\|_{H^2}\le C\|a\|_{H^3}\|b\|_{H^3}\).
After decreasing the universal \(\eta_*\), these four displayed lines prove
(3.6).

## 4. Three fixed smoothing windows and the delayed Lipschitz estimate

Integrating the \(m=0\) inequality in (3.6) over \([T,T+1]\) gives a time
\(\tau_1\in[T,T+1]\) with

\[
 F_1(\tau_1)\le F_0(T).
 \tag{4.1}
\]

Integrating the \(m=1\) inequality over
\([\tau_1,\tau_1+1]\) gives a time \(\tau_2\) with

\[
 F_2(\tau_2)\le F_1(\tau_1).
 \tag{4.2}
\]

Similarly, the \(m=2\) inequality gives
\(\tau_3\in[\tau_2,\tau_2+1]\) with

\[
 F_3(\tau_3)\le F_2(\tau_2),
 \qquad \tau_3\le T+3.
 \tag{4.3}
\]

Therefore

\[
 F_3(\tau_3)\le F_0(T)\le K_u^2F_0(0).
 \tag{4.4}
\]

The final inequality \(F_3'+F_4\le0\), together with
\(F_4\ge F_3\), yields

\[
 F_3(t)\le e^{-(t-\tau_3)}F_3(\tau_3).
 \tag{4.5}
\]

Since \(\tau_3\le T_3(M)+3\), for every
\(t\ge T_3(M)+3\),

\[
 \boxed{
 |v(t)-u(t)|_3
 \le K_u
 e^{-\frac12(t-T_3(M)-3)}
 |v_0-u_0|_0.}
 \tag{4.6}
\]

The usual inhomogeneous \(H^3\) version follows through fixed norm
equivalence constants.

## 5. Exact quantifiers and exclusions

The proved one-sided statement is

\[
 \begin{aligned}
 &\forall u\text{ satisfying the global strong hypothesis}\;
 \forall M\ge\|u_0\|_2\;
 \exists T_3(M),K_u;\\
 &\forall v_0\in L^2_{\sigma,0},\ \|v_0\|_2\le M;\
 \forall v\in LH(v_0)\ \forall t\ge T_3(M)+3:\quad
 \text{(4.6) holds}.
 \end{aligned}
 \tag{5.1}
\]

The constants have deliberately different dependencies:

- \(T_3(M)\) depends only on the energy radius and universal product
  constants;
- \(K_u\) depends on the fixed reference orbit through its early strain
  integral;
- the internal selection times can depend on \(v\), but their upper bounds
  do not.

The proof does **not** give a Lipschitz estimate between two arbitrary
Leray--Hopf selections, because the early relative-energy estimate uses one
side as a fixed global strong solution.  It also does not show that \(v\) is
strong on \([0,T_{\rm reg}(M))\).  The unknown early weak interval is exactly
what prevents backward conversion of eventual regularity into a Clay
conclusion.

```text
uniformEventualRegularityOnL2Ball=CLOSED_AFTER_AUDIT
uniformEventualSmallH3Entry=CLOSED_AFTER_AUDIT
oneSidedDelayedL2ToH3Synchronization=CLOSED_AFTER_AUDIT
arbitraryLerayPairLipschitzSemigroup=NOT_PROVED
strongRegularityFromInitialTime=OPEN
backwardRegularityInference=NOT_AVAILABLE
clayConclusion=OPEN
```
