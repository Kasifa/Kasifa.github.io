# R0.71K — A fixed aligned matched partition preserves the two-power localized heat-payment gap

## 0. Status and scope

This report closes one finite gate left by R0.71J.  It does not prove a new
regularity criterion and does not construct a singularity.

R0.71J used one global spatial cell.  The present calculation replaces that
cell by a fixed, smooth, scale-covariant, bounded-overlap partition at the
matched radius.  On the selected broad parent of the same global-smooth 2D3C
NSE family, the partition has \(K^3\) cells.  Translation symmetry makes the
initial work zero in every cell, not merely after summation.  At the end of
the parabolic window, the aggregate localized amplitude remains bounded below.

The resulting finite-cell positive creation is \(\gtrsim K^{-2}\), whereas
the same bounded-overlap local heat/support payment is
\(O((\nu K^4)^{-1})\).  Thus this fixed matched localization preserves the
R0.71J two-power gap.

Every cutoff--curl and viscous-collar term is retained.  The viscous collar is
itself leading order and can contribute at the \(K^{-2}\) scale.  The result
therefore rejects only heat-only payment.  It does not reject a genuinely
independent collar-, shape-, face-, or refresh-paid estimate.

## 1. Main statement

Work on \(\mathbb T^3\) with normalized Haar measure.  Let

\[
 L=\mathbb P(u\times\omega),
 \qquad \omega=\nabla\times u,
 \qquad Y=\|\omega\|_2^2.
\]

Use the fixed broad parent-only tight frame from R0.71E and R0.71J, with
parent scales \(\kappa_j=2^j\).  Put

\[
 F_j=T_jL,
 \qquad W_j=T_j\omega.
\]

For a cell cutoff \(\chi_{j,Q}\), define

\[
 C_{j,Q}=\nabla\times(\chi_{j,Q}W_j),
 \qquad d_{j,Q}=\|C_{j,Q}\|_2^2,
\]

\[
 B_{j,Q}=\langle F_j,C_{j,Q}\rangle,
 \qquad
 q_{j,Q}=\frac{(B_{j,Q}^+)^2}{d_{j,Q}},
 \qquad
 a_{j,Q}=\frac{q_{j,Q}}Y.
\]

On \(d_{j,Q}>0\), let

\[
 \rho_{j,Q}=\sqrt{d_{j,Q}},
 \qquad E_{j,Q}=\frac{C_{j,Q}}{\rho_{j,Q}},
 \qquad
 z_{j,Q}=\frac{\langle F_j,E_{j,Q}\rangle}{\sqrt Y}.
\]

Then \(a_{j,Q}=(z_{j,Q}^+)^2\).  With

\[
 N_j=F_{j,t}+\nu\kappa_j^2F_j,
 \qquad
 M_{j,Q}=C_{j,Q,t}+\nu\kappa_j^2C_{j,Q},
\]

and \(P_{j,Q}=I-E_{j,Q}\otimes E_{j,Q}\), define the complete signed source

\[
 \mathcal J_{j,Q}
 =\frac1{\sqrt Y}\left(
 \langle N_j,E_{j,Q}\rangle
 +\frac{\langle P_{j,Q}F_j,P_{j,Q}M_{j,Q}\rangle}{\rho_{j,Q}}
 \right)
 -\frac{Y_t}{2Y}z_{j,Q}.
 \tag{1.1}
\]

No radial, tangent, collar, or normalization row is separately truncated
before the positive part of \(\mathcal J_{j,Q}\) is taken.

Let

\[
 \theta_* =\frac{\log2}{18},
 \qquad
 I_K=\left[0,\frac{\theta_*}{\nu K^2}\right],
\]

and let

\[
 A_*
 =\frac{4}{
 57(2^{1/9}+44)
 (3\,2^{1/9}+4\,2^{7/9}+120)}
 =1.1965465392386773\times10^{-5}.
 \tag{1.2}
\]

### Theorem 1.1 — fixed aligned matched-cell heat-payment no-go

