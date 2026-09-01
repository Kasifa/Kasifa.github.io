# R0.74C — advected-shear obstruction to the large-payment endpoint

## Status and scope

This note resolves one narrowly frozen question from R0.74B. It tests
whether the fixed-centre buffered estimate

\[
 \mathcal U_{\rm ext}^{\infty,\square}
 +\mathcal D_{\rm ext}^{\square}
 \le C_{\nu,\square}(P^\square)^{2/3}
\tag{0.1}
\]

can hold at arbitrary payment. It is enough to fix

\[
 \nu=1,\qquad \theta=1.
\tag{0.2}
\]

The standard and viscosity clocks then coincide. For each radius used
below, set

\[
 t_0=65R^2,\qquad T_R=66R^2,\qquad
 I_\rho=(t_0-\rho^2,t_0),\qquad z_0=(t_0,0).
\tag{0.3}
\]

Thus

\[
 \overline{I_{8R}}=[R^2,65R^2]\Subset(0,T_R).
\tag{0.4}
\]

Retain exactly the R0.74B quantities

\[
 X_R=\mathcal U_{\rm ext}^{\infty}+\mathcal D_{\rm ext},
 \qquad
 P_R=\mathcal E(z_0,8R)^{3/2}
     +\mathcal A_{\rm ext}(z_0,2R;1).
\tag{0.5}
\]

The result proved here is

\[
 \boxed{
 \sup_{\substack{0<R<\pi/16\\
 (u,p)\ {\rm smooth\ periodic\ NSE}}}
 \frac{X_R}{P_R^{2/3}}=\infty.}
\tag{0.6}
\]

Consequently, the \(+P\) term in the R0.74B fixed-centre estimate cannot
simply be deleted. Equation (0.6) does not say that the particular \(+P\)
upper bound is sharp. It also does not address a co-moving or
Galilean-invariant observable.

Labels are literal: **PROVED**, **FINITE**, **OPEN**, and **NOT CLAY**.

---

## 1. An explicit mean-zero periodic family

Work on \(\mathbb T^3=(-\pi,\pi]^3\), and fix

\[
 q_*=\frac12.
\tag{1.1}
\]

Let

\[
 K_\tau^{\rm per}(z)
 =\frac1{\sqrt{4\pi\tau}}
  \sum_{n\in\mathbb Z}
  e^{-(z+2\pi n)^2/(4\tau)}
\tag{1.2}
\]

be the one-dimensional periodic heat kernel. Its spatial derivative has
zero periodic mean for every \(\tau>0\).

For an integer \(m\ge1\), put

\[
 M_m=3\,2^{m-1},\qquad q_m=M_mR,
\qquad
 V_m=\frac{q_m-q_*}{64R^2}.
\tag{1.3}
\]

The estimates below use only the admissible parameter set

\[
 0<R<R_0<\frac{\pi}{16},\qquad
 M_m\ge64,\qquad
 q_m=M_mR\le\frac{q_*}{16}.
\tag{1.3a}
\]

The exactness statement itself does not require (1.3a). The final
sequence in Section 7 satisfies all three conditions.

For \(0<t<T_R\), define

\[
 t_-=R^2,\qquad
 s=t-t_-,\qquad
 \tau(t)=2R^2+s=t+R^2,
\qquad
 q(t)=q_*+V_ms,
\tag{1.4}
\]

and

\[
 F_R(t,x_2)
 =R^2\partial_2K_{\tau(t)}^{\rm per}(x_2-q(t)).
\tag{1.5}
\]

Notice that

\[
 \tau(t)>R^2\quad(0<t<T_R),
\tag{1.6}
\]

so (1.5) is analytic throughout the full solution interval. On the
buffered interval,

\[
 2R^2<\tau(t)<66R^2,
\qquad
 q(t_-)=q_*,
\qquad
 q(t_0)=q_m.
\tag{1.7}
\]

For every \(A>0\), set

\[
 \boxed{
 u_{A,R,m}(t,x)=A F_R(t,x_2)e_1+V_me_2,
 \qquad
 p_{A,R,m}=0.}
\tag{1.8}
\]

### Lemma 1.1 — exact NSE trajectory

The pair (1.8) is a smooth periodic unforced Navier--Stokes solution on
\((0,T_R)\times\mathbb T^3\).

**Proof.** Since
\(\partial_\tau K_\tau^{\rm per}=\partial_2^2K_\tau^{\rm per}\),
direct differentiation of (1.5) gives

