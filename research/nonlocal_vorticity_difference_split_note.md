# R0.69R — The nonlocal vorticity difference returns to the classical sextic cost

## 1. Result

R0.69Q rules out absorption by interior vorticity-direction diffusion alone.
The next candidate is stronger: keep magnitude and direction coupled inside
the signed Biot--Savart representation and use the exact difference

\[
 \omega(x)\times\omega(x+z)
 =\omega(x)\times\bigl(\omega(x+z)-\omega(x)\bigr).           \tag{1.1}
\]

This removes one order of the near-field singularity without assuming a
modulus of continuity for the direction. R0.69R computes the complete
near/far estimate and optimizes its splitting radius.

Let

\[
 A=\|\omega\|_{L^2(\mathbb R^3)},\qquad
 B=\|\nabla\omega\|_{L^2(\mathbb R^3)}.                       \tag{1.2}
\]

For every smooth, rapidly decaying divergence-free velocity field and every
\(r>0\), the absolute vortex-stretching production satisfies

\[
 \boxed{
 \int_{\mathbb R^3}|\omega|^2|\xi\cdot S\xi|\,dx
 \le C_{\rm n}rA^{1/2}B^{5/2}
     +C_{\rm f}r^{-3/2}A^3.}                                 \tag{1.3}
\]

The first term is the difference-cancelled near field; the second is the
\(L^2\) far field. Exact optimization gives

\[
 r_*=
 \left(\frac{3C_{\rm f}}{2C_{\rm n}}\right)^{2/5}\frac AB      \tag{1.4}
\]

and

\[
 \boxed{
 \int|\omega|^2|\xi\cdot S\xi|
 \le C_*A^{3/2}B^{3/2}.}                                     \tag{1.5}
\]

Thus the nonlocal difference removes the local kernel singularity, but the
far field restores exactly the classical scale. With \(D=B^2\), Young
optimization returns

\[
 C_*A^{3/2}D^{3/4}
 \le\varepsilon D
 +\frac{27C_*^4}{256\varepsilon^3}A^6.                       \tag{1.6}
\]

The sextic enstrophy-norm remainder is unchanged.

This is not an artifact of a loose choice of \(r\). Any homogeneous monomial
bound using only \(A\) and \(B\),

\[
 |\mathcal V|\le C A^pB^q,                                   \tag{1.7}
\]

must respect amplitude scaling and Navier--Stokes spatial scaling. These force

\[
 p+q=3,\qquad p+3q=6,
\qquad\Longrightarrow\qquad
 \boxed{p=q=\frac32.}                                        \tag{1.8}
\]

Therefore no exponent gain can come from reorganizing the same two norms.
The difference identity remains useful only if it is paired with genuinely
new information: cancellation across scales, a critical Besov/Morrey
quantity, a signed flux, or a dynamical restriction on where magnitude
concentrates.

R0.69R closes this specific norm-only near/far branch. It does not disprove
nonlocal geometric depletion, prove blow-up, prove global regularity, or
solve the Millennium Problem.

## 2. Full-space signed stretching kernel

On \(\{\rho=|\omega|>0\}\), put \(\xi=\omega/\rho\) and
\(\alpha=\xi\cdot S\xi\). The full-space version of the geometric
vortex-stretching representation used in R0.69G is

\[
 \alpha(x)
 =\frac{3}{4\pi}\operatorname{p.v.}\!\int_{\mathbb R^3}
 D\bigl(\widehat z,\xi(x+z),\xi(x)\bigr)
 \frac{\rho(x+z)}{|z|^3}\,dz,                                \tag{2.1}
\]

where

\[
 D(e_1,e_2,e_3)
 =(e_1\cdot e_3)\bigl(e_1\cdot(e_2\times e_3)\bigr),
 \qquad
 |D(e_1,e_2,e_3)|\le|e_2\times e_3|.                         \tag{2.2}
\]

Multiplying by \(\rho(x)^2\) and using

\[
 \rho(x)\rho(x+z)|\xi(x+z)\times\xi(x)|
 =|\omega(x+z)\times\omega(x)|                               \tag{2.3}
\]

gives

\[
 \rho(x)^2\rho(x+z)|\xi(x+z)\times\xi(x)|
 \le\rho(x)^2|\omega(x+z)-\omega(x)|.                        \tag{2.4}
\]

Equation (2.4) is the exact magnitude--direction coupling absent from the
direction-only selector theorem in R0.69G. It converts the near-field
principal value into an absolutely integrable difference expression.

## 3. Near field: one singular order is removed

For \(|z|\le r\), the fundamental theorem of calculus gives

\[
 |\omega(x+z)-\omega(x)|
 \le |z|\int_0^1|\nabla\omega(x+\theta z)|\,d\theta.          \tag{3.1}
\]

If \(M\) is the centered Hardy--Littlewood maximal operator, then for
nonnegative \(f\)

\[
 \int_{|y|\le R}\frac{f(x+y)}{|y|^2}\,dy
 \le 4\pi R\,Mf(x).                                          \tag{3.2}
\]

After the change of variables \(y=\theta z\), the factor
\(\theta^{-1}\) is cancelled by the radius \(\theta r\) in (3.2). Hence

\[
 \int_{|z|\le r}
 \frac{|\omega(x+z)-\omega(x)|}{|z|^3}\,dz
 \le 4\pi r\,M(|\nabla\omega|)(x).                           \tag{3.3}
\]

Using the \(L^2\) boundedness of \(M\), Hölder, and the three-dimensional
Gagliardo--Nirenberg inequality,

