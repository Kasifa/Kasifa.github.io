# R0.74H — collar-flux repair and two-regime closure in local mollified frames

## Status and scope

R0.74G proves that the pure large-payment estimates R0.74E (3.11) and
(4.17) are false.  Its explicit two-packet family has

\[
 P_R\lesssim B^3R^3,
 \qquad
 X_R\gtrsim B^2LR^2,
 \qquad
 \frac{X_R}{P_R^{2/3}}\gtrsim L\longrightarrow\infty.
\tag{0.1}
\]

The two-regime theorem proved below, combined with the same family's target
lower bound, implies \(P_R\to\infty\); see (7.5a).  The sequence therefore
does not decide the small-payment implication
\(P_R\le1\Rightarrow X_R\lesssim P_R^{2/3}\).

This note identifies the missing large-payment row and proves two positive
size estimates for every smooth periodic unforced solution in the two local
frames frozen in R0.74E:

1. an exact correction by the positive cumulative velocity--pressure flux
   across the annular collars; and
2. a coarser estimate using only the existing frozen nonnegative ledger.

The principal conclusions are

\[
 \boxed{
 X_R^M\le C\bigl[(P_R^M)^{2/3}+P_R^M\bigr],}
\tag{0.2}
\]

and, with \(P_{0,R}^F\) denoting the Version-F payment before the
acceleration row,

\[
 \boxed{
 X_R^F\le C\bigl[(P_R^F)^{2/3}+P_{0,R}^F\bigr]
 \le C\bigl[(P_R^F)^{2/3}+P_R^F\bigr].}
\tag{0.3}
\]

Consequently,

\[
 \boxed{
 P_R^\alpha\le1
 \quad\Longrightarrow\quad
 X_R^\alpha\le C(P_R^\alpha)^{2/3},
 \qquad \alpha\in\{M,F\}.}
\tag{0.4}
\]

Thus R0.74G rejects the unrestricted large-payment extrapolation, not the
small-payment size bound.

This is a positive-scale energy estimate.  It is not an absorption theorem,
an epsilon-regularity theorem, a continuation criterion, or a solution of
the Millennium problem.  No novelty or priority claim is made.
**NOT CLAY.**

Current status:

    PROVED / THREE INDEPENDENT ANALYTIC AUDIT TRACKS PASS /
    FULL-NOTE ADVERSARIAL PASS / FINITE CERTIFICATE PASS 25/25 /
    INDEPENDENT EXACT RECOMPUTATION PASS 25/25 /
    PRIMARY-LITERATURE BOUNDARY PASS /
    FIGURE VALIDATOR PASS 69/69 / FROZEN

The inherited R0.74E and R0.74G research snapshots are respectively

    4d0a017f4fff08ec53ddf57d73a1d237e2bc866c

and

    88b599633d4de0b3754a37380eb91104be92da81.

---

## 1. Frozen frames, payments, and the pre-acceleration ledger

Work on

\[
 \mathbb T^3=(-\pi,\pi]^3,
 \qquad I_\rho=(t_0-\rho^2,t_0),
 \qquad 0<R<\frac\pi{16},
\tag{1.1}
\]

and assume that \((u,p)\) is a smooth periodic unforced Navier--Stokes
solution with \(\overline I_{8R}\Subset(0,T)\).

All implicit constants below depend only on the frozen mollifier and cutoff
profiles (and the fixed torus convention).  They are independent of the
solution, \(R\), \(x_0\), \(t_0\), the frame label, and the explicit-family
index \(j\).

Use exactly the terminally anchored R0.74E trajectory

\[
 \dot X_R(t)=u_R(t,X_R(t)),
 \qquad X_R(t_0)=x_0,
 \qquad a_R=\dot X_R,
\tag{1.2}
\]

and the two fields

\[
 v_R(t,y)=u(t,y+X_R(t)),
 \qquad
 w_R(t,y)=v_R(t,y)-a_R(t).
\tag{1.3}
\]

They obey the exact equations

