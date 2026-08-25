# R0.71A independent mathematical audit

**Date:** 2026-08-25

**Scope:** independent checking of the constant-projector Fourier family,
the critical mixed-norm exponent calculation, the compact nonzero seed, the
fixed-torus scaling sequence, the weighted continuation corollary, and the
claim boundary.

No audit below treats a kinematic test field as a Navier--Stokes solution.

## 1. Audit verdict

The following claims pass:

1. the ten-mode sign pair has identical pointwise frame covariance;
2. its principal projector is exactly the constant matrix
   \(e_3\otimes e_3\), not merely close to it;
3. the absolute, top-normalized, and trace-relative eigengap bounds are
   valid with the archived amplitude \(C^2=15\cdot9985\);
4. the covariance works are opposite and equal to
   \(\pm3\sqrt2\Lambda^3/40\);
5. the lower-plane residual is \(3\Lambda^2/2\), so the example does not
   contradict the complete-frame continuation bridge;
6. the critical projector norm gives the integration-by-parts error in
   \(L_t^1\), with exact endpoint exponents;
7. a smooth compact seed has nonzero positive error;
8. an amplitude-normalized concentrating sequence fixes all three input
   norms while its \(L_t^s\) error diverges for every \(s>1\);
9. the finite-\(p\) weighted continuation theorem follows from the stated
   interpolation and the already audited R0.70P middle-strain consumer.

No blocker or major mathematical issue was found after the corrections
listed in Section 8.

## 2. Fourier and frame audit

### 2.1 Base triad

For

\[
 n=(-1,0,-1),\quad p=(-3,-3,4),\quad q=(4,3,-3),
 \tag{2.1}
\]

direct arithmetic gives

\[
 n+p+q=0,
 \qquad
 |n|^2=2,
 \qquad
 |p|^2=|q|^2=34.
 \tag{2.2}
\]

The displayed polarizations \(c,a,b\) are unit vectors, lie in
\(e_3^\perp\), and are orthogonal to their own frequencies.  The strict
frame separation is

\[
 34-16\cdot2=2>0.
 \tag{2.3}
\]

Thus the low response is orthogonal to the common high response.  The
pointwise covariance range is contained in \(e_3^\perp\).  Its trace and
operator norm are bounded by

\[
 |c\cos(n\cdot x)|^2
 +|a\cos(p\cdot x)+b\cos(q\cdot x)|^2
 \le1+4=5.
 \tag{2.4}
\]

### 2.2 Independent work reconstruction

An independent ordered Fourier enumeration used

\[
 \widehat u(k)=\frac{i}{|k|^2}k\times\widehat\omega(k),
 \qquad
 \widehat S(k)=\frac i2
 (k\otimes\widehat u(k)+\widehat u(k)\otimes k),
 \tag{2.5}
\]

and contracted each strain coefficient against the covariance coefficient
at the opposite frequency.  It reproduced

\[
 \begin{aligned}
 \mathfrak I(\xi)&=\frac{6\sqrt2}{85},\\
 \mathfrak P_Q(\xi)&=\frac{3\sqrt2}{40},\\
 \mathfrak E_S(\xi)&=-\frac{3\sqrt2}{680},
 \end{aligned}
 \qquad
 \mathfrak I=\mathfrak P_Q+\mathfrak E_S.
 \tag{2.6}
\]

The exact producer obtains the same values symbolically.

### 2.3 Filler resonance count

The filler radii satisfy

\[
 24^2-16\cdot34=32,
 \qquad
 97^2-16\cdot24^2=193.
 \tag{2.7}
\]

The independent ordered zero-sum triple count, classified by the number of
filler modes, is

\[
 \boxed{\{0:12,\ 1:0,\ 2:0,\ 3:0\}.}
 \tag{2.8}
\]

Thus every cubic resonance is a base resonance.  The filler changes neither
the full, covariance, nor defect work.  Flipping the sign of the six base
modes flips all three works while leaving the quadratic covariance fixed.

## 3. Principal-projector and eigengap audit

Because the base polarizations lie in \(e_3^\perp\) and the filler
polarization is \(e_3\), the covariance is the exact orthogonal sum

\[
 Q=\Lambda^2 Q(\xi)
 \oplus \Lambda^2 C^2h\,e_3\otimes e_3.
 \tag{3.1}
\]

For \(h=\cos^2(24x_1)+\sin^2(97x_1)\), the zero-set argument is legal:
97 is odd, so a zero of the cosine and a zero of the sine cannot coincide
after denominators are cleared.  The same distance and sine-chord proof as
R0.70Y gives

\[
 h\ge\frac1{24^2+97^2}=\frac1{9985}.
 \tag{3.2}
\]

With \(C^2=15\cdot9985\), the scalar \(e_3\) block is at least 15 and the
plane block has operator norm at most 5.  Therefore