There is a smooth nonnegative scale-covariant partition family, fixed before
the data, with overlap at most \(N\), matched radii
\(r_j=\rho/\kappa_j\), and constants \(C_0,C_1\) such that

\[
 \sum_Q\chi_{j,Q}=1,
 \qquad
 \sum_Q\chi_{j,Q}^2\le C_0,
 \qquad
 \sum_Q|\nabla\chi_{j,Q}|^2\le C_1r_j^{-2}.
 \tag{1.3}
\]

Set

\[
 C_{\rm part}=2C_0+\frac{4C_1}{\rho^2}.
 \tag{1.4}
\]

For every fixed viscosity \(\nu>0\), use the R0.71J global-smooth fixed-energy
2D3C family and all sufficiently large dyadic \(K\).  On its selected parent
\(\kappa=4K\), the \(K^3\) aligned cells satisfy

\[
 d_{\kappa,Q}>0\quad\hbox{on }I_K,
 \qquad
 a_{\kappa,Q}(0)=0.
 \tag{1.5}
\]

The finite selected-cell positive creation obeys

\[
 \boxed{
 \mathcal Z_K^{\rm sel,loc}
 :=\kappa^{-2}\sum_Q\int_{I_K}
 z_{\kappa,Q}^+\mathcal J_{\kappa,Q}^+\,dt
 \ge\frac{A_*}{64C_{\rm part}K^2}.}
 \tag{1.6}
\]

Define the complete bounded-overlap local heat/support payment by the
nonnegative Tonelli sum

\[
 \mathcal H_K^{\rm loc}
 :=\sum_j\kappa_j^{-2}\int_{I_K}
 \frac{\sum_Q
 \|1_{\operatorname{supp}\chi_{j,Q}}F_j\|_2^2}{Y}\,dt.
 \tag{1.7}
\]

Then

\[
 \boxed{
 \mathcal H_K^{\rm loc}
 \le
 \frac{N(1-2^{-1/9})}{2\nu K^4}.}
 \tag{1.8}
\]

Consequently

\[
 \boxed{
 \frac{\mathcal Z_K^{\rm sel,loc}}
 {\mathcal H_K^{\rm loc}}
 \ge
 \frac{\nu A_*}{
 32C_{\rm part}N(1-2^{-1/9})}K^2.}
 \tag{1.9}
\]

The denominator in (1.9) may be zero only if the local heat payment is zero;
in that case (1.6) makes the no-go stronger.  Any full-frame/full-cell
positive-creation quantity defined as the supremum of finite nonnegative
truncations is at least (1.6).  No infinite frame--cell evolution identity is
used in that observation.

## 2. What R0.71F had already proved

R0.71F already established the complete moving-cutoff projected-Lamb ledger,
the equality of its projected and material forms, and the matched local
quotient

\[
 q_{j,Q}=\frac{((B^L_{j,Q})^+)^2}{
 \|\nabla\times(\chi_QW_j)\|_2^2}.
\]

It proved

\[
 \sum_Qd_{j,Q}\lesssim D_j,
 \qquad
 \frac{(b_j^+)^2}{D_j}\lesssim\sum_Qq_{j,Q},
 \qquad
 \sum_Qq_{j,Q}\le N\|F_j\|_2^2,
 \tag{2.1}
\]

and obtained an unconditional local heat-height packing estimate.  It also
showed that a matched partition cannot hide the critical bottom-trace cost of
a different six-mode low block.

R0.71K does not repeat those statements.  Its new finite question is temporal:
does the R0.71J zero-entry positive joint creation survive after every global
cell is replaced by matched spatial cells?  The answer is yes for one fixed
aligned scale-covariant partition family.  This adds a cellwise zero entry,
strict denominators over the physical-time window, and a positive-creation
lower bound for the broad-parent witness.

## 3. A fixed scale-covariant partition

Choose \(h\in C_c^\infty(\mathbb R)\), \(h\ge0\), such that

