# R0.71G — Exact time ledgers reject sign-only residence but do not close a high-trace occupation theorem

**Date:** 2026-08-25

**Audience:** analysts working on three-dimensional incompressible
Navier--Stokes regularity, projected Lamb vectors, localized
Littlewood--Paley estimates, time--frequency occupation, and intermittent
high-frequency events

**Status:** exact smooth-solution evolution and moving-cutoff ledgers, exact
radial cancellation for the signed quotient, a denominator-zero defect, a
global-smooth 2D3C sign-residence no-go, critical relative-superlevel
profiles, a scale-sharpness lemma, a residence-only functional obstruction,
one conditional residence-plus-BV criterion, and two independent finite
certificates; no Leray-level occupation closure, no unconditional regularity
theorem, no singularity construction, no novelty theorem, and no
Millennium-problem claim

## 1. Direct decision

R0.71F showed that matched localization preserves the heat-height bulk of a
positive projected-Lamb quotient, while the physical bottom trace still pays
the critical frequency square.  R0.71G asks whether physical NSE time can pay
that square: must a large positive trace at frequency \(K\) leave its active
state after \(O((\nu K^2)^{-1})\)?

The answer depends on what “large” means.

1. At every fixed heat height, the projected Lamb vector has the exact
   evolution

   \[
    \partial_tL=\nu\Delta L
    -\mathbb P\bigl((L\cdot\nabla)u+(u\cdot\nabla)L\bigr)
    +2\nu\mathbb P\sum_m
      ((\partial_m u\cdot\nabla)\partial_m u).
    \tag{1.1}
   \]

   Its dyadic expansion retains every low--high, high--low, comparable, and
   high--high-to-low interaction.  No near-diagonal truncation is free.
2. For the local signed work \(B=\langle F,C\rangle\),
   \(C=\nabla\times(\chi W)\), and \(d=\|C\|_2^2\), the separate \(B_t\) ledger
   contains a positive \(\int\chi|\nabla\times F|^2\) term.  That sign does not
   survive normalization.  If

   \[
    E=C/\sqrt d,\qquad
    \beta=B/\sqrt d=\langle F,E\rangle,
   \]

   then, on \(d>0\),

   \[
    \boxed{
    \beta_t
    =\langle A\partial_tL,E\rangle
    +d^{-1/2}\langle P_{E^\perp}F,C_t\rangle.}
    \tag{1.2}
   \]

   The radial part of \(C_t\) cancels exactly.  Only Lamb acceleration and
   angular rotation remain, with no universal sign.
3. The convention \(q=(B^+)^2/d=0\) when \(d=0\) need not be continuous.
   A full time ledger must either use
   \(q_\varepsilon=(B^+)^2/(d+\varepsilon)\), or work on every connected
   component of \(\{d>0\}\) and retain all internal time faces.
4. Positivity alone is not a residence threshold.  A true global-smooth,
   zero-mean 2D3C NSE family with fixed initial kinetic energy has the
   following property: for every \(M<\infty\), some member has positive low
   projected-Lamb work for at least

   \[
    \frac{M}{\nu K^2}.
    \tag{1.3}
   \]

   Thus no solution-independent \(C(\nu,E_0)/(\nu K^2)\) bound exists for the
   initial connected component of the sign set.  The surviving trace can be
   exponentially small; this is not a blow-up mechanism.
5. Fixed positive relative superlevels behave differently.  In the weakly
   nonlinear limit of the same true NSE family,

   \[
    \frac{B(t)}{B(0)}\to e^{-4\theta},\qquad
    \frac{q(t)}{q(0)}\to e^{-6\theta},
    \qquad \theta=\nu K^2t.
    \tag{1.4}
   \]

   Their first relative exits therefore converge to fixed multiples of the
   viscous time.  A matched-partition aggregate also has a rigorous
   \(O((\nu K^2)^{-1})\) relative-superlevel envelope for this family.
   The witness rejects sign-only residence, not a properly normalized
   high-trace theorem.
6. NSE scaling makes \(K^{-2}\) critical.  A smooth whole-space covariant
   family rejects \(o(K^{-2})\) duration laws whose thresholds, filters, and
   geometry scale covariantly and whose constants are scaling invariant,
   while leaving \(CK^{-2}\) entirely possible.
7. Even a proved \(CK^{-2}\) duration for every episode would not by itself
   close the R0.71F bottom trace.  An exact disjoint-interval construction has
   one \(K_n^{-2}\)-long event per shell and a finite \(K_n^{-2}\)-weighted
   bulk, but an infinite unweighted bottom integral.
8. A valid conditional statement is available: critical residence plus a
   summable weighted-BV/crossing budget implies bottom-trace integrability.
   Equations (1.1)--(1.2) show why standard Leray energy does not provide that
   BV budget: it would have to control \(\partial_tL\), angular inter-shell
   rotation, moving cutoffs, collars, denominator faces, and \(Y_t/Y\).

