# R0.69P — Sharp sign geometry of vortex stretching and its local realization

## 1. Result

R0.69O returns the leading localized pressure commutator to a quadratic
enstrophy time integral. The remaining cubic term is the genuinely
three-dimensional production

\[
 \mathcal V(u)=\int \omega\cdot S\omega\,dx,
 \qquad
 S=\frac12(\nabla u+\nabla u^T),
 \qquad \omega=\nabla\times u.                                \tag{1.1}
\]

R0.69P determines exactly what can, and cannot, be obtained from the
pointwise algebra of \((S,\omega)\) and incompressibility alone.

For every real symmetric trace-free \(3\times3\) matrix \(S\),

\[
 \boxed{
 |\omega\cdot S\omega|
 \leq \sqrt{\frac23}\,|S|\,|\omega|^2.}                      \tag{1.2}
\]

The constant is sharp. More strongly, for every \(s,w>0\), there is a
smooth compactly supported divergence-free field \(v\) and a ball on which

\[
 |S[v]|=s,\qquad |\omega[v]|=w,\qquad
 \omega[v]\cdot S[v]\omega[v]
 =\sqrt{\frac23}\,s w^2.                                     \tag{1.3}
\]

Changing the sign of the strain gives the opposite sign with the same
magnitudes. Thus incompressibility, smoothness, and finite energy do not
produce a universal pointwise sign or a coefficient smaller than
\(\sqrt{2/3}\).

There is one exact global reorganization. If
\(\lambda_1\leq\lambda_2\leq\lambda_3\) are the eigenvalues of \(S\), then
Betchov's identity gives

\[
 \boxed{
 \int\omega\cdot S\omega\,dx
 =-4\int\det S\,dx,}                                         \tag{1.4}
\]

and pointwise

\[
 \boxed{
 -4\det S\leq 2\lambda_2^+|S|^2.}                            \tag{1.5}
\]

The constant two in (1.5) is sharp as a supremum. This identifies the
positive middle strain eigenvalue as the correct signed quantity, but it
does not control that quantity. In fact,

\[
 \boxed{0\leq\lambda_2^+\leq\frac{|S|}{\sqrt6}}               \tag{1.6}
\]

is sharp and is locally realizable by smooth divergence-free fields. With
only energy-level norms, (1.5)--(1.6) return to \(\int|S|^3\), hence to

\[
 \|S\|_3^3
 \lesssim \|S\|_2^{3/2}\|\nabla S\|_2^{3/2}
 \leq \varepsilon\|\nabla S\|_2^2
 +C\varepsilon^{-3}\|S\|_2^6.                                \tag{1.7}
\]

Therefore the middle-eigenvalue reformulation is structurally informative
but supplies no unconditional exponent gain. Any successful continuation
must add a nonlocal or spacetime mechanism that controls
\(\lambda_2^+\), vorticity direction coherence, or an equivalent signed
depletion observable. R0.69P does not prove or disprove global regularity and
does not solve the Millennium Problem.

## 2. Sharp pointwise stretching constant

Let \(\lambda_1\leq\lambda_2\leq\lambda_3\), with
\(\lambda_1+\lambda_2+\lambda_3=0\). The Rayleigh quotient gives

\[
 |\omega\cdot S\omega|\leq
 \max\{|\lambda_1|,|\lambda_3|\}|\omega|^2.                  \tag{2.1}
\]

Because

\[
 \lambda_1^2+\lambda_2^2
 \geq\frac12(\lambda_1+\lambda_2)^2
 =\frac12\lambda_3^2,
\]

one has \(\lambda_3^2\leq(2/3)|S|^2\). Applying the same argument to
\(-S\) controls \(|\lambda_1|\) and proves (1.2).

Equality is attained by

\[
 S_+=s\,\operatorname{diag}
 \left(-\frac1{\sqrt6},-\frac1{\sqrt6},\frac2{\sqrt6}\right),
 \qquad \omega_+=w e_3,                                      \tag{2.2}
\]

for which

\[
 |S_+|=s,\qquad
 \omega_+\cdot S_+\omega_+
 =\frac2{\sqrt6}sw^2
 =\sqrt{\frac23}sw^2.                                        \tag{2.3}
\]

The pair \((-S_+,\omega_+)\) attains the negative endpoint. This is an
algebraic equality, not a numerical near-saturation.

## 3. Every trace-free velocity-gradient jet is locally realizable

The pointwise witnesses above must still be compatible with a velocity
field. Let

