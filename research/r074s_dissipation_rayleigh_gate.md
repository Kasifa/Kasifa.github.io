# R0.74S Step 7 — low-Rayleigh dissipation has parabolic kinetic mass

## 0. Result and scope

R0.74S Steps 1--6 show that linear cutoff completion, stopped Abel
summation, and unweighted block genealogy do not compress the stopped-work
ledger from its natural \(\ell^1\) scale to the matched square-function
scale.  This note returns to the other unresolved branch of the R0.74R
terminal triage: a terminal clock may be dominated by accumulated local
dissipation.

The result is positive but deliberately conditional only at the point where
new information is genuinely needed.  The total local-dissipation clock is
split into its viscous and anomalous-defect parts.  After fixing any
admissible shell profile \((\lambda_k)\), every dissipation-dominated clock
falls into one of three classes:

1. anomalous defect already carries at least one eighth of the terminal
   clock;
2. viscous dissipation on times with a large cutoff-weighted local Rayleigh
   ratio carries at least one eighth; or
3. low-Rayleigh viscous dissipation carries at least one quarter.

The third class has a parabolically normalized kinetic time mass.  Jensen's
inequality and the inherited padded-shell cubic estimate then pay the whole
class, simultaneously over all shells, by
\((P_R^M)^{2/3}\).  In particular, this part needs neither an exceptional
shell nor a signed cancellation theorem.

The remaining high-Rayleigh and anomalous-defect classes are **OPEN**.  A
large Rayleigh ratio here is only a cutoff-weighted gradient-to-energy ratio;
it is not asserted to be a sharp Fourier localization.  The theorem proves
an integrated kinetic-mass statement, not a positive lower bound for the
Lebesgue measure of a time set.  It does not prove the R0.74R arbitrary-clock
extraction hypotheses, the stopped-work depletion estimate, the
fixed-scale inequality (Q.1), regularity, or the Millennium problem.
**NOT CLAY.**

No novelty or priority claim is made.

## 1. Frozen clocks and the exact dissipation split

Work in the periodic suitable-weak Version-M chart of R0.74P, with viscosity
one.  Retain the interval \((s_R,t_0)\), whose length is \(4R^2\), the
nondecreasing cutoff \(\eta_R\), the periodized padded shell cutoffs
\(\Psi_k^R\), and

\[
 \gamma_k=\exp\!\left(-\frac{4^{k-1}}{32}\right).
\]

For almost every \(t\in(s_R,t_0)\), define the kinetic and viscous density
rows

\[
 \boxed{
 \begin{aligned}
 e_{k,R}(t)
  &:={\gamma_k\eta_R(t)\over2R}
    \int_{\mathbb T^3}\Psi_k^R(y)|v_R(t,y)|^2\,dy,\\
 g_{k,R}(t)
  &:={\gamma_k\eta_R(t)\over R}
    \int_{\mathbb T^3}\Psi_k^R(y)|\nabla v_R(t,y)|^2\,dy.
 \end{aligned}}
\tag{S.142}
\]

Fix measurable representatives of these rows, setting both to zero on their
common exceptional null set.  Thus \(e_{k,R}=E_{k,R}\) almost everywhere.
Recall the nonnegative total local-dissipation measure and its anomalous part,

\[
 \boldsymbol\mu
 =|\nabla u|^2\,dx\,dt+\boldsymbol D,
 \qquad \boldsymbol D\ge0.
\]

For a good terminal time \(\tau\in(s_R,t_0)\), put

\[
 \boxed{
 \begin{aligned}
 m_{k,R}(\tau)
  &:={\gamma_k\over R}
    \int_{(s_R,\tau)\times\mathbb T^3}
    \eta_R(t)\Psi_k^R(x-X_R(t))\,d\boldsymbol D(t,x),\\
 D_{k,R}(\tau)
  &=\int_{s_R}^{\tau}g_{k,R}(t)\,dt+m_{k,R}(\tau).
 \end{aligned}}
\tag{S.143}
\]

Both summands are nonnegative.  Equation (S.143) is the exact split of the
R0.74R clock, not an extra regularity assumption.  For smooth solutions
\(m_{k,R}=0\), but no such conclusion is used for a general suitable weak
solution.

## 2. Measurable low- and high-Rayleigh times