The route decision is therefore precise.  The sign-only version is false.
The scale-critical normalized high-superlevel version remains logically
possible, but R0.71G does not derive it from standard NSE budgets.  Replacing
the missing estimate by an assumed occupation or weighted-BV condition would
be a conditional criterion, not a solution of the gap.

## 2. Setup and solution class

Work first on

\[
 \mathbb T^3=(\mathbb R/2\pi\mathbb Z)^3
\]

with normalized spatial average.  Let \(u\) be a zero-mean classical solution
on \(I=[t_-,t_+]\):

\[
 \partial_tu+u\cdot\nabla u+\nabla p=\nu\Delta u,
 \qquad \nabla\cdot u=0,
 \qquad \omega=\nabla\times u.
 \tag{2.1}
\]

The displayed derivative identities are used only in the classical regime.
For example,

\[
 u\in C(I;H^5)\cap C^1(I;H^3)
\]

is more than sufficient; no minimal regularity claim is made.  At Leray--Hopf
level one would first need finite-shell and space--time mollification and then
uniform control of the new source terms.  That limiting step is not claimed.

Set

\[
 L=\mathbb P(u\times\omega)
  =\partial_tu-\nu\Delta u
  =-\mathbb P((u\cdot\nabla)u).
 \tag{2.2}
\]

For a time-independent real-even Fourier multiplier \(T_j\) and heat height
\(s\ge0\), write

\[
 A=A_{j,s}=e^{s\Delta}T_j,qquad
 W=A\omega,qquad F=AL.
 \tag{2.3}
\]

Let \(\chi=\chi_{j,Q}(t,x)\) satisfy

\[
 \chi\in C_t^1C_x^\infty,qquad 0\le\chi\le1,
 \tag{2.4}
\]

with periodic support convention on the torus.  Define

\[
 C=\nabla\times(\chi W),\quad
 B=\langle F,C\rangle,
 \quad d=\|C\|_2^2,
 \quad q=\frac{(B^+)^2}{d},
 \tag{2.5}
\]

where the pointwise convention is \(q=0\) when \(d=0\).  Also put

\[
 Y(t)=\|\omega(t)\|_2^2,qquad a_{j,Q}=q/Y
 \tag{2.6}
\]

when \(Y>0\).  The zero solution is harmless and can be separated.

## 3. Exact projected-Lamb evolution and all-shell transfer

Since

\[
 u_t=L+\nu\Delta u,qquad
 \omega_t=\nabla\times L+\nu\Delta\omega,
 \tag{3.1}
\]

direct product differentiation gives

\[
 \boxed{
 (\partial_t-\nu\Delta)L
 =\mathbb P\left(
 L\times\omega+u\times\nabla\times L
 -2\nu\sum_m\partial_m u\times\partial_m\omega
 \right).}
 \tag{3.2}
\]

The vector identity

\[
 a\times\nabla\times b+b\times\nabla\times a
 =\nabla(a\cdot b)-(a\cdot\nabla)b-(b\cdot\nabla)a
 \tag{3.3}
\]

and

\[
 \mathbb P(a\times\nabla\times a)
 =-\mathbb P((a\cdot\nabla)a)
 \tag{3.4}
\]

turn (3.2) into (1.1).  The independent symbolic producer reconstructs both
forms from the full Fourier datum and verifies every output coefficient.

To expose inter-shell transfer, let \(S_k=T_k^*T_k\) be a tight resolution and
write

\[
 u_k=S_ku,qquad L_k=S_kL,qquad \omega_k=S_k\omega.
 \tag{3.5}
\]

Finite truncation followed by the smooth limit yields

\[
 \begin{aligned}
 A\mathcal H
 =\sum_{k,\ell}\biggl{
 &-A\mathbb P((L_k\cdot\nabla)u_\ell)
 -A\mathbb P((u_k\cdot\nabla)L_\ell)\\
 &+2\nu\sum_m
 A\mathbb P((\partial_m u_k\cdot\nabla)\partial_m u_\ell)
 \biggr\},
 \end{aligned}
 \tag{3.6}
\]

where \(L_t=\nu\Delta L+\mathcal H\).  Similarly,

\[
 \nabla\times F
 =\sum_{k,\ell}A\left(
 (\omega_k\cdot\nabla)u_\ell
 -(u_k\cdot\nabla)\omega_\ell
 \right).
 \tag{3.7}
\]

Equations (3.6)--(3.7) retain high--high-to-low transfer.  Discarding all
terms except \(k,\ell\simeq j\) would require a new estimate.

There is also an exact heat--time diagonal identity.  If

\[
 H_{j,s}=A\mathcal H,qquad D_\nu=\partial_t-\nu\partial_s,
 \tag{3.8}
\]

then

