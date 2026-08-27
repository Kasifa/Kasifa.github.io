# R0.72I -- the physical absorption test and an odd-carrier repair

**Date:** 2026-08-27

**Status:** analytic method-obstruction theorem and a sharp complete-root
theorem for the perturbative all-odd Rudin--Shapiro branch of the exact
triangular 2.5D Navier--Stokes class. The direct positive-term absorption of
R0.72H (6.5) fails, but the true complete physical ledger on the same family
is smaller and tends to zero after the critical-log normalization. This is not
a theorem for general three-dimensional Navier--Stokes solutions.

**Keywords:** Navier--Stokes regularity, triangular 2.5D flow, critical-log
action, complete temporal roots, Rudin--Shapiro polynomial, physical
normalization, interaction exposure, lattice parity

---

## 0. Direct decision

R0.72H proved, in a compatible real finite-carrier sector,

\[
\begin{aligned}
 G_{\rm all}^{\rm ex}(I)
 \le{}&E_A\rho_A^2+2\lambda_0^2Q_*^I\\
 &+12\sqrt\nu\,d|K_z|
 [\lambda_0E_Am_*(A,X)Q_*^I]^{1/2}\\
 &+2|\delta|\sqrt{\lambda_0}B_AQ_*^I.
\end{aligned}
\tag{0.1}
\]

The open question was whether every positive term on the right could be
absorbed into the physical scale

\[
 D^{1/3}\Lambda_{1,*}.
\tag{0.2}
\]

The answer for the displayed factorization is **no**. On an all-odd shifted
Rudin--Shapiro block, take unit carrier modulus and coupling

\[
 g_M:=|\delta_M|=P_M=M.
\tag{0.3}
\]

After the exact physical amplitude balance, the four lifted terms in (0.1)
have orders

\[
 M,\qquad M^{-1/3}\log M,\qquad M,\qquad
 M^{13/6}\log M,
\tag{0.4}
\]

whereas

\[
 D_M^{1/3}\Lambda_{1,*}(I;u_M)\asymp M^{5/3}.
\tag{0.5}
\]

Thus the last positive upper-bound term alone has normalized size

\[
 \boxed{
 \frac{\widehat T_{B,M}}
 {D_M^{1/3}\Lambda_{1,*}(I;u_M)}
 \asymp M^{1/2}\log M\longrightarrow\infty.}
\tag{0.6}
\]

This does **not** make the true root ledger large. The same carrier block has
an interaction-exposure estimate omitted by the Cauchy--Schwarz step in
(0.1). Equivalently, its odd shifts give a direct two-colour parity estimate
for the cubic row. Either route yields

\[
 G_{{\rm all},M}^{\rm ex}\asymp M^2,
 \qquad
 \mathcal J_{{\rm all},M}\asymp\frac{g_M^2}{M}.
\tag{0.7}
\]

More generally, uniformly for

\[
 0<g_M\le\gamma_0M^{3/2},
\tag{0.8}
\]

the complete normalized physical ledger satisfies

\[
\boxed{
 \frac{\mathcal J_{{\rm all},M}}
 {D_M^{1/3}\Lambda_{1,*}(I;u_M)}
 \le
 C M^{-4/9}(\log M)^{-2/3}\longrightarrow0.}
\tag{0.9}
\]

R0.72I therefore separates two statements that cannot be conflated:

1. the fixed positive-term estimate (0.1) cannot be closed by termwise
   physical absorption;
2. the perturbative all-odd family is not a counterexample to (0.2).

The new remaining interface is the true cubic interaction row for generic,
especially mixed-parity, carrier sets.

---

## 1. Exact all-odd physical family

Work in the exact triangular class

\[
 u=(f(y,z,t),0,v(y,t)),
 \qquad
 v_t=\nu v_{yy},
 \qquad
 f_t+vf_z=\nu(f_{yy}+f_{zz}),
\tag{1.1}
\]

for which

