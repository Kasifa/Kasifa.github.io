# R0.75T primary audit -- sharp collar coercivity for one dyadic pair

## 0. Frozen objects and verdict

- Main note: `research/r075t_two_harmonic_collar_coercivity.md`
- Audited main SHA-256:
  `822059f8a6248143ff3f36938a2333bee9f909b9166db951e227c426c2e8bc66`
- Source report: `research/r075t_report-source.md`
- Audited source SHA-256:
  `c2255cdd07f2e490921d93ba7e62a809c0348a9e6136b7fd5537cf3799e4e8d8`
- Current verdict: **PASS**
- Mathematical blocker count: **0**
- Release blocker count: **0**

This audit certifies the internal proof and the stated narrow boundary.  It
does not prove the open temporal estimate T.31 and does not authorize a claim
about arbitrary packets, Version-M, regularity, or the Clay problem.

## 1. Dependency and geometry audit

The four dependency hashes in the main note match the frozen files.  The
geometric reduction is exact.  For `|y|<=aR/2`, the assumption
`a>=4delta_0` implies

\[
 |y|<(a-\delta_0)R,
\]

so both the inner and outer plateau spheres meet the fibre.  Subtraction of
their squared transverse radii cancels `y^2` and gives

\[
 \pi\left(((a+\delta_0)R)^2-((a-\delta_0)R)^2\right)
 =4\pi a\delta_0R^2.
\]

The chart assumption `(a+delta)R<pi/2` prevents a periodic wrap.  Multiplying
this fibre area by the interval length `ell=aR` yields the exact geometric
power `a^2R^3` used in T.3.

## 2. Slow-envelope lemma audit

The potentially singular limit is `beta->0` with nearly cancelling
coefficients.  The proof avoids the ill-conditioned basis
`(e^(i beta s/2),e^(-i beta s/2))` and instead uses

\[
 u_\beta=\cos(\beta s/2),\qquad
 v_\beta=2\beta^{-1}\sin(\beta s/2),
\]

with `v_0=s`.  The associated Gram matrix varies continuously on the compact
interval `0<=beta<=1` and is positive definite at every point, including the
limit basis `(1,s)`.  Thus the inverse estimate in T.15 is uniform and has no
hidden `beta^(-1)` loss.

For

\[
 g=\operatorname {Re}(e^{i\mu s}Z),
\]

the exact identity

\[
 \int|g|^2=\frac12\int|Z|^2
 +\frac12\operatorname {Re}\int e^{2i\mu s}Z^2
\]

is correct.  Integration by parts bounds the endpoint term by
`C mu^(-1)||Z||_2^2` through the uniform `L^infinity` row, and the derivative
term by the same quantity through Cauchy--Schwarz and the uniform derivative
row.  Choosing `mu` above one absolute threshold proves T.13.

## 3. Beat-defect audit

With `d=k-m`, `c=(k+m)/2`, `Delta=phi-psi`, and `Sigma=phi+psi`, direct
multiplication verifies T.19:

\[
 e^{i(cy-\Sigma/2)}Ae^{i(dy/2-\Delta/2)}
 =Ae^{i(ky-\phi)},
\]

and the second envelope term gives `Ce^(i(my-psi))`.

For `dell<=1`, exact integration gives T.21.  Writing
`theta=dist(Delta,pi+2pi Z)` changes its bracket to

\[
 (A-C)^2+2AC[1-\operatorname {sinc}(d\ell/2)\cos\theta].
\]

On the compact range `0<=dell<=1`,
`1-sinc(dell/2)` is bounded below by a constant times `(dell)^2`, while
`1-cos theta` is bounded below by a constant times `min{1,theta^2}`.
Since `sinc(dell/2)` stays positive and bounded away from zero, T.23 and T.24
follow with a uniform constant.

For `dell>=1`, the exact five-term Gram formula T.25 is correct.  The global
maximum of `|sinc x|` on `x>=1/2` is `sinc(1/2)=2sin(1/2)<1`: `sinc` decreases
on the first positive lobe, and all later lobes are smaller.  The main
quadratic form therefore has a fixed positive gap.  The two self-boundary
terms and the sum-frequency term are
`O((mell)^(-1)ell(A^2+C^2))`; the condition `mell>=C_0` absorbs them.  Because
`(A-C)^2+AC` is comparable to `A^2+C^2`, T.27 follows.

The two regimes meet without a gap at `dell=1`.  The amplitude degree in the
`L^2` row is two.  Holder raises the defect to degree three and supplies
exactly one interval-length factor, so T.28 and T.3 have the stated powers.

## 4. Diffusive and flux-identity audit

At each time, the heat evolution changes only the two nonnegative amplitudes
and the two phases.  It preserves `m<k<=2m` and `maR>=C_0`.  Applying T.3
without replacing `A_t` and `C_t` by a common damping factor therefore gives
T.6 exactly.

For the flux row, expand

\[
 F^2=A_t^2\cos^2(kx_2-\phi_t)
 +C_t^2\cos^2(mx_2-\psi_t)
 +2A_tC_t\cos(kx_2-\phi_t)\cos(mx_2-\psi_t).
\]

Oddness of `D_R` kills the constant and cosine coefficients.  The self rows
carry the outside `1/2` from the flux and the `1/2` from `cos^2`, hence `B/4`.
The product-to-sum row cancels its factor two and then retains only the
outside flux factor, hence `B/2` for both `d=k-m` and `k+m`.  The sine phases
are respectively `2phi_t`, `2psi_t`, `phi_t-psi_t`, and `phi_t+psi_t`.
Thus every coefficient, frequency, phase, and sign in T.30 is correct.

## 5. Finite-check boundary

A deterministic exploratory scan evaluated the exact T.25 formula over
widely varying dyadic integers, amplitudes, phases, and interval lengths with
`mell>=64`.  It found no negative Gram value or defect-ratio collapse.  This
was a falsification aid only.  It is not used to certify the continuum
constants; the proof rests on Sections 2--4 above.

The fail-closed certificate suite is required to bind the frozen files,
recompute the exact rational geometry, recompute representative beat
defects, check the four flux prefactors, check the `a^2R^3H^3` power ledger,
verify all 31 tags and 32 display pairs, reject named mutations in two
independent implementations, reject unknown mutations, and reproduce its
canonical outputs byte for byte.

## 6. Source and claim audit

The source report uses primary records for adjacent Logvinenko--Sereda and
torus scale-free observability results.  Those general theorems are not
inserted into the local proof.  The source report is explicitly bounded and
makes no completeness, novelty, or priority claim.

The final boundary is accurate:

- T.3 is a static spatial theorem for one dyadic pair with `maR>=C_0`.
- T.6 is its exact constant-shear diffusive time-slice integral.
- T.31, complete two-harmonic payment, low carriers, three or more modes,
  arbitrary packets, and inter-packet aggregation remain open.
- The result does not contradict the growing-mode concentration used in
  R0.75R.
- No arbitrary-field E.24, Version-M extraction, suitable-weak transfer,
  regularity, or singularity result is claimed.  **NOT CLAY.**
