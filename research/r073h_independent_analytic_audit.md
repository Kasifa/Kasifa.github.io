# R0.73H independent analytic audit

**Audit date:** 2026-08-30  
**Files audited:** `r073h_harmonic_energy_proof.md` and
`r073h_harmonic_derivation.md`  
**Method:** independent line-by-line reconstruction of the normalization,
continuum coercivity, harmonic algebra, Stieltjes estimates, and remainder
energy  
**Verdict:** **MATHEMATICAL FINAL PASS**

## 1. Normalization

The slow-time normalization is consistent:

\[
 d=4t,
 \qquad
 \mathcal B(u,v)=-\frac14\mathbb P[(u\cdot\nabla)v],
 \qquad
 M_u(s)=\frac14\int_0^s\|\nabla u\|_2^2,d\tau.
\]

In fast time \(\theta=\Lambda d\), the nonlinear coefficient is
\(\varepsilon_\nu/4\).  The launch amplitude is a separate parameter.
No physical-amplitude and fast-time equation has been mixed.

## 2. Backward localization

The selected R0.73G real frozen-top launch belongs to the R0.73F moving
unstable fiber at time zero.  Applying the inverse evolution from the
endpoint back to an intermediate time gives the stated upper envelope for
the endpoint-normalized orbit.  This is not an invalid reversal of an
operator-norm lower bound.

## 3. Continuum doubled-row estimate

The two-sign gauge correctly reduces \(\omega_1\le1/3\) to positivity of

\[
 H_d=-\partial_x^2+1-\frac94W_x(d,x)^2.
\]

The exact rational \(LDL^*\) calculation on \(|m|\le4\), the analytic
tail and cross-block bounds, and the two-by-two Schur estimate give

\[
 H_0\ge\frac1{20}I.
\]

The explicit perturbation for \(d\le1/450\) then gives
\(H_d\ge1/40\).  This is an infinite-dimensional continuum estimate; the
finite rational block is only one subcertificate.

## 4. Harmonic algebra

The \(K_z=2\), mean, cubic-return \(K_z=1\), and cubic \(K_z=3\) Leray
formulas were independently recomputed path by path.  No coefficient or
sign error remains.  The generic physical Fourier--Leray kernel agrees with
the profile formulas to below \(8\times10^{-15}\) in independent finite
checks.

The parity induction is exact:

\[
 u^{(j)}:\quad K_z=-j,-j+2,\ldots,j-2,j.
\]

Therefore the target \(K_z=\pm1\) has no quadratic or quartic Taylor term.

## 5. Localized energy estimates

Zero spatial mean propagates for the carrier, every coefficient, the exact
perturbation, and the error.  The homogeneous two-dimensional
Ladyzhenskaya inequality is therefore applicable.

The Stieltjes localization exponents are correct:

\[
 Y_a+M_a=O(e^{-2r\Lambda(D-s)}),
 \quad
 Y_b+M_b=O(e^{-4r\Lambda(D-s)}),
 \quad
 Y_c+M_c=O(e^{-6r\Lambda(D-s)}).
\]

The strict gates are exactly

\[
 \frac13<2r,
 \qquad
 \frac12<3r,
 \qquad
 \frac12<4r.
\]

No uniform high-Sobolev propagation is used.

## 6. Fourth-order remainder

The residual sign is fixed consistently by

\[
 R_{\rm app}
 =\mathcal L u_{\rm app}
 +\mathcal B(u_{\rm app},u_{\rm app})
 -\partial_du_{\rm app}.
\]

The two transport cancellations are exact.  The product measures
\(N_4,N_5,N_6\), the extra
\(g=\|\nabla u_{\rm app}\|_2^2\) integrating factor, and the cumulative
dissipation estimate yield

\[
 \|e(D)\|_2\le C\delta^4
\]

uniformly in sufficiently large \(\Lambda\) and \(0<\delta\le1\).

## 7. Endpoint and seed

Harmonic parity removes the quadratic target contribution, so

\[
 \|\Pi_{\pm1}u(D)\|_2
 \ge\delta-C_3\delta^3-C_R\delta^4
 \ge\frac\delta2
\]

for fixed sufficiently small \(\delta\).  The actual-gain-normalized seed
satisfies

\[
 \|u(0)\|_{H^3}
 \le C\delta\Lambda^2e^{-r\Lambda D}\longrightarrow0.
\]

## 8. Remaining boundary

These are open boundaries, not defects in the audited theorem:

- the proof treats \(\delta/G_\Lambda\), not the prescribed seed
  \(\delta e^{-r\Lambda D}\);
- it does not determine the matching action of \(G_\Lambda\);
- it is a varying-background family result, not Lyapunov instability of
  one fixed background;
- it stays in a globally regular planar invariant class;
- it gives no transverse three-dimensional, vortex-stretching, singularity,
  or Clay conclusion.

Formal certificate generation and release sealing remain publication gates,
but there is no remaining mathematical correction obligation in the two
audited proof files.
