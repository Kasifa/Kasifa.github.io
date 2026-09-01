# R0.73X — exterior-tail freeze for the localized heat ledger

**Frozen date:** 2026-09-01

**Status:** `EXACT_DECOMPOSITIONS + STANDARD_TAIL_LEMMAS + OPEN_ABSORPTION`

**Claim class:** smooth exact; suitable-weak positive-scale; no regularity
criterion

**Domain:** the normalized torus \(\mathbb T^3=(\mathbb R/2\pi\mathbb Z)^3\)

**Ordinary translation path:** `LOCAL_DIRECT_NO_DGX`

**DGX used:** `false`

This note fills one deliberately missing object in the R0.73X problem
freeze: a scale-invariant exterior functional which pays both for the
noncompact Gaussian filter and for the algebraically decaying harmonic
pressure created outside the local ball.  The two tails have different
decay laws and are therefore kept as two separate rows.

The main frozen candidate is

\[
 \boxed{
 \mathcal A_{\rm ext}^{\square}(z_0,R;\theta)
 =\mathcal G_{u,p}^{\square}(z_0,R;\theta)
  +\mathcal H_u^{\square}(z_0,R),
 \qquad \square\in\{{\rm std},\nu\}.}
\tag{0.1}
\]

Here \(\mathcal G_{u,p}\) is an exponentially weighted Gaussian-annulus
payment, while \(\mathcal H_u\) is an algebraically weighted harmonic
pressure payment.  Precise definitions appear in (3.3) and (4.9).

The result frozen below is a **tail-complete size lemma**, not an
epsilon-regularity estimate.  In particular, no claim is made that
\(\mathcal A_{\rm ext}\) is small or controlled by data on one smaller
cylinder.

---

## 1. Torus, Euclidean lift, and the two cylinder clocks

Let \(\pi:\mathbb R^3\to\mathbb T^3\) be the quotient map.  Fix a lift
\(\widetilde x_0\in\mathbb R^3\) of \(x_0\), and lift every periodic field
by

\[
 \widetilde f(t,y)=f(t,\pi y).
\tag{1.1}
\]

Throughout,

\[
 0<R<\frac{\pi}{8}.
\tag{1.2}
\]

Thus all balls through \(B_{4R}(\widetilde x_0)\) lie inside a fixed
Euclidean chart.  We write \(B_{aR}\) for the Euclidean ball centered at
\(\widetilde x_0\), and identify it with its torus image whenever
\(a\le4\).

The standard Navier--Stokes cylinder and the viscosity-adapted
heat-characteristic cylinder are, respectively,

\[
 \begin{aligned}
 I_R^{\rm std}&=(t_0-R^2,t_0),
 &Q_R(z_0)&=I_R^{\rm std}\times B_R,\\
 I_R^{\nu}&=(t_0-R^2/\nu,t_0),
 &Q_R^\nu(z_0)&=I_R^{\nu}\times B_R.
 \end{aligned}
\tag{1.3}
\]

