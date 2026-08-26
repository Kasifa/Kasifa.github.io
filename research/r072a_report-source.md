# R0.72A -- local-exposure strong-coupling closure and an exact Bessel obstruction

**Date:** 2026-08-27  
**Status:** analytic derivation and two independent finite audits passed. The statements are
restricted to the real-shear, fixed-target, triangular Fourier-lattice class
inherited from R0.71W--Z. They do not prove a universal Navier--Stokes
endpoint estimate, a continuation criterion, finite-time blow-up, or global
regularity.

**Keywords:** Navier--Stokes regularity, triangular 2.5D flows, shrinking
observation layers, strong coupling, bounded variation, Bessel functions,
Fourier lattices, exact temporal roots

---

## 0. Direct decision

R0.71Z bounded the complete squared slope mass of one target coordinate by

\[
 G_{\rm all}^{\rm ex}
 \le e^{2\lambda_0L}M\Omega^2(4+C_\kappa\eta),
 \qquad \eta=|\delta|\Omega .
 \tag{0.1}
\]

The factor \(C_\kappa\eta\) came from replacing the exposure on the actual
observation interval by the exposure on the whole future half-line. Keeping
the local integral instead gives the sharper quantity

\[
 \ell_2(I_x)
 :=\Omega^{-2}\int_{I_x}\|V_z(x)\|^2\,dx,
 \qquad
 0\le \ell_2(I_x)\le\min\{L,C_\kappa\},
 \tag{0.2}
\]

and the exact all-root estimate

\[
 \boxed{
 G_{\rm all}^{\rm ex}(I_x)
 \le e^{2\lambda_0L}M\Omega^2
 \bigl[1+q_I+\eta\ell_2(I_x)\bigr],}
 \tag{0.3}
\]

where

\[
 q_I=(\Omega\sqrt M)^{-1}
 \int_{I_x}|Q(x)F(x)|\,dx\le3.
 \tag{0.4}
\]

Consequently the launch-inclusive normalized ledger satisfies

\[
 \boxed{
 \frac{\mathcal J_{\rm all}(I_t)}
 {D^{1/3}\Lambda_1(K_t;u)}
 \le C\nu^{-2}e^{2\lambda_0L}
 \frac{\eta^{4/3}}{M^2}
 \bigl[4+\eta\min\{L,C_\kappa\}\bigr].}
 \tag{0.5}
\]

This changes the strong-coupling phase boundary. For a sequence

\[
 \eta_M=M^\alpha,
 \qquad L_M=M^{-\beta},
 \tag{0.6}
\]

the right side of (0.5) tends to zero whenever

\[
 \boxed{
 \alpha<\min\left\{\frac32,\frac{6+3\beta}{7}\right\}.}
 \tag{0.7}
\]

The old fixed-length threshold \(\alpha<6/7\) is the case \(\beta=0\).
When the layer shrinks fast enough that \(\eta_ML_M=O(1)\), the certified
range reaches every \(\alpha<3/2\). The present worst-case envelope cannot
certify decay beyond \(3/2\), because the first-root term still costs
\(\eta^{4/3}M^{-2}\).
Both boundaries describe where an upper bound ceases to vanish; neither is a
singularity construction.

There is also an endpoint closure at launch. For the finite-support initial
vectors used in the construction, the target coordinate has the required
regularity already at \(x=0\). Hence (0.3)--(0.5) hold uniformly for
\(A_0\ge0\). When observation starts at launch, \(A=A_0=0\), the payment
interval

\[
 K_t=[a-A_0q^{-2},b]
 \tag{0.8}
\]

is exactly the counted interval \(I_t=[a,b]\). The launch enstrophy then
cancels the contrast factor without an enlarged window, matched background,
or separate retention hypothesis.

Strong-coupling dependence cannot, however, be deleted altogether. Inside
the exact infinite Fourier lattice, a one-carrier family with
\(\delta_R=R^4\) and \(L_R\asymp R^{-3}\) has \(R\) positive exact target
roots and

