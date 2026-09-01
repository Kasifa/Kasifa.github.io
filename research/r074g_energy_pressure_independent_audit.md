# R0.74G — independent audit of buffered energy and gauge pressure

## Verdict

**PASS.**  No fatal or correctable mathematical error was found in
Sections 2--3 of the R0.74G main note.

The candidate source audited line by line was commit

    e92fbf8ab3b94c07c7a77513cb21d8e46f5bf49e

with full-note SHA-256

    757cd638b178105f8eaf03f99ebbc44366f5ba27c5099452a31d9787733d3d96.

After the audit, two optional exposition clarifications were added.  The
post-fix full-note SHA-256 checked read-only is

    7203fc857bce57b10a7bc788d5628c71760c7bfcdf158aefe443148a93e37725.

Those additions do not change a displayed estimate, scale, or
normalization.

---

## 1. Exact transverse-energy subsolution

For

\[
 H(t,z)=\int_{\mathbb T}|F(t,x_2,z)|^2\,dx_2,
\]

the passive equation gives

\[
 H_t-H_{zz}
 =-2\int_{\mathbb T}
 \left(|F_{x_2}|^2+|F_z|^2\right)dx_2\le0.
\]

The transport term vanishes exactly because its coefficient depends on
\(t,z\), not on \(x_2\).  The signs and the factor two are correct.

For one initial packet,

\[
 \|\partial K_{R^2}\|_2^2\asymp R^{-3},
 \qquad K_{R^2}(z-h)^2
 \asymp R^{-2}e^{-(z-h)^2/(2R^2)}.
\]

After the datum factor \(R^6\), the transverse marginal has scale

\[
 R^6R^{-3}R^{-2}=R.
\]

The paired field is controlled by
\(|F^++F^-|^2\le2(|F^+|^2+|F^-|^2)\).  Thus the initial marginal in
R0.74G (2.7) has the correct \(R\)-power and Gaussian exponent.

---

## 2. Buffered Gaussian exponent and cutoff row

The heat-convolved squared Gaussian has denominator

\[
 2R^2+4t\le262R^2
 \qquad(0\le t\le65R^2).
\]

Also,

\[
 h-16R
 =\left(\frac{15}{16}L-16\right)R
 \ge\frac{14}{15}LR
\]

whenever \(L\ge3840\).  Hence the exponent

\[
 d_E=\frac{(14/15)^2}{262}=\frac{98}{29475}
\]

is correct.  Its amplitude margin is

\[
 d_E-c_\gamma
 =\frac{17018}{12998475}>0.
\]

Let

\[
 \Psi=e^{-d_EL^2}+e^{-c/R^2}.
\]

The cutoff mass satisfies \(\int\eta_RF^2\le CR^2\Psi\).  Integrating
the exact cutoff energy identity gives

\[
 \int_{I_{8R}}\int\eta_R|\nabla_{2,3}F|^2
 \le CR^2\Psi.
\]

Indeed, the cutoff-error scale is

\[
 R^{-2}\cdot64R^2\cdot R^2\Psi=O(R^2\Psi).
\]

Multiplying by the invariant \(x_1\)-section and dividing by the
local-energy radius preserves the \(R^2\Psi\) scale.  The packet kinetic
row has the same scale.

Fixed polynomial factors multiplying a noncentral periodic Gaussian may be
absorbed after decreasing its positive exponent constant.  The post-audit
clarification stating this is valid.

---

## 3. Shear energy

On \(I_{8R}\),

\[
 |\theta|\le1,
 \qquad |\theta_3|\le Ct^{-1/2}\le C/R.
\]

Both the kinetic and gradient rows are therefore \(O(B^2R^2)\).  The
packet and shear occupy different velocity components, so their quadratic
velocity and gradient rows add without a mixed term.

---

## 4. Pressure gauge and Newton-ball formula

Because the physical pressure is zero,

\[
 h_\rho=-p_\rho^{\rm loc},
 \qquad c_\rho=-g_\rho,
 \qquad \pi-c_\rho=g_\rho.
\]

Thus the main note correctly retains a generally nonzero gauge row.

For \(\Gamma=(4\pi|y|)^{-1}\), the normalized ball potential satisfies

\[
 D^2N_a(y)=
 \begin{cases}
 -I/(3V_a),&|y|<a,\\
 D^2\Gamma(y),&|y|>a.
 \end{cases}
\]

Consequently the averaged local pressure is

\[
 g_\rho
 =-\frac1{3V_a}\int_{B_a}|u|^2
 +\int_{B_{4\rho}\setminus B_a}
 D^2\Gamma:(\zeta_\rho u\otimes u).
\]

The core sign, outer sign, and trace contraction are correct.  Both kernels
are bounded by \(C\rho^{-3}\), giving

\[
 |g_\rho|\le C\rho^{-3}\int_{B_{4\rho}}|u|^2.
\]

---

## 5. All-annulus pressure normalization

The exact volume is

\[
 |A_k(\rho)|=\frac{28\pi}{3}8^k\rho^3.
\]

Therefore the spatially constant gauge row becomes

\[
 \mathcal G_p
 =M_\gamma\rho\int_{I_\rho}|g_\rho(t)|^{3/2}dt,
\]

where

\[
 M_\gamma=\frac{28\pi}{3}
 \sum_{k\ge1}8^ke^{-4^{k-1}/32}<\infty.
\]

Using \(|I_\rho|=\rho^2\),

\[
 \mathcal G_p
 \le C\left[
 \rho^{-1}\sup_{I_\rho}
 \int_{B_{4\rho}}|u|^2
 \right]^{3/2}.
\]

The explicit comparison is

\[
 \rho^{-1}\sup_{I_\rho}\int_{B_{4\rho}}|u|^2
 \le4\mathcal E(z_0,4\rho).
\]

The factor \(4^{3/2}=8\) is harmless.  With \(\rho=2R\), this is exactly

\[
 \mathcal G_p(z_0,2R;1)
 \le C\mathcal E(z_0,8R)^{3/2}.
\]

No pressure annulus, periodic copy, or radius factor is missing.

---

## 6. Audit boundary

This audit establishes internal correctness of the energy and gauge-pressure
derivations in the cited source.  It does not audit the bridge occupation
lemma, the complete cubic/harmonic rows, the inherited R0.74F target, or any
Navier--Stokes regularity claim.  It is an analytic audit, not a numerical
certificate.  **NOT CLAY.**

