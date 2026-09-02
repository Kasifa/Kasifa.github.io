# R0.74N — all-shell synthesis of the signed annular collar flux

## Status and scope

This note proves the full familywise condition frozen in
r074n_problem_freeze.md:

\[
 \boxed{
 \sup_{\tau\in I_{R_j}}[\mathcal I_j(\tau)]_+
 \le C\Gamma_jL_jR_j^5}
\tag{0.1}
\]

for all sufficiently large \(j\).  The proof divides the exact annular sum
into three disjoint ranges.  R0.74L pays the target shell \(k=j\).  All
inward shells \(k\le j-1\) are combined into one positive chord and paid by
the R0.74M final-segment expulsion mechanism.  All outer shells
\(k\ge j+1\) are paid absolutely by the super-Gaussian annular weights.

The combined-inner step is stronger than a rowwise exponent argument.  It
uses

\[
 \sum_{k\ge1}2^k\Gamma_k<\infty
\tag{0.2}
\]

and the fact that the union of all inward supports remains inside the same
padded \(j-1\) tube already treated in R0.74M.  There is no cancellation
assumption between shells or between packets.

Consequently the exact family has matching collar-flux and weighted
kinetic--dissipation laws

\[
 X_j\asymp\mathfrak C_j\asymp B_j^2L_jR_j^2
 \asymp P_j^{2/3}\sqrt{1+\log_+P_j}.
\tag{0.3}
\]

This is a theorem for two observables on one constructed smooth family.  It
does not prove a universal endpoint inequality, singularity formation, or
global regularity.  **NOT CLAY.**

Throughout, suppress the index \(j\) and write

\[
 R=e^{-L^2/320},\qquad h=\frac{15}{16}LR,\qquad
 c_\gamma=\frac8{3969},\qquad \rho=\frac1{320},
\tag{0.4}
\]

\[
 \Gamma_k=e^{-4^{k-1}/32},\qquad
 \Gamma_j=e^{-c_\gamma L^2},\qquad
 \frac1{128R^2}\le B\le\frac1{64R^2}.
\tag{0.5}
\]

The time window and the complete R0.74H cutoff conditions are

\[
 \begin{gathered}
 s_R=61R^2,\qquad I_R=(64R^2,65R^2),\\
 \eta_R=0\ \hbox{near }s_R,\qquad
 \eta_R=1\ \hbox{on }I_R,\\
 0\le\eta_R\le1,\qquad \eta_R'\ge0,\qquad
 |\eta_R'|\le CR^{-2}.
 \end{gathered}
\tag{0.6}
\]

Here \(\eta_R\) is smooth and nondecreasing.  The shell proof below uses
only \(0\le\eta_R\le1\), but the endpoint-energy and full-dissipation
conclusion after Theorem 6.1 invokes R0.74H with this complete cutoff.

## 1. Finite annular decomposition

For the exact two-packet field

\[
 F=F^++F^-,\qquad
 F^-(t,x_2,x_3)=-F^+(t,-x_2,-x_3),
\tag{1.1}
\]

put

\[
 \mathcal J_{j,k}(\tau)
 =\Gamma_k\int_{s_R}^{\tau}\eta_R(t)
 \int_{\mathbb R^3}\theta(t,x_3)\widetilde F(t,x_2,x_3)^2
 \partial_2\psi_k^R(x)\,dx\,dt.
\tag{1.2}
\]

First truncate the smooth annular weight at \(N\ge j+1\).  Then

\[
 \mathcal I_j^{(N)}(\tau)
 =\mathcal I_{<}(\tau)+\mathcal I_{=}(\tau)
  +\mathcal I_{>,N}(\tau),
\tag{1.3}
\]

where

\[
 \mathcal I_{<}=\sum_{k=1}^{j-1}\mathcal J_{j,k},\qquad
 \mathcal I_{=}=\mathcal J_{j,j},\qquad
 \mathcal I_{>,N}=\sum_{k=j+1}^{N}\mathcal J_{j,k}.
\tag{1.4}
\]

These ranges are disjoint.  Their union is every shell index \(k\ge1\)
as \(N\to\infty\).

## 2. One cancellation-free chord for every inward shell

Define

\[
 D_{<}(t,x_2,x_3)
 :=\sum_{k=1}^{j-1}\Gamma_k
 \int_{\mathbb R}
 [\theta(t,x_3)\partial_2\psi_k^R(x)]_+\,dx_1
\tag{2.1}
\]

and let \(\overline D_{<}\) be its two-variable periodization.

