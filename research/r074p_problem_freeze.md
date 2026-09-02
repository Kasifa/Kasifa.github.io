# R0.74P problem freeze — temporal concentration and shell-clock compression

## Status at freeze

R0.74O proves that neither the positive cumulative collar flux nor the
endpoint quantity can be bounded universally by the frozen scalar payment at
the square-root-log scale.  Along one exact smooth periodic family,

\[
 X_*^\alpha\asymp\mathfrak C_*^\alpha
 \asymp T_*:=\varkappa^2B^2LR^2,
 \qquad
 P_*^\alpha\asymp B^3R^3,
\tag{F.1}
\]

where

\[
 \varkappa=L^{2/3}\exp\!\left(\frac m3L^2\right),
 \qquad m=\frac{43}{423360}>0.
\tag{F.2}
\]

In particular,

\[
 \frac{T_*}{(P_*^\alpha)^{2/3}}
 \asymp K_*:=\varkappa^2L\longrightarrow\infty.
\tag{F.3}
\]

Any nonnegative additive repair of the rejected scalar endpoint must detect
at least the scale \(T_*\).  R0.74P freezes the first search for such a
repair.  It does not assume that a temporal, BV, Carleson, or square-function
observable works merely because it is finite.

The principal conclusion to be tested is deliberately narrower:

> Is there a fixed-scale observable which detects \(T_*\), is not just the
> total collar flux in different notation, is lower semicontinuous under the
> standard suitable-weak compactness topology, and has a genuine route to a
> prescribed good scale?

This is not a singularity construction or a regularity theorem. **NOT CLAY.**

## 1. Frozen Version-M weak setting

Work first in the suitable-weak Version-M frame from R0.74I.  Let

\[
 v_R(t,y)=u(t,y+X_R(t)),
 \qquad
 \dot X_R(t)=u_R(t,X_R(t)),
 \qquad X_R(t_0)=x_0,
\tag{F.4}
\]

and retain the smooth periodic shell cutoffs \(\Psi_k^R\), weights

\[
 \gamma_k=e^{-4^{k-1}/32},
\tag{F.5}
\]

the nondecreasing time cutoff \(\eta_R\), and

\[
 s_R=t_0-4R^2.
\tag{F.6}
\]

For a suitable weak solution, define the total local dissipation measure by

\[
 \boldsymbol\mu[u,p]
 :=-\partial_t\frac{|u|^2}{2}
   -\nabla\!\cdot\!\left[
     \left(\frac{|u|^2}{2}+p\right)u
   \right]
   +\Delta\frac{|u|^2}{2}.
\tag{F.7}
\]

The local energy inequality gives the stronger measure inequality

\[
 \boldsymbol\mu\ge |\nabla u|^2\,dx\,dt.
\tag{F.7a}
\]

Thus \(\boldsymbol\mu\) is a nonnegative Radon measure.  In the smooth
class,

\[
 d\boldsymbol\mu=|\nabla u|^2\,dx\,dt.
\tag{F.8}
\]

Thus (F.7) includes both viscous dissipation and the nonnegative anomalous
defect

\[
 \boldsymbol D[u,p]
 :=\boldsymbol\mu[u,p]-|\nabla u|^2\,dx\,dt\ge0.
\tag{F.8a}
\]

The anomalous part alone is not an admissible primary observable: it
vanishes on the smooth R0.74O family.  Moreover, when
\(\boldsymbol\mu_n\rightharpoonup^*\boldsymbol\mu\) and
\(\nabla u_n\rightharpoonup\nabla u\), weak lower semicontinuity gives,
for nonnegative tests, an upper-semicontinuity inequality for
\(\boldsymbol D_n\), which is the wrong one-sided direction for the
candidate repair.

## 2. Defect-completed shell clocks

For each shell \(k\ge1\), define the unweighted clock

\[
\begin{aligned}
 \widetilde K_{k,R}(\tau)
 :={}&\frac{\eta_R(\tau)}{2R}
  \int_{\mathbb T^3}\Psi_k^R(y)|v_R(\tau,y)|^2\,dy\\
 &+\frac1R
  \int_{(s_R,\tau)\times\mathbb T^3}
  \eta_R(t)\Psi_k^R(x-X_R(t))
  \,d\boldsymbol\mu(t,x).
\end{aligned}
\tag{F.9}
\]

