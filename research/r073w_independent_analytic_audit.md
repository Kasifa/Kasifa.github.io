# R0.73W independent analytic audit

**Audit date:** 2026-09-01

**Scope:** signs, indices, coefficients, scale weights, and weak-solution
boundaries in `r073w_signed_production_heat_characteristic.md`

**Result:** `PASS_WITH_WEAK_SOLUTION_BOUNDARY`

**Ordinary translation path:** `LOCAL_DIRECT_NO_DGX`

**DGX used:** `false`

## 1. Stress scale equation and matrix order

Write

\[
 A_{ij,s}=\partial_jv_{s,i},\qquad
 B_{ij,s}=\partial_\ell v_{s,i}\partial_\ell v_{s,j}.
\]

The componentwise heat-product rule gives

\[
 (\partial_s-\Delta)\tau_{ij,s}=2B_{ij,s}.
\]

Under the declared gradient convention,
\(B_s=\nabla v_s\nabla v_s^T\), not
\(\nabla v_s^T\nabla v_s\).  The parent proof uses the correct order.  Since
\(\tau_s\) is symmetric and \(S_s\) is trace-free, the reductions
\(\Pi_s=-\tau_s:S_s=-\tau_s^\circ:S_s\) also pass.

The product rule for \(\Pi_s=-\tau_{ij,s}A_{ij,s}\) independently gives

\[
 (\partial_s-\Delta)\Pi_s
 =2\partial_\ell\tau_{ij,s}\partial_{\ell j}v_{s,i}
 -2B_{ij,s}\partial_jv_{s,i}.
\]

Both signs and the factor 2 agree with parent equation (6.8).

## 2. Heat-plane characteristic sign

The filtered resolved-energy equation is

\[
 \partial_te_s+\nabla\cdot[(e_s+p_s)v_s+\tau_sv_s]
 =\nu\Delta e_s-\nu|\nabla v_s|^2-\Pi_s.
\]

The independent heat identity is

\[
 \partial_se_s=\Delta e_s-|\nabla v_s|^2.
\]

Their difference is therefore

\[
 (\partial_t-\nu\partial_s)e_s+\nabla\cdot F_s=-\Pi_s.
\]

