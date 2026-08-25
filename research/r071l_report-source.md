# R0.71L — Fixed-cell viscous fusion removes the apparent free collar, but not the projective tangent

## 0. Status and scope

This report closes the finite gate posed at the end of R0.71K.  It does not
prove a regularity criterion, construct a singularity, or show that every
possible localized estimate must fail.

R0.71K retained the viscous cutoff collar as a leading row and asked whether
its weighted absolute budget could be paid noncircularly by a Leray-level
quantity.  The first answer is algebraic: on a fixed cell the raw collar is
not an independent source.  It cancels exactly with the commutator part of
the localized Laplacian.  The correct viscous object is the fused row

\[
 \nu\,\nabla\times\!\left(\chi_Q(\Delta+\kappa^2)W_j\right).
\]

The second answer is negative for the direct absolute-value route.  Standard
energy pays a weighted sum of the denominator masses and even a much more
strongly weighted square norm of the raw collar.  It does not pay the
normalized angular product that occurs in the projective tangent.  A direct
Cauchy estimate either retains that angular ratio or replaces it by the
normalized projected-Lamb quantity

\[
 \nu\int \frac{\|\mathbb P(u\times\omega)\|_2^2}{\|\omega\|_2^2}\,dt,
\]

which is not supplied by the Leray energy inequality.  Thus rowwise absolute
collar payment is not a new coercive mechanism.  Signed cancellation or an
additional critical input remains possible and is not excluded here.

## 1. Fixed-cell objects

Work on a classical interval on \(\mathbb T^3\), with normalized Haar
measure.  Put

\[
 L=\mathbb P(u\times\omega),\qquad
 Y=\|\omega\|_2^2,
\]

and for the fixed broad-parent frame use

\[
 F_j=T_jL,\qquad W_j=T_j\omega,\qquad \kappa=\kappa_j.
\]

For one fixed cutoff \(\chi_Q\), define the cutoff--curl operator

\[
 \mathsf A_QV:=\nabla\times(\chi_QV),
\]

and set

\[
 C_Q=\mathsf A_QW_j,\qquad
 r_Q=\|C_Q\|_2,\qquad
 E_Q=\frac{C_Q}{r_Q},\qquad
 P_Q=I-E_Q\otimes E_Q.
 \tag{1.1}
\]

Here \(E_Q\otimes E_Q\) is the rank-one orthogonal projector onto
\(\operatorname{span}\{E_Q\}\), while \(P_Q\) is its complementary orthogonal
projector onto \(E_Q^\perp\).  Thus \(P_Q\) is corank one (and generally
infinite rank) in the Hilbert space
\(L^2(\mathbb T^3;\mathbb R^3)\), not a pointwise matrix.  The notation
\(r_Q\) avoids the earlier collision between the partition-radius parameter
and \(\sqrt{d_Q}\).  Throughout the hard-cell calculation \(r_Q>0\).

Normalize the field rather than the individual row:

\[
 x_j=\frac{F_j}{\sqrt Y},\qquad
 z_Q=\langle x_j,E_Q\rangle,
 \qquad a_Q=(z_Q^+)^2.
 \tag{1.2}
\]

Let \(\lambda=\nu\kappa^2\),

\[
 N_j=F_{j,t}+\lambda F_j,
 \qquad M_Q=C_{Q,t}+\lambda C_Q.
 \tag{1.3}
\]

The complete signed source retained since R0.71I is

\[
 \mathcal J_Q
 =\frac1{\sqrt Y}\left(
 \langle N_j,E_Q\rangle
 +\frac{\langle P_QF_j,P_QM_Q\rangle}{r_Q}
 \right)
 -\frac{Y_t}{2Y}z_Q.
 \tag{1.4}
\]

## 2. Main theorem

### Theorem 2.1 — fixed-cell recombination and the no-free-collar boundary

