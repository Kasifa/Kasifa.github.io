# R0.69O — Dissipation-assisted time closure of the pressure commutator

## 1. Result

R0.69N replaced the unavailable near pressure-source norm by the spatial
estimate

\[
 r^3|\mathcal P_{v,r}|
 \leq C\mu_v^{1/2}\sigma_v^{3/2}
       \bigl(D_A^{1/2}+\sigma_A+\mu_A\bigr),                    \tag{1.1}
\]

where

\[
 \mu_v=r^{-1/2}\|v\|_2,\qquad
 \sigma_v=r^{1/2}\|\nabla v\|_2,\qquad
 D_A=r^3\|\nabla^2u\|_{L^2(A_\phi)}^2.                          \tag{1.2}
\]

Using Young's inequality only once leaves
\(\mu_v\sigma_v^3\), whose time integral is not controlled by the quadratic
CKN dissipation. R0.69O shows that this is not the final pressure exponent.
The second-derivative term that is already being absorbed also supplies the
Hilbert interpolation

\[
 \boxed{\sigma_v^2\leq C\mu_v\mathcal D_v^{1/2}},\qquad
 \mathcal D_v=r^3\|\nabla^2v\|_2^2.                             \tag{1.3}
\]

Because \(v=u\) on \(B_{2r}\) and
\(A_\phi\subset B_r\), one also has \(D_A\leq\mathcal D_v\). Thus the
leading term in (1.1) is bounded by the left side of the following estimate.

Consequently, for every \(\varepsilon>0\),

\[
 \boxed{
 \mu_v^{1/2}\sigma_v^{3/2}\mathcal D_v^{1/2}
 \leq \varepsilon\mathcal D_v+
      C\varepsilon^{-3}\mu_v^4\sigma_v^2.}                     \tag{1.4}
\]

Let \(\tau=(t-t_0)/r^2\) be normalized time on an interval \(I\) of length
one, and set

\[
 \mathsf A_v=\|\mu_v\|_{L^\infty_\tau(I)}^2,\qquad
 \mathsf E_v=\int_I\sigma_v^2\,d\tau,\qquad
 \mathsf F_v=\int_I\mathcal D_v\,d\tau.                         \tag{1.5}
\]

Then the leading near-pressure term closes as

\[
 \boxed{
 \int_I\mu_v^{1/2}\sigma_v^{3/2}\mathcal D_v^{1/2}\,d\tau
 \leq\varepsilon\mathsf F_v+
      C\varepsilon^{-3}\mathsf A_v^2\mathsf E_v.}               \tag{1.6}
\]

Thus the temporal remainder is quadratic in enstrophy, with a
scale-invariant local kinetic-energy coefficient. The time spike from R0.69N
does not contradict (1.6): enforcing (1.3) makes its second-derivative mass
diverge.

The exponent \(\mu_v^4\) is algebraically sharp if (1.3) is the only
additional input. This closes the previously missing temporal exponent in
the leading pressure commutator at the smooth level. It does not by itself
derive a complete localized \(H^1\) inequality, and it does not close the full
Navier--Stokes regularity problem. The localized cubic strain/vorticity stretching
term remains.

## 2. The exact Hilbert interpolation

The field \(v\) from R0.69N is compactly supported and divergence free. By
integration by parts,

\[
 \|\nabla v\|_2^2
 =-\int v\cdot\Delta v\,dx
 \leq\|v\|_2\|\Delta v\|_2
 \leq C\|v\|_2\|\nabla^2v\|_2.                                 \tag{2.1}
\]

Multiplying by \(r\) gives exactly (1.3):

\[
 r\|\nabla v\|_2^2
 \leq C
 \bigl(r^{-1/2}\|v\|_2\bigr)
 \bigl(r^{3/2}\|\nabla^2v\|_2\bigr).                            \tag{2.2}
\]

All three factors are invariant under the Navier--Stokes scaling. For a
Fourier packet concentrated at wavenumber \(k\), (2.1) is saturated up to a
constant:

\[
 \|\nabla v\|_2\asymp k\|v\|_2,\qquad
 \|\nabla^2v\|_2\asymp k^2\|v\|_2.                             \tag{2.3}
\]

## 3. Two uses of Young's inequality recover the quadratic time power

Write \(\mu=\mu_v\), \(\sigma=\sigma_v\), and
\(\mathcal D=\mathcal D_v\). First,

\[
 \mu^{1/2}\sigma^{3/2}\mathcal D^{1/2}
 \leq\delta\mathcal D+C\delta^{-1}\mu\sigma^3.                  \tag{3.1}
\]

The factor left by (3.1) is not estimated in time immediately. Instead,
(1.3) gives

\[
 \mu\sigma^3
 =\mu\sigma\,\sigma^2
 \leq C\mu^2\sigma\mathcal D^{1/2}.                             \tag{3.2}
\]

A second Young inequality yields

