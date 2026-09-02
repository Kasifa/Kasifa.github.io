# R0.74S Step 12 — terminal-window normal form and conditional Morrey packing

## 0. Result and scope

Step 11 reduced the open full-terminal clock estimate to two best-
\(N\) tails: the short non-dissipation residual \(r^{\rm sh}\) and the
selected dissipation excess \(x^{\rm sel}\), equivalently \(r^x\).  This
note does not prove either universal tail estimate.  It replaces both by
cleaner PDE interfaces and proves one conditional packing theorem.

There are six conclusions.

1. The short residual is bounded by a best-\(N\) tail of the absolute shell
   flux variation in one *common terminal window*, plus the already proved
   positive-depth cubic term.  Unlike the last-exit residual, this new
   window functional is continuous in the terminal time.
2. For each fixed solution and scale, absolute continuity makes the common-
   window variation vanish uniformly over all terminal times as the window
   shrinks.  The modulus is not uniform over solutions or scales.  A
   synchronized spike family proves that the inherited \(L_t^1\) ledger
   cannot supply any fixed-\(N\), \(P^{2/3}\)-scaled modulus.
3. An exact layer-cake identity turns the window problem into an integrated
   shell-counting problem at *every* amplitude level.  One-threshold bad-
   shell counts, or a critical \(A/t\) count without an endpoint gain, do
   not suffice.
4. The selected excess splits into anomalous-defect and high-Rayleigh
   ancestors.  Their exception budgets must be added.  CKN size information
   for the singular set cannot count the high-Rayleigh part and, by itself,
   cannot control the mass of the defect part.
5. If the total local dissipation has one uniform critical Morrey coefficient
   on \(R\)-cylinders and the lifted mollified path has uniformly bounded
   length in units of \(R\), then a sharpened moving-tube covering gives
   \[
      \sum_k x_k^{\rm sel}\le
      C M\bigl(\mathscr A_3+L\mathscr A_2\bigr).
   \]
   Combining this finite cap with the inherited linear payment proves the
   selected-excess gate with \(N_x=0\).  A scale-critical mixed-norm ball is
   one sufficient source of the two uniform coefficients; this is a
   conditional benchmark, not a theorem for the bare suitable-weak class.
6. Speeding up one inherited passive packet is not presently a route around
   the cubic obstruction.  The frozen family makes no full torus winding;
   in a hypothetical monotone many-winding extension, an exact occupation
   estimate cancels the speed gain.  This is a kinematic screen, not a
   universal Navier--Stokes theorem.

The new universal PDE inputs stated below remain **OPEN**.  Nothing here
proves the combined Step 11 gate (S.272), Q.12, Q.1, scale contraction,
regularity, singularity formation, or the Millennium problem.  The
conditional Morrey and mixed-norm conclusions carry constants depending on
their additional uniform bounds.  No novelty or priority claim is made.
**NOT CLAY.**

No DNS, floating-point asymptotics, or DGX computation is used.

## 1. Frozen setting and the common terminal window

Retain every definition of R0.74S Steps 10--11.  In particular,

\[
 \mathcal T_R=(s_R,t_0),\qquad |\mathcal T_R|=4R^2,
 \qquad A_R=(P_R^M)^{2/3},
\]

and for every local-energy good terminal
\(\tau\in\mathcal G_R\cap\mathcal T_R\),

\[
 r^{\rm sh}_k(\tau)
 =\mathbf 1_{\mathcal R_{\rm sh}(\tau)}
   \bigl[F_{k,R}(\tau)-F_{k,R}(\ell_k)\bigr],
 \qquad d_k={\tau-\ell_k\over R^2}.
\]

The canonical primitives \(F_{k,R}\) are absolutely continuous, and the
inherited absolute shell-flux ledger is

\[
 \sum_{k\ge1}\int_{\mathcal T_R}|\dot F_{k,R}(t)|\,dt
 \le \mathfrak L_{{\rm abs},R}^M
 \le C_FP_R^M.
\]

For \(0<\delta<4\), extend every \(|\dot F_{k,R}|\) by zero outside
\(\mathcal T_R\), and define

\[
 \boxed{
 \begin{aligned}
 J_{\tau,\delta}
  &:=(\max\{s_R,\tau-\delta R^2\},\tau),\\
 f_{k,R}(\tau,\delta)
  &:=\int_{J_{\tau,\delta}}|\dot F_{k,R}(t)|\,dt,\\
 \mathcal V^F_{N,R}(\tau,\delta)
  &:=\mathcal S_N\bigl((f_{k,R}(\tau,\delta))_{k\ge1}\bigr).
 \end{aligned}}
\tag{S.273}
\]

