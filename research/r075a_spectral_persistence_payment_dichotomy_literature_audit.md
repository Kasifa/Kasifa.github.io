# R0.75A literature audit -- moving local persistence versus parabolic observability

## 0. Binding, question, and verdict

This bounded literature audit is attached to

`research/r075a_spectral_persistence_payment_dichotomy.md`

at frozen SHA-256

`f8117a7ff6380676d2ed05e749119579cc3f6972463834dcc6ad2a0b03026388`.

The hash was recomputed locally before the audit.  The literature access date
is **2026-09-03**.

The question screened here is deliberately narrow.  Does any inspected
primary source already give, with constants usable in the frozen asymptotic
ledger, the implication

\[
 E(t_2)\quad\Longrightarrow\quad
 \int_{t_2-cR^3}^{t_2}\int_{\mathcal S_+(t)}|F|^2
 \gtrsim E(t_2)R^3
 \quad\Longrightarrow\quad
 (P_R^M)^{2/3}
 \gtrsim h_{\rm rem}R^{2/3}\omega^{-5/6}L^{-1/6}
 \tag{LA.1}
\]

for the periodic, moving-frame common-shear equation

\[
 (\partial_t+b(t,x_3)\partial_2-\Delta_{23})F=0,
 \qquad
 u=(F,b,0),
 \tag{LA.2}
\]

with the full periodic total field, a moving anisotropic remote strip, and the
nonnegative exterior row of the Version-M payment?

**Verdict: PASS; the material citation-and-framing requirement is satisfied
in the bound main note, with zero literature blockers.**  None of the seven
inspected papers directly supplies
all of (LA.1).  The closest precedent is nevertheless very close at the local
energy level: Wang--Wang--Zhang--Zhang, arXiv:1711.04279, prove for the pure
heat equation an inner-ball endpoint / outer-ball spacetime estimate with
coefficient