\[
 \boxed{
 G_R^{\rm sel}=\frac8{\pi^2}\log R+O(1),
 \qquad
 G_{R,\rm all}^{\rm ex}([0,L_R])\ge1+G_R^{\rm sel}.}
 \tag{0.9}
\]

The extra (1) is the row mass at the exact launch root \(\tau=0\); no
claim is made that the selected positive roots exhaust the complete root
set. The limiting target is \(J_1(2\tau)\). Thus an \(\eta\)-independent all-root
slope-mass constant is false even for one real shear carrier, although the
known gap between logarithmic growth and the upper envelope
\(O(1+\eta L)\) remains large. No conclusion about divergence of the
normalized Navier--Stokes ledger is drawn from this family, and it is not a
blow-up example.

---

## 1. Exact Fourier-lattice setting, including launch

Fix viscosity \(\nu>0\), target frequency \(k_*=(K_y,K_z)\) with
\(K_z\ne0\), carrier modulus \(d\ge1\), and pairwise distinct positive
integers \(r_1,\ldots,r_M\). The active scalar sector solves

\[
 \partial_xF=D_qF+\delta V_z(x)F,
 \qquad \delta=\frac P{q^2},
 \qquad \|F(0)\|_{\ell^2}^2=M,
 \tag{1.1}
\]

where the launch vector has finite support and unit-modulus nonzero
coefficients,

\[
 (D_qF)_r=-\lambda_{q,r}F_r,
 \qquad
 \lambda_{q,r}=\nu\left[
 \left(dr+\frac{K_y}{q}\right)^2+\frac{K_z^2}{q^2}
 \right],
 \tag{1.2}
\]

and, for real \(z_l\),

\[
 (V_z(x)F)_r
 =-iK_z\sum_{l=1}^Mz_le^{-\kappa r_l^2x}
 \left(F_{r-r_l}+F_{r+r_l}\right),
 \qquad \kappa=\nu d^2.
 \tag{1.3}
\]

For \(A_0\ge0\), let

\[
 \Omega=\sup_{x\ge A_0}\|V_z(x)\|_{\ell^2\to\ell^2},
 \qquad
 \eta=|\delta|\Omega,
 \qquad
 \lambda_0=\lambda_{q,0},
 \tag{1.4}
\]

and count roots on

\[
 I_x=[A,A+L]\subset[A_0,\infty).
 \tag{1.5}
\]

The real-shear hypothesis makes \(V_z(x)\) skew-adjoint. Therefore

\[
 \frac12\frac d{dx}\|F(x)\|_2^2
 =-\sum_r\lambda_{q,r}|F_r(x)|^2\le0,
 \tag{1.6}
\]

and

\[
 \|F(x)\|_2\le\sqrt M,
 \qquad
 \int_0^\infty\sum_r\lambda_{q,r}|F_r(x)|^2\,dx
 \le\frac M2.
 \tag{1.7}
\]

No coupling-dependent Gronwall factor appears.

### Lemma 1.1 -- regularity at \(A_0=0\)