Formula (F.9) is first read at local-energy good times.  Write
\(a_R=\dot X_R\), \(\pi_R(t,y)=p(t,y+X_R(t))\), and define the two
gamma-weighted cumulative terms

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
\tag{F.9a}
\]

\[
\begin{aligned}
 F_{k,R}(\tau)
 :={}&\frac{\gamma_k}{R}
 \int_{s_R}^{\tau}\!\int_{\mathbb T^3}\eta_R(t)
 \left[
  \frac12|v_R|^2(v_R-a_R)+\pi_Rv_R
 \right]\!\cdot\nabla\Psi_k^R\,dy\,dt.
\end{aligned}
\tag{F.9b}
\]

A time-dependent pressure gauge does not change (F.9b).  The integrands in
(F.9a)--(F.9b) lie in \(L^1_t\), so both cumulative terms have canonical
absolutely continuous representatives.

Put the physical shell weight inside the clock:

\[
 \boxed{K_{k,R}:=\gamma_k\widetilde K_{k,R}.}
\tag{F.10}
\]

The local-energy balance gives, first at good times and then by the unique
absolutely continuous representative,

\[
 K_{k,R}(\tau)=Q_{k,R}(\tau)+F_{k,R}(\tau),
 \qquad
 K_{k,R}(s_R)=0,
 \qquad K_{k,R}\ge0,
\tag{F.11}
\]

where \(Q_{k,R}\) is the signed quadratic cutoff clock and \(F_{k,R}\)
is the weighted cumulative physical shell flux.  The frozen total collar
flux is

\[
 \mathfrak F_R^M(\tau)=\sum_{k\ge1}F_{k,R}(\tau).
\tag{F.12}
\]

For a real-valued function \(f\), write

\[
 \operatorname{Var}^{+}_{[s_R,t_0)}f
 :=\sup_{s_R=\tau_0<\cdots<\tau_N<t_0}
 \sum_{i=1}^N
 [f(\tau_i)-f(\tau_{i-1})]_+.
\tag{F.13}
\]

The shell-clock row is

\[
 v_{k,R}:=\operatorname{Var}^{+}_{[s_R,t_0)}K_{k,R}.
\tag{F.14}
\]

Since every clock is nonnegative and starts at zero,

\[
 K_{k,R}(\tau)\le v_{k,R}.
\tag{F.15}
\]

Endpoint representatives, terminal good times, and the limit
\(\tau\uparrow t_0\) must be fixed in the proof.  Formula (F.14) is not
allowed to hide those issues.

## 3. Three aggregation levels

The immediately closable shellwise BV quantity is

\[
 \boxed{Y_{1,R}^{\rm clk}:=\sum_{k\ge1}v_{k,R}.}
\tag{F.16}
\]

Define the shellwise absolute quadratic ledger