\[
 A=S+\Omega,\qquad
 \Omega x=\frac12\omega\times x,
 \qquad \operatorname{tr}A=0,                                \tag{3.1}
\]

and set \(u_A(x)=Ax\). Then \(\nabla\cdot u_A=0\),
\(S[u_A]=S\), and \(\nabla\times u_A=\omega\). Although the affine field
does not have finite energy, it has the quadratic vector potential

\[
 B_A(x)=-\frac13 x\times(Ax),
 \qquad \nabla\times B_A=Ax.                                 \tag{3.2}
\]

Choose \(\chi\in C_c^\infty(B_2)\) with \(\chi=1\) on \(B_1\), and define

\[
 \boxed{v_A=\nabla\times(\chi B_A).}                           \tag{3.3}
\]

Then \(v_A\in C_c^\infty(\mathbb R^3)\),
\(\nabla\cdot v_A=0\), and \(v_A=Ax\) throughout \(B_1\). Hence every
trace-free matrix \(A\), including both equality cases in Section 2, occurs
on an open set inside a smooth finite-energy solenoidal field.

This construction is stronger than a single-point jet argument. Any
universal local estimate that improves (1.2) using only incompressibility
and smoothness fails on the entire core ball. The cutoff annulus supplies
the global compensation required by integral identities, but it cannot
alter the prescribed core geometry.

## 4. Betchov converts alignment into the strain determinant

Write \(A=S+\Omega\), with

\[
 \Omega^2=\frac14(\omega\otimes\omega-|\omega|^2I).           \tag{4.1}
\]

Cyclicity of the trace gives the pointwise identity

\[
 \operatorname{tr}(A^3)
 =\operatorname{tr}(S^3)+3\operatorname{tr}(S\Omega^2)
 =\operatorname{tr}(S^3)+\frac34\omega\cdot S\omega.         \tag{4.2}
\]

For a smooth periodic or sufficiently decaying divergence-free field,
integration by parts gives

\[
 \int\operatorname{tr}(A^3)\,dx=0.                            \tag{4.3}
\]

Since a trace-free \(3\times3\) matrix satisfies
\(\operatorname{tr}(S^3)=3\det S\), equations (4.2)--(4.3) prove (1.4).
This is the unweighted identity whose exact cutoff flux was computed in
R0.69I. It does not make the production nonpositive: it replaces vorticity
alignment by a signed strain determinant.

For a smooth Navier--Stokes solution with viscosity \(\nu>0\), the equivalent
enstrophy and strain identities are

\[
 \frac12\frac d{dt}\|\omega\|_2^2
 +\nu\|\nabla\omega\|_2^2
 =\int\omega\cdot S\omega
 =-4\int\det S,                                               \tag{4.4}
\]

and

\[
 \frac12\frac d{dt}\|S\|_2^2
 +\nu\|\nabla S\|_2^2
 =-2\int\det S.                                               \tag{4.5}
\]

The factor difference is consistent with
\(\|\omega\|_2^2=2\|S\|_2^2\) and
\(\|\nabla\omega\|_2^2=2\|\nabla S\|_2^2\).

## 5. Exact middle-eigenvalue reduction

If \(\lambda_2\leq0\), then
\(\det S=\lambda_1\lambda_2\lambda_3\geq0\), so
\(-4\det S\leq0\). Positive production can therefore occur only where
\(\lambda_2>0\).

On that set write \(\lambda_3=r\lambda_2\) with \(r\geq1\) and
\(\lambda_1=-(1+r)\lambda_2\). Then

\[
 |S|^2=2(1+r+r^2)\lambda_2^2,\qquad
 -4\det S=4r(1+r)\lambda_2^3.                                 \tag{5.1}
\]

Consequently,

\[
 \frac{-4\det S}{\lambda_2|S|^2}
 =\frac{2r(1+r)}{1+r+r^2}
 =2-\frac{2}{1+r+r^2}<2,                                     \tag{5.2}
\]

and the ratio tends to two as \(r\to\infty\). This proves (1.5) and the
sharpness of its constant.

The largest possible middle eigenvalue at fixed Frobenius norm is instead

\[
 \lambda_2^+\leq\frac{|S|}{\sqrt6}.                           \tag{5.3}
\]

Indeed, \(\lambda_1\leq-2\lambda_2\) whenever
\(0<\lambda_2\leq\lambda_3\), so
\(|S|^2\geq6\lambda_2^2\). Equality occurs at

