# R0.71T bounded primary-source audit: internal zeros, variation, and occupation

**Search date:** 2026-08-26
**Question:** which established results justify the positive-time
implicit-function construction, and does any checked NSE, parabolic,
variation, or crossing theorem pay the raw fixed zero-level entry atom from a
Leray-class budget?

## 1. Bounded answer

The standard local strong-solution theory supplies the smooth fixed-time flow
map needed for the finite-dimensional implicit-function construction.  After
that input, the R0.71T internal full-shell root and its positive entry follow
from an elementary finite-dimensional transversality calculation.

No checked primary source supplies the second, much stronger implication

\[
 \text{raw entries at the fixed level }C=0
 \quad\Longrightarrow\quad
 \text{a uniform sum paid by the bare Leray budget}.
\]

The nearest established mechanisms control different objects:

1. local energy, dissipation, and the size of the singular set;
2. ensemble- and time-averaged energy flux;
3. upper parabolic Carleson norms for small critical data;
4. maximal regularity when the forcing already belongs to a strong
   \(L^p\) class;
5. total or truncated variation and crossing counts averaged over the level;
6. expected crossings for a random process with a specified probability law.

A fixed smooth packet coefficient does admit a Leray-paid
**amplitude-weighted excursion** bound.  That result does not control the
number of arbitrarily shallow zero entries.  The distinction is both
functional and scale-theoretic, and the genuine internal scaling family shows
that the bare normalized \(\dot H^{-1}\)-Lamb time integral cannot pay the
R0.71P atom with a uniform constant.

The search was bounded to two focused waves: local NSE flow-map and analytic
regularity results, followed by local-energy/Carleson/variation/crossing
interfaces.  Failure to locate a theorem is not a claim of nonexistence,
novelty, or priority.

## 2. Standard flow-map input used by the internal construction

Let \(s>5/2\), and take smooth zero-mean divergence-free initial data on the
three-torus.  On a common short interval, the classical NSE solution depends
continuously and differentiably on a finite-dimensional family of such data.
At the zero solution, the derivative of the fixed-time map is the Stokes heat
semigroup.

R0.71T uses only this local statement.  If \(E_j\) is the finite real
target-shell space and \(R_j:E_j\to H^{s+2}_\sigma\) is a right inverse of
\(T_j\operatorname{curl}\), then

\[
 \Phi(a,w)=T_j\operatorname{curl}S_\tau(aU+R_jw)
\]

has

\[
 D_w\Phi(0,0)=e^{\nu\tau\Delta}|_{E_j}.
\]

The latter is an invertible matrix on a finite annulus.  The ordinary
finite-dimensional implicit-function theorem therefore prescribes a small
initial target-shell correction.  No backward NSE solution, infinite-
dimensional local surjectivity, or global regularity theorem is invoked.

### 2.1 Fujita--Kato