\[
 \partial_tv_R-\Delta v_R
 +(v_R-a_R)\cdot\nabla v_R+\nabla\pi_R=0,
\tag{1.4}
\]

\[
 \partial_tw_R-\Delta w_R
 +(w_R\cdot\nabla)w_R+\nabla\pi_R=-a_R'(t).
\tag{1.5}
\]

Taking divergence and using that \(a_R\) and \(a_R'\) are spatially
constant gives the two pressure identities

\[
 -\Delta\pi_R
 =\partial_i\partial_j(v_{R,i}v_{R,j})
 =\partial_i\partial_j(w_{R,i}w_{R,j}).
\tag{1.5a}
\]

Thus the R0.74E local/harmonic pressure split applies in both frames;
the constant drift and constant body force create no additional pressure
source.

All balls, annuli, and periodic lifts at radii \(R,2R,8R\) use this one
trajectory.  Retain every R0.74E definition of

\[
 \mathcal E^{\alpha,R},\quad
 \mathcal U_{\rm ext}^{\infty,\alpha,R},\quad
 \mathcal D_{\rm ext}^{\alpha,R},\quad
 \mathcal G_{z_\alpha,\pi_R}^{\alpha,R},\quad
 \mathcal H_{z_\alpha}^{\alpha,R},
\tag{1.6}
\]

where

\[
 z_M=v_R,
 \qquad z_F=w_R.
\tag{1.7}
\]

Write

\[
 \mathcal A_{\rm ext}^{\alpha,R}
 =\mathcal G_{z_\alpha,\pi_R}^{\alpha,R}
 +\mathcal H_{z_\alpha}^{\alpha,R},
\tag{1.8}
\]

and define the pre-acceleration payments

\[
 \boxed{
 P_{0,R}^\alpha
 =\mathcal E^{\alpha,R}(z_0,8R)^{3/2}
 +\mathcal A_{\rm ext}^{\alpha,R}(z_0,2R;1).}
\tag{1.9}
\]

Thus

\[
 P_R^M=P_{0,R}^M,
\tag{1.10}
\]

whereas

\[
 \boxed{
 P_R^F=P_{0,R}^F+
 \bigl(\mathcal J_{\rm acc}^{F,R}\bigr)^{3/2}.}
\tag{1.11}
\]

Finally,

\[
 X_R^\alpha
 =\mathcal U_{\rm ext}^{\infty,\alpha,R}
 +\mathcal D_{\rm ext}^{\alpha,R}.
\tag{1.12}
\]

The distinction between \(P_{0,R}^F\) and \(P_R^F\) will prevent the
acceleration payment from being enlarged a second time.

---

## 2. One smooth annular weight and finite-sum testing

Keep the R0.74E shell cutoffs \(\psi_j^R\):

\[
 \psi_j^R=1\quad\hbox{on }A_j(R),
 \qquad
 \operatorname{supp}\psi_j^R
 \subset\left\{y:\operatorname{dist}(y,A_j(R))\le\frac R8\right\},
\tag{2.1}
\]

\[
 |\nabla\psi_j^R|\le CR^{-1},
 \qquad
 |\Delta\psi_j^R|\le CR^{-2}.
\tag{2.2}
\]

Periodize them by

\[
 \Psi_j^R(x)
 =\sum_{n\in\mathbb Z^3}
 \psi_j^R(\widetilde x+2\pi n),
\tag{2.3}
\]

and retain the frozen weights

\[
 \gamma_j=e^{-4^{j-1}/32}.
\tag{2.4}
\]

For \(N\ge1\), put

\[
 \Theta_{R,N}=\sum_{j=1}^N\gamma_j\Psi_j^R.
\tag{2.5}
\]

Every \(\Theta_{R,N}\) is a legitimate nonnegative smooth periodic test.
For \(0\le k\le2\), lattice-point counting and (2.2) give

\[
 \|D^k\Psi_j^R\|_{L^\infty(\mathbb T^3)}
 \le C R^{-k}\bigl(1+2^{3j}R^3\bigr).
\tag{2.5a}
\]

The super-Gaussian factor makes the right side summable in \(j\), so

\[
 \Theta_{R,N}\longrightarrow\Theta_R
 \quad\hbox{in }C^2(\mathbb T^3).
\tag{2.6}
\]

In particular, all finite-shell terms in the energy identities below
converge absolutely and uniformly on compact time intervals.

Unfolding gives, for periodic integrable \(f\),

\[
 \int_{\mathbb T^3}f\Theta_R
 =\sum_{j\ge1}\gamma_j
   \int_{\mathbb R^3}\widetilde f\,\psi_j^R.
\tag{2.7}
\]

Since \(\psi_j^R=1\) on \(A_j(R)\),

\[
 \int_{\mathbb T^3}\Theta_R|z_\alpha|^2
 \ge U_\gamma^{\alpha,R}(t),
\tag{2.8}
\]

and

\[
 \int_{\mathbb T^3}\Theta_R|\nabla z_\alpha|^2
 \ge G_\gamma^{\alpha,R}(t).
\tag{2.9}
\]

Choose one nondecreasing time cutoff \(\eta_R\) satisfying

\[
 0\le\eta_R\le1,
 \qquad
 \eta_R=0\ \hbox{near }t_0-4R^2,
 \qquad
 \eta_R=1\ \hbox{on }I_R,
\tag{2.10}
\]

\[
 |\eta_R'|\le CR^{-2}.
\tag{2.11}
\]

Put \(s_R=t_0-4R^2\).

In particular, \(\eta_R(s_R)=0\) and \(\eta_R(\tau)=1\) for every
\(\tau\in I_R\); these endpoint values are used below.

---

## 3. Exact weighted identities and the collar flux

### 3.1 Version M

Multiply (1.4) by \(v_R\Theta_{R,N}\), integrate over the torus, and
use \(\nabla\cdot(v_R-a_R)=0\).  For every
\(\tau\in I_R\), integration from \(s_R\) to \(\tau\) gives

\[
\begin{aligned}
 &\frac1{2R}\int\Theta_{R,N}|v_R(\tau)|^2
 +\frac1R\int_{s_R}^{\tau}\eta_R
      \int\Theta_{R,N}|\nabla v_R|^2\\
 &=\frac1{2R}\int_{s_R}^{\tau}\eta_R'
      \int\Theta_{R,N}|v_R|^2
 +\frac1{2R}\int_{s_R}^{\tau}\eta_R
      \int |v_R|^2\Delta\Theta_{R,N}
 +\mathfrak F_{R,N}^M(\tau),
\end{aligned}
\tag{3.1}
\]

where

\[
\boxed{
\begin{aligned}
 \mathfrak F_{R,N}^M(\tau)
 =\frac1R\int_{s_R}^{\tau}\eta_R(t)
 \int_{\mathbb T^3}
 \left[
  \frac12|v_R|^2(v_R-a_R)
  +(\pi_R-c_{2R}^{M,R})v_R
 \right]\cdot\nabla\Theta_{R,N}\,dx\,dt .
\end{aligned}}
\tag{3.2}
\]

The pressure gauge contributes zero:

\[
 \int c_{2R}^{M,R}v_R\cdot\nabla\Theta_{R,N}
 =-c_{2R}^{M,R}
   \int\Theta_{R,N}\nabla\cdot v_R=0.
\tag{3.3}
\]

### 3.2 Version F

The same calculation applied to (1.5) gives

\[
\begin{aligned}
 &\frac1{2R}\int\Theta_{R,N}|w_R(\tau)|^2
 +\frac1R\int_{s_R}^{\tau}\eta_R
      \int\Theta_{R,N}|\nabla w_R|^2\\
 &=\frac1{2R}\int_{s_R}^{\tau}\eta_R'
      \int\Theta_{R,N}|w_R|^2
 +\frac1{2R}\int_{s_R}^{\tau}\eta_R
      \int |w_R|^2\Delta\Theta_{R,N}\\
 &\quad+\mathfrak F_{R,N}^F(\tau)
 +\mathfrak B_{R,N}^F(\tau),
\end{aligned}
\tag{3.4}
\]

where

\[
\boxed{
\begin{aligned}
 \mathfrak F_{R,N}^F(\tau)
 =\frac1R\int_{s_R}^{\tau}\eta_R(t)
 \int_{\mathbb T^3}
 \left[
  \frac12|w_R|^2w_R
  +(\pi_R-c_{2R}^{F,R})w_R
 \right]\cdot\nabla\Theta_{R,N}\,dx\,dt
\end{aligned}}
\tag{3.5}
\]

and

\[
 \mathfrak B_{R,N}^F(\tau)
 =-\frac1R\int_{s_R}^{\tau}\eta_R(t)a_R'(t)\cdot
 \left(\int_{\mathbb T^3}\Theta_{R,N}w_R\,dx\right)dt.
\tag{3.6}
\]

Expanding \(\Theta_{R,N}\), taking absolute values, and then passing to
the limit gives

\[
 \boxed{
 \sup_{\tau\in I_R}|\mathfrak B_R^F(\tau)|
 \le\frac12\mathcal J_{\rm acc,sh}^{F,R}
 \le\frac12\mathcal J_{\rm acc}^{F,R}.}
\tag{3.7}
\]

Thus the acceleration row was not missing in R0.74E.  Its \(3/2\) power
inside \(P_R^F\) becomes linear after the outer \(2/3\) power.

### 3.3 Limit and positive cumulative flux

The finite-sum fluxes converge absolutely as \(N\to\infty\).  Define

\[
 \mathfrak F_R^\alpha(\tau)
 =\lim_{N\to\infty}\mathfrak F_{R,N}^\alpha(\tau),
\tag{3.8}
\]

and

\[
 \boxed{
 \mathfrak C_R^\alpha
 =\sup_{\tau\in I_R}
   [\mathfrak F_R^\alpha(\tau)]_+.}
\tag{3.9}
\]

This is a cumulative incoming collar flux.  It contains neither the
terminal exterior energy nor the exterior dissipation from \(X_R^\alpha\).

---

## 4. The lower-order cutoff row

Define

\[
 S_{q,N}^\alpha
 =\sum_{j=1}^N\gamma_j
   \int_{I_{2R}}\int_{\operatorname{supp}\psi_j^R}
   |\widetilde z_\alpha|^q,
 \qquad q=2,3.
\tag{4.1}
\]

Weighted Holder and

\[
 \sum_{j\ge1}\gamma_j
 |I_{2R}|\,|\operatorname{supp}\psi_j^R|
 \le CR^5
\tag{4.2}
\]

give, uniformly in \(N\),

\[
 S_{2,N}^\alpha
 \le C R^{5/3}(S_{3,N}^\alpha)^{2/3}.
\tag{4.3}
\]

Hence

\[
 \boxed{
 R^{-3}S_{2,N}^\alpha
 \le C(R^{-2}S_{3,N}^\alpha)^{2/3}.}
\tag{4.4}
\]

The doubled-radius annular identity

\[
 A_k(R)=A_{k-1}(2R)
\tag{4.5}
\]

and the R0.74E support bookkeeping imply

\[
 R^{-2}S_{3,N}^\alpha
 \le C P_{0,R}^\alpha.
\tag{4.6}
\]

The inner collar pieces are paid by
\(\mathcal E^{\alpha,R}(z_0,8R)^{3/2}\); the outer pieces are paid by
the velocity component of
\(\mathcal G_{z_\alpha,\pi_R}^{\alpha,R}(z_0,2R;1)\).

Define the nonnegative quadratic-cutoff bound

\[
\begin{aligned}
 \mathfrak Q_R^\alpha
 =\frac1{2R}\int_{I_{2R}}\int_{\mathbb T^3}
 \bigl(
  |\eta_R'|\Theta_R
  +\eta_R|\Delta\Theta_R|
 \bigr)|z_\alpha|^2.
\end{aligned}
\tag{4.7}
\]

Equations (2.2), (4.4), and (4.6) yield

\[
 \boxed{
 \mathfrak Q_R^\alpha
 \le C(P_{0,R}^\alpha)^{2/3}
 \le C(P_R^\alpha)^{2/3}.}
\tag{4.8}
\]

This is the row naturally carrying the \(2/3\) exponent.

---

## 5. Exact collar-flux repair

### Theorem 5.1 — signed-flux closure

For \(\alpha\in\{M,F\}\), every solution in the scope of Section 1
satisfies

\[
 \boxed{
 X_R^\alpha
 \le C\left[(P_R^\alpha)^{2/3}
 +\mathfrak C_R^\alpha\right].}
\tag{5.1}
\]

Equivalently, if

\[
 \boxed{
 \widehat P_R^\alpha
 =P_R^\alpha+(\mathfrak C_R^\alpha)^{3/2},}
\tag{5.2}
\]

then

\[
 \boxed{
 X_R^\alpha\le C(\widehat P_R^\alpha)^{2/3}.}
\tag{5.3}
\]

**Proof.**  Let \(N\to\infty\) in (3.1) and (3.4).  Equations
(2.8)--(2.9) make the left sides dominate the frozen exterior energy and
dissipation.  After the right side is majorized as below, the identity at
each \(\tau\in I_R\), with the nonnegative dissipation dropped, gives

\[
 R^{-1}U_\gamma^{\alpha,R}(\tau)
 \le C\left[(P_R^\alpha)^{2/3}+\mathfrak C_R^\alpha\right].
\tag{5.1a}
\]

Letting \(\tau\uparrow t_0\), using continuity of the finite-time flux,
and dropping the nonnegative terminal energy gives separately

\[
 R^{-1}\int_{I_R}G_\gamma^{\alpha,R}(t)\,dt
 \le C\left[(P_R^\alpha)^{2/3}+\mathfrak C_R^\alpha\right].
\tag{5.1b}
\]

Taking the essential supremum in (5.1a) and adding (5.1b) costs only an
absolute constant.

The time and Laplacian terms are bounded by (4.8).  In Version M there is
no body force.  In Version F, (3.7) and (1.11) give

\[
 \mathcal J_{\rm acc}^{F,R}
 \le(P_R^F)^{2/3}.
\tag{5.4}
\]

Only the positive part of the signed flux can enlarge the left side.
This proves (5.1).  Finally,

\[
 (P_R^\alpha)^{2/3}
 +\mathfrak C_R^\alpha
 \le2\left[
 P_R^\alpha+(\mathfrak C_R^\alpha)^{3/2}
 \right]^{2/3},
\tag{5.5}
\]

which proves (5.3). \(\square\)

The correction in (5.2) is identity-level: it records the positive work
which moves energy across the frozen annular collars.  It is not asserted
to be an independently controllable regularity quantity.

---

## 6. Closure using only the frozen nonnegative ledger

### Lemma 6.1 — absolute collar flux

The fluxes in Section 3 satisfy

\[
 \boxed{
 \sup_{\tau\in I_R}|\mathfrak F_R^M(\tau)|
 \le CP_{0,R}^M=CP_R^M,}
\tag{6.1}
\]

and

\[
 \boxed{
 \sup_{\tau\in I_R}|\mathfrak F_R^F(\tau)|
 \le CP_{0,R}^F.}
\tag{6.2}
\]

**Proof.**  Since \(|\nabla\psi_j^R|\le CR^{-1}\), the velocity and
pressure pieces in (3.2) and (3.5) are bounded by

\[
 CR^{-2}\sum_j\gamma_j
 \int_{I_{2R}}\int_{\operatorname{supp}\psi_j^R}
 \left(|z_\alpha|^3
 +|\pi_R-c_{2R}^{\alpha,R}|^{3/2}\right).
\tag{6.3}
\]

The elementary inequality

\[
 |\pi_R-c|\,|z_\alpha|
 \le C\left(
 |\pi_R-c|^{3/2}+|z_\alpha|^3
 \right)
\tag{6.4}
\]

pays the pressure flux.  The radius shift (4.5), the local pressure split,
Calderon--Zygmund, and the harmonic row give

\[
 \text{right side of (6.3)}\le CP_{0,R}^\alpha.
\tag{6.5}
\]

For Version M, the remaining residual-transport row is

\[
 CR^{-2}\sum_j\gamma_j
 \int_{I_{2R}}\int_{\operatorname{supp}\psi_j^R}
 |a_R||v_R|^2.
\tag{6.6}
\]

R0.74E (3.4)--(3.5), Jensen, and Young bound (6.6) by the same local and
exterior velocity-cubic ledger.  Hence it is also bounded by \(CP_R^M\).
This proves (6.1)--(6.2). \(\square\)

### Theorem 6.2 — two-regime local-frame closure

Every solution in the scope of Section 1 satisfies

\[
 \boxed{
 X_R^M\le C\bigl[(P_R^M)^{2/3}+P_R^M\bigr],}
\tag{6.7}
\]

and

\[
 \boxed{
 X_R^F\le C\bigl[(P_R^F)^{2/3}+P_{0,R}^F\bigr]
 \le C\bigl[(P_R^F)^{2/3}+P_R^F\bigr].}
\tag{6.8}
\]

**Proof.**  Combine Theorem 5.1 with Lemma 6.1. \(\square\)

### Corollary 6.3 — the small-payment endpoint survives

If \(P_R^\alpha\le1\), then

\[
 \boxed{
 X_R^\alpha\le C(P_R^\alpha)^{2/3},
 \qquad \alpha\in\{M,F\}.}
\tag{6.9}
\]

**Proof.**  For Version M, \(P_R^M\le(P_R^M)^{2/3}\).  For Version F,
\(P_{0,R}^F\le P_R^F\le(P_R^F)^{2/3}\). \(\square\)

This is a size implication only.  It does not prove that the hypothesis
\(P_R^\alpha\le1\) propagates, absorbs another row, or excludes a
singularity.

---

## 7. The R0.74G family measures the missing flux

Return to the exact R0.74F--G family

\[
 u_j=(\mathfrak a_jF_j,B_j\theta_j,0),
 \qquad p_j=0,
 \qquad X_{R_j}=a_{R_j}=a_{R_j}'=0.
\tag{7.1}
\]

Versions M and F coincide.  Define the nonperiodized annular weight

\[
 \vartheta_R^{\rm ann}(x)=\sum_{k\ge1}\gamma_k\psi_k^R(x),
\tag{7.1a}
\]

whose derivatives and all products below are absolutely integrable.  It is
the lift-side representative of \(\Theta_R\) in the unfolding identity
(2.7).  Because the field is independent of \(x_1\), every
\(\partial_1\vartheta_R^{\rm ann}\) row integrates to zero.  The pure
shear row also vanishes after integration in \(x_2\).  Hence

\[
\boxed{
\begin{aligned}
 \mathfrak F_R(\tau)
 =\frac{\mathfrak a^2B}{2R}
 \int_{s_R}^{\tau}\eta_R(t)
 \int_{\mathbb R^3}
 \theta(t,x_3)F(t,x_2,x_3)^2
 \partial_2\vartheta_R^{\rm ann}(x)\,dx\,dt .
\end{aligned}}
\tag{7.2}
\]

This is the packet energy transported by the odd shear across the annular
collars.

Choose the R0.74G amplitude

\[
 \mathfrak a_j=B_j\gamma_j^{-1/2}.
\tag{7.3}
\]

The terminal lobe in R0.74F and (2.8) give, for every
\(\tau\in J_j=(t_{0,j}-R_j^3,t_{0,j})\),

\[
 \frac1R\int\Theta_R|u_j(\tau)|^2
 \ge cB_j^2L_jR_j^2.
\tag{7.4}
\]

R0.74G gives

\[
 P_{R_j}^M=P_{R_j}^F\le CB_j^3R_j^3,
\tag{7.5}
\]

There is also a rigorous lower conclusion, but no matching
\(B_j^3R_j^3\) claim is needed.  Since \(B_jR_j^2\to1/128\), (7.4)
tends to infinity.  Theorem 6.2 first forces \(P_{R_j}>1\) for all
sufficiently large \(j\), and then \((P_{R_j})^{2/3}\le P_{R_j}\) gives

\[
 \boxed{
 P_{R_j}^M=P_{R_j}^F
 \ge cB_j^2L_jR_j^2\longrightarrow\infty.}
\tag{7.5a}
\]

and the quadratic-cutoff proof above gives the sharper row

\[
 \mathfrak Q_{R_j}\le CB_j^2R_j^2.
\tag{7.6}
\]

Use the exact identity (3.1), the nonnegativity of its dissipation term,
and (7.4)--(7.6).  For all sufficiently large \(j\),

\[
 \boxed{
 \mathfrak C_{R_j}^M=\mathfrak C_{R_j}^F
 \ge cB_j^2L_jR_j^2.}
\tag{7.7}
\]

Consequently,

\[
 \boxed{
 (\mathfrak C_{R_j}^{\alpha})^{3/2}
 \ge cB_j^3L_j^{3/2}R_j^3,
 \qquad \alpha\in\{M,F\}.}
\tag{7.8}
\]

The missing factor \(L_j\) in R0.74G is therefore not an unknown pressure
or acceleration effect.  It is necessarily detected at the correct lower
scale by the positive collar flux.  No reverse comparison is claimed.
The linear \(P_R\) term also pays this family by Theorem 6.2.  No
quantitative slack relative to the family is claimed here.

---

## 8. Literature boundary

The use of a spatial weight in the Navier--Stokes local energy balance is
classical.  In particular, Fernández-Dalgo and Lemarié-Rieusset derive
weighted energy controls in which the diffusion, velocity transport, and
pressure all couple to the spatial derivative of the weight; the
velocity--pressure flux occurs linearly.  Their weights are polynomial
Muckenhoupt weights on \(\mathbb R^3\), not the periodic dyadic collars,
terminally anchored mollified trajectory, or two-frame acceleration ledger
used here:

- P. G. Fernández-Dalgo and P. G. Lemarié-Rieusset,
  [Weak solutions for Navier--Stokes equations with initial data in
  weighted L2 spaces](https://arxiv.org/abs/1906.11038), 2019/2020.

Their later weighted-energy paper treats a broader family of weights and
suitable weak solutions, with an axisymmetric no-swirl application.  It is
again methodologically adjacent rather than a statement of the present
periodic moving-frame theorem:

- P. G. Fernández-Dalgo and P. G. Lemarié-Rieusset,
  [Weighted energy estimates for the incompressible Navier--Stokes
  equations and applications to axisymmetric solutions without
  swirl](https://arxiv.org/abs/2010.00868), 2020/2021.

Bradshaw and Tsai develop local-energy solution bounds in uniformly local,
Morrey-type, and Wiener-amalgam settings.  Those results support the general
local-energy framework but do not state (5.1), (6.7), or (6.8) for the
R0.74E observables:

- Z. Bradshaw and T.-P. Tsai,
  [Global existence, regularity, and uniqueness of infinite energy
  solutions to the Navier--Stokes equations](https://arxiv.org/abs/1907.00256),
  2019/2020;
- Z. Bradshaw and T.-P. Tsai,
  [Local energy solutions to the Navier--Stokes equations in Wiener
  amalgam spaces](https://arxiv.org/abs/2008.09204), 2020.

R0.74B already proves the fixed-centre two-regime estimate.  The new task
here is the exact transfer to the R0.74E terminal local trajectory, including
the Version-M residual transport and the Version-F acceleration moments.

This bounded comparison is not an exhaustive collision or priority search.
The canonical primary-source ledger, search scope, and limitations are in
`research/r074h_report-source.md`.  No claim of novelty is made.

---

## 9. What is proved, and what remains open

### Established by the derivation

1. The finite-shell weighted energy identities (3.1) and (3.4).
2. The Version-F acceleration row is already paid at the correct power.
3. The exact positive collar-flux closure (5.1)--(5.3).
4. The existing-ledger two-regime estimates (6.7)--(6.8).
5. The pure \(2/3\) size estimate under \(P_R^\alpha\le1\).
6. The R0.74G two-packet family forces the collar-flux lower bound (7.7).

### Consequence for the route

The unrestricted pure \(P^{2/3}\) endpoint is retired.  The natural
large-payment correction is linear flux, or its coarser linear ledger
majorant.  The small-payment size estimate remains viable in both local
frames.

### Still open

1. control of \(\mathfrak C_R^\alpha\) by a weaker quantity not already
   tied to the local energy identity;
2. a scale iteration or absorption theorem starting from the small-payment
   estimate;
3. weak-solution stability and lower semicontinuity of the moving-frame
   collar flux;
4. an epsilon-regularity or continuation theorem; and
5. every global regularity, blow-up, or Millennium-problem claim.

**NOT CLAY.**

---

## 10. Verification and freeze record

The pre-promotion analytic source had SHA-256

    4140879118b501e0891646632aedb35e796434eb294454c28d35f4f7843c5aea.

The byte slice from Section 1 through Section 9 had SHA-256

    56d5e8487224348e9ce0282c4784a57921f70e0d277f261b705993e4e4b3b3ee.

The final-source rebind audit verifies that this analytic slice is unchanged
across status promotion and binds the final full-note hash.

### Analytic audits

1. `research/r074h_energy_identity_independent_audit.md` checks the
   finite-shell limit, both energy identities, pressure transfer, the
   quadratic row, and the Version-F acceleration power.
2. `research/r074h_packet_flux_independent_audit.md` checks the explicit
   packet-flux formula, parity cancellations, terminal lobe, and the
   one-sided lower bound.
3. `research/r074h_scaling_and_claim_audit.md` checks cubicization, the
   two-regime powers, the non-circular payment lower bound, and every
   one-sided claim boundary.
4. `research/r074h_full_note_adversarial_audit.md` checks definitions,
   radii, time buffers, quantifiers, cross-references, literature language,
   and the absence of a reversed upper bound.
5. `research/r074h_final_source_rebind_audit.md` binds the promoted source
   and the unchanged Sections 1--9 byte slice.

All required analytic audits return **PASS**.

### Finite certificate

The producer

    scripts/r074h_collar_flux_certificate.py

returns **PASS: 25/25**, byte-for-byte equal to

    research/r074h_collar_flux_certificate.json.

The report is

    research/r074h_collar_flux_certificate_report.md.

The independent implementation

    scripts/r074h_collar_flux_certificate_independent.rb

recomputes all 25 rows with Ruby `Rational`, compares 150 exact fields,
and returns 25/25 with zero mismatches.  Its audit is

    research/r074h_certificate_independent_audit.md.

These files check rational powers and elementary algebra only.  They do not
prove the analytic theorem.

### Primary-literature boundary

The canonical source report is

    research/r074h_report-source.md.

The public boundary record and independent audit are

    research/r074h_primary_literature_boundary.md
    research/r074h_primary_literature_independent_audit.md.

Four primary papers were checked.  Methodological precedents were found;
the exact R0.74H combination was not located in that bounded screen.  This
is not a novelty or priority conclusion.

### Journal figure

The 24-file exact-source package is

    research/figures/r074h/fig-r074h-collar-flux-repair/.

Its validator returns **PASS: 69/69** on two consecutive post-seal runs,
and every entry in `SHA256SUMS` verifies.  The package contains editable
SVG, one-page embedded-font PDF, 600 dpi PNG, exact source data, grayscale,
final-size, and PDF-rendered QA surfaces.  All four visual surfaces were
inspected after the final label repair.  The figure is an exact exponent
diagram, not DNS, a simulation, or measured data.

### Frozen boundary

The freeze manifest binds the final note, all audits, both certificate
implementations, literature ledger, and figure package.  The proved result
remains a smooth-solution one-scale size theorem.  Weak-solution stability,
independent flux payment, scale iteration, epsilon regularity,
continuation, singularity exclusion, global regularity, novelty, and
priority remain open or unclaimed.

**NOT CLAY.**
