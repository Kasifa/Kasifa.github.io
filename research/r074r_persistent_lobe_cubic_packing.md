# R0.74R — terminal-window lobe packing beyond equal targets

## 0. Result and boundary

R0.74Q used equal target scales to expose an exterior velocity-cubic
obstruction.  This note removes the equal-target hypothesis from the convex
part of that argument.

The main theorem is the following.  Consider any smooth Version-M solution
in the inherited zero-path chart and average its weighted \(L^2\) energy on
each disjoint R0.74Q target lobe over the common interval \(J\).  Let
\(E_\ell\) be those realized window-averaged target scales,
\(S=\sum E_\ell\), \(Q=(\sum E_\ell^2)^{1/2}\), and
\(U=\sum_{\ell\ge2}E_\ell\).  Then, for all sufficiently large base
parameters,

\[
 \boxed{
 (P_R^M)^{2/3}
 \ge2^{2/3}(2L)^{-1/3}e^{\kappa_2L^2}U,
 \qquad
 \kappa_2=\frac{8831}{1905120}>0.}
\tag{R.100}
\]

Consequently, whenever \(S>0\), bounded normalized payment forces

\[
 \boxed{
 \frac US
 \le2^{-2/3}\frac{(P_R^M)^{2/3}}S
             (2L)^{1/3}e^{-\kappa_2L^2}.}
\tag{R.101}
\]

Thus the only target distributions not rejected by this payment row are
exponentially concentrated on the first target shell, not merely on an
unspecified coordinate.  The statement requires terminal-window lobe mass,
but no pointwise amplitude floor.  It still does not cover an arbitrary
terminal clock, because a clock may be created by an endpoint-only spike,
accumulated dissipation, or earlier variation outside \(J\).  It gives no
signed-flux estimate and no upper bound for the full clock square function.
It neither proves nor disproves the fixed-scale inequality, regularity,
singularity formation, or the Millennium problem.  **NOT CLAY.**

No numerical simulation, asymptotic fit, or DGX computation is used.

## 1. Frozen geometry

Use the exact R0.74Q constants

\[
 \lambda=\frac{63}{32},
 \qquad
 \rho=\frac1{320},
 \qquad
 c_\gamma=\frac8{3969}.
\tag{R.102}
\]

For integers \(j\to\infty\), define

\[
\begin{aligned}
 L&=\lambda2^j,
 &R&=e^{-\rho L^2},
 &N&=j,\\
 L_\ell&=2^{\ell-1}L,
 &k_\ell&=j+\ell-1,
 &1&\le\ell\le N.
\end{aligned}
\tag{R.103}
\]

The physical-shell weights are

\[
 \Gamma_\ell:=\gamma_{k_\ell}
 =e^{-c_\gamma L_\ell^2}.
\tag{R.104}
\]

The doubled-radius identity and the exact super-Gaussian definition give

\[
 A_{k_\ell}(R)=A_{k_\ell-1}(2R),
 \qquad
 \gamma_{k_\ell-1}
 =e^{-c_\gamma L_\ell^2/4}
 =\Gamma_\ell^{1/4}.
\tag{R.105}
\]

Retain the positive lobe cylinders from R0.74Q:

\[
 \mathcal O_{\ell,+}
 :=\{(t,x):t\in J,\ x\in\Omega_{\ell,+}(t)\},
 \qquad
 J=(65R^2-R^3,65R^2).
\tag{R.106}
\]

They obey

\[
 |J|=R^3,
 \qquad
 |\Omega_{\ell,+}(t)|=\frac1{16}L_\ell R^3,
 \qquad
 \Omega_{\ell,+}(t)\subset A_{k_\ell-1}(2R).
\tag{R.107}
\]

The inherited explicit moving-lobe construction makes each
\(\mathcal O_{\ell,+}\) Lebesgue measurable.  The shell indices are
distinct, so these sets are pairwise disjoint.  Also \(J\subset I_{2R}\)
for all sufficiently small \(R\), because \(J\) lies in the final \(R^3\)
portion of a backward interval of length \(4R^2\).

## 2. Window-averaged targets and clock detection

Define the realized terminal-window lobe energy

\[
 E_\ell
 :=\frac{\Gamma_\ell}{2R|J|}
   \int_J\int_{\Omega_{\ell,+}(t)}|u(t,x)|^2\,dx\,dt
\tag{R.108}
\]

