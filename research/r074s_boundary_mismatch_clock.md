# R0.74S Step 4 — the two-collar mismatch is a thinner completed boundary clock

## 0. Result and scope

R0.74S Step 3 leaves a two-sided mismatch
\(\gamma_m(J_{m,R}^--J_{m,R}^+)\) at every internal active boundary.
This note identifies it exactly as the flux of a nonnegative thin
boundary bump.  That bump has its own defect-completed local-energy clock,
is pointwise dominated by the original padded shell cutoff, and has support
volume \(O(2^{2m}R^3)\) rather than \(O(2^{3m}R^3)\).

Three consequences follow.

1. Every stopped mismatch sum is bounded above by terminal boundary clocks
   plus the already-controlled quadratic \(Q\) ledger.
2. Exceptional boundary clocks are controlled by the original matched
   square function.
3. The boundary persistence coefficient cubes to
   \(2^{2m}\gamma_m(\Theta_m^\partial)^{-2}\), improving the shell-volume
   factor \(2^{3m}\) from R0.74R.

The clock-to-endpoint extraction and temporal persistence hypotheses remain
**OPEN**.  The result controls only the mismatch channel, not the root,
outer, or weight-drop channels from R0.74S Step 3.  **NOT CLAY.**

All notation and scope are inherited from R0.74S Steps 1--3.  In
particular,
\[
 A_R:=(P_R^M)^{2/3},
\]
and \(\vartheta\) is the frozen smooth nondecreasing cutoff with values in
\([0,1]\), equal to zero on \((-\infty,-1]\) and to one on
\([0,\infty)\).

## 1. Boundary bump and geometry

Retain

\[
 r_m=2^mR,\qquad \delta=\frac R8,
\]

and define

\[
 \beta_m^R(y)
 :=\vartheta\!\left(\frac{|y|-r_m}{\delta}\right)
   \vartheta\!\left(\frac{r_m-|y|}{\delta}\right).
\tag{S.60}
\]

The bump is supported on the two collars adjacent to the hard sphere
\(|y|=r_m\).  Since \(r_m-\delta>0\), it vanishes in a neighbourhood
of the origin, so the radial definition is smooth there as well.  On the
support of the derivative of either factor, the other factor is exactly
one.  Hence, for \(y\ne0\),

\[
 \boxed{
 \nabla\beta_m^R(y)
 =\delta^{-1}\left[
  \vartheta'\!\left(\frac{|y|-r_m}{\delta}\right)
  -\vartheta'\!\left(\frac{r_m-|y|}{\delta}\right)
 \right]\widehat y.}
\tag{S.61}
\]

The right side of (S.61) is defined to be zero at \(y=0\), consistently
with the fact that \(\beta_m^R\) vanishes near the origin.

For every \(m\ge1\),

\[
 0\le\beta_m^R\le\psi_m^R,
 \qquad
 \operatorname {supp}\beta_m^R
 \subset\{r_m-\delta\le |y|\le r_m+\delta\}
 =\overline {C_m^-}\cup\{|y|=r_m\}\cup\overline {C_m^+}.
\tag{S.62}
\]

Moreover,

\[
\begin{aligned}
 |\operatorname {supp}\beta_m^R|
 &\le C_\beta2^{2m}R^3,\\
 |\nabla\beta_m^R|
 &\le C_\beta R^{-1},\\
 |\Delta\beta_m^R|
 &\le C_\beta R^{-2}.
\end{aligned}
\tag{S.63}
\]

Indeed, the volume of the containing closed annulus is

\[
 \frac{4\pi}{3}\bigl[(r_m+\delta)^3-(r_m-\delta)^3\bigr]
 =8\pi r_m^2\delta+\frac{8\pi}{3}\delta^3,
\]

which proves the exponent two because \(\delta=R/8\) and
\(r_m=2^mR\).  The radial Laplacian formula, together with
\(r_m-\delta\ge15R/8\), proves the last two bounds in (S.63), with a
constant depending only on the frozen cutoff.  Let

\[
 B_m^R(x)
 :=\sum_{n\in\mathbb Z^3}\beta_m^R(\widetilde x+2\pi n),
 \qquad 0\le B_m^R\le\Psi_m^R,
\tag{S.64}
\]

be the periodization.  The sum is locally finite for each fixed \(m\), and
the inequality follows term by term from (S.62); it does not require the
periodic copies to be disjoint.

## 2. Defect-completed boundary clock

At local-energy good times define

