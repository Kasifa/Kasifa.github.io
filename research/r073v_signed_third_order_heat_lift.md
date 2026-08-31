# R0.73V analytic derivation: a pressure-aware signed heat lift and the \(3\to4\) boundary

**Status:** parent derivation, independent analytic audit, sealed two-path
finite certificate, and immutable formal-figure source seal complete; the
publication gate remains open

**Ordinary translation path:** `LOCAL_DIRECT_NO_DGX`

## 1. Setting and conventions

Work on the normalized periodic torus.  Let \(u\) be a smooth real
mean-zero divergence-free solution on its smooth lifespan:

\[
 \partial_tu+(u\cdot\nabla)u+\nabla p=\nu\Delta u,
 \qquad \nabla\cdot u=0.
 \tag{1.1}
\]

The mean-zero pressure is fixed by

\[
 -\Delta p=\partial_i\partial_j(u_i u_j).
 \tag{1.2}
\]

Put

\[
 P_s=e^{s\Delta},\qquad v_s=P_su,\qquad
 \Theta_s=P_s(u\otimes u),\qquad
 \tau_s=\Theta_s-v_s\otimes v_s.
 \tag{1.3}
\]

The Leray bilinear operator and the Navier--Stokes nonlinearity are

\[
 \mathcal B(a,b)=\mathbb P\nabla\!\cdot(a\otimes b),
 \qquad N=\mathcal B(u,u).
 \tag{1.4}
\]

Here \((a\otimes b)_{ik}=a_i b_k\), so

\[
 N=(u\cdot\nabla)u+\nabla p,qquad
 \partial_tu=\nu\Delta u-N.
 \tag{1.5}
\]

For \(a\odot b=a\otimes b+b\otimes a\), define

\[
 N_s=P_sN=\mathbb P\nabla\!\cdot\Theta_s,
 \tag{1.6}
\]

\[
 \mathcal C_s=P_s(u\odot N),\qquad
 \chi_s=\mathcal C_s-v_s\odot N_s.
 \tag{1.7}
\]

The field \(\mathcal C_s\) is the complete odd cubic contribution to the
quadratic tensor tangent.  The centered field \(\chi_s\) is its generalized
heat cross-covariance after the resolved product \(v_s\odot N_s\) is
removed.

## 2. A semigroup product lemma

Let \(L_s=\partial_s-\Delta\).  If \(A_s=P_sf\) and \(B_s=P_sg\), then

\[
 L_s(A_sB_s)=-2\nabla A_s\cdot\nabla B_s.
 \tag{2.1}
\]

If \(D_s=P_sh\), then

\[
 \begin{aligned}
 L_s(A_sB_sD_s)=-2\big(&D_s\nabla A_s\cdot\nabla B_s
 +B_s\nabla A_s\cdot\nabla D_s\\
 &+A_s\nabla B_s\cdot\nabla D_s\big).
 \end{aligned}
 \tag{2.2}
\]

Both identities are the ordinary Laplacian product rule.  They are valid
componentwise for vectors and tensors.

For

\[
 \tau_s(f,g)=P_s(fg)-P_sf\,P_sg,
 \tag{2.3}
\]

equation (2.1) gives the exact covariance identity

\[
 \boxed{
 L_s\tau_s(f,g)=2\nabla P_sf\cdot\nabla P_sg,
 \qquad \tau_0(f,g)=0.}
 \tag{2.4}
\]

This lemma is an identity in the filter variable for fields frozen at the
current physical time.  It is not a physical-time closure.

## 3. The equation-slot-compressed signed lift

Both \(P_s(u\odot N)\) and its components solve the free heat equation in
\(s\).  Applying (2.4) to each component of \(u\odot N\) gives

\[
 \boxed{
 (\partial_s-\Delta)\chi_s
 =2\sum_{\ell=1}^3
 \partial_\ell v_s\odot\partial_\ell N_s,
 \qquad \chi_0=0.}
 \tag{3.1}
\]

Consequently,

\[
 \boxed{
 \chi_s=2\int_0^sP_{s-r}\left[
 \sum_\ell\partial_\ell v_r\odot\partial_\ell N_r
 \right]dr.}
 \tag{3.2}
\]

