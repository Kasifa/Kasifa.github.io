# R0.73H report source: gain-normalized planar fixed-distance departure

**Date:** 2026-08-30
**Parent input:** R0.73F moving-bundle fixed-window lower law and the
R0.73G smooth real top-vector launch
**Physical realization:** viscosity one,
\(\overline U_\Lambda(t,y)=(0,0,2\Lambda W(4t,2y))\),
\(K_x=0\), real \(K_z=\pm1\) launch
**Evidence:** continuum nonlinear theorem, one adversarial audit and one
independent analytic audit,
an exact rational continuum subcertificate, a separately labelled finite
Galerkin diagnostic, independent alias-free FFT recomputation, and a sealed
hash ledger

## 0. Direct decision

R0.73H proves a fixed-distance nonlinear departure for a seed normalized by
the **actual selected linear gain**.  Put

\[
 W(d,x)=-\frac12e^{-d}\sin x+\frac14e^{-4d}\sin2x,
 \qquad
 \overline U_\Lambda(t,y)=(0,0,2\Lambda W(4t,2y)),
 \tag{0.1}
\]

and let R0.73F supply

\[
 r=\alpha+\eta>0.17035,
 \qquad D=\min\{d_0,1/450\},
 \qquad T=D/4.
 \tag{0.2}
\]

For the R0.73G real unit launch \(\phi_\Lambda\), define

\[
 G_\Lambda=\|S_{1,\Lambda}(D,0)\phi_\Lambda\|_2.
 \tag{0.3}
\]

There is a fixed \(\delta_0>0\) such that, for every
\(0<\delta\le\delta_0\) and all sufficiently large \(\Lambda\), the exact
solution with

\[
 u_\Lambda^\delta(0)=\frac{\delta}{G_\Lambda}\phi_\Lambda
 \tag{0.4}
\]

is globally smooth and satisfies

\[
 \boxed{
 \|\Pi_{\{K_z=\pm1\}}u_\Lambda^\delta(D)\|_2\ge\frac\delta2.}
 \tag{0.5}
\]

At the same time,

\[
 \|u_\Lambda^\delta(0)\|_{H^3}
 \le C\delta\Lambda^2e^{-r\Lambda D}\longrightarrow0.
 \tag{0.6}
\]

This is a genuine family-level nonlinear departure.  It is not a theorem
for the prescribed seed \(\delta e^{-r\Lambda D}\phi_\Lambda\), because no
matching upper action for \(G_\Lambda\) has been proved.  The background also
varies with \(\Lambda\), so (0.5) is not a Lyapunov-instability theorem for
one fixed background.

## 1. Exact slow-time equation and localized linear orbit

In profile time \(d=4t\), physical velocity obeys

\[
 \partial_du=\mathcal L_\Lambda(d)u+\mathcal B(u,u),
 \qquad
 \mathcal B(f,g)=-\frac14\mathbb P[(f\cdot\nabla)g].
 \tag{1.1}
\]

The factor \(1/4\) comes only from the time change.  In fast time
\(\theta=\Lambda d\), the coefficient is
\(\varepsilon_\nu/4\), with \(\varepsilon_\nu=\Lambda^{-1}\); the Taylor
amplitude \(\delta\) is a separate parameter.

Define the endpoint-normalized linear orbit

\[
 a(s)=G_\Lambda^{-1}S_{1,\Lambda}(s,0)\phi_\Lambda.
 \tag{1.2}
\]

The inverse-evolution estimate inherited from R0.73F gives

\[
 \|a(s)\|_2\le K_{\rm F}e^{-r\Lambda(D-s)},
 \qquad 0\le s\le D,
 \qquad \|a(D)\|_2=1.
 \tag{1.3}
\]

This backward localization, rather than a reversed operator-norm lower
bound, is the quantitative input for every Duhamel layer below.

## 2. Exact harmonic hierarchy

Let

\[
 \begin{aligned}
 \partial_db&=\mathcal L_\Lambda b+\mathcal B(a,a),&b(0)&=0,\\
 \partial_dc&=\mathcal L_\Lambda c
 +\mathcal B(a,b)+\mathcal B(b,a),&c(0)&=0.
 \end{aligned}
 \tag{2.1}
\]

Fourier addition gives the exact supports

\[
 a:\ \pm1,
 \qquad b:\ 0,\pm2,
 \qquad c:\ \pm1,\pm3.
 \tag{2.2}
\]

The cubic return to the positive target row contains the four ordered
paths

\[
 (1,0),\quad(0,1),\quad(-1,2),\quad(2,-1),
 \tag{2.3}
\]

and their real-conjugate partners.  More generally, Taylor order \(j\)
contains only rows congruent to \(j\pmod2\).  Consequently the target row
has neither a quadratic nor a quartic term; after the cubic correction, the
next possible target correction is quintic.

