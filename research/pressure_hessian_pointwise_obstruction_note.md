# R0.69H — Pressure Hessian nonlocality and the pointwise-sign obstruction

## 1. Result

R0.69G shows that sign cancellation in the vorticity-direction kernel is not
robust when the vorticity magnitude may concentrate on one sign lobe. The
next candidate is the pressure Hessian, because it is the nonlocal term that
counteracts local velocity-gradient self-amplification in many statistical
descriptions of turbulence.

The exact strain equation on
\(\mathbb T^3=(\mathbb R/2\pi\mathbb Z)^3\) is

\[
 \boxed{
 (\partial_t+u\cdot\nabla-\Delta)S
 +S^2+\frac14\omega\otimes\omega
 -\frac14|\omega|^2I+\nabla^2p=0.}
 \tag{1.1}
\]

Let

\[
 A=\nabla u,\qquad
 S=\frac12(A+A^T),\qquad
 q=\operatorname{tr}(A^2)
   =|S|^2-\frac12|\omega|^2.
 \tag{1.2}
\]

Then

\[
 -\Delta p=q,\qquad \int_{\mathbb T^3}q\,dx=0.
 \tag{1.3}
\]

If \(G\) is the mean-zero periodic Green function for \(-\Delta\), the pressure
Hessian is

\[
 \boxed{
 H_{ij}(x):=\partial_{ij}p(x)
 =\operatorname{p.v.}\!\int_{\mathbb T^3}
 \partial_{ij}G(z)\,q(x+z)\,dz.}
 \tag{1.4}
\]

Its local singular part is the trace-free quadrupole

\[
 \boxed{
 H_{ij}(x)
 =-\frac13\delta_{ij}q(x)
 +\frac1{4\pi}\operatorname{p.v.}\!\int
 \chi(z)\frac{3\widehat z_i\widehat z_j-\delta_{ij}}{|z|^3}
 q(x+z)\,dz
+(\mathcal R_\chi q)_{ij}(x).}
 \tag{1.5}
\]

The decisive result is an exact pointwise obstruction:

\[
 \boxed{
 \text{the sign of }e_1^T\nabla^2p\,e_1
 \text{ is not determined by the local pair }(S,\omega).}
 \tag{1.6}
\]

I prove (1.6) inside the class of smooth periodic divergence-free velocity
fields. Two explicit families have exactly the same velocity gradient at the
origin,

\[
 S(0)=\operatorname{diag}(1,-1,0),\qquad \omega(0)=0,
 \tag{1.7}
\]

so the principal stretching direction is the fixed vector \(e_1=(1,0,0)\).
Nevertheless their pressure Hessians satisfy

\[
 \boxed{
 H_{11}^{-}(0)=-1-\frac{54}{85}t^2,\qquad
 H_{11}^{+}(0)=-1+\frac{54}{85}t^2.}
 \tag{1.8}
\]

For \(t^2>85/54\), the two values have opposite signs. Thus no pointwise
closure \(H_{11}=F(S,\omega)\), and no universal pointwise sign rule based
only on \(S,\omega\), can capture pressure compensation.

This is a structural negative result. It does not prove regularity, construct
a singularity, or solve the three-dimensional Navier--Stokes problem.

## 2. Derivation of the strain and pressure equations

Use the convention \(A_{ij}=\partial_j u_i\). Differentiating the momentum
equation gives

\[
 (\partial_t+u\cdot\nabla-\Delta)A+A^2+\nabla^2p=0.
 \tag{2.1}
\]

Write \(A=S+\Omega\). The symmetric part of \(A^2\) is

\[
 \operatorname{sym}(A^2)=S^2+\Omega^2.
 \tag{2.2}
\]

Since

\[
 \Omega_{ij}=-\frac12\varepsilon_{ijk}\omega_k,\qquad
 \Omega^2=\frac14\bigl(\omega\otimes\omega-|\omega|^2I\bigr),
 \tag{2.3}
\]

equation (2.1) yields (1.1). Taking the trace of (2.1), using
\(\operatorname{tr}A=0\), gives (1.3).

The spatial mean in (1.3) vanishes for every smooth periodic divergence-free
field:

\[
 \int_{\mathbb T^3}\partial_j u_i\,\partial_i u_j\,dx
 =-\int_{\mathbb T^3}u_i\,\partial_i\partial_j u_j\,dx=0.
 \tag{2.4}
\]

For nonzero Fourier modes,

