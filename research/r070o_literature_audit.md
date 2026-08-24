# R0.70O bounded primary-literature audit

**Audit date:** 2026-08-25

**Question:** can a small eigenvalue of a local or multi-scale filtered
vorticity covariance be lifted to an established unfiltered regularity
criterion?

## 1. Corpus, method, and stopping rule

The audit checked primary papers, author manuscripts, journal pages, and DOI
records in the following families:

- two-component vorticity regularity criteria;
- locally varying anisotropic directions;
- vorticity-direction coherence;
- Littlewood--Paley and finite-window regularity criteria;
- curl spectral projections;
- determining observations and data assimilation;
- filtered, averaged, covariance, and structure-tensor formulations of
  vorticity geometry;
- forward keyword and citation checks through 2026-08-25.

Technical hypotheses were taken from paper text rather than secondary
summaries.  The search stopped after the exact theorem statements of the
three closest geometric criteria were verified, the principal
frequency-localized and finite-observation alternatives were checked, and two
further searches combining `vorticity covariance/eigenvalue` with
`regularity/continuation` returned only repeated papers, numerical turbulence
studies, or results without a relevant continuation theorem.

This is a bounded audit, not an exhaustive MathSciNet, zbMATH, or
all-language systematic review.  The phrase “no theorem was found” below is
limited by that corpus and stopping rule.

## 2. Direct collision decision

No audited paper proves that one or two small eigenvalues of a finite local
or multi-scale filtered vorticity covariance imply an unfiltered critical
vorticity norm.

The algebraic comparison is exact:

\[
 \lambda_3
 =\min_{|n|=1}\int\chi|n\cdot\omega|^2,
 \tag{2.1}
\]

while

\[
 \lambda_2+\lambda_3
 =\min_{|v|=1}\int\chi|v\times\omega|^2.
 \tag{2.2}
\]

Therefore:

- small \(\lambda_3\) controls one component and means near a plane;
- small \(\lambda_2+\lambda_3\) controls two transverse components and means
  near a line;
- only the second quantity matches the component count in Chae--Choe and
  Miller;
- neither quantity, when filtered or normalized by the trace, supplies the
  required unfiltered absolute spacetime norm.

R0.70O supplies an exact dynamic counterexample to the missing uniform
reconstruction estimate.  The literature comparison determines the narrow
claim boundary; it is not used as proof of the counterexample.

## 3. Chae--Choe: two fixed unfiltered vorticity components

