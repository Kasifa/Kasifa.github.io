# R0.74P — temporal concentration no-go and defect-completed shell clocks

## 0. Scope and result

R0.74O constructs an exact smooth periodic family for which the scalar
payment remains at the frozen cubic scale while the exterior endpoint and
the positive cumulative collar flux are larger than every fixed logarithmic
repair of the two-thirds power.  With

\[
 T_*:=\varkappa^2B^2LR^2,
 \qquad
 K_*:=\frac{T_*}{B^2R^2}=\varkappa^2L,
 \qquad K_*\longrightarrow\infty,
\tag{0.1}
\]

the family obeys

\[
 X_*^\alpha\asymp\mathfrak C_*^\alpha\asymp T_*,
 \qquad
 (P_*^\alpha)^{2/3}\asymp B^2R^2=\frac{T_*}{K_*}.
\tag{0.2}
\]

This note tests three ways of recording the missing temporal concentration.
It proves the following statements.

1. Every fixed positive-order time-window Carleson mass misses the exact
   scale by a factor tending to zero.
2. Time-window energy oscillation detects the scale and is weakly lower
   semicontinuous, but it reconstructs the endpoint energy rather than
   replacing it by a weaker mechanism.
3. A defect-completed shell clock has a rigorous shellwise \(\ell^1\)
   closure.  Its matched \(\ell^2\) square function detects the exact family
   and is stable under the standard fixed-scale suitable-weak compactness
   topology.

The missing theorem is also explicit: no estimate compressing the shellwise
\(\ell^1\) ledger to the matched \(\ell^2\) clock is proved.  Nor is there a
prescribed-centre scale-packing theorem.  The work below is an observable
triage and compactness result, not a regularity theorem.  **NOT CLAY.**

## 1. Frozen setting

Work on

\[
 \mathbb T^3=(-\pi,\pi]^3,
 \qquad I_\rho=(t_0-\rho^2,t_0),
 \qquad 0<R<\frac\pi{16},
\tag{1.1}
\]

and suppose that \(\overline I_{8R}\Subset(0,T)\).  Let \((u,p)\) be a
periodic suitable weak solution of the unforced incompressible
Navier--Stokes equations with viscosity one.  Use the R0.74I terminally
anchored mollified path

\[
 \dot X_R(t)=u_R(t,X_R(t)),
 \qquad X_R(t_0)=x_0,
 \qquad u_R=\varphi_R^{\rm per}*u,
\tag{1.2}
\]

and the moving fields

\[
 v_R(t,y)=u(t,y+X_R(t)),
 \qquad
 \pi_R(t,y)=p(t,y+X_R(t)),
 \qquad a_R=\dot X_R.
\tag{1.3}
\]

Fix the R0.74I pressure gauge \(c_R(t)=c_{2R}^{M,R}(t)\).  Since
\(v_R\) is divergence free, every shell satisfies

\[
 \int_{\mathbb T^3}c_R(t)v_R\cdot\nabla\Psi_k^R\,dy=0.
\tag{1.3a}
\]

Retain the R0.74H padded shell cutoffs and weights

\[
 \Psi_k^R\ge0,
 \qquad
 |\nabla\Psi_k^R|\le CR^{-1}(1+2^{3k}R^3),
 \qquad
 |\Delta\Psi_k^R|\le CR^{-2}(1+2^{3k}R^3),
\tag{1.4}
\]

\[
 \gamma_k=\exp(-4^{k-1}/32),
 \qquad
 \Theta_R=\sum_{k\ge1}\gamma_k\Psi_k^R.
\tag{1.5}
\]

The series in (1.5) converges in \(C^2(\mathbb T^3)\).  Let
\(\eta_R\) be the frozen nondecreasing time cutoff, equal to zero near
\(s_R=t_0-4R^2\) and equal to one on \(I_R\).

The Version-M payment \(P_R^M\), exterior endpoint
\(\mathcal U_{\rm ext}^{\infty,M,R}\), exterior dissipation
\(\mathcal D_{\rm ext}^{M,R}\), and

\[
 X_R^M=\mathcal U_{\rm ext}^{\infty,M,R}
       +\mathcal D_{\rm ext}^{M,R}
\tag{1.6}
\]

are exactly the R0.74I quantities.  The proofs below use Version M because
its mollified trajectory has a completed suitable-weak formulation.
Statements about the smooth exact family continue to hold in both frozen
frames \(\alpha\in\{M,F\}\).

Whenever a smooth exact-family formula below carries \(\alpha\), the notation
\(z_M=v_R\) and \(z_F=w_R:=v_R-a_R\) is inherited from R0.74O.  General
suitable-weak statements and every compactness theorem in this note are
Version M only.

For that family,

\[
 \varkappa=L^{2/3}\exp\!\left(\frac m3L^2\right),
 \qquad
 m=\frac{43}{423360},
 \qquad
 \mathfrak a_* =\varkappa B\Gamma^{-1/2},
\tag{1.7}
\]

where \(\Gamma=\gamma_j\) is the target-shell weight and
\(BR^2=\beta_j\to1/128\).  In particular,

