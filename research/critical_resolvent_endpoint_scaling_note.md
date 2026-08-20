# R0.69F — Fractional-Volterra endpoint scaling and the classical-rate barrier

## 1. Result

R0.69E proves that the critical linearized resolvent is finite on every
compact regular interval.  This note asks whether the quantitative bound can
force a new blow-up rate as the interval approaches a possible first singular
time \(T_*<\infty\).

The answer for the present certificate is negative.  The positive-time
linearization has an exact scalar fractional-Volterra majorant.  On a time
window of length \(h\), with

\[
 V=\sup_I\|v(t)\|_\infty,
\]

its exact local gain is

\[
 \boxed{
 G(x)=E_{1/2}(x)
 =e^{x^2}\operatorname{erfc}(-x),
 \qquad
 x=2C_S\sqrt{\pi h}\,V.}
\tag{1.1}
\]

Here \(E_{1/2}\) is the Mittag--Leffler function.  The exponent
\(x^2=4\pi C_S^2V^2h\) is sharp for this scalar majorant.  Optimizing the
R0.69E Bielecki parameter changes only a polynomial prefactor and cannot
remove that exponent.

To compare with the packet depth, fix

\[
 \beta=256,\qquad
 t_j=T_*-(T_*-\tau)\beta^{-j},\qquad
 h_j=t_j-t_{j-1},
\tag{1.2}
\]

where \(0<\tau<T_*\) is chosen so that

\[
 a:=2C_B\|v\|_{X_\tau}<1.
\tag{1.3}
\]

The value \(\beta=256\) is the inverse time-scale ratio
\(H_{j+1}^2/H_j^2\) of the R0.69A packet.  Put

\[
 V_j:=\sup_{t\in[t_{j-1},t_j]}\|v(t)\|_\infty,
 \qquad
 x_j:=2C_S\sqrt{\pi h_j}\,V_j.
\tag{1.4}
\]

On the positive-time continuous subspace used by the nonlinear perturbation
equation, the critical resolvent obeys

\[
 \boxed{
 \mathfrak M_v^{\,c}(t_r)
 \le
 \Gamma_*
 \left(\frac1{1-a}+2r\right)
 \prod_{j=1}^rG(x_j),}
\tag{1.5}
\]

where the product in (1.5) multiplies the preceding two factors and

\[
 \Gamma_*=
 1+\sqrt{27}
 +\sqrt{\frac{T_*}{\tau}}
 +\frac{\min\{1,\sqrt{T_*}\}}{\sqrt\tau}.
\tag{1.6}
\]

Equivalently,

\[
 \log \mathfrak M_v^{\,c}(t_r)
 \le
 O(\log r)
 +\sum_{j=1}^r
 \left(x_j^2+\frac{2x_j}{\sqrt\pi}\right).
\tag{1.7}
\]

Suppose the R0.69D packet-stability gate fails along these intervals:

\[
 4C_BC_HC_0
 \bigl(\mathfrak M_v^{\,c}(t_r)\bigr)^2\rho^r\ge1,
 \qquad
 C_0=6+4\sqrt2.
\tag{1.8}
\]

Then, with

\[
 c_\rho:=\frac12\log\frac1\rho,
\tag{1.9}
\]

one necessarily has

\[
 \boxed{
 \limsup_{r\to\infty}
 \frac1r\sum_{j=1}^r
 \left(x_j^2+\frac{2x_j}{\sqrt\pi}\right)
 \ge c_\rho,}
\tag{1.10}
\]

and therefore

\[
 \boxed{
 \limsup_{j\to\infty}V_j\sqrt{h_j}
 \ge
 \frac{x_\rho}{2C_S\sqrt\pi},\qquad
 x_\rho=
 -\frac1{\sqrt\pi}
 +\sqrt{\frac1\pi+c_\rho}.}
\tag{1.11}
\]

This is only a type-I scale lower bound on infinitely many time shells.
Standard \(L^\infty\) local continuation already gives a positive lower
bound for \(V_j\sqrt{h_j}\) on every sufficiently late shell if \(T_*\) is a
first singular time.  Thus (1.11) does not improve the classical continuation
rate.  R0.69F closes this endpoint-optimization branch as a rigorous negative
result.

## 2. The continuous positive-time resolvent

For fixed \(\tau>0\), let \(X_T^{c,\tau}\) be the closed subspace of \(X_T\)
whose elements are strongly continuous from \([\tau,T]\) into
\(L^\infty(\mathbb T^3)\).  Give it the same \(X_T\) norm.  The heat orbit
and every Duhamel term appearing in R0.69D belong to this subspace.
The bilinear map \(\mathcal B\) preserves it.

Write

\[
 \mathfrak M_v^{\,c}(T)
 :=
 \left\|
 (I-\mathcal A_v)^{-1}
 \right\|_{X_T^{c,\tau}\to X_T^{c,\tau}}.
\tag{2.1}
\]

