# R0.70D — Fixed-scale cover positivity does not control unresolved negative mass

> **Status:** internal canonical research report; not a public theorem chapter
> **Date:** 2026-08-24
> **Audience:** researchers in three-dimensional incompressible Navier--Stokes
> **Baseline:** R0.70C, commit `9bf4dfc`
> **Domain:** the normalized three-torus for the obstruction theorem; comparison
> with physical-space optimal-cover methods is stated separately
> **Arithmetic certificate:** `certificates/r070d/result.json`

The labels below are **[F]** for an externally sourced fact, **[P]** for a
proof completed here, **[O]** for a proved obstruction, and **[U]** for an
unresolved statement.  The distinction between a scalar cover theorem and a
Navier--Stokes flux realization is maintained throughout.

## 1. Direct answer and route decision

R0.70C showed that smooth Navier--Stokes evolution does not by itself turn a
signed annular work into a uniform proxy for its absolute activity.  R0.70D
tests the next possible repair:

> If every member of a positive spatial cover reports positive, comparable
> work, must the unresolved negative part be small?

For a fixed physical scale, the answer is **no as a purely
measure-theoretic implication**.

1. **[O] Uniform cover blindness.**  For any nonnegative cutoff family with a
   fixed positive mass and a uniform first-derivative budget, there are smooth
   scalar densities whose every normalized local average lies in
   \([\delta/2,3\delta/2]\), while the normalized \(L^1\) mass of the negative
   part stays above a universal positive constant.
2. **[P] Exact separation.**  The global signed mean is \(\delta\), whereas
   the negative mass tends to \(1/\pi\).  Their ratio therefore diverges like
   \(1/(\pi\delta)\).
3. **[F] Literature boundary.**  Dascaliuc--Grujić optimal covers are intended
   as detectors of sign coherence at scales comparable to or larger than the
   prescribed radius.  Their cascade theorems use local balance laws and
   additional Taylor/Kraichnan-scale and geometric hypotheses.  They do not
   assert control of \(\int f_-\) from cover positivity.
4. **[O] Closed route.**  A fixed-scale ensemble of positive signed averages,
   without cross-scale information or a PDE admissibility condition, cannot
   close the R0.70C sign defect.
5. **[U] Open transfer.**  The witness below is an abstract scalar density.
   It is not shown to equal Yu's filtered annular vortex-stretching density or
   any Navier--Stokes energy/enstrophy flux.  That realization problem is the
   next mathematical gate.

This is a useful no-go theorem: it prevents a false bridge from ensemble
positivity to absolute sign control.  It is **not** a regularity result, a
blow-up result, or progress on the Millennium claim in the formal sense.

## 2. Locked observation class

Let

\[
 \mathbb T^3=(\mathbb R/2\pi\mathbb Z)^3,
 \qquad d\mu=(2\pi)^{-3}\,dx
 \tag{2.1}
\]

and let \(\Theta\) be any nonempty family of real-valued weights satisfying

\[
 \theta\in W^{1,1}(\mathbb T^3),\qquad \theta\ge0,
 \tag{2.2}
\]

and the uniform bounds

\[
 \int_{\mathbb T^3}\theta\,d\mu\ge m_0>0,
 \qquad
 \|\partial_1\theta\|_{L^1(d\mu)}\le C_1<\infty.
 \tag{2.3}
\]

For a scalar density \(f\), define its normalized local observation by

\[
 \langle f\rangle_\theta
 =\frac{\int f\theta\,d\mu}{\int\theta\,d\mu}.
 \tag{2.4}
\]

Any ensemble observation considered in the obstruction is a convex
combination

\[
 \mathcal E(f)=\sum_{i=1}^n a_i\langle f\rangle_{\theta_i},
 \qquad a_i\ge0,\qquad \sum_{i=1}^n a_i=1.
 \tag{2.5}
\]