\[
 \partial_tF_R+V_m\partial_2F_R=\partial_2^2F_R.
\tag{1.9}
\]

Moreover,

\[
 \nabla\cdot u=0,\qquad
 (u\cdot\nabla)u=AV_m\partial_2F_R\,e_1.
\tag{1.10}
\]

Consequently,

\[
 \partial_tu-\Delta u+(u\cdot\nabla)u+\nabla p
 =A(\partial_tF_R-\partial_2^2F_R
       +V_m\partial_2F_R)e_1=0.
\tag{1.11}
\]

Smoothness follows from (1.6). The \(e_1\) component has zero spatial
mean because it is a derivative of a periodic kernel. \(\square\)

The free parameter \(A\) is an exact parameter of this orthogonal-shear
subclass. It is not an amplitude multiplication of a generic NSE
solution. Indeed, for a generic solution,

\[
 \mathcal N_\nu(Au,A^2p)
 =A(A-1)[(u\cdot\nabla)u+\nabla p],
\tag{1.12}
\]

so ordinary amplitude multiplication is not an NSE symmetry.

---

## 2. Analytic heat-kernel bounds

All constants in this section are independent of \(A,R,m\), subject to
(1.3a). The first two heat-kernel derivatives have polynomial degree at
most two; squaring and cubing require degree at most six. Fix the
convenient common majorant

\[
 \Pi_m=(1+M_m)^8.
\tag{2.0}
\]

After enlarging constants, \(\Pi_m\) pays every polynomial factor below.

### Lemma 2.1 — target strip and local leakage

There are fixed numbers \(1<b_1<b_2<2\) and constants \(c_0,C>0\)
such that:

1. for every \(t\) in a nonempty interval immediately before \(t_0\)
   on which \(|q(t)-q_m|\le R\), and

   \[
    x_2-q(t)\in[b_1R,b_2R],
   \tag{2.1}
   \]

   one has

   \[
    |F_R(t,x_2)|\ge c_0;
   \tag{2.2}
   \]

2. throughout \(I_{8R}\times B_{8R}\), once \(M_m\ge64\),

   \[
    |F_R|+R|\partial_2F_R|
    \le C\Pi_m e^{-M_m^2/528}.
   \tag{2.3}
   \]

In particular,

\[
 |F_R|^2+R^2|\partial_2F_R|^2
 \le C\Pi_m e^{-M_m^2/264}
\tag{2.4}
\]

and

\[
 |F_R|^3
 \le C\Pi_m e^{-3M_m^2/528}
\tag{2.5}
\]

on \(I_{8R}\times B_{8R}\).

**Proof.** At \(t=t_0\), \(\tau(t_0)=66R^2\). Scaling the central term
in (1.2) gives

\[
 R^2\partial_2
 \left[
  (4\pi 66R^2)^{-1/2}
  e^{-x_2^2/(264R^2)}
 \right]_{x_2=R\xi}
 =
 \frac{d}{d\xi}
 \left[
  (4\pi66)^{-1/2}e^{-\xi^2/264}
 \right].
\tag{2.6}
\]

The last derivative has a strictly positive absolute minimum on some
fixed interval \([b_1,b_2]\subset(1,2)\). After reducing the fixed
\(R_0\), the noncentral periodic images are \(O(e^{-c/R^2})\).
Continuity in the dimensionless heat age and in
the centre therefore proves (2.2) for times sufficiently close to
\(t_0\). The interval can be chosen with length \(cR/|V_m|\asymp R^3\),
so it has positive measure.

For the upper bound, the strip centre satisfies

\[
 q(t)\ge q(t_0)=M_mR
\quad\hbox{on }I_{8R}.
\tag{2.7}
\]

Every point of \(B_{8R}\) is therefore at least
\((M_m-8)R\) from the central kernel. Since
\(\tau(t)\le66R^2\) on \(I_{8R}\), its Gaussian exponent is no larger
than

\[
 -\frac{(M_m-8)^2}{264}.
\tag{2.8}
\]

Write \(\rho\) for the distance to a lifted kernel centre divided by
\(R\). The first two spatial derivatives of (1.2), after the
normalisation in (1.5), are bounded in the combination
\(|F_R|+R|\partial_2F_R|\) by
\(C(1+\rho)^2 e^{-\rho^2/264}\). For large \(m\)
this function is decreasing on \(\rho\ge M_m-8\), so its maximum there
is bounded by a fixed polynomial in \(M_m\) times the Gaussian at
\(\rho=M_m-8\). For \(M_m\ge64\),

