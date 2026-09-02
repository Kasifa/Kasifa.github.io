# R0.74R — terminal-window lobe packing and the first-shell gate

## 0. Decision

R0.74Q proves that the canonical equal-target common-shear family pays far
more exterior velocity-cubic cost than its total target-clock scale.  That
calculation leaves a natural escape: abandon equal target heights and make
the outer targets progressively weaker.

R0.74R will decide this escape at the correct level of generality before any
new packet construction is attempted.  The first target is a deterministic
terminal-window lobe-mass theorem:

> if a finite collection of disjoint moving target lobes carries prescribed
> time-averaged weighted kinetic mass on the common terminal window, then
> either the exterior cubic payment is large relative to the total target
> scale, or the target vector is exponentially concentrated on the first
> target shell.

The theorem is geometric and convex.  It requires no pointwise amplitude
floor; such a floor is only a sufficient corollary.  It does not control a
clock created by an endpoint-only spike, accumulated dissipation without
terminal-window kinetic mass, or a signed flux.  Extending it from averaged
lobe mass to arbitrary terminal clocks is the subsequent PDE gate.  The
fixed-scale inequality (Q.1), global regularity, singularity, novelty, and
the Millennium problem remain open.  **NOT CLAY.**

## 1. Inherited R0.74Q chart

Retain

\[
 \lambda=\frac{63}{32},
 \qquad
 \rho=\frac1{320},
 \qquad
 c_\gamma=\frac8{3969},
\tag{R.1}
\]

and, along integers \(j\to\infty\),

\[
 L=\lambda2^j,
 \qquad
 R=e^{-\rho L^2},
 \qquad
 N=j,
 \qquad
 L_\ell=2^{\ell-1}L,
 \qquad
 k_\ell=j+\ell-1.
\tag{R.2}
\]

The target-shell and doubled-radius payment weights are

\[
 \Gamma_\ell=\gamma_{k_\ell}=e^{-c_\gamma L_\ell^2},
 \qquad
 \gamma_{k_\ell-1}=\Gamma_\ell^{1/4}.
\tag{R.3}
\]

The common terminal interval and positive target lobes satisfy

\[
 J=(65R^2-R^3,65R^2),
 \qquad |J|=R^3,
\tag{R.4}
\]

\[
 \Omega_{\ell,+}(t)\subset A_{k_\ell}(R)
 =A_{k_\ell-1}(2R),
 \qquad
 |\Omega_{\ell,+}(t)|=\frac1{16}L_\ell R^3.
\tag{R.5}
\]

Write
\[
 \mathcal O_{\ell,+}
 :=\{(t,x):t\in J,\ x\in\Omega_{\ell,+}(t)\}.
\]
The inherited explicit moving-lobe construction makes these sets Lebesgue
measurable, and distinct shell indices make them pairwise disjoint.  No
assertion in this freeze requires equal amplitudes or equal target scales.

## 2. Realized terminal-window target scales

For a smooth solution in the inherited zero-path chart, define the realized
window-averaged lobe energy

\[
 E_\ell
 :=\frac{\Gamma_\ell}{2R|J|}
   \int_J\int_{\Omega_{\ell,+}(t)}|u(t,x)|^2\,dx\,dt
\tag{R.6}
\]

and the associated target scales

\[
 S:=\sum_{\ell=1}^NE_\ell,
 \qquad
 Q:=\left(\sum_{\ell=1}^NE_\ell^2\right)^{1/2},
 \qquad
 U:=\sum_{\ell=2}^NE_\ell=S-E_1.
\tag{R.7}
\]

Here \(S\) is the target \(\ell^1\) scale and \(Q\) is its target
square-function scale.  Always

\[
 0\le U\le S,
 \qquad E_1=S-U\le Q,
 \qquad U\ge S-Q.
\tag{R.8}
\]

For

\[
 e_\ell(t):=\frac{\Gamma_\ell}{2R}
       \int_{\Omega_{\ell,+}(t)}|u(t,x)|^2\,dx,
 \qquad
 E_\ell=\fint_Je_\ell(t)\,dt
 \le\sup_{t\in J}K_{k_\ell,R}(t)
 \le v_{k_\ell,R}.
\tag{R.9}
\]

Here the time and shell cutoffs equal one on the target lobe, the remaining
completed-clock terms are nonnegative, and \(K_{k,R}(s_R)=0\).  Therefore

