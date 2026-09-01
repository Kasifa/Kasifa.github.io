# R0.73X outcome and claim-state update

**Update date:** 2026-09-01

**Status:** `RESEARCH FREEZE / TWO INDEPENDENT AUDITS PASS`

**Claim class:** `EXACT IDENTITIES + POSITIVE-SCALE ABSOLUTE SIZE + EXACTLY SCOPED NEGATIVE RESULTS + OPEN COERCIVITY`

**Ordinary translation path:** `LOCAL_DIRECT_NO_DGX`

**DGX used:** `false`

This file records the exit state of R0.73X.  It does not rewrite the entry
contract in [`r073x_problem_freeze.md`](r073x_problem_freeze.md).  Every
statement below is routed to its analytic source, executable certificate, or
independent audit.

## 1. Resolution of the frozen questions

| Frozen question | R0.73X exit state | Exact boundary |
|---|---|---|
| localized resolved-energy and subfilter ledgers | `PROVED` | smooth exact; the suitable-weak characteristic identity is distributional after fixing \(0<\sigma\le s(t)\) |
| cutoff split \(\int\eta\Pi_s=-\int\nabla\eta\cdot K_s+\int\eta\mathscr S_s\) | `PROVED_AND_FINITE_EXACT_CHECKED` | the finite witness is a static Fourier field, not an NSE simulation |
| amplitude-independent quadratic absorption | `REFUTED_FOR_FIXED_HARMONIC_PROBE` | the certified probe is positive and periodic but not compactly supported; the compact-cutoff statement remains open |
| schematic exterior row in problem-freeze (5.3) | `REPLACED_BY_EXPLICIT_TAIL_COMPLETE_SIZE_LEMMAS` | the right side contains a separately declared exterior functional; no local smallness is inferred |
| pressure covariance | `PROVED_SIZE_BOUND_AT_POSITIVE_SCALE` | the harmonic pressure tail has algebraic, not Gaussian, decay |
| weighted tent/Carleson control | `OPEN` | the direct \(s^{-1/2}\)-weighted majorant has an endpoint obstruction |
| suitable-weak defect passage to \(s=0\) | `OPEN` | positive defect rows stay visible; no arbitrary endpoint trace is asserted |
| epsilon regularity and global regularity | `OPEN` | no CKN scale, continuation criterion, blow-up exclusion, or Clay conclusion follows |

The suitable-weak applications of the exterior size statements below use
the common quantifiers

\[
 \nu>0,
 \qquad 0<R<\frac{\pi}{8},
 \qquad 0<\theta\le1,
 \qquad I_{4R}^{\square}\Subset(0,T),
 \qquad \square\in\{\mathrm{std},\nu\},
\tag{U1.1}
\]

with a periodic suitable weak solution satisfying

\[
 u\in L_t^\infty L_x^2\cap L_t^2H_x^1,
 \qquad p\in L_{t,x}^{3/2}.
\tag{U1.2}
\]

The uniform lower scale \(\sigma\) belongs to the distributional pullback of
the full suitable-weak heat-characteristic identity.  The exterior size
lemmas themselves are stated for positive scales with no uniform lower bound.

## 2. Explicit exterior functional

For either the standard or viscosity-adapted cylinder clock, R0.73X freezes

\[
 \boxed{
 \mathcal A_{\rm ext}^{\square}(z_0,R;\theta)
 =\mathcal G_{u,p}^{\square}(z_0,R;\theta)
  +\mathcal H_u^{\square}(z_0,R),
 \qquad \square\in\{\mathrm{std},\nu\}.}
\tag{U2.1}
\]

The Gaussian part pays heat propagation of velocity and pressure data on
annuli.  Its annular coefficient contains

\[
 \gamma_m(\theta)
 =\theta^{-2}\exp\!\left[-{4^{m-1}\over32\theta}\right].
\tag{U2.2}
\]