\[
 K_*=\varkappa^2L
 =L^{7/3}\exp\!\left(\frac{2m}{3}L^2\right)\longrightarrow\infty.
\tag{1.8}
\]

## 2. Total dissipation and the canonical shell clock

### 2.1 The measure that completes the clock

Define the total local dissipation distribution

\[
 \boldsymbol\mu[u,p]
 :=-\partial_t\frac{|u|^2}{2}
   -\nabla\!\cdot\!\left[
     \left(\frac{|u|^2}{2}+p\right)u
   \right]
   +\Delta\frac{|u|^2}{2}.
\tag{2.1}
\]

The suitable local energy inequality gives the measure inequality

\[
 \boldsymbol\mu[u,p]
 \ge |\nabla u|^2\,dx\,dt.
\tag{2.2}
\]

Thus \(\boldsymbol\mu\) is a nonnegative Radon measure and

\[
 \boldsymbol D[u,p]
 :=\boldsymbol\mu[u,p]-|\nabla u|^2\,dx\,dt
 \ge0
\tag{2.3}
\]

is the anomalous local-energy defect.  For a smooth solution,

\[
 d\boldsymbol\mu=|\nabla u|^2\,dx\,dt,
 \qquad \boldsymbol D=0.
\tag{2.4}
\]

The defect alone cannot detect the smooth R0.74O family.  It also has the
wrong stability direction for the present purpose.  Indeed, if
\(\boldsymbol\mu_n\rightharpoonup^*\boldsymbol\mu\) and
\(\nabla u_n\rightharpoonup\nabla u\), then for every nonnegative smooth
\(\phi\),

\[
 \limsup_{n\to\infty}\langle\boldsymbol D_n,\phi\rangle
 \le \langle\boldsymbol D,\phi\rangle.
\tag{2.5}
\]

The total measure, rather than the anomaly alone, is therefore the natural
completion of the local-energy clock.

### 2.2 Exact balance representatives

At every local-energy good time \(\tau<t_0\), define

\[
\begin{aligned}
 \widetilde K_{k,R}(\tau)
 :={}&\frac{\eta_R(\tau)}{2R}
 \int_{\mathbb T^3}\Psi_k^R(y)|v_R(\tau,y)|^2\,dy\\
 &+\frac1R
 \int_{(s_R,\tau)\times\mathbb T^3}
 \eta_R(t)\Psi_k^R(x-X_R(t))\,d\boldsymbol\mu(t,x),
\end{aligned}
\tag{2.6}
\]

and put the physical shell weight inside the clock:

\[
 K_{k,R}:=\gamma_k\widetilde K_{k,R}.
\tag{2.7}
\]

The two cumulative terms on the right side of the local-energy balance are

\[
\begin{aligned}
 Q_{k,R}(\tau)
 :={}&\frac{\gamma_k}{2R}
 \int_{s_R}^{\tau}\!\int_{\mathbb T^3}
 \left[
  \eta_R'(t)\Psi_k^R(y)
  +\eta_R(t)\Delta\Psi_k^R(y)
 \right]|v_R(t,y)|^2\,dy\,dt,
\end{aligned}
\tag{2.8}
\]

\[
\begin{aligned}
 F_{k,R}(\tau)
 :={}&\frac{\gamma_k}{R}
 \int_{s_R}^{\tau}\!\int_{\mathbb T^3}\eta_R(t)
 \left[
  \frac12|v_R|^2(v_R-a_R)+(\pi_R-c_R)v_R
 \right]\!\cdot\nabla\Psi_k^R\,dy\,dt.
\end{aligned}
\tag{2.9}
\]

A different time-dependent pressure gauge changes neither (2.9) nor any
conclusion below, by (1.3a).  Every integrand in (2.8)--(2.9) lies in
\(L^1_t\).  Hence these
functions have canonical absolutely continuous representatives.

### Lemma 2.1 — defect-completed balance

For each fixed shell, the local-energy distributional equality implies

\[
 \boxed{K_{k,R}=Q_{k,R}+F_{k,R},}
 \qquad
 K_{k,R}(s_R)=0,
 \qquad K_{k,R}\ge0.
\tag{2.10}
\]

Here \(K_{k,R}\) means the absolutely continuous representative on the
right of (2.10), which agrees with (2.6)--(2.7) at every good time.

**Proof.**  Test the distribution (2.1) with
\(\eta_R(t)\Psi_k^R(x-X_R(t))\), first after the R0.74I smooth-path
approximation.  The time derivative of the test is

\[
 \eta_R'\Psi_k^R-\eta_Ra_R\cdot\nabla\Psi_k^R.
\tag{2.11}
\]

After integration by parts, the first term in (2.11) and the Laplacian of
the cutoff give (2.8).  The second term combines with the kinetic transport
to replace \(v_R\) by \(v_R-a_R\), giving (2.9).  The initial term is zero
because \(\eta_R\) vanishes near \(s_R\).  This proves (2.10) at good times.
Both right-hand terms are absolutely continuous, so they select a unique
representative at every time.  Nonnegativity follows from (2.2), (2.6), and
density of the good times.  \(\square\)