\[
 \mathfrak Q_{{\rm sh,abs},R}^M
 :=\frac1{2R}\sum_k\gamma_k
 \int_{s_R}^{t_0}\!\int_{\mathbb T^3}
 \left(|\eta_R'|\Psi_k^R+\eta_R|\Delta\Psi_k^R|\right)|v_R|^2.
\tag{F.16a}
\]

The R0.74H weighted \(S_2\) argument applies before the shell sum and its
absolute shell-flux argument applies before time integration.  They imply

\[
 \sum_k\operatorname{TV}_{[s_R,t_0)}Q_{k,R}
 \le \mathfrak Q_{{\rm sh,abs},R}^M
 \le C(P_R^M)^{2/3},
\tag{F.17}
\]

and

\[
 \sum_k\operatorname{TV}_{[s_R,t_0)}F_{k,R}
 \le \mathfrak L_{{\rm abs},R}^M
 \le CP_R^M.
\tag{F.17a}
\]

Consequently,

\[
 \mathfrak C_R^M
 \le Y_{1,R}^{\rm clk}+C(P_R^M)^{2/3}
\tag{F.18}
\]

and

\[
 Y_{1,R}^{\rm clk}
 \le C\left[(P_R^M)^{2/3}+P_R^M\right].
\tag{F.19}
\]

Indeed, for every \(\tau<t_0\),

\[
 \sum_kF_{k,R}(\tau)
 =\sum_k\bigl(K_{k,R}(\tau)-Q_{k,R}(\tau)\bigr)
 \le Y_{1,R}^{\rm clk}+\sum_k\operatorname{TV}Q_{k,R},
\tag{F.19a}
\]

which proves (F.18) after taking the positive part and supremum.  Also
\(\operatorname{Var}^+(Q_k+F_k)\le\operatorname{TV}Q_k+
\operatorname{TV}F_k\); summing (F.17)--(F.17a) proves (F.19).

This is a valid closure but not the desired end point: it is equivalent to
the quadratic cutoff plus a shellwise absolute-flux/BV ledger.

The scale-matched square-function candidate is

\[
 \boxed{
 Y_{2,R}^{\rm sf}
 :=\left(\sum_{k\ge1}v_{k,R}^2\right)^{1/2}.}
\tag{F.20}
\]

The super-Gaussian factor is already inside \(v_{k,R}\).  It therefore
cannot be used a second time to assert the false abstract inequality

\[
 \sum_kv_{k,R}\lesssim
 \left(\sum_kv_{k,R}^2\right)^{1/2}.
\tag{F.21}
\]

The finite sequence \(v_1=\cdots=v_N=1\) gives \(N\) on the left and
\(\sqrt N\) on the right.  Any proof of (F.21) must use new Navier--Stokes
structure, an effective-shell theorem, or a separate scale-packing
hypothesis.

For comparison, the over-weighted square function

\[
 Y_{2,R}^{\rm strong}
 :=\left(
  \sum_{k\ge1}\frac{v_{k,R}^2}{\gamma_k}
 \right)^{1/2}
\tag{F.22}
\]

does satisfy

\[
 Y_{1,R}^{\rm clk}
 \le\left(\sum_k\gamma_k\right)^{1/2}
 Y_{2,R}^{\rm strong}
\tag{F.23}
\]

by Cauchy--Schwarz.  It is deliberately retained as a negative control
because it over-penalizes a distant target shell.

## 4. Exact-family detection gate

On the R0.74O family, the target shell is \(k=j\) and

\[
 \Gamma=\gamma_j,
 \qquad
 \mathfrak a_*=\varkappa B\Gamma^{-1/2}.
\tag{F.24}
\]

The R0.74F terminal lobe gives, for every terminal good time,

\[
 \frac{\Gamma}{R}
 \int\Psi_j^R|u_*|^2
 \ge c\varkappa^2B^2LR^2=cT_*.
\tag{F.25}
\]

Since the total measure in (F.9) is nonnegative,

\[
 K_{j,R}(\tau)\ge cT_*,
 \qquad
 v_{j,R}\ge cT_*.
\tag{F.26}
\]

Consequently,

\[
 Y_{1,R}^{\rm clk}\ge cT_*,
 \qquad
 Y_{2,R}^{\rm sf}\ge cT_*.
\tag{F.27}
\]

The R0.74L target-shell absolute true-packet estimate, as inherited in
R0.74N Section 4, gives on the amplified family

\[
 \operatorname{TV}F_{j,R}
 \le C\mathfrak a_*^2B\Gamma LR^4
 =C(BR^2)T_*\le CT_*.
\tag{F.28a}
\]

Every other target-shell physical-flux term vanishes on the exact zero-frame
family.  Moreover,

\[
 \operatorname{TV}Q_{j,R}
 \le C(P_*^\alpha)^{2/3}
 \asymp CB^2R^2=CT_*/K_*=o(T_*).
\tag{F.28b}
\]

Since \(BR^2\) stays bounded, (F.28a)--(F.28b) give the target-component
upper bound

\[
 v_{j,R}\le CT_*.
\tag{F.28}
\]

No matching upper bound for the full \(Y_1\) or \(Y_2\) is frozen here.
Other shells must not be silently discarded.

The strong square function instead has

\[
 Y_{2,R}^{\rm strong}\ge cT_*\Gamma^{-1/2},
\tag{F.29}
\]

so it exceeds the necessary scale by an exponential factor.

## 5. Temporal Carleson kill test

Let

\[
 E_R^\alpha(t)
 :=\frac1R\int_{\mathbb T^3}
 \Theta_R|z_\alpha(t)|^2\,dx
\tag{F.30}
\]

and, for \(\sigma>0\), define the positive-order time-window mass

\[
 \mathcal C_{\sigma,R}(E)
 :=\sup_{J\Subset I_R,\ |J|>0}
 \left(\frac{|J|}{R^2}\right)^\sigma
 \fint_JE(t)\,dt.
\tag{F.31}
\]

Here and below, windows are intervals and \(|I_R|=R^2\).  The exponent
\(\sigma>0\) is fixed independently of the family index.

The R0.74O family satisfies

\[
 \operatorname*{ess\,sup}_{I_R}E_*\le CT_*,
 \qquad
 \fint_{I_R}E_*\le C\frac{T_*}{K_*}.
\tag{F.32}
\]

For \(x=|J|/R^2\), positivity gives

\[
 x^\sigma\fint_JE_*
 \le CT_*\min\left\{
 x^\sigma,K_*^{-1}x^{\sigma-1}
 \right\}.
\tag{F.33}
\]

For \(0<\sigma<1\), the two powers meet at \(x=K_*^{-1}\) and the
maximum is \(K_*^{-\sigma}\).  For \(\sigma=1\) it is \(K_*^{-1}\),
and for \(\sigma>1\) the supremum is again \(K_*^{-1}\).  Thus, for
each fixed \(\sigma>0\),

\[
 \boxed{
 \mathcal C_{\sigma,R}(E_*)
 \le CT_*K_*^{-\min\{\sigma,1\}}
 =o(T_*).}
\tag{F.34}
\]

Thus every positive-order member of (F.31) fails the exact-family
detection gate.  The little-o conclusion is not uniform as
\(\sigma\downarrow0\).  At \(\sigma=0\), the supremum collapses to

\[
 \sup_J\fint_JE
 =\operatorname*{ess\,sup}_{I_R}E,
\tag{F.35}
\]

which is the original endpoint-energy row rather than a new Carleson
observable.

## 6. Energy oscillation as a solved baseline

Define

\[
 \Omega_R^\alpha
 :=\sup_{J,K\Subset I_R,\ |J|,|K|>0}
 \left|
  \fint_JE_R^\alpha-
  \fint_KE_R^\alpha
 \right|.
\tag{F.36}
\]

For \(E_R^\alpha\in L^\infty(I_R)\),

\[
 \Omega_R^\alpha
 =\operatorname*{ess\,sup}_{I_R}E_R^\alpha
 -\operatorname*{ess\,inf}_{I_R}E_R^\alpha.
\tag{F.37}
\]

Indeed every window average lies between the essential infimum and
essential supremum, while Lebesgue differentiation supplies compact
intervals approaching both values.

The R0.74H quadratic row implies

\[
 \fint_{I_R}E_R^\alpha
 \le C(P_R^\alpha)^{2/3}.
\tag{F.38}
\]

Hence

\[
 \mathcal U_{\rm ext}^{\infty,\alpha,R}
 \le C\left[(P_R^\alpha)^{2/3}+\Omega_R^\alpha\right].
\tag{F.39}
\]

The full baseline

\[
 Y_{{\rm full},R}^\alpha
 :=\Omega_R^\alpha+\mathcal D_{\rm ext}^{\alpha,R}
\tag{F.40}
\]

therefore satisfies

\[
 X_R^\alpha
 \le C\left[(P_R^\alpha)^{2/3}
 +Y_{{\rm full},R}^\alpha\right].
\tag{F.41}
\]

This is a useful audit baseline, not the target repair.  It reconstructs the
cutoff endpoint energy needed to dominate
\(\mathcal U_{\rm ext}^{\infty,\alpha,R}\), modulo the already paid
average row, and it contains the full exterior dissipation explicitly.  No
reverse comparison with the sharp exterior endpoint is asserted.

On the exact family,

\[
 \Omega_R^{\alpha,*}\asymp
 Y_{{\rm full},R}^{\alpha,*}\asymp T_*.
\tag{F.42}
\]

For the lower bound, the terminal lobe gives
\(\operatorname*{ess\,sup}E_*\ge cT_*\), whereas (F.32) gives
\(\operatorname*{ess\,inf}E_*\le CT_*/K_*\).  The upper bound follows
from \(\operatorname*{ess\,sup}E_*\le CT_*\) and
\(\mathcal D_{\rm ext}^{\alpha,R}\le X_*^\alpha\le CT_*\).

Thus it passes detection but fails the strict non-circularity standard for
an eventual regularity mechanism.

## 7. Weak-stability gate

The intended fixed-scale compactness topology is

\[
 u_n\to u\quad\hbox{strongly in }L^3_{\rm loc},
 \qquad
 \nabla u_n\rightharpoonup\nabla u
 \quad\hbox{weakly in }L^2_{\rm loc},
\tag{F.43}
\]

\[
 p_n\rightharpoonup p
 \quad\hbox{weakly in }L^{3/2}_{\rm loc},
\tag{F.44}
\]

together with the standard local energy bounds.  At fixed \(R\), the proof
must establish:

1. uniform convergence of the mollified Version-M trajectories;
2. distributional, hence locally weak-*, convergence of the total
   dissipation measures, without using hard time sections of those measures;
3. convergence of (F.9a)--(F.9b) at every fixed partition time and hence
   convergence of the canonical absolutely continuous representatives
   \(K_{k,R}=Q_{k,R}+F_{k,R}\);
4. lower semicontinuity of \(v_{k,R}\);
5. Fatou passage from finite shells to \(Y_{2,R}^{\rm sf}\).

The third step avoids a genuine atom problem: weak-* convergence of
\(\boldsymbol\mu_n\) alone need not converge the mass of
\((s_R,\tau)\times\mathbb T^3\) when the limiting temporal marginal has
an atom at \(\tau\).  Instead, strong \(L^3\) convergence handles the
quadratic, cubic, and drift terms in (F.9a)--(F.9b), while weak
\(L^{3/2}\) convergence of \(p_n\) pairs with the strongly convergent
velocity-cutoff factor.  A fixed finite partition can then be passed term
by term, giving

\[
 v_{k,R}\le\liminf_{n\to\infty}v_{k,R}^{(n)}.
\tag{F.44a}
\]

Under the same fixed-scale path convergence, strong \(L^3_{\rm loc}\)
convergence gives \(E_{R,n}\to E_R\) in \(L^1(I_R)\).  Both
\(\mathcal C_{\sigma,R}\) and \(\Omega_R\) are then lower
semicontinuous because they are suprema of continuous fixed-window
average functionals.  Weak \(L^2\) convergence of the gradients gives
the corresponding lower semicontinuity of
\(\mathcal D_{\rm ext}\).  These conclusions depend on proving the
trajectory convergence; they do not follow from the formal
essential-supremum identities alone.

Only after these steps may the square function be labelled suitable-weak
stable.  Version F remains outside this freeze because its acceleration
row has no completed weak compactness theorem.

## 8. Genuine regularity gate

The statement

\[
 P_R^M+(Y_{2,R}^{\rm sf})^{3/2}\ll1
 \quad\Longrightarrow\quad\hbox{regularity}
\tag{F.45}
\]

is not by itself a new result: small \(P_R^M\) already implies regularity
through R0.74I.  A useful interface must instead prove at least one of:

\[
 \mathcal E_{\theta R}
 \le\lambda\mathcal E_R
 +C\left[(P_R^M)^{2/3}+Y_{2,R}^{\rm sf}\right],
 \qquad 0<\lambda<1,
\tag{F.46}
\]

or a scale-packing theorem at the prescribed centre which forces a sequence
\(R_n\downarrow0\) of genuinely good scales.  An almost-everywhere good
time or a regular subregion whose position is chosen after seeing the
solution does not meet this gate.

## 9. Promotion checklist

R0.74P may be promoted beyond a problem freeze only if all of the following
are explicit:

1. the sign and normalization of the total dissipation measure;
2. the shell weight is inside \(K_{k,R}\);
3. the \(\ell^1\), matched \(\ell^2\), and over-weighted \(\ell^2\)
   quantities are never interchanged;
4. (F.18)--(F.19), (F.26)--(F.29), and (F.34) are proved with all infinite
   shell limits justified;
5. weak stability is stated with its full compactness hypotheses;
6. the open \(\ell^1\)-to-\(\ell^2\) or good-scale gate remains visibly
   open unless a separate proof closes it;
7. no bounded literature search is promoted to novelty or priority.

## 10. Frozen outcome

The current hierarchy is:

- **REJECTED:** positive-order temporal energy Carleson masses, by (F.34);
- **PROVED BASELINE:** time-window energy oscillation, but it reconstructs
  endpoint energy modulo the paid average;
- **PROVED BUT FLUX-EQUIVALENT CANDIDATE:** shellwise \(\ell^1\) clock BV;
- **MAIN NONTRIVIAL CANDIDATE:** the matched shell-clock square function
  \(Y_{2,R}^{\rm sf}\);
- **OPEN:** compressing the shell \(\ell^1\) collar ledger to the matched
  \(\ell^2\) observable, or deriving a prescribed-centre good-scale theorem.

No item above proves a singularity, prevents one, or solves the global
regularity problem. **NOT CLAY.**