\[
 C\delta^{-1}\mu^2\sigma\mathcal D^{1/2}
 \leq\delta\mathcal D+C\delta^{-3}\mu^4\sigma^2.                \tag{3.3}
\]

Combining (3.1)--(3.3), and renaming \(2\delta\) as \(\varepsilon\),
proves (1.4). Taking the \(L^\infty_\tau\) norm of \(\mu^4\) and integrating
proves (1.6).

The important distinction is that \(\mathcal D\) is used twice: once as the
term to absorb, and once through interpolation. A time-only Hölder inequality
cannot do this.

## 4. The previous spike pays an unbounded second-derivative bill

R0.69N used

\[
 \mu_A(\tau)=1,\qquad
 \sigma_A(\tau)=A\mathbf1_{[0,A^{-2}]}(\tau),                  \tag{4.1}
\]

so that

\[
 \int\sigma_A^2\,d\tau=1,\qquad
 \int\mu_A\sigma_A^3\,d\tau=A.                                 \tag{4.2}
\]

If (1.3) is imposed, then on the spike

\[
 \mathcal D_A\geq c\frac{\sigma_A^4}{\mu_A^2}=cA^4.             \tag{4.3}
\]

Therefore

\[
 \boxed{\int\mathcal D_A\,d\tau\geq cA^2\longrightarrow\infty.} \tag{4.4}
\]

The spike remains a valid no-go witness for a time-only estimate from
\(\int\sigma^2\), but it is not a witness against dissipation-assisted
absorption.

## 5. The kinetic exponent four is sharp inside this mechanism

Suppose one seeks an algebraic estimate of the form

\[
 \mu^{1/2}\sigma^{3/2}\mathcal D^{1/2}
 \leq\varepsilon\mathcal D+C_\varepsilon\mu^\alpha\sigma^2,    \tag{5.1}
\]

using only nonnegativity and
\(\sigma^2\leq\mu\mathcal D^{1/2}\). Saturate the interpolation and write

\[
 \sigma=\mu z,\qquad \mathcal D=\mu^2z^4.                      \tag{5.2}
\]

After division by \(\mu^2z^2\), (5.1) requires

\[
 \mu z^{3/2}\leq\varepsilon z^2+C_\varepsilon\mu^\alpha.       \tag{5.3}
\]

The maximum of the left side minus the first right-side term occurs at

\[
 z_*=\left(\frac{3\mu}{4\varepsilon}\right)^2                 \tag{5.4}
\]

and equals

\[
 \frac{27}{256}\varepsilon^{-3}\mu^4.                          \tag{5.5}
\]

Hence \(\alpha\geq4\), and at \(\alpha=4\) the
\(\varepsilon^{-3}\) dependence is also optimal at the algebraic level.
Estimate (1.4) attains both exponents. This is sharpness of the interpolation
mechanism, not a claim that a Navier--Stokes pressure field saturates every
preceding estimate.

## 6. The localized second derivative is available on one enlarged ball

The R0.69N localization is

\[
 v=\eta u-w,\qquad \nabla\cdot w=\nabla\eta\cdot u,             \tag{6.1}
\]

where the correction is supported in a fixed-shape annulus. The higher-order
Sobolev mapping property of the Bogovskii operator gives

\[
 \|\nabla^2w\|_2
 \leq C\left(
 r^{-1}\|\nabla u\|_{L^2(A_\eta)}
 +r^{-2}\|u\|_{L^2(A_\eta)}\right).                             \tag{6.2}
\]

The same product-rule terms occur in \(\nabla^2(\eta u)\). Consequently,

\[
 \boxed{
 \mathcal D_v^{1/2}
 \leq C\left(
 D_{3r}^{1/2}+\sigma_{A_\eta}+\mu_{A_\eta}\right),}             \tag{6.3}
\]

where

\[
 D_{3r}=r^3\|\nabla^2u\|_{L^2(B_{3r})}^2.                      \tag{6.4}
\]

In particular,

\[
 \varepsilon\mathcal D_v
 \leq C\varepsilon D_{3r}
 +C\varepsilon\bigl(\sigma_{A_\eta}^2+\mu_{A_\eta}^2\bigr).    \tag{6.5}
\]

Thus the abstract absorbable term in (1.4) becomes an enlarged-ball
second-derivative term plus explicit cutoff costs. Any later use inside a
full local energy argument must still perform the corresponding radius
iteration and account for all equations generated by the localization.

For compactly supported divergence-free fields,
\(\|\nabla^2v\|_2^2\) is comparable to
\(\|\nabla S[v]\|_2^2\) by the Fourier identity. Thus the leading part of
\(\mathcal D_v\) is precisely the dissipation in a localized smooth
strain-energy estimate on an enlarged ball. The other terms in (6.3) are
lower-order cutoff costs.