\[
 \frac{(M_m-8)^2}{264}\ge\frac{M_m^2}{528}.
\tag{2.9}
\]

All noncentral periodic images have larger distance. Before the common
majorisation by \(\Pi_m\), the polynomial degrees in (2.3), (2.4), and
(2.5) are at most two, four, and six, respectively. Thus the single
choice \(\Pi_m=(1+M_m)^8\) proves all three displayed bounds.
\(\square\)

The exponent margin used later is strict:

\[
 \frac1{264}>\frac1{288}.
\tag{2.10}
\]

---

## 3. Target lower bound

The final strip lies in

\[
 A_m(R)=\{2^mR\le|y|<2^{m+1}R\},
\tag{3.1}
\]

because

\[
 2^mR=\frac23M_mR,\qquad
 2^{m+1}R=\frac43M_mR.
\tag{3.2}
\]

Its exact R0.73X weight is

\[
 \gamma_m(1)
 =e^{-4^{m-1}/32}
 =e^{-M_m^2/288}.
\tag{3.3}
\]

When \(M_mR\ll1\), this annulus lies in one Euclidean chart. Intersect
the strip from Lemma 2.1 with a disc in the \(y_1,y_3\) plane of radius
\(M_mR/4\). For all sufficiently large \(m\), (3.2) shows that the
resulting set is contained in \(A_m(R)\), and its volume is at least
\(cM_m^2R^3\). Hence

\[
 \boxed{
 \mathcal U_{\rm ext}^{\infty}
 \ge cA^2M_m^2R^2e^{-M_m^2/288}.}
\tag{3.4}
\]

The interval supplied by Lemma 2.1 has positive measure inside \(I_R\),
so the essential supremum causes no endpoint problem. Since
\(\mathcal D_{\rm ext}\ge0\), (3.4) also bounds \(X_R\) from below.

---

## 4. Lifted annular majorants

Put \(S=2R\), and define

\[
 W_S(y)=\sum_{j\ge1}\gamma_j(1)1_{A_j(S)}(y).
\tag{4.1}
\]

### Lemma 4.1 — Gaussian weight and all periodic copies

For \(|y|\ge2S\),

\[
 \boxed{
 W_S(y)\le C\left(\frac S{|y|}\right)^4,}
\tag{4.2}
\]

and

\[
 \int_{\mathbb R^3}W_S(y)\,dy\le CS^3.
\tag{4.3}
\]

Moreover,

\[
 \int_{\mathbb R^2}
 W_S(y_1,y_2,y_3)\,dy_1dy_3
 \le\frac{CS^4}{y_2^2+S^2}.
\tag{4.4}
\]

**Proof.** The elementary bound

\[
 e^{-4^{j-1}/32}\le C2^{-4j}
\tag{4.5}
\]

and the inequalities
\(2^jS\le|y|<2^{j+1}S\) prove (4.2). Also,

\[
 \sum_{j\ge1}\gamma_j(1)|A_j(S)|
 \le CS^3\sum_{j\ge1}
       2^{3j}e^{-4^{j-1}/32}<\infty,
\tag{4.6}
\]

which proves (4.3). If \(|y_2|\ge2S\), integrate
\(CS^4(y_1^2+y_2^2+y_3^2)^{-2}\) in the \(y_1,y_3\) plane. If
\(|y_2|<2S\), the exclusion of \(B_{2S}\) gives the upper bound \(CS^2\).
These two bounds are exactly (4.4). \(\square\)

For the harmonic row, define

\[
 L_S(y)
 =S\sum_{j\ge1}(2^jS)^{-4}1_{A_j(S)}(y).
\tag{4.7}
\]

The same proof gives

\[
 L_S(y)\le\frac{CS}{|y|^4},
\qquad
 \int_{\mathbb R^2}L_S(y)\,dy_1dy_3
 \le\frac{CS}{y_2^2+S^2}.
\tag{4.8}
\]

### Lemma 4.2 — lifted strip integrals

For \(t\in I_S=(61R^2,65R^2)\), let \(q=q(t)\). Then

\[
 \boxed{
 \int_{\mathbb R^3}
 W_S(y)|\widetilde F_R(t,y_2)|^3\,dy
 \le\frac{CR^5}{q^2},}
\tag{4.9}
\]

