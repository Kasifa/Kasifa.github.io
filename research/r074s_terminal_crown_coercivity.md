# R0.74S Step 15B — terminal crowns and the missing nonlinear dissipation charge

## 0. Result, status, and scope

Step 14 left the top-boundary and low-transition-corona rows in the open
jump--corona statement (S.375).  This note gives a precise way to avoid
counting every node of a corona.  It also proves that the presently frozen
linear ledgers and positive-measure tree facts cannot provide the remaining
estimate.

There are four conclusions.

1. After unfolding, countably many forest tops and all their overlaps can be
   handled by a measurable ownership partition, separately for each shell.
   The mass of every periodic copy remains in the unfolded incidences, and
   every repeated top occurrence remains visible in the incidence sums.
2. First density roots followed by first relative density jumps define
   pairwise disjoint terminal crowns.  Each crown is charged once, rather
   than once at every dyadic generation.  If the forest tops are at the
   single-lift incidence scale, the exact jump-radius estimate gives a
   uniform cubic coefficient budget.
3. The top and corona terms therefore reduce to one concrete PDE input: a
   selected-crown \(3/2\)-coercivity estimate.  Conditional on that estimate,
   the full top-plus-corona ancestor mass is bounded at the quadratic scale
   \(A_R=(P_R^M)^{2/3}\).  This implication is proved; the coercivity estimate
   is **OPEN** for the bare suitable-weak class.
4. A periodic lifted measure fixture and the already verified pure-defect
   scalar clocks separately pass the geometric and scalar stress tests.
   Independently, a converse-Hölder argument proves a formal-ledger
   obstruction.  For any
   adaptive forest, any topwise levels, one common fixed shell deletion, and
   the full repeated incidence multiset, either the \(q\)-budget or the cubic
   coefficient budget must diverge if only a linear payment is available.
   This is an **ABSTRACT METHOD OBSTRUCTION**, not a Navier--Stokes
   counterexample.

This note does not prove (S.375), (S.288), (S.303), (S.272), Q.12, Q.1,
scale contraction, regularity, singularity formation, or the Millennium
problem.  It does not modify any frozen Step 14 artifact.  **NOT CLAY.**

## 1. The selected ancestor as a shellwise submeasure

Fix a Version-M suitable weak solution, an admissible scale \(R\), and a
good terminal time \(\tau\).  Let
\(\nu_R=\nu_R^{\rm vis}+\nu_R^{\rm def}\) be the dimensionless comoving
pullback of the viscous and anomalous parts of the total local-dissipation
measure from (S.360).  If
\(\Phi_R\) is the map in (S.360), define the dimensionless tube
\[
 \widehat{\mathcal U}_{k,R}(\tau)
 :=\Phi_R^{-1}\bigl(\mathcal U_{k,R}(\tau)\bigr).
\]
Let \(\widehat\eta_R=\eta_R\circ\operatorname{pr}_t\circ\Phi_R\), let
\(\widehat\psi_{k,R}\) be the pulled-back unperiodized shell cutoff, and
let \(\widehat H_{k,R}=\Phi_R^{-1}(H_{k,R}\times\mathbb R^3)\).  The Step
12 ancestor coordinate is represented by the finite positive Borel measure

\[
 d\alpha^{\rm anc}_{k,\tau}
 :=\mathbf1_{\mathcal I_x(\tau)}(k)\,\gamma_k
   \mathbf1_{\widehat{\mathcal U}_{k,R}(\tau)}
   \widehat\eta_R\widehat\psi_{k,R}
   \left(d\nu_R^{\rm def}
       +\mathbf1_{\widehat H_{k,R}}d\nu_R^{\rm vis}\right).
\]

Consequently,

\[
 \boxed{
 \begin{aligned}
  b_k(\tau)&=\alpha^{\rm anc}_{k,\tau}
       (\mathbb R\times\mathbb R^3),\\
  0\le d\alpha^{\rm anc}_{k,\tau}&\le
      \gamma_k\mathbf 1_{\widehat{\mathcal U}_{k,R}(\tau)}\,d\nu_R.
 \end{aligned}}
 \tag{S.398}
\]