\[
 D_\nu W=\nabla\times F,qquad D_\nu F=H_{j,s}.
 \tag{3.9}
\]

For a cutoff independent of \(s\),

\[
 \boxed{
 D_\nu B
 =\langle H_{j,s},C\rangle
 +\int\chi|\nabla\times F|^2
 +\int\chi_tW\cdot\nabla\times F.}
 \tag{3.10}
\]

Along \(s(\tau)=\nu(t_1-\tau)\), this gives

\[
 B(t_1,0)-B(t_0,\nu(t_1-t_0))
 =\int_{t_0}^{t_1}
 (D_\nu B)(\tau,\nu(t_1-\tau))\,d\tau.
 \tag{3.11}
\]

This identity preserves both heat-height faces.  Its positive square is a
term in the unnormalized \(B\) ledger; Section 5 explains why it cannot be
transferred unchanged to \(q\).

## 4. Complete physical-time moving-cutoff ledger

At fixed \(s\), define

\[
 Z=\chi_tW+\chi\nabla\times F+\nu\chi\Delta W.
 \tag{4.1}
\]

Then

\[
 C_t=\nabla\times Z,
 \tag{4.2}
\]

and direct differentiation gives

\[
 \boxed{
 \begin{aligned}
 B_t={}&\langle A\partial_tL,C\rangle
 +\int\chi|\nabla\times F|^2
 +\int\chi_tW\cdot\nabla\times F\\
 &+\nu\int\chi\Delta W\cdot\nabla\times F,
 \end{aligned}}
 \tag{4.3}
\]

\[
 \boxed{d_t=2\langle C,\nabla\times Z\rangle.}
 \tag{4.4}
\]

To separate viscous bulk from the cutoff collar, put

\[
 \mathcal K_\chi W
 =2\sum_m(\partial_m\chi)\partial_mW+(\Delta\chi)W.
 \tag{4.5}
\]

Since \(\chi\Delta W=\Delta(\chi W)-\mathcal K_\chi W\),

\[
 \begin{aligned}
 C_t={}&\nu\Delta C
 +\nabla\times\left(
 \chi\nabla\times F+\chi_tW-\nu\mathcal K_\chi W
 \right),
 \tag{4.6}
 \end{aligned}
\]

and

\[
 \begin{aligned}
 d_t={}&-2\nu\|\nabla C\|_2^2
 +2\langle C,\nabla\times(\chi\nabla\times F)\rangle\\
 &+2\langle C,\nabla\times(\chi_tW-\nu\mathcal K_\chi W)\rangle.
 \tag{4.7}
\end{aligned}
\]

Substituting \(L_t=\nu\Delta L+\mathcal H\) into (4.3) gives the fully
separated form

\[
 \begin{aligned}
 B_t={}&2\nu\langle\Delta F,C\rangle
 +\langle A\mathcal H,C\rangle
 +\int\chi|\nabla\times F|^2\\
 &+\int\chi_tW\cdot\nabla\times F
 -\nu\langle F,\nabla\times\mathcal K_\chi W\rangle.
 \tag{4.8}
\end{aligned}
\]

For a mollified transport velocity \(V_r\), let

\[
 R=(\partial_t+V_r\cdot\nabla)\chi.
 \tag{4.9}
\]

Then \(\chi_t=R-V_r\cdot\nabla\chi\).  A perfectly flow-transported cutoff
has \(R=0\), but its Eulerian \(\chi_t=-V_r\cdot\nabla\chi\) remains in
(4.3)--(4.8).  It disappears only after conversion to the corresponding
material representation; it cannot be deleted in both ledgers.

## 5. The normalized quotient removes the apparent positive production

Assume \(d>0\) and define

\[
 E=C/\sqrt d,qquad
 \beta=B/\sqrt d=\langle F,E\rangle,qquad
 q=(\beta^+)^2.
 \tag{5.1}
\]

Because

\[
 E_t=\frac{P_{E^\perp}C_t}{\sqrt d},
 \tag{5.2}
\]

the exact derivative is (1.2), or equivalently

\[
 \boxed{
 q_t=2\beta^+\left[
 \langle A\partial_tL,E\rangle
 +d^{-1/2}\langle P_{E^\perp}F,\nabla\times Z\rangle
 \right].}
 \tag{5.3}
\]

The direct quotient form is

\[
 q_t=\frac{2B^+B_t}{d}-\frac{(B^+)^2d_t}{d^2}.
 \tag{5.4}
\]

Equation (5.2) is the decisive cancellation: radial growth of \(C\) changes
\(B\) and \(d\) in the same direction and vanishes from \(\beta_t\).  In
particular, the positive square in (4.3) cannot be treated as a standalone
favorable production term for \(q\).

The zero-denominator convention has a separate defect.  Take, in a Hilbert
space,

