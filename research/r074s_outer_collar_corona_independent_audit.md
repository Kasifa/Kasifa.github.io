# R0.74S Step 14 — independent adversarial audit

## 0. Frozen object and final verdict

The audited note is
`research/r074s_outer_collar_corona_obstruction.md`, with SHA-256

`c843284d68c0d7d441214b0b3e67e97ca4c5ebda5f527a957eb6e9bdc07f55f9`.

**Final verdict: PASS within the stated analytic, conditional, and abstract
scope.**

The first read-only pass returned **FAIL**.  The local calculations were
correct, but the proposed jump--corona statement was not yet a closed
mathematical proposition: its density level was unquantified, one local
root cell did not cover the unbounded lifted shell family, and the shell
incidence claim had not explicitly distinguished an unfolded Euclidean
support from a periodized torus support.  The critical-corona paragraph
also asserted a compatible decreasing density without displaying the
measure assignment.  Finally, the fixed-index tail and the best-
\(K\)-deletion functional used one display in a way that obscured their
different meanings.

The main note was revised by its author.  The final read-only pass checked
the repairs and reconstructed every formula below.  This audit did not
modify the main note or either certificate program.

## 1. Shell cutoffs, pressure split, and flux normalization

For \(\rho_k=2^kR\), differentiating the two cutoff factors places the
gradient in

\[
 (\rho_k-R/8,\rho_k)
 \quad\hbox{or}\quad
 (2\rho_k,2\rho_k+R/8).
\]

Both collars lie in \(B_{3\rho_k}\).  Since
\(\zeta_{\rho_k}=1\) on that ball, the pressure Poisson identity gives

\[
 -\Delta\bigl(\widetilde\pi_R-p_{k,R}^{\rm loc}\bigr)=0
 \quad\hbox{in }B_{3\rho_k}.
\]

Thus (S.344) has a legitimate smooth harmonic representative on the
neighborhood of the derivative collars.  Subtracting the fixed spatial
constant \(c_R(t)\) preserves harmonicity, and

\[
 \int_{\mathbb R^3}c_R(t)\widetilde v_R\cdot\nabla\psi_k^R=0
\]

follows from distributional incompressibility and compact support.  The
local pressure decomposition therefore does not change the inherited
pressure gauge or the signed flux.

The four rows in (S.346) add exactly to the physical flux derivative.
Under \(t=s_R+R^2\sigma\), multiplication by \(R^2\) changes the original
\(\gamma_k/R\) prefactor into \(\gamma_kR\).  Hence the normalization in
(S.347) is correct; replacing it by a bare \(\gamma_k\) is valid only
after using \(R|\nabla\psi_k^R|\le C\).

## 2. Independent reconstruction of the component payment

For the local pressure row, spatial Young and Calderon--Zygmund give, at
almost every time,

\[
 \int_{B_{3\rho_k}}|p_{k,R}^{\rm loc}|\,|\widetilde v_R|
 \le C\int_{B_{4\rho_k}}|\widetilde v_R|^3.
\]

The time change and gradient bound contribute \(R^{-2}\), not
\(R^{-1}\) or \(R^{-3}\).  If
\(y\in A_j(2R)\) outside the core, the condition
\(y\in B_{4\rho_k}\) forces \(k\ge j\).  Super-Gaussian summability then
gives

\[
 \sum_{k:y\in B_{4\rho_k}}\gamma_k
 \le C\bigl(\mathbf1_{B_{8R}}(y)+W_{2R}(y)\bigr).
\]

This pays the local row by the core and exterior cubic ledgers.  The
inequality

\[
 |h_{k,R}^{\rm pr}-c_R|\,|\widetilde v_R|
 \le |\widetilde\pi_R-c_R|\,|\widetilde v_R|
    +|p_{k,R}^{\rm loc}|\,|\widetilde v_R|
\]

pays the harmonic row without a gauge change.  The cubic row is direct,
and Jensen--Young pays the Version-M drift by the same local-plus-exterior
cubic ledger.  This reconstructs

\[
 \sum_{k,\alpha}\|\widehat h_{k,R}^{\alpha}\|_{L^1(0,4)}
 \le CP_R^M.
\]

It is an \(L_t^1\), linear-payment estimate.  It does not imply uniform
\(L_t^p\) control for any \(p>1\), and the note does not claim otherwise.

## 3. Fixed-scale tail, collar indices, and smooth spikes

The revised (S.349) correctly separates

