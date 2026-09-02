# R0.74Q — independent audit of the relaxed multipacket geometry

## 0. Bound source and audit scope

This audit is bound to the final source bytes

```text
research/r074q_relaxed_multipacket_cubic_obstruction.md
SHA-256 ba8897da349aa5c71c5ac355164a938599489c2691b09eb59760934b70617e8d
```

The audit covers only:

1. the exact finite-\(N\) common-shear Navier--Stokes solution and its
   parity/path identities;
2. the relaxed common calibration;
3. the uniform reuse of the R0.74F bridge argument;
4. the terminal annular geometry;
5. the simultaneous terminal lower bounds for the defect-completed clocks;
6. the claim boundary.

The cubic-payment lower bound and the detailed all-packet amplitude sums are
outside this audit.  No simulation or floating-point asymptotic fit is used.

**Overall verdict: PASS.**

## 1. Exact common-shear PDE, parity, and path — PASS

For each fixed \(j\), the number

\[
 N=\lfloor\log _2L\rfloor=j
\]

is finite.  Every passive packet solves the same equation

\[
 (\partial_t+B\theta_R\partial_2-\Delta_{23})G_\ell^\pm=0.
\]

Consequently their amplitude-weighted finite sum \(U_N\) solves the same
linear equation.  For

\[
 u^{(N)}=(U_N,B\theta_R,0),\qquad p^{(N)}=0,
\]

the fields are independent of \(x_1\), and the shear is independent of
\(x_2\).  Direct substitution gives

\[
 \nabla\!\cdot u^{(N)}=0,
 \qquad
 u^{(N)}\!\cdot\nabla=B\theta_R\partial_2,
\]

while the second component satisfies the one-dimensional heat equation.
Thus the PDE and the zero-pressure assertion are exact for each finite
\(N\); no nonlinear superposition principle is being invoked.

The inversion-paired data and the odd shear imply

\[
 u^{(N)}(t,-x)=-u^{(N)}(t,x).
\]

Convolution with the frozen even mollifier therefore vanishes at the origin.
Uniqueness for the smooth terminal-value trajectory ODE gives

\[
 X_R\equiv0,\qquad a_R\equiv a_R'\equiv0.
\]

This part is inherited from R0.74Q Step 1, Proposition 1.1 and Corollary 1.2,
with the source's explicit finite sum substituted.  The substitution and the
componentwise PDE identities were independently recomputed here.

## 2. Relaxed common calibration — PASS

The exact relations

\[
 D_\ell=\int_{R^2}^{65R^2}\theta_R(t,h_\ell)\,dt,
 \qquad
 B=\frac{q_*}{D_1},
 \qquad
 q_\ell=BD_\ell-q_*,
\]

and

\[
 q_{{\rm pre},\ell}
 =-q_*-B\int_0^{R^2}\theta_R(t,h_\ell)\,dt
\]

give, by direct integration,

\[
 Q_\ell(R^2)=-q_*,
 \qquad
 Q_\ell(65R^2)=q_\ell.
\]

The independently proved two-parameter saturation-platform lemma from
R0.74Q Step 1 yields

\[
 D_\ell=64R^2-\delta_\ell,
 \qquad
 0\le\delta_\ell\le256R^2e^{-a_DL_\ell^2}.
\]

Since \(L_\ell\ge L\), direct algebra gives, uniformly in \(N\) and
\(\ell\),

\[
 B=\frac1{128R^2}\bigl(1+O(e^{-a_DL^2})\bigr),
 \qquad q_1=0,
\]

\[
 \sup_{\ell\le N}|q_\ell|
 \le Ce^{-a_DL^2}.
\]

Using \(R=e^{-\rho L^2}\) and

\[
 a_D-\rho=\frac{211}{936000}>0
\]

then proves

\[
 \sup_{\ell\le N}\frac{|q_\ell|}{R}\longrightarrow0.
\]

No monotonicity or sign of \(D_R(h)\) is used or claimed.

The identity

\[
 L_N=\frac{16}{63}L^2
\]

was independently recomputed from \(N=j\).  Hence \(L_NR\to0\), so the
two-parameter platform hypotheses hold simultaneously for every packet after
one uniform increase of the base index.

## 3. Uniform bridge reuse — PASS with inherited analytic input

The all-winding stochastic representation, bridge conditioning, free
derivative-packet comparison, and single-packet positive-lobe theorem are
inherited from R0.74F.  This audit does not reprove those stochastic lemmas
from first principles.

Their parameter reuse is nevertheless valid.  In the \(\ell\)-th reference
frame the drift difference is exactly

\[
 B[\theta_R(t,h_\ell)-\theta_R(t,h_\ell+y)].
\]

The source family supplies, uniformly in \(\ell\),

\[
 B\lesssim R^{-2},
 \qquad L_\ell R\le L_NR\longrightarrow0,
 \qquad R^{-1}\ge L_N
\]

for all sufficiently large \(j\).  The R0.74F proof therefore gives the
uniform majorant

