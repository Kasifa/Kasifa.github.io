# R0.74S Step 5 — one-sided ball completion exposes the remaining \(\ell^1\) debt

## 0. Result and scope

R0.74S Step 4 completes the two-collar mismatch by a thin nonnegative
boundary clock.  Three signed channels remain: block-root supply, block-
outer leakage/backscatter, and the internal weight-drop row.

This note completes each one-sided collar by a compact ball cutoff and
proves three facts.

1. Root, outer, and weight-drop work have exact stopped ball-clock
   representations with different time orientations.
2. Every quadratic ball-cutoff row is still paid by
   \(A_R=(P_R^M)^{2/3}\).
3. The terminal weight-drop ball clocks satisfy an exact Abel identity:
   they equal one core ball clock plus the full \(\ell^1\) sum of
   shell-clock residuals.  A smooth abstract clock tower saturates this
   identity at size \(N\) while the matched square function is only
   \(\sqrt N\).

Thus completed-clock positivity and cutoff linearity do not, by themselves,
prove square-function compression.  The result is a rigorous algebraic
route rejection and a sharper interface for the missing dynamical sign
theorem.  It is not a counterexample built from a Navier--Stokes solution.
The unconditional stopped-work estimate, regularity, and the Clay problem
remain **OPEN / NOT CLAIMED**.  **NOT CLAY.**

All notation, good-time conventions, and the Version-M suitable-weak scope
are inherited from R0.74P and R0.74S Steps 2--4.

## 1. Two compact one-sided ball cutoffs

Retain \(r_m=2^mR\), \(\delta=R/8\), and the frozen cutoff
\(\vartheta\).  Define

\[
\begin{aligned}
 \chi_{m,R}^-(y)
 &:=1-\vartheta\!\left(\frac{|y|-r_m}{\delta}\right),\\
 \chi_{m,R}^+(y)
 &:=\vartheta\!\left(\frac{r_m-|y|}{\delta}\right).
\end{aligned}
\tag{S.85}
\]

The minus superscript means that the transition lies in the inner collar
\(C_m^-\); the plus superscript means that it lies in the outer collar
\(C_m^+\).  Both functions are smooth, compactly supported, radial, and
take values in \([0,1]\).  For \(y\ne0\),

\[
\begin{aligned}
 \nabla\chi_{m,R}^-
 &=-\delta^{-1}
   \vartheta'\!\left(\frac{|y|-r_m}{\delta}\right)\widehat y,\\
 \nabla\chi_{m,R}^+
 &=-\delta^{-1}
   \vartheta'\!\left(\frac{r_m-|y|}{\delta}\right)\widehat y.
\end{aligned}
\tag{S.86}
\]

The right sides are set to zero at the origin.  Direct inspection in the
four radial regions separated by \(r_m-\delta,r_m,r_m+\delta\) gives

\[
\boxed{
 0\le\chi_{m,R}^-\le\chi_{m,R}^+\le1,\qquad
 \beta_m^R=\chi_{m,R}^+-\chi_{m,R}^-,
 \qquad
 \psi_m^R=\chi_{m+1,R}^+-\chi_{m,R}^-.}
\tag{S.87}
\]

Let \(\mathsf B_{m,R}^{\pm}\) denote the periodizations of
\(\chi_{m,R}^{\pm}\).  Unfolding the two gradients against the periodic
work vector from Step 3 gives

\[
\boxed{
 \int_{\mathbb T^3}\mathcal W_R^M\cdot
 \nabla\mathsf B_{m,R}^-=-J_{m,R}^-,
 \qquad
 \int_{\mathbb T^3}\mathcal W_R^M\cdot
 \nabla\mathsf B_{m,R}^+=-J_{m,R}^+.}
\tag{S.88}
\]

## 2. The completed ball-clock operator

For any smooth compact lifted cutoff \(\phi\ge0\), let \(\Phi\) be its
periodization and define the unweighted linear rows