\[
 \sum_{n\in\mathbb Z}h(y-2\pi n)=1.
 \tag{3.1}
\]

One explicit choice is obtained from

\[
 g(y)=
 \begin{cases}
 \exp[-(1-(2y/3\pi)^2)^{-1}],&|y|<3\pi/2,\\
 0,&|y|\ge3\pi/2,
 \end{cases}
\]

by setting

\[
 h(y)=\frac{g(y)}{\sum_{n\in\mathbb Z}g(y-2\pi n)}.
 \tag{3.2}
\]

Let \(\eta(y)=h(y_1)h(y_2)h(y_3)\).  For a dyadic parent
\(\kappa_j\ge4\), put \(M_j=\kappa_j/4\), and for
\(Q\in(\mathbb Z/M_j\mathbb Z)^3\) define the periodic atom

\[
 \chi_{j,Q}(x)
 =\sum_{\ell\in\mathbb Z^3}
 \eta\!\left(
 \frac{\kappa_j}{4}x-2\pi Q-2\pi M_j\ell
 \right).
 \tag{3.3}
\]

The atoms sum to one because the pair \((Q,\ell)\) parametrizes
\(\mathbb Z^3\).  Their lattice spacing is \(8\pi/\kappa_j\), their support
radius is \(\rho/\kappa_j\) for a fixed \(\rho\), and their derivative
constants scale as \(\kappa_j^{|\alpha|}\).  The explicit tensor template has
overlap at most eight.  The finitely many parents below \(\kappa_j=4\) may be
assigned any fixed finite smooth partition; they play no role in the lower
bound.

At the selected parent \(\kappa=4K\), equation (3.3) has exactly \(K^3\)
cells with lattice spacing \(2\pi/K\).  This is a single fixed dyadic rule,
not a partition tuned separately after inspecting each datum.

## 4. Exact equal-cell identities

The R0.71J solution has the 2D3C form

\[
 u=(0,V(x_1,t),w(x_1,x_2,t)).
\]

Every Fourier frequency remains in

\[
 K\mathbb Z\times K\mathbb Z\times\{0\}.
 \tag{4.1}
\]

This follows exactly from the passive advection--diffusion equation for
\(w\): multiplication by the shear shifts only the first frequency by
\(\pm K\), while the vertical channels remain \(\pm4K\) and \(\pm5K\).
Therefore \(F_\kappa\) and \(W_\kappa\) are invariant under every translation
\(2\pi Q/K\), and the selected cells are translates of one another.

Set

\[
 D_{\rm loc}=\sum_Qd_{\kappa,Q}.
\]

All selected cell works and denominators are equal.  Since
\(\sum_Q\chi_{\kappa,Q}=1\),

\[
 \sum_QC_{\kappa,Q}
 =\nabla\times W_\kappa,
 \qquad
 \sum_QB_{\kappa,Q}=B_\kappa.
 \tag{4.2}
\]

Hence

\[
 \boxed{
 B_{\kappa,Q}=\frac{B_\kappa}{K^3},
 \qquad
 d_{\kappa,Q}=\frac{D_{\rm loc}}{K^3}.}
 \tag{4.3}
\]

Whenever \(B_\kappa\ge0\),

\[
 \boxed{
 \sum_Qq_{\kappa,Q}
 =\frac{B_\kappa^2}{D_{\rm loc}}.}
 \tag{4.4}
\]

This is stronger than the general reverse-Cauchy lower bound because exact
translation symmetry eliminates unequal-cell losses.

## 5. The denominator bound and strict positivity

The product rule gives

\[
 C_{\kappa,Q}
 =\chi_{\kappa,Q}\nabla\times W_\kappa
 +\nabla\chi_{\kappa,Q}\times W_\kappa.
 \tag{5.1}
\]

Therefore (1.3) yields

\[
 \begin{aligned}
 D_{\rm loc}
 &\le2C_0\|\nabla\times W_\kappa\|_2^2
 +2C_1r^{-2}\|W_\kappa\|_2^2.
 \end{aligned}
 \tag{5.2}
\]

