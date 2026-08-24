# R0.70V exact certificate

This directory locks the finite exact payload for the R0.70V
response-distance and strain-projection gate.

On the normalized torus, the release uses the complete scalar frame

\[
 \mathscr T=\{T_\star=\Pi_0\}\cup\{T_j:j\in\mathbb Z\},
 \qquad
 \sum_\alpha T_\alpha^2=I,
\]

and the covariance defect

\[
 \mathcal D_\times
 =\omega\otimes\omega
  -\sum_\alpha T_\alpha\omega\otimes T_\alpha\omega.
\]

The exact Fourier kernel is

\[
 K(p,q)
 =1-\langle V(p),V(q)\rangle
 =\frac12\|V(p)-V(q)\|_{\ell^2}^2.
\]

The release proves that the full tensor cannot be controlled by any positive
power of the covariance residual \(r\), even at exact rank one.  It then
isolates the smaller strain-compatible quantity

\[
 \mathfrak X_\times
 =\sum_{n\ne0}|n|^{-2}
  |\nu_n\times\widehat{\mathcal D_\times}(n)\nu_n|^2,
 \qquad \nu_n=n/|n|,
\]

for which

\[
 |\mathfrak E_S|
 \le\|\nabla\omega\|_2\mathfrak X_\times^{1/2}
 \le\frac\nu2\|\nabla\omega\|_2^2
  +\frac1{2\nu}\mathfrak X_\times.
\]

This is an exact viscosity ledger.  The certificate does not infer an a
priori bound for \(\mathfrak X_\times\), an enstrophy closure, or any
Navier--Stokes regularity conclusion.

## Direct machine checks

The producer performs six groups of exact checks.

### 1. Gram chord and response area

For finite response vectors \(x,y\), it verifies the unconstrained identity

\[
 1-x\cdot y-\frac12|x-y|^2
 =\frac12[(1-|x|^2)+(1-|y|^2)].
\]

Thus unit responses satisfy

\[
 K=1-\gamma=\frac12|x-y|^2.
\]

It also expands every two-coordinate minor and verifies the Lagrange identity

\[
 \sum_{i<j}|x_i y_j-x_j y_i|^2
 =|x|^2|y|^2-(x\cdot y)^2.
\]

On the unit sphere this gives the response-area coefficient

\[
 \kappa=1-\gamma^2=(1-\gamma)(1+\gamma).
\]

The quotient

\[
 \frac{1-\gamma}{\sqrt{1-\gamma^2}}
 =\sqrt{\frac{1-\gamma}{1+\gamma}}
\]

is asserted only for \(-1<\gamma<1\).  At \(\gamma=1\), it is the undefined
ratio \(0/0\), although the pair defect itself vanishes.  At \(\gamma=-1\),
the response chord equals two while the area vanishes.  The producer locks
both endpoint branches explicitly.

The finite three-coordinate calculation certifies the algebraic identity;
the passage to the actual \(\ell^2\) response vectors is analytic.

### 2. Two-shell exact-rank counterexample

The field is

\[
 \omega=e_3[A\cos(Nx_1)+B\cos(4Nx_1)].
\]

The producer checks the product-to-sum identity giving

\[
 \mathcal D_\times
 =AB[\cos(3Nx_1)+\cos(5Nx_1)]e_3\otimes e_3.
\]

It computes the normalized homogeneous periodic norm directly from the four
nonzero Fourier coefficients:

\[
 \|\mathcal D_\times\|_{\dot H^{-1}_\#,F}^2
 =\frac{17A^2B^2}{225N^2}.
\]

It also checks that

\[
 \nu_n\times\widehat{\mathcal D_\times}(n)\nu_n=0
\]

at all four output frequencies and that an \(e_2\)-directed shear strain has
zero Frobenius contraction with the \(33\)-polarized defect.

The strict-annulus response separation and the global top gap are analytic
arguments in the report.  In particular,
\(\cos(Nx_1)=0\Rightarrow\cos(4Nx_1)=1\), so the two covariance amplitudes
never vanish together.

### 3. Strain-projection constants

For a generic real symmetric matrix

\[
 D=\begin{pmatrix}
 d_{11}&d_{12}&d_{13}\\
 d_{12}&d_{22}&d_{23}\\
 d_{13}&d_{23}&d_{33}
 \end{pmatrix},
\]

the producer verifies

\[
 |D|_F^2-2|e_1\times De_1|^2
 =d_{11}^2+d_{22}^2+d_{33}^2+2d_{23}^2.
\]

This locks the constant

\[
 |\nu\times D\nu|^2\le\frac12|D|_F^2.
\]

It then checks the simultaneous equality anchor

\[
 \omega=e_2\cos x_1,
 \qquad
 D=-\cos x_1(e_1\otimes e_3+e_3\otimes e_1),
\]

for which

\[
 \left|\int S:D\right|=\frac12,
 \quad
 \|\nabla\omega\|_2^2=\frac12,
 \quad
 \mathfrak X[D]=\frac12,
 \quad
 \|D\|_{\dot H^{-1}_\#,F}^2=1.
\]

This sharpness statement concerns the ambient symmetric-tensor class.  The
producer does not assert equality inside the constrained subclass
\(D=\mathcal D_\times(\omega)\) for the same vorticity.

### 4. R0.70U critical subtotal

For the Pythagorean parameters

\[
 a=m^2-1,
 \qquad b=2m,
 \qquad K=m^2+1,
\]

the producer constructs the \(+k\) Fourier coefficient of
\(w\otimes h+h\otimes w\).  The two outputs \(\pm k\) contribute exactly

\[
 \frac{\delta^2m^2}{2(m^2+1)^4}
\]

to the unweighted coefficient \(X_0\).  All other output contributions are
nonnegative, so this gives a strict lower bound.

It separately verifies the abstract tensor identity

\[
 (w+\varepsilon h)^{\otimes2}-Q_\varepsilon
 =\varepsilon(1-\gamma)(w\otimes h+h\otimes w).
\]

Thus the certificate locks the order

\[
 \mathfrak X_{\times,\varepsilon}=\Theta(\varepsilon^2)
\]

after the fixed finite family and \(|\gamma|\le3/4\) are supplied by R0.70U.
The premises \(m\ge2\), \(A>\delta>0\), and the residual and signed-work
orders are inherited from the locked R0.70U theorem.  The R0.70V producer
checks the exact defect and a strictly positive projected subtotal; it does
not recompute every output contribution or relabel inherited results as new
machine calculations.

### 5. Divergence-free triad area

The producer parametrizes

\[
 n+k+l=0,
 \qquad
 a=k\times a_0,
 \qquad
 b=l\times b_0,
 \qquad
 c\perp n,
\]

with \(n\) rotated to the first axis.  It derives exactly

\[
 S_c:(a\otimes b+b\otimes a)
 =\frac{[(l-k)\times(\nu_n\times c)]\cdot(a\times b)}{|n|}.
\]

The radial response estimates

\[
 K(k,l)\frac{|k|+|l|}{|k+l|}\le2+2M_\varphi
\]

and the anti-correlation-guarded version are scalar analytic inequalities in
the report.  The producer records their constants but does not infer the
missing vector-valued shell summation.

### 6. Narrow-band expansion

For two abstract frame channels, the producer expands

\[
 T_\alpha\omega=c_\alpha\omega+e_\alpha
\]

and verifies, modulo \(\sum c_\alpha^2=1\),

\[
 \mathcal D_\times
 =-\omega\otimes g-g\otimes\omega
  -\sum_\alpha e_\alpha\otimes e_\alpha,
 \qquad
 g=\sum_\alpha c_\alpha e_\alpha.
\]

It also checks the unit-response identity

\[
 \langle c,V-c\rangle=-\frac12\|V-c\|^2.
\]

The resulting \(L^1\) theorem

\[
 \|\mathcal D_\times\|_{L^1(F)}
 \le\min\{2,2M_\varphi^2\delta^2\}\|\omega\|_2^2
\]

uses Plancherel and Cauchy--Schwarz analytically; it is not inferred from a
finite numerical sample.  In the actual mean-zero narrow-band application,
the constant frame coordinate satisfies \(c_\star=e_\star=0\).

## Reproduction

From the repository root, run the exact command in `command.txt`.  It writes
canonical, sorted, indented JSON to `result.json`.  The focused Node test
runs the same producer without `--output` and requires raw byte equality with
the archived JSON.

The archived interpreter is a local convenience and is ignored by Git.  A
clean checkout must recreate an equivalent Python 3.12 environment with
SymPy 1.14, then run the same producer.  The exact symbolic JSON and the
SHA-256 manifest are the reproducibility targets.

## Claim boundary

This certificate verifies exact finite algebra.  It does not:

- replace the constant frame block by zero when the frame acts on a product;
- turn scalar kernel positivity into pointwise tensor positivity;
- prove that the full tensor is controlled by covariance rank or residual;
- prove \(\mathfrak X_\times\lesssim r\) or time integrability of
  \(\mathfrak X_\times\);
- sum the pairwise Fourier area over all modes and shells;
- overcome the two-frequency-degree scaling mismatch of the raw
  \(\mathfrak X_\times\)-to-covariance-area comparison without an explicit
  inverse-frequency weight;
- control the principal covariance stretching term \(\int S:Q\);
- propagate a narrow band, a simple top gap, or near rank one;
- prove an enstrophy closure, singularity, global regularity, or a solution
  of the Millennium problem.

The exact-rank shear is a counterexample only to full-tensor residual
control.  Its strain projection and signed stretching defect vanish.  The
R0.70U family instead shows that the projected quantity and the residual
square root have the same critical order; it proves neither an upper bound
between them nor a PDE closure.
