# R0.72L -- an enstrophy-aware moderate strong-coupling window

**Date:** 2026-08-27

**Status:** a coupling-uniform complete-root upper theorem and an exact
moderate strong-coupling closure inside the common-band, row-aligned finite
triangular 2.5D Navier--Stokes class.  The proof keeps the actual enstrophy
contrast and the actual critical-log action.  It does not close arbitrarily
large coupling, multiscale physical absorption, or general three-dimensional
Navier--Stokes regularity.

**Keywords:** Navier--Stokes regularity, triangular 2.5D flow, strong
coupling, enstrophy contrast, critical-log action, complete temporal roots,
Fourier cascade, Galerkin truncation

---

## 0. Direct decision

R0.72K closed the complete complex-target ledger in a perturbative common
frequency band.  Its small parameter was not the bare coefficient
\(\delta\), but the dimensionless common-band exposure scale

\[
 \varepsilon:=\frac{gB}{R^2},
 \qquad g=|\delta|a.
 \tag{0.1}
\]

This is invariant under \(w_l\mapsto cw_l\),
\(\delta\mapsto\delta/c\).  Assumption (1.5) gives only the one-sided
comparison

\[
 |\delta|\int_0^\infty\|V_w(x)\|\,dx\lesssim\varepsilon;
 \tag{0.1a}
\]

no reverse inequality is used.  I therefore call \(\varepsilon\ll1\)
perturbative and \(\varepsilon\gtrsim1\) strong coupling in this declared
scale.  The actual Duhamel exposure may be smaller.

Let

\[
 p=\frac{\sqrt N}{B}\in(0,1],
 \qquad K=\mathcal R_Y(I),
 \qquad x=\Theta Q_*^I,
 \tag{0.2}
\]

where \(N\) is the carrier count, \(B\) is the multiplier coherence,
\(K\) is the actual enstrophy contrast, and \(x\) is the actual lifted
critical-log action.  For the amplitude-balanced exact physical family,

\[
 \Theta\asymp\frac{g^2}{a^2NR^2},
 \qquad D^{1/3}\asymp g^{2/3}N^{1/3}R^{2/3}.
 \tag{0.3}
\]

The first result is valid for every \(\varepsilon>0\).  With
\(L_R=1+\log R\), put

\[
\begin{aligned}
 U_0&=\varepsilon^{4/3}p^{4/3},\\
 W&=\varepsilon^{1/3}p^{1/3}R^{-1/3}L_R^{-1/2},\\
 U&=\varepsilon^{7/3}p^{4/3},\\
 V&=\varepsilon^{1/3}p^{1/3}R,
 \qquad H=\frac UV=\frac{\varepsilon^2p}{R}.
\end{aligned}
\tag{0.4}
\]

Then the complete physical root ledger obeys

\[
\boxed{
 \frac{\mathcal J_{\rm all}}
 {D^{1/3}\Lambda_{1,*}}
 \le C\left[
 \frac{U_0}{K+x}
 +W\frac{\sqrt x}{K+x}
 +\frac{\min\{U,Vx\}}{K+x}
 \right].}
\tag{0.5}
\]

No Duhamel-smallness assumption occurs in (0.5).  It is an exact
full-Fourier-lattice upper bound inside the declared triangular class.

For a phase-aligned, row-aligned common-band launch with the fixed background
specified below, a local interval of length

\[
 \tau=\frac{c_*}{R^2+gB}
 \tag{0.6}
\]

is perturbative even when the global scale \(\varepsilon\) is large.  A one-coordinate
correction produces an exact root at \(\tau\), preserves the target row, and
gives the action floor

\[
\boxed{
 x\ge Z
 :=c\varepsilon^2p^2R^{2/3}(1+\varepsilon)^{-2/3}
 \left[1+\log\!\left(2+R^2(1+\varepsilon)\right)\right].}
\tag{0.7}
\]

Consequently

\[
\boxed{
 \frac{\mathcal J_{\rm all}}
 {D^{1/3}\Lambda_{1,*}}
 \le C\left[
 \frac{U_0}{K+Z}
 +\frac{W}{\sqrt{K+Z}}
 +\frac{U}{K+\max\{H,Z\}}
 \right].}
\tag{0.8}
\]

For genuinely strong coupling in the growing window

