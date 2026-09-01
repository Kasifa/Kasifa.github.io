# R0.74F — two-packet survival in the odd local frame

## Status and scope

R0.74E constructed an exact smooth periodic mean-zero 2D3C
Navier--Stokes family whose \(R_j\)-mollified trajectory at the origin is
identically zero.  It proved the finite exponent gates but left the
two-packet Feynman--Kac survival estimate open.

This note closes that survival gate.  The proof has four pieces:

1. an exact time-reversed stochastic formula in the positive packet frame;
2. a periodic Brownian-bridge leakage estimate with every winding retained;
3. suppression of the inverted packet near the positive target; and
4. a terminal time slice whose lobe sets remain in the selected dyadic
   annulus.

The resulting target lower bound is **PROVED IN THIS VERSION**.  It has
passed the two same-source independent analytic audits indexed in Section 8.
No transition, pressure, exterior-copy, or full-denominator upper bound is
claimed here.  In particular, this note does not prove endpoint divergence,
regularity, blow-up, or the Millennium problem.  **NOT CLAY.**

The inherited R0.74E source is frozen at commit

    4d0a017f4fff08ec53ddf57d73a1d237e2bc866c.

---

## 1. Frozen paired-stream family

Write \(K_t=K_t^{\rm per}\) for the one-dimensional periodic heat kernel
with generator \(\partial_x^2\).  Retain the exact R0.74E parameters

\[
 \lambda=\frac{63}{32},\qquad
 c_h=\frac{15}{16},\qquad
 \alpha=\frac{14}{15},\qquad
 \beta=\frac{\sqrt{31}}{16},\qquad
 c_R=\frac1{320},\qquad
 \kappa=16.
\tag{1.1}
\]

For integers \(j\to\infty\), put

\[
 L_j=\lambda2^j,\qquad
 R_j=e^{-c_RL_j^2},\qquad
 r_j=L_jR_j,\qquad
 h_j=c_hr_j,\qquad
 q_j=\beta r_j.
\tag{1.2}
\]

Thus

\[
 h_j^2+q_j^2=r_j^2,
\qquad
 2^jR_j<r_j<2^{j+1}R_j.
\tag{1.3}
\]

Fix the odd saturation \(\sigma\) from R0.74E and define

\[
 g_j(x_3)=\sigma\!\left(\frac{\sin x_3}{\kappa R_j}\right),
\qquad
 \theta_j(t,x_3)=e^{t\partial_3^2}g_j(x_3),
\qquad
 b_j(t,x_3)=B_j\theta_j(t,x_3).
\tag{1.4}
\]

Set

\[
 t_{-,j}=R_j^2,\qquad
 t_{0,j}=65R_j^2,\qquad q_*=\frac12,
\tag{1.5}
\]

\[
 \mathfrak D_j
 =\int_{t_{-,j}}^{t_{0,j}}\theta_j(t,h_j)\,dt,
\qquad
 B_j=\frac{q_j+q_*}{\mathfrak D_j},
\tag{1.6}
\]

\[
 q_{{\rm pre},j}
 =-q_*-B_j\int_0^{t_{-,j}}\theta_j(t,h_j)\,dt,
\tag{1.7}
\]

\[
 Q_j(t)=q_{{\rm pre},j}
 +B_j\int_0^t\theta_j(s,h_j)\,ds.
\tag{1.8}
\]

R0.74E proves

\[
 Q_j(t_{-,j})=-q_*,
\qquad
 Q_j(t_{0,j})=q_j,
\qquad
 cR_j^{-2}\le B_j\le CR_j^{-2}.
\tag{1.9}
\]

Decompose the paired passive datum as

\[
\begin{aligned}
 F_j^+(0,x_2,x_3)
 &=R_j^3\partial_2K_{R_j^2}(x_2-q_{{\rm pre},j})
               K_{R_j^2}(x_3-h_j),\\
 F_j^-(0,x_2,x_3)
 &=R_j^3\partial_2K_{R_j^2}(x_2+q_{{\rm pre},j})
               K_{R_j^2}(x_3+h_j).
\end{aligned}
\tag{1.10}
\]

Let each component solve

\[
 \partial_tF_j^\pm+b_j\partial_2F_j^\pm
 =\Delta_{23}F_j^\pm,
\qquad
 F_j=F_j^++F_j^-.
\tag{1.11}
\]