\[
\begin{aligned}
 \mathscr E_R[\Phi](t)
 &:=
 \frac{\eta_R(t)}{2R}
 \int_{\mathbb T^3}\Phi(y)|v_R(t,y)|^2\,dy,\\
 \mathscr D_R[\Phi](t)
 &:=
 \frac1R
 \int_{(s_R,t)\times\mathbb T^3}
 \eta_R(r)\Phi(x-X_R(r))\,d\boldsymbol\mu(r,x),\\
 \mathscr Q_R[\Phi](t)
 &:=
 \frac1{2R}
 \int_{s_R}^{t}\!\int_{\mathbb T^3}
 [\eta_R'(r)\Phi+\eta_R(r)\Delta\Phi]|v_R|^2\,dy\,dr,\\
 \mathscr F_R[\Phi](t)
 &:=
 \frac1R
 \int_{s_R}^{t}\!\int_{\mathbb T^3}
 \eta_R(r)\mathcal W_R^M\cdot\nabla\Phi\,dy\,dr.
\end{aligned}
\tag{S.89}
\]

All undisplayed arguments in the last two rows are \((r,y)\).  Set

\[
 \mathscr K_R[\Phi]
 :=\mathscr Q_R[\Phi]+\mathscr F_R[\Phi].
\]

The R0.74P local-energy calculation gives, at good times and then through
the canonical absolutely continuous representative,

\[
\boxed{
 \mathscr K_R[\Phi]
 =\mathscr E_R[\Phi]+\mathscr D_R[\Phi]\ge0,
 \qquad
 \mathscr K_R[\Phi](s_R)=0.}
\tag{S.90}
\]

Write
\(\mathscr K_{m,R}^{\pm}:=
\mathscr K_R[\mathsf B_{m,R}^{\pm}]\), and similarly for
\(\mathscr Q,\mathscr F,\mathscr E,\mathscr D\).

Linearity of all five rows and (S.87) yield

\[
\boxed{
\begin{aligned}
 \mathscr K_{m,R}^{+}-\mathscr K_{m,R}^{-}
 &=\gamma_m^{-1}K_{m,R}^{\partial},\\
 \mathscr K_{m+1,R}^{+}-\mathscr K_{m,R}^{-}
 &=\gamma_m^{-1}K_{m,R}.
\end{aligned}}
\tag{S.91}
\]

The same identities hold separately for
\(\mathscr Q,\mathscr F\) at every time and for
\(\mathscr E,\mathscr D\) at good times.  Subtracting the first line from
the second gives the monotone ball tower

\[
\boxed{
 \mathscr K_{m+1,R}^{+}-\mathscr K_{m,R}^{+}
 =\gamma_m^{-1}
  (K_{m,R}-K_{m,R}^{\partial})\ge0.}
\tag{S.92}
\]

The inequality first follows at good times from Step 4 and then at every
time by continuity.

## 3. All ball quadratic rows remain quadratic

Put

\[
 d_m:=\gamma_{m-1}-\gamma_m>0,\qquad m\ge2.
\]

The frozen adjacent ratio gives
\(\sum_{k\ge j}\gamma_k\le(35/3)\gamma_j\), and
\(d_m\le\gamma_{m-1}\).  Radially splitting the lift into the central ball,
the hard-boundary collars, and the padded-shell interiors gives the
pointwise packing

\[
\begin{aligned}
 &\sum_{k\ge1}\gamma_k\chi_{k,R}^-
 +\sum_{k\ge1}\gamma_k\chi_{k+1,R}^+
 +\sum_{m\ge2}d_m\chi_{m,R}^+\\
 &\qquad\le
 C\left[
  \mathbf 1_{\{|y|<4R\}}
  +\sum_{j\ge1}\gamma_j
   \mathbf 1_{\operatorname {supp}\psi_j^R}(y)
 \right].
\end{aligned}
\tag{S.93}
\]

The same estimate holds for \(R^2\) times the sum of the corresponding
absolute Laplacians.  Near \(r_j\), the possible larger coefficient
\(\gamma_{j-1}\) is carried by
\(\operatorname {supp}\psi_{j-1}^R\); in the interior of shell \(j\), the
weight tail starts at \(\gamma_j\).  This is the only radius shift needed
in (S.93).

Periodize the nonnegative majorants and unfold.  The shell part is exactly
the R0.74H weighted \(S_2\) estimate.  The central row is paid separately:

\[
\begin{aligned}
 R^{-3}\int_{I_{2R}}\int_{B_{4R}}|v_R|^2
 &\le4R^{-1}
  \mathop{\rm ess\,sup}_{I_{8R}}\int_{B_{8R}}|v_R|^2\\
 &\le32\,\mathcal E^{M,R}(z_0,8R)
 \le32(P_R^M)^{2/3}=32A_R.
\end{aligned}
\]

Here the last inequality uses the local-energy component
\(\mathcal E^{M,R}(z_0,8R)^{3/2}\le P_R^M\).  Combining the core and shell
rows gives

\[
\boxed{
\begin{aligned}
 &\sum_{k\ge1}\gamma_k
   \operatorname {TV}\mathscr Q_{k,R}^-
 +\sum_{k\ge1}\gamma_k
   \operatorname {TV}\mathscr Q_{k+1,R}^+\\
 &\qquad
 +\sum_{m\ge2}d_m
   \operatorname {TV}\mathscr Q_{m,R}^+
 \le CA_R.
\end{aligned}}
\tag{S.94}
\]

Thus no lower-order loss is created by passing from collars to balls.

## 4. Exact time orientation of the three remaining channels

Fix a stopped family
\((\tau,I,\boldsymbol\sigma)\) from Step 2.  For \(k\in I\), define

\[
\begin{aligned}
 \rho_k&:=
 \begin{cases}
  \tau,&k=1\ \text{or}\ k-1\notin I,\\
  \sigma_{k-1},&k-1\in I,
 \end{cases}\\
 \lambda_k&:=
 \begin{cases}
  \tau,&k+1\notin I,\\
  \sigma_{k+1},&k+1\in I,
 \end{cases}\\
 I_{\rm rt}&:=\{k\in I:\sigma_k<\rho_k\},\qquad
 I_{\rm out}:=\{k\in I:\sigma_k<\lambda_k\}.
\end{aligned}
\tag{S.95}
\]

Shell \(k\) is a block root exactly on
\((\sigma_k,\rho_k]\) when \(k\in I_{\rm rt}\), and is a block outer edge
exactly on \((\sigma_k,\lambda_k]\) when
\(k\in I_{\rm out}\).  For an internal boundary, retain

\[
 I^\partial=\{m\ge2:m-1,m\in I\},
 \qquad
 \widehat\sigma_m=\max(\sigma_{m-1},\sigma_m).
\tag{S.96}
\]

Equations (S.51), (S.88), and these activation intervals give the exact
three clock formulas

\[
\boxed{
 \frac1R\int_{s_R}^{\tau}\eta_R(t)\mathcal R_R(t)\,dt
 =-\sum_{k\in I_{\rm rt}}\gamma_k
 [\mathscr F_{k,R}^-(\rho_k)
  -\mathscr F_{k,R}^-(\sigma_k)],}
\tag{S.97}
\]

\[
\boxed{
 -\frac1R\int_{s_R}^{\tau}\eta_R(t)\mathcal L_R(t)\,dt
 =\sum_{k\in I_{\rm out}}\gamma_k
 [\mathscr F_{k+1,R}^+(\lambda_k)
  -\mathscr F_{k+1,R}^+(\sigma_k)],}
\tag{S.98}
\]

and

\[
\boxed{
 \frac1R\int_{s_R}^{\tau}\eta_R(t)\mathcal G_R(t)\,dt
 =\sum_{m\in I^\partial}d_m
 [\mathscr F_{m,R}^+(\tau)
  -\mathscr F_{m,R}^+(\widehat\sigma_m)].}
\tag{S.99}
\]

All endpoints in these rows are good times.  Using
\(\mathscr F=\mathscr K-\mathscr Q\), nonnegativity of the completed ball
clocks, and (S.94) gives

\[
\boxed{
 \left[\frac1R\int_{s_R}^{\tau}
  \eta_R(t)\mathcal R_R(t)\,dt\right]_+
 \le
 \sum_{k\in I_{\rm rt}}\gamma_k
 \mathscr K_{k,R}^-(\sigma_k)+CA_R,}
\tag{S.100}
\]

\[
\boxed{
 \left[-\frac1R\int_{s_R}^{\tau}
  \eta_R(t)\mathcal L_R(t)\,dt\right]_+
 \le
 \sum_{k\in I_{\rm out}}\gamma_k
 \mathscr K_{k+1,R}^+(\lambda_k)+CA_R,}
\tag{S.101}
\]

and

\[
\boxed{
 \left[\frac1R\int_{s_R}^{\tau}
  \eta_R(t)\mathcal G_R(t)\,dt\right]_+
 \le
 \sum_{m\in I^\partial}d_m
 \mathscr K_{m,R}^+(\tau)+CA_R.}
\tag{S.102}
\]

The asymmetry is exact: the root row leaves a clock at the starting stop,
whereas the outer and weight-drop rows leave clocks at merge/terminal
times.  Positivity does not erase any of these retained clock values.

## 5. Exact Abel identity for the terminal weight-drop clocks

Let \(t\) be a good time and abbreviate
\(B_m=\mathscr K_{m,R}^+(t)\).  For every \(M\ge2\), direct summation gives

\[
\boxed{
 \sum_{m=2}^{M}d_mB_m
 =\gamma_1B_2
  +\sum_{m=2}^{M-1}\gamma_m(B_{m+1}-B_m)
  -\gamma_MB_M.}
\tag{S.103}
\]

By (S.92), the middle sum equals

\[
 \sum_{m=2}^{M-1}
  [K_{m,R}(t)-K_{m,R}^{\partial}(t)].
\tag{S.104}
\]

For fixed \(R\) and good \(t\), lattice counting and the
\(E+D\) representation give

\[
 0\le B_M\le C_{R,t}(1+2^{3M}).
\tag{S.105}
\]

Since
\(\gamma_M=\exp(-4^{M-1}/32)\), it follows that
\(\gamma_MB_M\to0\).  Taking \(M\to\infty\) in (S.103), and using the
\(m=1\) instance of (S.92), yields the exact nonnegative identity

\[
\boxed{
 \sum_{m\ge2}d_m\mathscr K_{m,R}^{+}(t)
 =
 \gamma_1\mathscr K_{1,R}^{+}(t)
 +\sum_{m\ge1}
  [K_{m,R}(t)-K_{m,R}^{\partial}(t)].}
\tag{S.106}
\]

All summands are nonnegative.  The inherited finiteness of
\(Y_{1,R}^{\rm clk}\), the comparison \(K_m^\partial\le K_m\), and
finiteness of the fixed core clock make both sides finite.

Consequently, every finite \(H\subset\{2,3,\ldots\}\) satisfies

\[
\boxed{
 \sum_{m\in H}d_m\mathscr K_{m,R}^{+}(t)
 \le
 \gamma_1\mathscr K_{1,R}^{+}(t)
 +\sum_{m\ge1}K_{m,R}(t)
 \le
 \gamma_1\mathscr K_{1,R}^{+}(t)+Y_{1,R}^{\rm clk}.}
\tag{S.107}
\]

This is a valid \(\ell^1\) bound.  It is not a matched-square-function
bound.  In particular, (S.102) and (S.107) return only

\[
 \left[\frac1R\int_{s_R}^{\tau}
 \eta_R(t)\mathcal G_R(t)\,dt\right]_+
 \le
 CA_R+\gamma_1\mathscr K_{1,R}^{+}(\tau)
 +Y_{1,R}^{\rm clk},
\]

which does not improve the already known large-payment ledger.

## 6. Saturating abstract clock tower

The loss in (S.107) cannot be repaired from the ball-tower identities and
nonnegativity alone.  Fix \(N\ge1\), choose a smooth nondecreasing
\(h:[s_R,t_0]\to[0,1]\) with \(h(s_R)=0\) and \(h(\tau)=1\), and prescribe
the abstract canonical clocks

\[
\begin{aligned}
 K_{m,R}(t)&=
 \begin{cases}
  h(t),&1\le m\le N,\\
  0,&m>N,
 \end{cases}\\
 K_{m,R}^{\partial}(t)&=0,\qquad
 \mathscr K_{1,R}^{+}(t)=0,\qquad
 \mathscr K_{m,R}^{-}(t)=\mathscr K_{m,R}^{+}(t).
\end{aligned}
\tag{S.108}
\]

Define the remaining ball tower recursively by (S.92).  Then every clock
is nonnegative, absolutely continuous, starts at zero, and
\[
 \mathscr K_{m+1,R}^{+}
 -\mathscr K_{m,R}^{+}
 =
 \begin{cases}
  \gamma_m^{-1}h,&1\le m\le N,\\
  0,&m>N.
 \end{cases}
\tag{S.109}
\]

To realize the scalar completed-clock identities literally, assign to each
abstract shell, boundary, and ball clock the rows

\[
 \mathscr E=\mathscr K,\qquad
 \mathscr D=0,\qquad
 \mathscr Q=0,\qquad
 \mathscr F=\mathscr K,
\]

and use the analogous assignment for \(K_m\) and \(K_m^\partial\).
The cutoff-operator identities are represented only at this scalar linear
level; no velocity or pressure field is asserted.

The shell positive variations are \(v_{m,R}=1\) for \(1\le m\le N\) and
zero afterward.  Hence

\[
 Y_{2,R}^{\rm sf}=\sqrt N,
 \qquad
 \sum_{m\ge2}d_m\mathscr K_{m,R}^{+}(\tau)=N.
\tag{S.110}
\]

Therefore no universal \(C\) can follow from only (S.90)--(S.92) such
that

\[
\boxed{
 \sum_{m\ge2}d_m\mathscr K_{m,R}^{+}(\tau)
 \le C\,Y_{2,R}^{\rm sf}.}
\tag{S.111}
\]

This is an abstract smooth clock witness, not a Navier--Stokes velocity,
pressure, work density, or dissipation measure.  It does not disprove a
dynamical theorem that uses the PDE beyond clock positivity and linear
cutoff identities.

## 7. Decision and next viable gate

The following are **PROVED**:

- the one-sided ball cutoff identities (S.85)--(S.88);
- the completed ball-clock tower (S.89)--(S.92);
- the quadratic ball ledger (S.93)--(S.94);
- the exact root, outer, and weight-drop time orientations
  (S.95)--(S.102);
- the terminal weight-drop Abel identity (S.103)--(S.107); and
- the abstract \(\ell^1/\ell^2\) saturation (S.108)--(S.111).

The result rejects one route: replacing every remaining signed face by the
absolute value or terminal value of a positive ball clock cannot close the
matched square-function estimate from scalar clock positivity, linearity,
and the tower identities alone.  It does not reject a PDE theorem that
couples root supply to an inactive inner shell,
outer leakage to a later merge, or weight-drop work to negative
work/backscatter before positivity is taken.

The next viable gate must retain such a cross-channel sign relation or
prove a finite-complexity theorem for the block genealogy.  Another
positive completion followed by an \(\ell^1\) sum is ruled out only as a
standalone algebraic mechanism.

Root/outer dynamical control, the dissipation-dominated branch, the
R0.74R persistence hypotheses, the unconditional fixed-scale inequality
(Q.1), scale contraction, regularity, singularity formation, and the
Millennium problem remain **OPEN / NOT CLAIMED**.  **NOT CLAY.**

## 8. Inherited source ledger

| Use | Frozen source | Status |
|---|---|---|
| Actual collar traces and four-channel split | R0.74S Step 3, (S.45)--(S.59) | **INHERITED / PROVED** |
| Stopped-family activation | R0.74S Step 2, (S.25)--(S.31) | **INHERITED / PROVED** |
| Thin boundary clock and \(K_m^\partial\le K_m\) | R0.74S Step 4, (S.60)--(S.84) | **INHERITED / PROVED** |
| Suitable-weak completed-clock operator | R0.74P, (F.9)--(F.17) | **INHERITED / PROVED** |
| Weighted \(S_2\) and doubled-radius support ledger | R0.74H, (4.1)--(4.8) | **INHERITED / PROVED** |
| Frozen adjacent-weight tail | R0.74S Step 1, (S.1)--(S.21) | **INHERITED / PROVED** |

No novelty or priority claim is made.