\[
 \mathfrak H^F_{4/3,K,R}
 =\inf_{\#S\le K}\sum_{k\notin S}\|h_{k,R}\|_{4/3}
\]

from the fixed-index tail

\[
 \mathfrak T^F_{4/3,K,R}
 =\sum_{k>K}\|h_{k,R}\|_{4/3}.
\]

Choosing \(S=\{1,\ldots,K\}\) gives
\(\mathfrak H\le\mathfrak T\), and the Step 13 envelope gives the second
inequality in (S.349).  The super-Gaussian coefficient tail tends to zero,
but the energy bracket is solution- and scale-dependent.  The conclusion
is therefore only fixed-solution, fixed-scale convergence.

The doubled-radius annuli satisfy

\[
 C_{k,R}^+\subset A_k(2R),\qquad
 C_{k,R}^-\subset A_{k-2}(2R)\quad(k\ge3).
\]

Consequently,

\[
 {\gamma_k\over\gamma_{k-2}}
 =\exp\!\left(-{15\,4^{k-3}\over32}\right),
 \qquad
 {\gamma_k\over\gamma_k}=1.
\]

The outer collar is genuinely coefficient-aligned with its payment
annulus, while the inner collar has the stated gain.

For the abstract spike, all \(N+1\) target coordinates equal
\((P/(N+1))\phi_d\).  Deleting at most \(N\) coordinates leaves exactly
one in the minimizing configuration, and

\[
 \inf_{\#S\le N}\sum_{i\notin S}\|H_i\|_p
 ={P\over N+1}\|\phi\|_p d^{1/p-1}.
\]

This diverges as \(d\downarrow0\) for every fixed
\(p\in(1,\infty]\), fixed \(P>0\), and fixed deletion budget.  The
construction is correctly labeled an abstract obstruction to an
\(L^1\)-only inference, not a Navier--Stokes counterexample.

## 4. Incidence Holder theorem and cubic duality

On the incidence multiset, Holder with exponents \(3\) and \(3/2\) gives

\[
 \sum a_{\nu k}
 \le
 \left(\sum {a_{\nu k}^3\over p_\nu^2}\right)^{1/3}
 \left(\sum p_\nu\right)^{2/3}.
\]

The zero-payment convention handles every \(p_\nu=0\) term.  For a
countable multiset, the displayed bound follows first for finite partial
sums and then by monotone convergence.  Repeated incidences are counted in
both sums, so no hidden multiplicity factor is dropped.  Adding the
\(q\)-row and testing the declared exceptional set proves (S.358).

For a finite coefficient vector,

\[
 \sup_{p_i\ge0,\ \sum p_i\le1}\sum_i c_ip_i^{2/3}
 =\left(\sum_i c_i^3\right)^{1/3};
\]

equality is attained at \(p_i=c_i^3/\sum_jc_j^3\) when the denominator is
nonzero.  Thus the coefficient cube in (S.357) is the exact dual quantity,
not a convenient sufficient exponent.

## 5. Measure scaling, roots, jumps, and Dini sums

Under parabolic Navier--Stokes scaling,
\(|\nabla u|^2\,dx\,dt\) has length dimension one.  The normalization

\[
 \nu_R(A)=R^{-1}\widetilde{\boldsymbol\mu}(\Phi_R(A))
\]

is therefore scale invariant, including for the anomalous part of the
total local-dissipation measure.  Halving parabolic radius creates eight
spatial children and four temporal children, hence \(32\) children.  The
half-open convention preserves exact mass additivity even if the measure
charges cell boundaries.

For a first \(\lambda\)-crossing root, the parent bound gives

\[
 \lambda\rho_Q<m_Q\le m_{Q^+}\le2\lambda\rho_Q.
\]

The roots form an antichain, so
\(\sum_Q\rho_Q\le\mathfrak M_R/\lambda\).  With

\[
 c_Q=\rho_Q^{1/3},\qquad
 p_Q=m_Q^{3/2}\rho_Q^{-1/2},
\]

one has \(m_Q=c_Qp_Q^{2/3}\) and

\[
 \sum c_Q^3\le{\mathfrak M_R\over\lambda},
 \qquad
 \sum p_Q\le(2\lambda)^{1/2}\mathfrak M_R.
\]

Their cubic Holder product is exactly
\(2^{1/3}\mathfrak M_R\); the level \(\lambda\) cancels.

For first relative \(\kappa\)-jumps below a node \(S\), disjointness and
the density lower bound give

\[
 \sum_{Q\in\mathscr J_\kappa(S)}\rho_Q
 \le{\rho_S\over\kappa}.
\]

If \(c_Q^3=\rho_Q^\alpha\), \(\alpha\ge1\), the proper-descendant bound
\(\rho_Q\le\rho_S/2\) yields

\[
 \sum_{Q\in\mathscr J_\kappa(S)}c_Q^3
 \le {2^{1-\alpha}\over\kappa}c_S^3.
\]

The geometric Dini sum in (S.368) is therefore correct.  Conversely,
\(\theta_d=(d+1)/(d+2)\) telescopes to a harmonic tail, so strictness at
each generation without a uniform Dini bound is insufficient.

## 6. Critical corona and lifted shell incidence

The revised corona model specifies

\[
 \rho_v=2^{-d}\rho_0,\qquad m_v=8^{-d}m_0,
 \qquad \Theta(v)=4^{-d}\Theta(0).
\]

The eight selected spatial children conserve mass inside one chosen
temporal child, while density strictly decreases along every branch.  Thus
the finite construction has no relative \(\kappa\)-jump.  Independently,
the Step 13 coefficient assignment obeys

\[
 \sum_{\rm eight\ children}c_Q^3
 =8(c_S/2)^3=c_S^3.
\]

This completes the claimed abstract low-transition-corona embedding.  The
coefficient \(c\) is correctly kept distinct from the root coefficient
\(\rho^{1/3}\), and no PDE realization is asserted.

The shell-incidence bound is valid only after unfolding.  For the single
Euclidean supports, the radial distance between
\(\operatorname{supp}\psi_k^R\) and
\(\operatorname{supp}\psi_{k+2}^R\) is at least

\[
 (4\rho_k-R/8)-(2\rho_k+R/8)
 =2\rho_k-R/4\ge15R/4.
\]

A set of physical spatial diameter at most \(2R\) therefore meets at most
two shell supports.  The final note explicitly warns that this is not a
claim about a torus cell meeting the periodized supports
\(\operatorname{supp}\Psi_k^R\).

## 7. Heat-shear screen

For

\[
 u^{(n)}=Ae^{-n^2t}\sin(nx_2)e_1,\qquad n=2^L,
\]

the nonlinear term vanishes and \(p=0\).  On the standard dyadic grid, a
child \(x_2\)-interval below a parent of depth \(d<L\) contains an integer
number of periods of \(\cos^2(nx_2)\).  Independence in \(x_1,x_3\) then
gives exactly one eighth of the parent viscous mass to each spatial child.

The moving velocity remains independent of \(y_1\), and the path velocity
is parallel to \(e_1\).  Every term in the physical flux is therefore an
\(y_1\)-independent coefficient times
\(\partial_{y_1}\Psi_k^R\); periodic integration proves
\(\dot F_{k,R}=0\).  This is a valid no-go for reading flux packing from a
raw critical dissipation tree.  It does not test the open shell-selective
PDE estimate.

## 8. Final audit of the open jump--corona lemma

The revision closes every quantifier defect from the first pass:

1. all nonnegative shell rows are unfolded before geometric incidence is
   used;
2. a countable locally finite forest covers the entire unbounded family of
   lifted, unperiodized shell supports;
3. each forest top may choose its own positive level \(\lambda_T\);
4. one \(\kappa>1\), one deletion budget, and all three constants are
   universal and independent of the solution, scale, terminal, levels,
   number of tops, and forest depth;
5. \(a_{\nu k}\), \(p_\nu\), the top row, and the corona row are explicitly
   assignments to be constructed by the open PDE argument; and
6. every periodic copy, forest overlap, and repeated node--shell incidence
   is charged in the payment multiset.

With these quantifiers, (S.375) is a well-defined **OPEN** sufficient PDE
statement.  Substitution into the already verified incidence theorem gives
(S.376) and hence the ancestor gate (S.288).  The implication is proved;
the antecedent is not.

## 9. Literature and claim boundary

The primary-source table is used only as a bounded collision screen.  Its
descriptions of suitable-weak partial regularity, moving cylinders,
critical Carleson solution classes, quantitative scale selection, and
pressure-sensitive epsilon regularity do not serve as proofs of (S.342) or
(S.375).  No novelty or priority claim is made.

The final claim ledger keeps the boundaries intact:

- (S.343)--(S.352), (S.356)--(S.371), and (S.372)--(S.374) are proved only
  in their displayed analytic, algebraic, geometric, or exact-family
  scopes;
- (S.353)--(S.355) and (S.370) remain abstract method obstructions, not NSE
  counterexamples;
- (S.358) and (S.376) are implications conditional on their displayed
  budgets; and
- (S.342), (S.375), (S.288), (S.303), Step 11 (S.272), Q.12, Q.1, scale
  contraction, regularity, singularity formation, and the Millennium
  problem remain open.

The note is therefore suitable to freeze as a rigorous method-boundary
result.  It neither proves a new regularity theorem nor resolves the Clay
problem.  **PASS / NOT CLAY.**