We use \(I_R^\square\) and \(Q_R^\square\) when the statement is valid
for either clock.  The normalization is always by powers of the spatial
radius \(R\).  Since viscosity is unchanged by Navier--Stokes scaling, both
clocks scale parabolically.  They coincide only when \(\nu=1\); no formula
below silently replaces one by the other.
For a descending characteristic \(s'(t)=-\nu\), the time depth
\(R^2/\nu\) in \(Q_R^\nu\) changes the heat coordinate by exactly \(R^2\).
The standard cylinder \(Q_R\) is retained for comparison with CKN-scale
quantities and with the tent cylinder in the R0.73X problem freeze.

For the normalized Euclidean Gaussian

\[
 g_s(z)=(4\pi s)^{-3/2}e^{-|z|^2/(4s)},
\tag{1.4}
\]

the periodic heat flow has the exact lift representation

\[
 P_sf(x)
 =\int_{\mathbb R^3}g_s(\widetilde x-y)\widetilde f(y)\,dy
 =\int_{[0,2\pi]^3}g_s^{\rm per}(x-y)f(y)\,dy.
\tag{1.5}
\]

Thus an integral over \(\mathbb R^3\) below is not a change of problem: it
is exactly the periodic heat kernel written as a sum over lattice copies.

Fix once and for all

\[
 0<\theta\le1,
 \qquad 0<s\le\theta R^2.
\tag{1.6}
\]

No positive lower bound for \(s/R^2\) is needed for the exterior estimates.
A lower bound remains necessary for the distributional pullback of the full
suitable-weak identity, as recorded in the localized heat-characteristic
note.

For every suitable-weak size statement below, the common quantifiers are

\[
 \nu>0,\qquad I_{4R}^{\square}\Subset(0,T),\qquad
 \square\in\{{\rm std},\nu\},
\tag{1.7}
\]

and \((u,p)\) is a periodic suitable weak solution on
\(\mathbb T^3\times(0,T)\) with

\[
 u\in L_t^\infty L_x^2\cap L_t^2H_x^1,
 \qquad p\in L_{t,x}^{3/2}.
\tag{1.8}
\]

Fixed-time pressure formulas are asserted for almost every
\(t\in I_{4R}^{\square}\).  Characteristic-size statements quantify over

\[
 s:I_R^{\square}\to(0,\theta R^2]
 \quad\hbox{measurable a.e.},
 \qquad
 \eta_R\in W_0^{1,\infty}(B_R),
 \quad \|\nabla\eta_R\|_\infty\le C_\eta/R.
\tag{1.9}
\]

Their constants may depend on the fixed cutoff constant \(C_\eta\), in
addition to the explicitly displayed \(\theta\) and \(\nu\) dependence.

---

## 2. Exact heat-annulus decomposition and a uniform kernel weight

Define the lifted dyadic annuli

\[
 A_m(R)=
 \left\{y\in\mathbb R^3:
 2^mR\le |y-\widetilde x_0|<2^{m+1}R\right\},
 \qquad m\ge1,
\tag{2.1}
\]

Set

\[
 C_R=B_{2R},\qquad E_R=\mathbb R^3\setminus C_R.
\tag{2.1a}
\]

and the Gaussian weight

\[
 \gamma_m(\theta)
 =\theta^{-2}
   \exp\!\left(-\frac{4^{m-1}}{32\theta}\right).
\tag{2.2}
\]

For any periodic \(f\) for which the displayed integrals exist, set

\[
 \begin{aligned}
 P_s^{\rm core}f(x)
 &=\int_{B_{2R}}g_s(\widetilde x-y)\widetilde f(y)\,dy,\\
 P_s^{(m)}f(x)
 &=\int_{A_m(R)}g_s(\widetilde x-y)\widetilde f(y)\,dy.
 \end{aligned}
\tag{2.3}
\]

Up to null boundaries, \(B_{2R}\) and the annuli \(A_m(R)\) partition
\(\mathbb R^3\).  Hence

\[
 \boxed{P_sf=P_s^{\rm core}f+\sum_{m=1}^{\infty}P_s^{(m)}f.}
\tag{2.4}
\]

Equation (2.4) is an exact decomposition, not an estimate or an asymptotic
expansion.

### Lemma 2.1 — Gaussian annulus bound

For \(x\in B_R\), \(y\in A_m(R)\), and
\(0<s\le\theta R^2\),

\[
 \boxed{
 R^3g_s(\widetilde x-y)
 +R^4|\nabla g_s(\widetilde x-y)|
 \le C\,\gamma_m(\theta),}
\tag{2.5}
\]

where \(C\) is numerical and independent of \(m,R,s,z_0\).

Indeed, \(|\widetilde x-y|\ge2^{m-1}R\), while the standard Gaussian
derivative bound gives

\[
 |\nabla^qg_s(z)|
 \le C_qs^{-(3+q)/2}e^{-|z|^2/(8s)},
 \qquad q=0,1.
\tag{2.6}
\]

Writing \(r=R^2/s\ge\theta^{-1}\), the dimensionless right side before
the last estimate is bounded by

\[
 C r^2\exp\!\left(-\frac{4^{m-1}}8r\right).
\tag{2.7}
\]

Absorbing half of the exponential controls the polynomial \(r^2\) and
gives (2.5), with room to spare in the denominator \(32\theta\).  In
particular,

\[
 \sum_{m\ge1}2^{3m}\gamma_m(\theta)<\infty.
\tag{2.8}
\]

The factor \(2^{3m}\) in (2.8) is important because the periodic lift has
order \(2^{3m}\) fundamental cells in its \(m\)-th annulus.

---

## 3. The Gaussian part of the exterior functional

Use the local pressure split frozen in Section 4 and fix the covariance
gauge by

\[
 c_R(t)=(h_R(t,\cdot))_{B_{2R}}.
\tag{3.1}
\]

Under \(p\mapsto p+C(t)\), both \(\widetilde p\) and \(c_R\) shift by
the same amount, whereas \(p_R^{\rm loc}\) is unchanged.  Every expression
below is therefore pressure-gauge invariant.  This apparently special
choice is useful: on \(B_{2R}\),
\(p-c_R=p_R^{\rm loc}+h_R-(h_R)_{B_{2R}}\), so the core pressure appearing
in an exterior covariance pair is paid exactly by (4.10)--(4.11).

Let

\[
 Y_R(t,y)=|\widetilde u(t,y)|^3
 +|\widetilde p(t,y)-c_R(t)|^{3/2}.
\tag{3.2}
\]

The Gaussian exterior payment is

\[
 \boxed{
 \mathcal G_{u,p}^{\square}(z_0,R;\theta)
 =\frac1{R^2}\sum_{m=1}^{\infty}\gamma_m(\theta)
 \int_{I_R^\square}\!\int_{A_m(R)}Y_R(t,y)\,dy\,dt.}
\tag{3.3}
\]

It is finite for a periodic suitable weak solution with

\[
 u\in L_t^\infty L_x^2\cap L_t^2H_x^1,
 \qquad p\in L_{t,x}^{3/2},
\tag{3.4}
\]

because \(u\in L_{t,x}^3\) on finite cylinders and (2.8) beats the growth
of the periodic lift.  No Serrin norm, boundedness, or spatial Hölder
regularity is assumed in (3.4).

For later bookkeeping, write

\[
 \mathcal G_{u,p}=\mathcal G_u+\mathcal G_p
\tag{3.5}
\]

according to the two summands in (3.2).

### Exact centered-production split

With \(v_s=P_su\), the centered production in lift variables is

\[
 \mathscr S_s(x)
 =-\frac12\int_{\mathbb R^3}
 \nabla g_s(\widetilde x-y)\cdot
 \bigl(\widetilde u(y)-v_s(x)\bigr)
 \bigl|\widetilde u(y)-v_s(x)\bigr|^2\,dy.
\tag{3.6}
\]

Define \(\mathscr S_s^{\rm core}\) by restricting (3.6) to \(B_{2R}\),
and \(\mathscr S_s^{(m)}\) by restricting it to \(A_m(R)\).  Then

\[
 \boxed{
 \mathscr S_s
 =\mathscr S_s^{\rm core}
  +\sum_{m=1}^{\infty}\mathscr S_s^{(m)}.}
\tag{3.7}
\]

This is the first exact tail decomposition.

Using

\[
 |a-b|^3\le4(|a|^3+|b|^3),
 \qquad |v_s|^3\le P_s(|u|^3),
\tag{3.8}
\]

and (2.5), one obtains the explicit intermediate bounds

\[
 \int_{E_R}|\nabla g_s(\widetilde x-y)|\,dy
 \le CR^{-1}\sum_{m\ge1}2^{3m}\gamma_m(\theta)
 \le C_\theta R^{-1},
\tag{3.8a}
\]

\[
 \int_{E_R}|\nabla g_s(\widetilde x-y)|
       |\widetilde u(t,y)|^3\,dy
 \le CR^{-4}\sum_{m\ge1}\gamma_m(\theta)
       \int_{A_m(R)}|\widetilde u(t,y)|^3\,dy,
\tag{3.8b}
\]

and, by Jensen and the \(q=0\) part of (2.5),

\[
 \begin{aligned}
 \int_{B_R}|v_s(x)|^3\,dx
 &\le\int_{B_R}P_s(|u|^3)(x)\,dx\\
 &\le\int_{B_{2R}}|u(y)|^3\,dy
   +C\sum_{m\ge1}\gamma_m(\theta)
        \int_{A_m(R)}|\widetilde u(y)|^3\,dy.
 \end{aligned}
\tag{3.8c}
\]

These three inequalities give the following exterior estimate.  If
\(s(t)\) is any measurable scale satisfying
\(0<s(t)\le\theta R^2\), then

\[
 \boxed{
 \begin{aligned}
 &\frac1R\int_{I_R^\square}\!\int_{B_R}
 \left|\sum_{m\ge1}\mathscr S_{s(t)}^{(m)}\right|dx\,dt\\
 &\qquad\le C_\theta\left[
 \frac1{R^2}\int_{I_R^\square}\!\int_{B_{2R}}|u|^3\,dx\,dt
 +\mathcal G_u^\square(z_0,R;\theta)\right].
 \end{aligned}}
\tag{3.9}
\]

The apparently local first term in (3.9) pays for the centered value
\(v_s(x)\) inside an exterior increment.  It is not an omitted tail.
Because the exterior begins a distance \(R\) from \(B_R\), (3.9) remains
uniform as \(s(t)\downarrow0\).  This does not justify the zero-scale
distributional endpoint of the full weak identity.

For the scale-integrated tent quantity, the same calculation and
\(\|\nabla g_s\|_{L^1}=Cs^{-1/2}\) yield

\[
 \boxed{
 \begin{aligned}
 &\frac1{R^3}\int_{I_R^\square}\int_0^{\theta R^2}
   \int_{B_R}|\mathscr S_s|\,dx\,ds\,dt\\
 &\qquad\le C_\theta\left[
 \frac1{R^2}\int_{I_R^\square}\!\int_{B_{2R}}|u|^3\,dx\,dt
 +\mathcal G_u^\square(z_0,R;\theta)\right].
 \end{aligned}}
\tag{3.10}
\]

Equation (3.10) is an absolute size bound.  It is not the absorbable
characteristic estimate (X8.1) sought in the localized note.

---

## 4. Local pressure decomposition and the algebraic harmonic tail

To make the pressure gauge reproducible, put

\[
 \psi(a)=
 \begin{cases}0,&a\le0,\\ e^{-1/a},&a>0,\end{cases}
 \qquad
 Z(r)=
 \begin{cases}
 1,&r\le3,\\
 \displaystyle\frac{\psi(4-r)}
 {\psi(4-r)+\psi(r-3)},&3<r<4,\\
 0,&r\ge4,
 \end{cases}
\tag{4.0}
\]

and freeze

\[
 \zeta_R(y)=Z\!\left(\frac{|y-\widetilde x_0|}{R}\right).
\tag{4.0a}
\]

Then \(\zeta_R\in C_c^\infty(B_{4R})\) and

\[
 0\le\zeta_R\le1,
 \qquad \zeta_R=1\ \hbox{on }B_{3R},
 \qquad |\nabla^k\zeta_R|\le C_kR^{-k}.
\tag{4.1}
\]

Let

\[
 \mathcal R_i=(-\Delta)^{-1/2}\partial_i,
 \qquad
 \widehat{\mathcal R_if}(\xi)=i{\xi_i\over|\xi|}\widehat f(\xi),
\tag{4.1a}
\]

denote the whole-space Riesz transform with its sign convention fixed, and
define

\[
 p_R^{\rm loc}
 =\mathcal R_i\mathcal R_j
   (\zeta_R\widetilde u_i\widetilde u_j),
 \qquad
 h_R=\widetilde p-p_R^{\rm loc}\quad\hbox{on }B_{3R}.
\tag{4.2}
\]

For an energy-class suitable weak solution, (4.2) and all pointwise-in-time
pressure formulas in this section are understood for almost every time.

Since

\[
 -\Delta\widetilde p=\partial_i\partial_j
   (\widetilde u_i\widetilde u_j),
\tag{4.3}
\]

we have the exact local decomposition

\[
 \boxed{\widetilde p=p_R^{\rm loc}+h_R,
 \qquad \Delta h_R=0\quad\hbox{in }B_{3R}.}
\tag{4.4}
\]

Let

\[
 G(z)={1\over4\pi|z|},
 \qquad
 K_{ij}(z)=\partial_i\partial_jG(z)\quad(z\ne0),
 \qquad
 \mathcal T_{\ell ij}:=\partial_\ell\partial_i\partial_jG
 \ \hbox{in }\mathcal D'(\mathbb R^3).
\tag{4.5}
\]

Thus \(K_{ij}\) denotes the classical kernel only away from the origin,
whereas \(\mathcal T_{\ell ij}\) denotes the **complete distributional
derivative**.  In particular, \(\mathcal T_{\ell ij}\) is not the naive
Cauchy principal value of the classical degree \(-4\) kernel: its canonical
distributional extension contains terms supported at the origin.  This
distinction will disappear only after the source has been removed from a
neighbourhood of the evaluation point.

### Lemma 4.1 — periodic multiplier and lifted free-space kernel

Put \(F_{ij}=u_i u_j\).  Let
\(\mathcal T^{\rm per}_{\ell ij}\) be the zero-mean periodic distribution
obtained by periodicising the **complete** distribution
\(\mathcal T_{\ell ij}\); equivalently, it is defined directly by its
Fourier coefficients below.  For almost every fixed time, the zero-mean
periodic pressure gradient has the representation

\[
 \boxed{
 \partial_\ell p(t,x)
 =\mathcal T^{\rm per}_{\ell ij}
   *_{\mathbb T^3}F_{ij}(t,x)
 \quad\hbox{in }\mathcal D'(\mathbb T^3).}
\tag{4.5a}
\]

Indeed, first take a trigonometric-polynomial \(F\).  On every nonzero
integer Fourier mode \(k\), the right side of (4.5a) has multiplier

\[
 -i\,{k_\ell k_i k_j\over|k|^2},
\tag{4.5b}
\]

while its zero mode is zero.  The pressure Poisson equation (4.3) gives the
same multiplier.  Approximation in \(L^{3/2}(\mathbb T^3)\) therefore gives
(4.5a) in distributions; equivalently one may differentiate the periodic
Green distribution and then unfold it.  No naive principal-value formula is
used at the diagonal.  Periodicity rules out
a spatially linear pressure, and the remaining time-dependent pressure
constant disappears after \(\partial_\ell\).  Thus the whole-space
nondecaying parasitic-pressure ambiguity does not occur in this periodic
Poisson problem.

The differentiated local operator in (4.2) is likewise convolution of the
complete distribution \(\mathcal T_{\ell ij}\) with
\(\zeta_R\widetilde F_{ij}\).  Unfold (4.5a) and subtract this compact local
source.  For \(x\in B_{2R}\), the remainder
\((1-\zeta_R)\widetilde F\) vanishes in a neighbourhood of \(x\), so every
origin-supported contact term in \(\mathcal T_{\ell ij}\) is zero.  What
remains is the classical off-diagonal kernel and hence

\[
 \boxed{
 \nabla h_R(t,x)
 =\int_{\mathbb R^3}\nabla K_{ij}(x-y)
   (1-\zeta_R(y))
   \widetilde u_i(t,y)\widetilde u_j(t,y)\,dy.}
\tag{4.6}
\]

There is neither a contact term nor a principal value in (4.6), because
\(1-\zeta_R=0\) on \(B_{3R}\).  The integral is absolutely convergent at
infinity: \(|\nabla K(z)|\le C|z|^{-4}\), and the lattice sum
\(\sum_{n\in\mathbb Z^3\setminus\{0\}}|n|^{-4}\) converges.

Equivalently, the pressure gauge can be removed before estimating.  For
\(x,x_*\in B_{2R}\),

\[
 \boxed{
 h_R(t,x)-h_R(t,x_*)
 =\int_{\mathbb R^3}
  [K_{ij}(x-y)-K_{ij}(x_*-y)](1-\zeta_R(y))
  \widetilde u_i(t,y)\widetilde u_j(t,y)\,dy.}
\tag{4.6a}
\]

The mean-value theorem turns the kernel difference in (4.6a) into the
distance factor \(|x-x_*|\) times the order \(-4\) kernel in (4.6).

Define the pressure-sized annular moment

\[
 \boxed{
 \Lambda_R(t)
 =R\sum_{m=1}^{\infty}(2^mR)^{-4}
   \int_{A_m(R)}|\widetilde u(t,y)|^2\,dy.}
\tag{4.7}
\]

The first annulus overpays the transition region
\(3R<|y-\widetilde x_0|<4R\), which is harmless.  Equations (4.6)--(4.7)
give

\[
 \boxed{
 R\|\nabla h_R(t)\|_{L^\infty(B_{2R})}
 \le C\Lambda_R(t).}
\tag{4.8}
\]

The harmonic exterior payment is

\[
 \boxed{
 \mathcal H_u^\square(z_0,R)
 =R\int_{I_R^\square}\Lambda_R(t)^{3/2}\,dt.}
\tag{4.9}
\]

For each fixed \(R>0\), this quantity is finite at the suitable-weak energy
level.  Indeed, periodicity gives

\[
 \int_{A_m(R)}|\widetilde u(t,y)|^2\,dy
 \le C\bigl(1+(2^mR)^3\bigr)
       \|u(t)\|_{L^2(\mathbb T^3)}^2,
\tag{4.9a}
\]

and the large-annulus part of (4.7) is then dominated by a geometric
\(\sum_m2^{-m}\) series.  The finitely many smaller annuli cause no
convergence issue.  Finally,
\(u\in L_t^\infty L_x^2\) makes the time integral in (4.9) finite.

Consequently,

\[
 \boxed{
 \frac1{R^2}\int_{I_R^\square}\!\int_{B_{2R}}
 |h_R-(h_R)_{B_{2R}}(t)|^{3/2}\,dx\,dt
 \le C\mathcal H_u^\square(z_0,R).}
\tag{4.10}
\]

This is the pressure tail that a Gaussian annulus sum alone misses.  Its
kernel decays like distance to the power \(-4\) after the pressure gauge is
removed, rather than exponentially.

The local part is controlled at the energy level by the standard
Calderón--Zygmund estimate

\[
 \boxed{
 \int_{I_R^\square}\!\int_{\mathbb R^3}
 |p_R^{\rm loc}|^{3/2}\,dx\,dt
 \le C\int_{I_R^\square}\!\int_{B_{4R}}|u|^3\,dx\,dt.}
\tag{4.11}
\]

No pressure regularity or Serrin assumption is used in (4.11).

---

## 5. Exact pressure-covariance decomposition

With the gauge from (3.1), first write the covariance in the explicitly
integrable form

\[
 \boxed{
 Q_s=P_s((p-c_R)u)-P_s(p-c_R)P_su
     =P_s(pu)-p_sv_s.}
\tag{5.0}
\]

At the energy level, \(u\in L^3_{t,x}\) locally and
\(p-c_R\in L^{3/2}_{t,x}\), hence \((p-c_R)u\in L^1_{t,x}\).  The
covariance and the pair integrals below are therefore defined for almost
every time and every \(s>0\); Young's inequality supplies the Fubini
majorant.

For fixed \(x,s\), let

\[
 d\Gamma_{s,x}(y)=g_s(\widetilde x-y)\,dy.
\tag{5.1}
\]

This is a probability measure on \(\mathbb R^3\).  The pressure covariance
has the exact pair representation

\[
 \boxed{
 Q_s(x)=\frac12\iint_{\mathbb R^3\times\mathbb R^3}
 [\widetilde p(y)-\widetilde p(z)]
 [\widetilde u(y)-\widetilde u(z)]
 \,d\Gamma_{s,x}(y)d\Gamma_{s,x}(z).}
\tag{5.2}
\]

Recall \(C_R=B_{2R}\), \(E_R=\mathbb R^3\setminus C_R\), and set

\[
 \Omega_{\rm ext}
 =(\mathbb R^3\times\mathbb R^3)\setminus(C_R\times C_R).
\tag{5.3}
\]

Define \(Q_s^{\rm ext}\) by restricting the pair integral (5.2) to
\(\Omega_{\rm ext}\).  On \(C_R\times C_R\), insert the exact pressure
split (4.4), and call the resulting two pair integrals
\(Q_s^{\rm loc,cc}\) and \(Q_s^{h,cc}\).  Then

\[
 \boxed{
 Q_s=Q_s^{\rm loc,cc}+Q_s^{h,cc}+Q_s^{\rm ext}.}
\tag{5.4}
\]

Equation (5.4) is the second exact tail decomposition.  It separates:

1. a Calderón--Zygmund local pressure row;
2. a harmonic pressure row generated by exterior velocity;
3. a genuinely Gaussian exterior-pair row.

The two core--core terms satisfy the separately auditable bounds

\[
 \begin{aligned}
 |Q_s^{\rm loc,cc}(x)|
 &\le C\int_{C_R}
   (|p_R^{\rm loc}|^{3/2}+|u|^3)\,d\Gamma_{s,x},\\
 |Q_s^{h,cc}(x)|
 &\le C\int_{C_R}
   (|h_R-c_R|^{3/2}+|u|^3)\,d\Gamma_{s,x}.
 \end{aligned}
\tag{5.4a}
\]

For any scalar \(c\), Young's algebraic inequality gives

\[
 |p(y)-p(z)|\,|u(y)-u(z)|
 \le C\sum_{\xi\in\{y,z\}}
 \left(|p(\xi)-c|^{3/2}+|u(\xi)|^3\right).
\tag{5.5}
\]

Taking \(c=c_R(t)\), (5.5) shows explicitly that

\[
 \begin{aligned}
 |Q_s^{\rm ext}(x)|
 \le C\bigg[&
 \int_{E_R}Y_R(t,y)\,d\Gamma_{s,x}(y)\\
 &+\Gamma_{s,x}(E_R)
   \int_{C_R}Y_R(t,y)\,d\Gamma_{s,x}(y)
 \bigg].
\end{aligned}
\tag{5.6}
\]

Moreover, (2.5) gives the three auditable kernel rows

\[
 \Gamma_{s,x}(E_R)
 \le C\sum_{m\ge1}2^{3m}\gamma_m(\theta)
 \le C_\theta,
\tag{5.6a}
\]

\[
 \int_{B_R}\!\int_{E_R}Y_R(t,y)
 d\Gamma_{s,x}(y)\,dx
 \le C\sum_{m\ge1}\gamma_m(\theta)
       \int_{A_m(R)}Y_R(t,y)\,dy,
\tag{5.6b}
\]

\[
 \int_{B_R}\Gamma_{s,x}(E_R)
 \int_{C_R}Y_R(t,y)d\Gamma_{s,x}(y)\,dx
 \le C_\theta\int_{C_R}Y_R(t,y)\,dy.
\tag{5.6c}
\]

The second line is the core value paired with an exterior Gaussian sample;
it must not be deleted.  Its pressure part is paid by (4.10)--(4.11), and
its velocity part by the local \(L^3\) row.

Let \(s(t)\) and \(\eta_R\) satisfy the common quantifiers (1.9).  From
(2.5), (4.10), (4.11), (5.4a), and (5.6),

\[
 \boxed{
 \begin{aligned}
 &\frac1R\int_{I_R^\square}\!\int_{B_R}
 |Q_{s(t)}\cdot\nabla\eta_R|\,dx\,dt\\
 &\quad\le C_{\theta,C_\eta}\left[
 \frac1{R^2}\int_{I_R^\square}\!\int_{B_{4R}}|u|^3\,dx\,dt
 +\mathcal A_{\rm ext}^{\square}(z_0,R;\theta)
 \right].
 \end{aligned}}
\tag{5.7}
\]

Thus (0.1) pays every nonlocal row in the pressure covariance.  What (5.7)
does **not** show is that this payment is small, absorbable, or determined by
data in \(Q_{4R}^\square\).

---

## 6. Energy-level local row and the proved size statement

For either clock define

\[
 \begin{aligned}
 \mathcal E^\square(z_0,\rho)
 ={}&\frac1\rho
  \operatorname*{ess\,sup}_{t\in I_\rho^\square}
  \int_{B_\rho}|u(t,x)|^2\,dx\\
 &+\frac\nu\rho
  \int_{I_\rho^\square}\!\int_{B_\rho}|\nabla u|^2\,dx\,dt.
 \end{aligned}
\tag{6.1}
\]

Local Sobolev interpolation on \(B_{4R}\), followed by time integration,
gives

\[
 \begin{aligned}
 \int_{I_R^\square}\!\int_{B_{4R}}|u|^3
 \le C\,&\left(\operatorname*{ess\,sup}_{I_{4R}^\square}
        \|u(t)\|_{L^2(B_{4R})}^2\right)^{3/4}\\
 &\times\left(
  \int_{I_{4R}^\square}
   [\|\nabla u(t)\|_{L^2(B_{4R})}^2
    +R^{-2}\|u(t)\|_{L^2(B_{4R})}^2]dt
 \right)^{3/4}|I_R^\square|^{1/4}.
 \end{aligned}
\tag{6.1a}
\]

Substitution of (6.1) into (6.1a) yields

\[
 \boxed{
 \frac1{R^2}\int_{I_R^\square}\!\int_{B_{4R}}|u|^3\,dx\,dt
 \le C_\nu\,\mathcal E^\square(z_0,4R)^{3/2}.}
\tag{6.2}
\]

Here \(C_\nu\) may depend on the fixed viscosity and on which clock is
used, but not on \(R,z_0\), or the solution.  Equation (6.2) uses only the
energy-class quantities in (6.1).  The interpolation inequality is a proof
tool; no Serrin integrability hypothesis and no Hölder-continuity hypothesis
is inserted.

Combining (3.9), (5.7), and (6.2) yields the tail-complete positive-scale
size statement

\[
 \boxed{
 \begin{aligned}
 &\frac1R\int_{I_R^\square}\!\int_{B_R}
 \left|\mathscr S_{s(t)}^{\rm ext}\right|dx\,dt
 +\frac1R\int_{I_R^\square}\!\int_{B_R}
 |Q_{s(t)}\cdot\nabla\eta_R|\,dx\,dt\\
 &\qquad\le C_{\theta,\nu,C_\eta}\left[
 \mathcal E^\square(z_0,4R)^{3/2}
 +\mathcal A_{\rm ext}^{\square}(z_0,R;\theta)
 \right].
 \end{aligned}}
\tag{6.3}
\]

In (6.3), \(\mathscr S^{\rm ext}\) means the sum of the annular rows in
(3.7); the unsigned **core** centered production is not included in its
first term.  The scale-integrated core has the proved bound (3.10), whereas
the full descending-characteristic core near \(s=0\) is a separate issue.

Equation (6.3) is the auditable candidate requested by the R0.73X problem
freeze, with its precise quantifiers.  Its proof uses exact decompositions,
Gaussian kernel bounds, the local pressure split, Calderón--Zygmund, and
energy-level Sobolev interpolation.  It does not use a regularity criterion.

For direct comparison with problem-freeze (5.3), define

\[
 \mathcal C_{\mathscr S,0,\theta}^{\rm abs,\square}(z_0,R)
 =\frac1{R^3}\int_{I_R^\square}\int_0^{\theta R^2}
   \int_{B_R}|\mathscr S_s|\,dx\,ds\,dt.
\tag{6.4}
\]

Equations (3.10) and (6.2) prove the fully specified replacement of that
schematic row:

\[
 \boxed{
 \mathcal C_{\mathscr S,0,\theta}^{\rm abs,\square}(z_0,R)
 \le C_{\theta,\nu}\left[
  \mathcal E^\square(z_0,4R)^{3/2}
  +\mathcal A_{\rm ext}^{\square}(z_0,R;\theta)
 \right].}
\tag{6.5}
\]

The pressure component of \(\mathcal A_{\rm ext}\) is not needed to bound
\(\mathscr S_s\) alone, but retaining the single definition (0.1) makes
(6.5) compatible with the pressure-covariance ledger (5.7).  The content of
(6.5) is finiteness and scale-compatible size, not smallness or coercivity.

---

## 7. Suitable-weak positive tails retained in the exact ledger

For a suitable weak solution, let \(\widetilde\mu\) be the periodic lift of
the nonnegative local-energy defect measure.  The heat-smoothed dissipation
and defect have the exact annular splits

\[
 \begin{aligned}
 P_s(|\nabla u|^2)
 &=P_s^{\rm core}(|\nabla u|^2)
   +\sum_{m\ge1}P_s^{(m)}(|\nabla u|^2),\\
 P_s\mu
 &=P_s^{\rm core}\mu+\sum_{m\ge1}P_s^{(m)}\mu,
 \end{aligned}
\tag{7.1}
\]

where the second equality is understood by duality against nonnegative test
functions.  Define

\[
 \mathcal D_{\rm ext}^{\square}
 =\frac\nu R\sum_{m\ge1}\gamma_m(\theta)
  \int_{I_R^\square}\!\int_{A_m(R)}|\nabla\widetilde u|^2\,dy\,dt,
\tag{7.2}
\]

\[
 \mathcal M_{\rm ext}^{\square}
 =\frac1R\sum_{m\ge1}\gamma_m(\theta)
  \widetilde\mu(I_R^\square\times A_m(R)).
\tag{7.3}
\]

Both are scale invariant and nonnegative.  By (2.5), they control the
corresponding exterior contributions after integration over \(B_R\), up to
a numerical constant.

The two rows are not included in the minimal obstruction functional (0.1)
because they enter the collapsed suitable-weak trace ledger with favorable
sign.  They must nevertheless remain visible in any claimed **equality**.
Dropping them is licensed only when passing from the exact equality to a
one-sided upper estimate with the correct sign.

---

## 8. Scale audit

Under

\[
 u_\lambda(t,x)=\lambda u(\lambda^2t,\lambda x),
 \qquad
 p_\lambda(t,x)=\lambda^2p(\lambda^2t,\lambda x),
\tag{8.1}
\]

the radius becomes \(R/\lambda\), the heat scale becomes
\(s/\lambda^2\), and \(\nu\) is unchanged.  On a torus, an arbitrary
\(\lambda\) simultaneously rescales the lattice from \(2\pi\mathbb Z^3\)
to \((2\pi/\lambda)\mathbb Z^3\).  Thus the audit is an exact equality
between the correspondingly rescaled periodic domains; for an integer
\(\lambda\), (8.1) can also be read as a field on the original normalized
torus.  This is the standard local Navier--Stokes scaling convention, not a
claim that every real dilation is an automorphism of a fixed torus.

Each row has the following degree audit.

| row | unnormalized degree | prefactor | result |
|---|---:|---:|---:|
| \(\int |u|^3\,dx\,dt\) on a parabolic annulus | length\(^2\) | \(R^{-2}\) | invariant |
| \(\int |p-c_R|^{3/2}\,dx\,dt\) | length\(^2\) | \(R^{-2}\) | invariant |
| \(\Lambda_R\) | pressure degree \(2\) | none | \(\Lambda_{R/\lambda}[u_\lambda]=\lambda^2\Lambda_R[u]\) |
| \(\int\Lambda_R^{3/2}dt\) | length\(^{-1}\) | \(R\) | invariant |
| \(\int_{I_R\times B_R}|\mathscr S_s|\,dx\,dt\) | length | \(R^{-1}\) | invariant |
| \(\int_{I_R\times B_R}|Q_s\cdot\nabla\eta_R|\,dx\,dt\) | length | \(R^{-1}\) | invariant |
| \(\int_{I_R\times B_R\times(0,R^2)}|\mathscr S_s|\,ds\,dx\,dt\) | length\(^3\) | \(R^{-3}\) | invariant |
| \(\int|\nabla u|^2dxdt\) | length | \(\nu/R\) | invariant |
| \(\mu(Q)\) | length | \(R^{-1}\) | invariant |

The weights \(\gamma_m(\theta)\) are dimensionless.  Therefore

\[
 \boxed{
 \mathcal A_{\rm ext}^{\square}
 (u_\lambda,p_\lambda;z_0/\lambda,R/\lambda;\theta)
 =\mathcal A_{\rm ext}^{\square}
 (u,p;z_0,R;\theta),}
\tag{8.2}
\]

with the usual centered rescaling of \(z_0\).  The same statement holds for
\(\mathcal D_{\rm ext}\) and \(\mathcal M_{\rm ext}\), with the lattice
rescaled as stated above.

---

## 9. What is proved, standard, and open

### Smooth exact

1. The Euclidean-lift representation (1.5).
2. The heat-annulus identities (2.4), (3.7), and (7.1).
3. The local pressure identity (4.4) and pressure-covariance identity
   (5.4).
4. The covariance pair formula (5.2).

### Standard lemmas proved or directly available at energy level

1. The kernel estimate (2.5).
2. The exterior centered-production bound (3.9) and tent bound (3.10).
3. The harmonic pressure estimates (4.8)--(4.11).
4. The pressure-flux size estimate (5.7).
5. The local interpolation (6.2), the tail-complete characteristic exterior
   size statement (6.3), and the absolute tent-size statement (6.5).

For suitable weak solutions these statements are read at positive heat
scale and in the integrability classes explicitly stated above.  No
pointwise endpoint trace at \(s=0\) is added.

### Open estimates and exact blocking item

The following implication is **not** proved:

\[
 \text{small signed heat-characteristic payment}
 \quad\Longrightarrow\quad
 \mathcal E^\square(z_0,4R)^{3/2}
 +\mathcal A_{\rm ext}^{\square}(z_0,R;\theta)
 \text{ is small}.
\tag{9.1}
\]

In particular, neither suitability nor the local energy inequality controls
the pressure annuli in \(\mathcal G_p\) or the harmonic moment
\(\mathcal H_u\) by data on \(Q_R^\square\) alone.  The algebraic tail in
\(\Lambda_R\) is an explicit visible obstruction: replacing it by a Gaussian
weight would discard the nonlocal elliptic pressure.

Also open are:

1. absorption of the full unsigned core \(\mathscr S_s^{\rm core}\) along
   a descending characteristic reaching \(s=0\);
2. an estimate of the form
   \[
    |\text{unsigned cubic and pressure rows}|
    \le\varepsilon\,\text{positive dissipation}
       +C_\varepsilon\,\text{small critical data};
   \tag{9.2}
   \]
3. any implication from (6.3) to a CKN/Lin/Vasseur/Kwon epsilon scale;
4. removal of the positive heat-scale floor in the suitable-weak
   characteristic identity;
5. control of \(\mathcal A_{\rm ext}\) without either a declared exterior
   hypothesis or a new compactness/rigidity argument.

These are analytic PDE obstructions.  They are not settled by the finite
Fourier harness.

---

## 10. Frozen claim-state ledger

\[
\begin{array}{ll}
\texttt{torusEuclideanLift} &=\texttt{EXACT},\\
\texttt{standardCylinderSeparatedFromNuCylinder} &=\texttt{TRUE},\\
\texttt{heatAnnulusDecomposition} &=\texttt{EXACT},\\
\texttt{localPressureHarmonicDecomposition} &=\texttt{EXACT},\\
\texttt{pressureCovarianceThreeWaySplit} &=\texttt{EXACT},\\
\texttt{exteriorFunctionalScaleInvariant} &=\texttt{PROVED},\\
\texttt{tailCompleteSizeLemma} &=\texttt{PROVED\_AT\_POSITIVE\_SCALE},\\
\texttt{signedToAbsoluteCoercivity} &=\texttt{OPEN},\\
\texttt{exteriorFunctionalLocallyControlled} &=\texttt{OPEN},\\
\texttt{epsilonRegularity} &=\texttt{OPEN},\\
\texttt{arbitraryThreeDimensionalGlobalRegularity} &=\texttt{OPEN},\\
\texttt{clayConclusion} &=\texttt{OPEN}.
\end{array}
\tag{10.1}
\]

No DNS or Navier--Stokes simulation was used.  This note does not prove
regularity, exclude blow-up, construct a singular solution, or resolve the
Clay Millennium problem.