The harmonic-pressure part is

\[
 \Lambda_R(t)
 =R\sum_{m\ge1}(2^mR)^{-4}
   \int_{A_m(R)}|\widetilde u(t,y)|^2\,dy,
 \qquad
 \mathcal H_u^{\square}
 =R\int_{I_R^{\square}}\Lambda_R(t)^{3/2}\,dt.
\tag{U2.3}
\]

The algebraic factor in (U2.3) is forced by the off-diagonal derivative of
the elliptic pressure kernel.  It must not be replaced by a Gaussian weight.

## 3. Proved positive-scale size statements

The Gaussian kernel calculation first gives the pointwise functional lemma

\[
 \boxed{
 |\mathscr S_s(t,x)|
 \le C_0s^{-1/2}P_{2s}(|u(t)|^3)(x),}
 \qquad
 C_0=2^{5/2}e^{-1/2}+{2^{7/2}\over\sqrt\pi}<10.
\tag{U3.1}
\]

Its scale integration closes the unweighted absolute centered-production
row with a critical Gaussian \(L^3\) velocity tail.  The complete
pressure/exterior decomposition then proves, for every positive measurable
heat scale \(0<s(t)\le\theta R^2\),

\[
 \boxed{
 \begin{aligned}
 &{1\over R}\int_{I_R^\square}\!\int_{B_R}
   |\mathscr S_{s(t)}^{\rm ext}|\,dx\,dt
 +{1\over R}\int_{I_R^\square}\!\int_{B_R}
   |Q_{s(t)}\cdot\nabla\eta_R|\,dx\,dt\\
 &\qquad\le C_{\theta,\nu,C_\eta}
 \left[
  \mathcal E^\square(z_0,4R)^{3/2}
  +\mathcal A_{\rm ext}^\square(z_0,R;\theta)
 \right].
 \end{aligned}}
\tag{U3.2}
\]

Precisely, (U3.2) quantifies over measurable

\[
 s:I_R^\square\to(0,\theta R^2],
 \qquad
 \eta_R\in W_0^{1,\infty}(B_R),
 \qquad
 \|\nabla\eta_R\|_\infty\le {C_\eta\over R}.
\tag{U3.2a}
\]

Its constant is independent of \(R,z_0\), the solution, and the selected
measurable scale \(s(t)\).  The same independence holds for (U3.4), with the
displayed dependence on \(\theta\) and \(\nu\).

Here \(\mathscr S^{\rm ext}\) excludes the unsigned core.  For the full
scale-integrated absolute centered production, define

\[
 \mathcal C_{\mathscr S,0,\theta}^{\rm abs,\square}(z_0,R)
 ={1\over R^3}\int_{I_R^\square}\!\int_0^{\theta R^2}\!\int_{B_R}
   |\mathscr S_s|\,dx\,ds\,dt.
\tag{U3.3}
\]

Then

\[
 \boxed{
 \mathcal C_{\mathscr S,0,\theta}^{\rm abs,\square}(z_0,R)
 \le C_{\theta,\nu}
 \left[
  \mathcal E^\square(z_0,4R)^{3/2}
  +\mathcal A_{\rm ext}^\square(z_0,R;\theta)
 \right].}
\tag{U3.4}
\]

Equations (U3.2)--(U3.4) are finiteness and scale-compatible size estimates.
They contain no assertion that either term on the right is small.

## 4. Exact negative results and their quantifiers

The finite Fourier harness proves that, for the declared fixed positive
harmonic probe, the ratios of the cubic production and centered remainder to
the full quadratic denominator \(\nu D+R^{-2}k\) grow linearly in the
amplitude.  Therefore no amplitude-independent quadratic absorption constant
exists in that probe class.  This does not yet refute the compactly supported
cutoff candidates in the problem freeze.

The translated-packet audit also rejects two purely functional candidates:

1. an exterior-free velocity estimate for unconstrained smooth
   divergence-free static triples with \(p=\mu=0\);