R0.69E implies that this inverse exists on each \(T<T_*\).  Restricting
R0.69D to this closed subspace leaves its fixed-point proof unchanged.
In particular, (1.8) is a sufficient stability gate for the actual
positive-time continuous perturbation branch.

The unweighted hybrid norm is

\[
 \|u\|_{\mathfrak X_{\tau,0}}
 =
 \max\left\{
 \|u\|_{X_\tau},
 \sqrt\tau
 \sup_{\tau\le t\le T}\|u(t)\|_\infty
 \right\}.
\tag{2.2}
\]

For every \(T<T_*\),

\[
 \|u\|_{X_T}
 \le\Gamma_*\|u\|_{\mathfrak X_{\tau,0}}.
\tag{2.3}
\]

The constant \(\Gamma_*\) is independent of the number of endpoint shells.

## 3. Exact local fractional-Volterra gain

On one window \(I=[s_0,s_0+h]\), the Oseen-gradient bound gives the scalar
operator

\[
 (K_{V,h}q)(t)
 =
 2C_SV\int_{s_0}^t(t-s)^{-1/2}q(s)\,ds.
\tag{3.1}
\]

For the constant function one, beta-integral convolution gives

\[
 K_{V,h}^{\,n}\mathbf1(t)
 =
 \frac{
 \left(2C_SV\sqrt\pi\right)^n
 (t-s_0)^{n/2}}
 {\Gamma(1+n/2)}.
\tag{3.2}
\]

Consequently

\[
 \sum_{n=0}^\infty
 \|K_{V,h}^{\,n}\|_{L^\infty\to L^\infty}
 =
 E_{1/2}\!\left(2C_SV\sqrt{\pi h}\right).
\tag{3.3}
\]

The closed identity

\[
 E_{1/2}(x)=e^{x^2}\operatorname{erfc}(-x)
\tag{3.4}
\]

then proves (1.1).  Since

\[
 \operatorname{erfc}(-x)=1+\operatorname{erf}(x),
 \qquad
 0\le\operatorname{erf}(x)\le\frac{2x}{\sqrt\pi},
\tag{3.5}
\]

one has the useful logarithmic bound

\[
 \boxed{
 \log G(x)
 \le x^2+\frac{2x}{\sqrt\pi},
 \qquad x\ge0.}
\tag{3.6}
\]

No factor larger than one is inserted when \(x=0\).

## 4. Shell gluing without an endpoint-trace loss

Let

\[
 z=f+\mathcal A_vz,
\qquad
 f\in X_{t_r}^{c,\tau},
\tag{4.1}
\]

and normalize

\[
 F:=
 \max\left\{
 \|f\|_{X_\tau},
 \sqrt\tau\sup_{\tau\le t\le t_r}\|f(t)\|_\infty
 \right\}.
\tag{4.2}
\]

The initial block gives

\[
 Z_0:=\sqrt\tau\|z(\tau)\|_\infty
 \le\frac{F}{1-a}.
\tag{4.3}
\]

For \(j\ge1\), set

\[
 Z_j:=\sqrt\tau
 \sup_{t\in[t_{j-1},t_j]}\|z(t)\|_\infty.
\tag{4.4}
\]

The exact restart identity from R0.69E reads

\[
 \begin{aligned}
 z(t)=&\ e^{(t-t_{j-1})\Delta}z(t_{j-1})
 +f(t)-e^{(t-t_{j-1})\Delta}f(t_{j-1})\\
 &-\int_{t_{j-1}}^t
 e^{(t-s)\Delta}\mathbb P\nabla\!\cdot
 (v\otimes z+z\otimes v)(s)\,ds.
 \end{aligned}
\tag{4.5}
\]

Heat contraction, (3.3), and (4.2) therefore give

\[
 \boxed{
 Z_j\le G(x_j)(Z_{j-1}+2F).}
\tag{4.6}
\]

Because \(G(x_j)\ge1\), induction yields

\[
 \frac{Z_j}{F}
 \le
 \left(\frac1{1-a}+2j\right)
 \prod_{i=1}^jG(x_i).
\tag{4.7}
\]

Combining (4.7) with (2.3) proves (1.5).

## 5. Consequence of failure of the nonlinear packet gate

If (1.8) holds, then

\[
 \log\mathfrak M_v^{\,c}(t_r)
 \ge
 \frac r2\log\frac1\rho
 -\frac12\log(4C_BC_HC_0).
\tag{5.1}
\]

Equations (1.5) and (3.6) give

\[
 \sum_{j=1}^r
 \left(x_j^2+\frac{2x_j}{\sqrt\pi}\right)
 \ge
 c_\rho r-O(\log r).
\tag{5.2}
\]

This proves (1.10).  The function

\[
 \phi(x)=x^2+\frac{2x}{\sqrt\pi}
\tag{5.3}
\]

is strictly increasing on \([0,\infty)\).  Therefore

\[
 \limsup_{j\to\infty}x_j
 \ge\phi^{-1}(c_\rho)=x_\rho,
\tag{5.4}
\]

which is (1.11).