\[
 \mathbb P(u\times\omega)=(-vf_z,0,0).
\tag{1.2}
\]

Fix

\[
 \nu=d=K_z=q=1,
 \qquad K_y=0,
 \qquad I=[0,T],
\tag{1.3}
\]

with fixed \(T>0\). Let \(M=2^n\), let

\[
 r_j=2M+2j+1,
 \qquad
 w_j=\varepsilon_j\in\{-1,1\},
 \qquad 0\le j<M,
\tag{1.4}
\]

where \(\varepsilon_j\) are the Rudin--Shapiro signs. The scaled active
sector is

\[
 F'=D F+\delta_MV_M(x)F,
 \qquad
 D e_r=-(r^2+1)e_r.
\tag{1.5}
\]

R0.72H constructed a real-gauged launch with

\[
 \|F_M(0)\|_2^2=M,
 \qquad
 F_{M,0}(\tau_M)=0,
 \qquad
 \tau_M=M^{-3},
\tag{1.6}
\]

and

\[
 |h_M(\tau_M)|\ge cM,
 \qquad
 h_M=P_0V_MF_M.
\tag{1.7}
\]

The scalar correction has size

\[
 |\zeta_M|\le Cg_MM^{-2},
 \qquad g_M=|\delta_M|.
\tag{1.8}
\]

The relevant exact carrier moment is

\[
 K_s=\sum_{j=0}^{M-1}r_j^2
 =\frac{M(28M^2-1)}3.
\tag{1.9}
\]

With unit carrier modulus, \(K_v=K_s\). If \(c_M\) is the normalization of
the corrected launch, then

\[
 K_{f,M}=c_M^2K_s,
 \qquad
 c_M^2=\frac{M}{M+|\zeta_M|^2}=1+o(1).
\tag{1.10}
\]

Choose the physical active and shear amplitudes by the exact balance

\[
 S_M^2K_{f,M}=3P_M^2K_v,
 \qquad
 P_M=g_M,
\tag{1.11}
\]

and set

\[
 E_M=S_M^2K_{f,M}+P_M^2K_v=4P_M^2K_v.
\tag{1.12}
\]

Add the inherited decoupled background. Uniformly under (0.8), the R0.72D
enstrophy argument gives

\[
 cE_M\le Y_M(t)\le CE_M,
 \qquad
 \mathcal R_{Y_M}(I)\le C,
 \qquad
 D_M\asymp E_M\asymp g_M^2M^3.
\tag{1.13}
\]

The parameter controlling the Duhamel expansion is not \(g_M\) alone but

\[
 \epsilon_M=g_MM^{-3/2}.
\tag{1.14}
\]

Thus the diagnostic choice \(g_M=M\) has
\(\epsilon_M=M^{-1/2}\to0\), so it stays inside the uniform perturbative
window. Large physical amplitude and small total carrier exposure coexist.

---

## 2. Physical lift and critical-log action

At every target root, the exact projected-Lamb identity gives

\[
 J_*(t_x)
 =c_*\frac{S_M^2P_M^2|h_M(x)|^2}{Y_M(t_x)}.
\tag{2.1}
\]

It is convenient to define the canonical lift

\[
 \Theta_M
 :=\frac{S_M^2P_M^2}{E_M}
 =\frac{3P_M^2}{4K_{f,M}}
 \asymp\frac{g_M^2}{M^3}.
\tag{2.2}
\]

Equation (1.13) implies

\[
 \mathcal J_{{\rm all},M}
 \asymp \Theta_M G_{{\rm all},M}^{\rm ex}.
\tag{2.3}
\]

The R0.72H heat-stable block estimates remain uniform when (1.14) is small:

\[
 Q_{*,M}\asymp M^{2/3}\log M,
 \qquad
 m_{*,M}\asymp\frac{M^{7/3}}{\log M},
\tag{2.4}
\]

\[
 E_{0,M}=M,
 \qquad
 \rho_{0,M}^2=2M,
 \qquad
 B_{0,M}^2=2(K_s+M)\asymp M^3.
\tag{2.5}
\]