Let \(I=[0,T]\), assume that \(u\) is classical on \(I\), and fix one smooth
scalar cutoff \(\chi_Q\) that is independent of time.  Assume
\(r_Q(t)>0\) for every \(t\in I\).  The identities in items 1--3 below are
pointwise in time for this one fixed hard cell and do not require a partition
of unity.  Write the projected vorticity equation as

\[
 W_{j,t}=\nu\Delta W_j+\mathcal G_j,
 \tag{2.1}
\]

where \(\mathcal G_j\) contains the complete projected nonlinear interaction
ledger.  Then items 1--3 hold exactly.  Item 4 is a separate estimate under
the additional family-level hypotheses stated there.

1. **Viscous/collar fusion**

\[
 \boxed{
 M_Q=\mathsf A_Q\!\left[
 \nu(\Delta+\kappa^2)W_j+\mathcal G_j
 \right].}
 \tag{2.2}
\]

2. **Normalization and projective fusion**

\[
 \boxed{
 \mathcal J_Q
 =\langle x_{j,t}+\lambda x_j,E_Q\rangle
 +\langle P_Qx_j,E_{Q,t}\rangle
 =z_{Q,t}+\lambda z_Q,}
 \tag{2.3}
\]

with

\[
 E_{Q,t}=\frac{P_QM_Q}{r_Q}.
 \tag{2.4}
\]

3. **Exact cancellation test.**  If \(\mathcal G_j=0\) and
\(-\Delta W_j=\kappa^2W_j\), then the fused viscous row in (2.2) vanishes,
\(M_Q=0\), for every fixed cutoff.  The expanded localized-Laplacian row and
the raw viscous collar can nevertheless both be nonzero and cancel exactly.

Consequently the separate nonnegative quantity obtained by taking the
absolute value of the raw collar before recombination is decomposition
dependent.  It is not an intrinsic positive defect of the fixed-cell
quotient.

4. **What Leray energy pays.**  For this estimate, add a separate family-level
hypothesis.  At each scale \(\kappa_j\), let
\(\{\chi_{j,Q}\}_Q\) be a finite, time-independent smooth partition of unity
obtained by translating and scaling one fixed \(C^3\) template at matched
radius \(\kappa_j^{-1}\).  Assume uniformly bounded overlap, the derivative
bounds

\[
 \|\partial^\alpha\chi_{j,Q}\|_\infty
 \le C_\alpha\kappa_j^{|\alpha|},
 \qquad |\alpha|\le3,
\]

and a broad-parent frame square bound
\(\sum_j\|T_jf\|_2^2\le C_{\rm frame}\|f\|_2^2\).  Then

\[
 \nu\int_I\sum_{j,Q}\kappa_j^{-2}\|C_{j,Q}\|_2^2\,dt
 \lesssim \nu\int_I Y(t)\,dt
 \lesssim \|u(0)\|_2^2.
 \tag{2.5}
\]

It also pays a strongly downweighted raw-collar square mass; see (8.3).
Neither estimate implies the weighted absolute projective-tangent budget in
(8.4).  The missing factor is the normalized angular velocity
\(\|P_QM_Q\|_2/r_Q=\|E_{Q,t}\|_2\), multiplied by a normalized local Lamb
field.

The last sentence is an implication boundary, not a theorem that all signed
NSE estimates fail.  It closes only the route using bounded overlap,
Bernstein inequalities, the standard energy inequality, and rowwise absolute
values.

## 3. Proof of viscous fusion

For a fixed scalar cutoff,

\[
 \Delta(\chi_QW_j)
 =\chi_Q\Delta W_j+\mathcal K_{\chi_Q}W_j,
 \tag{3.1}
\]

where

\[
 \mathcal K_{\chi_Q}W_j
 =2\sum_m(\partial_m\chi_Q)\partial_mW_j
 +(\Delta\chi_Q)W_j.
 \tag{3.2}
\]

Since curl commutes with \(\Delta\),