The one-dimensional row formulas were derived directly from the physical
Leray projector and then compared with a generic convolution kernel.  That
comparison verifies the algebra and code path, not a continuum tail.

## 3. Continuum doubled-row energy bound

For nonzero row \(K_z=q\), put \(\gamma=|q|/2\) and

\[
 E_\gamma(v)=\|v'\|_2^2+\gamma^2\|v\|_2^2.
 \tag{3.1}
\]

The universal inviscid numerical-abscissa estimate is \(1/2\).  The
doubled row needs the strict improvement

\[
 \boxed{\omega_1(d)\le\frac13,\qquad0\le d\le D.}
 \tag{3.2}
\]

For either sign, completing the square and applying the periodic unitary
gauge reduces (3.2) to positivity of

\[
 H_d=-\partial_x^2+1-\frac94W_x(d,x)^2.
 \tag{3.3}
\]

At \(d=0\), an exact rational \(|m|\le4\) block has nine positive
fractional \(LDL^*\) pivots and satisfies
\(PH_0P\ge P/5\).  The analytic complement and cross estimates are

\[
 QH_0Q\ge\frac{95}{4}Q,
 \qquad \|PH_0Q\|\le\frac{27}{16}.
 \tag{3.4}
\]

After subtracting \(1/20\), the exact two-block determinant is
\(4527/6400>0\).  Therefore

\[
 H_0\ge\frac1{20}I.
 \tag{3.5}
\]

The explicit time perturbation is at most \(1/40\) for
\(d\le1/450\), hence

\[
 H_d\ge\frac1{40}I.
 \tag{3.6}
\]

The finite rational block is one exact subcertificate inside an
infinite-dimensional analytic tail proof.  It is not being used as a
Galerkin approximation to prove the PDE statement.

## 4. Localized coefficient energies

Write

\[
 Y_h(s)=\|h(s)\|_2^2,
 \qquad
 M_h(s)=\frac14\int_0^s\|\nabla h(\tau)\|_2^2\,d\tau.
 \tag{4.1}
\]

The backward envelope (1.3), the two-dimensional Ladyzhenskaya inequality,
and a Stieltjes product-measure lemma give constants independent of large
\(\Lambda\) such that

\[
 \begin{aligned}
 Y_a(s)+M_a(s)&\le C_ae^{-2r\Lambda(D-s)},\\
 Y_b(s)+M_b(s)&\le C_be^{-4r\Lambda(D-s)},\\
 Y_c(s)+M_c(s)&\le C_ce^{-6r\Lambda(D-s)}.
 \end{aligned}
 \tag{4.2}
\]

The exact rate gates are

\[
 \frac13<2r,
 \qquad\frac12<3r,
 \qquad\frac12<4r.
 \tag{4.3}
\]

No uniform high-Sobolev propagation is inserted into this closure.

## 5. Fourth-order exact residual

Set

\[
 u_{\rm app}=\delta a+\delta^2b+\delta^3c.
 \tag{5.1}
\]

The exact residual begins at order four:

\[
 \begin{aligned}
 R_{\rm app}={}&\delta^4[
 \mathcal B(a,c)+\mathcal B(c,a)+\mathcal B(b,b)]\\
 &+\delta^5[\mathcal B(b,c)+\mathcal B(c,b)]
 +\delta^6\mathcal B(c,c).
 \end{aligned}
 \tag{5.2}
\]

For \(e=u_\Lambda^\delta-u_{\rm app}\), the divergence-free transport
cancellations remove the two dangerous self-advection pairings.  The
remaining energy inequality retains the necessary integrating factor
\(\|\nabla u_{\rm app}\|_2^2\|e\|_2^2\).  The cumulative envelopes in
(4.2) control every fourth-, fifth-, and sixth-order product measure and
give

\[
 \|e(D)\|_2\le C_R\delta^4.
 \tag{5.3}
\]

Since \(b\) has no target row,

\[
 \|\Pi_{\pm1}u_\Lambda^\delta(D)\|_2
 \ge\delta-C_3\delta^3-C_R\delta^4.
 \tag{5.4}
\]

A fixed sufficiently small \(\delta_0\) makes the right-hand side at least
\(\delta/2\), proving (0.5).

## 6. Exact planar regularity boundary

The subspace

\[
 \mathcal S_{2D}=\{(0,u_2(y,z),u_3(y,z)):
 \partial_yu_2+\partial_zu_3=0\}
 \tag{6.1}
\]

is invariant.  Inside it, the equation is periodic two-dimensional
Navier--Stokes.  The selected orbit is therefore globally smooth and has no
three-dimensional vortex stretching.  The fixed-distance departure and
global smoothness coexist; neither statement implies a finite-time
singularity.

## 7. Exact and finite certificates