The broad parent is supported in
\(|\xi|\ge\kappa/\sqrt2\), so

\[
 \|\nabla\times W_\kappa\|_2^2
 \ge\frac{\kappa^2}{2}\|W_\kappa\|_2^2.
 \tag{5.3}
\]

With \(r=\rho/\kappa\), equations (5.2)--(5.3) prove

\[
 \boxed{
 D_{\rm loc}\le C_{\rm part}D_\kappa,
 \qquad
 C_{\rm part}=2C_0+4C_1/\rho^2.}
 \tag{5.4}
\]

R0.71J proved that \(D_\kappa>0\) on the fixed window for all sufficiently
large dyadic \(K\).  If one selected local denominator vanished, translation
symmetry would make every local denominator vanish.  Equation (4.2) would
then imply \(\nabla\times W_\kappa=0\), contradicting \(D_\kappa>0\).
Thus every selected denominator is strictly positive, and no denominator
face occurs on \(I_K\).

## 6. Localized endpoint lower bound

At the initial trace, R0.71J gives \(B_\kappa(0)=0\).  Equation (4.3) now gives

\[
 B_{\kappa,Q}(0)=q_{\kappa,Q}(0)=a_{\kappa,Q}(0)=0
 \tag{6.1}
\]

for every selected cell.

At \(t_*=\theta_*/(\nu K^2)\), R0.71J gives

\[
 a_\kappa(t_*)
 =\frac{(B_\kappa^+)^2}{D_\kappa Y}
 \ge\frac{A_*}{2}
 \tag{6.2}
\]

for all sufficiently large dyadic \(K\).  Combining (4.4), (5.4), and (6.2)
gives

\[
 \boxed{
 A_{\rm loc}^{\rm sel}(t_*)
 :=\sum_Qa_{\kappa,Q}(t_*)
 =\frac{(B_\kappa^+)^2}{D_{\rm loc}Y}
 \ge\frac{A_*}{2C_{\rm part}}.}
 \tag{6.3}
\]

Thus matched localization changes a constant but not the scale of the
positive endpoint.

## 7. Complete fixed-cutoff time ledger

For a fixed spatial cutoff,

\[
 R=(\partial_t+V_r\cdot\nabla)\chi
 =V_r\cdot\nabla\chi,
\]

so the Eulerian cutoff-motion combination

\[
 R-V_r\cdot\nabla\chi
\]

vanishes exactly.  This is the only transport row removed by fixing the
partition.  The field/projective tangent row in (1.1) generally remains.

The complete localized-vorticity equation is

\[
 \begin{aligned}
 C_{j,Q,t}={}&\nu\Delta C_{j,Q}
 +\nabla\times\left(
 \chi_{j,Q}\sum_{k,\ell}\mathfrak G_{k\ell,j}
 \right)\\
 &-\nu\nabla\times(\mathcal K_{\chi_{j,Q}}W_j),
 \end{aligned}
 \tag{7.1}
\]

where

\[
 \mathcal K_\chi W
 =2\sum_m(\partial_m\chi)\partial_mW+(\Delta\chi)W.
 \tag{7.2}
\]

All frequency-pair interactions are retained in
\(\mathfrak G_{k\ell,j}\).  The last term is the viscous collar.  It remains
inside \(M_{j,Q}\), hence inside the radial/tangent combination in
\(\mathcal J_{j,Q}\).

Direct differentiation gives the hard scalar equation

\[
 z_{j,Q,t}+\nu\kappa_j^2z_{j,Q}=\mathcal J_{j,Q},
 \tag{7.3}
\]

and therefore

\[
 a_{j,Q,t}+2\nu\kappa_j^2a_{j,Q}
 =2z_{j,Q}^+\mathcal J_{j,Q}.
 \tag{7.4}
\]

Writing \(\mathcal J=\mathcal J^+-\mathcal J^-\), equation (7.4) becomes