### Lemma 2.1 — uniform combined chord

For all sufficiently large \(j\),

\[
 \boxed{0\le\overline D_{<}\le C_*}
\tag{2.2}
\]

with \(C_*\) independent of \(j\).  Moreover,

\[
 \overline D_{<}(t,\bar x_2,\bar x_3)\ne0
 \Longrightarrow
 |x_2|_{\rm lift},|x_3|_{\rm lift}\le r_-,
\tag{2.3}
\]

where

\[
 r_-=2^jR+\frac R8
 =\left(\frac{32}{63}L+\frac18\right)R<1.
\tag{2.4}
\]

**Proof.**  The cutoff \(\psi_k^R\) is supported in the \(R/8\)-padding
of the annulus \(2^kR\le|x|<2^{k+1}R\), and
\(|\partial_2\psi_k^R|\le C/R\).  At fixed \((x_2,x_3)\), its
\(x_1\)-chord has length at most \(C2^kR\).  Since \(|\theta|\le1\),

\[
 \int_{\mathbb R}
 [\theta\partial_2\psi_k^R]_+\,dx_1\le C2^k.
\tag{2.5}
\]

Therefore

\[
 D_{<}\le C\sum_{k=1}^{j-1}2^k\Gamma_k
 \le C\sum_{k\ge1}2^ke^{-4^{k-1}/32}=:C_*<\infty.
\tag{2.6}
\]

Every inward support is contained in the largest padded ball, whose radius
is (2.4).  Because \(r_-<1\), at most one lift in each periodic coordinate
can contribute.  Thus periodization preserves both (2.2) and (2.3).
\(\square\)

### Lemma 2.2 — exact positive-packet reduction

There is a nonnegative common-forward quantity

\[
\begin{aligned}
 \mathcal P_{<}(\tau)
 :={}&R^6\int_{s_R}^{\tau}\eta_R(t)
 \int_{\mathbb T}|\partial K_T(u)|^2\\
 &\times\mathbb E^{\rm fw}\!\left[
 K_T(X_t)\overline D_{<}
 (t,q_\omega(t)+u,h+X_t)
 \right]du\,dt,
\end{aligned}
\tag{2.7}
\]

where \(T=R^2+t\) and

\[
 q_\omega(t)=Q(t)-\mathfrak S_t^\leftarrow[X],\qquad
 \mathfrak S_t^\leftarrow[X]
 =B\int_0^t[\theta(s,h)-\theta(s,h+X_s)]\,ds,
\tag{2.8}
\]

such that

\[
 \boxed{[\mathcal I_{<}(\tau)]_+\le4\mathcal P_{<}(\tau).}
\tag{2.9}
\]

**Proof.**  Since \(\eta_R\ge0\),

\[
\begin{aligned}
 [\mathcal I_{<}(\tau)]_+
 &\le\sum_{k=1}^{j-1}\Gamma_k
 \int_{s_R}^{\tau}\!\!\int_{\mathbb R^3}
 \eta_R[\theta\partial_2\psi_k^R]_+|F|^2\,dx\,dt.
\end{aligned}
\tag{2.10}
\]

Each \([\theta\partial_2\psi_k^R]_+\) is even under full inversion,
because \(\theta(t,x_3)\) and \(\partial_2\psi_k^R(x)\) are both odd.
Use (1.1) and

\[
 |F^++F^-|^2\le2(|F^+|^2+|F^-|^2).
\tag{2.11}
\]

The two self-majorants are equal, so (2.10) is at most four times the
positive-packet term.  Jensen applied shell by shell, followed by Tonelli,
exact two-variable periodization, and the R0.74L common-forward-law identity,
gives (2.7).  All heat-kernel windings, collar copies, and the correlation
between \(X\) and \(q_\omega\) remain present.  \(\square\)

## 3. The combined inner sum is expelled

Use the R0.74M final-segment event

\[
 \mathcal H_t=
 \left\{
 \sup_{t-R^2/64\le s\le t}
 |\widetilde X_s-\widetilde X_t|
 \le\frac1{16}LR
 \right\}.
\tag{3.1}
\]

Its complement satisfies

\[
 \mathbb P(\mathcal H_t^c)\le4e^{-L^2/16}.
\tag{3.2}
\]

If the chord in (2.7) is nonzero, Lemma 2.1 selects a vertical lift with
\(|h+X_t|_{\rm lift}\le r_-\).  On \(\mathcal H_t\),