Fix a positive sequence \(\boldsymbol\lambda=(\lambda_k)_{k\ge1}\).  The
primary definition uses only the measurable rows in (S.142):

\[
 \boxed{
 \begin{aligned}
 L_{k,R}
 &:={\left\{t\in(s_R,\tau):
 g_{k,R}(t)\le {2\lambda_k\over R^2}e_{k,R}(t)\right\}},\\
 H_{k,R}&:=(s_R,\tau)\setminus L_{k,R}.
 \end{aligned}}
\tag{S.144}
\]

When the weighted kinetic denominator is positive and \(\eta_R(t)>0\),
membership in \(L_{k,R}\) is equivalently expressed through the
cutoff-weighted local Rayleigh ratio

\[
 \boxed{
 \begin{aligned}
 &\eta_R(t)>0,\quad
 \int_{\mathbb T^3}\Psi_k^R|v_R|^2>0:
 \qquad
 \rho_{k,R}(t)
 :=R^2\,
 {\displaystyle\int_{\mathbb T^3}\Psi_k^R|\nabla v_R|^2
  \over
  \displaystyle\int_{\mathbb T^3}\Psi_k^R|v_R|^2},\\
 &\hspace{44mm}
 t\in L_{k,R}\quad\Longleftrightarrow\quad
 \rho_{k,R}(t)\le\lambda_k.
 \end{aligned}}
\tag{S.145}
\]

These sets may depend on \(k,R,\tau\), and the solution.  This causes no
problem: the inherited nonnegative shell payment permits a different
measurable time set for every shell.

If the weighted kinetic denominator vanishes, then \(v_R=0\) almost
everywhere on the open set where \(\Psi_k^R>0\), and its weak gradient also
vanishes there.  Hence \(e_{k,R}=g_{k,R}=0\), and the time belongs to
\(L_{k,R}\) directly from (S.144).  No zero-over-zero convention is needed.
The defining low-Rayleigh inequality is

\[
 \boxed{
 1_{L_{k,R}}(t)g_{k,R}(t)
 \le {2\lambda_k\over R^2}
       1_{L_{k,R}}(t)e_{k,R}(t).}
\tag{S.146}
\]

## 3. The one-eighth/one-eighth/one-quarter trichotomy

Fix a good terminal time \(\tau\), and set
\(T_k:=K_{k,R}(\tau)\).  Consider a shell in the dissipation branch of
(S.23):

\[
 T_k>0,
 \qquad D_{k,R}(\tau)\ge\frac12T_k.
\]

Write
\[
 \mathcal I_D(\tau)
 :=\left\{k:T_k>0,\ D_{k,R}(\tau)\ge\frac12T_k\right\}.
\]

Partition all such shells in the following priority order:

\[
 \boxed{
 \begin{aligned}
 \mathcal I_{\rm def}(\tau)
  &:={\left\{k\in\mathcal I_D(\tau):
       m_{k,R}(\tau)\ge\frac18T_k\right\}},\\
 \mathcal I_{\rm hi}(\tau)
  &:={\left\{k\in\mathcal I_D(\tau)\setminus\mathcal I_{\rm def}(\tau):
       \int_{H_{k,R}}g_{k,R}(t)\,dt\ge\frac18T_k\right\}},\\
 \mathcal I_{\rm lo}(\tau)
  &:=\mathcal I_D(\tau)
    \setminus\bigl(\mathcal I_{\rm def}(\tau)
                   \cup\mathcal I_{\rm hi}(\tau)\bigr).
 \end{aligned}}
\tag{S.147}
\]

Zero clocks may be assigned arbitrarily and contribute nothing.  For every
\(k\in\mathcal I_{\rm lo}(\tau)\), (S.143) and (S.147) imply

\[
 \boxed{
 \int_{L_{k,R}}g_{k,R}(t)\,dt
 =D_{k,R}(\tau)-m_{k,R}(\tau)
  -\int_{H_{k,R}}g_{k,R}(t)\,dt
 >\frac14T_k.}
\tag{S.148}
\]

Thus (S.147) is exhaustive: anomalous defect carries one eighth, high-
Rayleigh viscous dissipation carries one eighth, or low-Rayleigh viscous
dissipation carries more than one quarter.  No Navier--Stokes sign is used
in this arithmetic step.

## 4. Low-Rayleigh dissipation creates parabolic kinetic mass