The vector in (S.273) belongs to \(\ell^1_+\).  Its deletion set is one
common shell set for the whole window; it is not allowed to vary with time
inside the integral.

## 2. Exact terminal variation-window reduction

### Proposition 2.1 — common-window domination of the short trace

For every shell set \(S\subset\mathbb N\), every good terminal, and every
\(0<\delta<4\),

\[
 \boxed{
 \sum_{\substack{k\in\mathcal R_{\rm sh}(\tau)\setminus S\\d_k\le\delta}}
 r_k^{\rm sh}(\tau)
 \le\sum_{k\notin S}f_{k,R}(\tau,\delta).}
\tag{S.274}
\]

Consequently, for every integer \(N\ge0\),

\[
 \boxed{
 \mathcal S_N(r^{\rm sh}(\tau))
 \le \mathcal V^F_{N,R}(\tau,\delta)
 +C_{\rm deep}\delta^{-2/3}A_R,\qquad
 C_{\rm deep}:=
 3C_1^{2/3}C_P^{2/3}\mathscr A_0^{1/3}.}
\tag{S.275}
\]

Here \(\mathscr A_0=\sum_{k\ge1}2^{3k}\gamma_k<\infty\), and the
constants are exactly those of Step 11 (S.259).

**Proof.**  If \(k\in\mathcal R_{\rm sh}(\tau)\) and \(d_k\le\delta\),
then

\[
 \ell_k=\tau-d_kR^2\ge\tau-\delta R^2,
 \qquad J_k^{\rm LE}=(\ell_k,\tau)\subset J_{\tau,\delta}.
\]

When \(d_k=\delta\), the left endpoints agree and both intervals are open,
so the inclusion remains literal.  The canonical AC representative gives
the identity even when \(\ell_k\) is not a good time:

\[
 0<r_k^{\rm sh}
 =\int_{\ell_k}^{\tau}\dot F_{k,R}(t)\,dt
 \le\int_{J_{\tau,\delta}}|\dot F_{k,R}(t)|\,dt.
\]

Sum by Tonelli to prove (S.274).  Step 11 (S.259), applied after deleting
the same \(S\), gives

\[
 \sum_{\substack{k\in\mathcal R_{\rm sh}(\tau)\setminus S\\d_k>\delta}}
 r_k^{\rm sh}\le C_{\rm deep}\delta^{-2/3}A_R.
\]