\[
\boxed{
 1\lesssim\varepsilon
 \lesssim p^{2/3}R^{2/3}(1+\log R),}
\tag{0.9}
\]

the right side of (0.8) is uniformly bounded.  If the upper relation in
(0.9) is little-o, the normalized complete ledger tends to zero.  Thus the
R0.72K perturbative restriction is not the true boundary of this coherent
common-band route.

The theorem does not cover arbitrary strong coupling.  Beyond (0.9), the
first unclosed quantity is explicitly

\[
 \frac{\varepsilon^{7/3}p^{4/3}}
 {K+\max\!\left\{\varepsilon^2p/R,Z\right\}}.
 \tag{0.10}
\]

Closing (0.10) requires a new enstrophy/cascade lower bound, a stronger
all-time action floor, or a better strong-mixing cubic estimate.

---

## 1. Exact common-band setting

I retain the finite-carrier triangular lattice of R0.72H--K:

\[
 F'=D_qF+\delta V_w(x)F,
 \tag{1.1}
\]

\[
 (V_w(x)F)_r
 =-iK_z\sum_{l=1}^N e^{-\kappa r_l^2x}
 \left(w_lF_{r-r_l}+\overline{w_l}F_{r+r_l}\right).
 \tag{1.2}
\]

The conjugate pairing gives \(V_w^*=-V_w\), and hence

\[
 \frac12\frac d{dx}\|F(x)\|_2^2
 =-\langle A_qF,F\rangle,
 \qquad A_q=-D_q.
 \tag{1.3}
\]

Assume, with fixed geometric constants,

\[
 R\le |r_l|\le C_0R,
 \qquad c_0a\le|w_l|\le C_0a,
 \tag{1.4}
\]

\[
 \|V_w(x)\|\le C_1aB e^{-c_1R^2x},
 \qquad \sqrt N\lesssim B\lesssim N.
 \tag{1.5}
\]

Distinct integer carriers in a fixed relative band imply \(N\lesssim R\).
Therefore

\[
 p=\frac{\sqrt N}{B}\gtrsim R^{-1/2}.
 \tag{1.6}
\]

Set

\[
 z=V_wF,
 \qquad h=P_0z,
 \qquad b=P_0V_w^2F,
 \tag{1.7}
\]

\[
 \mathfrak q=\langle A_q^{-1}z,z\rangle,
 \qquad
 Q_*^I=\int_Iw_*\!\left(\frac{x}{X}\right)\mathfrak q(x)\,dx,
 \tag{1.8}
\]

where \(I=[0,X]\) is fixed and

\[
 w_*(s)=s^{-1/3}[1+\log(1/s)].
 \tag{1.9}
\]

The exact differentiated row is