The full physical action, not only its target projection, has the same scale.
Indeed the Rudin--Shapiro heat estimate and active contraction give

\[
 \|v_M(t)\|_\infty^2
 \le Cg_M^2M e^{-cM^2t},
 \qquad
 \|\partial_zf_M(t)\|_2^2\le CS_M^2M.
\tag{2.6}
\]

Using (1.13),

\[
 \frac{\|\mathbb P(u_M\times\omega_M)\|_{\dot H^{-1}}^2}
 {Y_M(t)}
 \le C\frac{g_M^2}{M}e^{-cM^2t}.
\tag{2.7}
\]

The critical-log heat integral satisfies

\[
 \int_0^T
 w_*\!\left(\frac tT\right)e^{-cM^2t}\,dt
 \asymp_T M^{-4/3}\log M.
\tag{2.8}
\]

This proves the upper bound in

\[
 \boxed{
 \mathscr A_*(I;u_M)
 \asymp g_M^2M^{-7/3}\log M.}
\tag{2.9}
\]

The lower bound follows from the isolated target sector, (2.3), and (2.4).
Consequently

\[
 \boxed{
 D_M^{1/3}\Lambda_{1,*}(I;u_M)
 \asymp
 g_M^{2/3}M
 \left(1+g_M^2M^{-7/3}\log M\right).}
\tag{2.10}
\]

All comparisons in this section have constants independent of \(M\) and
\(g_M\) in (0.8). They may depend on the fixed interval, target multiplier,
background, and torus normalization.

---

## 3. The direct R0.72H absorption fails

Write the four positive terms in (0.1), with fixed geometric constants
suppressed, as

\[
 T_0=E_0\rho_0^2,
 \quad
 T_1=Q_*,
 \quad
 T_2=(E_0m_*Q_*)^{1/2},
 \quad
 T_B=g_MB_0Q_*.
\tag{3.1}
\]

Their physical lifts are \(\widehat T_j=\Theta_MT_j\). Equations
(2.2)--(2.5) give

\[
\begin{array}{c|c|c}
 \text{term}&T_j&\widehat T_j\\ \hline
 T_0&M^2&g_M^2M^{-1}\\
 T_1&M^{2/3}\log M&g_M^2M^{-7/3}\log M\\
 T_2&M^2&g_M^2M^{-1}\\
 T_B&g_MM^{13/6}\log M&g_M^3M^{-5/6}\log M.
\end{array}
\tag{3.2}
\]

Now set \(g_M=M\). Then the action in (2.9) tends to zero and

\[
 D_M\asymp M^5,
 \qquad
 \Lambda_{1,*}\asymp1,
 \qquad
 D_M^{1/3}\Lambda_{1,*}\asymp M^{5/3}.
\tag{3.3}
\]

The first, second, and third lifted terms have normalized sizes

\[
 M^{-2/3},
 \qquad
 M^{-2}\log M,
 \qquad
 M^{-2/3}.
\tag{3.4}
\]

The last one has size (0.6). Therefore there is no carrier-independent
constant \(C\) for which the **right side of the fixed positive estimate**
(0.1), after its physical lift, is bounded by
\(CD^{1/3}\Lambda_{1,*}\) on this family.

The logical direction matters. Equation (0.1) says
\(G_{\rm all}^{\rm ex}\le T_0+T_1+T_2+T_B\). Showing that \(T_B\) is too
large does not show that \(G_{\rm all}^{\rm ex}\) is large. It only rejects
this route of positive-term factorization.

---

## 4. First repair: retain the true interaction exposure

R0.72C did not separate the cubic row into \(B_0Q_*\). It retained

\[
 \ell_\times(I)
 =\frac1{\rho_0\Omega_0}
 \int_I\rho(x)\|V_M(x)\|\,dx,
 \qquad
 \eta=g_M\Omega_0,
\tag{4.1}
\]