The class may contain arbitrarily many translated cutoffs and arbitrarily
many covers.  Only \(m_0\) and \(C_1\) must be uniform.  This is the correct
fixed-resolution abstraction: the observers may move, but their resolving
power may not grow with the hidden frequency.

## 3. The fixed-scale blindness theorem

### Theorem 3.1 [O]

Let \(\Theta\) satisfy (2.2)--(2.3).  For any
\(0<\delta\le1/2\), choose a positive integer \(N\) such that

\[
 N\ge \frac{2C_1}{\delta m_0}
 \tag{3.1}
\]

and set

\[
 f_{\delta,N}(x)=\delta+\sin(Nx_1).
 \tag{3.2}
\]

Then every \(\theta\in\Theta\) obeys

\[
 \frac{\delta}{2}
 \le \langle f_{\delta,N}\rangle_\theta
 \le \frac{3\delta}{2}.
 \tag{3.3}
\]

Consequently every ensemble (2.5) lies in the same interval.  Nevertheless,

\[
 \int_{\mathbb T^3}(f_{\delta,N})_-\,d\mu
 =\frac{
 2\sqrt{1-\delta^2}
 -\delta\bigl(\pi-2\arcsin\delta\bigr)
 }{2\pi},
 \tag{3.4}
\]

independently of \(N\), and

\[
 \int_{\mathbb T^3}(f_{\delta,N})_-\,d\mu
 \ge c_*:=\frac{\sqrt3-\pi/3}{2\pi}>0.
 \tag{3.5}
\]

The global signed mean is

\[
 \int_{\mathbb T^3}f_{\delta,N}\,d\mu=\delta.
 \tag{3.6}
\]

### Proof

Periodicity and one integration by parts give

\[
 \int_{\mathbb T^3}\sin(Nx_1)\theta(x)\,d\mu
 =\frac1N\int_{\mathbb T^3}
       \cos(Nx_1)\partial_1\theta(x)\,d\mu.
 \tag{3.7}
\]

Hence

\[
 \left|\int\sin(Nx_1)\theta\,d\mu\right|
 \le \frac{C_1}{N}.
 \tag{3.8}
\]

Dividing by \(\int\theta\,d\mu\ge m_0\) and applying (3.1) yields

\[
 \left|\langle f_{\delta,N}\rangle_\theta-\delta\right|
 \le \frac{C_1}{Nm_0}
 \le\frac\delta2,
 \tag{3.9}
\]

which proves (3.3); convexity proves the ensemble statement.

To compute the negative part, put \(\alpha=\arcsin\delta\).  The map
\(x_1\mapsto Nx_1\) preserves normalized Haar measure for integer \(N\), and
the negative set in one period is
\((\pi+\alpha,2\pi-\alpha)\).  Therefore

\[
 \begin{aligned}
 \int(f_{\delta,N})_-\,d\mu
 &=\frac1{2\pi}
   \int_{\pi+\alpha}^{2\pi-\alpha}
      (-\delta-\sin s)\,ds\\
 &=\frac{2\sqrt{1-\delta^2}
 -\delta(\pi-2\arcsin\delta)}{2\pi}.
 \end{aligned}
 \tag{3.10}
\]

Its derivative in \(\delta\) is

\[
 -\frac{\pi-2\arcsin\delta}{2\pi}<0
 \qquad(0<\delta<1),
 \tag{3.11}
\]

so the minimum on \((0,1/2]\) occurs at \(1/2\), giving (3.5).  Finally,
the sine has zero Haar mean, which proves (3.6).  \(\square\)

### Corollary 3.2 [O]

There is no modulus \(\omega(s)\to0\) as \(s\downarrow0\) such that, for
all smooth scalar densities,

\[
 \int f_-\,d\mu
 \le \omega\!\left(
 \max\left\{
 \left|\int f\,d\mu\right|,
 \sup_{\theta\in\Theta}|\langle f\rangle_\theta|
 \right\}\right).
 \tag{3.12}
\]