\[
 v_{k_\ell,R}\ge E_\ell,
 \qquad
 Y_{2,R}^{\rm sf}\ge Q.
\tag{R.10}
\]

Only the lower direction in (R.10) is claimed.  The maximizing times may
differ across shells; no common time slice is required.

A pointwise floor is a sufficient but unnecessary special case.  If
\(m_\ell=\inf_{\mathcal O_{\ell,+}}|u|\) and
\(T_\ell=\Gamma_\ell m_\ell^2L_\ell R^2\), then the exact lobe measure
gives \(E_\ell\ge T_\ell/32\).

## 3. The additive exterior-cubic lower bound

Let \(W_{2R}\) be the nonnegative doubled-radius exterior weight in the
Version-M payment.  Equations (R.3) and (R.5) give

\[
 W_{2R}(x)\ge\Gamma_\ell^{1/4}
 \quad\hbox{on }\Omega_{\ell,+}(t).
\tag{R.11}
\]

The lobe cylinders are disjoint, so the genuine nonnegative velocity-cubic
row may be summed before any estimate:

\[
\begin{aligned}
 P_R^M
 &\ge (2R)^{-2}
       \sum_{\ell=1}^N
       \int_J\int_{\Omega_{\ell,+}(t)}
       W_{2R}(x)|u(t,x)|^3\,dx\,dt\\
 &\ge2\sqrt2\,R
       \sum_{\ell=1}^N
       \Gamma_\ell^{-5/4}L_\ell^{-1/2}E_\ell^{3/2}.
\end{aligned}
\tag{R.12}
\]

Indeed, spacetime Hölder is applied on each
\(\mathcal O_{\ell,+}\), whose measure is \(L_\ell R^6/16\), while
\(\int_{\mathcal O_{\ell,+}}|u|^2=2R^4\Gamma_\ell^{-1}E_\ell\).
Put

\[
 d_\ell:=\Gamma_\ell^{-5/4}L_\ell^{-1/2}.
\tag{R.13}
\]

Then (R.12) becomes

\[
 \boxed{
 P_R^M\ge2\sqrt2\,R
       \sum_{\ell=1}^Nd_\ell E_\ell^{3/2}.}
\tag{R.14}
\]

This is a lower bound on an actual nonnegative payment row, not a divergent
upper majorant.

## 4. Convex packing inequality

For every nonempty index set \(I\), weighted Hölder gives

\[
 \left(\sum_{\ell\in I}E_\ell\right)^{3/2}
 \le
 \left(\sum_{\ell\in I}d_\ell E_\ell^{3/2}\right)
 \left(\sum_{\ell\in I}d_\ell^{-2}\right)^{1/2}.
\tag{R.15}
\]

Since

\[
 d_\ell^{-2}=\Gamma_\ell^{5/2}L_\ell,
\tag{R.16}
\]

the adjacent ratio is

\[
 \frac{d_{\ell+1}^{-2}}{d_\ell^{-2}}
 =2\exp\!\left(-\frac{15}{2}c_\gamma L_\ell^2\right).
\tag{R.17}
\]

For all sufficiently large \(j\), (R.17) is at most \(1/2\) for every
\(\ell\ge2\).  Hence

\[
 \sum_{\ell=2}^Nd_\ell^{-2}
 \le2\Gamma_2^{5/2}L_2.
\tag{R.18}
\]

Apply (R.15) to \(I=\{2,\ldots,N\}\), then use (R.8), (R.14), and (R.18):

\[
 \boxed{
 (P_R^M)^{2/3}
 \ge
 2^{2/3}R^{2/3}
 \Gamma_2^{-5/6}L_2^{-1/3}U.}
\tag{R.19}
\]

The coefficient has the exact form

\[
 R^{2/3}\Gamma_2^{-5/6}L_2^{-1/3}
 =(2L)^{-1/3}e^{\kappa_2L^2},
\tag{R.20}
\]

where

\[
 \kappa_2
 :=\frac{10}{3}c_\gamma-\frac23\rho
 =\frac{80}{11907}-\frac1{480}
 =\frac{8831}{1905120}>0.
\tag{R.21}
\]

Thus every fixed \(\delta>0\) obeys the dichotomy

\[
 \boxed{
 U\ge\delta S
 \quad\Longrightarrow\quad
 \frac{(P_R^M)^{2/3}}S
 \ge2^{2/3}\delta(2L)^{-1/3}e^{\kappa_2L^2}
 \longrightarrow\infty.}
\tag{R.22}
\]