Since \(N_r=\mathbb P\nabla\cdot\Theta_r\), the source in (3.2) is a
functional of the lower signed heat path \((v_r,\Theta_r)_{0\le r\le s}\).
This is a downward-triangular scale identity.  It is not a same-scale
algebraic law because the integral uses all smaller heat scales.

The tensor product equation from (1.5) is

\[
 \partial_t(u\otimes u)
 =\nu\Delta(u\otimes u)
 -2\nu\sum_\ell\partial_\ell u\otimes\partial_\ell u
 -u\odot N.
 \tag{3.3}
\]

Therefore, with

\[
 G_s=P_s\sum_\ell\partial_\ell u\otimes\partial_\ell u,
 \tag{3.4}
\]

the exact heat-plane law is

\[
 \boxed{
 (\partial_t-\nu\partial_s)\Theta_s
 =-2\nu G_s-v_s\odot N_s-\chi_s.}
 \tag{3.5}
\]

Thus \(\chi_s\) fills exactly the odd cubic slot exposed in R0.73U.  The
even derivative moment \(G_s\) remains.  If the full scale path is retained,
then the R0.73U covariance equation gives

\[
 G_s={1\over2}P_s\left[
 \left.\partial_r\tau_r\right|_{r=0}\right].
 \tag{3.6}
\]

This observation uses a bottom-scale derivative.  It is not a stable
single-positive-scale constitutive formula.

## 4. Transparent velocity and pressure cumulants

The raw local third moment is

\[
 M_{ijk,s}=P_s(u_i u_j u_k).
 \tag{4.1}
\]

Define the third generalized heat cumulant

\[
 \begin{aligned}
 \kappa_{ijk,s}={}&M_{ijk,s}
 -v_{s,i}\Theta_{jk,s}-v_{s,j}\Theta_{ik,s}
 -v_{s,k}\Theta_{ij,s}\\
 &+2v_{s,i}v_{s,j}v_{s,k}.
 \end{aligned}
 \tag{4.2}
\]

Equivalently,

\[
 \kappa_{ijk,s}=M_{ijk,s}
 -v_{s,i}\tau_{jk,s}-v_{s,j}\tau_{ik,s}
 -v_{s,k}\tau_{ij,s}-v_{s,i}v_{s,j}v_{s,k}.
 \tag{4.3}
\]

Apply (2.1)--(2.2), use
\(L_s\tau_{ij,s}=2\partial_\ell v_{s,i}\partial_\ell v_{s,j}\),
and collect the three pairings.  The terms containing one undifferentiated
\(v_s\) cancel exactly.  The result is

\[
 \boxed{
 \begin{aligned}
 L_s\kappa_{ijk,s}=2\sum_\ell\big(&
 \partial_\ell v_{s,i}\,\partial_\ell\tau_{jk,s}
 +\partial_\ell v_{s,j}\,\partial_\ell\tau_{ik,s}\\
 &+\partial_\ell v_{s,k}\,\partial_\ell\tau_{ij,s}\big),
 \qquad \kappa_{ijk,0}=0.
 \end{aligned}}
 \tag{4.4}
\]

The local cubic transport is reconstructed by

\[
 P_s\left[u\odot(u\cdot\nabla u)\right]_{ij}
 =\partial_kM_{kij,s}.
 \tag{4.5}
\]

It does not include the pressure contribution

\[
 H_{ij,s}=P_s(u_i\partial_jp+u_j\partial_ip).
 \tag{4.6}
\]

Let \(g_s=\nabla p_s\), and set

\[
 \rho_s=P_s(u\odot\nabla p)-v_s\odot g_s.
 \tag{4.7}
\]

Another application of (2.4) gives

\[
 \boxed{
 L_s\rho_s=2\sum_\ell
 \partial_\ell v_s\odot\partial_\ell g_s,
 \qquad \rho_0=0.}
 \tag{4.8}
\]

The transparent and compressed representations agree:

\[
 \boxed{
 \mathcal C_{ij,s}
 =\partial_kM_{kij,s}+H_{ij,s}
 =v_s\odot N_s+\chi_s.}
 \tag{4.9}
\]