\[
 E_\ell\le\frac C R
 \left(e^{-a_DL_\ell^2}+e^{-a_SL_\ell^2}\right)
 +Ce^{-c/R^2}.
\]

Because \(L_\ell\ge L\) and

\[
 a_S-\rho=\frac{23}{112640}>0,
\]

the supremum over every packet tends to zero.  Thus one fixed \(c_0>0\)
and one base index work for every \(1\le\ell\le N\) on the common terminal
interval

\[
 J=(65R^2-R^3,65R^2).
\]

The stochastic theorem is inherited; the common-\(R\), growing-\(N\)
parameter closure and its exponent reserves were independently checked.

## 4. Terminal annular geometry — PASS

Let \(r_\ell=L_\ell R\) and \(k_\ell=j+\ell-1\).  Then

\[
 2^{k_\ell}R=\frac{r_\ell}{\lambda},
 \qquad
 2^{k_\ell+1}R=\frac{2r_\ell}{\lambda}.
\]

On the source lobe, the lower estimate is

\[
 |x|\ge|x_3|
 \ge r_\ell\left(c_h-\frac1{L_\ell}\right)
 >\frac{r_\ell}{\lambda}
\]

for one uniform base index.  The calibration and common-path estimates give
\(|x_2|\le2R\), while \(|x_1|<r_\ell/16\).  Therefore

\[
 \frac{|x|^2}{r_\ell^2}
 \le\frac1{256}
 +\left(c_h+\frac1{L_\ell}\right)^2
 +\frac4{L_\ell^2}.
\]

The right-hand side is largest at \(L_\ell=L\) and converges to

\[
 c_h^2+\frac1{256}
 =\frac{113}{128}
 <\left(\frac{64}{63}\right)^2.
\]

Hence both inversion-related lobes lie in \(A_{k_\ell}(R)\), uniformly in
\(N,\ell\), and the target indices are distinct.  Direct multiplication of
the three side lengths gives

\[
 |\Omega_{\ell,+}(t)|=\frac1{16}L_\ell R^3.
\]

All identities and inequalities in this section were independently
recomputed.

## 5. Simultaneous terminal clock lower bounds — PASS

For the smooth family, every terminal time is a local-energy good time and
the completed dissipation measure is \(|\nabla u^{(N)}|^2\,dx\,dt\).  On
\(J\), the frozen time cutoff satisfies \(\eta_R=1\).  The padded shell
cutoff satisfies

\[
 \Psi_{k_\ell}^R=1
 \quad\hbox{on }\Omega_{\ell,+}(\tau),
\]

because that lobe lies in \(A_{k_\ell}(R)\).  The dissipation part of the
clock is nonnegative.  The independently checked pointwise target dominance,
the lobe volume, and the terminal energy term therefore give

\[
\begin{aligned}
 K_{k_\ell,R}(\tau)
 &\ge\frac{\Gamma_\ell}{2R}
   \int_{\Omega_{\ell,+}(\tau)}|u^{(N)}(\tau,x)|^2\,dx\\
 &\ge c\Gamma_\ell\mathfrak a_\ell^2L_\ell R^2
 =c_KT.
\end{aligned}
\]

The last equality is the exact equal-target normalization

\[
 T=\Gamma_\ell\mathfrak a_\ell^2L_\ell R^2=A_*^2R^2.
\]

The constants are independent of \(j,N,\ell,A_*\).  Since the clocks start
at zero and are nonnegative,

\[
 v_{k_\ell,R}=\operatorname{Var}^+K_{k_\ell,R}
 \ge K_{k_\ell,R}(\tau).
\]

Thus the source correctly obtains only

\[
 Y_{2,R}^{\rm sf}\ge c_K\sqrt N\,T.
\]

It does not obtain a matching upper bound.  The clock definition and cutoff
properties are inherited from R0.74P; their application to the explicit lobe
geometry was independently checked.

## 6. Claim boundary — PASS

The audited source distinguishes the following correctly:

- exact finite-\(N\) PDE and geometry;
- inherited stochastic bridge input with a proved uniform parameter closure;
- simultaneous terminal clock lower bounds;
- the still-open all-shell square-function upper bound;
- the still-open signed cumulative-flux estimate.

In particular, terminal positivity of \(K_{k,R}\) is not promoted to a
positive signed-flux theorem.  The source does not claim an effective-shell
theorem for arbitrary suitable weak solutions, regularity, blow-up, or a
solution of the Millennium problem.

The conclusions audited here are restricted to the explicit smooth relaxed
common-shear family.  The signed-flux statement and the fixed-scale
inequality remain **OPEN**.  **NOT CLAY.**

## 7. Final verdict

```text
R074Q_RELAXED_GEOMETRY_INDEPENDENT_AUDIT_PASS
```

The exact PDE/common calibration, common-\(R\) bridge parameter closure,
annular geometry, terminal clock lower bound, and scope separation are
consistent with the bound source.  No claim in this audit upgrades an
inherited stochastic lemma or an open signed estimate to a new theorem.