and

\[
 \boxed{
 \int_{\mathbb R^3}
 L_S(y)|\widetilde F_R(t,y_2)|^2\,dy
 \le\frac{CR^2}{q^2}.}
\tag{4.10}
\]

**Proof.** On \(I_S\), the dimensionless heat age satisfies

\[
 62\le\frac{\tau(t)}{R^2}\le66.
\tag{4.11}
\]

Equations (1.3a)--(1.4) also give
\[
 M_mR\le q(t)
 \le\frac{q_*}{16}+\frac{15M_mR}{16}
 <\frac{q_*}{8}.
\tag{4.11a}
\]

Put \(q_n=q+2\pi n\). The explicit derivative in (1.2) and (4.11)
give

\[
 |\widetilde F_R(t,y_2)|
 \le C\sum_{n\in\mathbb Z}
 e^{-c|y_2-q_n|^2/R^2}.
\tag{4.12}
\]

The packets are separated by \(2\pi\), whereas \(R<R_0\). Hence their
overlap is uniformly bounded. For \(p=2,3\), Hölder in the counting
index gives

\[
 |\widetilde F_R(t,y_2)|^p
 \le C_p\sum_{n\in\mathbb Z}
 e^{-c_p|y_2-q_n|^2/R^2}.
\tag{4.13}
\]

For every \(n\), split the \(y_2\)-integral into
\(|y_2-q_n|\le|q_n|/2\) and its complement. On the first part the
denominator is comparable to \(q_n^2+S^2\). On the second part, use
\((y_2^2+S^2)^{-1}\le S^{-2}\) and the Gaussian tail. Since
\(|q_n|\ge q\ge M_mR\ge64R\), this proves

\[
 \int_{\mathbb R}
 \frac{e^{-c_p|y_2-q_n|^2/R^2}}{y_2^2+S^2}\,dy_2
 \le\frac{CR}{q_n^2+S^2}.
\tag{4.14}
\]

The chart condition \(q<q_*/8<1\) and the separation of the \(q_n\)
give

\[
 \sum_{n\in\mathbb Z}\frac1{q_n^2+S^2}
 \le C\left(\frac1{q^2+S^2}+1\right)
 \le\frac C{q^2}.
\tag{4.15}
\]

Combining (4.4), (4.13)--(4.15), and \(S=2R\) gives
\(CS^4R/q^2\le CR^5/q^2\), which is (4.9). Combining (4.8) with the
same \(p=2\) calculation gives \(CSR/q^2\le CR^2/q^2\), which is
(4.10). \(\square\)

Lemmas 4.1--4.2 include every lifted annulus and every periodic copy.
No finite truncation is used.

---

## 5. Frozen pressure gauge

At scale \(S=2R\), use exactly the R0.73X split

\[
 p_S^{\rm loc}
 =\mathcal R_i\mathcal R_j
  (\zeta_S\widetilde u_i\widetilde u_j),
\qquad
 h_S=\widetilde p-p_S^{\rm loc}
 \quad\hbox{on }B_{3S},
\tag{5.1}
\]

where \(\zeta_S=1\) on \(B_{3S}\) and is supported in
\(B_{4S}=B_{8R}\). The frozen gauge is

\[
 c_S(t)=(h_S(t))_{B_{2S}}
       =(h_{2R}(t))_{B_{4R}}.
\tag{5.2}
\]

Although the physical pressure in (1.8) is zero, \(c_S\) need not vanish.

### Lemma 5.1 — CZ/Jensen gauge bound

For every \(t\in I_S\),

\[
 \boxed{
 |c_S(t)|^{3/2}
 \le CS^{-3}\int_{B_{4S}}|u(t,y)|^3\,dy.}
\tag{5.3}
\]

Consequently,

\[
 \boxed{
 \mathcal G_p(z_0,S;1)
 \le CS^{-2}
 \int_{I_S}\int_{B_{4S}}|u|^3.}
\tag{5.4}
\]

**Proof.** Since \(p=0\), (5.1) gives

\[
 h_S=-p_S^{\rm loc}\quad\hbox{on }B_{3S},
\qquad
 c_S=-(p_S^{\rm loc})_{B_{2S}}.
\tag{5.5}
\]

Jensen and the whole-space Calderón--Zygmund bound give