Indeed, take \(\delta_j\downarrow0\) and integers
\(N_j\ge2C_1/(\delta_jm_0)\).  The argument above gives

\[
 \max\left\{
 \left|\int f_{\delta_j,N_j}\,d\mu\right|,
 \sup_{\theta\in\Theta}
 |\langle f_{\delta_j,N_j}\rangle_\theta|
 \right\}
 \le\frac{3\delta_j}{2}\longrightarrow0,
 \tag{3.13}
\]

while the left side of (3.12) is at least \(c_*\).

## 4. Exact asymptotic size of the hidden sign defect

Formula (3.4) gives

\[
 \int(f_{\delta,N})_-\,d\mu\longrightarrow\frac1\pi
 \qquad(\delta\downarrow0),
 \tag{4.1}
\]

and hence

\[
 \frac{\int(f_{\delta,N})_-\,d\mu}
      {\int f_{\delta,N}\,d\mu}
 \sim\frac1{\pi\delta}.
 \tag{4.2}
\]

Thus the failure is not a small quantitative loss: all resolved signed
observations can converge uniformly to zero from the positive side while an
order-one negative mass survives.  With unnormalized Lebesgue measure, the
certificate records the equivalent identities

\[
 \int(f_{\delta,N})_-\,dx
 =4\pi^2\!\left[
 2\sqrt{1-\delta^2}-\delta(\pi-2\arcsin\delta)
 \right],
 \tag{4.3}
\]

and

\[
 \int f_{\delta,N}\,dx=8\pi^3\delta.
 \tag{4.4}
\]

## 5. Exact relation to optimal-cover methods

### 5.1 What the primary papers actually assume

Dascaliuc--Grujić's energy-cascade paper defines **interior** refined spatial
cutoffs that equal one on \(B(x_i,R)\), are supported in \(B(x_i,2R)\), and
obey scale-sensitive gradient and Laplacian inequalities.  A boundary-ball
cutoff may instead extend along a prescribed cone to \(B(0,2R_0)\) and must
satisfy additional matching conditions.  An optimal \((K_1,K_2)\)-cover has

\[
 (R_0/R)^3\le n\le K_1(R_0/R)^3
\]

balls, while every point belongs to at most \(K_2\) doubled balls.  Its exact
ensemble definition is a spacetime average

\[
 \frac1T\int\frac1n\sum_{i=1}^n
 R^{-3}\Theta_{x_i,R}(t)\,dt,
\]

