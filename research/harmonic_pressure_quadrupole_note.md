# R0.69J — Harmonic pressure tails and the leading quadrupole obstruction

## 1. Result

R0.69I shows that spatial localization transfers the global pressure
orthogonality into boundary commutators of the same scaling degree. R0.69J
separates the pressure into a near-field Newtonian part and a far-field part
that is harmonic on the observation ball.

Let \(q=-\Delta p\), choose a cutoff \(\chi\) that equals one on \(B_R\),
and write schematically

\[
 p=p_{\mathrm{near}}+p_{\mathrm{far}},\qquad
 p_{\mathrm{near}}=(-\Delta)^{-1}(\chi q),\qquad
 p_{\mathrm{far}}=(-\Delta)^{-1}((1-\chi)q).
 \tag{1.1}
\]

Inside the region where \(\chi=1\), \(p_{\mathrm{far}}\) is harmonic. Its
Hessian has the Taylor decomposition

\[
 \boxed{
 \nabla^2p_{\mathrm{far}}(x)=Q_R+
 \bigl(\nabla^2p_{\mathrm{far}}(x)-Q_R\bigr),\qquad
 Q_R:=\nabla^2p_{\mathrm{far}}(0),\quad \operatorname{tr}Q_R=0.}
 \tag{1.2}
\]

For \(|x|\le r\le R/2\), the remainder gains one scale ratio:

\[
 \boxed{
 |\nabla^2p_{\mathrm{far}}(x)-Q_R|
 \le C r\int_{|y|\ge R}\frac{|q(y)|}{|y|^4}\,dy.}
 \tag{1.3}
\]

The leading constant quadrupole \(Q_R\), however, does not vanish when paired
with trace-free strain. For any constant symmetric matrix \(Q\),

\[
 \boxed{
 \int\phi S:Q=-\int (Qu)\cdot\nabla\phi.}
 \tag{1.4}
\]

Thus subtracting the leading harmonic quadratic polynomial creates a decaying
remainder but transfers its coefficient to another boundary flux. The route
decision is:

\[
 \boxed{
 \text{harmonic Taylor subtraction yields an }r/R\text{ remainder, but the}
 \text{ leading trace-free quadrupole remains uncontrolled}.}
 \tag{1.5}
\]

## 2. Near-field and far-field decomposition

In Euclidean local coordinates, the pressure Hessian kernel is

\[
 K_{ij}(z)=\frac{3z_i z_j-|z|^2\delta_{ij}}{4\pi|z|^5}.
 \tag{2.1}
\]

If the far source is supported outside \(B_R\), then for \(|x|\le R/2\)
the segment from \(0\) to \(x\) remains at distance at least \(|y|/2\)
from every source point. Since

\[
 |\nabla K(z)|\le \frac{C}{|z|^4},
 \tag{2.2}
\]

the mean-value theorem proves (1.3). On dyadic shells the corresponding
estimate is

\[
 |H_m(x)-H_m(0)|
 \le C\frac r{R_m}
 \frac{1}{R_m^3}\int_{|y|\sim R_m}|q(y)|\,dy.
 \tag{2.3}
\]

This is a genuine positive result: after the constant Hessian is removed,
each remote shell carries an extra \(r/R_m\).

## 3. Why trace freedom does not remove the constant quadrupole

Both \(S\) and \(Q_R\) have zero trace, but the Frobenius product of two
trace-free symmetric matrices need not vanish. In fact, choosing

\[
 S_0=\operatorname{diag}(1,-1,0),\qquad Q_R=cS_0
 \tag{3.1}
\]

gives \(S_0:Q_R=2c\). Equation (1.4) follows from symmetry of \(Q\),
incompressibility, and one integration by parts:

\[
 \int\phi S:Q=\int\phi\,\partial_j u_i Q_{ij}
 =-\int u_iQ_{ij}\partial_j\phi.
 \tag{3.2}
\]

So the constant harmonic Hessian is not annihilated; it is moved to the
cutoff annulus, exactly as in R0.69I.

## 4. Exact zero-mass, zero-dipole witness

The failure persists even after imposing the first two scalar multipole
constraints. On the sphere of radius \(R\), take the signed source

\[
 q_R=\delta_{Re_1}+\delta_{-Re_1}
     -\delta_{Re_2}-\delta_{-Re_2}.
 \tag{4.1}
\]

It has zero total mass and zero first moment. Its Newtonian potential is
harmonic in \(B_R\), and at the center

\[
 p_{\mathrm{far}}(0)=0,\qquad \nabla p_{\mathrm{far}}(0)=0,
 \tag{4.2}
\]

but

\[
 \boxed{
 Q_R=\nabla^2p_{\mathrm{far}}(0)
 =\frac{3}{2\pi R^3}\operatorname{diag}(1,-1,0).}
 \tag{4.3}
\]

Pairing with \(S_0\) from (3.1) gives

\[
 \boxed{S_0:Q_R=\frac{3}{\pi R^3}\ne0.}
 \tag{4.4}
\]

The witness is a signed scalar pressure source, not yet a construction of
\(q=\operatorname{tr}((\nabla u)^2)\) from a velocity field. Its role is to
prove that mean zero, zero dipole, harmonicity, and trace freedom do not by
themselves eliminate the leading pressure quadrupole.

The point sources may be replaced by symmetric smooth bumps supported near
the four points; the center Hessian converges to (4.3), so the nonzero
obstruction is stable under smooth approximation.

## 5. Scaling and route decision

The quadrupole coefficient in (4.3) decays as \(R^{-3}\), exactly the natural
homogeneity of a pressure Hessian kernel. When the remote source strength is
rescaled with the Navier--Stokes pressure source, this is not an additional
subcritical factor. Only the remainder after subtracting \(Q_R\) gains
\(r/R\).

R0.69J therefore closes the naive harmonic-subtraction route: removing
constant and linear pressure terms does not affect the Hessian, and removing
the quadratic harmonic term leaves its trace-free coefficient as a boundary
flux. The result does not rule out cancellation of these coefficients across
many dyadic shells or additional identities forced by
\(q=\operatorname{tr}((\nabla u)^2)\).

R0.69J gives no Navier--Stokes regularity or singularity conclusion and does
not solve the Millennium Problem.

R0.69K will treat the shellwise quadrupole coefficients as a signed sequence.
It will test whether the velocity-generated form of \(q\), rather than scalar
mean-zero information, forces a telescoping, Carleson, or square-function
bound across scales.