\[
 \lambda_1=\Lambda^2C^2h,
 \qquad
 \lambda_2\le5\Lambda^2,
 \qquad
 P_1=e_3\otimes e_3.
 \tag{3.3}
\]

It follows that

\[
 \lambda_1-\lambda_2\ge10\Lambda^2,
 \qquad
 \frac{\lambda_1-\lambda_2}{\lambda_1}\ge\frac23.
 \tag{3.4}
\]

Since \(\operatorname{tr}Q(\xi)\le5\),

\[
 \frac{\lambda_1-\lambda_2}{\operatorname{tr}Q}
 \ge\frac{C^2h-5}{C^2h+5}\ge\frac12.
 \tag{3.5}
\]

The projector is exactly constant, so \(\nabla P_1=0\).  Every frame block
is a scalar Fourier multiplier, hence

\[
 [T_\alpha,P_1]=[T_\alpha,I-P_1]=0.
 \tag{3.6}
\]

This step uses no rough projector-gradient upper estimate.

## 4. Residual and no-contradiction audit

Parseval and the unit polarizations give

\[
 \int_{\mathbb T^3}|\xi|^2\,dx
 =\frac12(1+1+1)=\frac32.
 \tag{4.1}
\]

Since \((I-P_1)\eta=0\),

\[
 R=\int\operatorname{tr}((I-P_1)Q)\,dx
 =\frac32\Lambda^2.
 \tag{4.2}
\]

Thus the constant-projector example does not satisfy a vanishing or
amplitude-small transverse residual.  It cannot refute R0.70P/Q's
continuation theorems.  It refutes only a law whose controlling side becomes
zero when projector variation and the scalar-frame commutator vanish, even
if a large eigengap is also supplied.

The nonzero covariance work comes from the common response of the equal
radii \(|p|=|q|\); their response chord is zero.  The example therefore also
rules out a proposed common-channel gain that is made solely from response
chords or projector variation.  It does not rule out a genuine Carleson or
BMO quantity that measures common amplitude.

With a free filler amplitude \(A\), the physical vorticity is the orthogonal
sum \(\sigma\xi+AFe_3\), where
\(F=\cos(24x_1)+\sin(97x_1)\).  Hence

\[
 \sin\theta_A
 =\frac{|\xi|}{\sqrt{|\xi|^2+A^2F^2}}.
 \tag{4.3}
\]

The nonzero analytic trigonometric polynomial \(F\) has a measure-zero zero
set.  Dominated convergence proves
\(\|\sin\theta_A\|_r\to0\) for every finite \(r\), while the covariance work
stays \(\pm3\sqrt2/40\).  This does not test \(L^\infty\) angle coherence or
the weighted transverse norm, which remains \(\|\xi\|_2\).

## 5. Critical exponent audit

Let \(\rho=3/p\) and \(q=2/(1-\rho)\).  With
\(r=2p/(p-2)\),

\[
 \frac1r+\frac12+\frac1p=1
 \tag{5.1}
\]

and

\[
 \|u\|_r
 \le C\|u\|_2^{1-\rho}\|\nabla u\|_2^\rho.
 \tag{5.2}
\]

Consequently,

\[
 |I_L|
 \le C
 \|\nabla L\|_p
 \|u\|_2^{1-\rho}
 \|\nabla u\|_2^{1+\rho}.
 \tag{5.3}
\]

The time exponents satisfy exactly

\[
 \frac1q+\frac{1+\rho}{2}=1.
 \tag{5.4}
\]

This proves the report's \(L_t^1\) estimate.  At \(p=3\), the velocity
\(L^2\) power vanishes and \(q=\infty\).  At \(p=\infty\), \(q=2\), and
the two time-\(L^2\) factors multiply only into \(L_t^1\).  No endpoint was
obtained by an illegal finite-exponent limit.

## 6. Compact seed and scaling audit

For the compact vector potential in the report, the core velocity and the
first-variation vector are

\[
 U=(z,0,y),
 \qquad
 F_i=U_1\partial_2U_i+U_2\partial_1U_i=(0,0,z).
 \tag{6.1}
\]

Thus \(\psi=\operatorname{div}F=1\) in the core and is not identically zero.
For
\(L_\varepsilon=(\cos(\varepsilon\psi),
\sin(\varepsilon\psi),0)^{\otimes2}\),

\[
 \left.\frac d{d\varepsilon}L_\varepsilon\right|_{\varepsilon=0}
 =\psi(e_1\otimes e_2+e_2\otimes e_1).
 \tag{6.2}
\]

Integration by parts gives

\[
 J'(0)=-\int\psi^2<0.
 \tag{6.3}
\]

The report uses \(I_L=-J\); a small positive \(\varepsilon\) therefore
makes \((I_L)_+\) nonzero.  Smooth nested time cutoffs preserve this sign on
the support of \(u\).

Under Navier--Stokes concentration, the three relevant scaling exponents are