and put

\[
 S:=\sum_{\ell=1}^NE_\ell,
 \qquad
 Q:=\left(\sum_{\ell=1}^NE_\ell^2\right)^{1/2},
 \qquad
 U:=\sum_{\ell=2}^NE_\ell=S-E_1.
\tag{R.109}
\]

These quantities use the realized total velocity.  They do not assume a
packet decomposition, equal targets, or a pointwise amplitude floor.

### Proposition 2.1 — terminal-window lobe detection

For every target index,

\[
 v_{k_\ell,R}\ge E_\ell,
 \qquad
 Y_{2,R}^{\rm sf}\ge Q.
\tag{R.110}
\]

**Proof.**  Let

\[
 e_\ell(t)
 :=\frac{\Gamma_\ell}{2R}
   \int_{\Omega_{\ell,+}(t)}|u(t,x)|^2\,dx.
\tag{R.111}
\]

The time and shell cutoffs equal one on the target lobe, and the remaining
part of the completed clock is nonnegative.  Thus

\[
 E_\ell=\fint_Je_\ell(t)\,dt
 \le\sup_{t\in J}e_\ell(t)
 \le\sup_{t\in J}K_{k_\ell,R}(t)
 \le v_{k_\ell,R}.
\tag{R.112}
\]

The last inequality uses \(K_{k,R}(s_R)=0\) and nonnegativity of the clock.
The target indices are distinct, so summing their squared lower bounds proves
(R.110). \(\square\)

The maximizing times may depend on \(\ell\); no common terminal slice is
needed for the square-function lower bound.  The result is intentionally
one-sided.  Off-target clocks and earlier positive variation may make the
full square function larger.

A pointwise floor remains a convenient sufficient condition.  If

\[
 m_\ell:=\inf_{(t,x)\in\mathcal O_{\ell,+}}|u(t,x)|,
 \qquad
 T_\ell:=\Gamma_\ell m_\ell^2L_\ell R^2,
\]

then the exact lobe measure gives \(E_\ell\ge T_\ell/32\).  The theorem
below is stronger because it is stated directly in terms of \(E_\ell\).

## 3. Additivity before convexity

Let \(W_{2R}\) denote the nonnegative periodized exterior weight in the
velocity-cubic payment row.  By (R.105) and the fact that the relevant
cutoff equals one on its annulus,

\[
 W_{2R}(x)\ge\gamma_{k_\ell-1}
 =\Gamma_\ell^{1/4}
 \quad\text{for }x\in\Omega_{\ell,+}(t).
\tag{R.113}
\]

### Proposition 3.1 — all-lobe exterior payment

Define

\[
 d_\ell:=\Gamma_\ell^{-5/4}L_\ell^{-1/2}.
\tag{R.114}
\]

Then the complete Version-M payment satisfies

\[
 \boxed{
 P_R^M\ge2\sqrt2\,R
       \sum_{\ell=1}^Nd_\ell E_\ell^{3/2}.}
\tag{R.115}
\]

**Proof.**  The exterior velocity-cubic row is a nonnegative summand of
\(P_R^M\).  Restrict its spacetime integral to the disjoint union of the
positive lobe cylinders.  Spacetime Hölder gives

\[
 \int_{\mathcal O_{\ell,+}}|u|^3
 \ge
 \frac{(\int_{\mathcal O_{\ell,+}}|u|^2)^{3/2}}
      {|\mathcal O_{\ell,+}|^{1/2}},
 \qquad
 |\mathcal O_{\ell,+}|=\frac1{16}L_\ell R^6.
\tag{R.116}
\]

By (R.108) and \(|J|=R^3\),

\[
 \int_{\mathcal O_{\ell,+}}|u|^2
 =2R^4\Gamma_\ell^{-1}E_\ell.
\tag{R.117}
\]

Therefore each restricted payment row obeys the exact scaling identity

\[
\begin{aligned}
 &(2R)^{-2}\Gamma_\ell^{1/4}
 \frac{(2R^4\Gamma_\ell^{-1}E_\ell)^{3/2}}
      {(L_\ell R^6/16)^{1/2}}\\
 &\hspace{35mm}
 =2\sqrt2\,R\Gamma_\ell^{-5/4}L_\ell^{-1/2}E_\ell^{3/2}.
\end{aligned}
\tag{R.118}
\]