\[
 |h+X_s|_{\rm lift}
 \le r_-+\frac1{16}LR
 \le\frac35LR
\tag{3.3}
\]

over the final segment.  The last inequality uses the exact padding margin

\[
 \frac35-\frac{32}{63}-\frac1{16}
 =\frac{149}{5040}>0.
\tag{3.4}
\]

R0.74M's lower caloric-defect lemma and plateau subtraction therefore give

\[
 \mathfrak S_t^\leftarrow[X]\ge\Sigma_L,
 \qquad
 \Sigma_L:=\frac1{32768}e^{-L^2/640}.
\tag{3.5}
\]

Since

\[
 \frac{\Sigma_L}{LR}
 =\frac{e^{L^2/640}}{32768L}\longrightarrow\infty,
\tag{3.6}
\]

Increase the base index so that \(2R\le\Sigma_L<1\), as in R0.74M.  The
same torus triangle argument as in R0.74M yields, on chord support and
\(\mathcal H_t\),

\[
 \operatorname{dist}_{\mathbb T}(u,0)\ge\frac12\Sigma_L.
\tag{3.7}
\]

No horizontal winding is selected in (3.7).

### Bad final segments

For \(62R^2\le T\le66R^2\),

\[
 \|K_T\|_\infty\le\frac CR,\qquad
 \int_{\mathbb T}|\partial K_T|^2\le\frac C{R^3}.
\tag{3.8}
\]

Using (2.2), (3.2), (3.8), and a time interval of length at most \(4R^2\)
in (2.7) gives

\[
 \mathcal P_{<}^{\rm bad}(\tau)
 \le CR^6R^2R^{-1}R^{-3}e^{-L^2/16}
 =CR^4e^{-L^2/16}.
\tag{3.9}
\]

The exact exponent reserve is

\[
 \boxed{
 \frac1{16}-\rho-c_\gamma
 =\frac{72851}{1270080}>0.}
\tag{3.10}
\]

Hence, uniformly in \(\tau\in I_R\),

\[
 \mathcal P_{<}^{\rm bad}(\tau)
 \le C\Gamma_jLR^5
\tag{3.11}
\]

for all sufficiently large \(j\).

### Good final segments

The periodic derivative-kernel tail used in R0.74M is

\[
 \int_{\operatorname{dist}_{\mathbb T}(u,0)\ge d}
 |\partial K_T(u)|^2du
 \le\frac C{R^4}\exp\!\left(-\frac{d^2}{264R^2}\right),
 \qquad R\le d\le1.
\tag{3.12}
\]

Equations (2.2), (3.7), (3.8), and (3.12) show

\[
 \mathcal P_{<}^{\rm good}(\tau)
 \le CR^3
 \exp\!\left(-\frac{\Sigma_L^2}{1056R^2}\right).
\tag{3.13}
\]

Here

\[
 \frac{\Sigma_L^2}{1056R^2}
 =\frac1{1056\cdot32768^2}
 \exp\!\left(\frac{L^2}{320}\right).
\tag{3.14}
\]

The right side of (3.14) eventually dominates
\((c_\gamma+2\rho)L^2\).  Therefore

\[
 \exp\!\left(-\frac{\Sigma_L^2}{1056R^2}\right)
 \le\Gamma_jR^2
\tag{3.15}
\]

for all sufficiently large \(j\), and

\[
 \mathcal P_{<}^{\rm good}(\tau)
 \le C\Gamma_jR^5
 \le C\Gamma_jLR^5.
\tag{3.16}
\]

Combining (2.9), (3.11), and (3.16) proves

\[
 \boxed{
 \sup_{\tau\in I_R}[\mathcal I_{<}(\tau)]_+
 \le C\Gamma_jLR^5.}
\tag{3.17}
\]

This one estimate covers every \(1\le k\le j-1\), including the complete
nearest-inward row.  It does not use cancellation between those rows.

## 4. The target shell is inherited from R0.74L

R0.74L proves the absolute true-packet estimate

\[
 \int_{s_R}^{\tau}\eta_R(t)
 \int_{\mathbb R^3}
 |\theta|\,|F|^2|\partial_2\psi_j^R|\,dx\,dt
 \le CLR^5
\tag{4.1}
\]

uniformly in \(\tau\in I_R\).  Multiplication by \(\Gamma_j\) gives

\[
 \boxed{
 \sup_{\tau\in I_R}|\mathcal I_{=}(\tau)|
 \le C\Gamma_jLR^5.}
\tag{4.2}
\]

## 5. Absolute summation of every outer shell