and proved

\[
 G_{\rm all}^{\rm ex}(I)
 \le e^{2\lambda_0|I|}M\rho_0^2
 [1+q_\rho(I)+\eta\ell_\times(I)],
 \qquad q_\rho\le3.
\tag{4.2}
\]

For the shifted Rudin--Shapiro heat profile,

\[
 \rho(x)\le C\sqrt M e^{-cM^2x},
 \qquad
 \|V_M(x)\|\le C\sqrt M e^{-cM^2x},
\tag{4.3}
\]

while \(\rho_0\asymp\Omega_0\asymp\sqrt M\). Hence

\[
 \boxed{
 \ell_\times(I)\le CM^{-2},
 \qquad
 \eta\ell_\times(I)\le Cg_MM^{-3/2}.}
\tag{4.4}
\]

Under (0.8), (4.2)--(4.4) give

\[
 G_{{\rm all},M}^{\rm ex}\le CM^2.
\tag{4.5}
\]

The exact root (1.6)--(1.7) gives the reverse inequality. Therefore

\[
 \boxed{G_{{\rm all},M}^{\rm ex}\asymp M^2.}
\tag{4.6}
\]

This already proves that the divergence in (0.6) was introduced by replacing
the short joint exposure in (4.1) by the separated moment product in (3.1).

---

## 5. Second repair: the odd-carrier parity lemma

The same conclusion can be seen directly in the cubic row. Let
\(\Pi_{\rm e}\) and \(\Pi_{\rm o}\) denote the even and odd lattice
projections. Because every \(r_j\) is odd,

\[
 V_M\Pi_{\rm e}=\Pi_{\rm o}V_M,
 \qquad
 V_M\Pi_{\rm o}=\Pi_{\rm e}V_M,
\tag{5.1}
\]

while \(D\) preserves parity. The aligned launch is odd, apart from the
controlled \(\zeta_Me_0\) root correction. Put

\[
 F_{\rm e}=\Pi_{\rm e}F_M,
 \qquad
 F_{\rm o}=\Pi_{\rm o}F_M.
\tag{5.2}
\]

Contractivity and Duhamel's formula give

\[
\begin{aligned}
 \|F_{\rm e}(x)\|_2
 &\le Cg_MM^{-2}
 +g_M\int_0^x\|V_M(s)\|\|F_{\rm o}(s)\|_2\,ds\\
 &\le C\min\!\left(\sqrt M,\frac{g_M}{M}\right).
\end{aligned}
\tag{5.3}
\]

The target index is even. Thus

\[
 h=P_0V_MF_{\rm o},
 \qquad
 b:=P_0V_M^2F_M=P_0V_M^2F_{\rm e}.
\tag{5.4}
\]

Equations (4.3), (5.3), and the target-row norm imply

\[
 |h(x)|\le CM e^{-cM^2x},
\tag{5.5}
\]

\[
 |b(x)|\le
 CM e^{-cM^2x}
 \min\!\left(\sqrt M,\frac{g_M}{M}\right).
\tag{5.6}
\]

After time integration,

\[
\boxed{
 g_M\int_0^T|h(x)b(x)|\,dx
 \le
 Cg_M\min\!\left(\sqrt M,\frac{g_M}{M}\right).}
\tag{5.7}
\]

In the perturbative window (0.8), this becomes

\[
 g_M\int_0^T|hb|\,dx\le C\frac{g_M^2}{M}\le CM^2.
\tag{5.8}
\]

Combining (5.8) with the R0.72H mixed-row theorem and the Rolle reduction
again gives (4.5). For \(g_M=M\), the true cubic payment in (5.7) is only
\(O(M)\), while the separated positive upper bound \(g_MB_0Q_*\) is
\(\asymp M^{19/6}\log M\). This quantifies the loss, not merely its
existence.

---

## 6. Complete physical theorem

### Theorem 6.1 -- uniform decay of the perturbative all-odd branch