Summing (R.118) over the disjoint lobe cylinders proves (R.115).  No
assertion of additivity for the complete nonlinear payment is needed.
\(\square\)

## 4. Sharp weighted Hölder optimization

### Lemma 4.1 — weighted target compression

For every nonempty finite index set \(I\),

\[
 \boxed{
 \sum_{\ell\in I}d_\ell E_\ell^{3/2}
 \ge
 \frac{(\sum_{\ell\in I}E_\ell)^{3/2}}
      {(\sum_{\ell\in I}d_\ell^{-2})^{1/2}}.}
\tag{R.119}
\]

Equality holds, when the denominator is nonzero, exactly along the ray
\(E_\ell=C_Id_\ell^{-2}\) on \(I\).

**Proof.**  Write

\[
 E_\ell
 =(d_\ell E_\ell^{3/2})^{2/3}d_\ell^{-2/3}
\tag{R.120}
\]

and apply Hölder with exponents \(3/2\) and \(3\).  Raising the result to
the power \(3/2\) proves (R.119).  The equality condition is the usual
Hölder proportionality condition. \(\square\)

The reciprocal weights are

\[
 b_\ell:=d_\ell^{-2}
 =\Gamma_\ell^{5/2}L_\ell.
\tag{R.121}
\]

Their adjacent ratio is exact:

\[
 \frac{b_{\ell+1}}{b_\ell}
 =2\exp\!\left[-\frac{15}{2}c_\gamma L_\ell^2\right].
\tag{R.122}
\]

Since \(L_\ell\ge L_2=2L\) for \(\ell\ge2\), all sufficiently large
\(j\) satisfy

\[
 \frac{b_{\ell+1}}{b_\ell}\le\frac12,
 \qquad \ell\ge2.
\tag{R.123}
\]

It follows that

\[
 \sum_{\ell=2}^Nb_\ell\le2b_2
 =2\Gamma_2^{5/2}L_2.
\tag{R.124}
\]

## 5. The first-shell stability theorem

### Theorem 5.1 — terminal-window lobe cubic packing

For all sufficiently large \(j\),

\[
 \boxed{
 (P_R^M)^{2/3}
 \ge2^{2/3}R^{2/3}
       \Gamma_2^{-5/6}L_2^{-1/3}U.}
\tag{R.125}
\]

Equivalently,

\[
 \boxed{
 (P_R^M)^{2/3}
 \ge2^{2/3}
       (2L)^{-1/3}e^{\kappa_2L^2}U,}
\tag{R.126}
\]

where

\[
 \kappa_2
 =\frac{10}{3}c_\gamma-\frac23\rho
 =\frac{80}{11907}-\frac1{480}
 =\frac{8831}{1905120}>0.
\tag{R.127}
\]

**Proof.**  Since \(E_1\le Q\),

\[
 U=\sum_{\ell=2}^NE_\ell=S-E_1\ge S-Q.
\tag{R.128}
\]

Apply Lemma 4.1 on \(I=\{2,\ldots,N\}\), use (R.124), then insert the
result into (R.115):

\[
 P_R^M
 \ge2\sqrt2\,R
       \frac{U^{3/2}}
            {(2\Gamma_2^{5/2}L_2)^{1/2}}.
\tag{R.129}
\]

Taking the \(2/3\) power yields (R.125):
\((2\sqrt2)^{2/3}=2\), and the factor \(2^{-1/3}\) from
the denominator leaves the exact prefactor \(2^{2/3}\).
Finally,

\[
\begin{aligned}
 R^{2/3}\Gamma_2^{-5/6}L_2^{-1/3}
 &=e^{-(2/3)\rho L^2}
   e^{(5/6)c_\gamma(2L)^2}(2L)^{-1/3}\\
 &=(2L)^{-1/3}
   e^{[(10/3)c_\gamma-(2/3)\rho]L^2},
\end{aligned}
\tag{R.130}
\]

and the rational arithmetic in (R.127) is exact. \(\square\)

### Corollary 5.2 — mass beyond the first shell is expensive

For every fixed \(\delta>0\),

\[
 U\ge\delta S
 \quad\Longrightarrow\quad
 \frac{(P_R^M)^{2/3}}S
 \ge2^{2/3}\delta
       (2L)^{-1/3}e^{\kappa_2L^2}
 \longrightarrow\infty.
\tag{R.131}
\]