\[
 C(t)=tc,qquad F(t)=f,qquad \langle f,c\rangle>0.
 \tag{5.5}
\]

For \(t>0\),

\[
 q(t)=\frac{\langle f,c\rangle^2}{\|c\|^2},
 \tag{5.6}
\]

while the convention sets \(q(0)=0\).  Thus \(q\) need not be continuous or
absolutely continuous across \(d=0\).

A global-in-time identity may instead use

\[
 q_\varepsilon=\frac{(B^+)^2}{d+\varepsilon},
 \tag{5.7}
\]

for which

\[
 (q_\varepsilon)_t
 =\frac{2B^+B_t}{d+\varepsilon}
 -\frac{(B^+)^2d_t}{(d+\varepsilon)^2}.
 \tag{5.8}
\]

For every \(\eta\in C^1([a,b])\), the exact time face is

\[
 [\eta q_\varepsilon]_a^b
 =\int_a^b\eta' q_\varepsilon\,dt
 +\int_a^b\eta(q_\varepsilon)_t\,dt.
 \tag{5.9}
\]

If \(q\) is used directly, (5.3)--(5.4) apply separately on every connected
component of \(\{d>0\}\), and all endpoint contributions at internal faces
must remain.  Refreshing a spatial partition does not cancel these nonlinear
faces even when the linear \(B_Q\) terms reconstruct exactly.

The normalized coefficient adds another term.  Since

\[
 Y_t=2\langle\omega,\nabla\times L\rangle
 -2\nu\|\nabla\omega\|_2^2,
 \tag{5.10}
\]

\[
 \left(\frac{q_\varepsilon}{Y}\right)_t
 =\frac{(q_\varepsilon)_t}{Y}
 -\frac{q_\varepsilon}{Y}\frac{Y_t}{Y}.
 \tag{5.11}
\]

Using \(Y_t/Y\) as a free coefficient would reinsert the enstrophy-growth
quantity that a continuation argument is meant to control.

## 6. A true NSE no-go for sign-only residence

### 6.1 Exact global-smooth 2D3C family

For \(a>0\) and integer \(K\ge1\), take

\[
 u_0(x)=\left(
 0,
 -2aK\cos(Kx_1),
 -2aK\sin(Kx_1+Kx_2)-2aK\cos(Kx_2)
 \right).
 \tag{6.1}
\]

It is zero mean and divergence free.  The horizontal velocity is a decaying
two-dimensional shear, and the vertical component is a passive scalar.
Therefore the resulting three-dimensional NSE solution is global and smooth.
Set

\[
 \theta=\nu K^2t,qquad \mu=a/\nu,qquad
 X=Kx_1,\quad Y=Kx_2.
 \tag{6.2}
\]

Then

\[
 u_2=-2aKe^{-\theta}\cos X,qquad
 u_3=aKZ_\mu(\theta,X,Y),
 \tag{6.3}
\]

where

\[
 \partial_\theta Z_\mu
 -2\mu e^{-\theta}\cos X\,\partial_YZ_\mu
 =\Delta_{X,Y}Z_\mu.
 \tag{6.4}
\]

Write the positive \(Y\)-frequency sector as

\[
 Z_\mu=\sum_{m\in\mathbb Z}c_m(\theta)e^{i(mX+Y)}
 +\text{complex conjugate}.
 \tag{6.5}
\]

The exact infinite sideband chain is

\[
 c_m'=-(m^2+1)c_m
 +i\mu e^{-\theta}(c_{m-1}+c_{m+1}),
 \tag{6.6}
\]

with

\[
 c_0(0)=-1,qquad c_1(0)=i,qquad c_m(0)=0
 \quad(m\ne0,1).
 \tag{6.7}
\]

The solution does not remain six-mode for \(t>0\).  Equation (6.6), rather
than a frozen modal ansatz, is the exact dynamics.

The phase class is invariant.  More precisely,

\[
 c_m=i^m x_m,\qquad x_m\in\mathbb R,
\]

and uniqueness for (6.6) reduces the chain to

\[
 x_m'=-(m^2+1)x_m
 +\mu e^{-\theta}(x_{m-1}-x_{m+1}).
 \tag{6.7a}
\]

In particular, both \(c_0\) and \(\ell_\mu\) below are real.  This phase
fact is what turns the Fourier reconstruction into the signed local-density
formula used in (6.14).

Define

\[
 \ell_\mu=i e^{-\theta}(c_{-1}+c_1),qquad
 H_\mu=\operatorname{Re}(\overline{c_0}\ell_\mu),
 \tag{6.8}
\]

\[
 G_\mu=|c_0|^2+e^{-2\theta},qquad
 \mathcal E_\mu=e^{-2\theta}
 +\sum_m(m^2+1)|c_m|^2.
 \tag{6.9}
\]

For the fixed low sphere \(|k|=K\), exact reconstruction gives