not the normalized spatial observation (2.4).  Theorem 4.1 gives a two-sided
comparison for the averaged **modified flux** under a Taylor-scale
condition; ordinary flux inherits the lower bound from nonnegative anomalous
flux, while its full two-sided comparison requires local energy equality, in
particular for regular solutions.  The condition is sufficient, not claimed
necessary. **[F]**
[Primary source: Dascaliuc--Grujić 2011, equations (2.4)--(2.8),
(3.4)--(3.7), Definition 3.1, equations (3.17)--(3.18), Theorem 4.1, and
Remark 4.3](https://arxiv.org/html/1101.2193v2).

The enstrophy-cascade paper uses refined spacetime cutoffs
\(\phi_i=\eta\psi_i\), with

\[
 |\eta'|\le C_0T^{-1}\eta^{\rho_1},\qquad
 |\nabla\psi_i|\le C_0R^{-1}\psi_i^{\rho_2},\qquad
 |\Delta\psi_i|\le C_0R^{-2}\psi_i^{2\rho_2-1},
 \tag{5.1}
\]

where \(1/2<\rho_1,\rho_2<1\).  Theorem 4.1 concerns a Leray solution on
\(\mathbb R^3\times(0,T)\) whose initial vorticity is a finite Radon measure.
Its positive comparable enstrophy-flux conclusion additionally assumes
vorticity-direction coherence, a Kraichnan-scale inequality, spatial
localization, and terminal-time enstrophy modulation.  On its inertial range,
it states

\[
 (4K_*)^{-1}P_0\le\langle\Phi\rangle_R\le4K_*P_0,
 \qquad \beta^{-1}\sigma_0\le R\le R_0.
\]

**[F]**
[Primary source: Dascaliuc--Grujić 2012, Sections 2 and 4](https://arxiv.org/pdf/1107.0058v4).

These are sufficient PDE hypotheses.  Neither paper defines or estimates
\(\int f_-\) for a general signed density.

### 5.2 How Theorem 3.1 applies at one fixed interior scale

The oscillatory estimate is not topological: for
\(\theta\in W^{1,1}_c(\mathbb R^3)\), the same integration by parts has no
boundary term and gives
\[
 \left|\int_{\mathbb R^3}\sin(Nx_1)\theta\,dx\right|
 \le N^{-1}\|\partial_1\theta\|_1.
\]
The torus is used in Sections 2--4 to give the global signed and negative
masses an exact finite normalization; the fixed-scale cutoff comparison below
uses only this local Euclidean estimate.

For an interior refined cutoff, \(\psi_i=1\) on \(B(x_i,R)\) gives a mass
lower bound of order \(R^3\).  The gradient inequality in (5.1), together
with \(0\le\psi_i\le1\) and support volume of order \(R^3\), gives an
\(L^1\) first-derivative bound of order \(R^2\).  Hence

\[
 \frac{C_1}{m_0}=O(R^{-1}).
 \tag{5.2}
\]

The hidden-frequency condition becomes

\[
 N\gtrsim\frac1{\delta R}.
 \tag{5.3}
\]

If the tested weight is a power \(\theta_i=\psi_i^q\), then

\[
 |\nabla(\psi_i^q)|
 \le qC_0R^{-1}\psi_i^{q+\rho_2-1}.
\]

Thus \(q\ge1-\rho_2\) is a sufficient, not necessary, condition for
\(\|\partial_1(\psi_i^q)\|_1\lesssim R^2\); the platform region still gives
the mass lower bound.  The signed-flux weight \(\phi=\eta\psi\) has spatial
power \(q=1\) and is included.  The 2012 paper's more general
\(\phi^\delta\)-weighted densities are **not all included** by this argument,
because that paper does not impose \(\delta\ge1-\rho_2\).  Likewise,
\(q=2\rho_2-1\) satisfies the displayed sufficient condition only when
\(\rho_2\ge2/3\), whereas the paper allows every \(\rho_2>1/2\).  At equality
the present theorem needs only \(W^{1,1}\); it does not assert that
\(\psi_i^q\) remains a smooth refined cutoff.

Because \(\int\theta_i\asymp R^3\), (3.3) implies that each
\(R^{-3}\int f\theta_i\) is positive and of order \(\delta\); averaging over
an optimal cover preserves that conclusion.  The witness is time
independent, so the extra \(T^{-1}\) average changes nothing.  This gives only
a fixed-scale constant comparison between (2.4) and the papers' exact
normalization, not identity of definitions.  The number and overlap constants
\(K_1,K_2\) affect comparison constants, not the subscale blindness mechanism.

This is only a **relaxation of the interior, fixed-scale observation
geometry**.  Conditions (2.2)--(2.3) do not encode the full optimal-cover
argument: they omit the exact platform coverage, time cutoff, power-weighted
Laplacian estimate, boundary cone matching, inward-gradient convention, and
the local energy/enstrophy balance.  Theorem 3.1 therefore cannot be called
an equivalent model of the Dascaliuc--Grujić framework.

### 5.3 No contradiction with cascade positivity

The 2011 paper describes ensembles as detectors of sign fluctuations at
scales comparable to or larger than \(R\), while allowing substantial
fluctuation below the detected scale.  Theorem 3.1 makes that resolution
limit explicit.  It does not challenge their result: the two-sided positive
quantity in Theorem 4.1 is the averaged modified flux obtained from a local
Navier--Stokes balance plus a sufficient Taylor-scale condition; ordinary
flux has the qualified transfer stated above.  The 2012 enstrophy result adds
the Leray/initial-measure setting, geometric hypotheses, localization, and
modulation.

The correct conclusion is therefore:

> Fixed-scale optimal-cover positivity controls signed averages at the
> prescribed physical scale under explicit sufficient PDE hypotheses.  It
> does not, by itself, control unresolved subscale cancellation or the
> \(L^1\) mass of the negative part.

## 6. Assumption and failure boundary

The obstruction depends on finite resolution.  It does **not** cover the
following stronger observation mechanisms.

1. **All shrinking scales.**  If localized averages are available at all
   radii tending to zero, Lebesgue differentiation detects a negative set at
   almost every negative point.
2. **Adaptive derivatives.**  A cutoff family whose derivative budget grows
   like \(N\), or whose support shrinks like \(N^{-1}\), may resolve the
   oscillation.
3. **High-frequency norms.**  Bounds that explicitly control a derivative,
   Besov tail, Littlewood--Paley tail, or another frequency-sensitive norm
   see information discarded by fixed-scale averages.
4. **Cross-scale consistency.**  A theorem coupling cover observations over
   a sufficiently dense interval of scales is not reduced to (2.2)--(2.3).
5. **PDE admissibility.**  A local energy equality/inequality, pressure
   relation, vorticity geometry, or transport-diffusion constraint may
   exclude arbitrary scalar witnesses.
6. **Yu realization.**  Nothing here proves that \(f_{\delta,N}\) is an
   annular kernel density generated by a divergence-free velocity after the
   specified filter, cutoff, shell geometry, and time evolution.

## 7. Proof-gap matrix

| Required bridge | Status | Evidence or missing step |
|---|---:|---|
| Uniform positivity for every fixed-resolution cutoff | **[P] closed** | Equations (3.7)--(3.9) |
| Order-one negative mass independent of hidden frequency | **[P] closed** | Exact formula (3.4) and bound (3.5) |
| Failure of every vanishing observation modulus | **[O] closed** | Corollary 3.2 |
| Compatibility with one fixed interior optimal-cover scale | **[P] closed as a relaxation** | Scaling (5.2)--(5.3) |
| Equivalence with the complete Dascaliuc--Grujić framework | **not claimed** | Boundary balls, time cutoff, cover geometry, and PDE balances are omitted |
| Realization as a Yu filtered annular density | **[U] open** | Requires divergence-free core construction and exact four-pair accounting |
| Persistence on a genuine smooth NSE cylinder | **[U] open for this object** | Requires heat/filter leading term plus nonlinear error control |
| All-scale cover positivity implies negative-mass control | **not addressed** | Lebesgue differentiation defeats the present witness |

## 8. Research value and next stage

The value of R0.70D is **methodological and route-selecting, not
Millennium-level**.  It establishes a sharp logical separation:

\[
 \text{positive fixed-scale signed averages}
 \centernot\Longrightarrow
 \text{small unresolved negative mass}.
 \tag{8.1}
\]

That removes a tempting but invalid shortcut from the route tree.  It also
specifies what a successful replacement must add: scale refinement,
frequency control, PDE admissibility, or a direct geometric sign-selection
mechanism.

The proposed R0.70E gate is the narrowest PDE-specific transfer.  Its scope
is one strictly separated pair \(j\le k-m_*\), not every \(j\le k\):

1. fix one inversion-even Yu core cutoff \(\chi_k\), one inversion-even shell
   window \(\eta_j\), and one even filter;
2. construct two inversion-related inner regions and two inversion-related
   outer regions, and retain **all four** shell cross-pairs rather than
   assuming unwanted pairs disappear;
3. compute the exact leading signed polynomial in one amplitude parameter;
4. prove a simple root with nonzero absolute annular activity;
5. pass from the heat layer to a genuine small-data smooth NSE cylinder with
   a quantified remainder;
6. stop immediately if the exact Yu kernel, filter, or core support destroys
   transversality.

The current ideal four-pair algebra suggests the candidate polynomial

\[
 K(\lambda^3+\lambda^2-\lambda-1)
 =K(\lambda-1)(\lambda+1)^2,
 \tag{8.2}
\]

whose derivative at \(\lambda=1\) is \(4K\).  This is a **design target**,
not yet a theorem about the exact filtered annular functional.  Compact curl
blocks have zero total vorticity, so transition or return fields cannot be
silently discarded.  They must either lie where \(\chi_k\eta_j=0\), have a
proved zero contribution, or be included in a rigorous integral/interval
certificate.

The construction for every prescribed Yu \(\chi_k\) and every \(j\le k\)
remains **[U]**.  R0.70E will test only the one-pair scope stated above.

Equivalently, if the exact centered Yu objects are inversion-even and
\(\mathcal Rv(x)=-v(-x)\), the minimum remaining lemma is to find
\(v\in C^\infty_{c,\sigma}(\mathbb R^3)\) for which the exact heat-averaged
Yu functional satisfies

\[
 \left.\partial_\lambda
 \int_{I_k}F_{j,k}^{\mathrm{Yu}}
 \bigl(e^{\nu(t-t_-)\Delta}(v-\lambda\mathcal Rv)\bigr)\,dt
 \right|_{\lambda=1}\ne0,
 \tag{8.3}
\]

while the corresponding absolute annular activity at \(\lambda=1\) is
strictly positive.  Passing this lemma would allow the normalized
small-data solution map and implicit-function argument from R0.70C to be
reused.  It would upgrade a generic-cutoff no-go result to one exact Yu
matching shell; it still would not address all shells or prove regularity.

## 9. Computation and publication decision

- **Certificate:** exact SymPy arithmetic verifies (3.4)--(4.4) and the
  frequency-gate algebra.  The analytic integration-by-parts theorem remains
  a human-readable proof, not a computer proof.
- **Figure:** the archived panel visualizes one analytic witness and the exact
  negative-to-signed ratio.  It is explanatory evidence, not DNS and not an
  NSE flux sample.
- **DGX:** not justified.  The decisive objects are exact one-dimensional
  integrals and inequalities; large-scale floating-point simulation would
  add no proof value.
- **Independent review:** three read-only audits passed after tightening the
  Dascaliuc--Grujić normalization/scope map and locking the four-cross-pair,
  heat-average, and all-shell **[U]** boundaries in tests.
- **Public site:** the review gate is passed, so a draft recap and figure may
  be prepared.  Do not publish R0.70D as a theorem chapter or merge it into
  the public site without separate approval.
- **Next gate (R0.70E):** test the exact heat-averaged Yu single-core
  parity--transversality lemma for one strictly separated shell pair.

## 10. Claim--source ledger

| Claim | Type | Source | Use in this report |
|---|---|---|---|
| Refined cutoffs, optimal covers, ensemble normalization, Taylor-scale positivity | primary paper | [Dascaliuc--Grujić 2011](https://arxiv.org/html/1101.2193v2) | Exact comparison class and interpretation boundary |
| Refined spacetime cutoffs, coherence/modulation hypotheses, enstrophy-flux interval | primary paper | [Dascaliuc--Grujić 2012](https://arxiv.org/pdf/1107.0058v4) | Shows that positive flux is a conditional PDE conclusion |
| Uniform cover-blindness theorem | this report | Sections 2--4 and exact certificate | New elementary obstruction proved here |
| Yu-specific four-core transfer | none yet | R0.70E design target | Explicitly unresolved |

The source search was bounded to the two primary optimal-cover papers most
directly used by the route.  No source found there asserts that positivity of
fixed-scale cover averages controls \(L^1\) negative mass.  This is a bounded
search result, not a claim that no historically equivalent observation
exists anywhere in the literature.