\[
 \boxed{
 2\kappa_j^{-2}z_{j,Q}^+\mathcal J_{j,Q}^+
 =\kappa_j^{-2}a_{j,Q,t}
 +2\nu a_{j,Q}
 +2\kappa_j^{-2}z_{j,Q}^+\mathcal J_{j,Q}^-.}
 \tag{7.5}
\]

Every term after the endpoint derivative is nonnegative.  Equation (7.5)
does not split radial and tangent positive parts and therefore preserves their
actual cancellation.

## 8. Proof of the positive-creation lower bound

Sum (7.5) over the finite \(K^3\) selected cells and integrate over \(I_K\).
Using (6.1) and dropping the two nonnegative defect terms gives

\[
 2\mathcal Z_K^{\rm sel,loc}
 \ge\kappa^{-2}A_{\rm loc}^{\rm sel}(t_*).
 \tag{8.1}
\]

Since \(\kappa=4K\), equation (6.3) yields

\[
 \mathcal Z_K^{\rm sel,loc}
 \ge
 \frac12\frac1{16K^2}\frac{A_*}{2C_{\rm part}}
 =\frac{A_*}{64C_{\rm part}K^2}.
 \tag{8.2}
\]

This proves (1.6).  The argument is finite and uses no frame--cell limit.

## 9. Proof of the local heat/support upper bound

Bounded overlap gives, for every parent,

\[
 \sum_Q
 \|1_{\operatorname{supp}\chi_{j,Q}}F_j\|_2^2
 \le N\|F_j\|_2^2.
 \tag{9.1}
\]

R0.71J proved for the same complete broad parent frame and 2D3C family that

\[
 \sum_j\kappa_j^{-2}\int_{I_K}
 \frac{\|F_j\|_2^2}{Y}\,dt
 \le\frac{1-2^{-1/9}}{2\nu K^4}.
 \tag{9.2}
\]

Equations (9.1)--(9.2) prove (1.8).  Cellwise Cauchy also gives

\[
 \sum_Qa_{j,Q}
 \le\frac{
 \sum_Q\|1_{\operatorname{supp}\chi_{j,Q}}F_j\|_2^2}{Y},
 \tag{9.3}
\]

so the same bound controls the physical-time mass of the localized amplitudes.
It still cannot control their positive source because the endpoint in (8.1)
is two powers larger after the outer frame weight.

## 10. Independent scale ledger

Each selected cell has volume \(K^{-3}\).  On the parabolic window,

\[
 F_\kappa=O(K),
 \qquad
 W_\kappa=O(K)
\]

pointwise.  Both pieces of (5.1) are \(O(K^2)\) pointwise.  Thus

\[
 \|C_{\kappa,Q}\|_2=O(K^{1/2}),
 \qquad
 d_{\kappa,Q}=O(K),
 \qquad
 B_{\kappa,Q}=O(1).
\]

Consequently

\[
 q_{\kappa,Q}=O(K^{-1}),
 \qquad
 a_{\kappa,Q}=O(K^{-3}),
 \qquad
 z_{\kappa,Q}=O(K^{-3/2}).
 \tag{10.1}
\]

The complete nominal derivatives satisfy

\[
 \|N_\kappa\|_{L^2(Q)}=O(\nu K^{3/2}),
 \qquad
 \|M_{\kappa,Q}\|_2=O(\nu K^{5/2}),
\]

which gives

\[
 \mathcal J_{\kappa,Q}=O(\nu K^{1/2}).
 \tag{10.2}
\]

Hence \(z_Q\mathcal J_Q=O(\nu K^{-1})\) per cell.  Multiplying by
\(dt=O((\nu K^2)^{-1})\) and \(\kappa^{-2}=O(K^{-2})\) gives
\(O(K^{-5})\) per cell, or \(O(K^{-2})\) after the \(K^3\)-cell sum.