Thus \((\kappa_s,\rho_s)\) and \(\chi_s\) are two exact representations of
the same pressure-aware third-order level.  No uniqueness or global
minimality follows.

## 5. Germano's complete second-stress ledger

For comparison with the classical filtered hierarchy, define

\[
 Q_{i,s}=\tau_s(p,u_i),\qquad
 R_{ij,s}=\tau_s(p,S_{ij}),
 \qquad S_{ij}=\tfrac12(\partial_i u_j+\partial_j u_i),
 \tag{5.1}
\]

and

\[
 D_{ij,s}=\sum_k\tau_s(\partial_k u_i,\partial_k u_j).
 \tag{5.2}
\]

The covariance identity gives

\[
 L_sQ_{i,s}=2\nabla p_s\cdot\nabla v_{s,i},
 \qquad Q_{i,0}=0,
 \tag{5.3}
\]

\[
 L_sR_{ij,s}=2\nabla p_s\cdot\nabla S_{ij}(v_s),
 \qquad R_{ij,0}=0.
 \tag{5.4}
\]

Differentiate \(\tau_{ij,s}=\tau_s(u_i,u_j)\) in physical time and insert
(1.1).  The viscosity identity is

\[
 \tau_s(\Delta u_i,u_j)+\tau_s(u_i,\Delta u_j)
 =\Delta\tau_{ij,s}-2D_{ij,s}.
 \tag{5.5}
\]

The pressure identity is

\[
 \begin{aligned}
 &-\tau_s(\partial_i p,u_j)-\tau_s(u_i,\partial_jp)\\
 &\qquad=-\partial_iQ_{j,s}-\partial_jQ_{i,s}+2R_{ij,s}.
 \end{aligned}
 \tag{5.6}
\]

The transport product identity, followed by incompressibility, supplies the
third velocity cumulant and the two resolved-strain production terms.  The
complete equation is

\[
 \boxed{
 \begin{aligned}
 \partial_t\tau_{ij,s}+\partial_k(v_{s,k}\tau_{ij,s})
 ={}&-\partial_k\!\left(
 \kappa_{ijk,s}+Q_{i,s}\delta_{jk}+Q_{j,s}\delta_{ik}
 -\nu\partial_k\tau_{ij,s}\right)\\
 &+2R_{ij,s}-2\nu D_{ij,s}
 -\tau_{ik,s}\partial_kv_{s,j}
 -\tau_{jk,s}\partial_kv_{s,i}.
 \end{aligned}}
 \tag{5.7}
\]

This is Germano's generalized-central-moment equation specialized to the heat
filter and the present sign convention.  It makes the pressure boundary
explicit: \(\kappa_s\) alone is a false truncation of the complete tensor
equation.  Equation (5.7) does not by itself prove that the pressure rows are
information-theoretically unreconstructible from every other declared field.

## 6. Conditional critical rows and the derivative gap

Let \(I\) lie inside the smooth lifespan and put

\[
 E(I)=L^4(I;L^6(\mathbb T^3)).
 \tag{6.1}
\]

Heat contraction, H\"older, and the R0.73U stress estimate give, with
dimension-only tensor constants,

\[
 \boxed{
 \sup_{s\ge0}\|\kappa_s\|_{L_t^{4/3}L_x^2(I)}
 \le C_\kappa\|u\|_{E(I)}^3.}
 \tag{6.2}
\]

Indeed, \(P_s(u^{\otimes3})\), \(v_s^{\otimes3}\), and each
\(v_s\otimes\tau_s\) lie in that row.  With the periodic double-Riesz
constant \(C_R\),

\[
 \|p\|_{L_t^2L_x^3(I)}\le C_R\|u\|_{E(I)}^2.
 \tag{6.3}
\]

Hence

\[
 \boxed{
 \sup_{s\ge0}\|Q_s\|_{L_t^{4/3}L_x^2(I)}
 \le 2C_R\|u\|_{E(I)}^3.}
 \tag{6.4}
\]

There is one exact scalar projection in which the pressure--strain gap
disappears.  Put

\[
 k_s={1\over2}\operatorname{tr}\tau_s,
 \qquad J_{k,s}={1\over2}\kappa_{iik,s}+Q_{k,s}.
 \tag{6.5}
\]