The tangent characteristic has \(s'(t)=-\nu\), and

\[
 {d\over dt}E_{s(t)}(t)=-\langle\Pi_{s(t)}(t)\rangle.
\]

Thus the endpoint order in parent equation (3.6) is correct.  This is a
signed spatial-mean payment, not an estimate for \(|\Pi_s|\).

## 3. Energy-class exponent

The stress Duhamel formula gives

\[
 \|\tau_s\|_1
 \le2\int_0^s\|\nabla v_r\|_2^2dr
 \le2s\|\nabla u\|_2^2.
\]

The three-dimensional derivative heat estimate is

\[
 \|\nabla P_su\|_\infty
 \le Cs^{-5/4}\|u\|_2.
\]

Here \(5/4=1/2+3/4\).  Multiplication leaves exactly
\(s\,s^{-5/4}=s^{-1/4}\), and time integration gives the parent energy-class
bound.  Integrating in \(s\) gives \((4/3)S^{3/4}\).  The alternate
\(L^{3/2}\)-stress and \(L^3\)-gradient factorization gives the same power.
No optimality or zero-scale uniformity follows.

## 4. Centered-increment coefficient and sign

Use the Euclidean heat kernel on the periodic extension,

\[
 g_s(y)=(4\pi s)^{-3/2}e^{-|y|^2/(4s)},\qquad
 a_i(x,y)=u_i(x-y)-v_{s,i}(x).
\]

Then

\[
 \tau_{ij,s}=\int g_sa_ia_j\,dy,
 \qquad
 K_{j,s}={1\over2}\int g_sa_j|a|^2\,dy.
\]

Incompressibility gives \(\partial_ja_j=0\).  Direct differentiation yields

\[
 \partial_jK_{j,s}
 =\int g_sa_ia_j\partial_ju_i(x-y)\,dy+\Pi_s.
\]

Since \(\partial_{y_j}a_i=-\partial_ju_i(x-y)\) and
\(\partial_{y_j}a_j=0\), integration by parts in \(y\) gives

\[
 \int g_sa_ia_j\partial_ju_i(x-y)\,dy
 ={1\over2}\int(\partial_{y_j}g_s)a_j|a|^2\,dy.
\]

Therefore

\[
 \Pi_s=\partial_jK_{j,s}
 -{1\over2}\int\nabla g_s\cdot a|a|^2\,dy.
\]

Using \(\nabla g_s=-yg_s/(2s)\) confirms the parent coefficient and sign:

\[
 \boxed{
 \mathscr S_s={1\over4s}\int y\cdot a|a|^2g_s(y)\,dy.}
\]

This last kernel derivative must be used with the Euclidean kernel on the
periodic extension.  It should not be copied verbatim for a basic-cell
periodic-kernel coordinate.

## 5. Exact trace cancellation and positive row

The frozen R0.73V trace equation is

\[
 \partial_tk_s+\nabla\cdot(v_sk_s)
 =-\nabla\cdot(K_s+Q_s-\nu\nabla k_s)
 -\nu D_{ii,s}+\Pi_s.
\]

Substitution of \(\Pi_s=\nabla\cdot K_s+\mathscr S_s\) cancels \(K_s\)
with no residual coefficient.  The resulting signs are

\[
 \partial_tk_s+\nabla\cdot(v_sk_s+Q_s-\nu\nabla k_s)
 =-\nu D_{ii,s}+\mathscr S_s.
\]

Applying the covariance identity to every \(f=\partial_ku_i\) verifies

\[
 \boxed{
 D_{ii,s}=2\int_0^sP_{s-r}
 \sum_{i,k,\ell}(\partial_{\ell k}v_{r,i})^2\,dr\ge0.}
\]

Positivity belongs to this trace covariance.  It does not imply pointwise
positivity of \(\partial_s\tau_s\) or any contraction with trace-free strain.

## 6. Spatial mean and critical scale weight

Let \(h=(u\cdot\nabla)u\) and \(L=-\Delta\).  Periodic integration by parts,
incompressibility, and heat-semigroup self-adjointness give

\[
 \langle\Pi_s\rangle
 =\langle v_s,P_sh\rangle
 =\langle e^{-2sL}u,h\rangle.
\]

For mean-zero fields,

\[
 \int_0^\infty s^{-1/2}e^{-2s\lambda}\,ds
 =\sqrt{\pi/2}\,\lambda^{-1/2}.
\]

Hence both the constant and operator in the parent formula pass:

\[
 \int_0^\infty s^{-1/2}\langle\Pi_s\rangle\,ds
 =\sqrt{\pi/2}\langle L^{-1/2}u,h\rangle.
\]

One spatial integration by parts gives the Riesz form

\[
 -\sqrt{\pi/2}\int u_i u_jR_ju_i,
 \qquad R_j=\partial_jL^{-1/2}.
\]

The corresponding subfilter-energy derivative has multiplier
\(Lm_w(L)=\sqrt{\pi/2}L^{1/2}\), so parent equation (7.7) also passes.

## 7. Applicability boundary

- For smooth divergence-free fields, the displayed scale, increment, and
  physical-time identities are classical equalities.
- For a static \(u\in L^3(\mathbb T^3)\), the centered-increment split holds
  distributionally in space and the critical weighted spatial mean is the
  Riesz trilinear form.
- A Leray--Hopf solution belongs to \(L_t^4L_x^3\), so these static cubic
  identities hold for almost every time and the time-integrated estimate in
  parent equation (7.9) is valid.
- The resolved-energy characteristic identity is valid for Leray--Hopf
  solutions along positive-scale paths kept in \(s\ge\sigma>0\).  An endpoint
  at \(s=0\) requires the corresponding energy equality.
- The smooth subfilter-energy trace equality must not be asserted unchanged
  for arbitrary weak limits.  A suitable weak solution with local
  energy-defect measure \(\mu\ge0\) contributes \(-P_s\mu\) to the right-hand
  side of the trace equation.
- Strong \(L^3\) approximation passes the centered cubic and Riesz forms.
  Weak gradient convergence alone does not give strong convergence of
  \(D_{ii,s}\).

## 8. Machine-readable conclusion

```text
centeredIncrementSign=PASS
centeredIncrementCoefficient=PASS_1_OVER_4S
traceKCancellation=PASS
pressureFluxSign=PASS
viscousCovarianceSign=PASS
gradientCovarianceHeatLift=PASS_FACTOR_2
meanProductionSemigroupIdentity=PASS
criticalWeightConstant=PASS_SQRT_PI_OVER_2
criticalRieszReduction=PASS
energyClassFixedScaleExponent=PASS_1_OVER_4
smoothApplicability=PASS
lerayStaticApplicability=PASS_AE_TIME
lerayPositiveScaleCharacteristic=PASS_AWAY_FROM_S0
lerayLocalTraceEquality=REQUIRES_ENERGY_DEFECT_ACCOUNTING
strongL3ApproximationPassage=PASS
weakGradientPassageForD=NOT_STRONG
analyticDisplayedIdentities=PASS
ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX
dgxUsed=false
NOT CLAY
```