\[
 \widehat H_{ij}(k)
 =-\frac{k_i k_j}{|k|^2}\widehat q(k).
 \tag{2.5}
\]

The distributional Hessian of \(1/(4\pi|z|)\) is

\[
 \partial_{ij}\frac1{4\pi|z|}
 =-\frac13\delta_{ij}\delta_0
 +\operatorname{p.v.}
 \frac{3z_i z_j-|z|^2\delta_{ij}}{4\pi|z|^5}.
 \tag{2.6}
\]

Combining (2.6) with the smooth part of the periodic Green function proves
(1.5).

## 3. Exact principal-eigenvalue budget

Assume the largest eigenvalue \(\lambda_1\) of \(S\) is simple, with a smooth
orthonormal eigenframe \(e_1,e_2,e_3\). Standard eigenvalue differentiation
gives

\[
 e_1^T\Delta S\,e_1
 =\Delta\lambda_1
 -2\sum_{a=1}^3\sum_{j=2}^3
 \frac{|e_j^T(\partial_aS)e_1|^2}{\lambda_1-\lambda_j}.
 \tag{3.1}
\]

Therefore

\[
 \boxed{
 (\partial_t+u\cdot\nabla-\Delta)\lambda_1
 =-\lambda_1^2+\frac14|\omega\times e_1|^2
 -e_1^THe_1-\Gamma_1,}
 \tag{3.2}
\]

where

\[
 \Gamma_1
 =2\sum_{a=1}^3\sum_{j=2}^3
 \frac{|e_j^T(\partial_aS)e_1|^2}{\lambda_1-\lambda_j}
 \ge0.
 \tag{3.3}
\]

The term \(-\Gamma_1\) is favorable for the largest eigenvalue. The pressure
term has no pointwise sign. With

\[
 H^\circ=H+\frac13qI,
 \tag{3.4}
\]

equation (3.2) becomes

\[
 (\partial_t+u\cdot\nabla-\Delta)\lambda_1
 =-\lambda_1^2+\frac14|\omega\times e_1|^2
 +\frac13q-e_1^TH^\circ e_1-\Gamma_1.
 \tag{3.5}
\]

The restricted-Euler approximation keeps the local \(q/3\) term and drops
\(H^\circ\). Formula (1.8) shows why a universal pointwise replacement for
the omitted term cannot depend only on the local velocity gradient.

## 4. Mean-zero source does not force quadrupolar cancellation

The constraint \(\int q=0\) is real, but by itself it does not yield a small
constant. For any \(K\in L^\infty(A)\),

\[
 \boxed{
 \sup_{\substack{\int_A g=0\\ \|g\|_{L^1(A)}=1}}
 \left|\int_AKg\right|
 =\frac12\left(
 \operatorname*{ess\,sup}_A K-\operatorname*{ess\,inf}_A K
 \right).}
 \tag{4.1}
\]

Indeed, the positive and negative parts of \(g\) each have mass \(1/2\).
Concentrating them near the essential maximum and minimum proves equality.

For a fixed unit vector \(e\), the angular quadrupole is

\[
 Q_e(\theta)=3(e\cdot\theta)^2-1,
 \qquad
 \int_{\mathbb S^2}Q_e\,d\sigma=0,
 \qquad
 \min Q_e=-1,\quad\max Q_e=2.
 \tag{4.2}
\]

Thus a mean-zero signed source can still select the two extreme angular
regions and recover half the full oscillation. Equation (4.1) alone does not
assert that every such scalar source is generated by a velocity gradient.
The explicit fields below remove that concern for the pointwise-sign claim.

## 5. Exact divergence-free witnesses

Embed a two-dimensional stream function in three dimensions by

\[
 u_\psi=(-\partial_y\psi,\partial_x\psi,0).
 \tag{5.1}
\]

Set

\[
 \psi_0=-\sin x\sin y
 \tag{5.2}
\]

and introduce

\[
 \phi_{m,n}=(1-\cos mx)(1-\cos ny).
 \tag{5.3}
\]

Consider

\[
 \psi_t^-=\psi_0+t\phi_{1,2},\qquad
 \psi_t^+=\psi_0+t\phi_{2,1}.
 \tag{5.4}
\]

Because every second derivative of \(\phi_{m,n}\) vanishes at the origin,

\[
 \nabla u_{\psi_t^-}(0)
 =\nabla u_{\psi_t^+}(0)
 =\begin{pmatrix}1&0&0\\0&-1&0\\0&0&0\end{pmatrix}.
 \tag{5.5}
\]