### Lemma 5.1 — uniform packet and collar bounds

On the full time interval used here,

\[
 \boxed{\|F(t)\|_{L^\infty(\mathbb T^2)}\le C.}
\tag{5.1}
\]

For every \(k\ge1\),

\[
 \boxed{
 \int_{\mathbb R^3}|\partial_2\psi_k^R(x)|\,dx
 \le C4^kR^2.}
\tag{5.2}
\]

**Proof.**  Initially each packet has the form

\[
 R^3\partial K_{R^2}(x_2-q)K_{R^2}(x_3-h),
\tag{5.3}
\]

up to sign and inversion.  The periodic heat-kernel bounds
\(\|\partial K_{R^2}\|_\infty\le CR^{-2}\) and
\(\|K_{R^2}\|_\infty\le CR^{-1}\) make (5.3) uniformly bounded.
The scalar advection-diffusion maximum principle preserves this bound for
each packet; (1.1) proves (5.1) for their sum.

For (5.2), \(|\partial_2\psi_k^R|\le C/R\), and its support lies in two
spherical layers of width \(O(R)\) at radii comparable to \(2^kR\) and
\(2^{k+1}R\).  Their total volume is \(O(4^kR^3)\).  Multiplication by
\(C/R\) proves (5.2), including both radial faces.  \(\square\)

Equations (0.6), (5.1), and (5.2) give, uniformly in \(\tau\in I_R\),

\[
 |\mathcal J_{j,k}(\tau)|
 \le C\Gamma_k4^kR^4.
\tag{5.4}
\]

Let \(a_k=4^k\Gamma_k\).  Then

\[
 \frac{a_{k+1}}{a_k}
 =4\exp\!\left(-\frac{3\cdot4^{k-1}}{32}\right).
\tag{5.5}
\]

For all sufficiently large \(j\), (5.5) is at most \(1/2\) whenever
\(k\ge j+1\).  Thus

\[
 \sum_{k\ge j+1}4^k\Gamma_k
 \le2\,4^{j+1}\Gamma_{j+1}.
\tag{5.6}
\]

Since

\[
 4^{j+1}=\frac{4096}{3969}L^2,
 \qquad
 \frac{\Gamma_{j+1}}{\Gamma_j}=e^{-3c_\gamma L^2},
\tag{5.7}
\]

we obtain

\[
 \sup_{\tau\in I_R}|\mathcal I_{>} (\tau)|
 \le C\Gamma_jL^2R^4e^{-3c_\gamma L^2}.
\tag{5.8}
\]

The exponent left after paying one inverse \(R\) is

\[
 \boxed{
 3c_\gamma-\rho
 =\frac{1237}{423360}>0.}
\tag{5.9}
\]

Consequently

\[
 \boxed{
 \sup_{\tau\in I_R}|\mathcal I_{>} (\tau)|
 \le C\Gamma_jLR^5.}
\tag{5.10}
\]

The estimate is performed on \(\mathbb R^3\) against the periodic lift of
the true packet, so every periodic copy is included.  The convergent
nonnegative majorant in (5.6) justifies Tonelli and the infinite outer sum.

## 6. Infinite-shell limit and complete theorem

The outer estimate (5.4)--(5.6) makes
\(\mathcal I_{>,N}\) uniformly Cauchy in \(\tau\).  Equivalently, it is an
explicit integrable domination for the inherited \(C^2\) convergence of the
finite annular weights.  Hence

\[
 \mathcal I_j^{(N)}(\tau)\longrightarrow\mathcal I_j(\tau)
\tag{6.1}
\]

uniformly on \(I_R\).  From (1.3),

\[
 [\mathcal I_j(\tau)]_+
 \le[\mathcal I_{<}(\tau)]_+
   +|\mathcal I_{=}(\tau)|+|\mathcal I_{>} (\tau)|.
\tag{6.2}
\]

Apply (3.17), (4.2), and (5.10).

### Theorem 6.1 — exact all-shell synthesis

For the exact R0.74F--H smooth periodic unforced family, there exist
\(C<\infty\) and \(j_0\) such that for every \(j\ge j_0\),

\[
 \boxed{
 \sup_{\tau\in I_{R_j}}[\mathcal I_j(\tau)]_+
 \le C\Gamma_jL_jR_j^5.}
\tag{6.3}
\]

The constant may depend on the frozen cutoff profile but not on \(j\).
The estimate is uniform over the inherited admissible time cutoffs because
only \(0\le\eta_R\le1\) was used.

R0.74K Theorem 4.1 converts (6.3) into

