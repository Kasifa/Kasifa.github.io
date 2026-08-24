# R0.70W exact certificate

This directory locks the finite exact payload for the R0.70W far-shell
rank-one projected-summation obstruction.

The release studies

\[
 \mathcal D_\times
 =\omega\otimes\omega
  -\sum_\alpha T_\alpha\omega\otimes T_\alpha\omega
\]

and its strain-compatible Hilbert majorant

\[
 \mathfrak X_\times
 =\sum_{n\ne0}|n|^{-2}
 |\nu_n\times\widehat{\mathcal D_\times}(n)\nu_n|^2.
\]

The exact field is

\[
 w=e_1\cos x_2-e_2\cos x_1,
 \qquad
 h=\cos(4x_3)w,
 \qquad
 \omega_\varepsilon=w+\varepsilon h.
\]

The two radial supports are \(1\) and \(\sqrt{17}>4\). Strict annular
support makes their complete-frame response vectors orthogonal. Every frame
block is pointwise parallel to \(w\), so

\[
 Q=(1+\varepsilon^2\cos^2(4x_3))w\otimes w,
\]

\[
 \Omega_\alpha\times\Omega_\beta=0,
 \qquad
 \lambda_2+\lambda_3=0.
\]

Nevertheless,

\[
 \mathcal D_\times
 =2\varepsilon\cos(4x_3)w\otimes w,
\]

and the complete projected Fourier sum is

\[
 \mathfrak X_\times=\frac{2\varepsilon^2}{729}>0.
\]

The certificate therefore rules out control of \(\mathfrak X_\times\) by
any definite norm of the physical covariance-area fields, including norms
with inverse-frequency weights applied after those fields have been formed.

The actual signed work is zero in the sample because the vorticity/strain
support and defect support are disjoint. The certificate does not rule out
a direct signed trilinear area estimate.

## Direct machine checks

The producer performs seven groups of exact checks.

### 1. Projected-wedge identity

For \(n=p+q\), \(p\cdot a=0\), and \(q\cdot b=0\), it verifies

\[
 \nu_n\times[(a\otimes b+b\otimes a)\nu_n]
 =-|n|^{-1}\nu_n\times[(q-p)\times(a\times b)].
\]

This is the algebraic source of the pair-dependent multiplier that prevents
physical cross products from being substituted after convolution.

The same symbolic block verifies the antisymmetric-current representation.
For

\[
 \mathcal C_m
 =2[\omega\times\partial_m\omega
  -\sum_\alpha\Omega_\alpha\times\partial_m\Omega_\alpha],
\]

it locks

\[
 \widehat{\mathcal C}(n)
 =i\sum_{p+q=n}K(p,q)(q-p)\otimes
  (\widehat\omega(p)\times\widehat\omega(q))
\]

and

\[
 \nu_n\times\widehat{\mathcal D_\times}(n)\nu_n
 =\frac{i}{2|n|}
  [\widehat{\mathcal C}(n)
   -\widehat{\mathcal C}(n)^{\mathsf T}]\nu_n.
\]

### 2. Field geometry

The producer differentiates the finite trigonometric fields and verifies

\[
 \operatorname{div}w=\operatorname{div}h=0.
\]

It locks the squared radii \(1\) and \(17\), and the strict factor-four
squared slack \(17-16=1\).

### 3. Rank-one covariance

Using two orthogonal response coordinates for the disjoint radial supports,
the producer checks

\[
 Q=(1+\varepsilon^2g^2)w\otimes w.
\]

Every \(2\times2\) minor vanishes, and the physical cross product of the two
response blocks is zero.

### 4. Complete projected defect

The producer enumerates all eighteen nonzero defect modes. Ten diagonal
modes have zero strain projection. At each of the eight modes

\[
 n=(\pm1,\pm1,\pm4)
\]

it checks

\[
 |n|^2=18,
\quad
 \widehat{\mathcal D_\times}(n)
 =-\frac\varepsilon4(e_1\otimes e_2+e_2\otimes e_1),
\]

\[
 |\nu_n\times\widehat{\mathcal D_\times}(n)\nu_n|^2
 =\frac{\varepsilon^2}{162},
\quad
 |n|^{-2}|\cdots|^2=\frac{\varepsilon^2}{2916}.
\]

