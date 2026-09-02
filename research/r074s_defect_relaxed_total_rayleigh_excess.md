# R0.74S Step 8 — a defect-relaxed total Rayleigh-excess residual

## 0. Result and scope

R0.74S Step 7 split a dissipation-dominated terminal clock into a
low-Rayleigh part, which is paid by the velocity-cubic ledger, and two open
parts: anomalous defect and high-Rayleigh viscous dissipation.  Those two
parts should not always be charged separately.  Some apparently large
dissipation is already visible to the quadratically paid time-cutoff clock
\(Q_{k,R}\).

This note performs that subtraction at the level of time measures.  For each
shell it introduces

- the parabolically normalized kinetic measure \(\sigma_{k,R}\);
- the total viscous-plus-defect measure \(\nu_{k,R}\);
- the absolute \(Q\)-density measure
  \(\beta_{k,R}=|\dot Q_{k,R}|\,dt\); and
- the minimal terminal scalar excess and the stronger Jordan local envelope
  \[
   x_{k,R}^{\boldsymbol\lambda}(\tau)
   :=\left[\nu_{k,R}(J_\tau)-\beta_{k,R}(J_\tau)
                 -2\lambda_k\sigma_{k,R}(J_\tau)\right]_+,
   \qquad
   X_{k,R}^{\boldsymbol\lambda}(\tau)
   :=\bigl(\nu_{k,R}-\beta_{k,R}
              -2\lambda_k\sigma_{k,R}\bigr)^+
       (J_\tau).
  \]

Every dissipation-dominated positive terminal clock then has one of three
payments: at least one sixth is carried by \(\beta\), its kinetic time mass
is larger than \(T_k/(12\lambda_k)\), or more than one sixth remains in the
smaller scalar excess \(x\).  The first family is paid by the inherited
quadratic \(Q\)-variation ledger; Jensen and the inherited padded-shell cubic
estimate pay the second family.  Only one selected excess family remains at
this stage of the algebra.  Replacing that selected residual by
\(\sum_kx_k\), or more conservatively by the local envelope \(\sum_kX_k\),
gives fixed-scale suitable-weak lower-semicontinuous interfaces.

The terminal clock identity then yields the decisive extra fact:
\(x_k\le[F_k(\tau)]_+\).  The full scalar ledger is bounded by the already
defined stopped signed-work gate, and on the priority-selected excess class
one has the sharper relation \(K_k(\tau)<6F_k(\tau)/5\).  Consequently the
entire dissipation-dominated branch is reduced to that existing gate with
coefficient \(6/5\).  Both global excess sums are finite at every fixed
\(R\) and good \(\tau\); the Jordan envelope is bounded by the total
localized dissipation, whereas the scalar ledger also has a linear flux
bound.

This is an exact unification and a weak-stability interface, not a quadratic
payment theorem.  In particular, the stopped-work supremum from Step 2
already permits the common zero-start stops used here.  The terminal
comparison therefore identifies the dissipation residual with that existing
gate rather than narrowing it.  The zero-start audit below goes further: the
universal quadratic bound proposed for this no-exception gate is false on the
inherited R0.74O/P smooth exact family.  The conditional implication (S.38)
remains valid, but its antecedent cannot be a universal theorem.  No quadratic,
square-function, or finite-exception estimate for the Jordan envelope is
proved.  The selected residual is not claimed to be lower semicontinuous,
because its index set depends on strict terminal inequalities.  No smooth
approximation of an arbitrary suitable weak solution is asserted to exist.
The note does not prove the repaired best-\(N\) terminal-tail estimate, the
R0.74R extraction hypotheses, the fixed-scale inequality (Q.1), regularity,
or the Millennium problem.  **NOT CLAY.**

No novelty or priority claim is made.

## 1. Three time measures and the open terminal interval

Retain exactly the periodic suitable-weak Version-M setting, viscosity one,
fixed \(R\), terminally anchored mollified path \(X_R\), nondecreasing cutoff
\(\eta_R\), padded shell cutoffs \(\Psi_k^R\), and weights

\[
 \gamma_k=\exp\!\left(-\frac{4^{k-1}}{32}\right)
\]

from R0.74P--R0.74R.  Put

\[
 \mathcal T_R:=(s_R,t_0)=I_{2R},
 \qquad J_\tau:=(s_R,\tau),
 \qquad s_R=t_0-4R^2,
 \qquad \tau\in(s_R,t_0).
\tag{S.163}
\]

The interval \(J_\tau\) is open at the terminal endpoint.  This is the same
endpoint convention as the spacetime measure integral defining
\(D_{k,R}(\tau)\) in (S.143) and (2.6).  In particular, a temporal atom of
the total dissipation measure at \(t=\tau\) is not silently inserted into a
clock whose terminal value was defined using \((s_R,\tau)\).

For a Borel set \(A\subset\mathcal T_R\), define

\[
 \boxed{
 \begin{aligned}
 \sigma_{k,R}(A)
  &:={1\over R^2}\int_A e_{k,R}(t)\,dt,\\
 \nu_{k,R}(A)
  &:={\gamma_k\over R}
    \int_{A\times\mathbb T^3}
      \eta_R(t)\Psi_k^R(x-X_R(t))\,d\boldsymbol\mu(t,x),\\
 \beta_{k,R}(A)
  &:=\int_A|\dot Q_{k,R}(t)|\,dt.
 \end{aligned}}
\tag{S.164}
\]

Here \(e_{k,R}\) is (S.142), \(\boldsymbol\mu\) is the total local
dissipation measure (2.1), and \(\dot Q_{k,R}\in L^1(\mathcal T_R)\) is the
almost-everywhere density of the canonical absolutely continuous primitive
(2.8).  Thus \(\sigma_{k,R}\), \(\nu_{k,R}\), and \(\beta_{k,R}\) are finite
nonnegative Radon measures on every \(J_\tau\).  The last is precisely the
total-variation measure of \(Q_{k,R}\).