2. replacement of the critical Gaussian \(L^3\) tail by weighted \(L^2\)
   mass followed only by a \(3/2\) power.

The packet is generally not an unforced Navier--Stokes trajectory.  These
negative results do not refute an estimate restricted to NSE trajectories or
an inequality in which \(p\) is the pressure associated with \(u\).

## 5. Independent audit and executable evidence

The Gaussian proof and certificate pass an independent second-producer
audit.  The deterministic certificate verifies the kernel maximum, annular
geometry, exact scale integral, scaling degrees, packet exponents and
quadrature slopes, local energy interpolation powers, and infinite-tail
summability.  Both the system and bundled Python runtimes reproduce payload

`fcac97440dde87d00103f3a09b346bdd918c9fbb7360ee792edc2c8d0357e3b7`.

The independent pressure audit passes the complete-distribution formulation
of the periodic pressure gradient, its Fourier multiplier

\[
 -i{k_\ell k_i k_j\over|k|^2},
\tag{U5.1}
\]

the disappearance of origin contact terms after the local source is
subtracted, the ordinary absolutely convergent off-diagonal formula, the
gauge-centered \(L^1\) pressure covariance, both core--core payments, and
the scale powers in (U3.2).  Its verdict is

`PASS_FOR_POSITIVE_SCALE_ABSOLUTE_SIZE_ONLY`.

Reproduction commands:

```bash
/usr/bin/python3 scripts/r073x_gaussian_tail_certificate.py --check-only
/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/r073x_gaussian_tail_certificate.py --check-only
/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/r073x_finite_fourier_harness.py --check-only
```

## 6. Exact remaining bridge

R0.73X does **not** prove

\[
 \text{small signed heat-characteristic payment}
 \quad\Longrightarrow\quad
 \mathcal E^\square(z_0,4R)^{3/2}
 +\mathcal A_{\rm ext}^\square(z_0,R;\theta)
 \text{ is small}.
\tag{U6.1}
\]

The unsigned descending-characteristic core, the algebraic harmonic-pressure
tail, and the positive-scale-to-zero-scale passage remain visible.  The next
stage must attack one of these rows without assuming a known regularity
criterion in disguise.

## 7. Exit ledger

\[
\begin{array}{ll}
\texttt{localizedHeatCharacteristicLedger}
 &=\texttt{PROVED\_WITH\_STATED\_SOLUTION\_CLASS},\\
\texttt{centeredIncrementCutoffSplit}
 &=\texttt{EXACT\_AND\_FINITE\_CHECKED},\\
\texttt{fixedHarmonicProbeQuadraticAbsorption}
 &=\texttt{REFUTED\_EXACTLY},\\
\texttt{compactCutoffQuadraticAbsorption}
 &=\texttt{OPEN},\\
\texttt{gaussianVelocityTailLemma}
 &=\texttt{INDEPENDENT\_AUDIT\_PASS},\\
\texttt{pressureExteriorTailSizeLemma}
 &=\texttt{PASS\_AT\_POSITIVE\_SCALE},\\
\texttt{signedToAbsoluteCoercivity}
 &=\texttt{OPEN},\\
\texttt{weightedTentCarlesonControl}
 &=\texttt{OPEN},\\
\texttt{suitableWeakZeroScaleEndpoint}
 &=\texttt{OPEN},\\
\texttt{epsilonRegularity}
 &=\texttt{OPEN},\\
\texttt{arbitraryThreeDimensionalGlobalRegularity}
 &=\texttt{OPEN},\\
\texttt{clayConclusion}
 &=\texttt{OPEN}.
\end{array}
\tag{U7.1}
\]

No DNS or Navier--Stokes time integration was used.  R0.73X does not prove
regularity, exclude blow-up, construct a singular solution, or resolve the
Clay Millennium problem.  `NOT CLAY.`