**Source.** Hiroshi Fujita and Tosio Kato, *On the Navier--Stokes initial
value problem. I*, Archive for Rational Mechanics and Analysis **16** (1964),
269--315. [DOI 10.1007/BF00276188](https://doi.org/10.1007/BF00276188).

**Relevant scope.** The paper establishes local and small-data theory through
the Stokes semigroup in critical/strong settings.  Its semigroup formulation
is the classical foundation for differentiating the mild solution with
respect to smooth finite-dimensional initial parameters.

**Boundary.** It gives no zero-entry count or payment theorem.

### 2.2 Kato

**Source.** Tosio Kato, *Strong \(L^p\)-solutions of the Navier--Stokes
equation in \(\mathbb R^m\), with applications to weak solutions*,
Mathematische Zeitschrift **187** (1984), 471--480.
[DOI 10.1007/BF01174182](https://doi.org/10.1007/BF01174182),
[EUDML record](https://eudml.org/doc/173504).

**Relevant scope.** The mild-solution contraction and smoothing estimates
support smooth dependence on small finite-dimensional perturbations in the
strong class.  The periodic version used here follows by the corresponding
torus Stokes semigroup construction.

**Boundary.** The release does not transfer a whole-space theorem verbatim to
the torus; it uses the standard periodic analogue for smooth data.

### 2.3 Temam

**Source.** Roger Temam, *Navier--Stokes Equations and Nonlinear Functional
Analysis*, 2nd ed., SIAM, 1995.
[Open book PDF](https://ftp.mi.fu-berlin.de/pub/klima/NavierStokes/Temam-NavierStokesEquationsAndNonlinearFunctionalAnalysis.pdf).

**Relevant scope.** The periodic weak formulation and energy inequality give
the fixed-test-function identity below.  The book also records time
analyticity on intervals where the solution is strong.  Thus one nontrivial
finite Fourier observable has isolated zeros on a compact classical
subinterval.

**Boundary.** Analyticity gives neither a solution-independent lower
separation of zeros nor a uniform count over shells, cells, or a maximal-time
limit.

## 3. A Leray-paid quantity that is actually available

Let \(u\) be a periodic Leray--Hopf solution, let
\(I=[s,t]\Subset(0,T)\), and fix a smooth divergence-free packet \(\psi\).
Set

\[
 a_\psi(\tau)=\langle u(\tau),\psi\rangle,
 \qquad
 E_I=\operatorname*{ess\,sup}_{\tau\in I}\|u(\tau)\|_2^2,
 \qquad
 D_I=\int_I\|\nabla u\|_2^2\,d\tau.
\]

The weak equation gives, in the distributional and then absolutely continuous
sense,

\[
 a_\psi'
 =-\nu(\nabla u,\nabla\psi)
 +\int_{\mathbb T^3}u\otimes u:\nabla\psi\,dx.
\]

Consequently \(a_\psi\in W^{1,2}(I)\) and

\[
 \boxed{
 V_I^+(a_\psi)
 \le
 \nu\|\nabla\psi\|_2(|I|D_I)^{1/2}
 +\|\nabla\psi\|_\infty E_I|I|.}
 \tag{3.1}
\]

If \((\alpha_k,\beta_k)\) are the internal connected components of
\(\{a_\psi>0\}\), excluding a component beginning at \(s\), and

\[
 m_k=\sup_{(\alpha_k,\beta_k)}a_\psi,
\]

then

\[
 \sum_km_k\le V_I^+(a_\psi),
 \qquad
 N_\delta\le\delta^{-1}V_I^+(a_\psi).
 \tag{3.2}
\]

This is a genuine internal dynamical charge: every excursion must pay its
height.  It does not pay a raw zero crossing.  Indeed

\[
 g_N(\tau)=N^{-1}\sin(N\tau),\qquad 0\le\tau\le2\pi,
\]

has uniformly bounded total variation and \(L^2\) derivative but \(N\)
positive zero entries.  This scalar example refutes only a functional
inference from BV or \(W^{1,2}\) to raw counting; it is not an NSE trajectory.

## 4. Primary-source interface ledger

### 4.1 Caffarelli--Kohn--Nirenberg: local energy and singular sets

**Source.** Luis Caffarelli, Robert Kohn, and Louis Nirenberg, *Partial
regularity of suitable weak solutions of the Navier--Stokes equations*,
Communications on Pure and Applied Mathematics **35** (1982), 771--831.
[DOI 10.1002/cpa.3160350604](https://doi.org/10.1002/cpa.3160350604).

**Checked scope.** Suitable weak solutions satisfy the local energy
inequality; suitable scale-normalized smallness conditions yield regularity
and the singular set has controlled parabolic Hausdorff size.

**Mismatch.** The R0.71T internal entry occurs inside a smooth solution.  A
filtered coefficient passing through zero neither creates a singular point
nor forces the positive concentration required by an epsilon-regularity
criterion.  At the constructed smooth event there is no anomalous defect to
charge.

### 4.2 Dascaliuc--Grujić: ensemble and time-averaged flux

**Source.** Radu Dascaliuc and Zoran Grujić, *Energy cascades and flux
locality in physical scales of the 3D Navier--Stokes equations*.
[arXiv:1101.2193](https://arxiv.org/abs/1101.2193),
[DOI 10.1007/s00220-011-1219-8](https://doi.org/10.1007/s00220-011-1219-8).

**Checked scope.** Under a Taylor-microscale condition, optimal-cover
ensembles and long-time averages of a modified physical-space flux are
positive and comparable to the mean enstrophy dissipation in an inertial
range.

**Mismatch.** This is an averaged signed-flux theorem, not a positive lower
charge for every cell, time, direction, or zero entry.  It also uses a
different domain and observation geometry.

### 4.3 Koch--Tataru: critical upper Carleson control

**Source.** Herbert Koch and Daniel Tataru, *Well-posedness for the
Navier--Stokes equations*, Advances in Mathematics **157** (2001), 22--35.
[Author PDF](https://math.berkeley.edu/~tataru/papers/nas.pdf),
[DOI 10.1006/aima.2000.1937](https://doi.org/10.1006/aima.2000.1937).

**Checked scope.** Small \(BMO^{-1}\) data give a unique global solution in
the critical space \(X\), whose norm contains an \(L^\infty\) decay term and
a parabolic-cylinder square-Carleson term.  The nonlinearity maps into the
matched source space \(Y\), and the Duhamel operator maps \(Y\) back to \(X\).

**Mismatch.** These are upper norm and bilinear mapping estimates.  They do
not assert that a smooth directional coefficient has a nonzero amount of
Carleson mass every time it crosses zero.

### 4.4 de Simon: maximal regularity needs a strong forcing class

**Source.** Luciano de Simon, *Un'applicazione della teoria degli integrali
singolari allo studio delle equazioni differenziali lineari astratte del
primo ordine*, Rendiconti del Seminario Matematico della Università di Padova
**34** (1964), 205--223.
[Primary PDF](https://www.numdam.org/item/RSMUP_1964__34__205_0.pdf).

**Checked scope.** For an analytic semigroup on a Hilbert space and forcing
in \(L^p\), \(p>1\), the abstract parabolic solution has the corresponding
maximal regularity.

**Mismatch.** For a general three-dimensional Leray solution, the natural
estimate gives the nonlinearity only in \(L_t^{4/3}V'\), not the strong
\(L_t^2L_x^2\) or differentiated class needed by the R0.71T trace--variation
right side.  Even scalar \(W^{1,2}\) regularity would not count shallow
zero entries.

### 4.5 Bertoin--Yor: occupation for finite-variation paths

**Source.** Jean Bertoin and Marc Yor, *Local times for functions with finite
variation*, Bulletin of the London Mathematical Society **46** (2014),
553--560. [DOI 10.1112/blms/bdu014](https://doi.org/10.1112/blms/bdu014).

**Checked scope.** The paper constructs signed and positive occupation
measures/local times for finite-variation paths.  Crossing information is
integrable with respect to the level.

**Mismatch.** A level-averaged occupation identity does not furnish a
uniform pointwise bound at the distinguished level zero.  R0.71T's outgoing
coarea formula is an exact deterministic zero-level representation, but its
approximating density concentrates like \(\delta^{-1}\).

### 4.6 Łochowski: truncated variation and level-averaged crossings

**Source.** Rafał M. Łochowski, *On a generalisation of the Banach indicatrix
theorem*, Colloquium Mathematicum **148** (2017), 301--313.
[arXiv:1503.01746](https://arxiv.org/abs/1503.01746),
[DOI 10.4064/cm6583-3-2017](https://doi.org/10.4064/cm6583-3-2017).

**Checked scope.** Integrating the number of crossings of a band
\([y,y+c]\) over the level \(y\) recovers a truncated-variation quantity.

**Mismatch.** This supports positive-height or level-averaged charges.  The
limit \(c\downarrow0\) at one prescribed level is exactly where raw counting
loses a uniform variation cost.

### 4.7 Rice: expected crossings under a probability law

**Source.** Stephen O. Rice, *Mathematical analysis of random noise*, Bell
System Technical Journal **23** (1944), 282--332.
[DOI 10.1002/j.1538-7305.1944.tb00874.x](https://doi.org/10.1002/j.1538-7305.1944.tb00874.x).

**Checked scope.** Rice formulas compute an expected crossing count from
joint distributions and differentiability/nondegeneracy assumptions on a
random process.

**Mismatch.** A deterministic NSE trajectory comes with no such probability
law.  The formula is not a pathwise Leray estimate.

## 5. Consequences for the R0.71T candidates

### 5.1 Exact outgoing coarea is a representation, not an a priori bound

For finitely many isolated finite-order zeros, let

\[
 r_\alpha=\|C_\alpha\|_2,
 \qquad
 \xi_\alpha=C_\alpha/r_\alpha,
 \qquad
 q_\alpha=\frac{\langle F_j,\xi_\alpha\rangle_+^2}{Y}.
\]

Then a one-sided mollifier yields

\[
 \sum_{\alpha,t_*}\kappa_j^{-2}A_{\alpha,+}(t_*)
 =\lim_{\delta\downarrow0}
 \sum_\alpha\kappa_j^{-2}\int
 q_\alpha\rho_\delta(r_\alpha)(r_{\alpha,t})_+\,dt.
\]

This formula retains both transverse crossings and even touches.  None of the
checked occupation or maximal-regularity results removes the concentration
factor uniformly for general Leray data.

### 5.2 Symmetric trace--variation is exact but strong

For a fixed entry direction, the exact triangular-kernel identity controls
the trace by a local mean plus \(\int|q_t|\).  Differentiating the normalized
pairing introduces both \(F_{j,t}\) and \(Y_t/Y\).  A finite active-direction
Bessel hypothesis then gives a scale-matched estimate, but its right side is
strictly stronger than the bare Leray budget and its multiplicity constant
can grow with repeated directions.

### 5.3 Amplitude thresholding is the established paid alternative

Equations (3.1)--(3.2) show the robust classical route: impose a positive
excursion height, average over the threshold, or charge the amplitude itself.
The raw R0.71P directional atom deliberately normalizes away that height, so
the theorem does not transfer without changing the target.

## 6. Exact literature boundary

The audit supports these statements with high confidence:

1. standard local strong NSE theory supplies the finite-dimensional
   fixed-time flow-map input used by the IFT construction;
2. a fixed smooth packet coefficient has the energy-paid variation and
   amplitude-excursion estimate (3.1)--(3.2);
3. CKN, physical-scale flux locality, Koch--Tataru, maximal regularity,
   finite-variation occupation, truncated variation, and Rice crossings do
   not state the raw fixed-level entry payment sought here.

The negative search conclusion has medium confidence because the search was
bounded.  No claim is made that every specialized theorem has been found, or
that the R0.71T formulation is new.  No regularity, singularity, or Millennium
Prize conclusion follows from this audit.