The two duration classes are disjoint and exhaustive.  Add them and take
the infimum over \(\#S\le N\). \(\square\)

The gain in (S.275) is structural.  It removes all last-exit selectors and
branch masks from the new term and replaces their shell-dependent intervals
by one terminal window.

## 3. Terminal continuity and the missing uniform modulus

Put

\[
 g_R(t):=\sum_{k\ge1}|\dot F_{k,R}(t)|.
\]

Tonelli and the absolute ledger give \(g_R\in L^1(\mathcal T_R)\).  For
fixed \(\delta\), if \(\tau_n\to\tau\), then

\[
 \begin{aligned}
 \bigl\|f_R(\tau_n,\delta)-f_R(\tau,\delta)\bigr\|_{\ell^1}
 &\le\int_{J_{\tau_n,\delta}\triangle J_{\tau,\delta}}g_R(t)\,dt
 \longrightarrow0,\\
 |\mathcal S_N(a)-\mathcal S_N(b)|
 &\le\|a-b\|_{\ell^1}\qquad(a,b\in\ell^1_+).
 \end{aligned}
\tag{S.276}
\]

The second line follows because \(\mathcal S_N\) is the infimum of the
uniformly one-Lipschitz maps \(a\mapsto\sum_{k\notin S}a_k\),
\(\#S\le N\).  Hence
\(\tau\mapsto\mathcal V^F_{N,R}(\tau,\delta)\) is continuous.  Since
\(\mathcal G_R\) has full measure and is dense,

\[
 \sup_{\tau\in\mathcal G_R\cap\mathcal T_R}
 \mathcal V^F_{N,R}(\tau,\delta)
 =\sup_{\tau\in\mathcal T_R}
 \mathcal V^F_{N,R}(\tau,\delta).
\]

This terminal continuity is not known for the original last-exit residual.

For each fixed pair \((u,R)\), absolute continuity of the Lebesgue integral
also gives

\[
 \boxed{
 \Omega_{u,R}(\delta)
 :=\sup_{\tau\in\mathcal T_R}
    \sum_k f_{k,R}(\tau,\delta)
 \longrightarrow0\qquad(\delta\downarrow0).}
\tag{S.277}
\]

Indeed, all windows have measure at most \(\delta R^2\).  The modulus in
(S.277) depends on the solution and scale.  Substitution into (S.275) does
not produce a universal estimate, because the positive-depth term grows as
\(\delta^{-2/3}A_R\).

## 4. Layer cake: the exact all-threshold counting problem

For \(z\in\ell^1_+\), define
\(n_z(t):=\#\{k:z_k>t\}\).  Deleting the \(N\) largest coordinates and
then applying Tonelli gives

\[
 \boxed{
 \mathcal S_N(z)
 =\int_0^\infty\bigl(n_z(t)-N\bigr)_+\,dt.}
\tag{S.278}
\]

In particular, if \(A_R>0\),

\[
 \mathcal V^F_{N,R}(\tau,\delta)
 =A_R\int_0^\infty
 \left(\#\{k:f_{k,R}(\tau,\delta)>sA_R\}-N\right)_+ds.
\]

If \(A_R=0\), then \(P_R^M=0\), the inherited absolute-variation ledger
forces every \(f_{k,R}=0\), and the window estimate is automatic.

Thus a sufficient distributional theorem is: find a fixed \(N_F\) and one
\(\Phi\in L^1(0,\infty)\), independent of the solution, scale, and terminal,
such that

\[
 \boxed{
 \#\{k:f_{k,R}(\tau,\delta_*)>sA_R\}
 \le N_F+\Phi(s)\quad(s>0)
 \quad\Longrightarrow
 \mathcal V^F_{N_F,R}(\tau,\delta_*)
 \le A_R\|\Phi\|_{L^1}.}
\tag{S.279}
\]

A count at one threshold is insufficient.  The critical bound
\(n_z(t)-N\lesssim A_R/t\) also has a logarithmically divergent layer-cake
integral unless an additional lower-end cutoff or gain is supplied.

The clean short-branch PDE target is therefore

\[
 \boxed{
 \begin{gathered}
 \textbf{OPEN: find fixed }N_F,\ 0<\delta_*<4,\ C_F^*<\infty
 \textbf{ such that}\\
 \sup_{\tau\in\mathcal T_R}
 \mathcal V^F_{N_F,R}(\tau,\delta_*)\le C_F^*A_R
 \quad\text{for every solution and scale}.\\
 \text{Then (S.275) proves the short gate with }N_{\rm sh}=N_F.
 \end{gathered}}
\tag{S.280}
\]

This is a sufficient replacement for Step 11 (S.261), not an equivalent
reformulation.  It is stronger because it uses absolute flux variation in
all shells, but it has a fixed window, a continuous terminal functional,
and no moving branch selector.

## 5. What the inherited \(L_t^1\) ledger can and cannot give

The total absolute variation alone cannot imply (S.280).  Fix \(N\), put
\(M=N+1\), choose a terminal \(\tau_0\), and for \(H>0\) choose
\(0<\varepsilon_H<\delta\) with the common support inside
\(\mathcal T_R\).  For \(1\le k\le M\), set

\[
 g_{k,H}(t)
 ={H\over\varepsilon_HR^2}
  \mathbf1_{(\tau_0-\varepsilon_HR^2,\tau_0)}(t),
 \qquad F_{k,H}(t)=\int_{s_R}^tg_{k,H}(s)\,ds.
\]

Then every \(F_{k,H}\) is AC and

\[
 \boxed{
 \sum_k\int_{\mathcal T_R}|\dot F_{k,H}|=MH,
 \qquad \mathcal S_N\left(
   \left(\int_{J_{\tau_0,\delta}}|\dot F_{k,H}|\right)_k
 \right)=H,
 \qquad {H\over(MH)^{2/3}}={H^{1/3}\over M^{2/3}}\to\infty.}
\tag{S.281}
\]

This is a vector-valued translated-spike witness, not a Navier--Stokes
solution.  It proves that AC plus the linear total-mass ledger does not
contain a uniform fixed-\(N\), \(P^{2/3}\) window estimate.

There is an averaged terminal statement.  Fubini gives

\[
 \boxed{
 \int_{\mathcal T_R}\sum_kf_{k,R}(\tau,\delta)\,d\tau
 \le\delta R^2\int_{\mathcal T_R}g_R(t)\,dt
 \le C_F\delta R^2P_R^M.}
\tag{S.282}
\]

Hence, for \(0<\eta<1\), every good terminal outside a set of terminal
times of measure at most \(\eta R^2\) satisfies

\[
 \sum_kr_k^{\rm sh}(\tau)
 \le C\left(\eta^{-1}\delta P_R^M
             +\delta^{-2/3}A_R\right).
\tag{S.283}
\]

Whenever the constant-factor optimizer
\(\delta\asymp(\eta A_R/P_R^M)^{3/5}\) lies in \((0,4)\)—in particular,
in the sufficiently large-payment regime—optimizing the two displayed
powers yields only

\[
 \boxed{
 \sum_kr_k^{\rm sh}(\tau)
 \le C\eta^{-2/5}A_R^{3/5}(P_R^M)^{2/5}
 =C\eta^{-2/5}(P_R^M)^{4/5}}
\tag{S.284}
\]

on that large set of terminals.  This is weaker than the required
\(P^{2/3}\) scale and says nothing about the supremum terminal.  It records
the exact exponent reached by this averaging-plus-depth argument; it is not
claimed sharp for Navier--Stokes.

## 6. The excess branch and honest exception accounting

On the Step 8 priority-selected set \(\mathcal I_x(\tau)\), define

\[
 \boxed{
 \begin{aligned}
 d_k^{\rm def}(\tau)&:=\mathbf1_{\mathcal I_x(\tau)}m_{k,R}(\tau),\\
 h_k(\tau)&:=\mathbf1_{\mathcal I_x(\tau)}
             \int_{H_{k,R}}g_{k,R}(t)\,dt,\\
 b_k(\tau)&:=d_k^{\rm def}(\tau)+h_k(\tau),
 \qquad 0\le x_k^{\rm sel}(\tau)\le b_k(\tau).
 \end{aligned}}
\tag{S.285}
\]

The two ancestor vectors need not have disjoint support.  Nevertheless,
unioning deletion sets gives, for all \(N_D,N_H\ge0\),

\[
 \boxed{
 \mathcal S_{N_D+N_H}(x^{\rm sel})
 \le\mathcal S_{N_D+N_H}(d^{\rm def}+h)
 \le\mathcal S_{N_D}(d^{\rm def})+\mathcal S_{N_H}(h).}
\tag{S.286}
\]

Thus separate defect and high-Rayleigh theorems remain useful, but their
budgets add exactly as the two main residual budgets did in Step 11.

A mechanism-level sufficient lemma is the following.  Suppose there are one
fixed exceptional set \(E_\tau\), \(\#E_\tau\le N_b\), and nonnegative
sequences \(q,p,c\), possibly depending on \((u,R,\tau)\), such that outside
\(E_\tau\)

\[
 b_k\le q_k+c_kp_k^{2/3},\qquad
 \sum_kq_k\le C_qA_R,\qquad
 \sum_kp_k\le C_pP_R^M,\qquad
 \sum_kc_k^3\le C_c.
\]

Then shellwise Holder gives

\[
 \boxed{
 \mathcal S_{N_b}(b)
 \le\left(C_q+C_c^{1/3}C_p^{2/3}\right)A_R.}
\tag{S.287}
\]

The open content is the PDE construction of \(q,p,c,E_\tau\), with one
shared exception set and the full-history ancestry retained.  The bare
minimal statement remains

\[
 \boxed{
 \textbf{OPEN:}\quad
 \exists N_b,C_b\text{ fixed such that }
 \mathcal S_{N_b}(b(\tau))\le C_bA_R
 \text{ for every }(u,R)\text{ and }
 \tau\in\mathcal G_R\cap\mathcal T_R.}
\tag{S.288}
\]

It implies Step 11 (S.269), because \(x^{\rm sel}\le b\).

## 7. A conditional moving-tube Morrey theorem

The next theorem gives a rigorous benchmark for (S.288).  Let
\(\widetilde{\boldsymbol\mu}\) be the periodic lift of the total local
dissipation measure and \(\widetilde X_R\) a continuous lift of the
mollified path.  Define the full-history lifted tube

\[
 \boxed{
 \mathcal U_{k,R}(\tau)
 :=\{(t,y):s_R<t<\tau,
       y-\widetilde X_R(t)\in\operatorname {supp}\psi_k^R\}.}
\tag{S.289}
\]

Assume there are constants \(M,L<\infty\), common to the entire restricted
solution class, all admissible scales, and all terminals, such that

\[
 \boxed{
 \sup_{Q_R^-(z,s)\ {\rm\ in\ the\ }I_{8R}{\rm\ buffer}}
 {\widetilde{\boldsymbol\mu}(Q_R^-(z,s))\over R}\le M,
 \qquad
 \mathcal L_R(\tau):={1\over R}\int_{s_R}^{\tau}
             |\dot{\widetilde X}_R(t)|\,dt\le L.}
\tag{S.290}
\]

Here \(Q_R^-(z,s)=B_R(z)\times(s-R^2,s)\), clipped to the buffer when
necessary.  Both quantities in (S.290) are invariant under the
Navier--Stokes scaling.

### Lemma 7.1 — sharpened moving-tube cover

There is a cutoff-dependent constant \(C_\psi\) such that

\[
 \boxed{
 \mathcal U_{k,R}(\tau)\text{ is covered by at most }
 C_\psi\bigl(2^{3k}+L2^{2k}\bigr)
 \text{ backward }R\text{-cylinders}.}
\tag{S.291}
\]

**Proof.**  Greedily partition \((s_R,\tau)\) whenever either elapsed time
reaches a fixed multiple of \(R^2\), or accumulated path variation reaches
a fixed multiple of \(2^kR\).  Since the total time is at most \(4R^2\)
and the total variation is at most \(LR\), the number of pieces is at most
\(C(1+L/2^k)\).  On one piece the moving centre stays within
\(C2^kR\) of its initial value.  The padded dyadic shell is therefore
contained in a fixed ball of radius \(C2^kR\), coverable by
\(C2^{3k}\) balls of radius \(R\).  Each time piece has length at most
\(CR^2\), so a fixed number of backward time slabs completes the cover.
Multiplication gives (S.291). \(\square\)

The arc-length stopping is essential; endpoint displacement alone would
not control repeated excursions.  Periodic unfolding introduces no hidden
multiplicity: it converts the integral against the periodized cutoff into
the integral of the single Euclidean cutoff against
\(\widetilde{\boldsymbol\mu}\), and (S.291) covers that lifted tube.

Since
\(\boldsymbol\mu=|\nabla u|^2dxdt+\boldsymbol D\) exactly, the defect
integral and the restricted high-Rayleigh viscous integral add to at most
the total \(\boldsymbol\mu\)-mass of the tube.  Thus (S.285), unfolding,
and (S.290)--(S.291) give

\[
 \boxed{
 b_k(\tau)
 \le{\gamma_k\over R}
     \widetilde{\boldsymbol\mu}(\mathcal U_{k,R}(\tau))
 \le C_\psi M\gamma_k\bigl(2^{3k}+L2^{2k}\bigr).}
\tag{S.292}
\]

Set

\[
 \mathscr A_m:=\sum_{k\ge1}2^{mk}\gamma_k<\infty
 \qquad(m=2,3).
\]

Then

\[
 \boxed{
 \sum_kx_k^{\rm sel}(\tau)
 \le\sum_kb_k(\tau)
 \le B(M,L):=C_\psi M(\mathscr A_3+L\mathscr A_2).}
\tag{S.293}
\]

Independently, Step 11 (S.264) gives
\(\sum_kx_k^{\rm sel}\le C_0P_R^M\).  Therefore

\[
 \sum_kx_k^{\rm sel}
 \le\min\{C_0P_R^M,B(M,L)\}.
\]

If \(0\le P_R^M\le1\), use \(P_R^M\le A_R\).  If \(P_R^M\ge1\), use
\(B(M,L)\le B(M,L)A_R\).  This proves the conditional theorem

\[
 \boxed{
 \mathcal S_0(x^{\rm sel}(\tau))
 \le\max\{C_0,B(M,L)\}A_R.}
\tag{S.294}
\]

The same \(M,L\) must work throughout the class.  Allowing
\(M=M(u,R)\) or \(L=L(u,R)\) recovers only nonuniform fixed-solution
finiteness.

## 8. A scale-critical mixed-norm benchmark

The hypotheses of the conditional theorem can be generated by a standard
strong mixed-norm bound.  Let \(q\in[3,\infty]\) and
\(r\in[3,\infty)\), put

\[
 \theta={3\over r}+{2\over q},\qquad
 \boxed{
 \mathcal U_{q,r}(R)
 :=R^{1-\theta}
   \|u\|_{L_t^q(I_{8R};L_x^r(\mathbb T^3))}\le M_*}
\tag{S.295}
\]

with one \(M_*\) for every target scale in the restricted class.  Use the
mean-zero periodic pressure gauge.  Calderon--Zygmund gives

\[
 \boxed{
 \|p-\bar p(t)\|_{L_t^{q/2}L_x^{r/2}}
 \le C_r\|u\|_{L_t^qL_x^r}^2
 \le C_rM_*^2R^{2\theta-2}.}
\tag{S.296}
\]

A smooth spacetime test equal to one on a backward \(R\)-cylinder and
supported on its doubled cylinder, inserted directly into the distribution
defining \(\boldsymbol\mu\), gives

\[
 \begin{aligned}
 \boldsymbol\mu(Q_R^-)
 \le C\bigg[
 &R^{-2}\int_{Q_{2R}^-}|u|^2
 +R^{-1}\int_{Q_{2R}^-}|u|^3\\
 &+R^{-1}\int_{Q_{2R}^-}|p-\bar p(t)|\,|u|
 \bigg].
 \end{aligned}
\tag{S.297}
\]

Mixed Holder gives, before (S.295) is inserted,

\[
 \begin{aligned}
 R^{-2}\int|u|^2
 &\le CR^{3-2\theta}\|u\|_{L_t^qL_x^r}^2,\\
 R^{-1}\int|u|^3
 &\le CR^{4-3\theta}\|u\|_{L_t^qL_x^r}^3,\\
 R^{-1}\int|p-\bar p|\,|u|
 &\le CR^{4-3\theta}
   \|p-\bar p\|_{L_t^{q/2}L_x^{r/2}}
   \|u\|_{L_t^qL_x^r}.
 \end{aligned}
\]

The powers cancel exactly after (S.295)--(S.296): every right-hand term is
\(R\) times a function of \(M_*\).  Hence

\[
 \boxed{
 \sup_{Q_R^-}{\boldsymbol\mu(Q_R^-)\over R}
 \le C_{q,r}(M_*^2+M_*^3)=:M_\mu.}
\tag{S.298}
\]

For the mollified path,

\[
 |\dot X_R(t)|\le CR^{-3/r}\|u(t)\|_{L^r},
\]

and temporal Holder on an interval of length at most \(4R^2\) gives

\[
 \boxed{
 {1\over R}\int_{s_R}^{\tau}|\dot X_R(t)|\,dt
 \le CM_*R^{-1-3/r+2-2/q+\theta-1}
 =CM_*.}
\tag{S.299}
\]

Substitute \(M=M_\mu\) and \(L=CM_*\) into (S.294):

\[
 \boxed{
 \mathcal S_0(x^{\rm sel}(\tau))
 \le C_{q,r,M_*}A_R.}
\tag{S.300}
\]

This corollary is intentionally a sanity check.  At or below the
Prodi--Serrin critical line, fixed strong norm balls are already covered by
stronger regularity theory.  When \(\theta>1\), finiteness of a global mixed
norm for each solution does not imply (S.295): the factor
\(R^{1-\theta}\) requires an explicit scale-Morrey decay rate.  Weak
\(L^3\) cannot be substituted into the cubic line of (S.297) without a
separate Lorentz endpoint argument.

## 9. Why partial regularity does not close the excess gate

At a regular point the local energy equality holds, so the anomalous defect
is supported in the singular set.  Caffarelli--Kohn--Nirenberg proves that
this set has zero one-dimensional parabolic Hausdorff measure.  That is a
support-size conclusion, not an upper-density estimate for
\(\boldsymbol D\).

The distinction is exact.  Choose one point \(z_k\) in each of \(M\)
distinct moving annular tubes and define the abstract measure

\[
 \boxed{
 \boldsymbol D_M:=\sum_{k=1}^Ma_k\delta_{z_k},\qquad a_k>0.}
\tag{S.301}
\]

Its support is finite and therefore has zero parabolic
\(\mathcal H^1\)-measure, while its weighted mass can be made nonzero in
every one of the \(M\) shells; choosing \(a_k\) proportional to
\(R/\gamma_k\) makes those weighted masses comparable.  This is a measure
countermodel to an invalid implication from dimension to packing.  It is
not asserted to be the defect of an NSE solution.

The high-Rayleigh ancestor is even farther from a singular-set count.  It is
part of \(|\nabla u|^2dxdt\), may be supported entirely in the regular set,
and can be large for smooth high-frequency fields.  Step 7's exact heat
shear has arbitrarily large cutoff Rayleigh ratio while its completed clocks
are paid by \(Q\).  Thus

\[
 \boxed{
 \text{large high-Rayleigh mass}\ \not\Longrightarrow\
 \text{a singular point detected by epsilon regularity}.}
\tag{S.302}
\]

The converse form of epsilon regularity says that a singular point cannot
have all relevant critical quantities small.  It does not turn every large
regular viscous mass into a singular point.  Likewise, estimates giving
finitely many terminal singular points under a Type-I bound have a count
depending on that extra norm and do not control the full-history annular
vector \(h\).

The exact layer-cake formula (S.278) applies to
\(d^{\rm def},h,b\) as well.  Even a
valid one-threshold singular-cylinder count would have to be upgraded to an
integrable all-threshold mass distribution before it could imply (S.288).

## 10. Bounded primary-source collision audit

A bounded search was made for an existing theorem with the quantifiers of
(S.280) or (S.288).  No direct match was found.

| Primary result | Established scope | Boundary for the present gate |
|---|---|---|
| Caffarelli--Kohn--Nirenberg, [*Partial regularity of suitable weak solutions*](https://doi.org/10.1002/cpa.3160350604) | Parabolic size of the singular set and epsilon regularity | It gives neither defect-mass upper density nor a fixed count for regular high-Rayleigh annuli. |
| De Rosa--Drivas--Inversi, [*On the Support of Anomalous Dissipation Measures*](https://arxiv.org/abs/2301.09603) | Dissipation-support/density conclusions under stated \(L_t^qL_x^r\) assumptions | The useful density estimates use extra integrability and a solution-dependent modulus outside the needed uniform regime. |
| Seregin, [*Estimates ... in critical Morrey spaces*](https://arxiv.org/abs/math/0607534) and [*Regularity ... in critical Morrey spaces*](https://arxiv.org/abs/math/0607537) | Estimates or regularity under bounded scale-invariant functionals | The bounded critical coefficient is an assumption, matching the conditional nature of Section 7 rather than proving it from the bare ledger. |
| Barker, [*Higher integrability and the number of singular points ...*](https://arxiv.org/abs/2111.14776) | Under a scale-invariant weak-\(L^3\) bound \(M\), at most \(O(M^{20})\) terminal singular points, plus higher gradient integrability | The count depends on \(M\), concerns singular points, and is not a best-\(N\) estimate for full-history viscous mass. |
| Neustupa, [*A note on local interior regularity ...*](https://doi.org/10.3934/dcdss.2013.6.1391) | A singular point forces persistent physical-ball \(L^3\) concentration in a left time neighborhood | It starts from a singular point and does not estimate arbitrary completed shell clocks about the prescribed moving centre. |

The search is evidence against an immediate literature shortcut, not a
novelty or priority proof.  The exact papers concern different observables
or require additional norm bounds.

## 11. Route decision

Step 12 changes the next proof obligations without claiming to close them.

1. For the short branch, attack the continuous common-window gate (S.280),
   preferably through the all-threshold count (S.279).  A scalar temporal
   \(L^1\) estimate, terminal averaging, or a critical one-threshold count
   has now been ruled out as sufficient.
2. For the excess branch, attack the shared ancestor charging lemma (S.287)
   or prove a uniform moving-tube coefficient strong enough for (S.294).
   Defect and high-Rayleigh budgets must be recombined with the exact budget
   sum (S.286).
3. Any exact-family falsification attempt must produce \(N+1\) large
   residual coordinates after all nonnegative cubic and local-energy rows
   are included.  Simultaneous persistent lobes already fail this test; the
   single moving-packet speed-up is screened separately below.

The combined Step 12 target is

\[
 \boxed{
 \begin{gathered}
 \textbf{OPEN: find fixed }N_F,N_b\textbf{ and constants such that}\\
 \sup_{\tau\in\mathcal T_R}
       \mathcal V^F_{N_F,R}(\tau,\delta_*)\lesssim A_R,
 \qquad
 \sup_{\tau\in\mathcal G_R\cap\mathcal T_R}
       \mathcal S_{N_b}(b(\tau))\lesssim A_R.\\
 \text{Then Step 11 closes with }
 N_{\rm sh}=N_F,\ N_x=N_b,
 \text{ and total budget }N_F+N_b.
 \end{gathered}}
\tag{S.303}
\]

Both antecedents are open in the bare suitable-weak class.  The second is
proved only under the additional uniform hypotheses of Section 7 or 8.

## 12. A single-packet speed-up is kinematically screened

The inherited R0.74F packet centre is

\[
 Q(t)=q_{\rm pre}+B\int_0^t\theta(s,h)\,ds,
 \qquad |\theta|\le1,
 \qquad 0<B\le{1\over32R^2}.
\]

Therefore its total variation, not merely its endpoint displacement,
satisfies

\[
 \boxed{
 \operatorname {Var}_{[0,65R^2]}Q\le{65\over32}<2\pi,
 \qquad
 \operatorname {Var}_{I_{2R}}Q\le{1\over8}.}
\tag{S.304}
\]

Thus the frozen exact family makes no physical winding of the packet centre
around the torus.  The ``all-winding'' estimates in R0.74F concern periodic
copies in a Brownian-bridge heat kernel; they are not packet-centre orbits.

There is also an exact abstract occupation bound.  Let
\(q\in AC([0,T])\) satisfy

\[
 0<\beta B\le q'(t)\le B\quad\text{for a.e. }t,
\]

and let \(J\subset\mathbb R/(2\pi\mathbb Z)\) be measurable.  Put

\[
 D=q(T)-q(0),\qquad m=\left\lfloor{D\over2\pi}\right\rfloor,
 \qquad
 \tau_J=\bigl|\{t\in[0,T]:q(t)\bmod2\pi\in J\}\bigr|.
\]

Changing variables from \(t\) to \(s=q(t)\), every complete interval of
length \(2\pi\) contributes exactly \(|J|\) to the \(s\)-occupation,
while the remaining interval contributes between zero and \(|J|\).  Hence

\[
 \boxed{
 {m|J|\over B}\le\tau_J
 \le{(m+1)|J|\over\beta B}.}
\tag{S.305}
\]

In a one-pass crossing of the entire set \(J\), the sharper bounds are
\(|J|/B\le\tau_J\le|J|/(\beta B)\).  In a many-winding regime,
\(m\asymp BT\), so the factors \(B\) and \(B^{-1}\) cancel: increasing
the speed increases the number of visits but decreases each residence time.
It does not create an exponential preference for outer dyadic shells.

That statement combines with a purely discrete filter.  Let
\(0<\Gamma<1\), \(H\ge0\), \(p\ge0\), and suppose a nonnegative sequence
indexed by \(\ell\ge0\) obeys

\[
 z_\ell\le H2^{p\ell}\Gamma^{4^\ell}.
\]

For every integer \(N\ge0\) such that
\(q_N:=2^p\Gamma^{3\cdot4^N}<1\), deletion of the first \(N\)
coordinates and the adjacent-ratio estimate give

\[
 \boxed{
 \mathcal S_N(z)
 \le\sum_{\ell\ge N}z_\ell
 \le {H2^{pN}\Gamma^{4^N}\over1-q_N}.}
\tag{S.306}
\]

Indeed, the ratio of consecutive majorants is
\(2^p\Gamma^{3\cdot4^\ell}\le q_N\) for \(\ell\ge N\).
For the inherited weights
\(L_\ell=2^\ell L\) and
\(\Gamma_\ell=e^{-c_\gamma L_\ell^2}=\Gamma^{4^\ell}\), any
single-packet row with only a fixed polynomial shell prefactor falls under
(S.306).  Formula (S.305) shows that uniform speed-up changes a common
prefactor, not the super-Gaussian shell ratio.

This is deliberately a conditional mechanism screen.  It does not prove
that every full clock coordinate has the displayed majorant.  If a lobe
persists inside the common terminal window, R0.74R already pays it through
the exterior cubic row.  If a packet crosses earlier and leaves only
viscous or anomalous dissipation behind, the frozen theory has no lower
identification of that deposited tube mass with the full ancestor vector
\(b\).  Consequently (S.304)--(S.306) rule out speed alone as the missing
ingredient, but do not prove (S.288).  A genuinely different candidate must
break at least one of common amplitude, \(R\)-scale spatial structure, or
near-uniform rigid translation—for example through dynamically generated
sub-\(R\) frequency or shell-dependent amplification.  Whether NSE permits
such a candidate while keeping the complete payment small remains open.

## 13. Claim ledger

The following are **PROVED** in the stated frozen setting:

- the terminal variation-window inequalities (S.274)--(S.275);
- continuity of the common-window best-\(N\) functional and the fixed-
  solution modulus (S.276)--(S.277);
- the best-\(N\) layer-cake identity and its all-threshold consequence
  (S.278)--(S.279);
- the synchronized-spike no-go for an \(L_t^1\)-only derivation and the
  averaged \(P^{4/5}\) boundary (S.281)--(S.284);
- honest exception-budget recombination and the conditional charging
  implication (S.285)--(S.287);
- the moving-tube cover and conditional critical-Morrey theorem
  (S.289)--(S.294);
- the mixed-norm sufficient benchmark (S.295)--(S.300);
- the literal no-winding estimate and monotone occupation lemma
  (S.304)--(S.305); and
- the abstract super-Gaussian best-\(N\) filter (S.306).

The following are **ABSTRACT BOUNDARY TESTS, NOT NSE COUNTEREXAMPLES**:

- the synchronized vector-valued temporal spikes (S.281); and
- the finite atomic defect-support model (S.301).

The following remain **OPEN**:

- the universal terminal-window gate (S.280);
- the universal ancestor gate (S.288);
- the combined Step 12 target (S.303), Step 11 (S.272), Q.12, and Q.1;
- any uniform critical Morrey/path estimate derived from the frozen payment
  alone;
- identification of an earlier moving-packet deposit with the complete
  ancestor vector \(b\);
- a fixed universal effective-shell count for arbitrary suitable weak
  solutions; and
- scale contraction, regularity, singularity formation, and the
  Navier--Stokes Millennium problem.

The advance is an exact terminal-window normal form, a continuous target for
the short trace, and a proved conditional Morrey packing theorem for both
excess ancestors.  **NOT CLAY.**