\[
 \begin{array}{c|c}
 \text{quantity}&\text{power of }\lambda\\ \hline
 \|\nabla L\|_{L_t^qL_x^p}&1-3/p-2/q=0,\\
 \|u\|_{L_t^\infty L_x^2}&-1/2,\\
 \|\nabla u\|_{L_t^2L_x^2}&-1/2,\\
 \|I_L\|_{L_t^1}&-1,\\
 \|I_L\|_{L_t^2}&0.
 \end{array}
 \tag{6.4}
\]

For the stronger sequence
\(\widehat u_\lambda=\lambda^{1/2}u_\lambda\), both energy norms and the
critical projector norm are fixed exactly, whereas

\[
 \|I_{L_\lambda}[\widehat u_\lambda]\|_{L_t^s}
 =\lambda^{2-2/s}\|I_L[u]\|_{L_t^s}.
 \tag{6.5}
\]

This proves the no-finite-control-function statement for every \(s>1\).
It also proves that the \(L_t^1\) result is optimal among estimates using
only those three norm values.

The fixed-torus realization is valid.  The spatial bubble has a zero/constant
collar, so it can be placed in one periodic coordinate cell.  The compact
curl has zero mean.  The rescaled time support lies inside a fixed interval.
All norms are therefore exactly the whole-space scaled norms; no torus
replication factor appears.

## 7. Weighted theorem dependency audit

Spatial Hölder with \(u\in L^2\), \(\nabla L\in L^p\), and
\(\nabla u\in L^{2p/(p-2)}\), followed by Sobolev interpolation of
\(\nabla u\), gives

\[
 |I_L|^2
 \le C_p
 \|u\|_2^2\|\nabla L\|_p^2
 \|\nabla u\|_2^{2(1-3/p)}
 \|\nabla^2u\|_2^{6/p}.
 \tag{7.1}
\]

Thus finiteness of the archived \(\mathfrak W_{L,p}\) gives
\(I_L\in L_t^2\).  Together with
\(P\omega\in L_t^4L_x^2\), the exact projector identity gives
\(Z_L\in L_t^2\).  R0.70P's already audited middle-strain theorem then gives
continuation.

The cost is dimensionally critical.  It is not an a priori bound: for finite
\(p\) it contains \(\nabla^2u\), and at \(p=\infty\) it reduces to the
R0.70Q weighted direction cost.  The report classifies it accordingly.

## 8. Corrections incorporated during audit

1. The preliminary filler amplitude \(C^2=10\cdot9985\) was enough for a
   top-normalized gap of \(1/2\), but not for the claimed trace-relative gap
   \(1/2\).  The archived value is
   \(C^2=15\cdot9985\), which gives (3.4)--(3.5).
2. The initial scaling statement rejected only the natural monomial
   \(L_t^2\) estimate.  The amplitude-normalized sequence now proves the
   stronger no-finite-control-function theorem for every \(s>1\).
3. The compact seed sign is recorded relative to the report's convention
   \(I_L=-J\), so the no-go reaches \((I_L)_+\).
4. The fixed-torus concentration is stated through a compact bubble, not a
   periodic replication scaling.
5. The report explicitly keeps physical-vorticity-direction criteria
   separate from covariance-projector criteria.

## 9. Final claim boundary

R0.71A proves a route-level obstruction, not a regularity no-go.  It does
not establish any of the following:

- failure of a critical projector criterion for Navier--Stokes solutions;
- a singular solution or a blow-up scenario;
- impossibility of using the solution-selected covariance dynamics;
- impossibility of a residual-weighted, signed, BMO, or Carleson estimate;
- propagation of \(R\), \(\mathfrak C_P\), or
  \(\mathfrak W_{L,p}\);
- global regularity or a solution of the Millennium problem.

The exact conclusion is narrower and fully supported: projector coherence
alone is insufficient, and the existing energy-level projector identity has
optimal unstructured time integrability \(L_t^1\) on the critical line.

## 10. Reproduction and repository validation

The final local candidate passed the following checks on 2026-08-25:

1. the exact producer reproduced `result.json` byte for byte;
2. the focused R0.71A test file passed all 8 tests;
3. the full repository test suite passed all 705 tests after placing the
   pinned Python environment first on `PATH`;
4. the nine archived payload hashes matched `SHA256SUMS`;
5. focused ESLint completed without an error;
6. the English catalogue build reported 105 pages, 9,855 translations, and
   41 already-known stale translations; and
7. the vinext production build completed all 5 stages.

The first full-suite invocation inherited the system Python and therefore
failed dependency imports in older exact-certificate tests.  Repeating the
same suite with `tmp/r068b-venv/bin` first on `PATH` removed those environment
failures and produced the 705/705 result.  No mathematical payload changed
between those two invocations.

No network was required by the exact reproduction and local validation
commands.  No GPU, DGX, GitHub push, or public-page update was used for the
internal release candidate described in this audit.