Combining (S.146) and (S.148), every
\(k\in\mathcal I_{\rm lo}(\tau)\) satisfies

\[
 \boxed{
 {1\over R^2}\int_{L_{k,R}}e_{k,R}(t)\,dt
 >{T_k\over8\lambda_k}.}
\tag{S.149}
\]

This is the promised parabolically normalized kinetic-mass lower bound.
It does not say that \(L_{k,R}\) itself has a fixed positive measure.

Set \(\delta_{k,R}:=|L_{k,R}|/R^2\).  The strict positivity in (S.149)
implies \(\delta_{k,R}>0\), while the frozen cutoff interval gives
\(\delta_{k,R}\le4\).  Jensen's inequality on \(L_{k,R}\) therefore yields

\[
 \boxed{
 \begin{aligned}
 {1\over R^2}\int_{L_{k,R}}e_{k,R}(t)^{3/2}\,dt
 &\ge\delta_{k,R}^{-1/2}
 \left({1\over R^2}\int_{L_{k,R}}e_{k,R}(t)\,dt\right)^{3/2}\\
 &>{1\over2}\left({T_k\over8\lambda_k}\right)^{3/2}.
 \end{aligned}}
\tag{S.150}
\]

Thin time support is favorable in this inequality: at fixed kinetic time
mass it increases, rather than decreases, the \(L_t^{3/2}\) quantity.

## 5. Per-shell and all-shell quadratic payment

Use the R0.74R cutoff-weighted velocity-cubic payment restricted to the
measurable low-Rayleigh set:

\[
 \boxed{
 p_{k,R}^{\rm lo}
 :=R^{-2}\gamma_k
 \int_{L_{k,R}}\eta_R(t)^{3/2}
 \int_{\operatorname{supp}\psi_k^R}
 |\widetilde v_R(t,y)|^3\,dy\,dt.}
\tag{S.151}
\]

The inherited padded-shell spatial Hölder estimate (R.214), integrated on
\(L_{k,R}\), is

\[
 \boxed{
 {1\over R^2}\int_{L_{k,R}}e_{k,R}(t)^{3/2}\,dt
 \le C_1\cdot2^{3k/2}\gamma_k^{1/2}p_{k,R}^{\rm lo}.}
\tag{S.152}
\]

Combining (S.150) and (S.152) proves the per-shell estimate

\[
 \boxed{
 T_k
 \le C_2\lambda_k\,2^k\gamma_k^{1/3}
       (p_{k,R}^{\rm lo})^{2/3},
 \qquad
 C_2=8(2C_1)^{2/3}.}
\tag{S.153}
\]

Define the deterministic coefficient ledger

\[
 \boxed{
 \mathscr L(\boldsymbol\lambda)
 :=\sum_{k\ge1}2^{3k}\gamma_k\lambda_k^3.}
\tag{S.154}
\]

### Theorem 5.1 — all low-Rayleigh dissipation clocks are quadratically paid

Suppose \(\mathscr L(\boldsymbol\lambda)<\infty\).  For every good terminal
time \(\tau\),

\[
 \boxed{
 \begin{aligned}
 \sum_{k\in\mathcal I_{\rm lo}(\tau)}K_{k,R}(\tau)
 &\le C_2\mathscr L(\boldsymbol\lambda)^{1/3}
       \left(\sum_{k\in\mathcal I_{\rm lo}(\tau)}
       p_{k,R}^{\rm lo}\right)^{2/3}\\
 &\le C_3\mathscr L(\boldsymbol\lambda)^{1/3}
       (P_R^M)^{2/3}.
 \end{aligned}}
\tag{S.155}
\]

**Proof.**  Apply Hölder with exponents \(3\) and \(3/2\) to (S.153) over
an arbitrary finite subset of \(\mathcal I_{\rm lo}(\tau)\).  This gives
the first line of (S.155).  Equation (R.211) permits the shell-dependent
sets \(L_{k,R}\) and bounds the sum of their nonnegative payments by
\(C_PP_R^M\).  Hence the second line holds with
\(C_3=C_2C_P^{2/3}\).  Finally let the finite subsets increase to the full
set; all terms are nonnegative.  \(\square\)

Thus the low-Rayleigh part of the dissipation branch supplies its own
clock-normalized persistence.  The endpoint energy
\(E_{k,R}(\tau)\) may be zero and is not used.

