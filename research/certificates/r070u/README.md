# R0.70U exact certificate

This directory locks the finite exact payload for the R0.70U fixed-frame
square-root obstruction.

On the normalized torus, the report uses the pinned complete scalar frame

\[
 \mathscr T=\{T_\star=\Pi_0\}\cup\{T_j:j\in\mathbb Z\},
 \qquad
 \sum_j|\varphi(2^{-j}\xi)|^2=1.
\]

For

\[
 Q=\sum_\alpha T_\alpha\omega\otimes T_\alpha\omega
 =\lambda L+H,
 \qquad r=\operatorname{tr}H,
\]

the signed remainder is

\[
 \mathfrak R_{\rm sgn}
 =-\int u_*\cdot\mathcal A_L
  +\int S:H+\mathfrak E_S.
\]

The release constructs a fixed three-frequency family satisfying

\[
 \|r_\varepsilon\|_{L^p}=\Theta(\varepsilon^2),
 \qquad
 \mathfrak R_{\rm sgn}(\omega_\varepsilon)
 =c_0\varepsilon+O(\varepsilon^2),
 \qquad c_0\ne0.
\]

It follows analytically that a locally bounded residual-only right side of
order \(r^\theta\) cannot control the remainder when \(\theta>1/2\).

## Direct machine checks

The producer performs four groups of exact checks.

### 1. Pythagorean triad and Biot--Savart signs

For an integer \(m\ge2\), retained symbolically by the producer, it sets

\[
 a=m^2-1,
 \qquad b=2m,
 \qquad K=m^2+1,
\]

\[
 k=(a,b,0),
 \qquad p=(a,-b,0),
 \qquad q=(2a,0,0),
 \qquad n=K^{-1}(-b,a,0).
\]

It derives

\[
 a^2+b^2=K^2,
 \qquad q=k+p,
 \qquad |n|=1,
 \qquad k\cdot n=0.
\]

The real Fourier fields are assembled from their exact complex coefficients:

\[
 w=A(n\cos k\cdot x+e_3\sin k\cdot x)
   +\delta e_3\cos p\cdot x,
\]

\[
 h=e_2\cos q\cdot x.
\]

The producer checks every Fourier divergence coefficient and verifies the
complete curl recovery from

\[
 u_w=-\frac A K(n\cos k\cdot x+e_3\sin k\cdot x)
     +\frac{\delta}{K^2}(b,a,0)\sin p\cdot x,
\]

\[
 u_h=-\frac1{2a}e_3\sin q\cdot x.
\]

The sign convention is locked by the nonzero identity

\[
 \nabla\times w_1=-Kw_1.
\]

### 2. Normalized resonant coefficient

The producer forms the strain coefficient of every velocity Fourier mode and
sums exactly the triples whose frequencies add to zero.  It derives rather
than inserts

\[
 I=\int h\cdot S_ww
 =-\frac{A\delta a^2b}{2K^3},
\]

and the independent auxiliary coefficient

\[
 J=\int w\cdot S_hw
 =\frac{A\delta b}{4K}.
\]

It then checks

\[
 \mathscr P'(0)=2I+J,
 \qquad
 \left(\int S:Q\right)'_{0}=2\gamma I+J,
\]

so

\[
 \mathfrak E_S'(0)
 =2(1-\gamma)I
 =-\frac{(1-\gamma)A\delta a^2b}{K^3}.
\]

The producer also forms the complete polynomials in \(\varepsilon\), rather
than only differentiating target formulas.  It verifies that the physical
stretching, frame covariance contraction, and their difference are exactly
linear: all quadratic and cubic coefficients vanish by Fourier
orthogonality.  The algebraic anchor

\[
 m=3,\quad (a,b,K)=(8,6,10),\quad A=2,\quad\delta=1
\]

gives

\[
 I=-\frac{48}{125},\qquad
 J=\frac3{10},\qquad
 \mathscr P'(0)=-\frac{117}{250},
\]

\[
 \mathfrak E_S'(0)=-\frac{96}{125}(1-\gamma).
\]

This numerical anchor checks algebraic signs and coefficients only; it does
not certify that \(m=3\) satisfies the actual unspecified cutoff response.
The calculation uses normalized Haar Fourier orthogonality.  It does not
infer any time persistence of the three-mode form.

### 3. Covariance and rank-two spectrum

For abstract real vectors \(w,h\), the producer checks entry by entry that

\[
 Q_\varepsilon
 =w\otimes w
  +\varepsilon\gamma(w\otimes h+h\otimes w)
  +\varepsilon^2h\otimes h
\]