\[
 \Delta C_Q
 =\mathsf A_Q\Delta W_j
 +\nabla\times(\mathcal K_{\chi_Q}W_j).
 \tag{3.3}
\]

The expanded fixed-cutoff ledger writes

\[
 C_{Q,t}
 =\nu\Delta C_Q+\mathsf A_Q\mathcal G_j
 -\nu\nabla\times(\mathcal K_{\chi_Q}W_j).
 \tag{3.4}
\]

Substitution of (3.3) into (3.4) gives

\[
 C_{Q,t}
 =\mathsf A_Q(\nu\Delta W_j+\mathcal G_j).
 \tag{3.5}
\]

Adding \(\nu\kappa^2C_Q\) proves (2.2).  In particular,

\[
 \boxed{
 \nu\left[(\Delta+\kappa^2)C_Q
 -\nabla\times(\mathcal K_{\chi_Q}W_j)\right]
 =\nu\mathsf A_Q(\Delta+\kappa^2)W_j.}
 \tag{3.6}
\]

Equation (3.6) is the exact cancellation that is lost if the two terms on the
left are estimated separately by absolute values.

## 4. A concrete exact-cancellation example

The phenomenon is not merely formal.  On the one-dimensional periodic
profile embedded in three dimensions, take

\[
 W(x)=(0,\sin x_1,0),
 \qquad \chi(x)=1+\varepsilon\cos x_1,
 \qquad 0<\varepsilon<1.
 \tag{4.1}
\]

Then \(-\Delta W=W\), and

\[
 C=\nabla\times(\chi W)
 =(0,0,\cos x_1+\varepsilon\cos2x_1).
 \tag{4.2}
\]

A direct differentiation gives

\[
 (\Delta+1)C=(0,0,-3\varepsilon\cos2x_1),
 \tag{4.3}
\]

and

\[
 \nabla\times(\mathcal K_\chi W)
 =(0,0,-3\varepsilon\cos2x_1).
 \tag{4.4}
\]

Both expanded rows are nonzero, while their difference in (3.6) is exactly
zero.  Therefore a positive ``collar mass'' obtained by separating (4.3) and
(4.4) cannot be interpreted as new localized dissipation.

## 5. Proof of normalization and projective fusion

Differentiate \(x_j=F_jY^{-1/2}\):

\[
 x_{j,t}+\lambda x_j
 =\frac{N_j}{\sqrt Y}-\frac{Y_t}{2Y}x_j.
 \tag{5.1}
\]

Because \(P_QC_Q=0\),

\[
 P_QM_Q=P_QC_{Q,t},
 \qquad
 E_{Q,t}=\frac{P_QC_{Q,t}}{r_Q}
 =\frac{P_QM_Q}{r_Q}.
 \tag{5.2}
\]

Also \(P_QF_j/\sqrt Y=P_Qx_j\).  Inserting (5.1) and (5.2) into
(1.4) proves the first equality in (2.3).  Finally,

\[
 z_{Q,t}
 =\langle x_{j,t},E_Q\rangle
 +\langle x_j,E_{Q,t}\rangle
 =\langle x_{j,t},E_Q\rangle
 +\langle P_Qx_j,E_{Q,t}\rangle,
 \tag{5.3}
\]

since \(E_{Q,t}\perp E_Q\).  This proves the second equality.

Thus the field row, normalization row, and tangent row are coordinate pieces
of one scalar identity.  Their separate positive parts have no invariant
meaning.

## 6. Two refinements for the aligned R0.71K witness

### 6.1 The static cutoff--curl numerator vanishes cellwise

Split

\[
 B_Q=\langle F_j,\chi_Q\nabla\times W_j\rangle
 +\underbrace{\langle F_j,\nabla\chi_Q\times W_j\rangle}_{B_Q^\partial}.
 \tag{6.1}
\]