The two pulled-back cutoff factors lie in \([0,1]\).  Thus the equality in
(S.398) is the inherited definition, including the common selected-shell
mask and the high-Rayleigh restriction; its second line is the resulting
domination.  The factors \(R^{-1}\) and \(\gamma_k\) are already explicit
in (S.360) and the display above, so no scale factor is hidden.  This does
not introduce a new PDE estimate.

Let \(\mathscr T\) be a finite or countable, locally finite family of
half-open forest-top occurrences, drawn from finitely many shifted
parabolic dyadic grids, and covering every dimensionless lifted tube.  An occurrence
retains its grid, lattice-copy, and top labels even when its underlying set
coincides with another occurrence.  For each shell \(k\), enumerate all top
occurrences meeting \(\widehat{\mathcal U}_{k,R}(\tau)\) and choose Borel ownership
sets \(\mathcal O_{Tk}\) such that

\[
 \boxed{
  \widehat{\mathcal U}_{k,R}(\tau)
   =\mathop{\dot\bigcup}_{T:(T,k)\in\mathscr I_{\rm top}}
      \mathcal O_{Tk},
  \qquad
  \mathcal O_{Tk}\subset T\cap\widehat{\mathcal U}_{k,R}(\tau).
 }
 \tag{S.399}
\]

One construction assigns a point to the first top occurrence containing
it.  The partition is made separately for every shell.  Hence an overlap of
two adjacent shell supports remains two shell incidences, while an overlap
of forest tops does not duplicate the ancestor mass.  If an argument
deliberately uses the same owned piece more than once, each use is a new
incidence occurrence and must carry a repeated payment.

Assume from now on that every top has dimensionless spatial diameter at
most \(2\), equivalently physical diameter at most \(2R\).  Larger
preliminary tops may be split before (S.399).  Step 14
(S.371) then shows that a single unperiodized top, and every descendant of
that top, meets at most two shell supports.  For a finite or countable
incidence multiset \(\mathscr A\) of triples \((Q,T,k)\), define
\[
 \operatorname {Cont}_{1,\gamma}(\mathscr A)
 :=\sum_{(Q,T,k)\in\mathscr A}\gamma_k\rho_Q,
\]
where geometrically equal cells with different occurrence labels are
summed with multiplicity.  The incidence-weighted top one-content is

\[
 \boxed{
  \mathscr C_{\rm top}
  :=\sum_{(T,k)\in\mathscr I_{\rm top}}\gamma_k\rho_T.
 }
 \tag{S.400}
\]