The sealed directory at `research/certificates/r073h/` contains 27 regular
files: the manifest binds 25 payloads (11 source files and 14 generated
files), and `SHA256SUMS` binds those payloads plus the manifest in 26 sorted
rows.  Its exact component has two independent producers:

- a fractional \(LDL^*\) reconstruction of the nine-by-nine block; and
- an independent Bareiss-minor reconstruction.

Both independently recover the Schur, perturbation, and rate arithmetic.

The separately labelled binary64 diagnostic contains:

- 319 primary rows on cutoffs \(24,32,48,64\), seven frozen viscosities,
  eleven profile-time snapshots, and one blind holdout;
- 21 cutoff comparisons and six step comparisons;
- 29 raw NPZ members containing the formal-grid and holdout coefficients;
- four preregistered formal alias-free physical-grid vorticity/FFT
  sentinels plus one independently recomputed blind holdout.

All response ratios in the finite diagnostic below use the profile endpoint
\(d=0.01\).  This is strictly outside the continuum-theorem interval
\(0\le d\le D\le1/450\).  The diagnostic endpoint must therefore not be
identified with the theorem endpoint \(d=D\), and the following values do
not provide numerical evidence for the constants in (0.5).

Over the frozen finite fit window at \(d=0.01\), the observed natural-log
slopes are

\[
 p_2=0.9876043066,
 \qquad p_3=1.9532334940.
 \tag{7.1}
\]

At the preregistered blind holdout
\((N,\varepsilon_\nu,h)=(64,7.5\times10^{-5},0.025)\), the compensated
values are

\[
 C_2=0.9250135449,
 \qquad C_3=0.8849248107,
 \qquad C_{3,\parallel}^{\rm signed}=-0.6597414810.
 \tag{7.2}
\]

All three lie inside their preregistered intervals.  The independent
implementation reports maximum coefficient relative error
\(2.0163303\times10^{-9}<2\times10^{-8}\), maximum forbidden-parity ratio
\(1.2024\times10^{-17}\), and the package validator recomputes NPZ endpoint
metrics to relative error at most \(1.043\times10^{-15}\).  The finest
outer-three-mode mass is at most \(1.607\times10^{-21}\).

These numbers diagnose the formal hierarchy and its finite scaling.  They
do not prove a continuum cubic coefficient, a uniform Taylor radius, a
nonlinear saturation limit, or a Fourier-tail enclosure.  The six step
rows have no raw step endpoints in the NPZ archive; their independent audit
is limited to the locked producer, CSV internal maximum and threshold, and
package hashes.  This limitation is explicit in the sealed validation.

## 8. Claim ledger

### CLOSED

- exact harmonic Taylor hierarchy and parity;
- absence of quadratic and quartic target terms;
- continuum \(K_z=\pm2\) numerical-abscissa bound;
- localized linear, quadratic, and cubic cumulative energies;
- exact fourth-order remainder in the planar subsystem;
- gain-normalized fixed-distance departure;
- global smoothness of the selected planar orbit.

### FALSE AS INFERENCE

- a lower bound for \(G_\Lambda\) does not determine its matching action;
- \(\delta/G_\Lambda\) cannot be replaced by
  \(\delta e^{-r\Lambda D}\) from the present evidence;
- a finite negative cubic projection does not prove continuum saturation;
- a varying-background departure is not fixed-background Lyapunov
  instability;
- the planar orbit does not create three-dimensional vortex stretching,
  singularity, or a Clay conclusion.

### OPEN

- a matching action for the selected gain \(G_\Lambda\);
- fixed-distance departure for a prescribed lower-law seed;
- a uniform all-order Taylor radius for the prescribed lower-law seed;
- a single-background Lyapunov sequence;
- the transverse Orr--Sommerfeld/Squire evolution and triad closure;
- finite-time singularity and the Clay problem.

## 9. Literature boundary and next gate

The bounded literature audit places this result next to autonomous
Navier--Stokes nonlinear-instability bootstraps, high-order boundary-layer
correctors, cubic interaction studies, unforced heat-evolving shear
stability, and near-Couette threshold theorems.  No located result covers
the same periodic two-harmonic, time-dependent, varying-amplitude family
with the selected moving bundle and gain-normalized launch.  This is a
bounded non-collision statement, not an originality or priority claim.

R0.73I should determine the matching exponential action of
\(G_\Lambda\), or prove that the available lower action is not sharp.  The
first target is a certified limit or matching upper/lower bounds for
\(\Lambda^{-1}\log G_\Lambda\).  Only then can
\(\delta/G_\Lambda\) be compared rigorously with a prescribed exponential
seed.  A transverse Orr--Sommerfeld/Squire row remains a separate later
branch; the finite cubic sign is not an admissible continuum hypothesis for
either task.