\[
 \begin{aligned}
 |c_S|^{3/2}
 &\le\frac1{|B_{2S}|}
      \int_{B_{2S}}|p_S^{\rm loc}|^{3/2}\\
 &\le CS^{-3}
      \int_{\mathbb R^3}|p_S^{\rm loc}|^{3/2}\\
 &\le CS^{-3}\int_{B_{4S}}|u|^3.
 \end{aligned}
\tag{5.6}
\]

Because \(p-c_S=-c_S\) throughout the lift, (4.3) and (5.3) imply

\[
 \begin{aligned}
 \mathcal G_p(z_0,S;1)
 &=S^{-2}\int_{I_S}|c_S(t)|^{3/2}\,dt
   \int_{\mathbb R^3}W_S(y)\,dy\\
 &\le CS^{-2}
   \int_{I_S}\int_{B_{4S}}|u|^3.
 \end{aligned}
\tag{5.7}
\]

This proves (5.4). \(\square\)

Thus the frozen gauge does not turn the remote strip into an unweighted
far-field pressure row. It sees only the constant background and the
heat tail inside \(B_{8R}\).

---

## 6. Complete payment ledger

Assume \(m\) is large enough that

\[
 q_m=M_mR\le\frac{q_*}{16}.
\tag{6.1}
\]

On \(I_S\),

\[
 q(t)\in
 \left[q_m,\frac{q_*}{16}+\frac{15q_m}{16}\right]
 \subset[q_m,q_*/8].
\tag{6.2}
\]

Moreover,

\[
 |V_m|\asymp R^{-2},
\qquad
 dt=\frac{dq}{|V_m|}\le CR^2\,dq.
\tag{6.3}
\]

The two velocity components are orthogonal, so

\[
 |u|^2=A^2F_R^2+V_m^2
\tag{6.4}
\]

and

\[
 |u|^3\le C(A^3|F_R|^3+|V_m|^3).
\tag{6.5}
\]

This also controls the apparent \(A\)-\(V_m\) pressure-source term:

\[
 (A|F_R|\,|V_m|)^{3/2}
 \le C(A^3|F_R|^3+|V_m|^3).
\tag{6.6}
\]

### Lemma 6.1 — buffered local energy

\[
 \boxed{
 \mathcal E(z_0,8R)
 \le C\left[
 R^{-2}
 +A^2R^2\Pi_m e^{-M_m^2/264}
 \right].}
\tag{6.7}
\]

**Proof.** The constant field contributes

\[
 (8R)^{-1}\int_{B_{8R}}|V_m|^2
 \le CV_m^2R^2\le CR^{-2}
\tag{6.8}
\]

and has zero gradient. For the strip, (2.4),
\(|B_{8R}|\asymp R^3\), and \(|I_{8R}|=64R^2\) give

\[
 (8R)^{-1}\mathop{\rm ess\,sup}_{I_{8R}}
 \int_{B_{8R}}A^2F_R^2
 \le
 CA^2R^2\Pi_m e^{-M_m^2/264}
\tag{6.9}
\]

and

\[
 (8R)^{-1}\int_{I_{8R}}\int_{B_{8R}}
 A^2|\partial_2F_R|^2
 \le
 CA^2R^2\Pi_m e^{-M_m^2/264}.
\tag{6.10}
\]

This proves (6.7). \(\square\)

### Lemma 6.2 — Gaussian velocity and pressure rows

\[
 \boxed{
 \mathcal G_u(z_0,S;1)
 \le C\left[
 R^{-3}+\frac{A^3R^4}{M_m}
 \right],}
\tag{6.11}
\]

and

\[
 \boxed{
 \mathcal G_p(z_0,S;1)
 \le C\left[
 R^{-3}
 +A^3R^3\Pi_m e^{-3M_m^2/528}
 \right].}
\tag{6.12}
\]

**Proof.** By (4.3), the constant part of \(\mathcal G_u\) is at most

\[
 S^{-2}|I_S||V_m|^3\int W_S
 \le C|V_m|^3R^3\le CR^{-3}.
\tag{6.13}
\]

For the strip, (4.9) and (6.3) give

\[
 \begin{aligned}
 S^{-2}A^3\int_{I_S}\frac{CR^5}{q(t)^2}\,dt
 &\le CA^3R^3R^2
      \int_{M_mR}^{q_*/8}\frac{dq}{q^2}\\
 &\le\frac{CA^3R^4}{M_m}.
 \end{aligned}
\tag{6.14}
\]