The results below apply to every forest with
\(\mathscr C_{\rm top}<\infty\), and have a forest-independent constant
when \(\mathscr C_{\rm top}\le C_0\) for one fixed \(C_0\).  For the
canonical bounded-overlap unit-radius lifted cover,
\(\#\{T:T\rightsquigarrow k\}\le C_{\rm geo}2^{3k}\).  Consequently

\[
 \mathscr C_{\rm top}
 \le C_{\rm geo}\sum_{k\ge1}2^{3k}\gamma_k
 =C_{\rm geo}\mathscr A_3<\infty.
\]

The constant includes the finite shifted-grid multiplicity and bounded top
multiplicity.  Arbitrarily repeating a top increases
\(\mathscr C_{\rm top}\); it is not hidden in \(C_{\rm geo}\).  The
periodic lifted measure is integrated in full inside these tops, with no
quotient or discarded copy.

## 2. First roots, jump nodes, and terminal crowns

For a top \(T\) with \(m_T:=\nu_R(T)>0\), choose the canonical top level

\[
 \lambda_T:=\Theta(T)={m_T\over\rho_T}.
\]

For \(m_T=0\), discard the top from the measure decomposition.  Since the
top is not strictly above its own level, the first
\(\lambda_T\)-crossing roots \(\mathscr R(T)\) satisfy the Step 14 estimate

\[
 \boxed{
  \sum_{S\in\mathscr R(T)}\rho_S
  \le{m_T\over\lambda_T}=\rho_T.
 }
 \tag{S.401}
\]

Starting from every \(S\in\mathscr R(T)\), iterate the first proper
\(\kappa\)-jump descendants, with one fixed \(\kappa>1\).  Denote the
resulting generation-\(j\) family by \(\mathscr J_j(T)\), where
\(\mathscr J_0(T)=\mathscr R(T)\), and recursively take the disjoint union

\[
 \mathscr J_{j+1}(T)
 :=\mathop{\dot\bigcup}_{S\in\mathscr J_j(T)}\mathscr J_\kappa(S).
\]

All cells use the same half-open convention, so these countable families
and the crowns below are Borel.  The first-jump estimate (S.366) gives

\[
 \boxed{
 \begin{aligned}
  \sum_{S\in\mathscr J_j(T)}\rho_S
   &\le\kappa^{-j}\rho_T,\\
  \sum_{j\ge0}\sum_{S\in\mathscr J_j(T)}\rho_S
   &\le {\kappa\over\kappa-1}\rho_T.
 \end{aligned}}
 \tag{S.402}
\]

For a finite stopping depth \(L\), form the following half-open pieces.
The top crown is

\[
 \Omega_T:=T\setminus\bigcup_{S\in\mathscr R(T)}S.
\]

For \(S\in\mathscr J_j(T)\), \(j<L\), put

\[
 \Omega_S:=S\setminus
       \bigcup_{Q\in\mathscr J_\kappa(S)}Q,
\]

and for \(S\in\mathscr J_L(T)\), put \(\Omega_S:=S\).  The half-open child
convention and first-crossing antichains imply the exact partition

\[
 \boxed{
  T=\Omega_T\mathbin{\dot\cup}
    \mathop{\dot\bigcup}_{0\le j\le L}
      \mathop{\dot\bigcup}_{S\in\mathscr J_j(T)}\Omega_S.
 }
 \tag{S.403}
\]

Thus a low-transition corona is not summed over all of its dyadic nodes.
It is one crown \(\Omega_S\), and it is counted once.  Formula (S.403) is
valid at every finite depth.  More precisely, the union of the finalized
crowns through generation \(L-1\) increases with \(L\), while
\(\bigcup_{S\in\mathscr J_L(T)}S\) is the decreasing terminal remainder.
Their limiting intersection is the infinite-jump set.  Its mass must be
retained in a terminal-depth crown, assigned to the jump row, or stated as
a separate remainder; it cannot be discarded.  Working at one finite
\(L\), with constants independent of \(L\), avoids an unrecorded
zero-radius remainder.

Let \(\mathscr C_L\) be the multiset of all owned crown--shell occurrences
\((\Omega_S,T,k)\), including the top crown \(S=T\).  Equations
(S.400)--(S.402) give the uniform coefficient-content bound

\[
 \boxed{
 \begin{aligned}
  \sum_{(\Omega_S,T,k)\in\mathscr C_L}\gamma_k\rho_S
  &\le C_{\kappa,L}\mathscr C_{\rm top}
   \le C_\kappa\mathscr C_{\rm top},\\
  C_{\kappa,L}&:=1+\sum_{j=0}^{L}\kappa^{-j}
   =1+{\kappa\over\kappa-1}
       \bigl(1-\kappa^{-(L+1)}\bigr),\\
  C_\kappa&:=1+{\kappa\over\kappa-1}
           ={2\kappa-1\over\kappa-1}.
 \end{aligned}}
 \tag{S.404}
\]

Every shifted-grid occurrence, periodic copy, adjacent-shell incidence,
and forest-top repetition is present on both sides.  The estimate uses
only that a descendant incident to \(k\) has an incident top ancestor and
that (S.402) holds separately below each top occurrence.  It does not use or
assert a payment estimate.

## 3. A proved terminal-crown reduction

Fix one shell exception set \(E_\tau\), with
\(\#E_\tau\le N_b\), before splitting any top or crown channel.  This is
the same set for the defect and high-Rayleigh parts, for all tops, and for
every crown generation.  For every
owned crown occurrence and every \(k\notin E_\tau\), set

\[
 a_{Sk}:=\alpha^{\rm anc}_{k,\tau}
       (\mathcal O_{Tk}\cap\Omega_S),
 \qquad
 \mathscr C_L(E_\tau):=
   \{(\Omega_S,T,k)\in\mathscr C_L:k\notin E_\tau\}.
\]

Suppose that the PDE supplies a nonnegative split

\[
 \boxed{
  a_{Sk}=q_{Sk}+a_{Sk}^{\rm pay},
  \qquad
  \sum_{(S,T,k)\in\mathscr C_L(E_\tau)}q_{Sk}\le C_qA_R.
 }
 \tag{S.405}
\]

The split itself carries no hidden existence issue: \(q_{Sk}=0\) is always
allowed.  Its purpose is to permit a part already controlled at the
quadratic scale to be removed before testing the nonlinear paid part.

Attach to the paid part the canonical crown payment

\[
 \boxed{
 \begin{aligned}
  p_{Sk}^{\rm crown}
   &:={\bigl(a_{Sk}^{\rm pay}\bigr)^{3/2}
        \over(\gamma_k\rho_S)^{1/2}},\\
  {\bigl(a_{Sk}^{\rm pay}\bigr)^3
        \over\bigl(p_{Sk}^{\rm crown}\bigr)^2}
   &=\gamma_k\rho_S\,
       \mathbf1_{\{a_{Sk}^{\rm pay}>0\}}
     \le\gamma_k\rho_S,
 \end{aligned}}
 \tag{S.406}
\]

with \(p=0\) when \(a^{\rm pay}=0\), and with the zero-over-zero convention
following (S.356).  The identity on the positive support is exact.  It identifies
the following single new PDE statement:

\[
 \boxed{
  \sum_{(S,T,k)\in\mathscr C_L(E_\tau)}p_{Sk}^{\rm crown}
  =\sum_{(S,T,k)\in\mathscr C_L(E_\tau)}
    {\bigl(a_{Sk}^{\rm pay}\bigr)^{3/2}
        \over(\gamma_k\rho_S)^{1/2}}
  \le C_pP_R^M.
  \qquad\textbf{OPEN}
 }
 \tag{S.407}
\]

The proposed PDE theorem has the following quantifier order: for every
solution, \(R\), and good \(\tau\), there must exist an admissible forest,
one common exception set, a split, and one finite stopping depth \(L\) for
which (S.407) holds.  The same universal \(C_p\) is independent of every
object produced by that construction, including the depth, number of tops,
and top levels.  It may depend only on
the frozen cutoffs, fixed grid multiplicity, and fixed \(\kappa\).  The
same frozen payment
may not be reused for different occurrences unless it is repeated in the
sum.  Formula (S.407) is a shell-selective reverse-Caccioppoli or nonlinear
dissipation-coercivity requirement.  It is not a consequence of the local
energy inequality established in this note.

### Proposition 3.1 — terminal-crown closure

If (S.400), (S.405), and (S.407) hold, then

\[
 \boxed{
 \begin{aligned}
  \mathcal S_{N_b}(b(\tau))
  &\le C_qA_R
   +\bigl(C_\kappa\mathscr C_{\rm top}\bigr)^{1/3}
      \bigl(C_pP_R^M\bigr)^{2/3}\\
  &=\left[C_q+
     \bigl(C_\kappa\mathscr C_{\rm top}\bigr)^{1/3}
       C_p^{2/3}\right]A_R.
 \end{aligned}}
 \tag{S.408}
\]

**Proof.**  The ownership partition and (S.403) give

\[
 \sum_{k\notin E_\tau}b_k
 =\sum_{(S,T,k)\in\mathscr C_L(E_\tau)}a_{Sk}.
\]

Insert (S.405).  Hölder on the complete crown-incidence multiset, followed
by (S.404), (S.406), and (S.407), bounds the paid sum by

\[
 \left(\sum\gamma_k\rho_S\right)^{1/3}
 \left(\sum p_{Sk}^{\rm crown}\right)^{2/3}.
\]

Finally, test \(E_\tau\) in the definition of
\(\mathcal S_{N_b}\).  For a countable forest, apply the finite argument
to increasing finite incidence subsets and use monotone convergence.  The
case \(P_R^M=0\) follows directly from (S.406)--(S.407).  No selector is
integrated in time.  \(\square\)

Proposition 3.1 is stronger bookkeeping than a nodewise corona sum: it
includes the top boundary as the top crown, counts every low-transition
crown only once, and uses one common shell exception.  It does not prove
the open antecedent (S.407).

## 4. Exact converse Hölder and the flat lower-plateau obstruction

The coercivity in (S.407) cannot be replaced by the current linear payment
ledger at the level of abstract nonnegative data.  The exact reason is the
following converse to the Hölder step.  For a finite or countable family of
nonnegative \(a_i,p_i\), with
\(A=\sum_i a_i\in(0,\infty)\) and
\(P=\sum_i p_i\in(0,\infty)\),

\[
 \boxed{
  \sum_i{a_i^3\over p_i^2}\ge{A^3\over P^2},
  \qquad
  \inf_{p_i\ge0,\ \sum p_i=P}
       \sum_i{a_i^3\over p_i^2}={A^3\over P^2}.
 }
 \tag{S.409}
\]

The zero convention is the one used after (S.356).  Equality holds exactly
when \(p_i=(P/A)a_i\) on every coordinate, including zero coordinates.
Formula (S.409) is Hölder rearranged.  The countable statement follows by
finite truncation and monotone convergence, and the proportional assignment
attains the infimum.

Fix any proposed universal shell budget \(N_b\), set \(M=N_b+1\), and let
\(H>0\).  On \(M\) distinct shells impose the lower plateau

\[
 \boxed{
  b_{k_i}\ge H\quad(1\le i\le M),
  \qquad P_H=C_MH,
  \qquad A_H=(C_MH)^{2/3},
 }
 \tag{S.410}
\]

where \(C_M<\infty\) is fixed independently of \(H\).  It may depend on
the fixed \(M\), chosen shell indices, and the fixed test scale \(R\), but
not on the amplitude \(H\).  Its value may include all lifted periodic
copies and all linear scalar-clock payments.
Every common exception set of size at most \(N_b\) leaves

\[
 B_E:=\sum_{k\notin E}b_k\ge H.
\]

The quantifier is universal.  For each \(H\), the forest, shifted grids,
topwise levels \(\lambda_T\), finite stopping depths, assignments, and the
single exception set \(E\) may all be chosen adaptively after seeing the
data.  Consider any resulting finite or countable decomposition of the
form (S.356)--(S.357).  All repeated occurrences and their payments are
included in its incidence multiset.  If

\[
 \sum q_k\le C_qA_H,
 \qquad
 \sum p_i\le C_pP_H,
\]

then, whenever \(H\ge(2C_qC_M^{2/3})^3\), the total incidence mass is at
least \(H/2\).  Formula (S.409) forces

\[
 \boxed{
  \sum_i{a_i^3\over p_i^2}
  \ge {H\over8C_p^2C_M^2}.
 }
 \tag{S.411}
\]

Equivalently, if the cubic coefficient sum is bounded by a fixed
\(C_{\rm cor}\), then every such decomposition obeys the exact tradeoff

\[
 \boxed{
  \sum q_k
  \ge H-C_{\rm cor}^{1/3}(C_pC_MH)^{2/3}.
 }
 \tag{S.412}
\]

Thus either the normalized \(q\)-budget or the cubic coefficient budget
diverges like a positive power of \(H\).  The number \(M=N_b+1\) is the
minimal number of equal positive shell coordinates that defeats every
deletion of at most \(N_b\) coordinates.  This conclusion is independent of
the forest and of all density-level choices.  Repeating a node without
repeating its payment would evade (S.411) only by violating the incidence
convention already required in (S.375).

## 5. Separate periodic-measure and selected-clock stress tests

The lower-plateau vector in (S.410) admits two separate compatibility checks: a
periodic positive-measure tree with arbitrarily deep coronas, and a
selected scalar clock with the required one-shell arithmetic.  They are
not asserted to satisfy one common completed-clock/measure identity.  This
subsection records the two stress tests without coupling them into a
Navier--Stokes solution or into one complete frozen ledger fixture.

Choose separated indices \(k_1,\ldots,k_M\) and then choose \(R>0\) so
small that \(M\) disjoint physical \(R\)-scale dyadic cells fit strictly
inside the plateau regions of the corresponding central lifted shell
supports, before the first spatial period is reached.  In dimensionless
coordinates, let their spatial cubes be \(Q_i^x\), choose one common
interior time \(\sigma_*\), and set

\[
 \boxed{
  d\nu_H(\sigma,z)
  :=\sum_{n\in\mathbb Z^3}\sum_{i=1}^M
    {H\over\gamma_{k_i}}
    \delta_{\sigma_*}(d\sigma)
    {|Q_i^x|^{-1}\mathbf1_{Q_i^x+(2\pi/R)n}(z)\,dz}.
 }
 \tag{S.413}
\]

This is a periodic, locally finite positive measure.  In the standard grid,
the temporal atom selects one of four temporal children and the spatial
Lebesgue factor splits equally among the eight spatial children.  Along
every retained child,

\[
 \boxed{
  \rho_v=2^{-d}\rho_0,
  \qquad m_v=8^{-d}m_0,
  \qquad\Theta(v)=4^{-d}\Theta(0).
 }
 \tag{S.414}
\]

Hence this forest has no proper upward \(\kappa\)-jump, for any
\(\kappa>1\), and it contains arbitrarily deep low-transition coronas.  Each
target central cell contributes exactly \(H\) after multiplication by
\(\gamma_{k_i}\).  Other periodic copies contribute only nonnegative
leakage.  Their complete weighted sum is finite because the number of
lattice copies in shell \(k\) is bounded by
\(C_R(1+2^{3k}R^3)\) and

\[
 \sum_{k\ge1}\gamma_k(1+2^{3k}R^3)<\infty.
\]

Thus all copies can be absorbed in the finite constant \(C_M\) in
(S.410); none is silently quotiented out.

For scalar-clock compatibility, scale the pure-defect Step 11 fixture
(S.266) by \(s=5H/3\).  On every target shell it gives

\[
 \boxed{
  T={5H\over3},\qquad b=m=H,\qquad
  r^x={5H\over9},\qquad
  \sigma={959H\over7200}<{T\over12},\qquad
  x={2641H\over3600}>{T\over6},\qquad\beta=0.
 }
 \tag{S.415}
\]

Every row lies strictly in the selected excess class and has a linear
absolute-flux ledger.  Enlarge the fixed \(C_M\), if necessary, to the
maximum of the separate periodic-measure and scalar-clock linear constants.
Taking \(M\) scalar copies is then bounded by the comparison budget
\(P_H=C_MH\), while

\[
 \boxed{
  {\mathcal S_{N_b}(b)\over A_H}
  \ge {H\over(C_MH)^{2/3}}
  =C_M^{-2/3}H^{1/3}\longrightarrow\infty.
 }
 \tag{S.416}
\]

The measure and clocks have not been coupled even at the completed-clock
ledger level, much less realized by one velocity and pressure satisfying
the Navier--Stokes momentum equation.  Hence (S.413)--(S.416) do not refute
(S.375), and their juxtaposition does not prove simultaneous compatibility
with every frozen ledger.  The forest stress test shows that the geometric
facts alone leave arbitrarily deep coronas; the clock stress test shows that
the selected scalar algebra alone permits the flat best-\(N\) scaling.  The
formal converse-Hölder obstruction (S.409)--(S.412) is independent of this
uncoupled juxtaposition.

The formal sequence-space calculation is genuinely stronger than either
earlier calculation alone.
Equation (S.365) showed only that one first-root density level cancels in a
critical Hölder product.  Equation (S.370) showed only coefficient-cube
conservation down one abstract corona.  Equations (S.409)--(S.416) add the
fixed best-\(N\) quantifier, arbitrary adaptive forest and top-level choices,
one common exception set, full periodic-copy accounting, repeated-incidence
payment, the exact equality case, and a lower bound on the budget that must
fail.

## 6. Relation to the hybrid-start route

The terminal-crown theorem is not needed if a separate signed flux theorem
closes both residual branches directly through (S.342).  Its role is exact:
if the ancestor route through (S.375) is retained, (S.404) closes the cubic
coefficient side for all finite-depth top and low-transition crowns, while
(S.407) is the only new occurrence-level PDE charge required for their paid
mass.  A quadratic \(q\)-split is allowed in (S.405).  Infinite-jump mass is
included in the last finite-depth crown and cannot be lost in a limit.

Accordingly, this result does not claim that the entire Step 15 route must
pass through (S.375).  It identifies the exact remaining burden conditional
on choosing that ancestor route.

## 7. The next PDE input

The smallest positive target exposed by Proposition 3.1 is not another
density threshold.  It is the following shell-selective statement.

> After one common fixed shell deletion, decompose every owned terminal
> crown mass into a quadratic \(q\)-part and a paid part so that the \(q\)
> masses sum to \(O(A_R)\) and the canonical crown payments in (S.407) sum
> to \(O(P_R^M)\), uniformly over a finite stopping depth.

There are two plausible analytic tests for this target.

1. Apply the defect-completed local-energy balance to the union of each
   crown rather than to every dyadic cell.  Internal time and spatial faces
   must cancel before absolute values are taken.  The remaining top,
   stopping, pressure, and moving-frame drift faces must then be matched to
   the same occurrence-level payment used in (S.407).
2. Split anomalous and viscous crown mass.  Any reverse Hölder estimate for
   the viscous part must have constants controlled by the frozen payment,
   not by a separate local kinetic-energy Morrey norm.  The anomalous
   infinite-jump remainder must be charged explicitly; a support-dimension
   statement alone is insufficient.

A failure of (S.407) for a future exact NSE family would be decisive only if
that family also realizes \(N_b+1\) selected shell coordinates after the
\(Q\), pressure, cubic, drift, and defect ledgers are all computed.  The
abstract fixture above does not do this.

## 8. Bounded primary-source collision boundary

The following primary sources are relevant to the proposed input, but none
supplies (S.407) with the frozen quantifiers.

| Primary result | Established scope | Boundary here |
|---|---|---|
| J. Yang, [*Construction of maximal functions associated with skewed cylinders generated by incompressible flows and applications*](https://doi.org/10.4171/AIHPC/20) | Weak-\((1,1)\), strong-\((p,p)\), and covering estimates for mollified-flow cylinders | It helps construct and count moving tops; it does not give the selected-crown \(3/2\) payment. |
| H. J. Choe, M. Yang, [*Local kinetic energy and singularities of the incompressible Navier--Stokes equations*](https://doi.org/10.1016/j.jde.2017.09.036) | A reverse Hölder estimate for the velocity gradient under a uniformly bounded scaled local-kinetic-energy functional | The extra uniform kinetic bound is not controlled by the frozen \(P_R^M\) ledger. |
| L. De Rosa, T. D. Drivas, M. Inversi, [*On the Support of Anomalous Dissipation Measures*](https://doi.org/10.1007/s00021-024-00894-z) | Density and support conclusions under stated \(L_t^qL_x^r\) assumptions; finite-\(q\) bounds use an absolute-continuity modulus | It does not give a uniform payment-controlled crown coercivity in the bare energy class. |
| Z. Lei, X. Ren, [*Quantitative partial regularity of the Navier--Stokes equations and applications*](https://doi.org/10.1016/j.aim.2024.109654) | Quantitative scale selection through non-overlapping dissipation layers and energy-dependent pigeonholing | Its selected scales do not yield one fixed shell deletion or the occurrence-level nonlinear payment in (S.407). |
| W. S. Ożański, [*Weak solutions to the Navier--Stokes inequality with arbitrary energy profiles*](https://arxiv.org/abs/1809.02109) | Flexibility for fields satisfying strong and local energy inequalities, but not necessarily the NSE momentum equation | It supports only the warning that energy inequalities alone are too flexible; it is not an NSE counterexample. |

This is a bounded collision search, not an exhaustive review or a novelty
claim.  Useful search keys for the next pass are:

- suitable weak Navier-Stokes reverse Hölder dissipation moving cylinder;
- local energy defect measure good lambda stopping time corona;
- skewed cylinder Carleson packing mollified flow dissipation;
- quantitative absolute continuity dissipation energy annular layers;
- local energy balance sawtooth region pressure boundary cancellation; and
- Navier-Stokes defect measure atoms parabolic density.

## 9. Validator design and claim ledger

A finite primary certificate should check:

1. exact first-root and generationwise jump-radius sums for rational
   \(\kappa>1\), followed by the depth-independent constant
   \(C_\kappa=(2\kappa-1)/(\kappa-1)\);
2. exact half-open crown partitions on all finite 32-child trees up to a
   fixed depth, including boundary atoms;
3. shellwise ownership under overlapping tops, adjacent shells, shifted
   grids, and explicitly enumerated periodic-copy occurrences;
4. the cubed identity on the positive paid support,
   \((a^{\rm pay})^3=(p^{\rm crown})^2\gamma_k\rho_S\), together with
   the zero-support convention, avoiding a floating-point square-root test;
5. Proposition 3.1 on exhaustive rational finite fixtures;
6. the converse lower bound (S.409), its equality assignment
   \(p_i=Pa_i/A\), and the threshold arithmetic in (S.411)--(S.412);
7. the scaled pure-defect constants in (S.415); and
8. negative mutations that omit a periodic copy, collapse occurrences to
   distinct nodes, reuse payment, change the common exception set between
   channels, discard a terminal-depth crown, or replace
   \(C_\kappa\) by a depth-dependent constant.

An independent implementation should use a different language and generate
the tree, ownership, and incidence multisets from first principles.  The
main-note hash, Step 11--14 hashes, equation sequence, display balance,
claim-boundary phrases, and wrong-path overrides should be locked.

The following are **PROVED** in this note:

- the shellwise ancestor submeasure representation and ownership mechanism
  (S.398)--(S.399);
- the first-root, jump-radius, terminal-crown, and weighted coefficient
  estimates (S.401)--(S.404);
- the exact canonical crown factorization and the conditional closure
  (S.405)--(S.408);
- the converse-Hölder minimum and equality case (S.409);
- the budget lower bounds (S.411)--(S.412), for every formal incidence
  decomposition of the stated flat data; and
- the periodic lifted measure geometry and scalar-clock arithmetic
  (S.413)--(S.416), only as two separate abstract stress tests.

The following is an **OPEN PDE INPUT**:

- the selected-crown nonlinear payment estimate (S.407), including signed
  top/stopping-face cancellation, pressure, moving drift, and any
  infinite-jump remainder.

The following is an **ABSTRACT METHOD OBSTRUCTION, NOT AN NSE
COUNTEREXAMPLE**:

- the formal flat-data obstruction (S.409)--(S.412); the two separate
  stress tests (S.413)--(S.416) are supporting screens, not a coupled
  obstruction fixture.

The following remain **OPEN**:

- (S.375), (S.288), (S.303), (S.272), Q.12, and Q.1;
- a coupled completed-clock/measure realization of the two stress tests,
  let alone a velocity-pressure realization satisfying Navier--Stokes;
- a uniform bound for anomalous infinite-jump mass;
- the common-deletion short-tail gate (S.342); and
- scale contraction, regularity, singularity formation, and the
  Navier--Stokes Millennium problem.

The useful advance is a sharper proof obligation.  Density stopping already
supplies the cubic coefficient side once terminal crowns are counted only
once.  The unresolved information is exactly the nonlinear relation between
selected dissipation mass and the frozen physical payment.  **NOT CLAY.**
