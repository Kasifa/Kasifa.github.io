# R0.74S Step 14 — outer-collar alignment and the jump--corona obstruction

## 0. Result and scope

Step 13 isolated two possible ways to reach the quadratic payment scale.  The
short branch asked for a common-deletion temporal tail

\[
 \mathfrak H^F_{p,N,R}\lesssim (P_R^M)^{2/3},
 \qquad p>1,
\]

and the excess branch asked for a strict cubic Dini--Carleson charging of its
full-history ancestors.  This note tests both interfaces against the actual
cutoffs and the actual scaling of the total local-dissipation measure.
As in Steps 12--13, write

\[
 A_R:=(P_R^M)^{2/3}.
\]

There are eight conclusions.

1. The physical shell-flux derivative has an exact four-part signed split:
   local cubic, local pressure, shell-scale harmonic pressure, and
   moving-frame drift.  After absolute values, the inherited estimates pay
   the four parts only in \(L_t^1\), at the linear scale \(CP_R^M\).
2. The outer derivative collar of shell \(k\) lies in the doubled-radius
   payment annulus carrying the same weight \(\gamma_k\).  The
   super-Gaussian ratio helps the inner collar for \(k\ge3\), but it gives no
   gain on infinitely many outer collars.  Deleting finitely many inner
   shells does not change this fact.
3. A smooth \((N+1)\)-coordinate construction, supported on arbitrary outer
   shell indices, proves that the aligned weighted \(L^1\) ledger cannot by
   itself imply any \(L^p\), \(p>1\), common-deletion tail.  This is an
   **ABSTRACT METHOD OBSTRUCTION**, not a Navier--Stokes counterexample.
4. The exact algebraic interface for the excess branch is a cubic
   coefficient sum over a shell-incidence multiset.  It must be paired with
   payment counted with the same incidence multiplicity.
5. A scale-invariant pullback of the dissipation measure produces a
   32-child parabolic tree.  First crossings of a density level are sparse,
   but the natural level parameter cancels exactly in the cubic Holder
   estimate.  Density stopping alone therefore returns total mass, not a
   smaller payment power.
6. First descendants whose density jumps by a factor \(\kappa>1\) do have a
   strict Dini coefficient.  The nodes between jumps form a low-transition
   corona, however, and the present PDE ledger does not pay that corona at
   the quadratic scale.  A levelwise strict factor without a uniform Dini
   sum is also insufficient.
7. The exact heat shear with frequency \(2^L\) can display \(L\) levels of
   critical spatial mass splitting while every physical shell flux remains
   zero.  It is a narrow no-go for using a raw critical tree as evidence of
   flux packing; it is not an NSE counterexample to either open gate.
8. The remaining excess task is stated as one shell-selective
   jump--corona lemma with explicit top, corona, incidence, payment, and
   coefficient budgets.  The lemma is **OPEN**.  If proved, the algebra in
   this note would imply the Step 12 ancestor gate.

The Step 13 short-tail target (S.342), the ancestor gate (S.288), the
combined gate (S.303), Step 11 (S.272), Q.12, and Q.1 remain **OPEN**.
Nothing below proves scale contraction, regularity, singularity formation,
or the Navier--Stokes Millennium problem.  No DNS or DGX computation is
used.  **NOT CLAY.**

## 1. Exact four-channel flux decomposition

Retain the Version-M path, moving velocity, pressure, time cutoff, shell
cutoffs, and weights from Steps 12--13.  Put

\[
 \rho_k:=2^kR,
 \qquad
 \gamma_k:=\exp\!\left(-{4^{k-1}\over32}\right).
\]

On the Euclidean lift, the frozen cutoff has the form

\[
 \psi_k^R(y)
 =\vartheta\!\left({|y|-\rho_k\over R/8}\right)
  \vartheta\!\left({2\rho_k-|y|\over R/8}\right).
\]

Its gradient is supported in the two collars

\[
 \boxed{
 \begin{aligned}
 C_{k,R}^-&:=\{\rho_k-R/8<|y|<\rho_k\},\\
 C_{k,R}^+&:=\{2\rho_k<|y|<2\rho_k+R/8\},\\
 \operatorname {supp}\nabla\psi_k^R
 &\subset C_{k,R}^-\cup C_{k,R}^+
 \subset B_{3\rho_k}.
 \end{aligned}}
\tag{S.343}
\]

The last inclusion is deliberately tied to \(\rho_k\).  A pressure
remainder constructed only at the fixed radius \(2R\) is harmonic on
\(B_{6R}\), not on every outer shell.  For the four-channel decomposition,
fix \(0\le\zeta\in C_c^\infty(B_4)\), \(\zeta=1\) on \(B_3\), set
\(\zeta_{\rho_k}(y)=\zeta(y/\rho_k)\), retain the fixed frozen gauge
\(c_R(t)=c_{2R}^{M,R}(t)\), and define