More sharply, if \((P_R^M)^{2/3}\le MS\), then

\[
 \boxed{
 \frac US
 \le2^{-2/3} M(2L)^{1/3}e^{-\kappa_2L^2}.}
\tag{R.23}
\]

Low payment therefore forces the terminal-window target vector exponentially
close in \(\ell^1\) to the first-shell vector: indeed
\(\|\mathbf E/S-\mathbf e_1\|_{\ell^1}=2U/S\).

## 5. Why the first shell is a genuine discrete escape

The all-index version of (R.15) gives

\[
 \left(\sum_{\ell=1}^Nd_\ell E_\ell^{3/2}\right)^{2/3}
 \ge
 \frac{S}{(\sum_{\ell=1}^Nd_\ell^{-2})^{1/3}},
\tag{R.24}
\]

with equality for the purely discrete allocation

\[
 E_\ell
 =S\frac{d_\ell^{-2}}{\sum_{m=1}^Nd_m^{-2}}.
\tag{R.25}
\]

The corresponding first-shell coefficient is

\[
 R^{2/3}d_1^{2/3}
 =L^{-1/3}e^{\kappa_1L^2},
 \qquad
 \kappa_1
 :=\frac56c_\gamma-\frac23\rho
 =-\frac{769}{1905120}<0.
\tag{R.26}
\]

Moreover,

\[
 \frac{d_2^{-2}}{d_1^{-2}}
 =2e^{-(15/2)c_\gamma L^2}\longrightarrow0,
\tag{R.27}
\]

so the optimizer (R.25) has \(E_1/S\to1\), \(U/S\to0\), and \(Q/S\to1\).
Consequently the exterior-cubic lower bound alone permits a low normalized
value only by concentrating essentially all target mass on the innermost
shell.  Equation (R.25) is a
discrete witness, not a proof that an exact NSE family realizes a matching
payment upper bound or all-lobe dominance.

## 6. Route consequence

Suppose a terminal-window lobe-mass route were intended to disprove the
fixed-scale inequality, and suppose its signed cumulative flux were later
proved comparable to \(S\).  That route would need both

\[
 Y_{2,R}^{\rm sf}=o(S)
 \quad\hbox{and}\quad
 (P_R^M)^{2/3}=o(S).
\tag{R.28}
\]

But (R.10) makes the first condition imply \(Q=o(S)\), hence
\(E_1=o(S)\), while (R.19) makes the second imply \(U=o(S)\).  This
contradicts \(S=E_1+U\).  Hence no fixed-window lobe-mass route with signed
flux comparable to \(S\) can satisfy (R.28), without assuming equal target
heights.  This is a conditional route-closing statement, not a claim about
every possible counterexample to (Q.1).

This closes only that branch.  It does not prove (Q.1), because a general
terminal clock can arise from:

1. energy visible only at the terminal slice rather than with positive
   average on \(J\);
2. accumulated viscous or defect dissipation;
3. earlier positive variation followed by decay;
4. source/flux interactions not represented by terminal-window kinetic mass.

The next PDE question is whether a stopping-time window-mass or dissipation
alternative can extract a subwindow and lobe scale from a large residual
terminal clock, with constants compatible with (R.19).

## 7. Falsification gates

The analytic note must not be frozen until all of the following pass:

1. verify the doubled-radius shell identity and weight
   \(\gamma_{k_\ell-1}=\Gamma_\ell^{1/4}\) for every target;
2. verify the common-window length, lobe volume, disjointness, and exact
   coefficient \(2\sqrt2\) in (R.12);
3. audit the spacetime Hölder step from (R.12) to (R.14) with every power of
   \(R,\Gamma_\ell,L_\ell\);
4. prove (R.15) directly and certify both exponent signs in
   (R.21) and (R.26);
5. verify the tail ratio and the uniform geometric sum in (R.18);
6. retain the distinction between a realized window-averaged target and an
   arbitrary terminal clock;
7. retain the lower-only direction in (R.10); and
8. state explicitly that signed flux, a full \(Y_2\) upper bound, (Q.1),
   regularity, singularity, and Clay remain open.

No numerical Navier--Stokes simulation or DGX run is needed for this stage.
Finite exact arithmetic may certify the exponent and scaling ledger, but it
does not prove terminal-window mass extraction or any PDE theorem.