\[
 S_2=s\,\operatorname{diag}
 \left(-\frac2{\sqrt6},\frac1{\sqrt6},\frac1{\sqrt6}\right).
 \tag{5.4}
\]

Section 3 realizes (5.4) on a ball. Thus positive middle strain is not
excluded or made small by local incompressibility.

## 6. Why the energy exponent remains six

Combining (1.5) and (1.6) gives only

\[
 \int\omega\cdot S\omega
 \leq2\int\lambda_2^+|S|^2
 \leq\frac2{\sqrt6}\int|S|^3.                                \tag{6.1}
\]

The three-dimensional Gagliardo--Nirenberg inequality then yields (1.7).
The exponent is also the exact algebraic Young endpoint. For
\(\sigma=\|S\|_2\) and \(D=\|\nabla S\|_2^2\),

\[
 \sup_{D\geq0}
 \left(\sigma^{3/2}D^{3/4}-\varepsilon D\right)
 =\frac{27}{256}\varepsilon^{-3}\sigma^6.                    \tag{6.2}
\]

Thus R0.69O and R0.69P separate the budget cleanly:

\[
 \text{leading pressure remainder}
 \lesssim \mathsf A_v^2\mathsf E_v,
 \qquad
 \text{stretching remainder}
 \lesssim \int\sigma^6\,dt.                                  \tag{6.3}
\]

The first term is quadratic in enstrophy; the second is genuinely sextic.
Replacing \(\omega\cdot S\omega\) by \(\lambda_2^+\) clarifies its sign but
does not change this exponent unless \(\lambda_2^+\) has independent
spacetime control.

## 7. A precise target for the next stage

Two normalized depletion observables isolate the missing information:

\[
 \Theta_{\rm align}
 =\frac{(\omega\cdot S\omega)_+}
 {\sqrt{2/3}|S||\omega|^2},
 \qquad
 \Theta_2=\frac{\sqrt6\,\lambda_2^+}{|S|},                    \tag{7.1}
\]

with value zero when the denominator vanishes. Both lie in \([0,1]\), and
the local constructions above show that energy and incompressibility alone
permit the endpoint value one.

Accordingly, the next useful question is not another pointwise matrix
inequality. It is whether the Navier--Stokes evolution forces a scale-local
spacetime deficit, for example a quantitative estimate of

\[
 \int_{Q_r}\Theta_2|S|^3
 \quad\hbox{or}\quad
 \int_{Q_r}\Theta_{\rm align}|S||\omega|^2,                  \tag{7.2}
\]

that is stronger than the absolute cubic bound and compatible with radius
iteration. Direction-coherence regularity criteria show that such geometric
information can be sufficient when assumed; they do not derive it from the
energy inequality.

R0.69Q will therefore test a scale-local transport identity for the
vorticity direction and the positive middle-eigenvalue set. The acceptance
criterion is strict: the identity must yield either an integrable time power
or a genuine small scale factor without assuming the desired coherence.
Otherwise it will be recorded as a conditional criterion, not as progress
toward unconditional regularity.

## 8. Scope and prior work

The global strain/vorticity relation is classical and goes back to Betchov.
The use of vorticity direction coherence as a conditional regularity
mechanism is classical work of Constantin and Fefferman. Criteria based on
the positive middle eigenvalue of the strain tensor also predate this note.

The project-specific contribution of R0.69P is narrower: an audited, sharp
comparison of these mechanisms at the exact point reached after R0.69O,
together with an explicit compactly supported vector-potential construction
proving that both pointwise endpoints are locally realizable. No claim of
literature priority is made for that construction. This closes the route
"incompressibility alone forces favorable stretching geometry." It does not
close any route that uses dynamics, nonlocality, or additional spacetime
information.

Primary references:

1. R. Betchov, *An inequality concerning the production of vorticity in
   isotropic turbulence*, Journal of Fluid Mechanics 1 (1956), 497--504,
   <https://doi.org/10.1017/S0022112056000317>.
2. P. Constantin and C. Fefferman, *Direction of vorticity and the problem of
   global regularity for the Navier--Stokes equations*, Indiana University
   Mathematics Journal 42 (1993), 775--789,
   <https://doi.org/10.1512/iumj.1993.42.42034>.
3. E. Miller, *A regularity criterion for the Navier--Stokes equation
   involving only the middle eigenvalue of the strain tensor*,
   <https://arxiv.org/abs/1710.05569>.