\[
 \begin{aligned}
 |\mathcal V_{\rm near}|
 &\le C r\int|\omega|^2M(|\nabla\omega|)\,dx\\
 &\le C r\|\omega\|_4^2\|\nabla\omega\|_2\\
 &\le C r A^{1/2}B^{5/2}.                                   \tag{3.4}
 \end{aligned}
\]

The cancellation is genuine: without the difference, the local kernel has
the borderline radial measure \(ds/s\); after (3.1), it has the integrable
measure \(ds\). But the price is one full derivative inside the maximal
function.

## 4. Far field: energy restores the missing scale

For \(|z|>r\), use only \(|D|\le1\). The truncated kernel satisfies

\[
 \left\|\mathbf1_{\{|z|>r\}}|z|^{-3}\right\|_2^2
 =4\pi\int_r^\infty s^{-4}\,ds
 =\frac{4\pi}{3r^3}.                                        \tag{4.1}
\]

Young's convolution inequality therefore gives

\[
 \left\|
 \int_{|z|>r}\frac{\rho(\,\cdot+z)}{|z|^3}\,dz
 \right\|_\infty
 \le\left(\frac{4\pi}{3}\right)^{1/2}r^{-3/2}A.              \tag{4.2}
\]

Multiplying by \(\rho^2\) and integrating yields

\[
 |\mathcal V_{\rm far}|
 \le C r^{-3/2}A^3.                                          \tag{4.3}
\]

This step uses only finite enstrophy. It is exactly where the scale recovered
by the near-field difference is lost again.

## 5. Exact optimization

For \(X,Y>0\), consider

\[
 F(r)=Xr+Yr^{-3/2}.                                          \tag{5.1}
\]

There is a unique critical point,

\[
 r_*=\left(\frac{3Y}{2X}\right)^{2/5},                       \tag{5.2}
\]

and

\[
 \min_{r>0}F(r)
 =\frac53\left(\frac32\right)^{2/5}X^{3/5}Y^{2/5}.           \tag{5.3}
\]

Taking

\[
 X=C_{\rm n}A^{1/2}B^{5/2},
 \qquad
 Y=C_{\rm f}A^3                                              \tag{5.4}
\]

gives (1.4)--(1.5), because

\[
 X^{3/5}Y^{2/5}
 =C_{\rm n}^{3/5}C_{\rm f}^{2/5}A^{3/2}B^{3/2}.              \tag{5.5}
\]

The optimal split radius is a constant multiple of \(A/B\), the usual
enstrophy length. No independent small parameter remains after optimization.

## 6. Scaling uniqueness of the exponents

First scale the amplitude by \(u\mapsto a u\). Then

\[
 \mathcal V\mapsto a^3\mathcal V,\qquad
 A\mapsto aA,\qquad B\mapsto aB.                             \tag{6.1}
\]

Any bound (1.7) with an amplitude-independent constant requires
\(p+q=3\).

Next use Navier--Stokes spatial scaling at a fixed time,

\[
 u_\lambda(x)=\lambda u(\lambda x),\qquad
 \omega_\lambda(x)=\lambda^2\omega(\lambda x).               \tag{6.2}
\]

Then

\[
 \mathcal V_\lambda=\lambda^3\mathcal V,\qquad
 A_\lambda=\lambda^{1/2}A,\qquad
 B_\lambda=\lambda^{3/2}B.                                  \tag{6.3}
\]

Thus \(p+3q=6\). Solving the two linear constraints gives (1.8). In
particular, no alternative Hölder interpolation using only \(A\) and \(B\)
can change the final exponents while remaining homogeneous.

## 7. Young endpoint and time-integrability boundary

Writing \(D=B^2\), the optimized bound is

\[
 C_*A^{3/2}D^{3/4}.                                         \tag{7.1}
\]

The exact optimizer of

\[
 C_*A^{3/2}D^{3/4}-\varepsilon D                            \tag{7.2}
\]

is

\[
 D_*=\left(\frac{3C_*A^{3/2}}{4\varepsilon}\right)^4,        \tag{7.3}
\]

with maximal remainder (1.6). Therefore the enstrophy inequality still has
the schematic form

\[
 \frac d{dt}A^2+\nu B^2
 \lesssim \nu^{-3}A^6.                                      \tag{7.4}
\]

This gives the usual local differential control, not a uniform global bound
for arbitrary data. The difference route has reorganized the proof but has
not changed its time exponent.

## 8. Decision and next step

R0.69R establishes a precise no-gain result:

\[
 \boxed{
 \text{difference cancellation}+\text{energy far field}
 \Longrightarrow A^{3/2}B^{3/2}
 \Longrightarrow A^6\text{ after Young}.}                   \tag{8.1}
\]

The next search must add a third quantity that is not fixed by \(A\) and
\(B\). R0.69S will test a signed, scale-local flux defect before taking
absolute values. The observable must couple neighboring scales and vanish on
the affine core only through an explicit boundary flux. Acceptance requires
either a scale-summable gain or a time exponent below the sextic endpoint;
otherwise the branch will be closed by the same scaling audit.

## 9. Prior work and claim boundary

The geometric vortex-stretching representation and direction-coherence
mechanism are classical, beginning with Constantin and Fefferman. The
maximal-function and near/far splitting tools are standard harmonic analysis.
R0.69R does not claim those ingredients as new. The project contribution is
the explicit route audit: the magnitude-coupled vorticity difference is
carried through the exact radius optimization and then matched to the unique
homogeneous \(L^2\)--\(\dot H^1\) exponents.

This note proves no regularity criterion stronger than known results, no
singularity result, and no solution of the Millennium Problem.