This proves (6.11). For (6.12), apply Lemma 5.1 and (6.5).
The constant term again gives \(CR^{-3}\). Equations (2.5),
\(|B_{8R}|\asymp R^3\), \(|I_S|=4R^2\), and
\(S^{-2}\asymp R^{-2}\) give the displayed strip term. \(\square\)

### Lemma 6.3 — harmonic row

\[
 \boxed{
 \mathcal H_u(z_0,S)
 \le C\left[
 R^{-3}+\frac{A^3R^4}{M_m^2}
 \right].}
\tag{6.15}
\]

**Proof.** By the definition of \(\Lambda_S\), (4.7), and (6.4),

\[
 \Lambda_S(t)
 \le CV_m^2
 +A^2\int_{\mathbb R^3}
       L_S(y)|\widetilde F_R(t,y_2)|^2\,dy.
\tag{6.16}
\]

Lemma 4.2 gives

\[
 \Lambda_S(t)
 \le C\left[
 V_m^2+\frac{A^2R^2}{q(t)^2}
 \right].
\tag{6.17}
\]

Therefore,

\[
 \begin{aligned}
 \mathcal H_u(z_0,S)
 &=S\int_{I_S}\Lambda_S(t)^{3/2}\,dt\\
 &\le CS|I_S||V_m|^3
 +CA^3SR^3R^2
   \int_{M_mR}^{q_*/8}\frac{dq}{q^3}\\
 &\le CR^{-3}+\frac{CA^3R^4}{M_m^2}.
 \end{aligned}
\tag{6.18}
\]

This proves (6.15). \(\square\)

### Proposition 6.4 — full payment upper bound

For the exact family (1.8),

\[
 \boxed{
 P_R\le C\left[
 R^{-3}
 +A^3R^3\Pi_m e^{-3M_m^2/528}
 +\frac{A^3R^4}{M_m}
 \right].}
\tag{6.19}
\]

Consequently,

\[
 \boxed{
 P_R^{2/3}\le C\left[
 R^{-2}
 +A^2R^2\Pi_m e^{-M_m^2/264}
 +A^2R^{8/3}M_m^{-2/3}
 \right].}
\tag{6.20}
\]

**Proof.** The heat-leakage polynomial in (6.7) comes from the
degree-at-most-four bound (2.4). Its \(3/2\) power has degree at most
six and is therefore still paid by the common \(\Pi_m\). Use

\[
 (a+b)^{3/2}\le C(a^{3/2}+b^{3/2}).
\tag{6.21}
\]

Then combine Lemmas 6.2--6.3. The row
\(A^3R^4/M_m^2\) is smaller than \(A^3R^4/M_m\). This proves
(6.19). Applying

\[
 (a+b+c)^{2/3}
 \le a^{2/3}+b^{2/3}+c^{2/3}
\tag{6.22}
\]

proves (6.20). \(\square\)

---

## 7. Divergence of three independent ratios

Choose

\[
 M_m=3\,2^{m-1}\longrightarrow\infty,
\qquad
 \boxed{
 R_m=e^{-M_m^2/96},
 \qquad
 \mathfrak a_m=R_m^{-2}e^{M_m^2/576}.}
\tag{7.1}
\]

Then \(R_m<\pi/16\), \(M_mR_m\to0\), and every preceding
large-\(m\) condition holds. In (1.8), take
\(R=R_m\) and \(A=\mathfrak a_m\). Denote the lower bound in (3.4) by

\[
 L_m=c\mathfrak a_m^2M_m^2R_m^2e^{-M_m^2/288}.
\tag{7.2}
\]

Against the local heat-leakage row in (6.20),

\[
 \frac{L_m}{
 \mathfrak a_m^2R_m^2\Pi_m e^{-M_m^2/264}}
 \ge
 \frac{cM_m^2}{\Pi_m}
 e^{M_m^2(1/264-1/288)}
 \longrightarrow\infty.
\tag{7.3}
\]

Against the exterior cubic row,

\[
 \begin{aligned}
 \frac{L_m}{\mathfrak a_m^2R_m^{8/3}M_m^{-2/3}}
 &=cM_m^{8/3}R_m^{-2/3}e^{-M_m^2/288}\\
 &=cM_m^{8/3}e^{M_m^2/288}
 \longrightarrow\infty.
 \end{aligned}
\tag{7.4}
\]

Against the constant-background row,