\[
\begin{aligned}
 E_{m,R}^{\partial}(t)
 &:=
 \frac{\gamma_m\eta_R(t)}{2R}
 \int_{\mathbb T^3}B_m^R(y)|v_R(t,y)|^2\,dy,\\
 D_{m,R}^{\partial}(t)
 &:=
 \frac{\gamma_m}{R}
 \int_{(s_R,t)\times\mathbb T^3}
 \eta_R(r)B_m^R(x-X_R(r))\,d\boldsymbol\mu(r,x).
\end{aligned}
\tag{S.65}
\]

Define the cumulative quadratic and flux rows

\[
\begin{aligned}
 Q_{m,R}^{\partial}(t)
 &:=
 \frac{\gamma_m}{2R}
 \int_{s_R}^{t}\!\int_{\mathbb T^3}
 [\eta_R'(r)B_m^R(y)+\eta_R(r)\Delta B_m^R(y)]
 |v_R(r,y)|^2\,dy\,dr,\\
 F_{m,R}^{\partial}(t)
 &:=
 \frac{\gamma_m}{R}
 \int_{s_R}^{t}\!\int_{\mathbb T^3}
 \eta_R(r)\mathcal W_R^M(r,y)\cdot\nabla B_m^R(y)\,dy\,dr.
\end{aligned}
\tag{S.66}
\]

Testing the suitable local-energy inequality with
\(\eta_R(r)B_m^R(x-X_R(r))\), and then using the total local-dissipation
measure exactly as in R0.74P, gives the canonical clock

\[
 \boxed{
 K_{m,R}^{\partial}
 :=Q_{m,R}^{\partial}+F_{m,R}^{\partial}
 =E_{m,R}^{\partial}+D_{m,R}^{\partial}\ge0,
 \qquad K_{m,R}^{\partial}(s_R)=0.}
\tag{S.67}
\]

The time-dependent pressure gauge in \(\mathcal W_R^M\) drops out by
periodicity and incompressibility.  The \(E+D\) formula is read at good
times; \(Q+F\) selects the canonical absolutely continuous representative
at every time.  Nonnegativity first holds on the full-measure set of good
times and then at every time by continuity.  From (S.64) and positivity of
the total dissipation measure,

\[
 \boxed{
 0\le K_{m,R}^{\partial}(t)\le K_{m,R}(t)
 \le v_{m,R}}
\tag{S.68}
\]

at every good time.

## 3. Boundary quadratic and cubic ledgers

For clarity, periodize a nonnegative derivative majorant before taking
absolute values.  Equations (S.62)--(S.63) give
\(|\Delta B_m^R|\le CR^{-2}\sum_n
\mathbf 1_{\operatorname {supp}\beta_m^R}(\widetilde y+2\pi n)\),
whereas \(B_m^R\le\Psi_m^R\).  Unfolding these nonnegative majorants and
then applying the R0.74H doubled-radius support ledger gives

\[
 \boxed{
 \sum_{m\ge1}\operatorname {TV}Q_{m,R}^{\partial}
 \le C(P_R^M)^{2/3}=CA_R.}
\tag{S.69}
\]

For measurable \(J\subset(s_R,t_0)\), put

\[
 p_{m,R}^{\partial}(J)
 :=R^{-2}\gamma_m
 \int_J\eta_R(t)^{3/2}
 \int_{\operatorname {supp}\beta_m^R}
 |\widetilde v_R(t,y)|^3\,dy\,dt.
\tag{S.70}
\]

Since \(\operatorname {supp}\beta_m^R\subset
\operatorname {supp}\psi_m^R\), arbitrary shell-dependent sets satisfy

\[
 \boxed{
 \sum_{m\ge1}p_{m,R}^{\partial}(J_m)
 \le CP_R^M.}
\tag{S.71}
\]

## 4. The stopped mismatch becomes terminal boundary clocks

For a stopped family \((\tau,I,\boldsymbol\sigma)\) from R0.74S Step 2,
let

\[
 I^\partial
 :=\{m\ge2:m-1\in I,\ m\in I\},
 \qquad
 \widehat\sigma_m:=\max(\sigma_{m-1},\sigma_m).
\tag{S.72}
\]

The internal mismatch channel of Step 3 is active precisely for
\(t\in(\widehat\sigma_m,\tau]\).  Equations (S.45), (S.61), and (S.66)
therefore give

\[
 \boxed{
 \frac1R\int_{s_R}^{\tau}\eta_R(t)\mathcal M_R(t)\,dt
 =\sum_{m\in I^\partial}
 [F_{m,R}^{\partial}(\tau)
  -F_{m,R}^{\partial}(\widehat\sigma_m)].}
\tag{S.73}
\]

Indeed, away from the finitely many stopping times,
\(\mathbf 1_{(\widehat\sigma_m,\tau]}
=\mathbf 1_{(\sigma_{m-1},\tau]}
 \mathbf 1_{(\sigma_m,\tau]}\).  Thus the left side unfolds to the
time integral of \(\gamma_m(J_{m,R}^--J_{m,R}^+)\) over exactly the same
active interval as the right side.

Because \(\widehat\sigma_m\) is one of two good stopping times, it is good.
Use \(F^\partial=K^\partial-Q^\partial\), nonnegativity of
\(K^\partial\), and (S.69) to obtain

\[
 \boxed{
 \left[
 \frac1R\int_{s_R}^{\tau}\eta_R\mathcal M_R
 \right]_+
 \le
 \sum_{m\in I^\partial}K_{m,R}^{\partial}(\tau)
 +CA_R.}
\tag{S.74}
\]

More explicitly, the right side of (S.73) is at most

\[
 \sum_{m\in I^\partial}K_{m,R}^\partial(\tau)
 +\sum_{m\in I^\partial}
   |Q_{m,R}^\partial(\tau)-Q_{m,R}^\partial(\widehat\sigma_m)|,
\]

because every stopped clock value is nonnegative.  This proves (S.74)
after taking the positive part and using total variation.

Thus all shell-dependent stopping times disappear from the upper bound for
the mismatch channel.

## 5. Thinner persistence coefficient

At almost every \(t\in(s_R,t_0)\), write

\[
 e_{m,R}^{\partial,\eta}(t)
 :=\frac{\gamma_m\eta_R(t)}{2R}
   \int_{\mathbb R^3}\beta_m^R(y)
   |\widetilde v_R(t,y)|^2\,dy
 =E_{m,R}^{\partial}(t).
\tag{S.75}
\]

For a good terminal time \(\tau\) and measurable
\(J\subset(s_R,\tau)\) of positive measure, define

\[
 \Theta_{m,R}^{\partial}(\tau;J)
 :=
 \frac{R^{-2}\int_J
       e_{m,R}^{\partial,\eta}(t)^{3/2}\,dt}
      {e_{m,R}^{\partial,\eta}(\tau)^{3/2}}.
\tag{S.76}
\]

Use the same zero and infinity labels as R0.74R, but make the resulting
extended-real arithmetic explicit.  If the terminal energy is zero, set
\(\Theta^\partial=+\infty\) and read (S.77) as \(0\le0\).  If the terminal
energy is positive but the numerator in (S.76) vanishes, set
\(\Theta^\partial=0\) and read the entire right side of (S.77) as
\(+\infty\); the estimate is then deliberately vacuous.  In every other
case ordinary arithmetic applies.  Spatial Hölder,
\(0\le\beta_m^R\le1\), and the \(2^{2m}R^3\) support volume give

\[
 \boxed{
 e_{m,R}^{\partial,\eta}(\tau)
 \le
 C_\partial2^{2m/3}\gamma_m^{1/3}
 [\Theta_{m,R}^{\partial}(\tau;J)]^{-2/3}
 p_{m,R}^{\partial}(J)^{2/3}.}
\tag{S.77}
\]

Indeed, before time integration,

\[
\begin{aligned}
 e_{m,R}^{\partial,\eta}(t)^{3/2}
 \le C2^mR^2\gamma_m^{1/2}
 \left[
 R^{-2}\gamma_m\eta_R(t)^{3/2}
 \int_{\operatorname {supp}\beta_m^R}
 |\widetilde v_R(t)|^3
 \right].
\end{aligned}
\tag{S.78}
\]

For the shellwise step, define the composite coefficient

\[
 \mathcal A_{m,R}^{\partial}(\tau;J,\Lambda)
 :=
 \begin{cases}
  0,&\Lambda=0,\\
  2^{2m}\gamma_m\Lambda^3
   [\Theta_{m,R}^{\partial}(\tau;J)]^{-2},
    &\Lambda>0,\quad\Theta_{m,R}^{\partial}(\tau;J)>0,\\
  +\infty,&\Lambda>0,\quad\Theta_{m,R}^{\partial}(\tau;J)=0.
 \end{cases}
\]

Here \((+\infty)^{-2}=0\) in the middle row.  Thus the definition never
forms either \(+\infty\cdot0\) or \(0\cdot+\infty\).  Consequently, for
nonnegative \(\Lambda_m\),

\[
\begin{aligned}
 \sum_{m\in H}\Lambda_me_{m,R}^{\partial,\eta}(\tau)
 \le{}&C
 \left[
  \sum_{m\in H}
  \mathcal A_{m,R}^{\partial}(\tau;J_m,\Lambda_m)
 \right]^{1/3}\\
 &\times
 \left[
  \sum_{m\in H}p_{m,R}^{\partial}(J_m)
 \right]^{2/3}.
\end{aligned}
\tag{S.79}
\]

Equation (S.79) is Hölder across shells with conjugate exponents \(3\) and
\(3/2\).  If the sum of the \(\mathcal A_{m,R}^{\partial}\) coefficients
is \(+\infty\), the entire right side of (S.79) is defined to be
\(+\infty\), independently of the payment factor, so the estimate is
vacuous rather than an undefined \(+\infty\cdot0\).  Otherwise ordinary
arithmetic applies.  In every nondegenerate row, its cubed coefficient is
exactly
\(2^{2m}\gamma_m\Lambda_m^3
[\Theta_{m,R}^{\partial}(\tau;J_m)]^{-2}\).

The cubed geometric coefficient is \(2^{2m}\gamma_m\), not
\(2^{3m}\gamma_m\).

## 6. Conditional mismatch-packing theorem

### Theorem 6.1

Assume there are universal \(N_\partial,C_q,C_*<\infty\) such that, for
every good \(\tau\) and every finite \(H\subset\mathbb N\), one can choose
\(S_{\tau,H}\subset H\), \(\#S_{\tau,H}\le N_\partial\), nonnegative
\(q_m,\Lambda_m\), and positive-measure measurable
\(J_m\subset(s_R,\tau)\) satisfying

\[
\begin{aligned}
 \sum_{m\in H\setminus S_{\tau,H}}q_m
 &\le C_qA_R,\\
 K_{m,R}^{\partial}(\tau)
 &\le q_m+\Lambda_me_{m,R}^{\partial,\eta}(\tau)
 \quad(m\in H\setminus S_{\tau,H}),
\end{aligned}
\tag{S.80}
\]

and

\[
 \boxed{
 \sum_{m\in H\setminus S_{\tau,H}}
 \mathcal A_{m,R}^{\partial}(\tau;J_m,\Lambda_m)
 \le C_*.}
\tag{S.81}
\]

Then every stopped mismatch channel with good terminal time obeys

\[
 \boxed{
 \left[
 \frac1R\int_{s_R}^{\tau}\eta_R\mathcal M_R
 \right]_+
 \le C A_R+\sqrt{N_\partial}\,Y_{2,R}^{\rm sf}.}
\tag{S.82}
\]

**Proof.**  Apply (S.79), (S.71), and (S.80)--(S.81) outside the
exceptional set to get

\[
 \sum_{m\in H\setminus S_{\tau,H}}
 K_{m,R}^{\partial}(\tau)\le CA_R.
\tag{S.83}
\]

On the exceptional set, (S.68) and Cauchy--Schwarz give

\[
 \sum_{m\in S_{\tau,H}}K_{m,R}^{\partial}(\tau)
 \le\sum_{m\in S_{\tau,H}}v_{m,R}
 \le\sqrt{N_\partial}\,Y_{2,R}^{\rm sf}.
\tag{S.84}
\]

Take \(H=I^\partial\) in (S.74).  \(\square\)

## 7. Value and exact open boundary

The result is a genuine geometric improvement: completing the two-collar
mismatch by a boundary bump lowers the spatial-volume exponent in the
persistence cube from three to two.  It also recycles the original matched
square function for finitely many boundary-clock exceptions through
\(K_m^\partial\le K_m\le v_m\).

It does not prove the hypotheses of Theorem 6.1.  In particular,
nonnegativity of the boundary clock still permits terminal mass to be
dominated by accumulated dissipation, and an endpoint boundary energy can
still occupy a time set with arbitrarily small thickness.

The mismatch channel is only one of four Step-3 channels.  Root supply,
outer leakage/backscatter, and the weight-drop row remain uncontrolled at
the quadratic scale.  The unconditional stopped-work estimate, (Q.1),
scale contraction, prescribed-centre scale packing, regularity, singularity
formation, and the Clay problem remain **OPEN / NOT CLAIMED**.
**NOT CLAY.**

## 8. Inherited source ledger

| Use | Frozen source | Status |
|---|---|---|
| Boundary collar geometry and traces | R0.74S Step 3, (S.39)--(S.46) | **INHERITED / PROVED** |
| Mismatch channel and stopped activation | R0.74S Step 3, (S.50)--(S.52) | **INHERITED / PROVED** |
| Suitable-weak completed-clock construction | R0.74P, (2.6)--(2.10) | **INHERITED / PROVED** |
| Quadratic and cubic support ledgers | R0.74H (4.1)--(4.8); R0.74P (3.4)--(3.6) | **INHERITED / PROVED** |
| Matched square function | R0.74P (3.13) | **INHERITED / PROVED DEFINITION** |

No novelty or priority claim is made.