Fix the single selected broad parent and its finite \(K^3\)-cell tensor
family.  For these cells, the R0.71K translation symmetry makes every
\(B_Q^\partial\) equal.  On the other hand, differentiating the finite
partition-of-unity identity gives

\[
 \sum_QB_Q^\partial
 =\left\langle F_j,
 \left(\sum_Q\nabla\chi_Q\right)\times W_j\right\rangle=0.
 \tag{6.2}
\]

There are finitely many selected cells, so

\[
 \boxed{B_Q^\partial=0}
 \tag{6.3}
\]

for every cell in this finite selected aligned family and every time in the
classical interval.  The argument does not cover arbitrary partitions or an
unchecked full frame.  The cutoff--curl term remains present in the
denominator and in \(E_{Q,t}\); it is only absent from this particular
numerator.

### 6.2 The denominator has a quantitative two-sided bound

Let

\[
 D_{\rm loc}=\sum_Q\|C_Q\|_2^2,
 \qquad D_j=\|\nabla\times W_j\|_2^2.
\]

R0.71K proved \(D_{\rm loc}\le C_{\rm part}D_j\).  Conversely,

\[
 \nabla\times W_j=\sum_QC_Q.
\]

If at most \(N\) supports overlap, pointwise Cauchy gives

\[
 \boxed{
 N^{-1}D_j\le D_{\rm loc}\le C_{\rm part}D_j.}
 \tag{6.4}
\]

All selected cells are translates, hence

\[
 d_Q=\frac{D_{\rm loc}}{K^3}.
 \tag{6.5}
\]

The certified broad-parent limit has \(D_j\asymp K^4\) uniformly on the
fixed parabolic window.  Therefore, for every fixed \(\nu>0\) and all
sufficiently large dyadic \(K\),

\[
 \boxed{c_\nu K\le d_Q\le C_\nu K.}
 \tag{6.6}
\]

This repairs the quantitative lower bound needed by the tangent scale
ledger.  It is special to the aligned witness and is not a lower bound for
arbitrary cells of arbitrary solutions.

## 7. Why the raw collar is leading but not independent

At matched radius \(K^{-1}\),

\[
 |\nabla\chi_Q|\sim K,
 \qquad |\Delta\chi_Q|\sim K^2,
 \qquad |\nabla W_j|\sim K|W_j|.
\]

Thus both

\[
 \nu(\Delta+\kappa^2)C_Q
 \quad\hbox{and}\quad
 -\nu\nabla\times(\mathcal K_{\chi_Q}W_j)
\]

can have \(L^2\) size \(\nu K^{5/2}\) in one cell.  The analytic fixed-window
transfer from R0.71J has the more precise form