For every fixed finite carrier set and finite-support launch vector, the
solution of (1.1) is classical from \(x=0\). In particular, on every finite
interval the target coordinate \(F_0\) is continuously differentiable,
\(F_0'\) is absolutely continuous, and the row identity in Section 3 holds
almost everywhere including an integrable right limit at launch.

#### Proof

For \(s\ge0\), equip the lattice with the polynomial weight
\((1+r^2)^{s/2}\). Every fixed shift \(T_{\pm r_l}\) is bounded on this
weighted space. The finite sum \(V_z(x)\), together with its time derivative,
is therefore bounded there on compact time intervals. The diagonal operator
\(D_q\) generates the same analytic contraction semigroup on every such
weighted space. A finite-support launch vector belongs to all of them.
Bounded nonautonomous perturbation theory, or equivalently the convergent
Dyson expansion in each weighted space, gives preservation of two diagonal
domains on finite intervals. Thus (1.1) may be differentiated once at
\(x=0\). Applying the bounded target row then gives the asserted scalar
regularity. The weighted norms may depend on the fixed carrier set; none is
used in the uniform estimates below. \(\square\)

This lemma is the only extra regularity input needed to set \(A_0=0\).
Positive-time analytic smoothing remains available when the launch vector is
merely in \(\ell^2\), but no such enlargement of the initial class is claimed
here.

---

## 2. Local multiplier exposure

Under Fourier transform on \(\ell^2(\mathbb Z)\), \(V_z(x)\) is multiplication
by

\[
 m_x(\theta)=-2iK_z\sum_{l=1}^M
 z_le^{-\kappa r_l^2x}\cos(r_l\theta).
 \tag{2.1}
\]

Normalized Haar orthogonality and heat-semigroup contraction give

\[
 \Omega^2\ge
 2K_z^2\sum_l|z_l|^2e^{-2\kappa r_l^2A_0},
 \qquad
 \|V_z(x)\|\le\Omega\quad(x\ge A_0).
 \tag{2.2}
\]

The half-line integral from R0.71Z remains valid at \(A_0=0\):

\[
 \int_{A_0}^\infty\|V_z(x)\|\,dx
 \le C_\kappa\Omega,
 \qquad
 C_\kappa=\frac{\pi^2}{\sqrt{45}\,\nu d^2},
 \tag{2.3}
\]

and hence

\[
 \int_{A_0}^\infty\|V_z(x)\|^2\,dx
 \le C_\kappa\Omega^2.
 \tag{2.4}
\]

For \(\Omega>0\), define the local quadratic exposure length

\[
 \ell_2(I_x)=\Omega^{-2}
 \int_{I_x}\|V_z(x)\|^2\,dx.
 \tag{2.5}
\]

Equations (2.2) and (2.4) prove

\[
 0\le\ell_2(I_x)\le\min\{L,C_\kappa\}.
 \tag{2.6}
\]

When \(\Omega=0\), the coupling row vanishes on the observation interval and
all target-root slopes vanish. In that case \(\ell_2=q_I=0\) by convention.

The distinction between \(L\) and \(C_\kappa\) is decisive. The former
records the local amount of fast rotation actually seen before observation
ends; the latter pays for the entire heat tail.

---

## 3. Local target-row payment

Put

\[
 h(x)=P_0V_z(x)F(x),
 \qquad
 F_0'=-\lambda_0F_0+\delta h.
 \tag{3.1}
\]

The combined differentiated row is

\[
 h'+\lambda_0h
 =Q(x)F+\delta P_0V_z(x)^2F,
 \qquad
 Q=P_0\left[V_z'+V_z(D_q+\lambda_0)\right].
 \tag{3.2}
\]

Assume

\[
 q\ge q_*:=\max\left(1,\frac{2|K_y|}{d}\right).
 \tag{3.3}
\]

The only nonzero inputs of \(Q\) are \(\pm r_l\). Weighted
Cauchy--Schwarz pairs one carrier derivative with one dissipative derivative
of \(F\) and yields, exactly as in R0.71Z,

\[
 \int_{A_0}^\infty|Q(x)F(x)|\,dx
 \le3\Omega\sqrt M.
 \tag{3.4}
\]

The proof uses

\[
 \int_{A_0}^\infty\sum_lr_l^2|z_l|^2
 e^{-2\kappa r_l^2x}\,dx
 \le\frac{\Omega^2}{4\kappa K_z^2}
 \tag{3.5}
\]

and the dissipation budget (1.7); it has no positive lower bound on
\(A_0\). Define

\[
 q_I=(\Omega\sqrt M)^{-1}
 \int_{I_x}|Q(x)F(x)|\,dx.
 \tag{3.6}
\]

Then

\[
 0\le q_I\le3.
 \tag{3.7}
\]

Retaining the local multiplier integral in the second term of (3.2) gives

\[
 \int_{I_x}|h'+\lambda_0h|\,dx
 \le\Omega\sqrt M
 \bigl[q_I+\eta\ell_2(I_x)\bigr].
 \tag{3.8}
\]

---

## 4. Local-exposure all-root theorem

### Lemma 4.1 -- derivative mass at scalar zeros

Let \(g\in C^1([a,b];\mathbb C)\) and let \(g'\) be absolutely continuous.
For any finite ordered subset of its zeros,

\[
 a\le\tau_1<\cdots<\tau_R\le b,
 \qquad g(\tau_j)=0,
 \tag{4.1}
\]

one has

\[
 \sum_{j=1}^R|g'(\tau_j)|^2
 \le |g'(\tau_1)|^2
 +\|g'\|_{L^\infty(a,b)}
 \int_a^b|g''(x)|\,dx.
 \tag{4.2}
\]

Indeed, the integral of \(g'\) between consecutive zeros is zero.
Integration by parts on each such interval gives

\[
 |g'(\tau_j)|
 \le\int_{\tau_{j-1}}^{\tau_j}|g''(x)|\,dx
 \qquad(j\ge2),
 \tag{4.3}
\]

and summation proves (4.2). The statement is valid for complex scalars and
has no root-count or root-separation factor.

### Theorem 4.2 -- complete local-exposure slope mass

Assume (1.1)--(1.5), real shear, finite-support launch, (3.3), and
\(A_0\ge0\). For every finite set of exact roots in \(I_x\),

\[
 \boxed{
 \sum_{F_0(\tau_j)=0}|F_0'(\tau_j)|^2
 \le e^{2\lambda_0L}\eta^2M
 \bigl[1+q_I+\eta\ell_2(I_x)\bigr].}
 \tag{4.4}
\]

If \(\delta\ne0\), then

\[
 \boxed{
 G_{\rm all}^{\rm ex}(I_x)
 :=\sum_{F_0(\tau)=0}|P_0V_z(\tau)F(\tau)|^2
 \le e^{2\lambda_0L}M\Omega^2
 \bigl[1+q_I+\eta\ell_2(I_x)\bigr].}
 \tag{4.5}
\]

Both inequalities hold for the extended nonnegative sum over the complete
root set. In particular,

\[
 G_{\rm all}^{\rm ex}(I_x)
 \le e^{2\lambda_0L}M\Omega^2
 \bigl[4+\eta\min\{L,C_\kappa\}\bigr].
 \tag{4.6}
\]

#### Proof

Set

\[
 g(x)=e^{\lambda_0(x-A)}F_0(x).
 \tag{4.7}
\]

Then

\[
 g'=\delta e^{\lambda_0(x-A)}h,
 \qquad
 g''=\delta e^{\lambda_0(x-A)}
 \left[QF+\delta P_0V_z^2F\right].
 \tag{4.8}
\]

Contraction gives

\[
 \|g'\|_\infty\le e^{\lambda_0L}\eta\sqrt M,
 \tag{4.9}
\]

while (2.5) and (3.6) give

\[
 \int_{I_x}|g''(x)|\,dx
 \le e^{\lambda_0L}\eta\sqrt M
 \bigl[q_I+\eta\ell_2(I_x)\bigr].
 \tag{4.10}
\]

Lemma 4.1 proves (4.4). At a target root,
\(F_0'=\delta h\); division by \(\delta^2\) gives (4.5). Every finite subset
has the same upper bound, so monotone supremum gives the complete extended
sum. Equations (2.6) and (3.7) give (4.6). \(\square\)

The theorem does not count roots. Multiple roots have zero slope. If the
target coordinate vanishes identically, its slope measure is identically
zero.

---

## 5. Launch-inclusive normalized ledger and phase diagram

For this normalized ledger, specialize to observation beginning at the
reference layer, \(I_x=[A_0,A_0+L]\). If \(\Omega=0\), the finite heat sum
has \(z_l=0\) for every carrier, the target charge is zero, and the claim is
trivial. If \(\delta=0\) or the shear amplitude \(S=0\), the inherited atom
formula has factor \(S^2P^2\) and \(\mathcal J_{\rm all}=0\), so the claim is
again trivial. Hence assume \(\Omega>0\), \(K_v>0\), \(\delta\ne0\), and
\(S\ne0\) below.

Roots are counted on \(I_t=[a,b]\). Let

\[
 K_t=[\sigma_q,b],
 \qquad \sigma_q=a-A_0q^{-2},
 \tag{5.1}
\]

and compute

\[
 \Lambda_1(K_t;u)=\mathcal R_Y(K_t)
 \left[\nu^2+\frac1{|K_t|}\int_{K_t}
 \frac{\|\mathbb P(u\times\omega)\|_{\dot H^{-1}}^2}{Y(t)}\,dt
 \right].
 \tag{5.2}
\]

For a nontrivial classical solution with
\(0<\inf_{K_t}Y\le\sup_{K_t}Y<\infty\), every counted root satisfies

\[
 \frac1{Y(t_*)\mathcal R_Y(K_t)}
 =\frac{\inf_{K_t}Y}{Y(t_*)\sup_{K_t}Y}
 \le\frac1{\sup_{K_t}Y}.
 \tag{5.3}
\]

Launch Parseval and the data ledger give

\[
 \sup_{K_t}Y\ge Y(\sigma_q)\ge c_Yq^2E,
 \qquad
 D\ge c_Dq^2E,
 \tag{5.4}
\]

where

\[
 E=S^2K_s+P^2K_v,
 \quad
 K_s=\sum_{l=1}^Mr_l^2,
 \quad
 K_v=\sum_{l=1}^Mr_l^2|z_l|^2.
 \tag{5.5}
\]

Repeating the exact amplitude optimization of R0.71Z, but inserting (4.5)
before the final simplification, gives

\[
 \frac{\mathcal J_{\rm all}(I_t)}
 {D^{1/3}\Lambda_1(K_t;u)}
 \le C\nu^{-2}e^{2\lambda_0L}
 \frac M{K_s}\eta^{4/3}
 \left(\frac{\Omega^2}{K_v}\right)^{1/3}
 \bigl[1+q_I+\eta\ell_2(I_x)\bigr].
 \tag{5.6}
\]

For distinct positive integer carriers,

\[
 K_s\ge\frac{M(M+1)(2M+1)}6,
 \qquad
 \frac{\Omega^2}{K_v}\le\frac{2\pi^2K_z^2}{3}.
 \tag{5.7}
\]

Thus

\[
 \boxed{
 \frac{\mathcal J_{\rm all}(I_t)}
 {D^{1/3}\Lambda_1(K_t;u)}
 \le C\nu^{-2}e^{2\lambda_0L}
 M^{-2}\eta^{4/3}
 \bigl[4+\eta\min\{L,C_\kappa\}\bigr].}
 \tag{5.8}
\]

The constant is independent of \(M,q,r_l,z_l,S,P\), the root count, root
separation, and \(A_0\). It depends on the fixed target normalization and the
declared values of \(\nu,d,K_z\). A sequence is uniform when
\(\lambda_0L\) remains bounded.

### Corollary 5.1 -- joint strong coupling and shrinking layer

Suppose \(M\to\infty\), \(\eta_M\to\infty\), \(L_M\to0\), and
\(\sup_M\lambda_{0,M}L_M<\infty\). If

\[
 M^{-2}\eta_M^{4/3}\longrightarrow0,
 \qquad
 M^{-2}\eta_M^{7/3}L_M\longrightarrow0,
 \tag{5.9}
\]

then the complete normalized ratio in (5.8) tends to zero. Equivalently,

\[
 M^{-2}\eta_M^{4/3}(1+\eta_ML_M)\longrightarrow0
 \tag{5.10}
\]

is sufficient.

For the power law (0.6), (5.9) is exactly (0.7). At the equality lines the
bound is only order one; no converse is asserted.

### Corollary 5.2 -- exact launch window

When observation begins at launch, \(A=A_0=0\), (5.1) gives
\(K_t=I_t\). Therefore (5.8) is a floor-free estimate on the original
observation interval itself. This statement is
not extended to every positive \(A_0\): even arbitrarily short positive
pre-observation layers can erase arbitrarily high-frequency launch
enstrophy. The exact endpoint and the positive-layer limit must not be
conflated.

---

## 6. Exact one-carrier Bessel family

The local upper theorem leaves open whether any strong-coupling dependence is
real or merely an artifact of bounded variation. The following family
settles that narrow question inside the exact infinite lattice.

Set

\[
 \nu=d=q=K_z=z_1=1,
 \qquad K_y=0,
 \qquad r_1=1,
 \tag{6.1}
\]

so

\[
 (D F)_r=-(r^2+1)F_r,
 \qquad
 V(x)=-ie^{-x}(T_1+T_{-1}),
 \qquad \Omega=2.
 \tag{6.2}
\]

Choose the unit launch

\[
 F(0)=i e_{-1}.
 \tag{6.3}
\]

For an integer \(R\ge1\), set

\[
 \delta_R=R^4,
 \qquad
 U_R(\tau)=F(\tau/\delta_R).
 \tag{6.4}
\]

Then

\[
 U_R'=\delta_R^{-1}DU_R+V(\tau/\delta_R)U_R.
 \tag{6.5}
\]

The frozen limit is

\[
 W'=V(0)W,
 \qquad W(0)=ie_{-1}.
 \tag{6.6}
\]

Using the lattice Fourier transform and the Jacobi--Anger expansion,

\[
 W(\theta,\tau)=ie^{-i\theta}e^{-2i\tau\cos\theta},
 \qquad
 P_0W(\tau)=J_1(2\tau).
 \tag{6.7}
\]

### Lemma 6.1 -- growing-window frozen approximation

There is an absolute \(C\) such that, for \(T\ge1\),

\[
 \sup_{0\le\tau\le T}\|U_R(\tau)-W(\tau)\|_2
 +\sup_{0\le\tau\le T}
 \left|P_0U_R'(\tau)-2J_1'(2\tau)\right|
 \le \frac{C(1+T^3)}{\delta_R}.
 \tag{6.8}
\]

#### Proof

Let \(E=U_R-W\). Dissipativity of \(D\) and skew-adjointness of
\(V(\tau/\delta_R)\) give

\[
 \frac d{d\tau}\|E\|_2
 \le\delta_R^{-1}\|DW\|_2
 +\|V(\tau/\delta_R)-V(0)\|\,\|W\|_2.
 \tag{6.9}
\]

The explicit Fourier formula (6.7) gives

\[
 \|DW(\tau)\|_2\le C(1+\tau^2),
 \tag{6.10}
\]

while

\[
 \|V(\tau/\delta_R)-V(0)\|
 =2\left(1-e^{-\tau/\delta_R}\right)
 \le2\tau/\delta_R.
 \tag{6.11}
\]

Integration proves the first term in (6.8). For the target derivative, use

\[
 P_0U_R'=-\delta_R^{-1}P_0U_R
 +P_0V(\tau/\delta_R)U_R
 \tag{6.12}
\]

and compare it with \(P_0W'=P_0V(0)W\). Contraction, (6.11), and the first
estimate prove the second term. \(\square\)

The target coordinate is real for all \(\tau\). One direct verification is
to write \(F_r=(-i)^rg_r\); the transformed lattice system has real
coefficients and \(g(0)=e_{-1}\).

### Theorem 6.2 -- logarithmic exact-root obstruction

Let \(j_{1,k}\) denote the \(k\)-th positive zero of \(J_1\), and put

\[
 \tau_k=\frac{j_{1,k}}2,
 \qquad
 T_R=\tau_R+\rho,
 \tag{6.13}
\]

where \(\rho>0\) is a sufficiently small fixed number. For all sufficiently
large \(R\), one can select a simple real zero
\(s_{k,R}\in(\tau_k-\rho,\tau_k+\rho)\) of the exact target \(P_0U_R\)
for every \(1\le k\le R\). In
the original variable,

\[
 x_{k,R}=s_{k,R}/\delta_R,
 \qquad
 0<x_{k,R}<L_R:=T_R/\delta_R=O(R^{-3}).
 \tag{6.14}
\]

Moreover,

\[
 \boxed{
 G_R^{\rm sel}:=\sum_{k=1}^R
 |P_0V(x_{k,R})F(x_{k,R})|^2
 =\frac8{\pi^2}\log R+O(1).}
 \tag{6.15}
\]

#### Proof

The standard large-zero and derivative asymptotics give

\[
 j_{1,k}=\pi\left(k+\frac14\right)+O(k^{-1}),
 \qquad
 J_1'(j_{1,k})^2=\frac2{\pi^2k}+O(k^{-2}).
 \tag{6.16}
\]

Choose \(\rho\) smaller than a fixed fraction of the minimum zero spacing.
The same asymptotics, with the finitely many initial zeros absorbed into the
constants, imply opposite endpoint signs and

\[
 |J_1(2(\tau_k\pm\rho))|\ge c k^{-1/2},
 \qquad
 |2J_1'(2\tau)|\ge c k^{-1/2}
 \tag{6.17}
\]

through a smaller neighborhood of \(\tau_k\).

Since \(T_R=O(R)\), Lemma 6.1 and \(\delta_R=R^4\) give a uniform
\(C^1\) error \(O(R^{-1})\). This is \(o(R^{-1/2})\), so the intermediate
value theorem and derivative sign stability give one simple exact root in
each neighborhood. Quantitative inversion at a simple zero gives

\[
 |s_{k,R}-\tau_k|\le C\frac{\sqrt{k}}R.
 \tag{6.18}
\]

At an exact target root, the diagonal target term in (6.12) vanishes, hence

\[
 P_0V(x_{k,R})F(x_{k,R})=P_0U_R'(s_{k,R}).
 \tag{6.19}
\]

The Bessel differential equation and (6.18) show that replacing
\(s_{k,R}\) by \(\tau_k\) changes the derivative by \(O(R^{-1})\), uniformly
for \(k\le R\). Together with Lemma 6.1,

\[
 P_0U_R'(s_{k,R})
 =2J_1'(j_{1,k})+O(R^{-1}).
 \tag{6.20}
\]

Squaring and summing creates an error bounded by
\(CR^{-1}\sum_{k\le R}k^{-1/2}+CR^{-1}=O(R^{-1/2})\). Finally, (6.16) and
the harmonic-sum asymptotic give

\[
 \sum_{k=1}^R[2J_1'(j_{1,k})]^2
 =\frac8{\pi^2}\log R+O(1),
 \tag{6.21}
\]

which proves (6.15). \(\square\)

Here

\[
 \eta_R=|\delta_R|\Omega=2R^4.
 \tag{6.22}
\]

The launch time is another exact target root:
\(P_0U_R(0)=0\) and \(P_0U_R'(0)=P_0V(0)ie_{-1}=1\). Therefore (6.15) also
gives
\(G_{R,\rm all}^{\rm ex}([0,L_R])\ge1+G_R^{\rm sel}
\ge c\log\eta_R\). Additional exact roots, if present, only increase this
complete nonnegative mass. The family proves
only that strong-coupling dependence is necessary. It does not saturate
the local upper bound, whose extra term is \(\eta_RL_R=O(R)\), and it does
not challenge the \(M\to\infty\) suppression because here \(M=1\).

---

## 7. Relation to enhanced-dissipation literature

Fourier transformation in the lattice index rewrites the exact system as a
diffusion equation with a large imaginary, heat-decaying trigonometric
potential. For a fixed nonconstant profile and fixed positive time,
large-coupling theory generally predicts enhanced dissipation rather than a
persistent escape. Quantitative rates depend on critical-point degeneracy and
sublevel-set constants.

These results control semigroup norms at the observation time; they do not
directly control coordinate zeros or slope mass accumulated before that time.

The regime not covered uniformly by that literature is precisely the joint
limit used here:

\[
 |\delta_M|\to\infty,
 \qquad L_M\to0,
 \tag{7.1}
\]

possibly with profile frequencies, heat-decay rates, and degeneracy changing
with \(M\). R0.72A therefore does not treat strong coupling as a scalar
parameter in isolation. Future certificates must record at least

\[
 \bigl(\eta_M,L_M,n_M,c_{{\rm sub},M},
 L_M\kappa r_{\max,M}^2\bigr),
 \tag{7.2}
\]

where \(n_M\) is the largest critical-point degeneracy and
\(c_{{\rm sub},M}\) represents quantitative sublevel control.

The Bessel family lies below the adjacent enhanced-dissipation comparison time
scale. It records coherent coordinate oscillation before shear mixing
transfers substantial mass to diffusively damped frequencies. For the frozen
profile \(b(\theta)=2\cos\theta\), \(n_0=1\), and \(\delta_R=R^4\), the
Bedrossian--Coti Zelati comparison rate is
\(\lambda_{{\rm ED},R}\asymp R^2/(\log R)^2\), whereas
\(L_R\asymp R^{-3}\), so \(L_R\lambda_{{\rm ED},R}\to0\). This is an
autonomous frozen-profile comparison, not a theorem for the nonautonomous
system studied here. It is not evidence against fixed-profile, fixed-time
enhanced dissipation.

---

## 8. Computational certificates

The analytic proof is primary. The release contains two independent finite
audits.

1. The producer recomputes the exact power-law phase boundary, local
   exposure factor, Bessel zero mass, finite-lattice strong-coupling roots,
   root shifts, and \(L_R\asymp R^{-3}\) scaling.
2. The independent program imports neither the producer nor its output. It
   uses a separate fixed-step exponential midpoint evolution and independent
   bracketing of target zeros, then checks the same asymptotic quantities and
   the launch regularity identities.

The finite matrices have an explicit spectral-radius margin, and the radius
is doubled as a truncation audit. These calculations corroborate the exact
algebra and asymptotic proof. They do not replace the infinite-lattice
argument, certify a full three-dimensional DNS, or prove a general NSE
statement.

---

## 9. Claim--evidence boundary

### Proved

1. The R0.71Z all-root theorem is valid from \(A_0=0\) for finite-support
   launch vectors; its constants are uniform for \(A_0\ge0\).
2. The global factor \(C_\kappa\eta\) localizes to
   \(\eta\ell_2(I_x)\le\eta\min\{L,C_\kappa\}\).
3. The normalized launch-inclusive ratio obeys (5.8), without root count or
   root separation.
4. The joint strong-coupling/shrinking-layer sufficient condition is (5.9),
   with the phase region (0.7).
5. At exact launch, \(K_t=I_t\), so the original interval obtains floor
   cancellation without retention loss.
6. A one-carrier exact infinite-lattice family has \(R\) persistent Bessel
   roots in a layer \(O(R^{-3})\) and logarithmically growing slope mass.

### Not proved

1. Sharpness of the local upper loss \(1+\eta L\); the exact lower family is
   only logarithmic.
2. Failure of the normalized \(D^{1/3}\Lambda_1\) estimate in any regime.
3. A strong-coupling construction with \(M\to\infty\) that defeats the
   \(M^{-2}\) lattice factor.
4. A uniform enhanced-dissipation theorem for heat-decaying profiles whose
   frequencies and degeneracies change with \(M\).
5. Floor-free retention on every positive pre-observation layer.
6. Non-unit or sparse launch phases, complex shear, nontriangular feedback,
   or a universal three-dimensional Navier--Stokes endpoint theorem.
7. A continuation criterion, finite-time singularity, or global regularity.

---

## 10. Research value and next finite gate

R0.72A removes two ambiguities left by R0.71Z. First, the strong-coupling
loss is controlled by local exposure rather than the entire future heat
tail. This creates a quantitatively larger vanishing region and closes the
launch endpoint. Second, an exact Bessel family proves that all strong-
coupling dependence cannot be erased by a better estimate.

The value to the Millennium problem remains indirect. The result eliminates
one candidate escape mechanism only inside a triangular 2.5D class and
identifies the precise double scale that a more serious construction would
have to exploit. It does not constrain every three-dimensional vortex-
stretching geometry.

The next finite gate is R0.72B. It should keep the exact local-exposure
ledger and test whether the logarithmic lower family can be promoted to a
many-carrier sequence while retaining the full nonlinear rotational charge.
Every candidate must record profile degeneracy, the enhanced-dissipation
comparison scale, the heat-freezing error, and the exact root payment. A
negative result with a uniform exclusion theorem is as valuable as a
construction; neither outcome is recorded before proof and independent
certificate agree.