Fix the interval, target multiplier, background, and geometry in
(1.1)--(1.4). There is \(\gamma_0>0\) such that, for every sequence

\[
 0<g_M\le\gamma_0M^{3/2},
 \qquad M=2^n,
\tag{6.1}
\]

the exact amplitude-balanced triangular solutions above satisfy

\[
 \mathcal J_{{\rm all},M}\asymp\frac{g_M^2}{M},
\tag{6.2}
\]

\[
 D_M\asymp g_M^2M^3,
 \qquad
 \Lambda_{1,*}(I;u_M)
 \asymp1+g_M^2M^{-7/3}\log M,
\tag{6.3}
\]

and

\[
 \frac{\mathcal J_{{\rm all},M}}
 {D_M^{1/3}\Lambda_{1,*}(I;u_M)}
 \asymp
 \frac{g_M^{4/3}M^{-2}}
 {1+g_M^2M^{-7/3}\log M}.
\tag{6.4}
\]

In particular, the ratio converges to zero uniformly over (6.1).

#### Proof of the uniform rate

Set

\[
 z=g_M^2M^{-7/3}\log M.
\tag{6.5}
\]

Then the right side of (6.4) is

\[
 M^{-4/9}(\log M)^{-2/3}
 \frac{z^{2/3}}{1+z}.
\tag{6.6}
\]

The scalar factor \(z^{2/3}/(1+z)\) is bounded on \((0,\infty)\), with its
maximum at \(z=2\). This proves (0.9). \(\square\)

For the diagnostic subfamily \(g_M=M\), (6.4) gives

\[
 \frac{\mathcal J_{{\rm all},M}}
 {D_M^{1/3}\Lambda_{1,*}}
 \asymp M^{-2/3}.
\tag{6.7}
\]

The direct R0.72H upper-bound factor diverges by (0.6) at exactly the same
parameters. Equations (0.6) and (6.7) are the central separation in this
section.

---

## 7. Finite audit contract

The analytic estimates above are the result. Two finite computations test
their implementation.

The producer audit:

1. generates Rudin--Shapiro signs by the polynomial recurrence;
2. evolves the complex Fourier lattice with \(\delta_M=M\);
3. constructs the exact root correction from two evolution columns;
4. evaluates \(h\), \(QF\), \(P_0V^2F\), \(Q_*\), \(m_*\), \(B_0\), and
   the canonical physical lift;
5. records the direct \(B_0Q_*\) loss and the smaller true cubic exposure.

The independent audit:

1. generates the signs from adjacent binary-\(11\) parity;
2. evolves the real-gauge lattice with a different integrator and quadrature;
3. recomputes the even/odd exposure and physical ratios without importing the
   producer implementation;
4. compares common finite sizes and fitted log--log exponents.

Configurations, progress streams, resource logs, raw data, environments,
reproduction commands, and SHA-256 manifests are retained. Finite agreement
cannot certify the asymptotic theorem.

---

## 8. Literature boundary

A bounded primary-source search through 2026-08-27 found adjacent tools but
no theorem that directly performs the absorption or parity repair above.