The support heat density is \(O(K^{-3})\) per cell after division by \(Y\).
After the same physical-time and frame weights it is
\(O((\nu K^7)^{-1})\) per cell, or \(O((\nu K^4)^{-1})\) after summation.
The independent checker obtains exact successive factors four in the ratio
when \(K\) doubles.

## 11. The collar is leading, not a hidden gain

At matched radius,

\[
 \nabla\chi=O(K),
 \qquad
 \Delta\chi=O(K^2).
\]

The cutoff--curl part \(\nabla\chi\times W\) in (5.1) is the same size as the
interior curl.  Interior, collar-square, and cross contributions to \(d_Q\)
are all \(O(K)\) per cell and \(O(K^4)\) after summation.

The viscous collar in (7.1) is \(O(\nu K^4)\) pointwise and
\(O(\nu K^{5/2})\) in one-cell \(L^2\).  Its contribution to the complete
source can therefore be \(O(\nu K^{1/2})\) per cell.  After the same
weighting and integration as in (8.2), its aggregate absolute contribution
can be \(O(K^{-2})\).

This has two consequences:

1. the collar cannot be discarded as lower order; and
2. the present theorem cannot reject a separate collar-paid estimate merely
   from scaling, because the collar is large enough to pay the creation.

R0.71F already showed that the cutoff--curl collar has no universal sign.
Here it remains inside the exact signed joint source.  Calling its absolute
value a new right-hand-side budget would not by itself close the route: one
would still have to derive that budget from a quantity available at the
Leray level without simply restating \(\mathcal J_Q\).

Fixed cutoffs make the cutoff-motion and refresh rows zero.  They do not make
the projective tangent term

\[
 \langle P_QF_Q,P_QM_Q\rangle/\rho_Q
\]

zero.  That angular row remains leading and is included in (1.1).

## 12. Independent numerical audit

The independent checker uses the explicit partition (3.2), direct Fourier
convolution, and a tensor 360-point Gauss--Legendre quadrature.  It imports
neither the SymPy producer nor the repository Fourier helper.

At \(\theta=0\), it reconstructs

\[
 B=0,
 \qquad D=3942,
 \qquad Y=178.
\]

At \(\theta_*\), it obtains

\[
 B=0.5400298694461556,
 \quad D=693.8204950994357,
 \quad Y=35.12843837102585,
\]

and hence

\[
 B^2/(DY)=1.1965465392386885\times10^{-5}.
\]

The complete one-cell denominator, including every cutoff--curl component and
cross term, gives

\[
 \frac{D_{\rm loc}}{D}=0.7182690194
 \quad(\theta=0),
 \qquad
 \frac{D_{\rm loc}}{D}=0.7246675861
 \quad(\theta=\theta_*).
\]

The endpoint one-cell work differs from the global normalized work by only
\(2.27\times10^{-10}\), the quadrature residual of an exact translation
identity.  These numerical values are diagnostics, not inputs to the theorem;
the proof uses (5.4).

## 13. Literature boundary

The closest classical and current sources concern related but different
localization objects.