\[
 \frac{L_m}{R_m^{-2}}
 =c\mathfrak a_m^2M_m^2R_m^4e^{-M_m^2/288}
 =cM_m^2
 \longrightarrow\infty.
\tag{7.5}
\]

Equations (6.20) and (7.3)--(7.5) prove

\[
 \boxed{
 \frac{X_{R_m}}{P_{R_m}^{2/3}}\longrightarrow\infty.}
\tag{7.6}
\]

This proves (0.6).

The mechanism is endpoint transport. The large constant velocity moves a
much larger orthogonal shear through the fixed observation annulus during
a time of order \(R^3\). The earlier local ball sees only the Gaussian
heat tail and the constant background. The time-integrated exterior cubic
row sees the moving strip, but its residence time is too short to control
the quadratic endpoint with exponent \(2/3\).

---

## 8. Function-level obstructions and the NSE boundary

The R0.74A high-frequency packet and time-spike tests remain stronger in
the class of arbitrary smooth divergence-free fields. A packet can make

\[
 \mathcal D_{\rm ext}/P_R^{2/3}\to\infty,
\tag{8.1}
\]

and a short time spike can keep the integrated cubic payment bounded while
\(\mathcal U_{\rm ext}^{\infty}\to\infty\). Those fields are not
unforced NSE trajectories.

In contrast, every member of (1.8) is an exact smooth unforced periodic
NSE solution. The proof of (7.6) uses no DNS, Galerkin truncation, or
finite sampling.

The older dissipating shear

\[
 Ae^{-N^2(t-t_-)}\sin(Nx_2)e_1
\tag{8.2}
\]

does not give this buffered no-go: the \(8R\) energy sees its earlier
quadratic amplitude. The constant transport in (1.8), together with the
fixed Eulerian centre, is the new ingredient in the obstruction.

---

## 9. Revised positive question

Equation (7.6) rules out the exact large-payment endpoint proposed in
R0.74B. It does not prove that

\[
 X_R\le C(P_R^{2/3}+P_R)
\tag{9.1}
\]

has an optimal large-\(P_R\) exponent.

The smallest revised positive question should first remove the transport
defect. On the periodic unforced equation, the spatial mean \(\bar u\)
is constant. A Galilean-invariant version would use

\[
 u-\bar u,\qquad
 x_c(t)=x_0+\bar u(t-t_0),
\tag{9.2}
\]

and centre all balls and annuli at \(x_c(t)\). The family (1.8) then
reduces to a non-advected dissipating strip, so the present counterexample
does not apply. Whether a pure \(P^{2/3}\) closure holds for that
co-moving observable is **OPEN**.

For a fixed centre, another option is an explicit quadratic entrance-flux
or transport payment. Its minimal form and its relation to (9.1) are also
**OPEN**.

---

## 10. Audit ledger

### PROVED

1. Equation (1.8) is a smooth exact periodic unforced NSE family on the
   full interval \((0,T_R)\), and \(I_{8R}\Subset(0,T_R)\).
2. The shear profile has zero periodic mean; there is no heat-invariant
   constant tail.
3. The final strip gives the target lower bound (3.4).
4. The lifted Gaussian weight has the uniform polynomial majorant (4.2),
   including all periodic copies.
5. The frozen \(c_{2R}\) gauge obeys the CZ/Jensen estimate
   (5.3)--(5.4).
6. The local \(L^2\) and gradient-energy leakage share the strict exponent
   in (6.7).
7. All \(A\)-\(V_m\) rows are included in (6.19)--(6.20).
8. The three ratios (7.3)--(7.5) diverge, proving (0.6).

### FINITE

For each fixed \(m\), \(R_m>0\), \(\mathfrak a_m<\infty\), and
\(T_{R_m}>0\). The corresponding solution is analytic and has finite
periodic energy and finite R0.74B payments. The sequence has no uniform
global energy bound, and none is assumed in (0.1).

### OPEN

1. The optimal replacement for the large-\(P\) term in a fixed-centre
   estimate.
2. A pure \(P^{2/3}\) closure for a co-moving, mean-subtracted observable.
3. Weak stability and lower semicontinuity of the exterior tails.
4. Any absorption, epsilon-regularity, or regularity consequence.

### NOT CLAY

This note is a negative positive-scale estimate. It proves no singularity,
no epsilon-regularity theorem, and no global regularity or blow-up result
for three-dimensional Navier--Stokes.