This representative avoids a hard-time atom problem.  Weak-* convergence
of \(\boldsymbol\mu_n\) does not by itself imply convergence of its mass on
\((s_R,\tau)\times\mathbb T^3\) when the limiting temporal marginal has an
atom at \(\tau\).  The balance representative never requires that passage.

## 3. Positive variation and the shell hierarchy

For a real function \(f\) on \([s_R,t_0)\), set

\[
 \operatorname{Var}^+_{[s_R,t_0)}f
 :=\sup_{s_R=\tau_0<\cdots<\tau_N<t_0}
 \sum_{i=1}^N[f(\tau_i)-f(\tau_{i-1})]_+,
\tag{3.1}
\]

and define

\[
 v_{k,R}:=\operatorname{Var}^+_{[s_R,t_0)}K_{k,R}.
\tag{3.2}
\]

Since \(K_{k,R}\ge0\) and \(K_{k,R}(s_R)=0\),

\[
 K_{k,R}(\tau)\le v_{k,R}.
\tag{3.3}
\]

### 3.1 Absolute ledgers

Every un-subscripted total variation in this section is taken on
\([s_R,t_0)\).

Define

\[
\begin{aligned}
 \mathfrak Q_{{\rm sh,abs},R}^M
 :={}&\frac1{2R}\sum_{k\ge1}\gamma_k
 \int_{s_R}^{t_0}\!\int_{\mathbb T^3}
 \left(
  |\eta_R'|\Psi_k^R+\eta_R|\Delta\Psi_k^R|
 \right)|v_R|^2\,dy\,dt,
\end{aligned}
\tag{3.4}
\]

Define the gauge-correct absolute physical-flux ledger by

\[
\begin{aligned}
 \mathfrak L_{{\rm abs},R}^M
 :={}&\frac1R\sum_{k\ge1}\gamma_k
 \int_{s_R}^{t_0}\!\int_{\mathbb T^3}\eta_R
 \left[
  \frac12|v_R|^2(|v_R|+|a_R|)
  +|\pi_R-c_R|\,|v_R|
 \right]|\nabla\Psi_k^R|\,dy\,dt.
\end{aligned}
\tag{3.4a}
\]

### Lemma 3.1 — absolute clock bound

The R0.74H--I payment estimates give

\[
 \sum_{k\ge1}\operatorname{TV}Q_{k,R}
 \le\mathfrak Q_{{\rm sh,abs},R}^M
 \le C(P_R^M)^{2/3},
\tag{3.5}
\]

and

\[
 \sum_{k\ge1}\operatorname{TV}F_{k,R}
 \le\mathfrak L_{{\rm abs},R}^M
 \le CP_R^M.
\tag{3.6}
\]

**Proof.**  For (3.5), take absolute values in (2.8) and use the periodized
majorant

\[
 |\Delta\Psi_k^R(x)|
 \le\sum_{n\in\mathbb Z^3}
 |\Delta\psi_k^R(\widetilde x+2\pi n)|.
\tag{3.6a}
\]