\[
 B_{\rm lo}=2a^3K^6H_\mu,qquad
 d_{\rm lo}=2a^2K^6G_\mu,
 \tag{6.10}
\]

\[
 q_{\rm lo}
 =2a^4K^6\frac{(H_\mu^+)^2}{G_\mu},
 \qquad
 Y=2a^2K^4\mathcal E_\mu,
 \tag{6.11}
\]

\[
 A_{\rm lo}:=\frac{q_{\rm lo}}Y
 =a^2K^2\frac{(H_\mu^+)^2}{G_\mu\mathcal E_\mu}.
 \tag{6.12}
\]

At \(t=0\), \(H=1\), \(G=2\), and \(\mathcal E=4\), so

\[
 B_{\rm lo}=2a^3K^6,\quad
 q_{\rm lo}=a^4K^6,\quad
 A_{\rm lo}=a^2K^2/8.
 \tag{6.13}
\]

At every fixed time for which \(\chi(t,\cdot)\ge0\) and
\(\chi(t,\cdot)\not\equiv0\), curl integration by parts gives the localized
work

\[
 B_\chi(t)
 =4a^3K^6H_\mu(\theta)
 \int_{\mathbb T^3}\chi(t,x)\sin^2(Kx_2)\,dx.
 \tag{6.14}
\]

Thus \(H_\mu>0\) forces positive work for every such cutoff, including
\(\chi\equiv1\).

### 6.2 Explicit arbitrary-duration estimate

The coupling operator

\[
 i\mu e^{-\theta}(S+S^{-1})
 \tag{6.15}
\]

is skew-adjoint on \(\ell^2(\mathbb Z)\).  Since the diagonal in (6.6) is at
most \(-1\),

\[
 \|c_\mu(\theta)\|_{\ell^2}
 \le\sqrt2e^{-\theta}.
 \tag{6.16}
\]

Duhamel's formula and \(\|S+S^{-1}\|\le2\) give

\[
 \|c_\mu(\theta)-c_0(\theta)\|_{\ell^2}
 \le2\sqrt2\mu e^{-\theta}(1-e^{-\theta}).
 \tag{6.17}
\]

The reduced coefficient system extends analytically to \(\mu=0\), where

\[
 H_0(\theta)=e^{-4\theta}>0.
 \tag{6.18}
\]

The elementary product estimate following from (6.17) is

\[
 |H_\mu(\theta)-H_0(\theta)|
 \le(4+4\sqrt2)\mu.
 \tag{6.19}
\]

Hence, for any \(M<\infty\),

\[
 0<\mu<
 \frac{e^{-4M}}{2(4+4\sqrt2)}
 \tag{6.20}
\]

implies

\[
 H_\mu(\theta)\ge\frac12e^{-4M}>0
 \qquad(0\le\theta\le M).
 \tag{6.21}
\]

Now choose the fixed-energy sequence

\[
 a=K^{-1},qquad \|u_0\|_2^2=6,qquad
 \mu=(\nu K)^{-1}.
 \tag{6.22}
\]

For any prescribed \(M\), a sufficiently large integer \(K\) satisfies
(6.20).  Equations (6.14) and (6.21) prove positive local work throughout

\[
 0\le t\le\frac{M}{\nu K^2}.
 \tag{6.23}
\]

Because \(M\) is arbitrary while the initial kinetic energy and viscosity are
fixed, no universal finite viscous-time constant can bound sign-only
residence.  This statement concerns a very small positive tail of a
global-smooth solution; it neither constructs nor suggests a singularity.

### 6.3 Fixed positive relative levels retain viscous scaling

At the analytically extended coefficient value \(\mu=0\),

\[
 H_0=e^{-4\theta},\qquad
 G_0=2e^{-2\theta},\qquad
 \mathcal E_0=2e^{-2\theta}+2e^{-4\theta}.
 \tag{6.24}
\]

Therefore, for the physical family with \(\mu>0\), after division by its
nonzero initial amplitudes,

\[
 \lim_{\mu\downarrow0}
 \frac{B_{{\rm lo},\mu}(t)}
      {B_{{\rm lo},\mu}(0)}
 =e^{-4\theta},\qquad
 \lim_{\mu\downarrow0}
 \frac{q_{{\rm lo},\mu}(t)}
      {q_{{\rm lo},\mu}(0)}
 =e^{-6\theta},
 \tag{6.25}
\]

and

\[
 \lim_{\mu\downarrow0}
 \frac{A_{{\rm lo},\mu}(t)}
      {A_{{\rm lo},\mu}(0)}
 =\frac{2e^{-4\theta}}{1+e^{-2\theta}}.
 \tag{6.26}
\]

For a fixed \(0<\rho<1\), analytic dependence on \(\mu\) and the transverse
crossings in (6.25)--(6.26) give the first-exit limits