Since \(S_{ii}=\nabla\cdot u=0\), one has \(R_{ii,s}=0\).  Taking half the
trace of (5.7) gives

\[
 \boxed{
 \partial_t k_s+\partial_k(v_{s,k}k_s)
 =-\partial_k\big(J_{k,s}-\nu\partial_k k_s\big)
 -\nu D_{ii,s}-\tau_{ik,s}\partial_kv_{s,i}.}
 \tag{6.6}
\]

The viscous covariance satisfies \(D_{ii,s}\ge0\) by the heat-kernel
covariance inequality applied to every gradient component.  Moreover,

\[
 \boxed{
 \sup_{s\ge0}\|J_s\|_{L_t^{4/3}L_x^2(I)}
 \le C_J(1+C_R)\|u\|_{E(I)}^3.}
 \tag{6.7}
\]

Thus the complete signed third-order scalar flux lies in a critical row under
the strong-norm hypothesis.  Equation (6.6) is not a regularity theorem: the
production \(-\tau_s:\nabla v_s\) is signed, and (6.7) remains conditional on
\(u\in E\).

The pressure--strain covariance \(R_s\), the pressure-gradient covariance
\(\rho_s\), and the compressed derivative-carrying field \(\chi_s\) are not
placed in (6.2)--(6.4).  The hypothesis \(u\in E\) contains no velocity
derivative.  Treating these objects as if they occupied the same undifferentiated
flux row would conceal the remaining analytic loss.

Equations (6.2)--(6.4) are conditional and circular for the Clay problem:
they start from the classical critical strong norm that arbitrary energy data
do not presently control.

## 7. Exact physical-time ascent to fourth order

The raw third moment gives the cleanest next-level calculation.  Applying the
three-factor product rule to (1.5) yields

\[
 \boxed{
 \begin{aligned}
 (\partial_t-\nu\partial_s)M_{ijk,s}
 ={}&-2\nu P_s\sum_\ell\Big[
 u_k\partial_\ell u_i\partial_\ell u_j
 +u_j\partial_\ell u_i\partial_\ell u_k\\
 &\hspace{42mm}+u_i\partial_\ell u_j\partial_\ell u_k\Big]\\
 &-P_s\Big[N_i u_j u_k+u_iN_j u_k+u_i u_jN_k\Big].
 \end{aligned}}
 \tag{7.1}
\]

Since \(N=\mathcal B(u,u)\) is quadratic, the last line is fourth order in
velocity.  Obtaining a general physical-time equation for the centered
\(\kappa_s\) requires differentiating every subtraction in (4.2).  The
classical generalized-moment hierarchy places a connected fourth-order level
there, but that full centered index ledger is not asserted as a new
self-contained formula in this section.  The finite gate instead tests one
selected \(\kappa\) coefficient directly.

The same fact can be displayed directly for the compressed lift.  Define

\[
 \mathcal R_4=\mathcal B(N,u)+\mathcal B(u,N),
 \qquad
 \mathcal S_3=\sum_\ell\mathcal B(\partial_\ell u,\partial_\ell u).
 \tag{7.2}
\]

Differentiating \(N=\mathcal B(u,u)\) gives

\[
 \partial_tN=\nu\Delta N-2\nu\mathcal S_3-\mathcal R_4.
 \tag{7.3}
\]

Consequently,

\[
 \boxed{
 \begin{aligned}
 (\partial_t-\nu\partial_s)\mathcal C_s
 =-P_s\Big\{&N\odot N+u\odot\mathcal R_4\\
 &+2\nu\big[
 \sum_\ell\partial_\ell u\odot\partial_\ell N
 +u\odot\mathcal S_3\big]\Big\}.
 \end{aligned}}
 \tag{7.4}
\]

The first line in braces is quartic.  Subtracting the resolved product gives

\[
 \begin{aligned}
 (\partial_t-\nu\partial_s)\chi_s
 ={}&(\partial_t-\nu\partial_s)\mathcal C_s
 +N_s\odot N_s\\
 &+v_s\odot\mathbb P\nabla\!\cdot(2\nu G_s+\mathcal C_s).
 \end{aligned}
 \tag{7.5}
\]