1. [Dascaliuc--Grujić](https://arxiv.org/abs/1101.2193) use refined physical
   covers and ensemble-averaged local energy flux for suitable weak NSE
   solutions under a Taylor-scale condition.  Their object is a linear signed
   flux, not the positive-part-square/local-denominator quotient.
2. [Leitmeyer](https://arxiv.org/abs/1502.01258) gives refined test functions,
   bounded multiplicity, and conditional enstrophy-cascade estimates.  The
   matched/refined partition technology is established; the normalized
   projected-Lamb quotient is different.
3. [Tao](https://arxiv.org/abs/1108.1165) uses moving cutoffs to control local
   transport leakage and explicitly retains collars.  R0.71K does not claim a
   first transported-cutoff or collar ledger.
4. [Eyink--Aluie](https://arxiv.org/abs/0909.2386) develop smooth
   space--scale coarse-graining and Germano flux telescopes under cascade
   scaling assumptions.  Ordinary signed flux locality is not the target
   quantity here.
5. [Yu, 2026 preprint](https://arxiv.org/abs/2606.27560v1) studies positive
   filtered vortex stretching, filtered palinstrophy, commutator defects, and
   localization residuals.  Its localization budgets have no automatic
   coercive contribution, and its unweighted closure uses additional
   summability hypotheses.  It does not contain the matched cellwise
   projected-Lamb quotient, denominator faces, or refresh ledger.

The full ten-source comparison is recorded in
`research/r071k_literature_audit.md`.  That bounded primary-source search did
not locate an isomorphic theorem.  This is not an originality or priority
claim.

## 14. What is closed and what remains open

### 14.1 Closed in R0.71K

1. A fixed smooth scale-covariant matched partition can be aligned with the
   R0.71J broad-parent witness.
2. Every selected cell has exact zero initial work.
3. Every selected denominator is positive on the parabolic window; there are
   no selected-cell denominator faces.
4. The localized endpoint satisfies a \(K\)-uniform positive lower bound.
5. The finite selected-cell positive creation is at least
   \(A_*/(64C_{\rm part}K^2)\).
6. The complete bounded-overlap local heat/support payment is at most
   \(N(1-2^{-1/9})/(2\nu K^4)\).
7. The ratio therefore grows at least as a fixed positive multiple of
   \(\nu K^2\).
8. Cutoff--curl, denominator collar, viscous collar, tangent, and
   normalization rows have all been retained.

### 14.2 Not closed

1. The theorem does not cover arbitrary phase-misaligned matched partitions.
   Their endpoint aggregate is still bounded below, but their cellwise initial
   work need not vanish.
2. Moving/deforming partitions and their distortion costs are not covered.
3. General denominator faces and refresh atoms are not paid.
4. The absolute viscous collar is not bounded by a Leray-level quantity.
5. No infinite frame--cell hard/soft evolution identity is proved.
6. No child-refined frequency frame theorem is proved.
7. No unconditional weighted-BV continuation criterion follows.
8. No global regularity or finite-time singularity conclusion follows.

## 15. Route verdict and next finite gate

The fixed matched-localization escape left by R0.71J is now closed for one
explicit aligned partition family:

\[
 \text{same bounded-overlap local heat/support payment}
 \not\Longrightarrow
 \text{uniform payment of localized positive joint creation}.
 \tag{15.1}
\]

Localization has not produced a free coercive defect.  It has exposed a
leading viscous collar and a leading projective tangent row.  These terms may
be large enough to pay the positive creation, but no unconditional estimate
for them has been obtained.

The next finite gate is R0.71L: isolate the fixed-cell viscous-collar and
tangent contributions without taking their positive parts separately, and
test whether their weighted absolute budget follows from an existing
Leray-level NSE quantity.  If the only available bound restates the complete
source or costs an uncontrolled derivative, the temporal-residence branch
should stop.  Faces, refresh atoms, moving cells, and infinite soft limits
remain later questions and should not be entered before that fixed-cell gate.

## 16. Reproduction and evidence map

`research/r071k_exact_audit.py` is the exact symbolic producer.  It checks the
equal-cell quotient algebra, the analytic partition constant, the endpoint
lower bound, the positive-defect coefficient, the local heat bound, the
\(K^2\) separation, and the complete scale-exponent ledger.

`research/r071k_independent_audit.py` independently reconstructs the
pure-heat Fourier field and the explicit smooth partition, then evaluates the
complete one-cell cutoff--curl denominator with Gauss--Legendre quadrature.
It also checks zero entry, the endpoint amplitude, and successive \(K^2\)
ratios.

`research/r071k_independent_audit.md` explains the independent derivation,
while `research/r071k_gap_matrix.md` records the exact closed/open quantifiers.
The certificate bundle pins both machine-readable results and their hashes.

No DNS, fitted model, stochastic simulation, GPU calculation, or DGX run is
used.  Exact Fourier algebra and finite deterministic quadrature are stronger
and more transparent evidence for this structural gate.