\[
 \theta_{B,\mu}(\rho)\longrightarrow\frac14\log(1/\rho),
 \tag{6.27}
\]

\[
 \theta_{q,\mu}(\rho)\longrightarrow\frac16\log(1/\rho),
 \tag{6.28}
\]

and

\[
 \theta_{A,\mu}(\rho)\longrightarrow-\frac12\log z_\rho,\qquad
 z_\rho=\frac{\rho+\sqrt{\rho^2+8\rho}}4.
 \tag{6.29}
\]

In all three arrows \(\mu\downarrow0\).  The corresponding physical times
are fixed multiples of \((\nu K^2)^{-1}\).

There is also a matched-aggregate envelope valid for every \(\mu>0\).  Let

\[
 Q_K(t)=\sum_Qq_Q(t,0)
 \tag{6.30}
\]

for the R0.71F matched partition.  Assume

\[
 \phi_Q\ge0,\qquad
 \sum_Q\phi_Q=1,\qquad
 \sum_Q\mathbf1_{\operatorname{supp}\phi_Q}\le N,
 \tag{6.30a}
\]

and

\[
 \sum_Q\phi_Q^2\le C_0,qquad
 \sum_Q|\nabla\phi_Q|^2\le C_1r^{-2},qquad r=\rho_0/K.
 \tag{6.31}
\]

The passive-scalar energy identity and its fixed \(Y\)-frequency imply

\[
 \|u_3(t)\|_2^2\le4a^2K^2e^{-2\theta},qquad
 \|L(t)\|_2^2\le16a^4K^6e^{-4\theta}.
 \tag{6.32}
\]

Local Cauchy and bounded overlap give

\[
 Q_K(t)\le16Na^4K^6e^{-4\theta}.
 \tag{6.33}
\]

R0.71F gives the initial lower bound

\[
 Q_K(0)\ge
 \frac{a^4K^6}{2(C_0+C_1/\rho_0^2)}.
 \tag{6.34}
\]

Consequently,

\[
 Q_K(t)\ge\rho Q_K(0)
 \Longrightarrow
 t\le\frac1{4\nu K^2}
 \log\frac{32N(C_0+C_1/\rho_0^2)}\rho.
 \tag{6.35}
\]

The horizontal shear alone gives

\[
 Y(t)\ge2a^2K^4e^{-2\theta}.
 \tag{6.36}
\]

Thus \(\mathcal A_K=Q_K/Y\) satisfies

\[
 \mathcal A_K(t)\le8Na^2K^2e^{-2\theta},
 \qquad
 \mathcal A_K(0)\ge
 \frac{a^2K^2}{16(C_0+C_1/\rho_0^2)},
 \tag{6.37}
\]

and

\[
 \mathcal A_K(t)\ge\rho\mathcal A_K(0)
 \Longrightarrow
 t\le\frac1{2\nu K^2}
 \log\frac{128N(C_0+C_1/\rho_0^2)}\rho.
 \tag{6.38}
\]

These bounds use the initial \(t=0\) envelope.  They cannot be reset at an
arbitrary later time without a nondegeneracy hypothesis: near a sign crossing,
the new reference value can be arbitrarily small and a later positive lobe can
turn a “relative” level back into a sign-only test.

## 7. Scale-critical sharpness

On \(\mathbb R^3\), use the covariant NSE scaling

\[
 u_\lambda(t,x)=\lambda u(\lambda^2t,\lambda x),qquad
 \chi_\lambda(t,x)=\chi(\lambda^2t,\lambda x),
 \tag{7.1}
\]

with filter, radius, and heat height scaled together.  Then

\[
 W_\lambda\sim\lambda^2,qquad
 F_\lambda\sim\lambda^3,qquad
 C_\lambda\sim\lambda^3,
 \tag{7.2}
\]

and after spatial integration

\[
 B_\lambda,d_\lambda,q_\lambda\sim\lambda^3,qquad
 Y_\lambda\sim\lambda,qquad
 a_\lambda=q_\lambda/Y_\lambda\sim\lambda^2.
 \tag{7.3}
\]

Every complete term in the time-derivative ledgers (4.3), (4.4), and
(4.6)--(4.8) scales like \(\lambda^5\), while
\(\mathcal K_\chi W\sim\lambda^4\) before the outer curl and
\(dt\sim\lambda^{-2}\).  Hence, if a smooth base solution has

\[
 a(t)>\alpha>0
 \]

on an interior interval, its scaled copy satisfies

\[
 |\{t:a_\lambda(t)>\lambda^2\alpha\}|
 =\lambda^{-2}|\{\tau:a(\tau)>\alpha\}|.
 \tag{7.4}
\]

Consequently, a duration law with covariantly scaled threshold, filter,
radius, heat height, and geometry, with a scaling-invariant constant and an
\(o(K^{-2})\) right-hand side, is false on such a smooth family.  This
argument does not exclude constants that depend on non-scale-invariant
quantities.  The critical \(CK^{-2}\) law is saturated, not rejected.