Conversely, whenever \(S>0\) and \((P_R^M)^{2/3}\le MS\),

\[
 \frac US
 \le2^{-2/3}M(2L)^{1/3}e^{-\kappa_2L^2}.
\tag{R.132}
\]

In particular, \(E_1/S=1-U/S\).  If
\(\mathbf E=(E_1,\ldots,E_N)\) and
\(\mathbf e_1=(1,0,\ldots,0)\), then

\[
 \left\|\frac{\mathbf E}{S}-\mathbf e_1\right\|_{\ell^1}
 =\frac{2U}{S}
 \le2^{1/3}M(2L)^{1/3}e^{-\kappa_2L^2}.
\]

This is quantitative concentration on the first target shell, not a claim
about the complete shell-clock sequence.

## 6. Sharpness of the convex step

Apply Lemma 4.1 to all indices.  One obtains

\[
 \left(\sum_{\ell=1}^Nd_\ell E_\ell^{3/2}\right)^{2/3}
 \ge\frac{S}{(\sum_{\ell=1}^Nb_\ell)^{1/3}},
\tag{R.133}
\]

and equality is attained by the discrete vector

\[
 E_\ell=S\frac{b_\ell}{\sum_{m=1}^Nb_m}.
\tag{R.134}
\]

At the innermost shell,

\[
 R^{2/3}d_1^{2/3}
 =L^{-1/3}e^{\kappa_1L^2},
 \qquad
 \kappa_1
 =\frac56c_\gamma-\frac23\rho
 =-\frac{769}{1905120}<0.
\tag{R.135}
\]

Meanwhile

\[
 \frac{b_2}{b_1}
 =2e^{-(15/2)c_\gamma L^2}\longrightarrow0.
\tag{R.136}
\]

Thus (R.134) has \(E_1/S\to1\), \(U/S\to0\), and \(Q/S\to1\).  The negative exponent
in (R.135) shows why a bound using only \(S\), with no penalty for
concentration, cannot produce the outer-shell coercivity in Theorem 5.1.

This is the exact discrete escape and it is harmless for the intended
counterexample route: if one shell carries essentially all of \(S\), the
target square-function scale is also essentially \(S\).  Equation (R.134)
does not prove that an exact PDE family realizes a matching upper bound for
the full payment.

## 7. Consequence for the counterexample program

Suppose a sequence of terminal-window lobe-mass configurations were intended to
disprove the fixed-scale inequality by producing signed flux comparable to
\(S\).  It would necessarily require

\[
 (P_R^M)^{2/3}=o(S),
 \qquad
 Y_{2,R}^{\rm sf}=o(S).
\tag{R.137}
\]

Proposition 2.1 makes the second relation imply \(Q=o(S)\), hence
\(E_1=o(S)\).  The first relation and Theorem 5.1 imply \(U=o(S)\).
Together they contradict \(S=E_1+U\).  Therefore

\[
 \boxed{
 \text{no terminal-window lobe-mass configuration in the inherited chart can satisfy
 both requirements in (R.137).}}
\tag{R.138}
\]

This conclusion does not require equal \(E_\ell\).  It also does not require
a signed-flux lower bound: it is a conditional route-closing statement saying
that even if signed flux were later proved comparable to \(S\), the two
necessary small right-hand-side terms cannot coexist.

## 8. What the theorem does not see

The window average is weaker than a pointwise floor, but it still requires
positive kinetic lobe mass on a fixed terminal interval of length \(R^3\).
A general large completed clock may instead be caused by:

- endpoint energy that rises only on a time set much shorter than \(R^3\);
- accumulated viscous or anomalous dissipation without a terminal amplitude
  average;
- earlier positive variation followed by decay;
- a source/flux transfer whose sign is not represented by the energy floor;
- off-target shell interactions.

An instantaneous spatial Hölder inequality cannot replace a spacetime
interval, because the payment row is integrated in time while terminal
energy may live on a single time slice.  The next analytic gate is therefore
a stopping-time window-mass or dissipation alternative for a large residual
clock.  Such a gate would have to preserve the super-Gaussian shell
coefficients in (R.125), not merely produce an unweighted interval.

The signed cumulative flux, a matching upper bound for the full
\(Y_{2,R}^{\rm sf}\), a universal effective-shell theorem, the fixed-scale
inequality (Q.1), scale contraction, global regularity, and blow-up remain
**OPEN**.  **NOT CLAY.**