For any amplitude \(\mathfrak a_j>0\),

\[
 u_j=(\mathfrak a_jF_j,b_j,0),\qquad p_j=0
\tag{1.12}
\]

is exact smooth periodic mean-zero unforced Navier--Stokes.  Full inversion
oddness and the even mollifier give

\[
 X_{R_j}(t)\equiv0,\qquad
 a_{R_j}(t)=a_{R_j}'(t)=0.
\tag{1.13}
\]

Hence Versions M and F coincide for this family.

For the proof, abbreviate

\[
 R=R_j,\quad L=L_j,\quad r=r_j,\quad h=h_j,\quad
 q=q_j,\quad B=B_j,\quad Q=Q_j,\quad \theta=\theta_j.
\tag{1.14}
\]

All constants below are independent of \(j\) once \(j\) is sufficiently
large.  On the discrete sequence (1.2),

\[
 L_{12}=8064<9216<L_{13}=16128,
\tag{1.15}
\]

so every later condition \(L_j\ge9216\) is equivalent to \(j\ge13\).

---

## 2. Exact positive-packet stochastic formula

Define the positive reference-centred profile

\[
 G^+(t,z,y)=F_j^+(t,Q(t)+z,h+y).
\tag{2.1}
\]

Since \(Q'(t)=B\theta(t,h)\), equation (1.11) gives

\[
 \partial_tG^+
 =\Delta_{z,y}G^+
 +d(t,y)\partial_zG^+,
\qquad
 d(t,y)=B[\theta(t,h)-\theta(t,h+y)].
\tag{2.2}
\]

The sign in (2.2) follows from

\[
 \partial_tG^+
 =\partial_tF_j^++Q'(t)\partial_2F_j^+
 =\Delta F_j^++[Q'(t)-b_j(t,h+y)]\partial_2F_j^+.
\tag{2.3}
\]

Let

\[
 Y_s^y=y+\sqrt2W_3(s)\pmod{2\pi}
\tag{2.4}
\]

and define the time-ordered displacement

\[
 \mathfrak S_t^y
 =\int_0^t d(t-s,Y_s^y)\,ds
 =B\int_0^t
 [\theta(t-s,h)-\theta(t-s,h+Y_s^y)]\,ds.
\tag{2.5}
\]

### Lemma 2.1 — time-reversed packet representation

For \(0\le t\le t_{0,j}\),

\[
 \boxed{
 G^+(t,z,y)
 =R^3\mathbb E_y\!\left[
   \partial_zK_{R^2+t}(z+\mathfrak S_t^y)
   K_{R^2}(Y_t^y)
 \right].}
\tag{2.6}
\]

**Proof.**  At stochastic time \(s\), use the generator

\[
 \Delta_{z,y}+d(t-s,y)\partial_z.
\tag{2.7}
\]

More explicitly, with an independent Brownian motion \(W_2\), set

\[
 Z_s=z+\int_0^s d(t-r,Y_r^y)\,dr+\sqrt2W_2(s)
 \pmod{2\pi}.
\]

Ito's formula applied to
\(G^+(t-s,Z_s,Y_s^y)\) has zero drift by (2.2).  At stochastic time \(t\),
the initial datum in the reference frame is

\[
 G^+(0,z,y)=R^3\partial_zK_{R^2}(z)K_{R^2}(y).
\tag{2.8}
\]

Conditioning on the \(W_3\)-path and convolving the independent
\(z\)-Brownian motion gives

\[
 \mathbb E_{W_2}
 \partial K_{R^2}(z+\mathfrak S_t^y+\sqrt2W_2(t))
 =\partial K_{R^2+t}(z+\mathfrak S_t^y).
\tag{2.9}
\]

This is (2.6).  The coefficient is evaluated at \(t-s\), not at \(s\).
\(\square\)

---

## 3. Periodic Brownian-bridge leakage

Let

\[
 A(\tau,x)=1-\theta(\tau,x)\ge0,
\tag{3.1}
\]

and put

\[
 \delta_R=\arcsin(\kappa R),
 \qquad
 P_R=[\delta_R,\pi-\delta_R]\pmod{2\pi}.
\tag{3.2}
\]

For \(L\ge9216\), one has \(R\le1/32\) and hence

\[
 \delta_R\le2\kappa R=32R.
\tag{3.3}
\]

The function \(g_j\) equals one on \(P_R\).  Moreover,

\[
 \operatorname{dist}_{\mathbb T}(h,P_R^c)
 \ge(c_hL-32)R\ge\alpha LR,
\tag{3.4}
\]

because \((c_h-\alpha)L=L/240\ge32\).  The transition at the torus
seam is farther away by a fixed distance: indeed
\(LR\le320/L\le5/144\), so \(h+[-R,R]\) stays in the central chart.

### Lemma 3.1 — exact all-copy bridge identity

Let \(k_\tau(x)=(4\pi\tau)^{-1/2}e^{-x^2/(4\tau)}\) be the
real-line heat kernel.  For every nonnegative periodic function \(\Phi\),
\(0<s\le t\), and \(|y|\le R\),

\[
\begin{aligned}
 &\mathbb E_y[\Phi(Y_s^y)K_{R^2}(Y_t^y)]\\
 &\quad=
 \sum_{n\in\mathbb Z}k_T(2\pi n-y)
 \int_{\mathbb R}k_v(\xi-\mu_{n,s})
 \Phi(\xi\bmod2\pi)\,d\xi,
\end{aligned}
\tag{3.5}
\]

where

\[
 T=t+R^2,
 \qquad
 v=\frac{s(T-s)}T,
 \qquad
 \mu_{n,s}=\frac{T-s}{T}y+\frac{s}{T}2\pi n.
\tag{3.6}
\]

At \(s=0\), (3.5) is understood as its Dirac limit.

**Proof.**  The Markov property and the heat semigroup give

\[
\begin{aligned}
 &\mathbb E_y[\Phi(Y_s^y)K_{R^2}(Y_t^y)]\\
 &\quad=
 \int_{\mathbb T}K_s(\eta-y)\Phi(\eta)K_{T-s}(\eta)\,d\eta.
\end{aligned}
\tag{3.7}
\]

Expand both periodic kernels, translate one fundamental interval to tile
\(\mathbb R\).  More explicitly, write the two kernel-copy indices as
\(a,b\in\mathbb Z\), set \(\xi=\eta+2\pi a\), and then set
\(n=a-b\).  The resulting integrand is reduced by the Gaussian product
identity

\[
 k_s(\xi-y)k_{T-s}(2\pi n-\xi)
 =k_T(2\pi n-y)k_v(\xi-\mu_{n,s}).
\tag{3.8}
\]

All terms are nonnegative, so Tonelli justifies both rearrangements.  This
proves (3.5) without discarding any winding. \(\square\)

For the central winding \(n=0\), write

\[
 \mu_s=\mu_{0,s}=\frac{T-s}{T}y,
 \qquad |\mu_s|\le R.
\tag{3.9}
\]

If \(r=t-s\), then the bridge heat time and the pre-existing heat age add
to

\[
 v+r
 =t-\frac{s^2}{T}
 \le t\le65R^2.
\tag{3.10}
\]

The distance from \(h+\mu_s\) to the nearest defect \(P_R^c\) is at least

\[
 h-\delta_R-|\mu_s|
 \ge(c_hL-33)R.
\tag{3.11}
\]

For \(L\ge9216\),

\[
 33\le\frac{c_hL}{256},
 \qquad
 c_hL-33\ge\frac{255}{256}c_hL,
\tag{3.12}
\]

and the exact rational inequality

\[
 \frac{(255/256)^2}{260}>\frac1{264}
\tag{3.13}
\]

gives the separation estimate

\[
 \frac{(h-\delta_R-|\mu_s|)^2}{4(v+r)}
 \ge\frac{c_h^2L^2}{264}.
\tag{3.14}
\]

At zero heat age, the points in (3.4) and (3.11) lie strictly inside
\(P_R\), so the following bounds are read by continuity.  The periodic
Gaussian tail estimate follows directly from
\[
 A(\tau,x)
 =\int_{\mathbb T}K_\tau(x-\xi)[1-g_j(\xi)]\,d\xi.
\]
Indeed, if \(x\) is at circular distance \(\rho\) from \(P_R^c\), then
the union of every lifted defect copy lies outside
\((x-\rho,x+\rho)\); since \(0\le1-g_j\le2\), the real Gaussian
two-tail bound gives \(A(\tau,x)\le4e^{-\rho^2/(4\tau)}\).  Consequently,

\[
 A(r,h)\le4e^{-\alpha^2L^2/260},
 \qquad
 A(r+v,h+\mu_s)\le4e^{-c_h^2L^2/264}.
\tag{3.15}
\]

### Lemma 3.2 — weighted periodic bridge leakage

For \(L\ge9216\), \(0\le s\le t\le65R^2\), and \(|y|\le R\),

\[
\begin{aligned}
 &\mathbb E_y\!\left[
 |\theta(t-s,h)-\theta(t-s,h+Y_s^y)|K_{R^2}(Y_t^y)
 \right]\\
 &\quad\le\frac6R\left(
 e^{-\alpha^2L^2/260}+e^{-c_h^2L^2/264}
 \right).
\end{aligned}
\tag{3.16}
\]

**Proof.**  Since \(-1\le\theta\le1\),

\[
 |\theta(r,h)-\theta(r,h+\eta)|
 \le A(r,h)+A(r,h+\eta).
\tag{3.17}
\]

For the central winding in (3.5), the semigroup identity and (3.15) give

\[
 \int_{\mathbb R}k_v(\xi-\mu_s)
 |\theta(r,h)-\theta(r,h+\xi)|\,d\xi
 \le4e^{-\alpha^2L^2/260}+4e^{-c_h^2L^2/264}.
\tag{3.18}
\]

Its weight satisfies \(k_T(-y)\le(2R)^{-1}\).  For \(n\ne0\), use the
direct bound \(|\theta(r,h)-\theta(r,h+\eta)|\le2\) and
\(T\le66R^2\) to obtain

\[
 \sum_{n\ne0}k_T(2\pi n-y)
 \le\frac2R e^{-1/(264R^2)}
 \le\frac2R e^{-c_h^2L^2/264}.
\tag{3.19}
\]

For the first inequality, \(|2\pi n-y|\ge|n|\) and, with
\(a=(264R^2)^{-1}\ge1\),
\(\sum_{n\ge1}e^{-n^2a}\le2e^{-a}\).  The second inequality follows
from \(R^{-1}=e^{L^2/320}\ge L\).
Combining the central contribution and all noncentral windings proves
(3.16).  Thus the torus seam and all periodic copies are part of the
estimate rather than an omitted error. \(\square\)

### Lemma 3.3 — the accumulated shift is negligible at packet scale

For \(L\ge9216\), \(0\le t\le65R^2\), and \(|y|\le R\),

\[
\begin{aligned}
 &\mathbb E_y\!\left[
 |\mathfrak S_t^y|K_{R^2}(Y_t^y)
 \right]\\
 &\quad\le\frac{13}{R}\left(
 e^{-\alpha^2L^2/260}
 +e^{-c_h^2L^2/264}\right).
\end{aligned}
\tag{3.20}
\]

In particular, the right side tends to zero as \(j\to\infty\).

**Proof.**  For large \(j\), (3.15) makes \(\theta(s,h)\ge1/2\) on
\([R^2,65R^2]\), while \(q\le LR\le5/144<1/2\).  The exact calibration
(1.6) therefore gives

\[
 0<B\le\frac1{32R^2}.
\tag{3.21}
\]

Tonelli, (2.5), and Lemma 3.2 now give the factor
\(6Bt/R\le195/(16R)<13/R\), which proves (3.20).  Finally,

\[
 \frac{\alpha^2}{260}-c_R
 =\frac{211}{936000}>0,
 \qquad
 \frac{c_h^2}{264}-c_R
 =\frac{23}{112640}>0.
\tag{3.22}
\]

Thus both inverse-\(R\) weighted exponentials in (3.20) tend to zero.
At \(t=0\), \(\mathfrak S_0^y=0\) exactly; at \(s=0\), Lemma 3.1 is
its Dirac limit; and at \(s=t>0\), the bridge variance is positive because
\(T-s=R^2\).  There is no hidden zero-time endpoint singularity.
\(\square\)

---

## 4. Survival of the positive packet

### Lemma 4.1 — comparison with the free derivative packet

Uniformly for \(0\le t\le65R^2\), \(|y|\le R\), and all \(z\),

\[
\begin{aligned}
 &\left|
 G^+(t,z,y)
 -R^3\partial_zK_{R^2+t}(z)K_{R^2+t}(y)
 \right|\\
 &\quad\le
 CR^{-1}\left(
 e^{-\alpha^2L^2/260}
 +e^{-c_h^2L^2/264}\right).
\end{aligned}
\tag{4.1}
\]

**Proof.**  The periodic heat-kernel derivative satisfies

\[
 \|\partial_z^2K_{R^2+t}\|_\infty\le CR^{-3}.
\tag{4.2}
\]

Subtract the zero-shift value in (2.6), apply the mean-value theorem, and
use Lemma 3.3.  The factor \(R^3\) in the datum cancels the \(R^{-3}\)
second-derivative cost.  The semigroup identity
\(\mathbb E_yK_{R^2}(Y_t^y)=K_{R^2+t}(y)\) supplies the free transverse
factor. \(\square\)

### Proposition 4.2 — uniform positive-packet lobe

Fix

\[
 b_1=\frac54,
 \qquad b_2=\frac32.
\tag{4.3}
\]

There is a fixed \(c_0>0\) such that, for all sufficiently large \(j\),

\[
 |F_j^+(t,Q(t)+z,h+y)|\ge2c_0
\tag{4.4}
\]

whenever

\[
 t_{0,j}-R^3<t<t_{0,j},\qquad
 b_1R\le z\le b_2R,\qquad |y|\le R.
\tag{4.5}
\]

The sign is constant on this set.

**Proof.**  On (4.5),

\[
 66-R\le\frac{R^2+t}{R^2}\le66.
\tag{4.6}
\]

For \(z/R\) in a fixed compact subinterval of \((1,2)\) and
\(|y|/R\le1\), the central real-Gaussian term in

\[
 R^3\partial_zK_{R^2+t}(z)K_{R^2+t}(y)
\tag{4.7}
\]

has one sign and an absolute value bounded below by a fixed positive
constant.  Its noncentral periodic copies are \(O(e^{-c/R^2})\).  Choose
\(c_0\) so that the free term is at least \(3c_0\) for small \(R\).
The error in Lemma 4.1 tends to zero by (3.22), and is at most
\(c_0\) for large \(j\). \(\square\)

---

## 5. The inverted packet is negligible near the positive target

The original-frame time-reversed diffusion for (1.11) has generator

\[
 \Delta_{2,3}-b_j(t-s,x_3)\partial_2.
\tag{5.1}
\]

Let

\[
 X_s^{x_3}=x_3+\sqrt2W_3(s)\pmod{2\pi},
\qquad
 \mathfrak B_t^{x_3}
 =\int_0^tb_j(t-s,X_s^{x_3})\,ds.
\tag{5.2}
\]

Conditioning on the \(x_3\)-path gives

\[
\begin{aligned}
 F_j^-(t,x_2,x_3)
 =R^3\mathbb E_{x_3}\!\left[
  \partial_2K_{R^2+t}
  (x_2+q_{{\rm pre},j}-\mathfrak B_t^{x_3})
  K_{R^2}(X_t^{x_3}+h)
 \right].
\end{aligned}
\tag{5.3}
\]

The sign of \(\mathfrak B_t^{x_3}\) is irrelevant for the following bound.

### Lemma 5.1 — cross-packet suppression

Uniformly for \(0\le t\le65R^2\), all \(x_2\), and \(|y|\le R\),

\[
 |F_j^-(t,x_2,h+y)|
 \le
 C\exp\!\left[-\frac{(2c_hL-1)^2}{264}\right]
 +Ce^{-c/R^2}.
\tag{5.4}
\]

Consequently the right side tends to zero.

**Proof.**  For \(t\le65R^2\),

\[
 \|\partial K_{R^2+t}\|_\infty\le CR^{-2}.
\tag{5.5}
\]

The transverse semigroup identity gives

\[
 \mathbb E_{h+y}K_{R^2}(X_t^{h+y}+h)
 =K_{R^2+t}(2h+y).
\tag{5.6}
\]

The central distance is at least \(2h-R=(2c_hL-1)R\), while
\(4(R^2+t)\le264R^2\).  Multiply the \(CR^{-2}\) derivative bound and the
\(CR^{-1}\) transverse kernel bound by the initial factor \(R^3\).  The
central Gaussian gives (5.4), and all noncentral copies give the second
term. \(\square\)

### Proposition 5.2 — survival of the full paired field

After increasing the base index, the full passive field satisfies

\[
 \boxed{
 |F_j(t,Q(t)+z,h+y)|\ge c_0}
\tag{5.7}
\]

throughout (4.5).

**Proof.**  Proposition 4.2 gives \(2c_0\) from the positive packet.
Lemma 5.1 makes the inverted packet at most \(c_0\) for all sufficiently
large \(j\).  The triangle inequality proves (5.7). \(\square\)

By inversion oddness, the reflected lobe has the opposite sign and the same
absolute lower bound.

---

## 6. Terminal residence in the selected outer annulus

For large \(j\), (3.15) and the calibration (1.6) give

\[
 \mathfrak D_j\ge32R^2,\qquad q_j\le\frac12,
\qquad B_j\le\frac1{32R^2}.
\tag{6.1}
\]

Hence, for

\[
 J_j=(t_{0,j}-R^3,t_{0,j}),
\tag{6.2}
\]

one has \(J_j\subset I_{R_j}\) and

\[
 |Q(t)-q|
 \le B_j(t_{0,j}-t)
 \le\frac R{32}
\qquad(t\in J_j).
\tag{6.3}
\]

Define

\[
\begin{aligned}
 \Omega_{j,+}(t)=\{x:\;&|x_1|<r/16,\quad
 b_1R<x_2-Q(t)<b_2R,\\
 &|x_3-h|<R\}.
\end{aligned}
\tag{6.4}
\]

Let \(\Omega_{j,-}(t)=-\Omega_{j,+}(t)\).

### Lemma 6.1 — lobe geometry

For \(L\ge9216\),

\[
 \Omega_{j,+}(t)\cup\Omega_{j,-}(t)
 \subset A_j(R)
 =\{2^jR\le|x|<2^{j+1}R\}
\tag{6.5}
\]

for every \(t\in J_j\).  Moreover,

\[
 |\Omega_{j,\pm}(t)|
 =c_\Omega rR^2
 =c_\Omega LR^3,
\qquad
 c_\Omega=\frac{b_2-b_1}{4}>0.
\tag{6.6}
\]

**Proof.**  The reference centre \((0,q,h)\) has radius \(r\).  On
\(\Omega_{j,+}(t)\),

\(LR\le5/144\), and the bounds below place all three coordinates in the
central interval \((-1/16,1/16)\) for sufficiently large \(j\).  Thus the
Euclidean norm used here is the unambiguous central lift of the torus box.

\[
 |x_2-q|
 \le b_2R+\frac R{32}
 <\frac{65}{32}R,
\qquad
 |x_3-h|<R.
\tag{6.7}
\]

Thus the planar perturbation has length at most \(97R/32\) by the
triangle inequality.  The lower radial bound is

\[
 |x|\ge r-\frac{97}{32}R
 >\frac r\lambda
 =2^jR.
\tag{6.8}
\]

At \(L=9216\), the exact normalized inner margin is

\[
 1-\frac1\lambda-\frac{97}{32L}
 =\frac{1015129}{2064384}>0,
\]

and it increases with \(L\).

For the upper bound, write
\(\varepsilon_2=x_2-q\) and \(\varepsilon_3=x_3-h\).  Then
\(|\varepsilon_2|<65R/32\), \(|\varepsilon_3|<R\), and
\(|x_1|<r/16\), so

\[
 \frac{|x|^2}{r^2}
 \le
 1+\frac1{256}
 +\frac{97}{16L}
 +\frac{5249}{1024L^2}
 <\left(\frac2\lambda\right)^2
 =\left(\frac{64}{63}\right)^2
\tag{6.9}
\]

At \(L=9216\), the exact outer squared margin is

\[
 \left(\frac2\lambda\right)^2-
 \left(1+\frac1{256}+\frac{97}{16L}
 +\frac{5249}{1024L^2}\right)
 =\frac{116914328399}{4261681299456}>0.
\]

The correction terms decrease as \(L\) increases.  This proves (6.5) for
the positive lobe; inversion proves
it for the negative lobe.  The three side lengths in (6.4) give (6.6).
\(\square\)

### Theorem 6.2 — two-packet outer-annulus survival

Here \(X_R^M\) and \(X_R^F\) are exactly the frozen endpoint quantities
defined in R0.74E, equations (3.6)--(3.9) and
(4.15b)--(4.15c), respectively; no endpoint has been redefined in this
note.

Let

\[
 \gamma_j=e^{-4^{j-1}/32}
 =e^{-c_\gamma L_j^2},
\qquad c_\gamma=\frac8{3969}.
\tag{6.10}
\]

For every amplitude \(\mathfrak a_j>0\) and all sufficiently large \(j\),
the exact Navier--Stokes field (1.12) satisfies

\[
\boxed{
 X_{R_j}^M=X_{R_j}^F
 \ge c\,\mathfrak a_j^2L_jR_j^2
 e^{-c_\gamma L_j^2}.}
\tag{6.11}
\]

**Proof.**  Since the local trajectory and acceleration vanish, Versions M
and F coincide.  Proposition 5.2 and Lemma 6.1 give, for every
\(t\in J_j\),

\[
\begin{aligned}
 U_\gamma(t)
 &\ge\gamma_j
 \int_{\Omega_{j,+}(t)}
 |\mathfrak a_jF_j(t,x_2,x_3)|^2\,dx\\
 &\ge c\gamma_j\mathfrak a_j^2L_jR_j^3.
\end{aligned}
\tag{6.12}
\]

The interval \(J_j\) has positive measure and lies in \(I_{R_j}\), so the
essential supremum in the definition of
\(\mathcal U_{\rm ext}^{\infty}\) sees (6.12).  Multiplication by
\(R_j^{-1}\) gives

\[
 \mathcal U_{\rm ext}^{\infty}
 \ge c\mathfrak a_j^2L_jR_j^2\gamma_j.
\tag{6.13}
\]

The dissipation parts of \(X_{R_j}^M=X_{R_j}^F\) are nonnegative, which
proves (6.11).
\(\square\)

---

## 7. Frozen claim boundary

### Proved in this version

1. the exact positive-packet reference-frame stochastic formula;
2. the periodic weighted Brownian-bridge leakage estimate;
3. vanishing of the drift-shift error at packet scale;
4. suppression of the inverted packet near the positive target;
5. terminal two-lobe residence in the selected dyadic annulus; and
6. the target lower bound (6.11).

### Still open

1. the buffered \(8R_j\) local-energy upper bound for both velocity
   components and both gradient rows;
2. the complete \(G_u\) transition, background, packet, and mixed rows;
3. the gauge-fixed \(G_p\) row;
4. the algebraic \(H_u\) row with all periodic copies;
5. one amplitude \(\mathfrak a_j\) that closes the full denominator and
   makes the Version-M/F ratio diverge or proves this family paid;
6. either arbitrary-solution endpoint and every regularity consequence.

The theorem here is a survival theorem for one explicit exact family.  It
does not decide the complete local-frame estimate.  **NOT CLAY.**

---

## 8. Verification and literature boundary

The analytic proof is covered by two separate same-source audits:

1. `research/r074f_periodic_bridge_independent_audit.md` independently
   checks the moving-coordinate equation, time-reversed Feynman--Kac
   formula, every periodic bridge winding, the leakage constants, the
   packet comparison, and inverted-packet suppression;
2. `research/r074f_two_packet_survival_independent_audit.md` independently
   checks the exact 2D3C Navier--Stokes family, symmetry cancellation,
   terminal-slice geometry, annular margins, volume, normalization, and
   Theorem 6.2.

Both audits lock the exact final source hash.  They are analytic audits,
not finite numerical evidence.

The separate exact-arithmetic certificate
`research/r074f_two_packet_survival_certificate.json` returns **PASS:
30/30**.  It certifies only rational identities, strict exponent margins,
the discrete threshold, and conditional annular geometry.  The journal
figure package
`research/figures/r074f/fig-r074f-two-packet-survival-gates/` returns
**PASS: 50/50** under its validator and visualizes the same finite and
conditional gates.  Neither artifact certifies the stochastic or PDE
proof.

The bounded primary-literature comparison is recorded in
`research/r074f_primary_literature_boundary.md`.  It identifies classical
Feynman--Kac, Brownian-bridge, 2D3C passive-scalar, shear-dispersion, and
mollified-trajectory antecedents.  The bounded search found no direct
statement of the combined theorem proved here, but it is not a priority or
novelty proof.  No such claim is made.