## 8. Critical residence alone does not close the bottom trace

Let

\[
 K_n=2^n,\qquad n\ge1
 \]

and choose pairwise disjoint intervals \(I_n\subset[0,1]\) with

\[
 |I_n|=K_n^{-2}.
 \tag{8.1}
\]

Set

\[
 A_n(t)=K_n^2\mathbf1_{I_n}(t).
 \tag{8.2}
\]

Every episode has exactly critical residence and at most one shell is active
at each time.  Nevertheless,

\[
 \sum_{n\ge1}K_n^{-2}\int_0^1A_n(t)\,dt
 =\sum_{n\ge1}K_n^{-2}<\infty,
 \tag{8.3}
\]

whereas

\[
 \sum_{n\ge1}\int_0^1A_n(t)\,dt
 =\sum_{n\ge1}1=\infty.
 \tag{8.4}
\]

Smooth bumps give the same conclusion.  Thus the R0.71F
\(K^{-2}\)-weighted heat bulk plus a \(K^{-2}\) upper bound on each residence
episode does not imply the unweighted bottom-trace sum.  Amplitude, number of
crossings, or a frequency envelope must also be summable.

## 9. A valid conditional residence-plus-BV criterion

Let \(a:I\to[0,\infty)\) be continuous and of bounded variation.  Suppose
that for almost every \(\lambda>0\), every connected component of

\[
 \{t\in I:a(t)>\lambda\}
 \]

has length at most \(CK^{-2}\).  Extend \(a\) by zero outside \(I\).  One-
dimensional coarea gives

\[
 2\int_0^\infty N_a(\lambda)\,d\lambda
 =\operatorname{TV}_I(a)+a(t_-)+a(t_+),
 \tag{9.1}
\]

where \(N_a(\lambda)\) is the number of superlevel components.  Layer cake
then yields

\[
 \boxed{
 \int_Ia(t)\,dt
 \le\frac C2K^{-2}
 \left[
 \operatorname{TV}_I(a)+a(t_-)+a(t_+)
 \right].}
 \tag{9.2}
\]

For the application, set
\(a_{j,Q,\varepsilon}=q_{j,Q,\varepsilon}/Y\).  Assume that one constant
\(C\) works for every \(j,Q\), and \(0<\varepsilon\le1\), and that for
almost every \(\lambda>0\), every connected component of
\[
 \{t\in I:a_{j,Q,\varepsilon}(t)>\lambda\}
\]
has length at most \(CK_j^{-2}\).  The lemma gives a conditional continuation
route if, in addition,

\[
 \sup_{0<\varepsilon\le1}\sum_{j,Q}K_j^{-2}
 \left[
 \operatorname{TV}_I(a_{j,Q,\varepsilon})
 +a_{j,Q,\varepsilon}(t_-)
 +a_{j,Q,\varepsilon}(t_+)
 \right]<\infty
 \tag{9.3}
\]

with any zero-denominator defect faces retained in the
\(\varepsilon\downarrow0\) limit.  This is a genuine theorem, but (9.3) is an additional
weighted-BV/crossing hypothesis.  It is not supplied by the residence bound
alone.

## 10. Why Leray energy does not supply the missing BV budget

Equation (5.3) exposes the required quantities.  A differential-damping
attempt of the form

\[
 q_t+c\nu K^2q\le R
 \tag{10.1}
\]

encounters a source \(2\sqrt q\,\|A\partial_tL\|_2\).  Young's inequality at
the viscous scale asks for

\[
 (\nu K^2)^{-1}\|T_j\partial_tL\|_2^2.
 \tag{10.2}
\]

This is the unnormalized \(q\) target.  For the coefficient
\(a=q_\varepsilon/Y\) used in Section 9, the same source contains an
additional \(Y^{-1/2}\).  After the outer \(K^{-2}\) BV weight, the
corresponding source-curvature budget is, up to viscosity constants,
\[
 K^{-4}\frac{\|T_j\partial_tL\|_2^2}{Y}.
 \tag{10.2a}
\]
The angular term in (5.3) similarly carries \(Y^{-1}\); before the BV
weight it naturally contains \(K^2\|F_j\|_2^2/Y\), together with a
direction/denominator ratio.  The normalized route also retains
moving-cutoff and collar terms.

By contrast, the R0.71F energy endpoint controls the heat-bulk scale

\[
 K^{-2}\frac{\|F_j\|_2^2}{Y}
 \tag{10.3}
\]

after the appropriate summations.  It does not control \(\|L\|_2^2\), much
less (10.2), \(K^2\|F_j\|_2^2\), or the angular denominator.  The standard
Leray bounds are only