## 6. Explicit admissible Rayleigh profiles

The constant choice \(\lambda_k=1\) is admissible.  Indeed, if
\(a_k=2^{3k}\gamma_k\), then

\[
 \boxed{
 {a_{k+1}\over a_k}
 =8\exp\!\left(-{3\cdot4^{k-1}\over32}\right)
 \longrightarrow0,
 \qquad
 \sum_{k\ge1}2^{3k}\gamma_k<\infty.}
\tag{S.156}
\]

More generally, for every \(0\le\alpha<1/3\), the choice
\(\lambda_k=\gamma_k^{-\alpha}\) gives

\[
 \boxed{
 \mathscr L(\boldsymbol\lambda)
 =\sum_{k\ge1}2^{3k}\gamma_k^{1-3\alpha}<\infty.}
\tag{S.157}
\]

There is also a convenient near-critical family.  For every
\(\varepsilon>0\), set

\[
 \boxed{
 \lambda_k^{(\varepsilon)}
 :=2^{-(1+\varepsilon)k}\gamma_k^{-1/3}.
 \quad\text{Then}\quad
 \mathscr L(\boldsymbol\lambda^{(\varepsilon)})
 =\sum_{k\ge1}2^{-3\varepsilon k}
 ={2^{-3\varepsilon}\over1-2^{-3\varepsilon}}.}
\tag{S.158}
\]

The corresponding uncorrected boundary is genuinely non-summable:

\[
 \boxed{
 \lambda_k^{\rm crit}:=2^{-k}\gamma_k^{-1/3}
 \quad\Longrightarrow\quad
 2^{3k}\gamma_k(\lambda_k^{\rm crit})^3=1,
 \quad
 \mathscr L(\boldsymbol\lambda^{\rm crit})=\infty.}
\tag{S.159}
\]

Equations (S.158)--(S.159) locate the exact sequence-space boundary of this
argument.  They do not assert that the cutoff-weighted Rayleigh ratios of an
arbitrary solution obey any one of these profiles.

## 7. Exact residual ledger

The trichotomy and Theorem 5.1 give an unconditional residual formula for
what remains.  For every \(\boldsymbol\lambda\) with
\(\mathscr L(\boldsymbol\lambda)<\infty\) and every good terminal time,

\[
 \boxed{
 \begin{aligned}
 \sum_{k\in\mathcal I_D(\tau)}T_k
 \le{}&C_3\mathscr L(\boldsymbol\lambda)^{1/3}A_R\\
 &+8\sum_{k\in\mathcal I_{\rm def}(\tau)}m_{k,R}(\tau)
 +8\sum_{k\in\mathcal I_{\rm hi}(\tau)}
      \int_{H_{k,R}}g_{k,R}(t)\,dt,
 \qquad A_R=(P_R^M)^{2/3}.
 \end{aligned}}
\tag{S.160}
\]

Indeed, the low-Rayleigh sum is (S.155).  On
\(\mathcal I_{\rm def}\), definition (S.147) gives
\(T_k\le8m_{k,R}(\tau)\); on \(\mathcal I_{\rm hi}\), it gives
\(T_k\le8\int_{H_{k,R}}g_{k,R}\).  Apply these estimates first to finite
subsets and then use monotone convergence.  Equation (S.160) does not bound
either residual term.  It identifies them without hiding an additional
\(\ell^1\) clock remainder.

## 8. Conditional finite-exception consequence

Let

\[
 \mathcal B_\tau
 :=\mathcal I_{\rm def}(\tau)\cup\mathcal I_{\rm hi}(\tau)
\]