Because the frozen smooth cutoff is identically zero on a neighborhood of
\(s_R\), both \(\eta_R\) and \(\eta_R'\) vanish there.  Hence all three
measures in (S.164) vanish on one common neighborhood of the left endpoint.
This removes any possible loss of mass through \(s_R\) in the later
open-interval argument.

If \(\boldsymbol\delta_{k,R}\) denotes the weighted temporal pushforward of
the anomalous measure \(\boldsymbol D\), then the exact measure identity is

\[
 \boxed{
 d\nu_{k,R}(t)=g_{k,R}(t)\,dt+d\boldsymbol\delta_{k,R}(t),
 \qquad
 \boldsymbol\delta_{k,R}(J_\tau)=m_{k,R}(\tau).}
\tag{S.165}
\]

Consequently, at every local-energy good terminal time,

\[
 \boxed{
 \nu_{k,R}(J_\tau)=D_{k,R}(\tau),
 \qquad
 \beta_{k,R}(J_\tau)
 =\operatorname {TV}_{J_\tau}Q_{k,R}.}
\tag{S.166}
\]

The second equality is valid at every \(\tau\), since \(Q_{k,R}\) is
absolutely continuous.  The first is asserted at the same good times at
which the inherited measure formula for the terminal clock is valid.

## 2. Jordan positive excess and its variational meaning

Fix a positive deterministic profile
\(\boldsymbol\lambda=(\lambda_k)_{k\ge1}\).  On the full interval
\(\mathcal T_R\), form the signed Radon measure below; its restriction to
each \(J_\tau\) is finite:

\[
 \alpha_{k,R}^{\boldsymbol\lambda}
 :=\nu_{k,R}-\beta_{k,R}-2\lambda_k\sigma_{k,R},
 \qquad
 \boxed{
 x_{k,R}^{\boldsymbol\lambda}(\tau)
 :=\left[\alpha_{k,R}^{\boldsymbol\lambda}(J_\tau)\right]_+,
 \qquad
 X_{k,R}^{\boldsymbol\lambda}(\tau)
 :=(\alpha_{k,R}^{\boldsymbol\lambda})^+(J_\tau).}
\tag{S.167}
\]

Here \(x\) applies the scalar positive part only after taking the full
terminal mass.  By contrast, the superscript \(+\) defining \(X\) is the
positive measure in the Jordan decomposition, so \(X\) retains positive
local excess even when it is cancelled by negative excess at other times.
For every finite signed Radon measure \(\alpha\) on the locally compact open
interval \(J_\tau\), regularity of the Jordan measures gives

\[
 \boxed{
 \begin{aligned}
 0\le[\alpha(J_\tau)]_+
 &\le\alpha^+(J_\tau),\\
 \alpha^+(J_\tau)
 &=\sup_{A\in\mathcal B(J_\tau)}\alpha(A)\\
 &=\sup_{\substack{\phi\in C_c(J_\tau)\\0\le\phi\le1}}
       \int_{J_\tau}\phi\,d\alpha.
 \end{aligned}}
\tag{S.168}
\]

For completeness, the Borel-set equality follows from a Hahn positive set.
For the continuous-test equality, every displayed test is bounded above by
\(\alpha^+(J_\tau)\).
Conversely, inner regularity selects a compact subset of a Hahn positive set
carrying all but an arbitrary \(\varepsilon>0\) of its positive mass;
outer regularity of \(\alpha^-\) and Urysohn approximation then give a
compactly supported continuous \(0\le\phi\le1\) whose integral is within
an arbitrarily small error of that mass.  Letting \(\varepsilon\downarrow0\)
proves (S.168).  This argument does not require the Hahn set to have positive
Lebesgue measure: an interior atom is detected exactly.

In particular,

\[
 \boxed{
 \nu_{k,R}(J_\tau)
 \le\beta_{k,R}(J_\tau)
    +2\lambda_k\sigma_{k,R}(J_\tau)
    +x_{k,R}^{\boldsymbol\lambda}(\tau)
  \le\beta_{k,R}(J_\tau)
    +2\lambda_k\sigma_{k,R}(J_\tau)
    +X_{k,R}^{\boldsymbol\lambda}(\tau).}
\tag{S.169}
\]

The first inequality is the scalar identity
\(a\le[a]_+\); the second uses \(x\le X\) from (S.168).  The smaller \(x\)
is sufficient for the terminal trichotomy.  The stronger measure-level
quantity \(X\) is retained because it has a local density formula and
prevents positive excess on one time region from being erased by negative
excess on another.

## 3. The one-sixth trichotomy

Fix a local-energy good terminal time \(\tau\), write
\(T_k:=K_{k,R}(\tau)\), and retain the Step 7 dissipation-dominated set

\[
 \mathcal I_D(\tau)
 :=\left\{k:T_k>0,\ D_{k,R}(\tau)\ge\frac12T_k\right\}.
\]

Partition it in the following priority order:

\[
 \boxed{
 \begin{aligned}
 \mathcal I_\beta(\tau)
 &:={\left\{k\in\mathcal I_D(\tau):
       \beta_{k,R}(J_\tau)\ge\frac16T_k\right\}},\\
 \mathcal I_\sigma(\tau)
 &:={\left\{k\in\mathcal I_D(\tau)\setminus\mathcal I_\beta(\tau):
       \sigma_{k,R}(J_\tau)>\frac{T_k}{12\lambda_k}\right\}},\\
 \mathcal I_x(\tau)
 &:=\mathcal I_D(\tau)
    \setminus\bigl(\mathcal I_\beta(\tau)
                    \cup\mathcal I_\sigma(\tau)\bigr).
 \end{aligned}}
\tag{S.170}
\]

For every \(k\in\mathcal I_x(\tau)\), (S.166) and the two failed priority
tests imply

\[
 \alpha_{k,R}^{\boldsymbol\lambda}(J_\tau)
 =\nu_{k,R}(J_\tau)-\beta_{k,R}(J_\tau)
       -2\lambda_k\sigma_{k,R}(J_\tau)
 >\frac12T_k-\frac16T_k-\frac16T_k
 =\frac16T_k.
\]

Hence \(x_{k,R}^{\boldsymbol\lambda}(\tau)>T_k/6\) on the residual class,
and the priority trichotomy is

\[
 \boxed{
 \beta_{k,R}(J_\tau)\ge\frac16T_k,
 \quad\hbox{or}\quad
 \sigma_{k,R}(J_\tau)>\frac{T_k}{12\lambda_k},
 \quad\hbox{or}\quad
 x_{k,R}^{\boldsymbol\lambda}(\tau)>\frac16T_k.}
\tag{S.171}
\]

The constants are literal.  Failure of the first test and of the strict
kinetic-mass test leaves more than \(T_k/6\) in the scalar excess.  Choosing
the paid kinetic branch before the excess branch makes
\(\mathcal I_x(\tau)\) no larger than it needs to be.  No Navier--Stokes
sign or time-regularity statement enters this arithmetic.

## 4. Jensen and velocity-cubic payment of the kinetic branch

For \(k\in\mathcal I_\sigma(\tau)\), set
\(\delta_\tau:=|J_\tau|/R^2=(\tau-s_R)/R^2\).  Then
\(0<\delta_\tau<4\), and Jensen gives

\[
 \boxed{
 \begin{aligned}
 {1\over R^2}\int_{J_\tau}e_{k,R}(t)^{3/2}\,dt
 &\ge\delta_\tau^{-1/2}
       \sigma_{k,R}(J_\tau)^{3/2}\\
 &>{1\over2}
       \left({T_k\over12\lambda_k}\right)^{3/2}.
 \end{aligned}}
\tag{S.172}
\]

The non-strict constant \(1/2\) is valid because
\(\delta_\tau^{-1/2}>1/2\).  Define the full preterminal shell payment

\[
 p_{k,R}^{\tau}
 :=R^{-2}\gamma_k
   \int_{J_\tau}\eta_R(t)^{3/2}
   \int_{\operatorname {supp}\psi_k^R}
      |\widetilde v_R(t,y)|^3\,dy\,dt.
\tag{S.173}
\]

The inherited spatial estimate (R.214), integrated on \(J_\tau\), gives

\[
 {1\over R^2}\int_{J_\tau}e_{k,R}^{3/2}\,dt
 \le C_1\,2^{3k/2}\gamma_k^{1/2}p_{k,R}^{\tau}.
\]

Combining this with (S.172) yields

\[
 \boxed{
 T_k
 \le C_4\lambda_k\,2^k\gamma_k^{1/3}
       (p_{k,R}^{\tau})^{2/3},
 \qquad C_4=12(2C_1)^{2/3}.}
\tag{S.174}
\]

Retain the Step 7 coefficient ledger

\[
 \mathscr L(\boldsymbol\lambda)
 :=\sum_{k\ge1}2^{3k}\gamma_k\lambda_k^3.
\tag{S.175}
\]

If \(\mathscr L(\boldsymbol\lambda)<\infty\), finite-shell Hölder followed
by monotone convergence and (R.211) gives

\[
 \boxed{
 \sum_{k\in\mathcal I_\sigma(\tau)}T_k
 \le C_5\mathscr L(\boldsymbol\lambda)^{1/3}
       (P_R^M)^{2/3},
 \qquad C_5=C_4C_P^{2/3}.}
\tag{S.176}
\]

The admissible profiles in (S.156)--(S.159), including
\(\lambda_k=1\) and every near-critical
\(2^{-(1+\varepsilon)k}\gamma_k^{-1/3}\) with \(\varepsilon>0\), apply
unchanged.

## 5. Selected and global all-shell excess ledgers

The \(\beta\)-branch is already quadratic.  From (3.5),

\[
 \sum_{k\in\mathcal I_\beta(\tau)}T_k
 \le6\sum_{k\ge1}\beta_{k,R}(J_\tau)
 \le6\sum_{k\ge1}\operatorname {TV}_{[s_R,t_0)}Q_{k,R}
 \le C_\beta(P_R^M)^{2/3}.
\tag{S.177}
\]

On the selected excess branch, \(T_k\le6x_k\).  Equations
(S.176)--(S.177) therefore prove the exact terminal residual inequality

\[
 \boxed{
 \begin{aligned}
 \sum_{k\in\mathcal I_D(\tau)}K_{k,R}(\tau)
 \le{}&C_6\bigl(1+\mathscr L(\boldsymbol\lambda)^{1/3}\bigr)
          (P_R^M)^{2/3}\\
 &+6\sum_{k\in\mathcal I_x(\tau)}
          x_{k,R}^{\boldsymbol\lambda}(\tau).
 \end{aligned}}
\tag{S.178}
\]

All infinite sums are obtained from arbitrary finite shell subsets and then
monotone convergence.  Equation (S.178) is the sharper algebraic theorem:
it charges only the priority-selected excess shells.

For compactness arguments it is safer to discard the moving index set and
define the two global one-residual interfaces, initially as extended
nonnegative sums,

\[
 \mathfrak x_{1,R}^{\boldsymbol\lambda}(\tau)
 :=\sum_{k\ge1}x_{k,R}^{\boldsymbol\lambda}(\tau),
 \qquad
 \mathcal X_{1,R}^{\boldsymbol\lambda}(\tau)
 :=\sum_{k\ge1}X_{k,R}^{\boldsymbol\lambda}(\tau),
 \qquad
 \mathfrak x_{1,R}^{\boldsymbol\lambda}(\tau),
 \mathcal X_{1,R}^{\boldsymbol\lambda}(\tau)\in[0,\infty],
 \qquad
 \mathfrak x_{1,R}^{\boldsymbol\lambda}(\tau)\le
 \mathcal X_{1,R}^{\boldsymbol\lambda}(\tau).
\tag{S.179}
\]

Section 10 proves that both extended sums in (S.179) are in fact finite at
every fixed \(R\) and good \(\tau\).  Then (S.178) has the stable, possibly
weaker consequences

\[
 \boxed{
 \begin{aligned}
 \sum_{k\in\mathcal I_D(\tau)}K_{k,R}(\tau)
 &\le C_6\bigl(1+\mathscr L(\boldsymbol\lambda)^{1/3}\bigr)
          (P_R^M)^{2/3}
      +6\mathfrak x_{1,R}^{\boldsymbol\lambda}(\tau)\\
 &\le C_6\bigl(1+\mathscr L(\boldsymbol\lambda)^{1/3}\bigr)
          (P_R^M)^{2/3}
      +6\mathcal X_{1,R}^{\boldsymbol\lambda}(\tau).
 \end{aligned}}
\tag{S.180}
\]

The distinction between the selected sum and either global sum is essential:
a global sum can charge shells that the priority trichotomy had already paid
through \(\beta\).  The Jordan envelope \(\mathcal X_{1,R}\) can additionally
retain local positive excess cancelled at the terminal scalar level.  Its
purpose is localization and the smooth density formula, not a smaller
terminal bound.  The estimates displayed so far do not give a quadratic
bound for either global interface; the later clock-identity argument gives a
linear bound for \(\mathfrak x_{1,R}\) and only fixed-scale finiteness for
\(\mathcal X_{1,R}\).

## 6. Exact comparison with the Step 7 residual

Let \(L_{k,R}\) and \(H_{k,R}\) be the Step 7 sets (S.144), built with the
same \(\lambda_k\).  The absolutely continuous density
\(g_{k,R}-2\lambda_kR^{-2}e_{k,R}\) is nonpositive on \(L_{k,R}\), while
its positive part on \(H_{k,R}\) is at most \(g_{k,R}\).  Subtracting the
additional nonnegative measure \(\beta_{k,R}\) can only reduce the positive
part.  Therefore the variational formula (S.168) gives the shellwise bound

\[
 \boxed{
 x_{k,R}^{\boldsymbol\lambda}(\tau)
 \le X_{k,R}^{\boldsymbol\lambda}(\tau)
 \le m_{k,R}(\tau)
    +\int_{H_{k,R}}g_{k,R}(t)\,dt.}
\tag{S.181}
\]

A direct proof is useful.  For every Borel \(A\subset J_\tau\),

\[
 \alpha_{k,R}^{\boldsymbol\lambda}(A)
 \le\boldsymbol\delta_{k,R}(A)
   +\int_{A\cap H_{k,R}}g_{k,R}(t)\,dt
 \le m_{k,R}(\tau)+\int_{H_{k,R}}g_{k,R}(t)\,dt;
\]

take the supremum over \(A\) using (S.168).

Equation (S.181) is a per-shell domination of both new excess tiers by the
*raw* sum of the two old
residual channels.  It does **not** imply that the last line of (S.178) is
numerically bounded by the prioritized residual in (S.160).  Step 7 sums
\(m_k\) only on \(\mathcal I_{\rm def}\), sums
\(\int_{H_k}g_k\) only on \(\mathcal I_{\rm hi}\), and pays
\(\mathcal I_{\rm lo}\) cubically; Step 8 uses a different priority
partition.  Moreover, \(\mathfrak x_{1,R}\) and
\(\mathcal X_{1,R}\) sum every shell.  Thus Step 8 is
a one-residual, weakly stable refinement and reorganization, not an
unconditional strict numerical sharpening of (S.160).

## 7. The exact shear is absorbed by \(\beta\)

For the inherited smooth heat shear

\[
 u_N(t,x)=Ae^{-N^2(t-t_-)}\sin(Nx_2)e_1,
 \qquad p_N=0,
\]

the R0.74S Step 7 audit gives \(F_{k,R}=0\) shellwise.  Hence
\(K_{k,R}=Q_{k,R}\), with both primitives zero at \(s_R\).  At every good
terminal time for which \(T_k=K_{k,R}(\tau)>0\),

\[
 \boxed{
 T_k=Q_{k,R}(\tau)
 \le\int_{s_R}^{\tau}|\dot Q_{k,R}(t)|\,dt
 =\beta_{k,R}(J_\tau),
 \qquad
 x_{k,R}^{\boldsymbol\lambda}(\tau)=0.}
\tag{S.182}
\]

The last equality follows from
\(\nu_{k,R}(J_\tau)=D_{k,R}(\tau)\le K_{k,R}(\tau)=T_k\le\beta_{k,R}(J_\tau)\).
Thus every dissipation-dominated shell of this exact shear enters
\(\mathcal I_\beta\), before the excess branch is tested.  This is stronger
than the one-sixth threshold and reconciles its arbitrarily large local
Rayleigh ratio with the completed-clock payment.  It is not asserted that
the Jordan-envelope value \(X_{k,R}^{\boldsymbol\lambda}\) vanishes; the
priority partition simply does not charge it.

## 8. Fixed-scale suitable-weak lower semicontinuity

Consider exactly the R0.74P fixed-scale convergence setting: periodic
suitable weak solutions \((u_n,p_n)\) obey the standard Lin compactness
bounds and, on every compact subcylinder,

\[
 u_n\to u\quad\hbox{strongly in }L^3,
 \qquad
 \nabla u_n\rightharpoonup\nabla u
       \quad\hbox{weakly in }L^2,
 \qquad
 p_n\rightharpoonup p
       \quad\hbox{weakly in }L^{3/2}.
\tag{S.183}
\]

Use the same fixed \(R\), the same terminal point \((t_0,x_0)\), and the
same deterministic profile \(\boldsymbol\lambda\) for every \(n\), together
with the corresponding Version-M paths.  R0.74P Lemmas 5.1--5.2 then give uniform
path convergence and local weak-* convergence of the total dissipation
measures.  For each fixed shell and every
\(\chi\in C_c(\mathcal T_R)\),

\[
 \int\chi\,d\nu_{k,R}^{(n)}\longrightarrow
 \int\chi\,d\nu_{k,R}.
\tag{S.184}
\]

Indeed, the moving weight
\(\chi(t)\eta_R(t)\Psi_k^R(x-X_{n,R}(t))\) converges uniformly to its
limit and has a common compact support.  The local masses of
\(\boldsymbol\mu_n\) are uniformly bounded by the proof of R0.74P Lemma
5.2, so the varying-test error tends to zero.

Strong moving-field convergence also gives

\[
 \|e_{k,R}^{(n)}-e_{k,R}\|_{L^1(\mathcal T_R)}\longrightarrow0,
 \qquad
 \|\dot Q_{k,R}^{(n)}-\dot Q_{k,R}\|_{L^1(\mathcal T_R)}\longrightarrow0.
\tag{S.185}
\]

Indeed, the fixed spacetime cylinder has finite measure, so strong
\(L^3\) convergence implies strong \(L^2\) convergence, and

\[
 \bigl\||v_{n,R}|^2-|v_R|^2\bigr\|_{L^1}
 \le\bigl(\|v_{n,R}\|_{L^2}+\|v_R\|_{L^2}\bigr)
       \|v_{n,R}-v_R\|_{L^2}\longrightarrow0.
\]

Multiplication by the fixed bounded coefficients
\(\eta_R\Psi_k^R\) and
\(\eta_R'\Psi_k^R+\eta_R\Delta\Psi_k^R\), followed by spatial integration,
gives the two \(L^1_t\) statements in (S.185).
The second statement uses the explicit quadratic density in (2.8), not
merely uniform convergence of its primitives.  Since absolute value is
one-Lipschitz,
\(\beta_{k,R}^{(n)}\to\beta_{k,R}\) in total variation; the first statement
likewise gives total-variation convergence of \(\sigma_{k,R}^{(n)}\).
Therefore

\[
 \alpha_{k,R}^{(n),\boldsymbol\lambda}
 \rightharpoonup^*
 \alpha_{k,R}^{\boldsymbol\lambda}
 \quad\hbox{locally on }\mathcal T_R,
 \qquad
 \nu_{k,R}(J_\tau)
 \le\liminf_{n\to\infty}\nu_{k,R}^{(n)}(J_\tau).
\tag{S.186}
\]

The second statement is the Portmanteau lower bound for the open set
\(J_\tau\); it does not assert convergence of its mass.  More explicitly,
choose \(\varepsilon_0>0\), uniform in \(n\), such that the frozen cutoff
and its derivative vanish on \((s_R,s_R+2\varepsilon_0)\).  All the measures
in (S.164) vanish there, and
\(\nu_{k,R}(J_\tau)=\nu_{k,R}((s_R+\varepsilon_0,\tau))\); the latter open
set is relatively compact in \(\mathcal T_R\), so local/vague
Portmanteau applies.  Equivalently,
inner regularity writes \(\nu(J_\tau)\) as the supremum of
\(\int\phi\,d\nu\) over \(0\le\phi\le1\) in \(C_c(J_\tau)\); each such
integral converges by (S.184), and taking the supremum gives the displayed
lower bound.  Since the
\(\beta\)- and \(\sigma\)-masses converge, the elementary implication
\(a\le\liminf a_n\), \(b_n\to b\Rightarrow
[a-b]_+\le\liminf[a_n-b_n]_+\) proves

\[
 \boxed{
 x_{k,R}^{\boldsymbol\lambda}[u,p](\tau)
 \le\liminf_{n\to\infty}
 x_{k,R}^{\boldsymbol\lambda}[u_n,p_n](\tau).}
\tag{S.187}
\]

For the stronger local envelope, apply (S.168) to one compactly supported
test at a time and then take the supremum.  This proves

\[
 \boxed{
 X_{k,R}^{\boldsymbol\lambda}[u,p](\tau)
 \le\liminf_{n\to\infty}
 X_{k,R}^{\boldsymbol\lambda}[u_n,p_n](\tau).}
\tag{S.188}
\]

Finite-shell Fatou followed by monotone convergence gives both global results

\[
 \boxed{
 \begin{aligned}
 \mathfrak x_{1,R}^{\boldsymbol\lambda}[u,p](\tau)
 &\le\liminf_{n\to\infty}
 \mathfrak x_{1,R}^{\boldsymbol\lambda}[u_n,p_n](\tau),\\
 \mathcal X_{1,R}^{\boldsymbol\lambda}[u,p](\tau)
 &\le\liminf_{n\to\infty}
 \mathcal X_{1,R}^{\boldsymbol\lambda}[u_n,p_n](\tau).
 \end{aligned}}
\tag{S.189}
\]

No convergence of \(\nu_{k,R}^{(n)}(J_\tau)\) is used.  Such convergence
can fail when mass reaches the hard time \(\tau\).  The open-interval
Portmanteau inequality makes (S.187) valid, and the compact-test formula
(S.168) makes (S.188) valid, under the verified R0.74P topology.  These
statements are fixed-scale Version M only;
they do not provide cross-scale compactness or a Version-F theorem.

## 9. Smooth formula and the approximation boundary

If \((u,p)\) itself is smooth on the relevant cylinder, then
\(\boldsymbol D=0\) and all three measures in (S.164) are absolutely
continuous.  Consequently,

\[
 \boxed{
 \begin{aligned}
 x_{k,R}^{\boldsymbol\lambda}[u,p](\tau)
 &=\left[
   \int_{s_R}^{\tau}
   \left(g_{k,R}(t)-|\dot Q_{k,R}(t)|
            -{2\lambda_k\over R^2}e_{k,R}(t)\right)dt
   \right]_+,\\
 X_{k,R}^{\boldsymbol\lambda}[u,p](\tau)
 &=\int_{s_R}^{\tau}
   \left[g_{k,R}(t)-|\dot Q_{k,R}(t)|
            -{2\lambda_k\over R^2}e_{k,R}(t)\right]_+dt.
 \end{aligned}}
\tag{S.190}
\]

More generally, **conditionally**, suppose a sequence of smooth periodic
solutions \((u_n,p_n)\) satisfies every convergence hypothesis in (S.183)
and converges to the suitable weak pair \((u,p)\), with the same fixed-scale
Version-M geometry.  Equations (S.187)--(S.190) then give

\[
 \boxed{
 \begin{aligned}
 x_{k,R}^{\boldsymbol\lambda}[u,p](\tau)
 &\le\liminf_{n\to\infty}
 \left[
 \int_{s_R}^{\tau}
 \left(g_{k,R}^{(n)}-|\dot Q_{k,R}^{(n)}|
       -{2\lambda_k\over R^2}e_{k,R}^{(n)}\right)dt
 \right]_+,\\
 X_{k,R}^{\boldsymbol\lambda}[u,p](\tau)
 &\le\liminf_{n\to\infty}
 \int_{s_R}^{\tau}
 \left[g_{k,R}^{(n)}-|\dot Q_{k,R}^{(n)}|
       -{2\lambda_k\over R^2}e_{k,R}^{(n)}\right]_+dt.
 \end{aligned}}
\tag{S.191}
\]

The same finite-Fatou passage gives the corresponding all-shell inequality.
R0.74P verifies the implication *if such a convergent sequence is supplied*;
it does not prove that every suitable weak solution admits smooth
Navier--Stokes approximants in this topology.  Equation (S.191) is therefore
an approximation formula under a stated hypothesis, not a smooth-density
theorem.

## 10. Fixed-scale finiteness and the stopped-work bridge

The measure order in (S.167) first gives a useful finiteness statement that
does not require the terminal clock identity.  Since
\(\alpha_{k,R}^{\boldsymbol\lambda}\le\nu_{k,R}\) as signed measures and
\(\nu_{k,R}\ge0\), one has
\((\alpha_{k,R}^{\boldsymbol\lambda})^+\le\nu_{k,R}\).  Therefore Tonelli,
the inherited \(C^2\)-convergence
\(\Theta_R=\sum_k\gamma_k\Psi_k^R\), and local finiteness of
\(\boldsymbol\mu\) imply the following.  Here the time cutoff makes the
integrand supported in a compact subcylinder because \(\tau<t_0\).

\[
 \boxed{
 \begin{aligned}
 0\le x_{k,R}^{\boldsymbol\lambda}(\tau)
 &\le X_{k,R}^{\boldsymbol\lambda}(\tau)
 \le\nu_{k,R}(J_\tau),\\
 \mathcal X_{1,R}^{\boldsymbol\lambda}(\tau)
 &\le\sum_{k\ge1}\nu_{k,R}(J_\tau)\\
 &= {1\over R}\int_{J_\tau\times\mathbb T^3}
       \eta_R(t)\Theta_R(x-X_R(t))\,d\boldsymbol\mu(t,x)
 <\infty.
 \end{aligned}}
\tag{S.192}
\]

This is fixed-scale finiteness, not a bound uniform in \(R\), a quadratic
payment by \((P_R^M)^{2/3}\), or a shell square-function estimate.

The smaller scalar excess has a stronger terminal comparison.  The canonical
primitives vanish at \(s_R\), so
\(\beta_{k,R}(J_\tau)\ge|Q_{k,R}(\tau)|\).  At every good terminal time the
completed-clock identity gives

\[
 \boxed{
 \begin{aligned}
 \alpha_{k,R}^{\boldsymbol\lambda}(J_\tau)
 &=Q_{k,R}(\tau)+F_{k,R}(\tau)-E_{k,R}(\tau)
   -\beta_{k,R}(J_\tau)-2\lambda_k\sigma_{k,R}(J_\tau)\\
 &\le F_{k,R}(\tau)-E_{k,R}(\tau)
          -2\lambda_k\sigma_{k,R}(J_\tau)
 \le F_{k,R}(\tau),\\
 x_{k,R}^{\boldsymbol\lambda}(\tau)
 &\le[F_{k,R}(\tau)]_+,\\
 \mathfrak x_{1,R}^{\boldsymbol\lambda}(\tau)
 &\le\sum_{k\ge1}[F_{k,R}(\tau)]_+
 \le\sum_{k\ge1}\operatorname {TV}_{[s_R,t_0)}F_{k,R}
 \le\mathfrak L_{{\rm abs},R}^M\le CP_R^M.
 \end{aligned}}
\tag{S.193}
\]

There is also an exact connection to the Step 2 stopped-work gate.  Choose a
common local-energy good time \(\sigma_0\), from the inherited common
full-measure good set, in the initial interval on which
\(\eta_R=\eta_R'=0\).  Then
\(K_{k,R}(\sigma_0)=Q_{k,R}(\sigma_0)=F_{k,R}(\sigma_0)=0\) for every shell.
If \(x_k(\tau)>0\), then \(D_k(\tau)>0\), hence \(K_k(\tau)>0\), and this
zero start satisfies the strict upcrossing condition (S.25).  For every
finite nonempty \(G\subset\{k:x_k(\tau)>0\}\), (S.193) gives

\[
 \boxed{
 \begin{aligned}
 W_R^M(\tau;G,(\sigma_0)_{k\in G})
 &=\sum_{k\in G}F_{k,R}(\tau)
 \ge\sum_{k\in G}x_{k,R}^{\boldsymbol\lambda}(\tau)>0,\\
 \mathfrak x_{1,R}^{\boldsymbol\lambda}(\tau)
 &\le\mathfrak W_{{\rm up},R}^M
 \le\mathfrak L_{{\rm abs},R}^M\le CP_R^M.
 \end{aligned}}
\tag{S.194}
\]

The second line follows by taking the supremum over finite \(G\), then using
the definition (S.37) and the inherited absolute estimate (S.35).  It is
stronger conceptually than the last line of (S.193): the scalar residual is
not a new open channel but a subledger of the existing signed stopped work.

The priority-selected class gives a better coefficient than the generic
bound \(T_k\le6x_k\).  If \(k\in\mathcal I_x(\tau)\), failure of the
\(\beta\)-test and \(T_k=Q_{k,R}(\tau)+F_{k,R}(\tau)\) yield

\[
 \boxed{
 |Q_{k,R}(\tau)|
 \le\beta_{k,R}(J_\tau)<{T_k\over6},
 \qquad
 F_{k,R}(\tau)=T_k-Q_{k,R}(\tau)
 \ge T_k-|Q_{k,R}(\tau)|>{5T_k\over6},
 \qquad
 T_k<{6\over5}F_{k,R}(\tau).}
\tag{S.195}
\]

Apply the same common zero stop first to an arbitrary finite subset of
\(\mathcal I_x(\tau)\), and then pass monotonically to all selected shells.
Combining the result with (S.176)--(S.177) proves

\[
 \boxed{
 \begin{aligned}
 \sum_{k\in\mathcal I_x(\tau)}K_{k,R}(\tau)
 &\le {6\over5}\mathfrak W_{{\rm up},R}^M,\\
 \sum_{k\in\mathcal I_D(\tau)}K_{k,R}(\tau)
 &\le C_6\bigl(1+\mathscr L(\boldsymbol\lambda)^{1/3}\bigr)
        (P_R^M)^{2/3}
      +{6\over5}\mathfrak W_{{\rm up},R}^M.
 \end{aligned}}
\tag{S.196}
\]

Thus anomalous defect and high-Rayleigh viscous dissipation do not leave an
independent scalar terminal obstruction after the \(Q\)-visible and kinetic
payments: their selected remainder is contained in the frozen Step 2 gate.
This does not itself improve that gate.  Indeed, because (S.37) ranges over
all good stops satisfying (S.25), the same common zero start is already
admissible for any finite family with positive terminal clocks; (S.27)
therefore supplied an all-shell conditional estimate before Step 8.  The new
content is the exact residual identification, the sharper selected
coefficient, and the lower-semicontinuous scalar/Jordan interfaces.

The same zero-start observation also decides whether the no-exception gate
can be the next target.  Define the already-paid quadratic variation and the
full terminal clock supremum by

\[
 \boxed{
 B_{Q,R}^M:=\sum_{k\ge1}
    \operatorname {TV}_{[s_R,t_0)}Q_{k,R}
    \le C_Q(P_R^M)^{2/3},
 \qquad
 \mathcal K_R^M:=\sup_{\tau\in\mathcal G_R}
    \sum_{k\ge1}K_{k,R}(\tau),
 \qquad
 \mathfrak C_{{\rm full},R}^M
 :=\sup_{s_R<\tau<t_0}
    \left[\sum_{k\ge1}F_{k,R}(\tau)\right]_+.}
\tag{S.197}
\]

where \(\mathcal G_R\) is the inherited common full-measure good-time set.
All three quantities are finite: \(K_k=Q_k+F_k\), \(K_k\ge0\), and the two
absolute variation ledgers are summable.  For any family admissible in
(S.37), compare its work directly with the full terminal flux:

\[
 W_R^M-\sum_kF_{k,R}(\tau)
 =\sum_{k\in I}\bigl[Q_{k,R}(\sigma_k)-K_{k,R}(\sigma_k)\bigr]
  +\sum_{k\notin I}\bigl[Q_{k,R}(\tau)-K_{k,R}(\tau)\bigr]
 \le B_{Q,R}^M.
\]

Here the two shell sets partition the ledger and \(K_k\ge0\).  Conversely,
at a good \(\tau\), use the common zero stop on arbitrary finite subsets of
the shells with \(K_k(\tau)>0\) and \(F_k(\tau)>0\), then pass monotonically.
Any omitted shell with \(K_k(\tau)=0<F_k(\tau)\) obeys
\(F_k(\tau)=-Q_k(\tau)\), and their total is at most \(B_{Q,R}^M\).
Uniform convergence and density of the common good-time set then give the
full-time comparison.  Hence

\[
 \boxed{
 \mathcal K_R^M-B_{Q,R}^M
 \le\mathfrak W_{{\rm up},R}^M
 \le\mathcal K_R^M+B_{Q,R}^M,
 \qquad
 \bigl|\mathfrak W_{{\rm up},R}^M-
             \mathfrak C_{{\rm full},R}^M\bigr|
 \le B_{Q,R}^M.}
\tag{S.198}
\]

The first comparison follows in the same way from the common zero stop and
the identity \(\sum_kF_k=\sum_kK_k-\sum_kQ_k\).  The coefficient one in the
second comparison is sharp already for the scalar single-shell stress
\(K=0\), \(Q=-B\), \(F=B\): then
\(\mathfrak C_{\rm full}=B\) while \(\mathfrak W_{\rm up}=0\).  Thus the
Step 2 observable is, up to an already-paid quadratic row, the full-cutoff
positive cumulative flux itself; it is not a smaller signed-depletion
quantity.  The inherited plateau quantity obeys
\(\mathfrak C_R^M\le\mathfrak C_{{\rm full},R}^M\); equality is neither
needed nor claimed.

Finally apply the inherited R0.74O/P smooth periodic exact family.  In its
notation,

\[
 \boxed{
 \mathfrak C_{R_j}^{M,*}\asymp T_*,
 \qquad
 \mathfrak C_{{\rm full},R_j}^{M,*}\ge\mathfrak C_{R_j}^{M,*},
 \qquad
 (P_{R_j}^{M,*})^{2/3}\asymp{T_*\over K_*},
 \qquad K_*\longrightarrow\infty,
 \qquad
 {\mathfrak W_{{\rm up},R_j}^{M,*}
   \over(P_{R_j}^{M,*})^{2/3}}\longrightarrow\infty.}
\tag{S.199}
\]

The last conclusion follows from (S.198) and the first two exact-family
comparisons, since the additive \(Q\)-error is only
\(O((P_{R_j}^{M,*})^{2/3})\).  Equivalently, one may select the
exact-family target shell alone: its terminal clock is
\(\gtrsim T_*\), its full \(Q\)-variation is
\(O(T_*/K_*)\), and the common zero stop makes its stopped work
\(\gtrsim T_*\).  The solution is smooth, periodic, mean zero, unforced,
and pressure free.  This refutes the *universal antecedent*
\(\mathfrak W_{{\rm up},R}^M\lesssim(P_R^M)^{2/3}\); it does not refute the
conditional algebra in (S.38), (S.196), an estimate with terminal
exceptions paid by \(Y_{2,R}^{\rm sf}\), or (Q.1).  The viable next target
must therefore return to the fixed best-\(N\), terminal-dependent exception
quantifier of R0.74Q (Q.7)--(Q.12), not the no-exception supremum (S.37).

## 11. Scalar and functional stress tests

### 11.1 Interior atoms are retained

On an open interval \(J\), take an interior point \(a\in J\) and the scalar
measures

\[
 \nu=T\delta_a,
 \qquad \beta=0,
 \qquad \sigma=0.
\]

Then \(x=X=T\).  Smooth nonnegative approximate identities concentrating at
\(a\) have the same limiting positive mass.  This confirms that (S.168)
detects a possible anomalous interior atom and that the residual is not
merely the positive part of an absolutely continuous density.  This is a
measure stress test, not a construction of a Navier--Stokes defect.

### 11.2 Already paid dissipation is removed

Let \(r\ge0\) be smooth and compactly supported in \(J\), and set

\[
 d\nu=r(t)\,dt,
 \qquad d\beta=r(t)\,dt,
 \qquad \sigma=0.
\]

Then \(x=X=0\), even if \(\nu(J)\) is large.  At the abstract clock level this
is realized by \(E=0\), \(D=K=Q=\int r\), and \(F=0\).  The test isolates
the intended algebraic role of \(\beta\); it is not asserted to be a PDE
trajectory.

### 11.3 There is no functional cubic bound for either excess tier

Choose a shell region on which \(\Psi_k^R\ge c_0>0\), a nonzero smooth
cutoff \(\zeta\) supported there, and

\[
 A_n(x)=n^{-2}\zeta(x)\sin(nx_1)e_3,
 \qquad w_n=\nabla\times A_n.
\]

After multiplication by a fixed smooth time cutoff supported where
\(\eta_R=1\), freeze the path at zero.  The inherited R0.74R functional
calculation gives

\[
 \int|\nabla w_n|^2\ge c>0,
 \qquad
 \int|w_n|^3=O(n^{-3}),
 \qquad
 \int|w_n|^2=O(n^{-2}).
\]

Thus the viscous part of \(\nu\) stays bounded below, while \(\sigma\), the
quadratic density defining \(\beta\), and the two-thirds power of the cubic
payment are all \(O(n^{-2})\).  Since
\(\alpha^+(J)\ge[\alpha(J)]_+\), one obtains
\(X\ge x\ge c/2\) for all large \(n\).  Therefore no estimate of either
excess tier by \(C(P_R^M)^{2/3}\) follows from incompressibility, cutoff geometry, and
Hölder alone.  These smooth divergence-free test fields are not asserted to
solve Navier--Stokes.  In particular, the test does not satisfy the
completed-clock identity used in (S.193), so it does not contradict the
linear PDE flux bound proved there.

### 11.4 The local envelope can exceed the terminal scalar excess

Take an absolutely continuous signed measure \(d\alpha=h(t)\,dt\), with
\(h=1\) on one subinterval, \(h=-1\) on a disjoint subinterval of the same
length, and \(h=0\) elsewhere.  Then \(x=[\int h]_+=0\), whereas
\(X=\int[h]_+>0\).  This verifies both the order \(x\le X\) and the reason
the sharper terminal theorem uses \(x\), while the Jordan envelope records
uncancelled local excess.

### 11.5 Endpoint escape permits only lower semicontinuity

For \(a_n\uparrow\tau\), let \(\nu_n=\delta_{a_n}\) and
\(\beta_n=\sigma_n=0\).  On the ambient interval \(\mathcal T_R\), one has
\(\nu_n\rightharpoonup^*\delta_\tau\); after restriction to the open
\(J_\tau\), the same sequence converges vaguely to zero.  Thus
\(x_n=X_n=1\) and the ambient limiting measure gives \(x=X=0\) when
evaluated on \(J_\tau\).  Hence
(S.187)--(S.188) are sharp in direction and ordinary convergence of the total mass on
\(J_\tau\) is false.  Including the endpoint without changing the inherited
clock convention would define a different object.

### 11.6 Uniform primitive convergence is insufficient for \(\beta\)

On a fixed interval, \(Q_n(t)=n^{-1}\sin(nt)\) converges uniformly to zero,
but

\[
 \int|\dot Q_n(t)|\,dt=\int|\cos(nt)|\,dt
\]

does not converge to zero.  This scalar test explains why the proof of
(S.185) uses strong \(L^1\) convergence of the explicit \(Q\)-densities,
not only the uniform primitive convergence in R0.74P Lemma 5.3.

## 12. Decision and claim ledger

The following are **PROVED**:

- the time-measure identities (S.164)--(S.166), with the open-terminal
  convention inherited from the completed clock;
- the Jordan/continuous-test variational formula (S.168) and total-mass
  bound (S.169);
- the exact one-sixth trichotomy (S.170)--(S.171);
- the Jensen, per-shell, and all-shell kinetic payments
  (S.172)--(S.176);
- the selected residual theorem (S.178) and its global consequence
  (S.180);
- the per-shell comparison with the raw Step 7 residual (S.181);
- absorption of the inherited exact shear into the \(\beta\)-priority branch
  (S.182); and
- fixed-scale Version-M lower semicontinuity (S.187)--(S.189) under exactly
  the convergence hypotheses (S.183);
- fixed-scale finiteness of both global ledgers, including
  \(\mathcal X_{1,R}\le\sum_k\nu_k<\infty\), in (S.192);
- terminal physical-flux domination and the linear scalar estimate
  (S.193)--(S.194); and
- the \(5/6\) positive-flux relation on the selected class and the exact
  reduction of the full dissipation branch to the existing stopped-work gate
  in (S.195)--(S.196);
- the two-sided equivalence of the no-exception stopped-work supremum with
  the full terminal clock and positive cumulative flux, modulo the paid
  \(Q\)-variation, in (S.197)--(S.198); and
- the smooth exact-family refutation of a universal quadratic bound for that
  no-exception gate in (S.199).

The following are **CONDITIONAL**:

- the smooth-approximation inequalities (S.191), conditional on being supplied
  a smooth Navier--Stokes sequence satisfying the inherited R0.74P topology.

The following are **INHERITED**:

- the suitable-weak total dissipation measure and canonical clocks from
  R0.74P;
- the absolute quadratic \(Q\)-variation ledger from R0.74P;
- the padded-shell cubic estimate and shell-dependent payment bound from
  R0.74R;
- the Step 7 dissipation branch, Rayleigh split, coefficient profiles, and
  exact-shear audit;
- the R0.74O/P smooth exact-family scale separation used in (S.199).

The following are **REFUTED**:

- the universal all-solution estimate
  \(\mathfrak W_{{\rm up},R}^M\lesssim(P_R^M)^{2/3}\) for the
  no-exception supremum (S.37).  The conditional implication (S.38) itself
  remains correct.

The following remain **OPEN**:

- a fixed best-\(N_0\), terminal-dependent-exception estimate compatible
  with the \(\sqrt{N_0}Y_{2,R}^{\rm sf}\) payment in R0.74Q;
- any quadratic, square-function, or finite-exception bound for
  \(\mathcal X_{1,R}\); fixed-scale finiteness alone is not such a bound;
- a quadratic or finite-exception bound for \(\mathfrak x_{1,R}\) beyond
  its proved linear control by \(CP_R^M\) and \(\mathfrak W_{{\rm up},R}^M\);
- suitable-weak approximation by smooth Navier--Stokes solutions;
- the full R0.74R extraction hypotheses;
- unconditional fixed-scale (Q.1), scale contraction, prescribed-centre
  scale packing, and regularity.

The following are **NOT CLAIMED**:

- that \(X_k\) vanishes for the exact shear;
- that the selected excess sum is lower semicontinuous;
- that (S.178) is numerically smaller than the prioritized Step 7 bound
  (S.160);
- that \(\mathcal X_{1,R}\le\mathfrak W_{{\rm up},R}^M\), or that the
  linear estimate \(CP_R^M\) is a quadratic estimate when \(P_R^M>1\);
- that Step 8 narrows the definition of the ultimate Step 2 stopped-work
  obstruction;
- that weak-* convergence passes the hard-interval masses
  \(\nu_n(J_\tau)\);
- existence of smooth approximants, novelty, priority, singularity
  formation, or a solution of the Navier--Stokes Millennium problem.

## 13. Inherited source ledger

| Use in this note | Frozen source | Status |
|---|---|---|
| Total local dissipation measure, anomalous split, and open-terminal completed clock | R0.74P, (2.1)--(2.10) | **INHERITED / PROVED** |
| Absolute \(Q\)-variation bound \(\sum_k\operatorname{TV}Q_k\le C(P_R^M)^{2/3}\) | R0.74P, (3.4)--(3.5) | **INHERITED / PROVED** |
| \(C^2\)-convergent shell weight \(\Theta_R\) and absolute \(F\)-variation bound | R0.74P, (1.4)--(1.5), (3.4a)--(3.6) | **INHERITED / PROVED** |
| Fixed-scale Version-M path, field, total-measure, and canonical-density convergence | R0.74P, Lemmas 5.1--5.3 | **INHERITED / PROVED UNDER (S.183)** |
| Terminal upcrossing condition, stopped work, absolute bound, and conditional gate | R0.74S Step 2, (S.25)--(S.38) | **INHERITED / CONDITIONAL IMPLICATION PROVED; UNIVERSAL ANTECEDENT REFUTED HERE** |
| Padded-shell spatial Hölder estimate and shell-dependent cubic payment | R0.74R, (R.209)--(R.215) | **INHERITED / PROVED** |
| Dissipation-dominated branch, low/high-Rayleigh split, old residual ledger, and shear audit | R0.74S Step 7, (S.142)--(S.162) | **INHERITED / PROVED** |
| Exact heat shear and shellwise \(F_k=0\) audit | R0.73Y; R0.74B; R0.74S Step 7, Section 9 | **INHERITED / PROVED IN THEIR STATED SCOPE** |
| Smooth pressure-free amplitude family and scale separation \(\mathfrak C_*\asymp T_*\), \((P_*^M)^{2/3}\asymp T_*/K_*\) | R0.74O, (1.7)--(1.12), (4.1)--(4.6), (6.1), (6.5)--(6.9); R0.74P, (0.1)--(0.2), (4.1)--(4.4) | **INHERITED / PROVED** |
| High-frequency divergence-free functional stress family | R0.74R, Proposition 5.3 | **INHERITED / NOT A PDE SOLUTION** |

The new content is the measure residual, one-sixth trichotomy, selected and
global excess ledgers, exact endpoint-safe lower-semicontinuity proof,
conditional smooth formula, fixed-scale finiteness, and the physical-flux /
stopped-work bridge, followed by the zero-start equivalence and exact-family
refutation (S.163)--(S.199).  No novelty or priority claim is made.

**NOT CLAY.**