1. [Koch--Tataru](https://math.berkeley.edu/~tataru/papers/nas.pdf) use a
   critical heat-extension tent/Carleson norm for small-data well-posedness in
   \(BMO^{-1}\). Their norm is an initial-data space and does not sample the
   present solution-dependent temporal roots.
2. [Chemin--Planchon](https://www.numdam.org/articles/10.24033/bsmf.2638/)
   turn negative Besov a priori bounds into positive regularity. This does not
   identify the quotient action in (2.9) with a standard Besov norm or pay the
   shear moments in (3.1).
3. [Haak--Ouhabaz](https://arxiv.org/abs/1102.3268) treat fixed observation
   operators for autonomous semigroups through admissibility and square
   functions. Here the observations \(V_M\) and \(V_M'\) vary in time and the
   sampling set is endogenous.
4. [Dong--Zhang](https://doi.org/10.1016/j.jfa.2020.108563) prove time
   analyticity for bounded mild Navier--Stokes solutions. Isolated temporal
   zeros do not by themselves give a carrier-uniform sum of squared slopes.
5. [Lei--Lin--Zhou](https://arxiv.org/abs/1505.00142) obtain a critical but
   conditionally coercive helicity energy, while
   [Biferale--Titi](https://arxiv.org/abs/1303.1215) obtain a positive
   \(H^{1/2}\)-type helicity control after helical decimation. Neither supplies
   an unconditional payment for \(B_0\), \(m_*\), or the complete roots of the
   full equations.
6. [Lerner--Vigneron](https://arxiv.org/abs/2203.07950) analyze curl
   diagonalization, spin components, and the cross-product structure of the
   nonlinearity. They do not prove the critical-log action estimate used here.
7. [Bedrossian--Germain--Masmoudi](https://annals.math.princeton.edu/2017/185-2/p04)
   prove a high-Sobolev stability threshold near fixed three-dimensional
   Couette flow and convergence toward 2.5D streaks. That perturbative geometry
   is different from arbitrary finite shear carriers and complete target-root
   sampling.
8. [Mahalov--Titi--Leibovich](https://doi.org/10.1007/BF00381234) and
   [Chemin--Gallagher](https://arxiv.org/abs/0710.5408) prove global regularity
   for special helical or slowly varying large-data classes. Their structural
   assumptions do not yield (0.1), (4.4), or (5.7).

The search found no source simultaneously controlling the critical-log
negative-Sobolev action, the complete endogenous root-slope ledger, and the
explicit shear moments with a constant uniform in carrier count. This is a
bounded non-collision statement, not a claim of priority, exhaustiveness, or
global novelty.

---

## 9. What is proved and what is not

### Proved

1. The direct physical lift of the positive \(B_AQ_*\) term in R0.72H (6.5)
   is not uniformly absorbable into \(D^{1/3}\Lambda_{1,*}\).
2. The other three terms are not responsible for the loss on the diagnostic
   family.
3. The all-odd block retains a short interaction exposure
   \(\ell_\times=O(M^{-2})\).
4. Odd-carrier parity gives a direct improved estimate for the true cubic row.
5. The complete raw root mass is \(\asymp M^2\) throughout the perturbative
   coupling window.
6. The complete normalized physical ledger tends to zero uniformly at the
   rate in (0.9).

### Not proved

1. A generic replacement for \(B_AQ_*\) on arbitrary carrier sets.
2. The physical critical-log inequality for every finite triangular flow.
3. A counterexample to that physical inequality.
4. A restart covering theorem outside the triangular invariant class.
5. A new continuation criterion or a finite-time singularity for the full
   three-dimensional Navier--Stokes equations.

---

## 10. Exact conclusion and next gate

R0.72I resolves the amplitude audit posed at the end of R0.72H. The fixed
positive-term corollary cannot be completed by absorbing its four terms one by
one. The obstruction is explicit, asymptotic, and isolated to the
\(B_AQ_*\) factorization.

The same exact solutions also show why that failure must not be advertised as
a physical counterexample. Retaining the joint heat exposure, or using the
odd-carrier parity split, recovers the true complete ledger and makes its
normalized ratio vanish.

The next finite section should test the cubic row beyond one parity coset. A
useful R0.72J gate is:

1. decompose a general carrier set by its residue graph and identify when
   \(V^2\) returns mass to the target sector;
2. seek a hybrid bound using the minimum of critical action and joint
   interaction exposure, without a positive \(B_AQ_*\) product;
3. build a mixed-parity block and measure the **true**
   \(|\delta|\int|hP_0V^2F|\), not only its separated upper bound;
4. decide whether the generic branch is absorbable or supports an actual
   normalized counterfamily.

Until that gate is closed, the result remains a rigorous theorem inside an
exact globally smooth test class and a diagnosis of one proof route. It does
not resolve the Millennium problem.