\[
 z_Q=K^{-3/2}\bigl(\zeta(\theta)+O_\nu(K^{-1})\bigr),
 \qquad
 \mathcal J_{\#,Q}=\nu K^{1/2}
 \bigl(\tau_\#(\theta)+O_\nu(K^{-1})\bigr).
\]

Thus \(z_Q=O_\nu(K^{-3/2})\) uniformly; a two-sided comparison is valid only
on subwindows where \(|\zeta|\) is bounded below.  In particular
\(\zeta(0)=0\) for the aligned zero-entry witness.  With physical-window
length \((\nu K^2)^{-1}\), \(K^3\) selected cells, and the
\(\kappa^{-2}\) weight, a nonvanishing leading coefficient has aggregate
scale \(K^{-2}\).  The standalone quadrature diagnoses, but does not prove,
that nonvanishing or its continuous sign.

This leading scale is correct for each expanded row.  What was missing in
R0.71K is that the rows are two coordinates of the same fused expression.
Leading order does not imply an independent nonnegative payment.

For the explicit pure-heat limit and fixed tensor partition, deterministic
quadrature provides a diagnostic: the collar and localized-heat tangent have
opposite signs, and the collar cancels only a small fraction of the complete
tangent.  This numerical observation is not used in Theorem 2.1 and is not a
continuous sign certificate.

## 8. What the Leray budget controls

### 8.1 Denominator mass

The partition estimates and broad-parent frequency support give

\[
 \sum_Qd_{j,Q}\lesssim \kappa_j^2\|W_j\|_2^2.
 \tag{8.1}
\]

Tight-frame summation and the energy inequality imply

\[
 \nu\int_I\sum_{j,Q}\kappa_j^{-2}d_{j,Q}\,dt
 \lesssim \nu\int_I\sum_j\|W_j\|_2^2\,dt
 \lesssim \nu\int_I Y\,dt
 \lesssim\|u(0)\|_2^2.
 \tag{8.2}
\]

This pays the interior, collar-square, and cross terms after they have been
reassembled into the positive denominator mass.

### 8.2 A downweighted raw-collar square

Let

\[
 \mathcal V_{j,Q}
 =-\nu\nabla\times(\mathcal K_{\chi_Q}W_j).
\]

The uniform third-order cutoff bounds
\(\|\partial^\alpha\chi_{j,Q}\|_\infty
\lesssim\kappa_j^{|\alpha|}\) for \(|\alpha|\le3\), finite overlap, and
Bernstein yield

\[
 \frac1\nu\int_I\sum_{j,Q}\kappa_j^{-6}
 \|\mathcal V_{j,Q}\|_2^2\,dt
 \lesssim \nu\int_I Y\,dt.
 \tag{8.3}
\]

The six inverse powers are essential.  They do not match the quotient weight.

### 8.3 An absolute envelope for the projective product

The positive-branch tangent target naturally contains \(z_{j,Q}^+\).  For a
direct absolute estimate it is convenient to introduce the stronger envelope
below, since \(z_{j,Q}^+\le |z_{j,Q}|\):

\[
 \mathfrak T_{\rm env}^\nu
 =\sum_{j,Q}\kappa_j^{-2}\int
 |z_{j,Q}|\,
 \frac{|\langle P_Qx_j,P_QM_{j,Q}^\nu\rangle|}{r_{j,Q}}\,dt,
 \tag{8.4}
\]

where

\[
 M_{j,Q}^\nu
 =\nu\mathsf A_Q(\Delta+\kappa_j^2)W_j.
\]

An estimate for this envelope also estimates the positive-branch target; a
failure to derive such an envelope estimate is not, by itself, a no-go theorem
for the smaller signed or positive-branch quantity.  Define the hard-cell
condition number

\[
 \Gamma_{j,Q}
 =\frac{\|M_{j,Q}^\nu\|_2}
 {\nu\kappa_j^2r_{j,Q}}.
 \tag{8.5}
\]

Let \(U_{j,Q}\) contain \(\operatorname{supp}\chi_{j,Q}\), and choose these
support neighborhoods so that
\(\sum_Q1_{U_{j,Q}}\le N\) uniformly in \(j\).  Both \(E_Q\) and
\(M_{j,Q}^\nu\) are supported in \(U_{j,Q}\).  Although \(P_QF_j\) need not
be supported there, its restriction obeys

\[
 |z_{j,Q}|\le
 \frac{\|1_{U_{j,Q}}F_j\|_2}{\sqrt Y},
 \qquad
 \|1_{U_{j,Q}}P_QF_j\|_2
 \le2\|1_{U_{j,Q}}F_j\|_2.
\]

Therefore

\[
 \boxed{
 \kappa_j^{-2}|z_{j,Q}|
 \frac{|\langle P_Qx_j,P_QM_{j,Q}^\nu\rangle|}{r_{j,Q}}
 \le
 2\nu\Gamma_{j,Q}
 \frac{\|1_{U_{j,Q}}F_j\|_2^2}{Y}.}
 \tag{8.6}
\]

Even if \(\Gamma_{j,Q}\le\Gamma\) uniformly, bounded overlap and frame
summation lead to

\[
 \mathfrak T_{\rm env}^\nu
 \le2\nu\Gamma N C_{\rm frame}\int_I
 \frac{\|L\|_2^2}{Y}\,dt.
 \tag{8.7}
\]

The right side of (8.7) is a normalized projected-Lamb budget, not the Leray
energy or dissipation.  Without a bound on \(\Gamma\), (8.6) also retains the
same angular ratio that one was trying to control.  Thus this direct estimate
is either stronger than the energy inequality or circular.

## 9. Scaling and functional obstructions

These observations delimit the direct route; they are not NSE blow-up
counterexamples.

### 9.1 NSE scaling on \(\mathbb R^3\)

For

\[
 u_\lambda(t,x)=\lambda u(\lambda^2t,\lambda x),
\]

viscosity is unchanged and

\[
 \|u_{\lambda,0}\|_2^2=\lambda^{-1}\|u_0\|_2^2,
 \qquad
 \nu\int\|\omega_\lambda\|_2^2dt
 =\lambda^{-1}\nu\int\|\omega\|_2^2dt.
 \tag{9.1}
\]

But, writing \(L=\mathbb P(u\times\omega)\),

\[
 \nu\int
 \frac{\|L_\lambda\|_2^2}{\|\omega_\lambda\|_2^2}\,dt
 =\nu\int
 \frac{\|L\|_2^2}{\|\omega\|_2^2}\,dt.
 \tag{9.2}
\]

Hence no universal homogeneous linear estimate of (9.2) by the standard
energy quantity can be scale consistent on \(\mathbb R^3\).  This does not
exclude a signed estimate, a critical additional norm, a domain scale, or a
nonhomogeneous bound with extra information.

### 9.2 Amplitude does not control direction

In an abstract two-dimensional Hilbert space, let

\[
 C_n(t)=n^{-1}(\cos nt\,e_1+\sin nt\,e_2).
 \]

Then \(\|C_n\|=n^{-1}\to0\), but

\[
 \left\|\frac d{dt}\frac{C_n}{\|C_n\|}\right\|=n.
 \tag{9.3}
\]

Thus an upper bound for denominator amplitude cannot by itself control the
projective tangent.  Equation (9.3) is a functional warning only; it is not a
Navier--Stokes solution.

## 10. Independent witness diagnostic

The standalone checker rebuilds the R0.71J pure-heat Fourier limit and the
R0.71K tensor cutoff without importing the exact producer.  In scaled
variables

\[
 y=Kx,\qquad \theta=\nu K^2t,
\]

it evaluates

\[
 \tau_{\rm heat},\qquad
 \tau_{\rm collar},\qquad
 \tau_{\rm tangent}=\tau_{\rm heat}+\tau_{\rm collar},
\]

as well as the radial and normalization rows.  It checks

\[
 \tau_{\rm tangent}-\tau_{\rm heat}-\tau_{\rm collar}=0
\]

numerically and the integrated scalar identity

\[
 \int_0^{\theta_*}\zeta j\,d\theta
 =\frac12\bigl(\zeta(\theta_*)^2-\zeta(0)^2\bigr)
 +16\int_0^{\theta_*}\zeta^2\,d\theta.
 \tag{10.1}
\]

The computed rows are deterministic quadrature diagnostics.  They are useful
for checking signs, constants, and code paths, but they are not interval
proofs of a sign on the entire time window.  The analytic theorem uses only
the exact identities in Sections 3--6.

## 11. Literature boundary

Several neighboring mechanisms are classical, but none supplies the missing
implication used by the direct route.

1. Caffarelli--Kohn--Nirenberg and Dascaliuc--Grujić control scalar local
   energy fluxes with cutoff terms.  Their objects have no local curl
   denominator or Hilbert-space projective tangent.
2. Tao's enstrophy-localization theorem uses local initial-enstrophy
   smallness, a favorable shrinking cutoff, and a quantitative buffer radius.
3. Dascaliuc--Grujić and Leitmeyer obtain conditional enstrophy-cascade
   results using direction coherence, Kraichnan-scale, Morrey, or modulation
   hypotheses beyond the Leray energy inequality.
4. Constantin--Fefferman and Beirão da Veiga--Berselli control a
   magnitude-weighted spatial vorticity-direction quantity under additional
   assumptions.  It is not the temporal direction of a localized projected
   field.
5. Yu's 2026 preprint is the closest adjacent ledger.  It cancels one
   localization residual with a solution-adapted backward adjoint cutoff and
   closes other rows only with increment-defect, Carleson, or shell
   summability inputs.

The full primary-source matrix is in `research/r071l_literature_audit.md`.
The bounded search did not locate a theorem that pays the fixed matched-cell
fused projective tangent from Leray energy alone.  This is a search result,
not a claim of nonexistence, originality, or priority.

## 12. What is closed and what remains open

### 12.1 Closed in R0.71L

1. The fixed-cell viscous collar and localized Laplacian recombine exactly.
2. The field, normalization, and projective rows recombine into
   \(z_t+\nu\kappa^2z\).
3. A monochromatic heat mode gives an exact nontrivial cancellation of the
   two expanded viscous rows.
4. The aligned witness has zero cutoff--curl numerator cell by cell.
5. Its local denominator has a quantitative two-sided bound.
6. Leray energy pays the weighted denominator mass and a more strongly
   downweighted raw-collar square mass.
7. The direct rowwise absolute estimate for the tangent requires an angular
   condition number and a normalized Lamb budget not provided by the energy
   inequality.

### 12.2 Not closed

1. No sign theorem for the complete fused tangent is proved.
2. No continuous sign certificate is claimed for the numerical witness.
3. No general denominator-face or refresh budget is proved.
4. Moving or solution-adapted cutoffs are not treated.
5. No Carleson estimate for the normalized Lamb or increment defects is
   derived from Leray energy.
6. No infinite frame--cell identity or Leray-limit passage is proved.
7. No unconditional weighted-BV continuation criterion follows.
8. No global regularity or finite-time singularity conclusion follows.

## 13. Route verdict and next finite gate

The R0.71K proposal of using an explicit absolute viscous collar as the next
payment is closed:

\[
 \boxed{
 \text{raw collar}+\text{localized heat commutator}
 =\text{one signed fused viscous tangent}.}
 \tag{13.1}
\]

Taking absolute values before (13.1) creates a representation-dependent cost.
After correct fusion, bounded overlap and Leray energy do not pay the
remaining normalized tangent product.

The temporal-residence branch should therefore not proceed directly to
faces, refresh atoms, or moving cells.  The next finite gate is R0.71M:
retain the signed fused tangent and test one scale-critical replacement for
the missing energy estimate, namely a velocity-increment/commutator budget
with an explicit annular or Carleson ledger.  The gate must state the extra
hypothesis exactly and then test whether that hypothesis follows from Leray
energy.  If it does not, it remains a conditional bridge rather than a
regularity result.

## 14. Reproduction and evidence map

`research/r071l_exact_audit.py` checks the universal algebra, the explicit
Helmholtz cancellation, the aligned symmetry consequences, the scale ledger,
and the exact claim boundaries.

`research/r071l_independent_audit.py` independently reconstructs the
pure-heat Fourier witness and fixed tensor partition, evaluates the fused and
split tangent rows by deterministic quadrature, and checks the scalar
identity.  Its numerical signs are diagnostic only.

`research/r071l_independent_audit.md` explains that reconstruction;
`research/r071l_gap_matrix.md` separates exact conclusions from diagnostics
and open implications; `research/r071l_literature_audit.md` records the
bounded primary-source search.

No DNS, fitted model, stochastic simulation, GPU computation, or DGX run is
needed.  Exact algebra is stronger evidence for the recombination theorem,
while deterministic quadrature is retained only as an independent audit of
the explicit witness.