This is a one-step radius enlargement, not an infinite nonlocal cascade.
It does, however, require a smooth approximation or a strong solution:
generic suitable weak solutions do not have \(L^2_{t,x}\) second derivatives
a priori.

## 7. Lower commutator terms and the remote budget

The lower part of (1.1) is controlled using
\(\sigma\leq C\mu^{1/2}\mathcal D^{1/4}\):

\[
 \begin{aligned}
 \mu^{1/2}\sigma^{5/2}
 &\leq\varepsilon\mathcal D
   +C\varepsilon^{-5/3}\mu^{14/3},\\
 \mu^{3/2}\sigma^{3/2}
 &\leq\varepsilon\mathcal D
   +C\varepsilon^{-3/5}\mu^{18/5}.                             \tag{7.1}
 \end{aligned}
\]

On a unit normalized time interval these are finite powers of
\(\mathsf A_v\). They are lower-order Caccioppoli costs, not critical
dissipation terms.

The transition and far-shell contribution remains

\[
 r^3|\mathcal P_{\mathrm{ext}}|
 \leq C\sigma_r(e_{\mathrm{tr}}+B_\infty).                     \tag{7.2}
\]

If

\[
 \mathsf H=\|e_{\mathrm{tr}}+B_\infty\|_{L^\infty_\tau(I)},
                                                                            \tag{7.3}
\]

then

\[
 \int_I r^3|\mathcal P_{\mathrm{ext}}|\,d\tau
 \leq C\mathsf H\mathsf E_r^{1/2}
 \leq\delta\mathsf E_r+C\delta^{-1}\mathsf H^2.                \tag{7.4}
\]

R0.69M still supplies
\(B_\infty\leq\mathfrak M_2/120\). No far-shell gain is lost.

## 8. Complete temporal pressure statement

Combining the preceding estimates gives the schematic pressure-sector
Caccioppoli bound

\[
 \begin{aligned}
 \int_I r^3|\mathcal P_r|\,d\tau
 \leq{}&
 \varepsilon\mathsf F_v
 +C\varepsilon^{-3}\mathsf A_v^2\mathsf E_v\\
 &+C_\varepsilon\left(
   \mathsf A_v^{7/3}+\mathsf A_v^{9/5}\right)
 +\delta\mathsf E_r+C\delta^{-1}\mathsf H^2.                  \tag{8.1}
 \end{aligned}
\]

The first line is the principal result: the leading near-pressure term is an
absorbable second-derivative contribution plus quadratic enstrophy with a
scale-invariant energy coefficient. The second line contains lower-order
cutoff, transition, and remote-energy costs.

## 9. What remains in the full equation

Estimate (8.1), together with (6.5), repairs the pressure commutator's time
exponent in a localized smooth \(H^1\) calculation. It does not derive or
close the full identity. The convection/strain stretching term contains the
scale-invariant quantity

\[
 r^3\int|\nabla u|^3\,dx
 \leq C\sigma^{3/2}\mathcal D^{3/4}
 \leq\varepsilon\mathcal D+C_\varepsilon\sigma^6.              \tag{9.1}
\]

Unlike the pressure term, the interpolation (1.3) does not turn (9.1) into a
quadratic-enstrophy remainder: substituting it produces a power of
\(\mathcal D\) greater than one. This is the classical vortex-stretching
obstruction in localized form.

The route decision is therefore:

1. the R0.69N pressure commutator passes its temporal acceptance test once
   the absorbable second derivative is used through Hilbert interpolation;
2. backward-heat-kernel or time-frequency cancellation is not needed to
   repair the leading pressure exponent;
3. the next unresolved term is the signed cubic strain/vorticity stretching,
   not pressure.

R0.69P will test whether strain-eigenframe geometry, vorticity-direction
coherence, or a signed space-time commutator can reduce (9.1) without assuming
a known conditional regularity criterion.

R0.69O proves no global regularity or singularity conclusion. It does not solve the Millennium Problem.

## 10. Primary sources

1. L. Caffarelli, R. Kohn, and L. Nirenberg, *Partial regularity of suitable
   weak solutions of the Navier--Stokes equations*, Comm. Pure Appl. Math. 35
   (1982), 771--831,
   <https://doi.org/10.1002/cpa.3160350604>.
2. M. E. Bogovskii, *Solution of the first boundary value problem for the
   equation of continuity of an incompressible medium*, Dokl. Akad. Nauk SSSR
   248 (1979), 1037--1040,
   <https://www.mathnet.ru/eng/dan43056>.
3. J. Guzmán and A. J. Salgado, *Estimation of the continuity constants for
   Bogovskii and regularized Poincare integral operators*, J. Math. Anal.
   Appl. 502 (2021), 125246,
   <https://arxiv.org/abs/2010.04105>.
4. A. Vasseur and J. Yang, *Second derivatives estimate of suitable solutions
   to the 3D Navier--Stokes equations*,
   <https://arxiv.org/abs/2009.14291>.
