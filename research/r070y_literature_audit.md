# R0.70Y literature-boundary audit

**Audit date:** 2026-08-25

**Scope:** primary-source check for the response-slope factorization, the
critical complete-frame defect estimates, high--high--low locality, and the
\(q=3\) scale-packet obstruction.

## Verdict

**PASS with a strict no-priority boundary.**  A bounded search of ten
high-signal primary sources and one standard monograph did not locate the
same complete radial-frame signed-defect estimates

\[
 |\mathfrak E_S|
 \lesssim
 \|\omega\|_{B^0_{\infty,\infty}}\|\omega\|_2^2,
 \qquad
 |\mathfrak E_S|
 \lesssim
 \|\omega\|_{B^0_{3,3}}^3.
\]

That search result is not evidence of priority.  Classical work already
covers the harmonic-analysis machinery, Besov vorticity criteria, triadic
scale locality, signed cancellation, and sequence-space sharpness patterns.
The defensible contribution boundary is narrower:

- the exact response/metric split for this frame symbol;
- the symbol-specific HHL derivative gain after cyclic summation;
- the no-log \(B^0_{\infty,\infty}\times L^2\times L^2\) estimate for this
  signed defect; and
- the explicit operator-level packet and top-eigenvalue counterexamples.

The \(B^0_{3,3}\) theorem is useful but its shell summation is comparatively
standard.  The \(q=3\) example is a supporting sharpness proposition, not a
new general theory of Besov sequence exponents.

## Claim-to-source ledger

### 1. Vorticity, Littlewood--Paley, and Besov methods are established

Manna and Sritharan study the three-dimensional vorticity equation using
Littlewood--Paley analysis and prove local Lyapunov properties in Besov
spaces under smallness assumptions on negative-index velocity and vorticity
norms:

- Utpal Manna and Sivaguru S. Sritharan, *Lyapunov Functionals and Local
  Dissipativity for the Vorticity Equation in Lp and Besov Spaces*, 2008,
  [arXiv:0802.2898](https://arxiv.org/abs/0802.2898).

Yuan and Zhang prove a continuation criterion formulated with negative-index
Besov norms of vorticity:

- Baoxiang Yuan and Jian Zhang, *Blow-up criterion of strong solutions to the
  Navier--Stokes equations in Besov spaces with negative indices*, 2007,
  [arXiv:math/0703883](https://arxiv.org/abs/math/0703883).

Kozono, Ogawa and Taniuchi establish logarithmic critical Besov inequalities
and apply them to regularity criteria for Navier--Stokes and related systems:

- Hideo Kozono, Takayoshi Ogawa and Yasushi Taniuchi, *The critical Sobolev
  inequalities in Besov spaces and regularity criterion to some semi-linear
  evolution equations*, 2002,
  [DOI 10.1007/s002090100332](https://doi.org/10.1007/s002090100332).

**Boundary:** none of these sources studies the complete-frame covariance
defect \(\mathfrak E_S\), and none supplies R0.70Y's theorem.  Conversely,
R0.70Y is not a new general Besov vorticity criterion and does not control the
full stretching term.

### 2. The paraproduct and multiplier machinery is classical

Bony's paradifferential calculus supplies the low--high/high--low/comparable
frequency organization:

- Jean-Michel Bony, *Calcul symbolique et propagation des singularités pour
  les équations aux dérivées partielles non linéaires*, 1981,
  [DOI 10.24033/asens.1404](https://doi.org/10.24033/asens.1404).

Coifman and Meyer are a primary source for bilinear singular-integral and
commutator estimates:

- Ronald R. Coifman and Yves Meyer, *On commutators of singular integrals and
  bilinear singular integrals*, 1975,
  [DOI 10.1090/S0002-9947-1975-0380244-8](https://doi.org/10.1090/S0002-9947-1975-0380244-8).

A standard modern reference for LP and Besov conventions is:

- Hajer Bahouri, Jean-Yves Chemin and Raphaël Danchin, *Fourier Analysis and
  Nonlinear Partial Differential Equations*, 2011,
  [DOI 10.1007/978-3-642-16830-7](https://doi.org/10.1007/978-3-642-16830-7).

**Boundary:** R0.70Y does not claim a new general multiplier theorem.  The
\((\infty,2,2)\) block estimate is proved directly from a compact localized
periodic \(L^1\) kernel.  The nonclassical input is the frame-response cyclic
symbol's \(2^{k-J}\) derivative gain.

### 3. Triadic cancellation and scale locality have strong precedents

Waleffe analyzes helical triads and the cancellation of large, opposite-sign
nonlocal transfers:

- Fabian Waleffe, *The nature of triad interactions in homogeneous
  turbulence*, 1992,
  [DOI 10.1063/1.858309](https://doi.org/10.1063/1.858309).

L'vov and Falkovich derive a scale-ratio suppression in a quasi-Lagrangian
statistical theory:

- Victor L'vov and Gregory Falkovich, *Counterbalanced interaction locality
  of developed hydrodynamic turbulence*, 1992,
  [DOI 10.1103/PhysRevA.46.4762](https://doi.org/10.1103/PhysRevA.46.4762).

Eyink and Aluie distinguish absolute nonlocal-triad bounds from stronger
cancellation in signed averages, for smooth coarse-graining:

- Gregory L. Eyink and Hussein Aluie, *Localness of energy cascade in
  hydrodynamic turbulence, I. Smooth coarse-graining*, 2009,
  [arXiv:0909.2386](https://arxiv.org/abs/0909.2386).

The sharp-filter sequel distinguishes large individual nonlocal triads from
their aggregate contribution:

- Hussein Aluie and Gregory L. Eyink, *Localness of energy cascade in
  hydrodynamic turbulence, II. Sharp spectral filter*, 2009,
  [arXiv:0909.2451](https://arxiv.org/abs/0909.2451).

**Boundary:** these works treat energy transfer or statistical correlations,
not the deterministic complete-frame vorticity defect.  R0.70Y may claim its
specific Laplacian-weighted cyclic symbol and response/metric split, but not
the discovery of triadic locality or signed cancellation in general.

### 4. Cubic shell convolution and critical sharpness have close precedents

Cheskidov, Constantin, Friedlander and Shvydkoy use a Littlewood--Paley shell
convolution to control Euler energy flux and prove a natural critical-space
sharpness statement:

- Alexey Cheskidov, Peter Constantin, Susan Friedlander and Roman Shvydkoy,
  *Energy conservation and Onsager's conjecture for the Euler equations*,
  2007,
  [arXiv:0704.0759](https://arxiv.org/abs/0704.0759).

**Boundary:** their observable and scaling weights differ from
\(\mathfrak E_S\), so the paper does not imply the R0.70Y estimate.  It does,
however, show why a cubic \(\ell^3\) shell aggregation and separated-packet
sharpness should not be advertised as a new general mechanism.

## Safe wording

The following wording is supported:

> For a fixed complete radial frame, the signed covariance defect obeys two
> log-free critical shell estimates.  Their proof combines the classical
> Bony--Coifman--Meyer framework with a symbol-specific HHL cyclic
> cancellation.  A scale-separated exact Fourier atom shows that
> \(q>3\) is impossible in the uniform family
> \(|\mathfrak E_S|\le C\|\omega\|_{B^0_{3,q}}^3\).

The following wording is not supported:

- first discovery of the critical Besov index \(q=3\);
- first proof of nonlocal-triad locality or signed cancellation;
- first use of \(B^0_{\infty,\infty}\) in a vorticity criterion;
- a regularity criterion for the full Navier--Stokes equation; or
- a novelty or priority claim based only on this bounded search.

## Stop rule and remaining gap

The search stopped after the principal claim families had high-confidence
primary precedents and additional query variants returned repeated or weaker
material.  A journal submission would still require a broader MathSciNet or
zbMATH search, citation chasing from the nearest multiplier papers, and
external review by a specialist in multilinear harmonic analysis.