\[
 h'+\lambda_0h=QF+\delta b,
 \qquad
 Q=P_0[V_w'+V_w(D_q+\lambda_0)].
 \tag{1.10}
\]

For every finite target-root subset, and hence for the complete extended
root mass, the R0.72K directional sampling theorem gives

\[
 G_{\rm all}^{\rm ex}
 \le E_0\rho_0^2+2\mathcal E_Q+2\mathcal C_\times,
 \tag{1.11}
\]

where

\[
 \mathcal E_Q=\int_I|hQF|\,dx,
 \qquad
 \mathcal C_\times=|\delta|\int_I|hb|\,dx.
 \tag{1.12}
\]

Equation (1.11) has no root-count, root-separation, or real-gauge loss.

---

## 2. Raw estimates without small coupling

The R0.72H mixed-row theorem and the R0.72J hybrid cubic estimate were
proved from energy contraction, negative-norm duality, and heat moments.
Their upper halves do not require \(\varepsilon\ll1\):

\[
 \mathcal E_Q
 \le C(E_0m_*Q_*^I)^{1/2},
 \tag{2.1}
\]

\[
 \mathcal C_\times
 \le\min\left\{
 C|\delta|B_0Q_*^I,
 C|\delta|E_0\int_I\rho(x)^2\|V_w(x)\|\,dx
 \right\}.
 \tag{2.2}
\]

In the common band,

\[
 E_0=N,
 \qquad \rho_0^2\lesssim a^2N,
 \qquad B_0\lesssim aR\sqrt N,
 \tag{2.3}
\]

\[
 m_*\lesssim\frac{a^2NR^{4/3}}{L_R},
 \qquad
 \int_I\rho^2\|V_w\|\,dx
 \lesssim\frac{a^3NB}{R^2}.
 \tag{2.4}
\]

Substitution gives

\[
 \boxed{
 \mathcal E_Q
 \lesssim aNR^{2/3}L_R^{-1/2}(Q_*^I)^{1/2},}
 \tag{2.5}
\]

\[
 \boxed{
 \mathcal C_\times
 \lesssim\min\left\{
 gR\sqrt N\,Q_*^I,
 \varepsilon a^2N^2
 \right\}.}
 \tag{2.6}
\]

The second branch in (2.6) can grow linearly with the scale \(\varepsilon\).  The point
of the next step is not to discard this factor, but to compare it with the
actual enstrophy and action already present in the physical denominator.

---

## 3. The enstrophy-aware complete-ledger theorem

Let

\[
 Y(t)=\|\omega(t)\|_2^2,
 \qquad K=\mathcal R_Y(I)=\frac{\sup_IY}{\inf_IY}.
 \tag{3.1}
\]

The critical-log physical quantity is

\[
 \Lambda_{1,*}
 =K[\nu^2+\mathscr A_*(I;u)].
 \tag{3.2}
\]

The inherited fixed decoupled background gives

\[
 \inf_IY\gtrsim E_{\rm phys},
 \tag{3.3}
\]

so each target-root atom satisfies

\[
 J_*(t_x)
 \lesssim\Theta|h(x)|^2,
 \qquad
 \Theta=\frac{S^2P^2}{E_{\rm phys}}
 \asymp\frac{g^2}{a^2NR^2}.
 \tag{3.4}
\]

Conversely, the target Fourier sector gives

\[
 \mathscr A_*(I;u)
 \gtrsim\frac{S^2P^2}{\sup_IY}Q_*^I.
 \tag{3.5}
\]

Since \(\inf_IY\le Y(0)\asymp E_{\rm phys}\), multiplying (3.5) by
\(K\) yields

\[
 K\mathscr A_*(I;u)\gtrsim\Theta Q_*^I=x.
 \tag{3.6}
\]

Also \(K\nu^2\gtrsim K\) for the fixed positive viscosity.  Thus

\[
 \boxed{\Lambda_{1,*}\gtrsim K+x.}
 \tag{3.7}
\]

This is the step that must be retained in strong coupling.  Replacing
\(K\) by a perturbative constant would remove the mechanism that can pay a
real Fourier cascade.

### Theorem 3.1 -- coupling-uniform normalized ledger

Under (1.4)--(1.5), the amplitude balance, and the background floor (3.3),
the complete root ledger obeys (0.5) for every \(\varepsilon>0\).

#### Proof

Multiply the three terms in (1.11), with (2.5)--(2.6), by \(\Theta\),
divide by \(D^{1/3}\Lambda_{1,*}\), and use (3.7).

For the first-root payment,

\[
 \frac{\Theta a^2N^2}{D^{1/3}}
 \asymp\varepsilon^{4/3}p^{4/3}=U_0.
 \tag{3.8}
\]

For the mixed row, write \(Q_*^I=x/\Theta\).  Then

\[
 \frac{\Theta aNR^{2/3}L_R^{-1/2}(Q_*^I)^{1/2}}
 {D^{1/3}}
 \asymp W\sqrt x.
 \tag{3.9}
\]

The two cubic branches become

\[
 \frac{\Theta\varepsilon a^2N^2}{D^{1/3}}
 \asymp U,
 \tag{3.10}
\]

and

\[
 \frac{\Theta gR\sqrt N\,Q_*^I}{D^{1/3}}
 \asymp Vx.
 \tag{3.11}
\]

Taking their minimum and dividing every term by \(K+x\) proves (0.5).
\(\square\)

Optimizing in the unknown actual action gives the weaker but useful form

\[
\boxed{
 \frac{\mathcal J_{\rm all}}
 {D^{1/3}\Lambda_{1,*}}
 \le C\left[
 \frac{U_0}{K}
 +\frac{W}{2\sqrt K}
 +\frac{U}{K+H}
 \right].}
\tag{3.12}
\]

Indeed

\[
 \sup_{x\ge0}\frac{\sqrt x}{K+x}=\frac1{2\sqrt K},
 \tag{3.13}
\]

and

\[
 \sup_{x\ge0}\frac{\min\{U,Vx\}}{K+x}
 =\frac{U}{K+U/V}.
 \tag{3.14}
\]

In particular, if

\[
 K\gtrsim\varepsilon^{7/3}p^{4/3},
 \tag{3.15}
\]

then enstrophy contrast alone pays the largest strong-coupling cubic term.
This is an enstrophy-contrast sufficient branch, not a proof that a cascade
must force (3.15), and it is not an assumption used in the main window below.

---

## 4. A local action floor at arbitrary global exposure scale

Assume a row-aligned launch \(G\) with

\[
 \|G\|_2^2=N,
 \qquad G_0=0,
 \qquad |P_0V_w(0)G|\ge c_2aN.
 \tag{4.1}
\]

Assume also that the free target row is phase aligned on a fixed multiple of
\(R^{-2}\), as in R0.72J, and retain the fixed decoupled background used in
(3.3).  These are hypotheses on the constructed family, not conclusions for
an arbitrary launch.

Let

\[
 \Omega=R^2+gB=R^2(1+\varepsilon),
 \qquad \tau=\frac{c_*}{\Omega},
 \tag{4.2}
\]

where \(c_*>0\) is a sufficiently small fixed geometric constant.  On this
short interval,

\[
 |\delta|\int_0^\tau\|V_w(s)\|\,ds
 \lesssim gB\tau\le Cc_*.
 \tag{4.3}
\]

The diagonal heat change is also \(O(R^2\tau)\le O(c_*)\).  Thus this
local window is perturbative for every value of the global scale \(\varepsilon\).

### Lemma 4.1 -- exact root correction and retained row

Let \(U(x,s)\) be the exact full-lattice evolution.  Put

\[
 A_\tau=P_0U(\tau,0)e_0,
 \qquad B_\tau=P_0U(\tau,0)G.
 \tag{4.4}
\]

For sufficiently small fixed \(c_*\),

\[
 |A_\tau|\ge\frac12,
 \qquad |B_\tau|\le CgN\tau.
 \tag{4.5}
\]

Define

\[
 \zeta=-B_\tau/A_\tau,
 \qquad \widetilde F(0)=G+\zeta e_0.
 \tag{4.6}
\]

After a harmless normalization back to energy comparable with \(N\),

\[
 P_0F(\tau)=0,
 \tag{4.7}
\]

\[
 \frac{|\zeta|}{\sqrt N}
 \lesssim c_*\frac{g\sqrt N}{R^2+gB}
 =c_*\frac{\varepsilon p}{1+\varepsilon}
 \le Cc_*,
 \tag{4.8}
\]

and

\[
 |h(x)|\ge caN,
 \qquad0\le x\le\tau.
 \tag{4.9}
\]

#### Proof

The free evolution preserves the target coordinate of \(e_0\), while
(4.3) controls the coupled correction.  This gives the first estimate in
(4.5).  Since \(G_0=0\), Duhamel's formula, the heat change, and (4.1)
give the second estimate.  Equation (4.6) gives (4.7) exactly by linearity.
Because \(B\ge\sqrt N\), (4.8) follows from (4.2).  Finally
\(P_0V_w(x)e_0=0\); the row variation, the evolution of \(G\), and the
effect of \(\zeta e_0\) over \([0,\tau]\) are all \(O(c_*aN)\).
Decreasing \(c_*\) proves (4.9). \(\square\)

The target inequality \(|h|^2\le\lambda_0\mathfrak q\), (4.9), and the
regular variation of \(w_*\) give

\[
 Q_*^I
 \ge ca^2N^2\Omega^{-2/3}[1+\log(2+\Omega)].
 \tag{4.10}
\]

Multiplication by \(\Theta\) proves (0.7).

---

## 5. The moderate strong-coupling closure

For \(x\ge Z\), the three scalar optimizations in (0.5) give

\[
 \frac{U_0}{K+x}\le\frac{U_0}{K+Z},
 \tag{5.1}
\]

\[
 \frac{\sqrt x}{K+x}\le\frac1{\sqrt{K+Z}},
 \tag{5.2}
\]

and

\[
 \frac{\min\{U,Vx\}}{K+x}
 \le\frac{U}{K+\max\{H,Z\}}.
 \tag{5.3}
\]

This proves (0.8).

For \(\varepsilon\ge1\), write

\[
 L_{R,\varepsilon}
 =1+\log\!\left(2+R^2(1+\varepsilon)\right).
 \tag{5.4}
\]

Then

\[
 Z\gtrsim
 \varepsilon^{4/3}p^2R^{2/3}L_{R,\varepsilon}.
 \tag{5.5}
\]

The first term satisfies

\[
 \frac{U_0}{Z}
 \lesssim p^{-2/3}R^{-2/3}L_{R,\varepsilon}^{-1}
 \lesssim R^{-1/3}L_R^{-1},
 \tag{5.6}
\]

where (1.6) was used.  The mixed term is no larger, up to a further
nonpositive power of \(\varepsilon\).  The cubic term satisfies

\[
 \frac UZ
 \lesssim
 \frac{\varepsilon}
 {p^{2/3}R^{2/3}L_{R,\varepsilon}}.
 \tag{5.7}
\]

Equations (5.6)--(5.7) prove the window (0.9).  They also show that a
little-o upper relation makes the whole normalized ledger tend to zero.

Two representative endpoints are worth separating:

1. if \(B\asymp\sqrt N\), then \(p\asymp1\), and the window reaches
   \(\varepsilon\lesssim R^{2/3}L_R\);
2. if \(B\asymp N\) and \(N\asymp R\), then \(p\asymp R^{-1/2}\), and
   the uniform worst-case window still reaches
   \(\varepsilon\lesssim R^{1/3}L_R\).

This is a genuine strong-coupling range because its upper endpoint diverges
with \(R\).

---

## 6. Why a finite Galerkin countermodel is not portable

There is a precise warning beyond the closed window.  A three-mode
Fourier--Galerkin projection can make the continuous row grow linearly with
strong coupling.

Take one real carrier and project to

\[
 \mathcal H_R=\operatorname{span}\{e_{-R},e_0,e_R\},
 \qquad
 u_R=\frac{e_R+e_{-R}}{\sqrt2}.
\tag{6.1}
\]

Here the fixed normalization is
\(\nu=d=K_z=q=1\), \(K_y=0\), so the target and carrier decay rates are
\(1\) and \(R^2+1\).

Write \(F=Ue_0-iVu_R\), \(c=\sqrt2a\), and set

\[
 y=R^2x,
 \qquad \sigma=\frac{\delta c}{R^2},
 \qquad U=r\cos\theta,
 \qquad V=r\sin\theta.
 \tag{6.2}
\]

For \(r(0)=1\), \(\theta(0)=\pi/4\), the projected equations give
exactly

\[
 \theta_y=\sigma e^{-y}-\frac12\sin2\theta,
 \qquad
 (\log r)_y=-R^{-2}-\sin^2\theta.
 \tag{6.3}
\]

On \(0\le y\le1\), the number of target roots is

\[
 \#\{U=0\}
 =\frac{1-e^{-1}}\pi\sigma+O(1).
 \tag{6.4}
\]

With the projected rows

\[
 h=-ce^{-y}V,
 \qquad b=-c^2e^{-2y}U,
 \qquad QF=-2R^2h,
 \tag{6.5}
\]

fast-phase averaging gives

\[
 G_{\rm Gal}\asymp a^2\sigma,
 \qquad
 \mathcal C_{\times,{\rm Gal}}\asymp a^2\sigma,
 \qquad
 \mathcal E_{Q,{\rm Gal}}\asymp a^2.
 \tag{6.6}
\]

This is a rigorous statement about the projected ODE.  It is not a
triangular Navier--Stokes counterexample.

### Proposition 6.1 -- no finite Fourier-support embedding

For every nonzero real-carrier convolution (1.2), there is no nonzero finite
coordinate-support invariant subspace of the full Fourier lattice.

#### Proof

Let \(r_*\) be the largest positive carrier and let \(s_*\) be the largest
active index of a nonzero finitely supported vector \(F\).  At the output
index \(s_*+r_*\), the unique extremal convolution term is a nonzero
constant times \(w_{r_*}F_{s_*}\).  Every smaller carrier would require an
input index larger than \(s_*\), and the conjugate direction also lies
outside the support.  Hence \(VF\) leaves the proposed finite support.
\(\square\)

For the single-carrier operator \(W_R=V_R(0)\), the first leakage is already
order one:

\[
 W_Re_0=-i\sqrt2a\,u_R,
 \tag{6.7}
\]

\[
 W_Ru_R=-i\sqrt2a\,e_0
 -\frac{ia}{\sqrt2}(e_{2R}+e_{-2R}).
 \tag{6.8}
\]

Therefore

\[
 \frac{\|(I-P_{\mathcal H_R})W_Ru_R\|}
 {\|P_{\mathcal H_R}W_Ru_R\|}
 =\frac1{\sqrt2}.
 \tag{6.9}
\]

On one coupling time, the shell deleted by the projection has \(O(1)\)
amplitude before a large number of projected rotations can occur.  This
exactly identifies the missing mechanism: full-lattice cascade can raise
\(K\), raise the action, or reduce later target slopes.  A Galerkin
divergence cannot decide which occurs.

This boundary is consistent with Moffatt's comparison of isolated triad
truncations and exact Euler evolution: preservation of a few quadratic
invariants does not make the truncated orbit an exact fluid orbit.

---

## 7. A shell-count-free multiscale raw estimate

The same joint-exposure argument has a useful multiscale form.  Split the
carriers into dyadic shells \(R_j\le|r_l|<2R_j\), and assume

\[
 \rho_j(x)^2\lesssim\sigma_j^2e^{-cR_j^2x},
 \qquad
 \|V_j(x)\|\lesssim\beta_je^{-cR_j^2x}.
 \tag{7.1}
\]

Then energy contraction gives

\[
 \mathcal C_\times
 \lesssim |\delta|E_0
 \sum_{j,k}\frac{\sigma_j^2\beta_k}{R_j^2+R_k^2}.
 \tag{7.2}
\]

Since

\[
 \frac{R_jR_k}{R_j^2+R_k^2}\lesssim2^{-|j-k|},
 \tag{7.3}
\]

the discrete Schur--Young inequality yields

\[
\boxed{
 \mathcal C_\times
 \lesssim |\delta|E_0
 \left(\sum_j\frac{\sigma_j^4}{R_j^2}\right)^{1/2}
 \left(\sum_k\frac{\beta_k^2}{R_k^2}\right)^{1/2}.}
\tag{7.4}
\]

The constant is independent of the number of occupied shells.  Similarly,

\[
 m_*\lesssim
 \sum_j\frac{\sigma_j^2R_j^{4/3}}{1+\log R_j}.
 \tag{7.5}
\]

Equations (7.4)--(7.5) remove an uncontrolled shell-count factor from the
raw continuous ledger.  They do not yet absorb all three explicit shell
moments into one global \(D^{1/3}\Lambda_{1,*}\) payment.

---

## 8. Finite two-route audit

The proof above is analytic.  Two deterministic finite implementations
separately corroborate its exponent algebra, scalar optimizations, local
floor scaling, Galerkin asymptotics, and full-lattice leakage identity.

The producer route uses exact rational exponent arithmetic, Cartesian
\((U,V)\) RK4 for the projected oscillator, and explicit convolution
dictionaries.  It passes all 16 declared checks over 48 scalar optimization
cases, 10 local-floor cases, 12 closure-window cases, and 10 Galerkin cases.

The independent route rewrites the scalar formulas and integrates the polar
\((\theta,\log r)\) system.  It reads no producer output.  It passes all 10
declared checks.  At \(R=16,\sigma=512\), both routes find 103 target roots.
The producer ratios to the fast-phase formulas are

\[
 1.0048622\quad(G_{\rm Gal}),\qquad
 0.9990459\quad(\mathcal C_{\times,\rm Gal}),\qquad
 1.0016977\quad(\mathcal E_{Q,\rm Gal}).
 \tag{8.1}
\]

Across all projected cases, the largest producer-independent relative
difference is \(7.11\times10^{-5}\).  Both routes recover the exact leakage
ratio \(1/\sqrt2\).  Every file in the 25-item certificate ledger passes its
recorded SHA-256 check.

These are finite binary64 audits, not interval proofs.  The local-floor
samples normalize an unknown absolute constant to one, and the closure
sequences illustrate scaling rather than prove convergence.  The Galerkin
oscillator is not DNS and is not a full-lattice counterexample.

---

## 9. Literature and novelty boundary

The declared velocity class is an exact 2D3C reduction: the in-plane shear
solves a two-dimensional equation and the transverse component solves a
passive advection--diffusion equation.  This exact PDE reduction, rather
than a Galerkin closure, is the reason the full-lattice statements above are
legitimate.  Biferale, Buzzicotti, and Linkmann discuss the general 2D3C
structure and its relation to three-dimensional turbulence
([Physics of Fluids 29, 111101](https://doi.org/10.1063/1.4990082)).

The strong-coupling window should be compared only conceptually with the
small-critical-data theorem of Koch and Tataru
([Advances in Mathematics 157 (2001)](https://doi.org/10.1006/aima.2000.1937)).
The present result does not enlarge their theorem and is confined to a much
narrower exact class.

Logarithmic improvements can matter at regularity endpoints; Chan and
Vasseur proved one such improvement of the Prodi--Serrin criterion
([Methods and Applications of Analysis 14 (2007)](https://doi.org/10.4310/MAA.2007.v14.n2.a5)).
Their space-time functional is not the project-specific temporal
critical-log action, so the two criteria are not interchangeable.

The most concrete bridge to the Clay problem remains the
Escauriaza--Seregin--Sverak endpoint theorem
([Russian Mathematical Surveys 58 (2003)](https://doi.org/10.1070/RM2003v058n02ABEH000609)).
The current ledger has not been shown to imply
\(u\in L^\infty_tL^3_x\), or any other general three-dimensional
continuation criterion.

Moffatt's exact-versus-truncated triad comparison
([Journal of Fluid Mechanics 741 (2014)](https://doi.org/10.1017/jfm.2013.637))
supports the non-portability warning in Section 6.  Tao's averaged
Navier--Stokes blowup theorem
([JAMS 29 (2016)](https://doi.org/10.1090/jams/838)) gives a separate,
broader warning: energy cancellation and generic harmonic-analysis bounds
alone do not capture all structure of the genuine Navier--Stokes
nonlinearity.

I found no paper in the bounded primary-source search that states (0.5)--
(0.9) in this notation or this exact triangular setting.  I do not infer
priority from that search.  The result is presented as a theorem internal to
the declared project framework, with its proof and audit trail exposed.

---

## 10. Claim boundary

R0.72L proves:

1. a complete-root physical upper bound that retains the actual enstrophy
   contrast and actual critical-log action for every coupling strength in
   the declared common-band triangular class;
2. an exact local root and action floor at arbitrary common-band exposure
   scale for the fixed-background, phase-aligned, row-aligned, exactly
   corrected launch;
3. uniform closure throughout the growing moderate strong-coupling window
   (0.9), with decay under its little-o form;
4. a finite-Galerkin strong-coupling countertheorem together with an exact
   proof that the projected orbit cannot embed in the full Fourier lattice;
5. a shell-count-free dyadic Schur estimate for the raw multiscale cubic row.

It does not prove:

1. closure for \(\varepsilon\gg p^{2/3}R^{2/3}L_R\);
2. a quantitative full-lattice enhanced-dissipation theorem in that extreme
   regime;
3. physical absorption of every multiscale moment in (7.4)--(7.5);
4. a continuation criterion for arbitrary three-dimensional solutions;
5. finite-time singularity or global smoothness for general Navier--Stokes.

The Clay Millennium problem remains open.

---

## 11. Next exact gate

R0.72M should attack the explicit remainder (0.10).  The first useful target
is a full-lattice alternative of the form

\[
 K\gtrsim\varepsilon^{7/3}p^{4/3}
 \quad\text{or}\quad
 x\gtrsim\varepsilon^{7/3}p^{4/3}
 \quad\text{or}\quad
 \mathcal C_\times=o(\varepsilon a^2N^2),
 \tag{11.1}
\]

with constants uniform in the common band.  This is the point at which
Fourier cascade and enhanced dissipation must be quantified rather than
named.  The multiscale Schur ledger (7.4) remains the parallel interface
after that extreme strong-coupling audit.