The statement is deliberately a limsup.  A linearly growing sum can be
carried by a positive density of time shells; the argument does not force a
larger lower bound on every individual shell.

## 6. Exact optimization of the Bielecki parameter

R0.69E uses

\[
 b_\lambda=2C_SV\sqrt{\frac\pi\lambda}<1.
\tag{6.1}
\]

On a late interval of length \(L\), put

\[
 A:=4\pi C_S^2V^2L,
 \qquad
 \theta:=b_\lambda\in(0,1).
\tag{6.2}
\]

The exponential part of the R0.69E certificate becomes

\[
 F_A(\theta)
 :=
 \frac{\exp(A/\theta^2)}{1-\theta}.
\tag{6.3}
\]

Its unique minimizer \(\theta_A\in(0,1)\) is determined by

\[
 \boxed{
 \theta_A^3=2A(1-\theta_A).}
\tag{6.4}
\]

As \(A\to\infty\),

\[
 1-\theta_A=\frac1{2A}+O(A^{-2}),
\qquad
 \min_{0<\theta<1}F_A(\theta)
 =
 2eA\,e^A\left(1+O(A^{-1})\right).
\tag{6.5}
\]

By contrast, the exact scalar gain satisfies

\[
 G(\sqrt A)
 =
 e^A\operatorname{erfc}(-\sqrt A)
 =
 2e^A(1+o(1)).
\tag{6.6}
\]

Thus Bielecki optimization removes no exponential.  It loses only the
polynomial factor \(eA\) relative to the exact scalar majorant.  Refining the
finite partition recovers (6.6), not a subexponential bound.

## 7. Comparison with the classical continuation rate

The same Oseen-gradient estimate gives local mild well-posedness from an
\(L^\infty\) state at time \(t_0>0\), with a lifespan bounded below by

\[
 \Delta t\ge
 \frac{c_\infty}{\|v(t_0)\|_\infty^2}
\tag{7.1}
\]

for a positive constant \(c_\infty\) depending only on the periodic kernel
normalization.  If \(T_*\) is the first singular time, continuation past
\(T_*\) must fail, and therefore

\[
 \boxed{
 \|v(t)\|_\infty\sqrt{T_*-t}
 \ge\sqrt{c_\infty}}
\tag{7.2}
\]

for every sufficiently late regular time \(t<T_*\).

For the geometric windows in (1.2),

\[
 T_*-t_{j-1}
 =\frac{\beta}{\beta-1}h_j.
\tag{7.3}
\]

Taking \(t=t_{j-1}\) in (7.2) gives

\[
 V_j\sqrt{h_j}
 \ge
 \sqrt{c_\infty\frac{\beta-1}{\beta}}
\tag{7.4}
\]

on every late shell.  Equation (7.4) is stronger in form than the limsup
condition (1.11).  The endpoint \(L_t^2L_x^\infty\) Serrin criterion also
already requires

\[
 \int_0^{T_*}\|v(t)\|_\infty^2\,dt=\infty
\tag{7.5}
\]

at a first singular time.

The new calculation remains useful because it identifies the exact
fractional-Volterra conditioning hidden in R0.69E and proves that parameter
optimization cannot change its scale.  It does not create a criterion beyond
classical continuation theory.

## 8. Decision and next branch

R0.69F decides the announced endpoint-optimization test.

1. The exact positive-time majorant is \(E_{1/2}\), not an artifact of an
   arbitrary Bielecki weight.
2. Its unavoidable exponent is the scale-invariant quantity
   \(V_j^2h_j\).
3. Failure of the R0.69D packet gate forces at most a type-I shell lower
   bound.
4. Classical \(L^\infty\) continuation already supplies a stronger
   every-shell statement.

The reference-resolvent branch is therefore stopped here.  The next useful
problem must use information not collapsed into
\(\sup_I\|v\|_\infty\): for example, a localized geometric quantity,
vorticity direction, pressure depletion, or a genuinely signed
frequency-space interaction.  Merely optimizing \(\tau\), \(\lambda\), or
the time partition cannot resolve the Millennium problem.

This note proves neither global regularity nor finite-time singularity.  It
does not solve the three-dimensional Navier--Stokes Millennium problem.

## References

1. H. Koch and D. Tataru, *Well-posedness for the Navier--Stokes equations*,
   Advances in Mathematics 157 (2001), 22--35,
   <https://math.berkeley.edu/~tataru/papers/nas.pdf>.
2. P. G. Lemarié-Rieusset, *The Navier--Stokes equations in the critical
   Morrey--Campanato space*, Revista Matemática Iberoamericana 23 (2007),
   897--930,
   <https://projecteuclid.org/journals/revista-matematica-iberoamericana/volume-23/issue-3/The-Navier-Stokes-equations-in-the-critical-Morrey-Campanato-space/rmi/1204128305.full>.
3. H. Hou, *On regularity of solutions to the Navier--Stokes equation with
   initial data in \(BMO^{-1}\)*, SIAM Journal on Mathematical Analysis,
   <https://doi.org/10.1137/24M1719487>.