For a two-dimensional stream function,

\[
 q=-2\det\nabla^2\psi.
 \tag{5.6}
\]

Expanding (5.6) in exact Fourier coefficients, applying the multiplier
(2.5), and evaluating at the origin gives

\[
 H_{11}[\psi_0](0)=-1,
 \tag{5.7}
\]

\[
 H_{11}[\psi_0,\phi_{1,2}](0)
 =H_{11}[\psi_0,\phi_{2,1}](0)=0,
 \tag{5.8}
\]

and

\[
 H_{11}[\phi_{1,2}](0)=-\frac{54}{85},\qquad
 H_{11}[\phi_{2,1}](0)=+\frac{54}{85}.
 \tag{5.9}
\]

Equations (5.7)--(5.9) prove (1.8). Both witnesses are smooth, periodic,
real-valued, and divergence free. They are legitimate smooth initial data;
the pressure Hessian calculation is the exact instantaneous pressure
determined by those data.

The witnesses are two-dimensional and therefore globally regular. Their
purpose is only to isolate the nonlocal information missing from the local
pair \((S,\omega)\).

## 6. Literature boundary

The strain equation (1.1) and its global strain-space structure are known.
Evan Miller used the strain formulation and the exact global identity

\[
 \frac{d}{dt}\|S\|_2^2
 =-2\|\nabla S\|_2^2-4\int\det S
 \tag{6.1}
\]

to obtain scale-critical criteria involving the positive part of the middle
strain eigenvalue. A new pointwise pressure-sign criterion must be compared
with this stronger global cancellation mechanism.

The turbulence literature also treats the anisotropic pressure Hessian as a
nonlocal closure problem. Chevillard and collaborators explicitly separated
local and nonlocal pressure-Hessian effects, and later work studies how the
anisotropic pressure Hessian counteracts velocity-gradient self-amplification
statistically. Those statistical observations do not supply the deterministic
pointwise sign needed here.

I do not claim that the nonlocality of the pressure Hessian is new. The
specific contribution of R0.69H is the exact, source-audited periodic witness
(5.4)--(5.9) and the resulting route decision.

References used for the boundary:

1. E. Miller, *A regularity criterion for the Navier--Stokes equation
   involving only the middle eigenvalue of the strain tensor*, Arch. Rational
   Mech. Anal. 235 (2020), 99--139,
   https://doi.org/10.1007/s00205-019-01419-z.
2. L. Chevillard, E. Leveque, F. Taddia, C. Meneveau, H. Yu, and C. Rosales,
   *Local and nonlocal pressure Hessian effects in real and synthetic fluid
   turbulence*, Phys. Fluids 23 (2011), arXiv:1106.1046.
3. M. Wilczek and C. Meneveau, *Pressure Hessian and viscous contributions to
   velocity gradient statistics based on Gaussian random fields*, J. Fluid
   Mech. 756 (2014), 191--225, arXiv:1401.3351.

## 7. Certified checks

The audit research/pressure_hessian_pointwise_obstruction_audit.py checks:

1. the matrix identities (2.2)--(2.3);
2. the zero mean of \(q\) for the two exact witness families;
3. divergence freedom and the common local gradient (5.5);
4. the exact Fourier pressure multiplier (2.5);
5. the three coefficients (5.7)--(5.9);
6. the sign reversal above \(t^2=85/54\);
7. the finite mean-zero selector analogue of (4.1);
8. the quadrupole mean, minimum, and maximum in (4.2).

These checks certify finite symbolic and Fourier calculations. The continuum
identities (1.1)--(4.2) are proved algebraically in the note.

## 8. Decision and next step

R0.69H closes the pointwise pressure-compensation branch:

\[
 \boxed{
 \text{local }(S,\omega)\text{ data do not determine even the sign of the}
 \text{ principal pressure-Hessian component}.}
 \tag{8.1}
\]

The pressure Hessian remains potentially useful only through genuinely
nonlocal or integrated structure. R0.69I will localize the exact strain-space
orthogonality

\[
 \int_{\mathbb T^3}S:\nabla^2p\,dx=0
 \tag{8.2}
\]

with a spatial weight, derive every resulting commutator term, and test
whether a scale-invariant localized strain budget survives. If localization
only reproduces an uncontrolled pressure commutator, I will record that
obstruction and continue.

R0.69H does not prove regularity or singularity for three-dimensional
Navier--Stokes and does not solve the Millennium Problem.