\[
 \boxed{
 \begin{aligned}
 p_{k,R}^{\rm loc}
  &:=\mathcal R_i\mathcal R_j
       (\zeta_{\rho_k}\widetilde v_{R,i}\widetilde v_{R,j}),\\
 h_{k,R}^{\rm pr}
  &:=\widetilde\pi_R-p_{k,R}^{\rm loc}.
 \end{aligned}}
\tag{S.344}
\]

In distributions, both \(h_{k,R}^{\rm pr}\) and
\(h_{k,R}^{\rm pr}-c_R\) are harmonic on \(B_{3\rho_k}\).  Weyl's lemma
supplies their smooth harmonic representatives there.  The fixed gauge
does not change the flux because

\[
 \int_{\mathbb R^3}c_R(t)\widetilde v_R(t,y)
       \cdot\nabla\psi_k^R(y)\,dy=0.
\]

For almost every \(t\), unfolding the periodized cutoff gives

\[
 \boxed{
 \dot F_{k,R}
 =\dot F_{k,R}^{\rm cub}
  +\dot F_{k,R}^{\rm loc}
  +\dot F_{k,R}^{\rm har}
  +\dot F_{k,R}^{\rm dr},}
\tag{S.345}
\]

where

\[
 \boxed{
 \begin{aligned}
 \dot F_{k,R}^{\rm cub}
  &:={\gamma_k\over R}\eta_R
     \int_{\mathbb R^3}{|\widetilde v_R|^2\over2}
        \widetilde v_R\cdot\nabla\psi_k^R,\\
 \dot F_{k,R}^{\rm loc}
  &:={\gamma_k\over R}\eta_R
     \int_{\mathbb R^3}p_{k,R}^{\rm loc}\widetilde v_R
        \cdot\nabla\psi_k^R,\\
 \dot F_{k,R}^{\rm har}
  &:={\gamma_k\over R}\eta_R
     \int_{\mathbb R^3}(h_{k,R}^{\rm pr}-c_R)
        \widetilde v_R\cdot\nabla\psi_k^R,\\
 \dot F_{k,R}^{\rm dr}
  &:=-{\gamma_k\over R}\eta_R
     \int_{\mathbb R^3}{|\widetilde v_R|^2\over2}
        a_R\cdot\nabla\psi_k^R.
 \end{aligned}}
\tag{S.346}
\]

All variables in the integrals are evaluated at \((t,y)\).  The word
``harmonic'' in (S.346) refers only to the shell-scale remainder in
(S.344), on the neighborhood in (S.343).

With \(t(\sigma)=s_R+R^2\sigma\), define the four nonnegative dimensionless
majorants

\[
 \widehat h_{k,R}^{\alpha}(\sigma)
 :=\gamma_kR\eta_R(t(\sigma))
   \int_{\mathbb R^3}|\mathcal W_{k,R}^{\alpha}(t(\sigma),y)|
      |\nabla\psi_k^R(y)|\,dy,
 \quad
 \alpha\in\{{\rm cub,loc,har,dr}\},
\]

where the four \(\mathcal W^\alpha\) are the four vector integrands in
(S.346), before multiplication by \(\nabla\psi_k^R\).  Then

\[
 \boxed{
 h_{k,R}(\sigma)=R^2|\dot F_{k,R}(t(\sigma))|
 \le\sum_\alpha\widehat h_{k,R}^{\alpha}(\sigma).}
\tag{S.347}
\]

The prefactor in this formula is \(\gamma_kR\).  It becomes a bare
\(C\gamma_k\) only after the bound
\(R|\nabla\psi_k^R|\le C\) is used.

The componentwise payment can be checked without changing the gauge.  The
direct fixed-gauge pressure majorant is already part of the frozen payment.
For the local row, Calderon--Zygmund and Young give

\[
 \sum_k\|\widehat h_{k,R}^{\rm loc}\|_1
 \le CR^{-2}\int_{\mathcal T_R}\!\int_{\mathbb R^3}
       \left(\sum_{k:y\in B_{4\rho_k}}\gamma_k\right)
       |\widetilde v_R(t,y)|^3\,dy\,dt.
\]

The exact weight comparison

\[
 \sum_{k:y\in B_{4\rho_k}}\gamma_k
 \le C\bigl(\mathbf1_{B_{8R}}(y)+W_{2R}(y)\bigr)
\]

puts this term in the frozen core-plus-exterior cubic payment.  Since

\[
 |h_{k,R}^{\rm pr}-c_R|\,|\widetilde v_R|
 \le |\widetilde\pi_R-c_R|\,|\widetilde v_R|
    +|p_{k,R}^{\rm loc}|\,|\widetilde v_R|,
\]

the harmonic majorant is paid by the direct pressure row plus the local
row.  The local cubic and Jensen--Young drift estimates handle the other
two channels.  Therefore

\[
 \boxed{
 \sum_{k\ge1}\sum_\alpha
     \|\widehat h_{k,R}^{\alpha}\|_{L^1(0,4)}
 \le C P_R^M.}
\tag{S.348}
\]

This is a **PROVED / INHERITED** \(L^1\) statement.  The displayed argument
extracts the local and harmonic pressure rows without replacing the fixed
payment gauge.  It supplies neither \(p>1\) time integrability with a
uniform payment coefficient nor a sublinear power of \(P_R^M\).

