# R0.70N independent audit

**Audit status:** PASS

**Audit date:** 2026-08-25
**Mode:** independent, read-only mathematical and reproducibility audit

## 1. Scope checked

- Aggregate, native-source mismatch, moving-weight, time-window, and
  common-pullback ledgers.
- Exact rank-one periodic shear.
- Exact single-axis Beltrami obstruction.
- Exact two-axis Beltrami positive control, including pressure sign and
  covariance.
- Common-subspace theorem.
- Near-shear genuinely three-dimensional perturbation.
- Whole-space Biot--Savart initial datum.
- Whole-space Gaussian covariance.
- Equation numbering, MathJax syntax, and claim boundary.
- Symbolic producer against the archived certificate.

## 2. Evolution ledgers

Starting from

\[
 \dot Q_j=\Sigma_jQ_j+Q_j\Sigma_j+F_j
 \tag{2.1}
\]

and writing \(\Sigma_j=\Sigma_*+\Delta_j\), direct differentiation of

\[
 \mathcal Q=\sum_jw_jQ_j
 \tag{2.2}
\]

gives exactly

\[
 \dot{\mathcal Q}
 =\Sigma_*\mathcal Q+\mathcal Q\Sigma_*
 +\sum_jw_j(F_j+\Delta_jQ_j+Q_j\Delta_j)
 +\sum_j\dot w_jQ_j.
 \tag{2.3}
\]

The report retains every source-mismatch and moving-weight term with the
correct sign and multiplication order.

For a fixed lag kernel and fixed lag endpoints,

\[
 \overline{\mathcal Q}(t)
 =\int_0^\tau a(r)\mathcal Q(t-r)\,dr
 \tag{2.4}
\]

has the stated historical-source mismatch relative to \(\Sigma_*(t)\).  The
report correctly notes that time-dependent kernels or endpoints require
additional derivative and boundary terms.

With

\[
 \dot G_*=\Sigma_*G_*,
 \qquad
 \widehat{\mathcal Q}=G_*^{-1}\mathcal QG_*^{-\mathsf T},
 \tag{2.5}
\]

the two homogeneous terms cancel exactly and leave

\[
 \dot{\widehat{\mathcal Q}}
 =G_*^{-1}\mathcal FG_*^{-\mathsf T}.
 \tag{2.6}
\]

The filtered-vorticity cutoff, strain, diffusion, and commutator terms were
also checked term by term; their signs and integrations by parts are correct.

## 3. Exact NSE witnesses

For the shear

\[
 u_s=Ae^{-\nu N^2t}\sin(Ny)e_1,
 \tag{3.1}
\]

the divergence and nonlinear term vanish,
\(\partial_tu_s=\nu\Delta u_s\), and

\[
 \omega_s=-ANe^{-\nu N^2t}\cos(Ny)e_3.
 \tag{3.2}
\]

Every scalar/componentwise observation remains in
\(\operatorname{span}(e_3)\), so every nonzero positive aggregate is rank
one.

For the single-axis Beltrami wave

\[
 u_b=Ae^{-\nu N^2t}(\cos Nz,-\sin Nz,0),
 \tag{3.3}
\]

the divergence and nonlinear term vanish, the heat equation holds, and

\[
 \nabla\times u_b=Nu_b.
 \tag{3.4}
\]

Its covariance has the exact common null direction \(e_3\) and rank two when
the Fourier response is nonzero.

For

\[
 u_{2h}=e^{-\nu t}(ab_z+bb_x),
 \tag{3.5}
\]

both modes satisfy \(\nabla\times b=b\), and the correct pressure is

\[
 p=-\frac12|u_{2h}|^2.
 \tag{3.6}
\]

Under the now-explicit full-torus, translation-invariant Fourier-multiplier
hypothesis,

\[
 \mathcal Q_{2h}
 =\operatorname{diag}(\alpha,\alpha+\beta,\beta),
 \tag{3.7}
\]

so

\[
 \det\mathcal Q_{2h}=\alpha\beta(\alpha+\beta)>0,
 \qquad
 c_*=\frac{\min(\alpha,\beta)}{2(\alpha+\beta)}.
 \tag{3.8}
\]

## 4. Rank and whole-space boundaries

The common-subspace theorem is now correctly stated either with the subspace
hypothesis on the entire spatial input domain of each nonlocal filter or
directly on the filtered outputs.  Componentwise scalar operators commute
with constant target-space projections, so the range and kernel conclusions
follow.

For a fixed finite frame near shear,

\[
 \Omega_j^\varepsilon=f_je_3+\varepsilon\eta_j
 \tag{4.1}
\]

gives, for \(e\perp e_3\),

\[
 e^{\mathsf T}\mathcal Q^\varepsilon e
 =\varepsilon^2\sum_jw_j\int\chi_j|e\cdot\eta_j|^2,
 \tag{4.2}
\]

while the trace approaches a positive limit.  Hence
\(c_*(\mathcal Q^\varepsilon)\to0\).  The report limits the positive-definite
calibration to the full-torus identity filter with the explicit
\(v_0=b_z+b_x\); it does not assert positive definiteness for an arbitrary
filter frame.

For

\[
 \omega_0=\nabla\times(\psi e_3),
 \qquad
 u_0=\nabla\times(-\Delta)^{-1}\omega_0,
 \tag{4.3}
\]

the derivative structure controls the zero-frequency multiplier.  The
resulting velocity is smooth, divergence free, has curl \(\omega_0\), and
lies in the finite-energy Sobolev classes needed for local smooth existence.

For the Gaussian family, direct integration confirms the whole-space
Gaussian covariance

\[
 Q_L=\pi^{3/2}
 \operatorname{diag}\left(\frac1{4L},\frac1{4L},2L\right)
 \tag{4.4}
\]

and

\[
 \frac{\lambda_{\min}(Q_L)}{\operatorname{tr}Q_L}
 =\frac1{8L^2+2}\to0.
 \tag{4.5}
\]

## 5. Corrections resolved during audit

1. Strengthened the common-subspace hypothesis for nonlocal filters.
2. Replaced a false equivalence by the weaker direct filtered-output
   alternative.
3. Restricted the two-axis Fourier-orthogonality calculation to its valid
   filter class.
4. Replaced the overbroad near-shear positive-definiteness statement with an
   explicit identity-filter calibration.
5. Extended the cutoff convention to include integrable full-space weights.
6. Corrected the MathJax syntax in the route alternative.
7. Split the next route into coercive, near-plane, and near-line eigenvalue
   regimes.

## 6. Reproducibility result

The producer reproduced byte-identically against the archived result.

SHA-256:

    a652ae1264af52fc5e36c937f33dd0abeabaa18102b127c6a13b5b188ba7a440

The regenerated and archived result.json files have the same hash.
The whitespace audit reports no error in the audited artifacts.

## 7. Claim boundary

The certified conclusion is narrow:

> Scalar/componentwise filters with nonnegative scale, center, or time
> aggregation cannot provide a universal positive vorticity-frame constant
> for every smooth periodic Navier--Stokes solution.

The report does not claim that conditional coercivity is impossible, that
every Beltrami field is rank deficient, that low covariance rank implies
regularity, that an augmented observable closes, or that global regularity,
blow-up, or the Millennium problem has been resolved.

No remaining mathematical correction is required for the audited R0.70N
claim.