\[
 u\in L_t^\infty L_x^2\cap L_t^2H_x^1.
 \tag{10.4}
\]

Even a coarse negative-Sobolev estimate for \(\mathcal H\) introduces terms
such as \(\|u\|_\infty\|L\|_2\) and
\(\nu\|\nabla u\|_4^2\), already on the stronger side of known
Serrin/Besov-type controls.  Finally, (5.11) requires \(Y_t/Y\), which is part
of the continuation problem itself.

The missing object is therefore not “more algebra.”  It is a propagated
angular/source-curvature budget that is stronger than (10.3) yet not merely a
known regularity criterion in disguise.

## 11. Exact initial physical-time audit

The full six-mode datum in (6.1), evaluated at the true NSE initial time, gives

\[
 B=2a^3K^6,qquad
 d=4a^2K^6,qquad
 q=a^4K^6,qquad
 Y=8a^2K^4.
 \tag{11.1}
\]

The exact derivatives are

\[
 B_t=-2a^3(a+4\nu)K^8,qquad
 d_t=4a^2(a-2\nu)K^8,
 \tag{11.2}
\]

\[
 q_t=-3a^4(a+2\nu)K^8,qquad
 Y_t=-4a^2(a+6\nu)K^6.
 \tag{11.3}
\]

Consequently,

\[
 \boxed{
 \frac{\partial_t(q/Y)}{q/Y}
 =-\frac{5a+6\nu}{2}K^2.}
 \tag{11.4}
\]

This true-solution initial derivative is exactly on the critical viscous time
scale.  It supports scale sharpness but proves no general occupation bound.
The symbolic Fourier producer and an independent FFT reconstruction agree on
all displayed identities in (11.1)--(11.4).  The ten scalar certificate
entries are \(B,d,q,Y,q/Y,B_t,d_t,q_t,Y_t\), and
\(\partial_t(q/Y)\).

The independent sideband checker also integrates (6.6) at two truncation
radii.  For \(\mu\in\{1,0.5,0.2,0.1,0.05\}\), the first dimensionless sign exits are
approximately

\[
 0.433500867,\quad
 0.893739511,\quad
 2.334768638,\quad
 4.798940448,\quad
 9.776250058.
 \tag{11.5}
\]

The two radii agree to better than \(4\times10^{-14}\) on these events, and
the checked chain energy identity has residual below \(2\times10^{-15}\).
These are finite floating-point checks.  The arbitrary-\(M\) theorem rests on
(6.16)--(6.21), not on extrapolating (11.5).

## 12. Relation to published criteria

Cheskidov--Shvydkoy prove that every Leray--Hopf solution has dynamic
dissipation wavenumber \(\Lambda\in L_t^1\), while stronger low-mode or
\(\Lambda\in L_t^{5/2}\) conditions imply regularity.  Chebyshev applied only
to the unconditional \(L^1\) bound yields a \(K^{-1}\) active-frequency tail,
one frequency power short of the desired \(K^{-2}\) scale.  Their observable
is not signed Lamb work, so this is a baseline comparison rather than a
counterexample.

Cheskidov--Dai give the closest explicit time--frequency occupation formula:
an indicator that a shell lies below the dynamic dissipation cutoff multiplies
the shell-vorticity amplitude in a time integral.  Its smallness is a
regularity hypothesis, not an energy consequence.

Gibbon--Doering prove genuine good/bad-interval width estimates for global
higher-derivative ratios and Reynolds-number parameters.  Miller proves a
scale-critical criterion involving only the positive middle strain
eigenvalue.  Yu gives a conditional filtered-stretching closure under far
field, commutator, and remaining-shell summability.  These are important
neighbors, but none supplies (9.3) or a standard-budget derivation of the
R0.71G signed occupation.

The bounded primary-source audit found no exact theorem collision for the
complete ledger (3.2)--(5.11) plus the 2D3C sign-residence no-go.  That bounded
finding is not a claim of originality, priority, or global literature
nonexistence.

## 13. Route decision and next gate

R0.71G closes three questions.

1. “Positive for how long?” is not a valid high-trace question: positivity
   can persist for arbitrarily many viscous times on a fixed-energy,
   global-smooth family.
2. A fixed positive relative level is scale compatible with \(K^{-2}\), and
   the exact witness saturates that scale rather than rejecting it.
3. Critical residence alone cannot convert the R0.71F heat bulk into the
   bottom trace; weighted variation or crossing information is also needed.

The next justified gate is R0.71H: test whether the angular term in (5.3) has
a non-circular depletion estimate.  The test must retain all inter-shell
pairs, moving-cutoff and collar terms, zero-denominator faces, and
normalization by \(Y\).  If the required estimate reduces to Serrin/Besov,
Cheskidov--Dai occupation, or an assumed weighted-BV sum, the temporal-
residence branch must stop rather than relabel that assumption as a derived
budget.