There is a different fixed-solution tail.  With the energy quantities
\(e_R,d_R\) from Step 13, put

\[
 T_K(R):=\sum_{k>K}\gamma_k(1+2^{3k}R^3).
\]

To distinguish a fixed index tail from the best-\(K\) deletion functional,
write

\[
 \mathfrak T^F_{4/3,K,R}
 :=\sum_{k>K}\|h_{k,R}\|_{L^{4/3}(0,4)}.
\]

Deleting the first \(K\) shells in Step 13 (S.313) gives

\[
 \boxed{
 \mathfrak H^F_{4/3,K,R}
 \le \mathfrak T^F_{4/3,K,R}
 \le C T_K(R)
 \left([e_R(e_R+d_R)]^{3/4}+e_R^{3/2}\right).}
\tag{S.349}
\]

For every fixed \(R_*>0\),

\[
 \sup_{0<R\le R_*}T_K(R)
 \le\sum_{k>K}\gamma_k(1+2^{3k}R_*^3)
 \longrightarrow0.
\]

This does not make (S.349) uniform in \(R\): the energy bracket has no
available uniform bound.  The conclusion is only that, for each fixed
solution and fixed scale, the \(L^{4/3}\) shell tail tends to zero as
\(K\to\infty\).

## 2. The outer face has the payment weight

The doubled-radius exterior payment uses

\[
 A_j(2R)=\{2^{j+1}R\le|y|<2^{j+2}R\},
 \qquad j\ge1,
\]

with coefficient \(\gamma_j\).  The collars in (S.343) obey

\[
 \boxed{
 C_{k,R}^+\subset A_k(2R)\quad(k\ge1),
 \qquad
 C_{k,R}^-\subset A_{k-2}(2R)\quad(k\ge3).}
\tag{S.350}
\]

The two inner collars with \(k=1,2\) lie in the \(B_{8R}\) core and are
paid there.  For \(k\ge3\), the target-to-payment weight ratio on the inner
face is

\[
 \boxed{
 {\gamma_k\over\gamma_{k-2}}
 =\exp\!\left(-{15\,4^{k-3}\over32}\right)
 \longrightarrow0.}
\tag{S.351}
\]

There is no analogous factor on the outer face:

\[
 \boxed{
 {\hbox{target coefficient on }C_{k,R}^+
  \over
  \hbox{payment coefficient on }A_k(2R)}
 ={\gamma_k\over\gamma_k}=1.}
\tag{S.352}
\]

Equations (S.350)--(S.352) are a **PROVED GEOMETRIC OBSTRUCTION** to a
specific method.  They do not say that the signed outer flux is large.
They say that a proof which takes absolute values on each outer collar and
then compares it to the nonnegative exterior payment cannot extract a
super-Gaussian weight gain.  Removing any fixed number of inner shells
still leaves infinitely many aligned outer faces.

## 3. Smooth aligned spikes after arbitrary finite deletion

The preceding alignment has an exact functional consequence.  Fix
\(p\in(1,\infty]\), integers \(N,K_0\ge0\), and \(C_*,P>0\).  Put
\(M=N+1\) and choose distinct shell indices
\(k_1,\ldots,k_M>K_0\).  Let
\(0\le\phi\in C_c^\infty((-1,0))\), \(\int\phi=1\), choose an interior
terminal \(\vartheta_0\), and for sufficiently small \(d>0\) put

\[
 \phi_d(\sigma):=d^{-1}
       \phi\!\left({\sigma-\vartheta_0\over d}\right).
\]

For abstract raw outer-collar densities \(g_i\), target coefficients
\(\alpha_i\), and payment coefficients \(w_i\), set

\[
 \boxed{
 w_i=\alpha_i=\gamma_{k_i},
 \qquad
 g_i(\sigma)={P\over Mw_i}\phi_d(\sigma),
 \qquad
 H_i(\sigma):=\alpha_i g_i(\sigma).}
\tag{S.353}
\]

The aligned weighted payment is exactly

\[
 \sum_{i=1}^Mw_i\|g_i\|_1=P.
\]

Since deletion of \(N=M-1\) coordinates leaves one of the equal target
coordinates,