After unfolding each nonnegative summand to \(\mathbb R^3\), the
single-lift bounds \(|\eta_R'|\le CR^{-2}\) and
\(|\Delta\psi_k^R|\le CR^{-2}\) give

\[
 \mathfrak Q_{{\rm sh,abs},R}^M
 \le CR^{-3}\sum_{k\ge1}\gamma_k
 \int_{I_{2R}}\!\int_{\operatorname{supp}\psi_k^R}
 |\widetilde v_R|^2\,dy\,dt.
\tag{3.6b}
\]

This is the same weighted \(R^{-3}S_2\) row as R0.74H
(4.3)--(4.8).  Weighted Hölder, the shell-volume sum, and the
doubled-radius cubic ledger give \(C(P_R^M)^{2/3}\).  Monotone
convergence applies to the unfolded nonnegative majorant.

For (3.6), take absolute values in (2.9).  The velocity and pressure terms
are bounded by the shellwise absolute integrals in R0.74H (6.3)--(6.5).
Here \(|\nabla\Psi_k^R|\) is handled by the gradient analogue of the lifted
majorant (3.6a).  The pressure row uses

\[
 |\pi_R-c_R|\,|v_R|
 \le C\bigl(|\pi_R-c_R|^{3/2}+|v_R|^3\bigr).
\tag{3.7}
\]

The residual drift is R0.74H (6.6).  R0.74I proves that these estimates use
only the suitable-weak integrability ledger.  They sum to \(CP_R^M\).
Monotone convergence of the nonnegative absolute integrals justifies the
infinite-shell limit.  \(\square\)

### 3.2 The closable \(\ell^1\) clock

Put

\[
 Y_{1,R}^{\rm clk}:=\sum_{k\ge1}v_{k,R}.
\tag{3.8}
\]

### Theorem 3.2 — shellwise BV closure

The quantity in (3.8) is finite and obeys

\[
 \boxed{
 Y_{1,R}^{\rm clk}
 \le C\left[(P_R^M)^{2/3}+P_R^M\right].}
\tag{3.9}
\]

It also controls the positive cumulative collar flux:

\[
 \boxed{
 \mathfrak C_R^M
 \le Y_{1,R}^{\rm clk}+C(P_R^M)^{2/3}.}
\tag{3.10}
\]

**Proof.**  Since \(K_k=Q_k+F_k\),

\[
 v_{k,R}\le\operatorname{TV}Q_{k,R}
              +\operatorname{TV}F_{k,R}.
\tag{3.11}
\]

Summing and applying Lemma 3.1 proves (3.9).  For every \(\tau<t_0\),
absolute convergence and (3.3) give

\[
\begin{aligned}
 \mathfrak F_R^M(\tau)
 &=\sum_{k\ge1}F_{k,R}(\tau)\\
 &=\sum_{k\ge1}\bigl(K_{k,R}(\tau)-Q_{k,R}(\tau)\bigr)\\
 &\le Y_{1,R}^{\rm clk}
   +\sum_{k\ge1}\operatorname{TV}Q_{k,R}.
\end{aligned}
\tag{3.12}
\]

Take the positive part and the supremum, then use (3.5).  \(\square\)

This is a valid theorem but not the desired compression.  The right side of
(3.9) is the already available quadratic cutoff plus the shellwise absolute
flux ledger.

### 3.3 Matched and over-weighted square functions

Define

\[
 \boxed{
 Y_{2,R}^{\rm sf}
 :=\left(\sum_{k\ge1}v_{k,R}^2\right)^{1/2}.}
\tag{3.13}
\]

The weight \(\gamma_k\) is already inside \(v_{k,R}\).  There is no
abstract inequality

\[
 \sum_kv_{k,R}\lesssim
 \left(\sum_kv_{k,R}^2\right)^{1/2}.
\tag{3.14}
\]

Indeed \(v_1=\cdots=v_N=1\) gives \(N\) on the left and \(\sqrt N\) on
the right.  Any proof replacing (3.8) by (3.13) must use additional PDE or
shell-packing structure.

The negative control

\[
 Y_{2,R}^{\rm strong}
 :=\left(\sum_{k\ge1}\frac{v_{k,R}^2}{\gamma_k}\right)^{1/2}
\tag{3.15}
\]

does close the abstract sum:

\[
 Y_{1,R}^{\rm clk}
 \le\left(\sum_k\gamma_k\right)^{1/2}Y_{2,R}^{\rm strong}.
\tag{3.16}
\]

This follows from Cauchy--Schwarz.  Section 4 shows why (3.15) is too strong
on the exact family.

## 4. Exact-family discrimination

### Lemma 4.1 — target shell clock

On the R0.74O family, for all sufficiently large \(j\), the target component
satisfies, with constants uniform in \(j\),

\[
 \boxed{cT_*\le v_{j,R}\le CT_*.}
\tag{4.1}
\]

**Proof.**  The R0.74F terminal lobe has positive time measure and gives,
at its good times,

\[
 \frac{\Gamma}{R}
 \int_{\mathbb T^3}\Psi_j^R|u_*|^2
 \ge c\varkappa^2B^2LR^2=cT_*.
\tag{4.2}
\]

The measure term in (2.6) is nonnegative.  Since \(K_j(s_R)=0\), equations
(2.6)--(2.7) and (3.2) give \(v_{j,R}\ge cT_*\).

For the reverse bound, R0.74L's target-shell absolute true-packet theorem,
as assembled in R0.74N (4.1)--(4.2), bounds the nonnegative accumulated
absolute integrand uniformly for \(\tau<t_0\).  Monotone convergence as
\(\tau\uparrow t_0\) therefore gives

\[
 \operatorname{TV}F_{j,R}
 \le C\mathfrak a_*^2B\Gamma LR^4
 =C(BR^2)T_*\le CT_*.
\tag{4.3}
\]

On this exact zero-frame family, the pressure, pure-shear,
\(x_1\)-derivative, and residual-drift target-shell terms vanish.  Thus
(4.3) covers every nonzero physical target-shell term.  Lemma 3.1 and (0.2)
also give

\[
 \operatorname{TV}Q_{j,R}
 \le C(P_*^\alpha)^{2/3}
 \le C\frac{T_*}{K_*}=o(T_*).
\tag{4.4}
\]

Now use (3.11) and the boundedness of \(BR^2\).  \(\square\)

Consequently,

\[
 Y_{1,R}^{\rm clk}\ge cT_*,
 \qquad
 Y_{2,R}^{\rm sf}\ge cT_*.
\tag{4.5}
\]

No matching upper bound for the full quantities in (4.5) is asserted; the
other shells have not been discarded.  In contrast,

\[
 Y_{2,R}^{\rm strong}
 \ge\frac{v_{j,R}}{\sqrt\Gamma}
 \ge cT_*\Gamma^{-1/2},
\tag{4.6}
\]

which over-penalizes the target by an exponential factor.

### Theorem 4.2 — every fixed positive-order window mass misses the target

Let

\[
 E_R^\alpha(t)
 :=\frac1R\int_{\mathbb T^3}
 \Theta_R|z_\alpha(t)|^2\,dx,
\tag{4.7}
\]

and, for a fixed \(\sigma>0\), define

\[
 \mathcal C_{\sigma,R}(E)
 :=\sup_{J\Subset I_R,\ |J|>0}
 \left(\frac{|J|}{R^2}\right)^\sigma
 \fint_JE(t)\,dt.
\tag{4.8}
\]

Then, for all sufficiently large \(j\), the exact family satisfies, with a
constant independent of \(j\),

\[
 \boxed{
 \mathcal C_{\sigma,R}(E_*)
 \le CT_*K_*^{-\min\{\sigma,1\}}
 =o(T_*).}
\tag{4.9}
\]

The little-o statement holds for each fixed \(\sigma>0\); it is not uniform
as \(\sigma\downarrow0\).

**Proof.**  The exact weighted energy identity, the quadratic cutoff row,
and the R0.74O collar upper give

\[
 \operatorname*{ess\,sup}_{I_R}E_*(t)\le CT_*.
\tag{4.10}
\]

The R0.74H average quadratic row gives

\[
 \fint_{I_R}E_*(t)\,dt
 \le C(P_*^\alpha)^{2/3}
 \le C\frac{T_*}{K_*}.
\tag{4.11}
\]

Because \(|I_R|=R^2\), positivity implies, for
\(x=|J|/R^2\in(0,1)\),

\[
 x^\sigma\fint_JE_*
 \le CT_*\min\{x^\sigma,K_*^{-1}x^{\sigma-1}\}.
\tag{4.12}
\]

If \(0<\sigma<1\), the maximum occurs where the two powers meet,
\(x=K_*^{-1}\), and equals \(K_*^{-\sigma}\).  If \(\sigma=1\), the
maximum is \(K_*^{-1}\).  If \(\sigma>1\), the second branch increases and
its supremum as \(x\uparrow1\) is \(K_*^{-1}\).  This proves (4.9).
\(\square\)

At \(\sigma=0\), Lebesgue differentiation gives

\[
 \sup_{J\Subset I_R,\ |J|>0}\fint_JE
 =\operatorname*{ess\,sup}_{I_R}E.
\tag{4.13}
\]

Thus the limiting endpoint is precisely the original endpoint-energy row,
not a new positive-order Carleson mechanism.

### Proposition 4.3 — energy oscillation is a solved baseline

For \(\alpha=M\) at suitable-weak regularity, and for
\(\alpha\in\{M,F\}\) in the smooth class, define

\[
 \Omega_R^\alpha
 :=\sup_{J,K\Subset I_R,\ |J|,|K|>0}
 \left|\fint_JE_R^\alpha-\fint_KE_R^\alpha\right|.
\tag{4.14}
\]

Then

\[
 \Omega_R^\alpha
 =\operatorname*{ess\,sup}_{I_R}E_R^\alpha
 -\operatorname*{ess\,inf}_{I_R}E_R^\alpha,
\tag{4.15}
\]

and

\[
 \mathcal U_{\rm ext}^{\infty,\alpha,R}
 \le C\left[(P_R^\alpha)^{2/3}+\Omega_R^\alpha\right].
\tag{4.16}
\]

Therefore

\[
 Y_{{\rm full},R}^\alpha
 :=\Omega_R^\alpha+\mathcal D_{\rm ext}^{\alpha,R}
\tag{4.17}
\]

satisfies

\[
 X_R^\alpha
 \le C\left[(P_R^\alpha)^{2/3}
 +Y_{{\rm full},R}^\alpha\right].
\tag{4.18}
\]

On the exact family, for all sufficiently large \(j\), with constants
uniform in \(j\),

\[
 \Omega_R^{\alpha,*}\asymp
 Y_{{\rm full},R}^{\alpha,*}\asymp T_*.
\tag{4.19}
\]

**Proof.**  Every interval average lies between the essential infimum and
essential supremum.  Lebesgue differentiation supplies compact intervals
approaching both values, proving (4.15).  The essential supremum is at most
the mean plus the oscillation, and the R0.74H mean row is paid by
\(C(P_R^\alpha)^{2/3}\); this gives (4.16)--(4.18).

For (4.19), the terminal lobe gives
\(\operatorname*{ess\,sup}E_*\ge cT_*\), while (4.11) gives
\(\operatorname*{ess\,inf}E_*\le CT_*/K_*\).  This proves the lower
bound for \(\Omega_*\).  Equations (4.10) and
\(\mathcal D_{\rm ext}\le X_*\le CT_*\) give the upper bound.  \(\square\)

The baseline reconstructs the cutoff endpoint sufficient to dominate the
sharp exterior energy and explicitly reintroduces all exterior dissipation.
No reverse comparison with \(X_R^\alpha\) is claimed.

## 5. Fixed-scale weak stability

Consider a sequence of periodic suitable weak solutions satisfying the
standard Lin compactness bounds and, on every compact subcylinder,

\[
 u_n\to u\quad\hbox{strongly in }L^3,
 \qquad
 \nabla u_n\rightharpoonup\nabla u
 \quad\hbox{weakly in }L^2,
\tag{5.1}
\]

\[
 p_n\rightharpoonup p
 \quad\hbox{weakly in }L^{3/2}.
\tag{5.2}
\]

All paths below have the same fixed mollification scale \(R>0\) and the
same terminal point.

### Lemma 5.1 — path and moving-field convergence

The mollified paths satisfy

\[
 X_{n,R}\longrightarrow X_R
 \quad\hbox{uniformly on }\overline I_{8R},
\tag{5.3}
\]

and

\[
 a_{n,R}\to a_R\quad\hbox{strongly in }L^3_t.
\tag{5.4}
\]

After moving coordinates,

\[
 \begin{gathered}
 v_{n,R}\to v_R\quad\hbox{strongly in }L^3,\\
 \nabla v_{n,R}\rightharpoonup\nabla v_R
 \quad\hbox{weakly in }L^2,\\
 \pi_{n,R}\rightharpoonup\pi_R
 \quad\hbox{weakly in }L^{3/2}.
 \end{gathered}
\tag{5.5}
\]

**Proof.**  Fixed-scale convolution gives

\[
 \|(u_n-u)_R\|_{L^3_tC_x^1}
 \le C_R\|u_n-u\|_{L^3_{t,x}}\longrightarrow0.
\tag{5.6}
\]

Writing \(b_n=(u_n)_R\) and \(b=u_R\), (5.6) implies

\[
 \|b_n-b\|_{L^1_tC_x^0}\longrightarrow0,
 \qquad
 \sup_n\|\nabla b_n\|_{L^1_tL_x^\infty}<\infty.
\tag{5.6a}
\]

These are the direct inputs to the backward Caratheodory--Gronwall
stability estimate and prove (5.3).  Evaluation along the paths gives

\[
 \|a_{n,R}-a_R\|_{L^3_t}
 \le \|b_n-b\|_{L^3_tC_x^0}
 +\|\nabla b\|_{L^3_tL_x^\infty}
   \|X_{n,R}-X_R\|_{L^\infty_t},
\tag{5.6b}
\]

which proves (5.4).  Translation invariance and continuity of translations
in \(L^3\) prove the strong convergence in (5.5); approximate the limiting
field by a smooth function to handle the time-dependent shifts.  For every
smooth compactly supported \(\phi\),
\(\phi(t,x-X_{n,R}(t))\to\phi(t,x-X_R(t))\) strongly in the relevant
\(L^2\) and \(L^3\) dual spaces.  Testing against these translated
functions proves the weak gradient and pressure statements in (5.5).
\(\square\)

### Lemma 5.2 — total dissipation convergence

The measures defined by (2.1) satisfy

\[
 \boldsymbol\mu[u_n,p_n]
 \rightharpoonup^*\boldsymbol\mu[u,p]
 \quad\hbox{locally as Radon measures}.
\tag{5.7}
\]

**Proof.**  For a compactly supported smooth test \(\phi\),

\[
\begin{aligned}
 \langle\boldsymbol\mu_n,\phi\rangle
 ={}&\int\frac{|u_n|^2}{2}(\partial_t\phi+\Delta\phi)\\
 &+\int\left(\frac{|u_n|^2}{2}+p_n\right)u_n\cdot\nabla\phi.
\end{aligned}
\tag{5.8}
\]

Strong \(L^3\) convergence passes the quadratic and cubic terms.  Weak
\(L^{3/2}\) convergence of \(p_n\) pairs with strong \(L^3\) convergence
of \(u_n\).  Thus \(\boldsymbol\mu_n\to\boldsymbol\mu\) in distributions.
For a compact set \(K\), choose
\(0\le\chi\in C_c^\infty\) with \(\chi\ge1\) on \(K\).  Nonnegativity gives

\[
 \boldsymbol\mu_n(K)
 \le\langle\boldsymbol\mu_n,\chi\rangle
 \longrightarrow\langle\boldsymbol\mu,\chi\rangle.
\tag{5.8a}
\]

Thus the local masses are uniformly bounded.  Distributional convergence
of these nonnegative measures upgrades to local weak-* measure convergence.
\(\square\)

Lemma 5.2 is not used to take a hard time section of the measure.

### Lemma 5.3 — canonical clock convergence

For each fixed shell,

\[
 Q_{k,R}^{(n)}\longrightarrow Q_{k,R},
 \qquad
 F_{k,R}^{(n)}\longrightarrow F_{k,R}
 \quad\hbox{uniformly on }[s_R,t_0],
\tag{5.9}
\]

and hence

\[
 K_{k,R}^{(n)}\longrightarrow K_{k,R}
 \quad\hbox{uniformly on }[s_R,t_0].
\tag{5.10}
\]

**Proof.**  The quadratic integrands in (2.8) converge strongly in
\(L^1_t\) by Lemma 5.1.  The cubic and drift integrands in (2.9) also
converge strongly in \(L^1_t\), using (5.4)--(5.5).

Extend every cumulative integral continuously to \(\tau=t_0\).  By the
shellwise cancellation (1.3a), the signed pressure primitive may be
evaluated with \(\pi_{n,R}\), without its time-dependent gauge.  For each
fixed \(\tau\in[s_R,t_0]\), the factor

\[
 1_{(s_R,\tau)}\eta_Rv_{n,R}\cdot\nabla\Psi_k^R
\tag{5.11}
\]

converges strongly in \(L^3\).  Pairing it with the weakly convergent
pressure proves convergence of the pressure primitive at every fixed
\(\tau\).  If

\[
 g_n(t)=\int_{\mathbb T^3}
 \eta_R\pi_{n,R}v_{n,R}\cdot\nabla\Psi_k^R\,dy,
\tag{5.11a}
\]

then every measurable \(A\subset[s_R,t_0]\) satisfies

\[
 \int_A|g_n(t)|\,dt
 \le C_{k,R}\|\pi_{n,R}\|_{L^{3/2}}
 \left(
  \int_{A\times\mathbb T^3}|v_{n,R}|^3
 \right)^{1/3}.
\tag{5.11b}
\]

Strong \(L^3\) convergence makes the last factor uniformly small when
\(|A|\) is small.  Hence the pressure primitives are equicontinuous.
Pointwise convergence on the compact interval plus equicontinuity gives
uniform convergence.  This proves (5.9), and (2.10) gives (5.10).
\(\square\)

### Theorem 5.4 — lower semicontinuity of the clock observables

For every fixed shell,

\[
 v_{k,R}\le\liminf_{n\to\infty}v_{k,R}^{(n)}.
\tag{5.12}
\]

Consequently,

\[
 Y_{1,R}^{\rm clk}[u,p]
 \le\liminf_{n\to\infty}Y_{1,R}^{\rm clk}[u_n,p_n],
\tag{5.13}
\]

and

\[
 \boxed{
 Y_{2,R}^{\rm sf}[u,p]
 \le\liminf_{n\to\infty}Y_{2,R}^{\rm sf}[u_n,p_n].}
\tag{5.14}
\]

**Proof.**  Fix a finite partition in (3.1).  Uniform convergence (5.10)
passes every positive increment to the limit.  The sum for that partition
is bounded by \(v_{k,R}^{(n)}\); take the lower limit and then the supremum
over partitions to obtain (5.12).

For \(q\in\{1,2\}\) and every finite \(M\), (5.12) and finite Fatou give

\[
 \sum_{k=1}^M v_{k,R}^{\,q}
 \le\liminf_{n\to\infty}
     \sum_{k=1}^M\bigl(v_{k,R}^{(n)}\bigr)^q
 \le\liminf_{n\to\infty}
     \sum_{k\ge1}\bigl(v_{k,R}^{(n)}\bigr)^q.
\tag{5.14a}
\]

Let \(M\uparrow\infty\); for \(q=2\), take the square root.  This proves
(5.13)--(5.14).  \(\square\)

### Proposition 5.5 — lower semicontinuity of the window baselines

At fixed \(R\), Lemma 5.1 gives

\[
 E_{R,n}\longrightarrow E_R\quad\hbox{strongly in }L^1(I_R).
\tag{5.15}
\]

Therefore, for every fixed \(\sigma>0\),

\[
 \mathcal C_{\sigma,R}(E_R)
 \le\liminf_n\mathcal C_{\sigma,R}(E_{R,n}),
 \qquad
 \Omega_R(E_R)\le\liminf_n\Omega_R(E_{R,n}).
\tag{5.16}
\]

Weak \(L^2\) convergence of the moving gradients and positivity of the
fixed shell weights also give

\[
 \mathcal D_{\rm ext}^{M,R}[u]
 \le\liminf_n\mathcal D_{\rm ext}^{M,R}[u_n].
\tag{5.17}
\]

Hence \(Y_{{\rm full},R}^M\) is lower semicontinuous.

**Proof.**  Every fixed-window average is continuous under (5.15).
The quantities in (5.16) are suprema of continuous fixed-window
functionals, hence are lower semicontinuous.  Equation (5.17) follows first
as follows.  Let

\[
 N_{k,R}(y)
 :=\sum_{m\in\mathbb Z^3}
 1_{A_k(R)}(y+2\pi m),
 \qquad
 w_{M,R}:=\sum_{k=1}^M\gamma_kN_{k,R}.
\tag{5.17a}
\]

For fixed \(M\), \(w_{M,R}\) is bounded and nonnegative.  The weak gradient
convergence in (5.5) gives

\[
 \sqrt{w_{M,R}}\,\nabla v_{n,R}
 \rightharpoonup
 \sqrt{w_{M,R}}\,\nabla v_R
 \quad\hbox{weakly in }L^2.
\tag{5.17b}
\]

Weak Hilbert-space lower semicontinuity proves the finite-shell
dissipation inequality.  Finally,
\(\mathcal D_{\rm ext}^{M,R}=\sup_M\mathcal D_{{\rm ext},M}^{M,R}\);
monotone convergence proves (5.17).  The sum of the two nonnegative
lower-semicontinuous terms is again lower semicontinuous.
\(\square\)

## 6. What remains open

The results can be organized without conflating their roles:

- \(Y_{1,R}^{\rm clk}\) is rigorously closable but retains the full
  shellwise absolute-flux ledger.
- The target component of \(Y_{2,R}^{\rm sf}\) is comparable to \(T_*\),
  so the full square function passes the lower detection gate and has the
  desired fixed-scale weak lower semicontinuity.  Its full-family upper
  bound remains open.
- \(Y_{2,R}^{\rm strong}\) closes by Cauchy--Schwarz but pays the target
  shell by the exponentially excessive factor \(\Gamma^{-1/2}\).
- Positive-order temporal Carleson masses are too small on the exact family.
- Energy oscillation is stable and detects the family, but it reconstructs
  the cutoff endpoint rather than yielding a weaker flux mechanism.

The central open inequality is a PDE statement, not a sequence-space fact:

\[
 \mathfrak C_R^M
 \stackrel{?}{\le}
 C\left[(P_R^M)^{2/3}+Y_{2,R}^{\rm sf}\right].
\tag{6.1}
\]

The finite equal-entry sequence rules out a purely abstract proof.  A proof
of (6.1) would require an effective-shell theorem, a scale-packing estimate,
or another Navier--Stokes relation between the clocks.

Even (6.1) would not finish the regularity problem.  Small \(P_R^M\) already
implies regularity by R0.74I.  One useful interface could be a contraction

\[
 \mathcal E_{\theta R}
 \le\lambda\mathcal E_R
 +C\left[(P_R^M)^{2/3}+Y_{2,R}^{\rm sf}\right],
 \qquad 0<\theta<1,\quad 0<\lambda<1,
\tag{6.2}
\]

but only together with a proof that the
additive terms are small or summable along a nested sequence of prescribed
scales.  Equation (6.2) by itself is not a regularity criterion.

An alternative interface would be a prescribed-centre scale-packing theorem
forcing radii \(R_n\downarrow0\) that satisfy a named smallness gate, such
as the R0.74I moving-energy epsilon gate.  A regular strip, spatial interval,
or time epoch chosen after seeing the solution does not supply that
prescribed-centre conclusion.

## 7. Primary-literature boundary

The following sources establish the surrounding tools, not the new clock
theorem.

- Caffarelli, Kohn, and Nirenberg establish the suitable-weak local-energy
  framework and partial regularity:
  [CPAM 35 (1982)](https://doi.org/10.1002/cpa.3160350604).
- Lin's compactness theorem gives the standard suitable-weak subsequence and
  strong local \(L^q\) convergence for every \(q<10/3\), including the
  strong \(L^3\) convergence used here:
  [CPAM 51 (1998)](https://doi.org/10.1002/(SICI)1097-0312(199803)51:3%3C241::AID-CPA2%3E3.0.CO;2-A).
- Duchon and Robert separate viscous dissipation from the anomalous local
  energy defect and give the velocity-increment representation of the
  latter:
  [Nonlinearity 13 (2000)](https://doi.org/10.1088/0951-7715/13/1/312).
- Yang constructs trajectories of spatially mollified incompressible flows
  and skewed-cylinder maximal functions:
  [arXiv:2008.05588](https://arxiv.org/abs/2008.05588).
- Vasseur and Yang use related skewed cylinders for suitable-solution
  derivative estimates, but not the clock BV or shell square function:
  [arXiv:2009.14291](https://arxiv.org/abs/2009.14291).
- Dascaliuc and Grujic study ensemble-averaged fluxes through fixed physical
  shells, not moving positive-variation clocks:
  [arXiv:1101.2193](https://arxiv.org/abs/1101.2193).
- Lei and Ren obtain solution-chosen regular intervals in one spatial
  direction and quantitative epochs of regularity.  Neither selection
  forces a shrinking scale sequence through a prescribed spacetime centre:
  [arXiv:2210.01783](https://arxiv.org/abs/2210.01783).
- Yu's 2026 preprint studies moving parabolic window chains, local-energy
  supply--tax ledgers, and scale-defect packages for suitable weak solutions.
  It is an adjacent method, but it does not state the mollified-trajectory
  defect-completed shell clock, temporal positive-variation BV theorem, or
  matched shell-\(\ell^2\) lower-semicontinuity result proved here:
  [arXiv:2606.13887](https://arxiv.org/abs/2606.13887).

The measure convergence in Lemma 5.2 and the fixed-scale path convergence in
Lemma 5.1 are direct consequences of the displayed topology.  The canonical
clock convergence and positive-variation lower semicontinuity are project
lemmas proved in Section 5; they are not attributed to the cited papers.

A bounded exact-phrase and nearest-method search, including the adjacent Yu
preprint, did not locate the same
defect-completed moving shell-clock BV or matched shell-\(\ell^2\) theorem.
This is only a bounded non-hit.  It is not evidence of novelty or priority.

## 8. Conclusion

R0.74P removes two misleading routes and leaves one precise gate.

1. Positive-order temporal window masses cannot see the exact concentration.
2. Energy oscillation can see it, but largely repackages the endpoint.
3. Defect-completed shell clocks make the local-energy balance compatible
   with suitable-weak limits.
4. Its target-shell component has the right scale, so the matched square
   function passes the lower detection gate and has fixed-scale weak
   stability; a full upper bound remains open.
5. Compressing the full shellwise collar ledger to that square function, or
   forcing a prescribed good scale, remains open.

No singular solution is constructed, no singularity is excluded, and no
global regularity theorem is proved.  **NOT CLAY.**