Summing the eight terms gives \(2\varepsilon^2/729\).

### 5. Cancellation lost under projection

At \(n=(1,1,4)\), the two low--high polarization cross products are

\[
 -e_3/8,\qquad +e_3/8.
\]

They cancel in the physical covariance-area field. Their symmetric tensor
products instead add to

\[
 -\frac\varepsilon4(e_1\otimes e_2+e_2\otimes e_1).
\]

Thus a fixed multiplicity of two already defeats the proposed summation.

### 6. Signed-work boundary

The producer enumerates twelve vorticity modes and eighteen defect modes and
checks that their supports are disjoint. Since Biot--Savart strain preserves
Fourier support,

\[
 \int S(\omega_\varepsilon):\mathcal D_\times\,dx=0.
\]

### 7. Resonant negative control

For integer \(M\ge4\), the producer first verifies the generalized exact-rank
formula

\[
 \mathfrak X_{\times,\varepsilon,M}
 =\frac{\varepsilon^2M^2}{(M^2+2)^3}.
\]

It then adds

\[
 z_{\eta,M}
 =\eta(1,-1,0)\cos(x_1+x_2+Mx_3).
\]

The full signed calculation gives

\[
 \mathfrak E_S
 =-\frac{\varepsilon\eta M}
 {2(M^2+1)(M^2+2)}.
\]

For

\[
 \mathcal A_{-1}
 =\sum_{\alpha<\beta}
 \|\Omega_\alpha\times\Omega_\beta\|_{\dot H^{-1}_\#}^2,
\]

the exact spatial factors are

\[
 A_{13}
 =\frac{M^2+3}{2(M^2+1)(M^2+5)}
\]

and

\[
 A_{23}
 =\frac{(2M^2+3)(12M^2+5)}
 {20(4M^2+1)(4M^2+5)}.
\]

The result is

\[
 \mathcal A_{-1}
 =\eta^2[A_{13}
  +\varepsilon^2(1-\gamma_{23}^2)A_{23}].
\]

The producer also checks the complete response-wedge assembly: the
low/resonant wedge has squared norm one, the high/resonant wedge has
squared norm \(1-\gamma_{23}^2\), their mixed response inner product is
zero, their physical \(\dot H^{-1}\) inner product is zero, and the full
formula above has zero symbolic residual.

The signed work is order \(\varepsilon\eta M^{-3}\), while
\(A_{13}^{1/2}\) is order \(M^{-1}\). This finite perturbation is a negative
control: it does not disprove the direct signed-area route.

## Analytic all-mode consequence

The report additionally proves, analytically,

\[
 \mathfrak X_\times
 \le C_0^2\mathcal U_{-2},
 \qquad
 C_0=\max\{12,3M_\varphi^2\},
\]

where

\[
 \mathcal U_{-2}
 =\frac14\sum_{n\ne0}
 \left[
  \sum_{p+q=n}
  \frac{|\widehat\omega(p)\times\widehat\omega(q)|}
       {\max(|p|,|q|)}
 \right]^2.
\]

Convolution, Parseval, and the torus Sobolev embedding give

\[
 \mathfrak X_\times
 \le\frac{C_0^2C_{S,4}^4}{4}
  \|\omega\|_{\dot H^{1/4}_\#}^4.
\]

The producer locks only the scaling and interpolation exponent arithmetic
for this result. The near/far inequalities and Sobolev embedding are
analytic dependencies. After interpolation and Young's inequality, this
returns the classical cubic-enstrophy term
\(C_\varphi\nu^{-3}\|\omega\|_2^6\), not a large-data closure.

## Analytic boundary

The producer does not infer:

- the infinite-frame reconstruction from a finite response vector;
- a bilinear, trilinear, Coifman--Meyer, or paraproduct theorem;
- a uniform positive top covariance gap;
- a direct signed covariance-area estimate;
- a time-integrated commutator bound;
- control of the principal covariance stretching term;
- an enstrophy closure, continuation theorem, singularity, global
  regularity, or a solution of the Millennium problem.

The strict annular response separation, the infinite Parseval sums, and the
fact that Biot--Savart strain preserves support are analytic arguments in
the report. The machine certificate locks the finite algebra and Fourier
arithmetic only.