Equations (7.1) and (7.4)--(7.5) prove the narrow \(3\to4\) statement for
these natural lifts.  They do not prove that every conceivable higher-order
state fails, that no exceptional cancellation exists, or that an infinite
hierarchy cannot be controlled.

## 8. Bottom-scale order separation

For smooth periodic fields, (2.4) gives the local heat expansion

\[
 \tau_s(f,g)=2s\sum_\ell\partial_\ell f\,\partial_\ell g+O(s^2)
 \qquad(s\downarrow0),
 \tag{8.1}
\]

in every fixed spatial \(C^m\) norm permitted by the smoothness.  In
particular,

\[
 Q_{i,s}=2s\sum_\ell\partial_\ell p\,\partial_\ell u_i+O(s^2),
 \tag{8.2}
\]

\[
 R_{ij,s}=2s\sum_\ell\partial_\ell p\,\partial_\ell S_{ij}+O(s^2).
 \tag{8.3}
\]

The third velocity cumulant starts one order later.  Equation (4.4) gives
\(\partial_s\kappa_{ijk,0}=0\).  Differentiating it once more at \(s=0\)
gives

\[
 \boxed{
 \begin{aligned}
 \kappa_{ijk,s}=2s^2\sum_{\ell,m}\big[&
 \partial_\ell u_i\,\partial_\ell(
     \partial_m u_j\,\partial_m u_k)\\
 &+\partial_\ell u_j\,\partial_\ell(
     \partial_m u_i\,\partial_m u_k)\\
 &+\partial_\ell u_k\,\partial_\ell(
     \partial_m u_i\,\partial_m u_j)\big]+O(s^3).
 \end{aligned}}
 \tag{8.4}
\]

Let the complete centered pressure contribution to (5.7) be

\[
 \mathfrak P_{ij,s}
 =-\partial_iQ_{j,s}-\partial_jQ_{i,s}+2R_{ij,s}.
 \tag{8.5}
\]

Substituting (8.2)--(8.3) and using
\(2S_{ij}=\partial_i u_j+\partial_j u_i\) cancels the second derivatives of
velocity.  The leading term is

\[
 \boxed{
 \mathfrak P_{ij,s}
 =-2s\sum_\ell\left[
 (\partial_i\partial_\ell p)(\partial_\ell u_j)
 +(\partial_j\partial_\ell p)(\partial_\ell u_i)
 \right]+O(s^2).}
 \tag{8.6}
\]

Thus the local velocity-cumulant flux is \(O(s^2)\), while the centered
pressure source is generically \(O(s)\).  The formal finite gate must supply
a witness on which both leading coefficients are nonzero before concluding
that their ratio costs \(s^{-1}\).  The expansion alone does not make that
nondegeneracy assertion for every field.

The equation-slot-compressed lift has the correct first order:

\[
 \boxed{
 \chi_s=2s\sum_\ell\partial_\ell u\odot\partial_\ell N+O(s^2).}
 \tag{8.7}
\]

This explains why the pressure-aware cross-covariance is the natural object
at the bottom heat scale.  It does not provide an energy-class bound for the
derivatives in (8.7).

## 9. Exact conclusion and remaining gates

The pressure-aware signed lift supplies one exact positive result and one
exact boundary:

1. in the heat variable, \(\chi_s\) has the downward-triangular
   carr\'e-du-champ law (3.1)--(3.2) and exactly fills the odd tensor-tangent
   slot in (3.5);
2. in physical time, the raw third moment and the compressed lift both enter
   a fourth-order level, as displayed in (7.1) and (7.4).

The trace corollary (6.6) removes pressure--strain exactly and places its
remaining third-order flux in the conditional critical row (6.7).  Its signed
production term is the next scalar obstruction.

The independent sign/index readback passes, the separate sealed two-path
certificate closes the declared four-site, six-site, and selected quartic
finite gates, and the formal figure passes its immutable source seal and two
independent readbacks.  The publication transaction remains.  No result here
controls the derivative pressure row or the critical strong norm from
arbitrary energy data.
Arbitrary-data three-dimensional global regularity remains open.  `NOT CLAY`.