has the exact factorization

\[
 Q_\varepsilon
 =(w+\varepsilon\gamma h)\otimes(w+\varepsilon\gamma h)
  +(1-\gamma^2)\varepsilon^2h\otimes h.
\]

It also checks the exact physical covariance defect

\[
 \omega_\varepsilon\otimes\omega_\varepsilon-Q_\varepsilon
 =\varepsilon(1-\gamma)(w\otimes h+h\otimes w),
\]

zero determinant, and the two nonzero spectral invariants

\[
 \operatorname{tr}Q
 =W^2+2\varepsilon\gamma C+\varepsilon^2H^2,
\]

\[
 \lambda_1\lambda_2
 =(1-\gamma^2)\varepsilon^2(W^2H^2-C^2).
\]

Here \(W^2=|w|^2\), \(H^2=|h|^2\), and \(C=w\cdot h\).  Expanding the
smaller root gives

\[
 \lim_{\varepsilon\to0}
 \frac{\lambda_2}{\varepsilon^2}
 =(1-\gamma^2)
 \left(H^2-\frac{C^2}{W^2}\right).
\]

At \(x=0\), the producer obtains the nonzero transverse coefficient

\[
 |w\times h|^2
 =\delta^2+\frac{A^2b^2}{K^2}>0.
\]

It additionally checks the two-entry sum-of-squares identity underlying the
ideal shifted-response bound \(|xy|\le1/2\) when \(x^2+y^2=1\).

### 4. Critical exponent arithmetic

If the signed remainder has order \(|\varepsilon|\) and the residual norm has
order \(|\varepsilon|^2\), their ratio at residual exponent \(\theta\) has
power

\[
 1-2\theta.
\]

The producer checks the linear exponent \(-1\), the sample exponent
\(\theta=3/4\) giving \(-1/2\), and the critical exponent \(1/2\) giving
zero.  The quantified statement for every \(\theta>1/2\), and the general
modulus \(o(\sqrt{s})\), are analytic consequences in the report.

## Analytic dependencies

The machine payload does not prove:

- the countable pinned-frame convergence or multiplier lifting;
- the response-vector derivative estimate for an arbitrary cutoff;
- the resulting analytic existence of \(m_0(\varphi)\); a numerical \(m\)
  remains unavailable without an explicit formula for \(\varphi\);
- the uniform global spectral-gap estimate;
- smooth eigenprojector stability and
  \(\mathcal A_L(Q_\varepsilon)=O(\varepsilon^2)\);
- the uniform residual expansion in physical space or its
  \(L^p\)-norm consequence;
- the locally bounded-prefactor quantifiers;
- local or global Navier--Stokes evolution.

The countable complete-frame convention and multiplier lifting in the first
item are inherited from R0.70P/R0.70T.  Sections 4--7 of the R0.70U report
prove items 2--7 at the smooth instantaneous level, while preserving the
non-numerical cutoff boundary.  Standard local strong existence only explains
why the smooth vorticity is admissible initial data; no finite-mode trajectory
or global evolution is claimed.

## Exact-rank sign boundary

The cutoff is real and even but is not assumed nonnegative.  Therefore
\(1-\gamma^2=0\) allows \(\gamma=1\) or \(\gamma=-1\).  The second case need
not cancel the physical/frame covariance defect.  Neither the report nor the
certificate infers a universal commutator cancellation from exact rank
alone.  The obstruction family instead fixes \(|\gamma|\le3/4\).

## Claim boundary

This certificate and the analytic lemmas in the report prove a fixed-frame,
fixed-frequency, instantaneous obstruction to locally bounded residual-only
control with exponent \(\theta>1/2\).  They do not prove failure at the
critical exponent, a positive square-root estimate, a time-integrated
obstruction, a PDE closure, a finite-time singularity, unconditional global
regularity, or a solution of the Millennium problem.

## Reproduction

Run the exact command in `command.txt`.  It writes `result.json`; the focused
Node test also regenerates that result into a temporary file and requires
byte equality.  `SHA256SUMS` locks the producer and all certificate payloads.

The interpreter under `tmp/r068b-venv` is intentionally ignored by Git.  On a
clean checkout, recreate an equivalent Python 3.12.13 environment with
`sympy==1.14.0`, then either place it at that path or replace only the
interpreter path in `command.txt`.  The archived JSON and raw-byte focused
check are the reproducibility targets; the local virtual environment is not
part of the certificate.