- Source: Dongho Chae and Hi-Jun Choe, “Regularity of Solutions to the
  Navier--Stokes Equation,” *Electronic Journal of Differential Equations*
  1999, No. 05, 1--7,
  [journal page](https://ejde.math.txstate.edu/Volumes/1999/05/abstr.html),
  [paper PDF](https://ejde.math.txstate.edu/Volumes/1999/05/chae.pdf).
- Setting: \(\mathbb R^3\times(0,T)\), with the displayed paper taking zero
  force for simplicity.
- Initial data: \(v_0\in L^2\), \(\nabla\cdot v_0=0\), and
  \(\omega_0=\nabla\times v_0\in L^2\).
- Solution: Leray--Hopf weak solution.

The paper fixes

\[
 \widetilde\omega=(\omega_1,\omega_2,0).
 \tag{3.1}
\]

Its Theorem 1 states regularity if

\[
 \widetilde\omega\in L^\alpha(0,T;L^\gamma(\mathbb R^3)),
 \qquad
 \frac2\alpha+\frac3\gamma\leq2,
 \tag{3.2}
\]

with

\[
 1<\alpha<\infty,
 \qquad \frac32<\gamma<\infty,
 \tag{3.3}
\]

or at the endpoint if

\[
 \|\widetilde\omega\|_{L_t^\infty L_x^{3/2}}
 \tag{3.4}
\]

is sufficiently small.  Rotation invariance permits replacing the third
coordinate direction by any one **preassigned fixed global unit vector**
\(e\), so the controlled object is \(e\times\omega\).

The paper supports:

- two transverse vorticity components;
- unfiltered whole-space norms;
- a scale-critical mixed-norm family.

It does not support:

- one small covariance eigenvalue;
- a direction selected separately at each scale or spatial cell;
- a spatially or temporally varying direction;
- a filtered or finite-band norm;
- a normalized covariance ratio.

## 4. Miller: a spatially Lipschitz varying direction

- Source: Evan Miller, “A Locally Anisotropic Regularity Criterion for the
  Navier--Stokes Equation in Terms of Vorticity,” *Proceedings of the
  American Mathematical Society, Series B* 8 (2021), 60--74,
  [DOI 10.1090/bproc/74](https://doi.org/10.1090/bproc/74),
  [author manuscript](https://arxiv.org/abs/2002.02152).

Theorem 1.6 assumes

\[
 u\in C([0,T_{\max});H^1(\mathbb R^3))
 \tag{4.1}
\]

is a mild solution, and

\[
 v\in L^\infty(\mathbb R^3\times[0,\infty);\mathbb R^3),
 \qquad |v(x,t)|=1\quad\hbox{a.e.},
 \tag{4.2}
\]

with

\[
 \nabla_xv\in
 L^\infty_{\mathrm{loc}}([0,\infty);L^\infty(\mathbb R^3)).
 \tag{4.3}
\]

No time derivative of \(v\) is assumed.  The theorem gives an exponential
\(\dot H^1\) bound involving \(\|\nabla v\|_{L_t^\infty L_x^\infty}\) and

\[
 \int_0^t\|v(\tau)\times\omega(\tau)\|_2^4\,d\tau.
 \tag{4.4}
\]

In particular, if \(T_{\max}<\infty\), then

\[
 \int_0^{T_{\max}}
 \|v(t)\times\omega(t)\|_2^4\,dt=\infty.
 \tag{4.5}
\]

This is exactly the vorticity-critical space

\[
 v\times\omega\in L_t^4L_x^2.
 \tag{4.6}
\]

The paper explicitly notes that its proof uses the Hilbert structure of
\(L^2\) and does not recover the entire Chae--Choe critical family.

The result is “locally anisotropic” because \(v\) can vary with \(x,t\), but
the norm remains a global whole-space norm.  A covariance principal line can
only be inserted after proving:

1. a common direction field rather than unrelated cellwise minimizers;
2. a nonvanishing principal spectral gap;
3. a spatially Lipschitz unit lift of the principal line;
4. an unfiltered \(L_t^4L_x^2\) bound.

Covariance eigenvalues alone supply none of items 3--4.

## 5. Constantin--Fefferman: pointwise high-vorticity direction coherence

- Source: Peter Constantin and Charles Fefferman, “Direction of Vorticity
  and the Problem of Global Regularity for the Navier--Stokes Equations,”
  *Indiana University Mathematics Journal* 42 (1993), no. 3, 775--789,
  [journal page](https://iumj.org/article/3627/),
  [DOI 10.1512/iumj.1993.42.42034](https://doi.org/10.1512/iumj.1993.42.42034).

Writing

\[
 \xi(x,t)=\frac{\omega(x,t)}{|\omega(x,t)|},
 \tag{5.1}
\]

the paper imposes a uniform geometric coherence condition on pairs of points
where both vorticity magnitudes exceed a fixed threshold.  In one equivalent
projection form, for fixed \(\Omega,\rho>0\),

\[
 |P_{\xi(x,t)}^\perp\xi(x+y,t)|
 \leq\frac{|y|}{\rho}
 \tag{5.2}
\]

whenever

\[
 |\omega(x,t)|>\Omega,
 \qquad |\omega(x+y,t)|>\Omega.
 \tag{5.3}
\]

This is a pointwise, pairwise, all-small-separation condition on the
**unfiltered vorticity direction**.  It is not an averaged covariance
condition.  The projection or sine of the angle is insensitive to parallel
versus antiparallel orientation, so the geometry is naturally an unoriented
line field.

A small covariance angular variance at one or finitely many radii cannot
imply (5.2).  Such an implication would require, at minimum, compatible
directions over all shrinking balls, decay of the angular excess in a
Campanato/Morrey scale, and control conditioned on the high-vorticity set.

## 6. Frequency-localized criteria retain absolute amplitudes

### 6.1 Cheskidov--Dai

- Source: Alexey Cheskidov and Mimi Dai, “Regularity Criteria for the 3D
  Navier--Stokes and MHD Equations,” *Proceedings of the Edinburgh
  Mathematical Society* 68 (2025), no. 4, 1262--1296,
  [DOI 10.1017/S0013091525100813](https://doi.org/10.1017/S0013091525100813),
  [author manuscript](https://arxiv.org/abs/1507.06611).

The NSE criteria use absolute \(L^\infty\) amplitudes of
Littlewood--Paley vorticity blocks near a solution-dependent dissipation
wavenumber, together with a critical time integral and a small constant.
They support direct use of filtered vorticity blocks in a regularity theorem,
but not a lift from finite covariance ratios or small covariance
eigenvalues.  The criteria retain a limiting high-frequency requirement.

### 6.2 Bradshaw--Grujić

- Source: Zachary Bradshaw and Zoran Grujić, “Frequency Localized Regularity
  Criteria for the 3D Navier--Stokes Equations,” *Archive for Rational
  Mechanics and Analysis* 224 (2017), 125--133,
  [DOI 10.1007/s00205-016-1069-9](https://doi.org/10.1007/s00205-016-1069-9),
  [author manuscript](https://arxiv.org/abs/1501.01043).

This paper gives a genuine finite dynamic frequency-window condition, but
the object is an absolute critical Besov amplitude of velocity blocks.  The
window endpoints depend on solution norms and the time condition retains the
critical power.  It does not replace those amplitudes by directional
covariance geometry.

## 7. Curl spectral projections are a different observation

- Source: Jiří Neustupa and Patrick Penel, “Regularity Criteria for Weak
  Solutions to the Navier--Stokes Equations Based on Spectral Projections of
  Vorticity,” *Comptes Rendus Mathématique* 350 (2012), 597--602,
  [DOI 10.1016/j.crma.2012.06.008](https://doi.org/10.1016/j.crma.2012.06.008),
  [journal PDF](https://comptes-rendus.academie-sciences.fr/mathematique/item/10.1016/j.crma.2012.06.008.pdf).

The projections in this paper are spectral projections of the self-adjoint
curl operator, separating Beltrami spectral signs relative to a threshold.
The conditions retain fractional derivative norms of the projected
vorticity.  They are not local spatial filters, LP blocks, or target-space
covariance eigenspaces.

## 8. Finite observations can imply regularity only with a PDE mechanism

- Source: Abhishek Balakrishna and Animikh Biswas, “A Novel Regularity
  Criterion for the Three-Dimensional Navier--Stokes Equations Based on
  Finitely Many Observations,” *Research in the Mathematical Sciences* 12
  (2025), article 46,
  [DOI 10.1007/s40687-025-00530-w](https://doi.org/10.1007/s40687-025-00530-w),
  [author manuscript](https://arxiv.org/abs/2211.15048).
- Follow-up: Abhishek Balakrishna and Animikh Biswas, “Reformulation and
  Interpretation of the Regularity Criterion for 3D NSE Based on Finitely
  Many Observations,” *Applied Mathematics Letters* 181 (2026), article
  110017,
  [author manuscript](https://arxiv.org/abs/2603.17322).

These results are the closest audited examples of coarse finite observations
participating in a regularity criterion.  Their mechanism is materially
different from an algebraic covariance lift:

- the observations concern velocity modes, nodes, or volume elements;
- a nudging/data-assimilation PDE reconstructs and synchronizes a solution;
- the resolution \(h\) is constrained by viscosity, forcing, initial
  \(H^1\) size, and the absolute observed amplitude;
- the criterion is not an inequality from finite observations alone to an
  unfiltered critical vorticity norm.

This literature prevents the overbroad statement that finite observations
can never participate in a regularity theorem.  R0.70O proves only that the
proposed finite scalar covariance residual has no universal direct
reconstruction estimate.

## 9. Exact gap between covariance and the closest criteria

### 9.1 Near-plane branch

Small \(\lambda_3\) gives one small normal component.  The matrix

\[
 Q=\operatorname{diag}(M,M,0)
 \tag{9.1}
\]

has zero plane residual and best-line residual \(M\).  Therefore this branch
is already one full component short of Chae--Choe or Miller.  It also allows
unrestricted rotation inside the plane and does not imply
Constantin--Fefferman coherence.

### 9.2 Near-line branch

Small \(\lambda_2+\lambda_3\) has the correct two-component algebra.  The
remaining gaps are:

1. **absolute amplitude:** a ratio to \(\operatorname{tr}Q\) can stay small
   while the transverse energy grows;
2. **all-frequency coverage:** finitely many filters have blind or weakly
   observed modes;
3. **critical time aggregation:** Miller needs the square of the transverse
   \(L^2\) energy integrable in time;
4. **common direction:** separate minimizers over scales and windows need not
   agree;
5. **spatial direction regularity:** a principal gap must be combined with
   \(\nabla Q\), not used alone;
6. **frequency commutators:** a variable projection does not commute with LP
   filters;
7. **orientation:** covariance determines a line \(v\otimes v\), while a
   vector-field theorem needs a suitable lift;
8. **pointwise coherence:** average angular variance does not imply the
   Constantin--Fefferman pairwise high-vorticity condition.

R0.70O's exact shear family closes item 2 for any proposed direct uniform
finite-filter estimate.  The other items remain requirements of a
conditional all-scale route.

## 10. Safe novelty boundary

The project must not claim:

- the first two-vorticity-component criterion;
- the first spatially varying anisotropic criterion;
- the first frequency-localized vorticity criterion;
- the first finite-observation regularity theorem;
- that small \(\lambda_3\) is close to a two-component criterion;
- that small \(\lambda_2+\lambda_3\) is itself a continuation criterion;
- that average covariance implies pointwise vorticity-direction coherence.

The bounded audit supports the following narrow statement:

> No audited primary source turns one or two small eigenvalues of a local,
> finite-scale filtered vorticity covariance, especially only their ratios to
> the trace, directly into the Chae--Choe, Miller, or
> Constantin--Fefferman hypotheses.  Existing frequency-localized and
> finite-observation results retain absolute amplitudes and additional PDE or
> resolution structure.

Potentially nonredundant future work is limited to either:

1. an all-scale, absolute-residual, common-direction and commutator theorem
   that genuinely reaches Miller's \(L_t^4L_x^2\) hypothesis; or
2. sharper impossibility results showing that one of those added assumptions
   is unavoidable.

## 11. Audit confidence

- Chae--Choe theorem statement: high; checked in the journal PDF.
- Miller hypotheses and critical norm: high; checked in the author
  manuscript and DOI record.
- Constantin--Fefferman geometric scope: high; checked against the journal
  record and paper statement.
- Frequency-localized and finite-observation contrasts: high for the stated
  mechanism and claim boundary.
- Absence of an exact covariance-lift theorem: bounded-search confidence
  only; not an absolute novelty proof.