\[
 T^{-1}+C_n(r-r')^{-2}.
 \tag{LA.3}
\]

With $T\asymp R^3$, $r-r'\asymp R$, and $R\leq1$, (LA.3) has the same
dominant $R^{-3}$ scale as the frozen local dichotomy.  Thus A.18--A.26
must be framed as an exact moving-drift, anisotropic adaptation of a standard
localized-energy mechanism, not as a new generic observability principle.
The frozen note makes no novelty claim, so this is not a blocker.  The bound
revision now cites and delimits this precedent accurately.

The thick-set, non-autonomous observability, moving-control, and quantitative
unique-continuation results below are genuine neighbors, but their operator
classes, global geometry, or constants do not directly produce the polynomial
$R^3$ residence scale.  None of them contains the subsequent shell-weighted
Hölder conversion to $P_R^M$.

This is **not** a priority or novelty determination.  A bounded non-hit cannot
establish either one.

## 1. Target anatomy and the constant that must be preserved

The frozen proof works after the packet translation
$z=x_2-Q_2(t)$.  The total field obeys

\[
 \partial_t\widetilde F
 =\Delta_{z3}\widetilde F-c(t,x_3)\partial_z\widetilde F,
 \qquad
 c=b(t,x_3)-Q_2'(t).
 \tag{LA.4}
\]

For a cutoff fixed in the moving frame, equal to one on the endpoint core and
supported in the enlarged strip, the exact identity is

\[
 \frac12E'(t)+\int\phi|\nabla_{z3}\widetilde F|^2
 =\frac12\int
 \bigl(c\,\partial_z\phi+\Delta_{z3}\phi\bigr)|\widetilde F|^2.
 \tag{LA.5}
\]

The frozen estimates are

\[
 |c|\lesssim R^{-2},\qquad
 |\partial_z\phi|\lesssim R^{-1},\qquad
 |\Delta\phi|\lesssim R^{-2}.
 \tag{LA.6}
\]

Consequently, for $R\leq1$, the cutoff error is bounded by
$CR^{-3}\int_{\mathcal S_+(t)}|F|^2$.  Integrating on a time interval of
length $cR^3$ yields the field-level dichotomy in (LA.1).  No spectral
decomposition, propagation of smallness, or observability constant is used.

The second arrow in (LA.1) has three project-specific ingredients:

1. the spacetime tube has volume
   $O(L^{1/2}R^6)$;
2. Hölder converts its $L^2$ mass to an $L^3$ lower bound;
3. on that tube the shifted scale-$2R$ exterior weight is at least
   $\omega^{1/4}$, and
   $E(t_2)\geq (2R/\omega)h_{\rm rem}$.

These give

\[
 P_R^M\gtrsim
 h_{\rm rem}^{3/2}R\omega^{-5/4}L^{-1/4},
 \qquad
 (P_R^M)^{2/3}\gtrsim
 h_{\rm rem}R^{2/3}\omega^{-5/6}L^{-1/6}.
 \tag{LA.7}
\]

An applicable collision would therefore need more than qualitative unique
continuation or final-state observability.  It would need a compatible
operator, nested moving geometry, a constant no worse than $CR^{-3}$, and a
route to the precise nonnegative weighted cubic payment.  That is the standard
used below.

## 2. Primary-source register and access boundary

Only arXiv-hosted primary manuscripts and their landing-page metadata were
used.  No secondary summaries or citation-count claims enter the verdict.

| ID | title, authors, date | version and material inspected |
|---|---|---|
| [arXiv:1711.04279](https://arxiv.org/abs/1711.04279) | *Observable set, observability, interpolation inequality and spectral inequality for the heat equation in \(\mathbb R^n\)*; Gengsheng Wang, Ming Wang, Can Zhang, Yubiao Zhang; submitted 2017-11-12, revised 2017-11-28 | v2 landing page and full TeX source; in particular the main equivalence, the explicit observability constant, and Section 3.2's local ball theorem and proof. Experimental HTML was not relied upon. |
| [arXiv:2203.08469](https://arxiv.org/abs/2203.08469) | *Observability for Non-autonomous Systems*; Clemens Bombach, Fabian Gabel, Christian Seifert, Martin Tautenhahn; submitted 2022-03-16, v3 dated 2023-02-27 | v3 landing page and full arXiv HTML; Theorems 4.8 and 4.10, Remark 4.9, and the Ornstein--Uhlenbeck section. The landing page records publication in *SIAM Journal on Control and Optimization* 61 (2023), 313--339. |
| [arXiv:1908.10603](https://arxiv.org/abs/1908.10603) | *Geometric conditions for the null-controllability of hypoelliptic quadratic parabolic equations with moving control supports*; Karine Beauchard, Michela Egidi, Karel Pravda-Starov; submitted 2019-08-28 | v1 landing page and full arXiv HTML; Definition 1.3 and Theorem 1.5, including the linear-flow integral-thickness condition. |
| [arXiv:1711.06730](https://arxiv.org/abs/1711.06730) | *Quantitative unique continuation for a parabolic equation*; Guher Camliyurt, Igor Kukavica; submitted 2017-11-17 | v1 landing page and full arXiv HTML; equation (2.1), Dirichlet quotient (2.5), and Theorem 2.1. |
| [arXiv:2107.11698](https://arxiv.org/abs/2107.11698) | *On quantitative uniqueness for parabolic equations*; Igor Kukavica, Quinn Le; submitted 2021-07-24 | v1 landing page and full arXiv HTML; Theorems 2.1--2.3 and Lemmas 4.1--4.2. Any later date printed by a live `\today` command in rendered source is not treated as bibliographic metadata. |
| [arXiv:1109.3863](https://arxiv.org/abs/1109.3863) | landing-page title *An observability for parabolic equations from a measurable set in time*; Kim Dang Phung, Gengsheng Wang; submitted 2011-09-18 | v1 landing page and full arXiv HTML. The manuscript title is *An observability estimate for parabolic equations from a measurable set in time and its applications*. Theorem 1.1 and Proposition 2.2 were inspected. |
| [arXiv:1702.00449](https://arxiv.org/abs/1702.00449) | *Local energy bounds and \(\epsilon\)-regularity criteria for the 3D Navier--Stokes system*; Cristi Guevara, Nguyen Cong Phuc; submitted 2017-02-01 | v1 landing page and full arXiv HTML; suitable-weak local energy inequality, Theorem 1.8, and Proposition 3.1. |

No paywalled publisher text was required to read the stated results.  This
screen did not exhaust references cited by these papers, later citing papers,
books, or the full literature on parabolic Caccioppoli inequalities.  Its
negative finding is therefore an applicability result for this corpus, not
priority evidence.

## 3. Source-by-source collision and applicability screen

### 3.1 Wang--Wang--Zhang--Zhang, arXiv:1711.04279

There are two distinct results to separate.

First, the paper characterizes observable sets for the autonomous heat
equation on $\mathbb R^n$: a measurable set is observable exactly when it is
$\gamma$-thick at some scale.  For a $\gamma$-thick set at scale $L_0$,
the paper tracks a global observability constant of the form

\[
 C_{\rm obs}
 =\exp\!\left[
 C_n(1+L_0)^2(1+\log(1/\gamma))^2(1+T^{-1})
 \right].
 \tag{LA.8}
\]

The periodic lift of the frozen torus strip is thick for each fixed
$(R,L)$, because its copies recur every torus period.  It is not uniformly
thick in the asymptotic family: its volume fraction is of order
$L^{1/2}R^3$ in the three-dimensional lift and tends to zero.  Even before
that degeneration is inserted, $T\asymp R^3$ makes (LA.8) exponential in
$R^{-3}$.  This global theorem therefore cannot recover the polynomial
$R^{-3}$ local ledger.

Second, and much closer, Section 3.2, Theorem 3.2 (TeX label `prop-1`), proves
for the pure heat equation that for $0<r'<r$,

\[
 \int_{B_{r'}}|u(T)|^2
 \leq
 \left(\frac1T+\frac{C n}{(r-r')^2}\right)
 \int_0^T\int_{B_r}|u(t,x)|^2\,dx\,dt.
 \tag{LA.9}
\]

Its proof uses a nested spatial cutoff and an energy computation.  Thus it is
a direct structural precedent for the endpoint-core / enlarged-tube step in
R0.75A.  Under $T\asymp R^3$ and $r-r'\asymp R$, (LA.9) already gives the
same dominant $R^{-3}$ scale for pure heat.

It is not, however, a theorem that can simply be cited in place of the frozen
proof:

- its operator is $\partial_t-\Delta$, whereas (LA.4) has the
  space-dependent drift $c(t,x_3)\partial_z$;
- its balls are fixed and isotropic in $\mathbb R^n$, whereas the frozen
  core and strip are anisotropic and move in the original coordinates;
- it contains neither the torus/all-winding formulation nor the shell
  inclusion and shifted weight;
- it ends with an $L^2$ observation inequality, not the Version-M weighted
  cubic payment (LA.7).

The gap is small at the **local-energy mechanism** and large at the
**project-specific conclusion**.  Publication framing should explicitly cite
(LA.9) as the closest precedent.  No novelty claim should be attached to the
bare cutoff mechanism.

### 3.2 Bombach--Gabel--Seifert--Tautenhahn, arXiv:2203.08469

The abstract theorem combines an uncertainty principle for low frequencies
with high-frequency dissipation and yields final-state observability from a
positive-measure time set.  Its concrete elliptic application, Theorem 4.8,
uses operators

\[
 A(t)=\sum_{|\alpha|\leq m}a_\alpha(t)\partial^\alpha
 \tag{LA.10}
\]

whose coefficients depend on time but not on space, on $\mathbb R^d$, and a
family of observation sets uniformly thick in time.  For full-time
observation, Remark 4.9 gives

\[
 C_{\rm obs}\leq C_1T^{-1/r}
 \exp\!\left(
 C_2T^{-\gamma_1\gamma_3/(\gamma_2-\gamma_1)}+C_3T
 \right).
 \tag{LA.11}
\]

For a second-order heat operator the exponent is $C/T$, hence
$e^{C/R^3}$ at the frozen time scale.  The constants also inherit the
uniform-thickness parameters.

The paper separately treats non-autonomous Ornstein--Uhlenbeck operators with
linear spatial drift $-\langle B(t)x,\nabla\rangle$ under a Kalman condition.
Neither concrete class contains the periodic nonlinear shear coefficient
$b(t,x_3)\partial_2$.  The target strip's periodic lift is only
parameter-dependently thick, not uniformly thick as $R\downarrow0$.

One could try to apply the paper's abstract theorem only after separately
proving an uncertainty principle and a dissipation estimate for the
common-shear evolution with constants tracked through $(R,L)$.  Those would
be new hypotheses, not consequences of the cited application theorems, and
their usual cost is far too weak for (LA.1).  The output is also global
final-state observability rather than a nested local endpoint-to-tube estimate
and contains no Version-M weight.  **No direct applicability.**

### 3.3 Beauchard--Egidi--Pravda-Starov, arXiv:1908.10603

The paper studies null controllability on $\mathbb R^d$ for non-autonomous
Ornstein--Uhlenbeck equations and more general quadratic generators.  Theorem
1.5 assumes a generalized Kalman rank condition.  A sufficient condition is
uniform thickness of the moving control support on times accumulating at the
final time.  A necessary condition is the integral thickness

\[
 \exists r,\delta>0\quad\forall x\in\mathbb R^d:\quad
 \int_0^T
 |B_d(x,r)\cap R(0,T-t)\omega(t)|\,dt\geq\delta,
 \tag{LA.12}
\]

where $R$ is the resolvent of the **linear** drift system.  If the support
exactly follows that linear flow, thickness of the reference support is
necessary and sufficient.

This is the most relevant inspected source for the phrase “moving support,”
but the match stops there.  The frozen translation $Q_2(t)$ follows the
shear at the single height $h_2$; it is not the full flow of
$x_2'=b(t,x_3)$ at every $x_3$.  After translation the residual coefficient
$c(t,x_3)$ remains.  This is not an Ornstein--Uhlenbeck linear drift or a
quadratic Weyl generator, and the domain is a torus rather than
$\mathbb R^d$.  Moreover, (LA.12) is a global geometric condition for null
control, not a quantitative $CR^{-3}$ local residence estimate.  It supplies
no scale-sharp observability cost and no weighted cubic payment.  **Geometric
adjacency, no direct theorem.**

### 3.4 Camliyurt--Kukavica, arXiv:1711.06730

The equation studied is

\[
 u_t-\Delta u=w_j(x,t)\partial_j u+v(x,t)u
 \tag{LA.13}
\]

with bounded lower-order coefficients, including a periodic setting.  Thus
the common-shear scalar equation fits formally with $v=0$ and one component
of $w$ equal to $-b$, or with $-c$ after moving coordinates.  Theorem 2.1
bounds the order of vanishing by

\[
 O_{(x_0,t_0)}(u)
 \leq C\bigl(M_1^2+M_0^{2/3}\bigr),
 \tag{LA.14}
\]

where the paper expressly states that $C$ depends on the time interval,
period, and an a priori upper bound $q_0$ for the global Dirichlet quotient.

This is not the quantity required in R0.75A.  It controls finite-order
vanishing at a point; it does not lower-bound residence of positive-volume
endpoint mass in a moving tube.  At the frozen scale
$M_1\sim\|b\|_\infty\sim R^{-2}$, even the displayed vanishing exponent is
of order $R^{-4}$, before the $q_0$ dependence is considered.  An
arbitrarily ill-conditioned finite corrector family need not have a uniform
$q_0$.  The theorem neither preserves the needed polynomial constant nor
reaches (LA.7).  **Formal operator match, conclusion and constant mismatch.**

### 3.5 Kukavica--Le, arXiv:2107.11698

This paper treats (LA.13) with drift and potential in mixed Lebesgue classes,
in periodic and whole-space settings.  It proves quantitative vanishing-order
bounds and a same-time global-to-ball estimate of the form

\[
 \|u(t)\|_{L^2(\mathbb T^n)}
 \lesssim
 e^{P(n,\delta_0,M_0,M_1,p,q)}
 \|u(t)\|_{L^2(B_{\delta_0})}.
 \tag{LA.15}
\]

The hypotheses include finiteness of a global Dirichlet quotient $q_0$, and
Theorem 2.1 explicitly declares dependence of its implicit constant on
$q_0$ and the time interval.  Lemma 4.2 displays the more informative cost
$e^{(n+1)\delta_0^2/\delta^2}$, where $\delta$ must be chosen below
quantities involving the coefficient norms and $\delta_0$.  Thus, with
$\delta_0\asymp R$ and $M_1\asymp R^{-2}$, the available cost is of
exponential-of-polynomial type in $R^{-1}$, not the $CR^{-3}$ coefficient
needed in (LA.1).  The displayed argument also does not furnish a constant
uniform over unrestricted temporal/spectral conditioning in the sense needed
by the frozen ledger.

More basically, (LA.15) is a **same-time spatial doubling/observability**
statement.  R0.75A starts with a positive-volume endpoint witness and asks for
backward spacetime residence in a moving enlarged strip.  Turning (LA.15)
into that statement would require additional temporal propagation and moving-
geometry estimates, followed by the shell-weighted cubic conversion.  The
paper provides none of those steps.  It supports the frozen warning that
global modal energy cannot be relabeled as favorable local payment without a
quantified geometry-dependent cost.  **Relevant caution, no direct closure.**

### 3.6 Phung--Wang, arXiv:1109.3863

Theorem 1.1 considers a bounded convex domain with homogeneous Dirichlet
boundary conditions and

\[
 u_t-\Delta u+a u+b\cdot\nabla u=0.
 \tag{LA.16}
\]

For a fixed nonempty open $\omega\subset\Omega$ and a measurable time set
$E\subset(0,T)$ of positive measure, it proves

\[
 \|u(T)\|_{L^2(\Omega)}
 \leq C_{\Omega,n,q,\omega,E,T,a,b}
 \int_{\omega\times E}|u|.
 \tag{LA.17}
\]

This is a true lower-order-drift and measurable-time neighbor.  Its geometry
is nevertheless a fixed product $\omega\times E$, not the moving nested
remote strip on a torus.  Its left side is global, and the boundary condition
and convex-domain Carleman geometry do not match the periodic problem.

The paper also exposes why merely invoking its theorem loses the frozen
constant.  Proposition 2.2 uses

\[
 \beta(r,T,\|b\|)=r^{-2}
 e^{2T(1+\|b\|_\infty^2)},
 \qquad
 K=1+A(T,\|a\|)+T\|b\|_\infty^2,
 \tag{LA.18}
\]

inside further exponential factors that also contain the inverse time gap.
Inserting the available uniform coefficient scale
$r\asymp R$, $T\asymp R^3$, and $\|b\|_\infty\lesssim R^{-2}$ into the
paper's stated bound permits a tracked cost as bad as
$\beta\lesssim R^{-2}e^{C/R}$.  The cited estimate therefore does not supply
the polynomial $CR^{-3}$ ledger.  Neither (LA.17) nor its proof includes the
Version-M weight or the exact $L^2\to L^3$ shell conversion.  **Operator adjacency,
but domain, motion, and constants are incompatible.**

### 3.7 Guevara--Phuc, arXiv:1702.00449

This paper is relevant only as local-energy/Caccioppoli adjacency.  For
suitable weak Navier--Stokes solutions it uses the standard local generalized
energy inequality

\[
 \begin{aligned}
 \int |u(t)|^2\phi+2\int|\nabla u|^2\phi
 \leq{}&\int |u|^2(\phi_t+\Delta\phi)\\
 &+\int (|u|^2+2p)u\cdot\nabla\phi,
 \end{aligned}
 \tag{LA.19}
\]

and proves local bounds on nested parabolic cylinders, including pressure in
negative Sobolev norms.  This confirms that testing a parabolic energy with a
nested cutoff, and paying derivatives of that cutoff, is standard local-
energy technology.

It does not directly imply R0.75A.  Its setting is a general suitable weak
solution with the nonlinear flux and pressure terms in (LA.19), whereas the
frozen family has an exact smooth passive scalar identity, pressure zero, and
a quadratic commutator $c\partial_z\phi+\Delta\phi$.  Its cylinders have
the parabolic time scale $r^2$; the frozen $R^3$ interval is selected by
the shear/cutoff balance.  The paper's $L^3$ quantities are standard
scale-invariant NSE quantities, not the shifted shell weight or the Version-M
payment.  Therefore it is a useful citation for method ancestry, not a
substitute theorem and not a route to arbitrary suitable weak solutions.

## 4. Claim-gap matrix

| frozen claim or proof component | closest inspected primary result | overlap | unresolved applicability gap | audit disposition |
|---|---|---|---|---|
| Endpoint energy on an inner set forces spacetime $L^2$ mass on a larger set with $R^3$ normalization | arXiv:1711.04279, local inner-ball/outer-ball theorem | Same nested-cutoff energy mechanism; its $T^{-1}+(r-r')^{-2}$ becomes $O(R^{-3})$ at $T\sim R^3$ | Pure heat, fixed balls, Euclidean domain; no residual shear drift, moving anisotropic strip, torus, or shell payment | **ADJACENT; not directly applicable. Citation requirement satisfied in bound main.** |
| Global final-state observability from a moving observation family | arXiv:2203.08469 | Abstract uncertainty+dissipation theorem; moving uniformly thick sets | Concrete elliptic operator has no spatially dependent coefficients; OU drift is linear; available cost $e^{C/T}$; target lift loses uniform thickness | **NOT APPLICABLE AS STATED.** |
| Moving support follows transport | arXiv:1908.10603 | Integral thickness along a linear resolvent and control sets moving with the OU flow | Frozen $Q_2$ follows one reference height, not the full nonlinear shear flow; torus and constants differ | **ADJACENT GEOMETRY; not directly applicable.** |
| Drift-compatible quantitative nonvanishing | arXiv:1711.06730 | Target scalar fits the lower-order drift equation formally | Point vanishing order, $M_1^2\sim R^{-4}$, and $q_0$-dependent constants do not yield tube residence | **ADJACENT OPERATOR; not directly applicable.** |
| Same-time local-to-global spatial control with drift | arXiv:2107.11698 | Periodic lower-order-drift setting and quantitative ball estimate | Exponential-of-polynomial small-scale cost; no moving-time persistence; hypotheses/constants do not furnish conditioning-uniform $CR^{-3}$ | **ADJACENT; not directly applicable.** |
| Observation on a positive-measure time set with drift | arXiv:1109.3863 | Lower-order drift and spacetime observation | Fixed product set, convex Dirichlet domain, global final state, and an available bound as bad as $\beta\lesssim R^{-2}e^{C/R}$ | **ADJACENT; constant unusable, so not directly applicable.** |
| Local energy/Caccioppoli mechanism for NSE | arXiv:1702.00449 | Nested cutoff and local energy bookkeeping | Suitable-weak inequality has pressure and cubic transport; fixed parabolic cylinders; no common-shear exact equality or Version-M weight | **ADJACENT METHOD; not directly applicable.** |
| Full-field treatment automatically retains correction interference and periodic windings | None of the screened theorems is needed | Frozen proof acts directly on total periodic $F$ | Literature theorems usually estimate a generic solution but do not encode the project's winding decomposition | **Internal exact feature; no literature claim.** |
| Hölder plus tube volume and $W_{2R}\geq\omega^{1/4}$ gives the precise payment exponents | No inspected paper | Hölder itself is standard | Shell identity, weight, $h_{\rm rem}$, and Version-M normalization are project-specific | **No direct collision found; no novelty inference.** |
| Complete-clock extraction, fixed deletion, or arbitrary suitable-weak-solution consequence | No inspected paper | None | These are expressly outside R0.75A | **Remain OPEN / NOT PROVED.** |

## 5. Framing compliance and safe statements

The following statements are supported by the bounded screen:

1. The frozen moving-cutoff identity and dichotomy do not need a spectral or
   Carleman observability theorem.
2. The bare inner-endpoint / outer-spacetime local-energy mechanism has clear
   primary-source precedent for the pure heat equation, especially
   arXiv:1711.04279, Section 3.2.
3. The cited global observability and quantitative-unique-continuation
   theorems do not directly give the frozen $R^{-3}$ constant for the moving
   common-shear strip.
4. The shell-weighted cubic step (LA.7) is not a standard output of those
   observability theorems; it must remain visibly derived from the Version-M
   definition, shell inclusion, tube volume, and Hölder.
5. “No frequency/geometry-uniform local observability constant” must be read
   as a denial of a constant uniform over the shrinking geometry and
   unrestricted conditioning relevant here.  It must not be read as denying
   fixed-geometry spectral observability with a possibly exploding cost.

The following stronger statements are **not** supported:

- that the cutoff argument or local $L^2$ persistence idea is novel;
- that the seven-paper screen establishes priority;
- that a cited observability theorem proves (LA.7) without the frozen local
  calculation;
- that R0.75A extends to arbitrary suitable weak solutions;
- that the remote witness controls the complete clock or proves fixed
  deletion.

The bound main note now implements the minimum literature addition immediately
after A.22.  It calls the calculation a moving-drift, anisotropic version of
the standard nested-cutoff local heat estimate, cites
Wang--Wang--Zhang--Zhang, arXiv:1711.04279, Section 3.2, and then states that
the cited pure-heat result does not cover the residual shear, moving periodic
strip, or subsequent Version-M weighted cubic payment.  That wording is
accurate and safely delimited.  It neither asserts novelty nor suggests that
the cited theorem proves the frozen extension.  arXiv:1702.00449 remains an
optional broader citation for NSE local-energy ancestry.  The remaining
papers are useful for explaining why generic observability or unique
continuation is not substituted for the exact cutoff ledger.

## 6. Final audit status

\[
\boxed{
\begin{gathered}
\textbf{DIRECT APPLICABILITY COLLISION IN SCREENED CORPUS: NONE;}\\
\textbf{CLOSE LOCAL-HEAT PRECEDENT: YES, arXiv:1711.04279;}\\
\textbf{MATHEMATICAL BLOCKERS FROM THIS SCREEN: 0;}\\
\textbf{CITATION/FRAMING REQUIREMENT: SATISFIED IN BOUND MAIN;}\\
\textbf{PRIORITY OR NOVELTY CONCLUSION: NOT MADE;}\\
\textbf{COMPLETE CLOCK / FIXED DELETION / REGULARITY: OPEN.}
\end{gathered}}
\tag{LA.20}
\]

This audit changes neither the frozen proof nor its stated boundary.