\[
 \boxed{
 \inf_{\#S\le N}\sum_{i\notin S}\|H_i\|_{L^p}
 ={P\over N+1}\|\phi\|_{L^p}
     d^{1/p-1}.}
\tag{S.354}
\]

Here \(1/\infty=0\).  The right side tends to infinity as \(d\downarrow0\).
In particular, after \(p,N,K_0,C_*\), and \(P\) are fixed, \(d\) can be chosen so
that (S.353) has payment \(P\) but

\[
 \boxed{
 \inf_{\#S\le N}\sum_{i\notin S}\|H_i\|_{L^p}
 >C_*P^{2/3}.}
\tag{S.355}
\]

This is an **ABSTRACT METHOD OBSTRUCTION**.  The \(g_i\) are smooth
nonnegative scalar rates, not fluxes generated by one velocity and
pressure.  Thus (S.355) does not refute the PDE estimate (S.342).  It proves
that (S.342) cannot be deduced from (S.348), outer-shell deletion, and the
super-Gaussian coefficients alone.  A positive proof must retain signed
local-energy cancellation or prove a PDE time anti-concentration estimate.

## 4. The exact coefficient-cube interface

The excess branch has a useful algebraic normal form.  Let
\(E_\tau\subset\mathbb N\), \(\#E_\tau\le N_b\), and let
\(\mathscr I_\tau\) be a countable incidence multiset of pairs
\((\nu,k)\) with \(k\notin E_\tau\).  Suppose nonnegative quantities obey

\[
 \boxed{
 b_k\le q_k+\sum_{\nu:(\nu,k)\in\mathscr I_\tau}a_{\nu k},
 \qquad k\notin E_\tau.}
\tag{S.356}
\]

Attach a payment \(p_\nu\ge0\) to each node occurrence.  Repetition in the
incidence multiset is counted repeatedly.  Use the convention
\(a_{\nu k}^3/p_\nu^2=0\) when both entries vanish and \(+\infty\) when
\(p_\nu=0<a_{\nu k}\).  If

\[
 \boxed{
 \begin{aligned}
 \sum_{k\notin E_\tau}q_k&\le C_qA_R,\\
 \sum_{(\nu,k)\in\mathscr I_\tau}p_\nu&\le C_pP_R^M,\\
 \sum_{(\nu,k)\in\mathscr I_\tau}
       {a_{\nu k}^3\over p_\nu^2}&\le C_{\rm cor},
 \end{aligned}}
\tag{S.357}
\]

then Holder on the incidence multiset gives

\[
 \begin{aligned}
 \sum_{(\nu,k)\in\mathscr I_\tau}a_{\nu k}
 &=\sum_{\mathscr I_\tau}
   {a_{\nu k}\over p_\nu^{2/3}}p_\nu^{2/3}\\
 &\le C_{\rm cor}^{1/3}(C_pP_R^M)^{2/3}.
 \end{aligned}
\]

Consequently,

\[
 \boxed{
 \mathcal S_{N_b}(b(\tau))
 \le\left(C_q+C_{\rm cor}^{1/3}C_p^{2/3}\right)A_R.}
\tag{S.358}
\]

This implication is **PROVED / CONDITIONAL**: the algebra is proved, while
the PDE construction of (S.356)--(S.357) is not.

Writing \(a_{\nu k}=c_{\nu k}p_\nu^{2/3}\) turns the last line of (S.357)
into a cubic coefficient sum.  For every finite nonnegative coefficient
vector, the exponent is exact because

\[
 \boxed{
 \sup_{p_i\ge0,\ \sum_ip_i\le1}
       \sum_ic_ip_i^{2/3}
 =\left(\sum_ic_i^3\right)^{1/3}.}
\tag{S.359}
\]

Thus a nodewise coefficient sum is insufficient if a node is incident to
many shells.  Either incidence multiplicity must be uniformly bounded, or
the repeated cubic sum and repeated payment in (S.357) must be proved
directly.

## 5. Scale-invariant parabolic measure and density roots

Let \(\widetilde{\boldsymbol\mu}\) be the periodic lift of the total local
dissipation measure and \(\widetilde X_R\) the lifted mollified path.  In
dimensionless comoving coordinates define

\[
 \boxed{
 \begin{aligned}
 \Phi_R(\sigma,z)
 &:=\bigl(s_R+R^2\sigma,
      \widetilde X_R(s_R+R^2\sigma)+Rz\bigr),\\
 \nu_R(A)&:=R^{-1}\widetilde{\boldsymbol\mu}(\Phi_R(A)).
 \end{aligned}}
\tag{S.360}
\]

The factor \(R^{-1}\) is forced by Navier--Stokes scaling:
\(|\nabla u|^2\,dx\,dt\) has length dimension one.  The same normalization
applies to the anomalous part of the total measure.

Take a parabolic dyadic root cell \(Q_0\) inside the lifted buffer.  A cell
of parabolic radius \(\rho_Q\) has spatial sidelength comparable to
\(\rho_Q\) and time length comparable to \(\rho_Q^2\).  Halving the radius
therefore gives eight spatial children and four temporal children.  Fix a
half-open convention throughout, so the children partition their parent
even when \(\nu_R\) charges a cell boundary:

\[
 \boxed{
 \#\operatorname {child}(Q)=32,
 \qquad
 \rho_{Q'}={1\over2}\rho_Q
 \quad(Q'\in\operatorname {child}(Q)).}
\tag{S.361}
\]

Put

\[
 m_Q:=\nu_R(Q),
 \qquad
 \Theta(Q):={m_Q\over\rho_Q},
 \qquad
 \mathfrak M_R:=\nu_R(Q_0).
\]

For \(\lambda>0\), call \(Q\ne Q_0\) a first \(\lambda\)-root when

\[
 \Theta(Q)>\lambda,
 \qquad
 \Theta(Q^+)\le\lambda,
\]

and every proper ancestor below \(Q_0\) has density at most \(\lambda\).
Equivalently, these are the maximal-by-inclusion first crossing cells.  The
top cell, when already above level, is recorded separately.  First roots
form an antichain.  Since \(\rho_{Q^+}=2\rho_Q\), they satisfy

\[
 \boxed{
 \lambda\rho_Q<m_Q\le2\lambda\rho_Q,
 \qquad
 \sum_{Q\in\mathscr R_\lambda}\rho_Q\le{\mathfrak M_R\over\lambda}.}
\tag{S.362}
\]

There is an exact critical factorization of root mass:

\[
 \boxed{
 a_Q:=m_Q,
 \qquad c_Q:=\rho_Q^{1/3},
 \qquad p_Q:=m_Q^{3/2}\rho_Q^{-1/2},
 \qquad a_Q=c_Qp_Q^{2/3}.}
\tag{S.363}
\]

Equations (S.362)--(S.363) give

\[
 \boxed{
 \sum_{\mathscr R_\lambda}c_Q^3
 \le{\mathfrak M_R\over\lambda},
 \qquad
 \sum_{\mathscr R_\lambda}p_Q
 \le(2\lambda)^{1/2}\mathfrak M_R.}
\tag{S.364}
\]

The level cancels in the cubic Holder product:

\[
 \boxed{
 \left({\mathfrak M_R\over\lambda}\right)^{1/3}
 \left((2\lambda)^{1/2}\mathfrak M_R\right)^{2/3}
 =2^{1/3}\mathfrak M_R.}
\tag{S.365}
\]

This is a **PROVED THRESHOLD NO-GAIN** statement.  It does not say that
first roots are useless; it says that density pigeonholing plus the critical
cubic duality returns the total measure mass with no favorable choice of
\(\lambda\).  If the available estimate for \(\mathfrak M_R\) is only
linear in a payment, (S.365) remains linear.  A quadratic conclusion
requires an additional PDE estimate, not optimization of the density
threshold.

## 6. Density jumps are sparse; the low-transition corona is not paid

Fix \(\kappa>1\) and a tree node \(S\) with \(m_S>0\).  Let
\(\mathscr J_\kappa(S)\) be the first proper descendants \(Q\subsetneq S\)
on each branch for which

\[
 \Theta(Q)>\kappa\Theta(S).
\]

These first-jump cells are disjoint.  Their defining lower bound and mass
subadditivity imply

\[
 \kappa{m_S\over\rho_S}
       \sum_{Q\in\mathscr J_\kappa(S)}\rho_Q
 <\sum_{Q\in\mathscr J_\kappa(S)}m_Q
 \le m_S.
\]

Hence

\[
 \boxed{
 \sum_{Q\in\mathscr J_\kappa(S)}\rho_Q
 \le{\rho_S\over\kappa}.}
\tag{S.366}
\]

More generally, if \(c_Q^3=\rho_Q^\alpha\) with \(\alpha\ge1\), every
proper descendant has \(\rho_Q\le\rho_S/2\), so

\[
 \boxed{
 \sum_{Q\in\mathscr J_\kappa(S)}c_Q^3
 \le\theta_\alpha c_S^3,
 \qquad
 \theta_\alpha:={2^{1-\alpha}\over\kappa}<1.}
\tag{S.367}
\]

Iterating only through first-jump descendants gives the uniform Dini sum

\[
 \boxed{
 \sum_{n\ge0}\theta_\alpha^n
 ={1\over1-\theta_\alpha}.}
\tag{S.368}
\]

Equations (S.366)--(S.368) are **PROVED** measure-tree facts.  They control
the jump skeleton, not every descendant.  Define the low-transition corona
of \(S\) to consist of nodes reached before a first \(\kappa\)-jump.  On
that corona one knows only
\(\Theta(Q)\le\kappa\Theta(S)\).  No inherited local-energy inequality
turns all of its shell contributions into the \(q\)-row of (S.357) at scale
\(A_R\).

The distinction cannot be repaired by asking only for a strict factor at
each generation.  For example,

\[
 \boxed{
 \theta_d={d+1\over d+2}<1,
 \qquad
 \prod_{j=0}^{n-1}\theta_{d_0+j}
 ={d_0+1\over d_0+n+1},
 \qquad
 \sum_{n\ge0}\prod_{j=0}^{n-1}\theta_{d_0+j}=\infty.}
\tag{S.369}
\]

Uniform Dini summability, not pointwise strictness, is the required tree
property.

There is also a critical corona model already present in Step 13.  Inside
the 32-child parabolic tree, retain one temporal child and all eight spatial
children at each generation.  The Step 13 eight-ary ledger has
\(c_{\rm child}=c_{\rm parent}/2\).  More explicitly, assign each retained
node at depth \(d\)

\[
 \rho_v=2^{-d}\rho_0,
 \qquad
 m_v=8^{-d}m_0.
\]

The eight selected children conserve mass, while

\[
 \Theta(v)={m_0\over\rho_0}4^{-d}
\]

strictly decreases down every branch.  This abstract measure may be viewed
as supported on one nested temporal branch and split uniformly among the
eight spatial children.  Hence it has no relative \(\kappa\)-jump for any
\(\kappa>1\), while

\[
 \boxed{
 \sum_{Q\in\operatorname {child}_{\rm spatial}(S)}c_Q^3
 =8\left({c_S\over2}\right)^3=c_S^3.}
\tag{S.370}
\]

Here \(c\) is the Step 13 incidence coefficient, not the root-factor
coefficient \(\rho^{1/3}\) in (S.363).  The example tests whether a jump
skeleton exhausts all admissible incidence coefficients; it does not
identify the two factorizations.

Its cubic sum repeats for arbitrarily many generations inside one corona.
This is an **ABSTRACT
METHOD OBSTRUCTION**.  Step 13 did not realize the full tree as the clocks
of one Navier--Stokes solution.

## 7. Shell incidence and the missing analytic charge

There is a favorable geometric fact.  In comoving coordinates the collar
family is stationary after each nonnegative periodized integral has been
unfolded to the Euclidean lift.  An unperiodized lifted cell whose physical
spatial diameter is at most \(2R\) can meet padded supports belonging to at
most two shell indices:

\[
 \boxed{
 \#\{k:R\operatorname {pr}_zQ
       \cap\operatorname {supp}\psi_k^R\ne\varnothing\}\le2.}
\tag{S.371}
\]

Indeed, the supports of shells \(k\) and \(k+2\) are separated radially by
at least \(2\rho_k-R/4\ge15R/4\).  The possible double incidence is between
adjacent padded shells at one hard boundary.  The same bound therefore
holds for derivative collars.  Larger tree cells must be split to this
resolution before the bound is used.  Equation (S.371) is not a statement
about one torus cell meeting the periodized supports
\(\operatorname {supp}\Psi_k^R\); periodic copies must be unfolded first.

Equation (S.371) is geometric.  Applying the local energy inequality on a
cell transported by \(X_R\) also creates the Version-M drift term.  Its
absolute estimate belongs to the linear payment (S.348).  Therefore the
bounded shell incidence does not, by itself, put the drift or the
low-transition corona into the quadratic \(q\)-budget.  Likewise, if a
covering or a top-boundary decomposition repeats the same cell, the payment
must be counted with that repetition as required in (S.357).

Combining the exact calculations gives the present boundary:

- first density roots are sparse, but their critical estimate is
  \(O(\mathfrak M_R)\) because of (S.365);
- first density jumps have a strict Dini skeleton by (S.368), but leave an
  unpaid corona;
- finite shell incidence controls geometric multiplicity, but the moving
  test retains a linearly paid drift row; and
- a nonuniform sequence of strict child factors can still have an infinite
  Dini sum by (S.369).

Thus the displayed threshold, jump-skeleton, incidence, and finite-deletion
estimates alone do not turn the existing nonnegative ledgers into (S.342)
or (S.288).

## 8. Exact heat shear: a narrow tree no-go

On the \(2\pi\)-periodic torus, take \(A>0\), an integer \(L\ge1\), and
retain the exact smooth solution

\[
 \boxed{
 u^{(n)}(t,x)=Ae^{-n^2t}\sin(nx_2)e_1,
 \qquad p^{(n)}=0,
 \qquad n=2^L.}
\tag{S.372}
\]

For the standard dyadic spatial grid and every generation strictly above
the wavelength, each child interval in \(x_2\) contains an integer number
of periods of \(\cos^2(nx_2)\).  Since the density is constant in
\(x_1,x_3\), every spatial child receives exactly one eighth of its
parent's viscous mass:

\[
 \boxed{
 \int_{J}\!\int_{Q'}|\nabla u^{(2^L)}|^2
 ={1\over8}
  \int_{J}\!\int_Q|\nabla u^{(2^L)}|^2,
 \qquad Q'\in\operatorname {child}_{\rm spatial}(Q),
 \quad d(Q)<L.}
\tag{S.373}
\]

Here \(J\) is any common time interval.  Thus the raw spatial dissipation
tree has \(L\) exact levels on which the critical eight-child coefficient
identity (S.370) can be imposed.

Nevertheless, the moving velocity is independent of \(y_1\), the path
velocity is parallel to \(e_1\), and periodic integration in \(y_1\) gives

\[
 \boxed{
 \dot F_{k,R}^{(2^L)}(t)=0
 \quad\hbox{for every }k,R,t.}
\tag{S.374}
\]

This exact family shows that a deep critical dissipation tree need not
produce any physical shell-flux tail.  It neither refutes (S.342) nor
realizes the abstract ancestor failure in (S.370): its completed clocks are
paid by the quadratic local-energy channel, with \(K_{k,R}=Q_{k,R}\).
Any future exact-family test must create nonzero shell-selective residuals
after the \(Q\), cubic, pressure, drift, and defect payments are all
included.

## 9. The shell-selective jump--corona lemma

The preceding work isolates one exact sufficient PDE statement.  First
unfold every nonnegative collar row to the Euclidean lift.  A candidate
construction must use a countable, locally finite forest of comoving
parabolic dyadic trees, drawn from a fixed finite family of shifted grids,
whose top cells cover

\[
 (0,4)\times
 \bigcup_{k\ge1}\{z:Rz\in\operatorname {supp}\psi_k^R\}.
\]

This forest is essential.  The single local cell \(Q_0\) in Section 5 does
not cover the unbounded lifted shell family, while the unweighted periodic
lift of the dissipation measure has infinite total mass.  For each top cell
\(T\), a construction may select a level \(\lambda_T>0\), take its first
crossing roots, and then iterate first relative jumps.  Write
\(\nu\rightsquigarrow k\) only for incidence with one unperiodized lifted
support.

The following statement is **OPEN** for the bare periodic suitable-weak
class.  There should exist a universal \(\kappa>1\), a universal integer
\(N_b\), constants \(C_q,C_p,C_{\rm cor}\), and one common shell set
\(E_\tau\), \(\#E_\tau\le N_b\), such that for every solution, scale, and
good terminal one can choose the forest and levels above and construct
nonnegative top, corona, jump, and payment rows satisfying

\[
 \boxed{
 \begin{gathered}
 b_k(\tau)\le q_k^{\rm top}+q_k^{\rm cor}
       +\sum_{\nu:\nu\rightsquigarrow k}a_{\nu k}
       \quad(k\notin E_\tau),\\
 \sum_{k\notin E_\tau}(q_k^{\rm top}+q_k^{\rm cor})
       \le C_qA_R,\\
 \sum_{\substack{(\nu,k):\nu\rightsquigarrow k\\k\notin E_\tau}}
       p_\nu\le C_pP_R^M,\\
 \sum_{\substack{(\nu,k):\nu\rightsquigarrow k\\k\notin E_\tau}}
       {a_{\nu k}^3\over p_\nu^2}\le C_{\rm cor}.
 \end{gathered}}
\tag{S.375}
\]

Here \(b_k(\tau)\) is the inherited Step 12 excess-ancestor coordinate.
The quantity \(a_{\nu k}\) is the part assigned to one jump-skeleton
node--shell incidence, \(p_\nu\) is a nonnegative portion of the frozen
payment used at that incidence, and \(q_k^{\rm top},q_k^{\rm cor}\) are
the unassigned top and low-transition rows.  These assignments are part of
the asserted PDE construction; the measure-tree facts alone do not define
them.

The same \(E_\tau\) must be used for the defect and high-Rayleigh
ancestors; it cannot move between tree levels or payment channels.
\(N_b,C_q,C_p,C_{\rm cor}\), and \(\kappa\) are independent of the
solution, \(R\), \(\tau\), the selected levels \(\lambda_T\), the number of
top cells, and the forest depth.

In the payment sum in (S.375), the notation means summation over the
full incidence multiset, not over distinct nodes.  It must include every
periodic copy after unfolding and every repeated use across forest tops.
The zero-payment convention is the one following (S.356).  The top row
includes cells before a first crossing and every top-boundary contribution.
The corona row includes the moving-frame drift and every node not reached
by the jump skeleton.  These terms may instead be split further, but their
total must retain the stated \(A_R\) bound.

If (S.375) holds, substitute

\[
 q_k=q_k^{\rm top}+q_k^{\rm cor},
 \qquad
 \mathscr I_\tau=\{(\nu,k):\nu\rightsquigarrow k\}
\]

into (S.356)--(S.358).  This proves the conditional implication

\[
 \boxed{
 \text{(S.375)}\quad\Longrightarrow\quad
 \mathcal S_{N_b}(b(\tau))
 \le\left(C_q+C_{\rm cor}^{1/3}C_p^{2/3}\right)A_R.}
\tag{S.376}
\]

Thus (S.375) would close the ancestor gate (S.288).  The new mathematical
content is not the Holder step; it is the PDE estimate that pays the top and
low-transition corona quadratically while preserving shell incidence and
payment additivity.  Neither partial regularity, the bare measure mass, nor
the current moving-tube estimate supplies that statement.

## 10. Route decision

This step removes two proof patterns from the immediate route.

1. For the short branch, I will not pursue further estimates obtained by
   taking absolute values separately in (S.345) and applying only the
   existing nonnegative payment.  The outer face is coefficient-aligned and
   the smooth spike (S.353)--(S.355) saturates that information.  The next
   admissible input is a signed local-energy cancellation on the outer
   collars or a PDE time anti-concentration theorem that is uniform after
   one common finite shell deletion.  Target (S.342) remains **OPEN**.
2. For the excess branch, the useful positive algebra is complete at
   (S.358).  The next task is the PDE content of (S.375), beginning with the
   low-transition corona and the top-boundary row.  Density thresholds and
   jump sparsity will be used only after repeated incidence payments have
   been recorded.
3. Exact-family screens must be shell selective.  A high Fourier frequency,
   a deep raw dissipation tree, or a large Rayleigh ratio is insufficient
   when the physical flux vanishes or the completed clock is already paid
   by \(Q\).

No route decision changes the frozen target or its quantifiers.

## 11. Bounded primary-source boundary

The bounded primary-source screens from Steps 12--13 were compared with the
two interfaces isolated here.  No cited theorem has the common-deletion
flux-tail or shell-selective jump--corona quantifiers of (S.342) or (S.375).

| Primary result | Established scope | Boundary for Step 14 |
|---|---|---|
| Caffarelli--Kohn--Nirenberg, [*Partial regularity of suitable weak solutions*](https://doi.org/10.1002/cpa.3160350604) | Suitable-weak local energy inequality, epsilon regularity, and parabolic size of the singular set | A support-size conclusion does not give the repeated mass, incidence, or low-transition-corona budgets in (S.375).  The high-Rayleigh ancestor can also lie in the regular set. |
| J. Yang, [*Construction of maximal functions associated with skewed cylinders generated by incompressible flows and applications*](https://doi.org/10.4171/AIHPC/20), *Ann. Inst. H. Poincare C* **39** (2022), 793--818 | Mollified-flow trajectories, skewed cylinders, and associated covering/maximal-function estimates | This supplies neighboring moving-cylinder geometry, not the shell payment or the cubic incidence charge (S.357). |
| H. Koch, D. Tataru, [*Well-posedness for the Navier--Stokes equations*](https://doi.org/10.1006/aima.2000.1937), *Adv. Math.* **157** (2001), 22--35 | Critical small-data well-posedness in \(BMO^{-1}\) through a Carleson-type spacetime norm | The Carleson control is part of a critical solution class; it is not derived for every bare suitable weak solution from \(P_R^M\). |
| Z. Lei, X. Ren, [*Quantitative partial regularity of the Navier--Stokes equations and applications*](https://doi.org/10.1016/j.aim.2024.109654), *Adv. Math.* **445** (2024), 109654 | Quantitative partial regularity through scale selection and pigeonholing | Its selected levels and constants do not supply one common terminal window, fixed physical shell deletion, or the corona decomposition (S.375). |
| C. Guevara, N. C. Phuc, [*Local energy bounds and epsilon-regularity criteria for the 3D Navier--Stokes system*](https://doi.org/10.1007/s00526-017-1151-7), *Calc. Var. PDE* **56** (2017), 68 | Pressure-sensitive local-energy estimates and epsilon-regularity criteria | These estimates convert stated local inputs into regularity; they do not yield the aligned outer-collar \(L^p\) tail or the payment-additive corona charge. |

This is a collision boundary, not a novelty or priority claim.  The cited
results provide relevant local-energy, moving-cylinder, Carleson, and
quantitative-partial-regularity context, but they do not prove the open
interfaces stated here.

## 12. Claim ledger

The following are **PROVED** in the frozen setting:

- the shell-scale pressure decomposition and exact four-channel signed flux
  identity (S.343)--(S.347);
- the inherited componentwise \(L^1\) payment and the fixed-solution tail
  boundary (S.348)--(S.349);
- the outer/inner collar inclusions, inner-face weight gain, and outer-face
  coefficient alignment (S.350)--(S.352);
- the incidence Holder theorem and exact cubic duality
  (S.356)--(S.359), conditional only on the displayed input budgets;
- the scale-invariant measure normalization, 32-child parabolic scaling,
  first-root bounds, critical factorization, and threshold cancellation
  (S.360)--(S.365);
- first-jump sparsity and its strict Dini coefficient
  (S.366)--(S.368);
- failure of levelwise strictness without a uniform Dini sum (S.369);
- bounded fine-scale shell incidence (S.371); and
- the heat-shear mass-splitting and zero-flux identities
  (S.372)--(S.374).

The following are **ABSTRACT METHOD OBSTRUCTIONS, NOT NSE
COUNTEREXAMPLES**:

- the aligned smooth \((N+1)\)-coordinate rates
  (S.353)--(S.355); and
- the critical eight-ary corona embedding (S.370), inherited from the
  Step 13 ledger model.

The following statements are **CONDITIONAL**:

- the quadratic ancestor estimate (S.358), conditional on the exact
  incidence budgets (S.356)--(S.357); and
- the implication (S.376), conditional on the shell-selective
  jump--corona lemma (S.375).

The following remain **OPEN**:

- the common-deletion temporal estimate (S.342), including any uniform
  \(p>1\) outer-collar anti-concentration estimate;
- the PDE shell-selective jump--corona lemma (S.375), especially the
  top-boundary, low-transition-corona, and moving-drift charge;
- the ancestor gate (S.288), the combined gate (S.303), Step 11 (S.272),
  Q.12, and Q.1; and
- scale contraction, regularity, singularity formation, and the
  Navier--Stokes Millennium problem.

The advance is a precise method boundary.  Super-Gaussian weights do not
help the aligned outer flux face, density thresholds do not improve the
critical cubic payment power, and density jumps leave a corona that the
current PDE ledger does not control.  The next positive statement is now
the explicit open lemma (S.375).  **NOT CLAY.**