be the unclosed part of the dissipation-dominated family.  If a future PDE
argument proves \(\#\mathcal B_\tau\le N_D\), uniformly in the solution,
\(R\), and the good terminal time, then (S.155),
\(K_{k,R}(\tau)\le v_{k,R}\), and Cauchy--Schwarz give

\[
 \boxed{
 \begin{aligned}
 \sum_{k\in\mathcal I_{\rm lo}(\tau)}K_{k,R}(\tau)
 &\le C_3\mathscr L(\boldsymbol\lambda)^{1/3}A_R,\\
 \sum_{k\in\mathcal B_\tau}K_{k,R}(\tau)
 &\le\sqrt{N_D}\,Y_{2,R}^{\rm sf},
 \qquad A_R=(P_R^M)^{2/3}.
 \end{aligned}}
\tag{S.161}
\]

This is a **PROVED CONDITIONAL IMPLICATION**, not a finite-exception
theorem.  No uniform bound on \(\#\mathcal B_\tau\) is obtained here.  Even
if such a bound were later proved, the kinetic-persistence and terminal-
upcrossing branches would still have to be combined with their own valid
estimates before (Q.1) could follow.

## 9. Exact-shear diagnostic and its boundary

The high-Rayleigh alternative cannot simply be deleted.  Choose an anchor
with zero transverse phase.  The exact smooth periodic shear already audited
in R0.73Y and R0.74B has the form

\[
 u_N(t,x)=Ae^{-N^2(t-t_-)}\sin(Nx_2)e_1,
 \qquad p_N=0,\qquad A\ne0,\quad N\in\mathbb N.
\]

For fixed \(k,R\) and a nonzero cutoff \(\Psi_k^R\), its ratio is

\[
 \boxed{
 \rho_{k,R}^{(N)}
 =R^2N^2
 {\displaystyle\int_{\mathbb T^3}\Psi_k^R(x)\cos^2(Nx_2)\,dx
  \over
  \displaystyle\int_{\mathbb T^3}\Psi_k^R(x)\sin^2(Nx_2)\,dx},
 \qquad
 {\rho_{k,R}^{(N)}\over R^2N^2}\longrightarrow1.}
\tag{S.162}
\]

The limit is the Riemann--Lebesgue lemma applied separately to the two
trigonometric squares.  Thus, for each fixed threshold \(\lambda_k\), all
sufficiently high carrier frequencies lie in the high-Rayleigh time set
\(H_{k,R}\) at every active time with \(\eta_R(t)>0\).  This is consistent
with R0.74B's same-window cubic-only no-go and shows why the low-Rayleigh
branch alone cannot cover arbitrary carrier frequencies.

Equation (S.162) is only a diagnostic reuse of an inherited globally smooth
family.  This note does not claim a new exact-shear theorem, does not identify
the present dissipation clock with a constitutive memory stress, and does not
assert that the shear violates (S.155): it lies outside the low-Rayleigh
hypothesis when \(N\) is large.

More explicitly, let

\[
 M_k^R:=\int_{\mathbb T^3}\Psi_k^R(x)\,dx,
 \qquad
 c_{k,N}^R:=\int_{\mathbb T^3}\Psi_k^R(x)\cos(2Nx_2)\,dx.
\]

Then the quotient in (S.162) is
\((NR)^2(M_k^R+c_{k,N}^R)/(M_k^R-c_{k,N}^R)\), and
\(c_{k,N}^R\to0\).  At every active time, sufficiently large \(N\)
therefore places the shear in \(H_{k,R}\).

This shear also shows why it would be incorrect to advertise (S.162) as a
counterexample to the present completed-clock estimate.  Its mollified path
velocity and \(v_R\) are parallel to \(e_1\), and \(v_R-a_R\) is independent
of \(y_1\).  Since \(p_N=0\), periodic integration in \(y_1\) gives
\(F_{k,R}=0\) for every shell.  Hence \(K_{k,R}=Q_{k,R}\), and at each good
terminal time

\[
 \sum_kD_{k,R}(\tau)
 \le\sum_kK_{k,R}(\tau)
 =\sum_kQ_{k,R}(\tau)
 \le\sum_k\operatorname{TV}Q_{k,R}
 \le C_QA_R.
\]

Thus the exact shear proves that the high-Rayleigh time set can be nonempty,
while its own completed clocks are already paid by the inherited
\(Q\)-ledger.
In the conditional interface (R.216)--(R.217), this subclass may take
\(S_\tau=\varnothing\), \(q_{k,R,\tau}=\operatorname{TV}Q_{k,R}\), and
\(\Lambda_{k,R,\tau}=0\).  If
\(e_{k,R}^{\eta}(\tau)>0\), choose \(J_{k,\tau}\subset(s_R,\tau)\) of
positive measure where \(\eta_R>0\); the nontrivial shear then gives
\(0<\Theta_{k,R}^{\eta}(\tau;J_{k,\tau})<\infty\).  If the endpoint row
vanishes, choose any positive-measure \(J_{k,\tau}\subset(s_R,\tau)\) and
use the inherited convention
\(\Theta_{k,R}^{\eta}(\tau;J_{k,\tau})=+\infty\).  In both cases the
coefficient term in (R.217) is unambiguously zero.  Thus the extraction
condition closes for this shear subclass with no terminal exception; its
high Rayleigh ratio does not itself produce an obstruction to the completed
clock.

### Inherited instantaneous-sign sentinel

R0.73U is retained only as a warning about the other proposed route.  Its
exact \(u\), \(-u\) initial-data pair has the same even quadratic snapshot
and opposite odd tangent information, so even instantaneous data alone
cannot select a fixed signed-flux orientation.  That certificate probes a
selected Fourier coefficient, not the frozen padded collar used here, and
the comparison is not a trajectory symmetry.  More importantly, the
stopping eligibility in (S.25) depends on the preceding clock history and is
not preserved by the snapshot sign change.  No new sign-pair theorem and no
conclusion about the stopped estimate (S.38) are claimed in this note.

## 10. Decision and claim ledger

The following are **PROVED**:

- the exact viscous/defect split (S.143);
- measurability of the low/high-Rayleigh sets and the pointwise estimate
  (S.146);
- the exhaustive one-eighth/one-eighth/one-quarter trichotomy
  (S.147)--(S.148);
- the parabolic kinetic-mass and Jensen bounds (S.149)--(S.150);
- the per-shell payment (S.153) and all-shell theorem (S.155);
- the admissible constant, subcritical, and near-critical coefficient
  profiles (S.156)--(S.159); and
- the exact residual ledger (S.160) and conditional finite-exception
  implication (S.161).

The following are **INHERITED**:

- the suitable-weak total local-dissipation measure and completed clocks
  from R0.74P;
- the dissipation-dominated branch (S.23) from R0.74S Step 2;
- the padded-shell Hölder estimate (R.214) and shell-dependent payment
  bound (R.211) from R0.74R; and
- the exact shear and same-window high-frequency diagnostic from R0.73Y
  and R0.74B.

The following remain **OPEN**:

- quadratic payment or a uniform finite-exception theorem for
  \(\mathcal I_{\rm hi}(\tau)\);
- quadratic payment or a uniform finite-exception theorem for
  \(\mathcal I_{\rm def}(\tau)\);
- the large-payment stopped-work depletion estimate (S.38);
- a cross-channel Navier--Stokes sign or backscatter theorem;
- the full R0.74R extraction and persistence hypotheses;
- unconditional fixed-scale (Q.1), scale contraction, prescribed-centre
  scale packing, and regularity.

The following are **NOT CLAIMED**:

- a Fourier support theorem from the ratio \(\rho_{k,R}\);
- positive Lebesgue-time thickness of \(L_{k,R}\);
- absence of anomalous local-energy defect for suitable weak solutions;
- novelty or priority; or
- any conclusion on singularity formation or the Navier--Stokes existence
  and smoothness Millennium problem.

## 11. Inherited source ledger

| Use in this note | Frozen source | Status |
|---|---|---|
| Total local-dissipation measure and anomalous-defect split | R0.74P, (2.1)--(2.7) | **INHERITED / PROVED** |
| Completed shell balance \(K=E+D=Q+F\) | R0.74P, (2.8)--(2.10); R0.74R, (R.200)--(R.201) | **INHERITED / PROVED** |
| Padded-shell kinetic row, shell-dependent cubic payment, spatial Hölder estimate, and cross-shell Hölder ledger | R0.74R, (R.208)--(R.215) | **INHERITED / PROVED** |
| Dissipation-dominated terminal branch \(D_{k,R}(\tau)\ge K_{k,R}(\tau)/2\) | R0.74S Step 2, (S.23) | **INHERITED / PROVED** |
| Smooth exact shear, vanishing production structure, and same-window high-frequency diagnostic | R0.73Y; R0.74B, Section 6 | **INHERITED / PROVED IN THEIR STATED SCOPE** |
| Instantaneous even-state sign sentinel | R0.73U | **INHERITED / DIFFERENT FOURIER OBSERVABLE** |

The new argument is only the dissipation trichotomy and low-Rayleigh
payment (S.142)--(S.161).  No novelty or priority claim is made.

**NOT CLAY.**