\[
 \mathfrak C_j\le CB_j^2L_jR_j^2.
\tag{6.4}
\]

Together with the R0.74H lower bound and the R0.74J payment-scale identity,

\[
 \boxed{
 \mathfrak C_j\asymp B_j^2L_jR_j^2
 \asymp P_j^{2/3}\sqrt{1+\log_+P_j}.}
\tag{6.5}
\]

### Corollary 6.2 — familywise weighted kinetic--dissipation saturation

For \(\alpha\in\{M,F\}\), write

\[
 \mathcal U_j^\alpha
 :=\mathcal U_{\rm ext}^{\infty,\alpha,R_j},\qquad
 \mathcal D_j^\alpha
 :=\mathcal D_{\rm ext}^{\alpha,R_j},\qquad
 X_j^\alpha=\mathcal U_j^\alpha+\mathcal D_j^\alpha.
\tag{6.6}
\]

The zero-frame identities on the exact family make the two versions equal;
write their common values as \(\mathcal U_j,\mathcal D_j,X_j\), and put
\(T_j=B_j^2L_jR_j^2\).  There exist \(0<c<C<\infty\) and \(j_0\) such
that, for every \(j\ge j_0\),

\[
 \boxed{
 cT_j\le\mathcal U_j\le X_j\le CT_j,
 \qquad 0\le\mathcal D_j\le CT_j.}
\tag{6.7}
\]

In particular,

\[
 \boxed{
 X_j\asymp\mathfrak C_j\asymp B_j^2L_jR_j^2
 \asymp P_j^{2/3}\sqrt{1+\log_+P_j}.}
\tag{6.8}
\]

**Proof.**  R0.74H Theorem 5.1, more precisely its separate endpoint-energy
and full-dissipation estimates (5.1a)--(5.1b), gives

\[
 \mathcal U_j,\ \mathcal D_j
 \le C\bigl(P_j^{2/3}+\mathfrak C_j\bigr).
\tag{6.9}
\]

R0.74J Theorem 3.3 and (6.4) give

\[
 P_j^{2/3}\le CB_j^2R_j^2\le CT_j,
 \qquad \mathfrak C_j\le CT_j,
\tag{6.10}
\]

where \(L_j\ge1\) for all sufficiently large \(j\).  This proves both
upper bounds in (6.7).  R0.74F Theorem 6.2 and
\(\mathfrak a_j=B_j\Gamma_j^{-1/2}\) give the lower bound

\[
 \mathcal U_j
 \ge c\mathfrak a_j^2\Gamma_jL_jR_j^2
 =cT_j.
\tag{6.11}
\]

Equation (6.8) now follows from (6.5) and R0.74J (4.6).  Notice that the
proof does not give a matching lower bound for \(\mathcal D_j\). \(\square\)

This corollary is a non-circular cross-note synthesis, not a new stochastic
estimate.  R0.74H proves (6.9) for every smooth solution in its scope;
R0.74J obtains the payment law from a nonnegative fifth-shell velocity
ledger and the direct R0.74G upper bound; and Theorem 6.1 obtains the collar
upper bound from the packet integral.  None of those three inputs assumes
the upper bound for \(X_j\).

## 7. What is proved and what remains open

### Proved here

1. All inward rows are controlled together by one bounded positive chord;
   no rowwise shell cancellation is used.
2. The R0.74M support-conditioned final-segment expulsion remains valid for
   that complete inward union.
3. The target row is paid absolutely by the audited R0.74L theorem.
4. Every outer row, every Euclidean lift, and the infinite outer tail are
   paid absolutely by the super-Gaussian weights.
5. The full signed R0.74K condition and the matching collar-flux law hold on
   this exact family.
6. Combining the audited R0.74H energy closure, the R0.74J payment law, and
   the new collar upper bound gives the matching familywise \(X_j\) law,
   with a matching kinetic component and an upper bound for dissipation.

### Still open

1. a matching lower bound for the dissipation component \(\mathcal D_j\)
   by itself;
2. a universal square-root-log endpoint inequality for arbitrary smooth
   Navier--Stokes solutions;
3. payment-to-admissibility or prescribed-point core-from-shell control;
4. singularity formation or exclusion for arbitrary three-dimensional data;
5. global existence and smoothness; and
6. novelty or priority beyond the bounded literature audit.

The result is a rigorous familywise saturation theorem for the collar flux
and the weighted kinetic--dissipation endpoint.  It is not a resolution of
the Millennium problem.
**NOT CLAY.**
