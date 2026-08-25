# R0.71I independent mathematical audit

**Date:** 2026-08-26

**Status:** release-grade adversarial audit of
`research/r071i_report-source.md`.  The audit verifies algebra, constants,
quantifiers, and claim boundaries.  It is not a peer-review report or a
novelty determination.

## 1. Independence design

The release uses two computational paths and one manual synthesis pass.

1. `research/r071i_exact_audit.py` uses SymPy and the repository's exact
   finite-Fourier primitives.  It produces the canonical sorted JSON for the
   hard/soft scalar identities, common-heat pulse, symmetric 2D3C datum,
   limiting profiles, and refresh gap.
2. `research/r071i_independent_audit.py` imports neither the producer nor the
   project Fourier helper.  It uses only the Python standard library.  It
   checks a smooth three-dimensional Hilbert path, rebuilds curl, convolution,
   Leray projection, and Parseval sums directly with Python complex numbers,
   and separately evaluates the heat integrals and scaling ratios.
3. The manual synthesis pass recomputed every sign and factor, reconciled two
   different candidate Fourier supports, and separated exact initial algebra
   from the fixed-window \(K\to\infty\) conclusion.

The figure package adds a fourth path: a producer validator and an independent
70-digit `Decimal` validator for all plotted rows.  No audit performs DNS or
time-steps the three-dimensional PDE.

## 2. Canonical witness reconciliation

Two drafts contained different valid-looking data and therefore different
constants.

The stale four-target version retained only

\[
 (1,2),\ (-1,-2),\ (1,3),\ (-1,-3)
 \tag{2.1}
\]

at \(K=1\).  It gives

\[
 \|u_0\|_2^2=127/45,
 \quad Y=33K^2/5,
 \quad\|F\|_2^2=4K^2,
 \quad d=4K^4.
 \tag{2.2}
\]

Those constants are not used in the release.

The canonical version is symmetric and compatible from the start with the
fixed radial two-ring multiplier.  It retains all eight modes

\[
 (\pm K,\pm2K,0),
 \qquad(\pm K,\pm3K,0).
 \tag{2.3}
\]

Direct normalized-Haar Parseval reconstruction gives

\[
 \boxed{
 \|u_0\|_2^2=263/90,
 \quad Y=36K^2/5,
 \quad\|F\|_2^2=8K^2,
 \quad d=8K^4,
 \quad B=0.}
 \tag{2.4}
\]

For every \(|n|=2\) retained mode,

\[
 (\widehat u_3,\widehat F_3/K,\widehat C_3/K^2)=(1/5,1,1),
 \tag{2.5}
\]

and for every \(|n|=3\) mode,

\[
 (\widehat u_3,\widehat F_3/K,\widehat C_3/K^2)=(1/10,-1,1).
 \tag{2.6}
\]

The independent binary64 convolution has maximum residual
\(1.78\times10^{-15}\) against (2.4), including the zero Lamb--curl pairing.

**Verdict:** PASS for the symmetric eight-target version; the four-target
constants are excluded from formal and public claims.

## 3. Hard joint identity

Let \(\lambda=\nu K^2\),
\(N=F_t+\lambda F\), \(M=C_t+\lambda C\),
\(E=C/\rho\), \(P=I-E\otimes E\), and

\[
 S=\langle N,E\rangle+\rho^{-1}\langle PF,PM\rangle.
 \tag{3.1}
\]

Because \(P C=0\),

\[
 PM=PC_t,
 \qquad E_t=PM/\rho.
 \tag{3.2}
\]

Therefore

\[
 \beta_t+\lambda\beta=S.
 \tag{3.3}
\]

With \(z=\beta/\sqrt Y\),

\[
 \mathcal J=S/\sqrt Y-\frac{Y_t}{2Y}z,
 \tag{3.4}
\]

and hence

\[
 z_t+\lambda z=\mathcal J,
 \qquad
 a_t+2\lambda a=2z^+\mathcal J.
 \tag{3.5}
\]

The standard-library checker evaluates these identities at 101 points along
an analytic three-dimensional path with strictly positive \(\beta\).  Maximum
residuals are:

| Row | Maximum residual |
|---|---:|
| \(E_t=PM/\rho\) | \(3.02\times10^{-16}\) |
| \(\beta_t+\lambda\beta=S\) | \(6.66\times10^{-16}\) |
| \(z_t+\lambda z=\mathcal J\) | \(4.44\times10^{-16}\) |
| \(a_t+2\lambda a=2z\mathcal J\) | \(8.88\times10^{-16}\) |

The enstrophy logarithm appears once, inside \(\mathcal J\).  If the
unnormalized \(S\) ledger is used instead, \(Y_t/Y\) must be paid separately;
adding it again after budgeting \(\mathcal J\) would double count.

**Verdict:** PASS.

## 4. Amplitude-vector Pythagorean identity

For \(\Xi=z^+E\), radial and tangent parts are orthogonal:

\[
 \Xi_t+\lambda\Xi
 =\mathbf1_{\{z>0\}}\mathcal J E+z^+PM/\rho.
 \tag{4.1}
\]

Thus

\[
 \|\Xi_t+\lambda\Xi\|_2^2
 =\mathbf1_{\{z>0\}}\mathcal J^2
 +a\|PM\|_2^2/d.
 \tag{4.2}
\]

The 101-point independent maximum residual is
\(6.66\times10^{-16}\).

The alternative equation

\[
 \|\Xi_t+(\lambda+Y_t/(2Y))\Xi\|_2^2
 =\mathbf1_{\{\beta>0\}}S^2/Y+a\|PM\|_2^2/d
 \tag{4.3}
\]

is equivalent.  Equations (4.2) and (4.3) must not be mixed by using
\(\mathcal J\) on the right of (4.3).

**Verdict:** PASS.

## 5. BV and endpoint coefficients

For nonnegative absolutely continuous \(a\),

\[
 \operatorname{TV}(a)+a(T_-)+a(T_+)
 =2a(T_-)+2\int(a_t)^+dt.
 \tag{5.1}
\]

Since \((a_t)^+\le2z^+\mathcal J^+\),

\[
 \operatorname{TV}(a)+a(T_-)+a(T_+)
 \le2a(T_-)+4\int z^+\mathcal J^+dt.
 \tag{5.2}
\]

Both endpoint amplitudes occur on the left.  The terminal amplitude is paid
through the entry and positive creation; denominator-component faces have
not been deleted.  If a refresh produces \(\Delta a\), the exact coarea
extension adds \(2(\Delta a)^+\), safely bounded by
\(2|\Delta a|\).

**Verdict:** PASS; the factors two and four are necessary.

## 6. Soft denominator

For

\[
 E_\varepsilon=C/\sqrt{d+\varepsilon},
 \quad P_\varepsilon=I-C\otimes C/(d+\varepsilon),
 \quad\theta_\varepsilon=\varepsilon/(d+\varepsilon),
 \tag{6.1}
\]

\(P_\varepsilon\) is symmetric but is not an orthogonal projection.  The
global fixed-\(\varepsilon\) identity is

\[
 (E_\varepsilon)_t
 +\lambda\theta_\varepsilon E_\varepsilon
 =(d+\varepsilon)^{-1/2}P_\varepsilon M.
 \tag{6.2}
\]

It implies

\[
 (a_\varepsilon)_t
 +2\lambda(1+\theta_\varepsilon)a_\varepsilon
 =2z_\varepsilon^+\mathcal J_\varepsilon.
 \tag{6.3}
\]

The extra radial damping has a plus sign on the left.  Independent maximum
residuals over 101 points are \(2.43\times10^{-16}\) for (6.2) and
\(1.78\times10^{-15}\) for (6.3).

The scalar equations cross \(d=0\) for fixed \(\varepsilon\).  A vector
Pythagorean identity using the hard unit vector \(E\) does not.

**Verdict:** PASS with this domain qualification.

## 7. Common-heat pulse

For the abstract two-eigenvalue path, independent differentiation and
quadrature give

\[
 x_*=0.28077640640441515,
 \qquad
 \tau_*=0.6350983165684457,
 \tag{7.1}
\]

\[
 a_*=0.056700272781236016,
 \qquad
 \operatorname{TV}(a)=0.11340054556247203.
 \tag{7.2}
\]

The dimensionless heat integral is \(3/8\), numerically
\(0.3750000000078062\), and

\[
 \int\frac{\mathcal J^2}{\nu K^2}dt
 =\frac34(1-\log2)
 =0.23013961458004104,
 \tag{7.3}
\]

with quadrature value \(0.23013961459034804\).  The exact ratio is

\[
 \frac{\nu(71-17\sqrt{17})}{3}K^2.
 \tag{7.4}
\]

Both outer **amplitude** faces vanish; \(\|C(0)\|>0\), so they are not
denominator faces.

**Verdict:** PASS as an abstract common-heat obstruction, not an NSE pair.

## 8. Fixed-window 2D3C limit and quantifiers

For fixed \(\nu>0\), fixed \(M<\infty\), finite weighted index \(s\), and
admissible torus frequencies \(K\to\infty\), the rescaled sideband equation
is a diagonal heat generator plus a bounded shift of size \(1/(\nu K)\).
Duhamel's formula and the differentiated equation give

\[
 \|c^{(K)}-c^{(0)}\|_{C^1([0,M];\ell_s^2)}
 \le C_{M,s,\nu}/K.
 \tag{8.1}
\]

The limiting profiles are therefore rigorous fixed-window asymptotics, not
exact finite-\(K\) curves.  At \(\theta_*=\log2/10\),

\[
 Q_0(\theta_*)=1/3,
 \qquad
 A_0(\theta_*)
 =\frac{2}{3(1+3\,2^{1/5}+2\,2^{4/5})}
 =0.08408699118010307.
 \tag{8.2}
\]

Independent quadrature gives

\[
 \int_0^{\theta_*}G_0(\theta)d\theta
 =0.06432964680804105.
 \tag{8.3}
\]

For \(K=8,16,32,64\), the ratio of the certified weighted-BV lower bound to
the limiting weighted heat volume is respectively

\[
 41.8281, 167.3122, 669.2488, 2676.9952,
 \tag{8.4}
\]

and successive ratios are exactly four up to binary64 rounding.  This checks
the \(K^2\) law.

The logical force is termwise: the physical-time heat volume of the declared
smooth radial two-ring component does not pay that component's positive
joint creation.  The audit does not certify the preselected broad single-ring
frame, every radial multiplier, an explicit completed Parseval frame, or the
total full-frame right side.

**Verdict:** PASS as a rigorous asymptotic, componentwise no-go for
heat-volume-only control.

## 9. Refresh witness

For the separate complementary-cutoff construction,

\[
 \sum_\pm a_{\delta,\pm}=\frac{U^2}{3\delta^2+4}.
 \tag{9.1}
\]

The endpoint values are \(U^2/4\) and \(U^2/7\), and their difference is

\[
 \frac{3U^2}{28}=0.10714285714285715\,U^2.
 \tag{9.2}
\]

This is a cutoff shape/refresh cost.  The parameter \(\delta\) is not NSE
time; time enters only after choosing a schedule \(\delta(t)\).

**Verdict:** PASS only against uncontrolled motion or refresh.

## 10. Final release verdict

The following rows are independently supported:

1. complete classical all-shell \(F_t,C_t\) bookkeeping;
2. hard and soft normalized joint identities;
3. the hard amplitude-vector Pythagorean identity;
4. the face-aware BV coefficient and endpoint formula;
5. exact common-heat constants and \(K^2\) ratio;
6. exact symmetric eight-mode 2D3C initial Fourier data;
7. fixed-window \(C^1\) asymptotics and the resulting componentwise no-go;
8. the exact \(3U^2/28\) refresh gap.

The release must not claim:

- an exact finite-\(K\) 2D3C profile;
- coverage of the preselected broad standard dyadic frame;
- a proved full Parseval-frame no-go;
- control or failure of the full face-paid weighted-BV target;
- a Leray-level passage, continuation theorem, singularity, regularity
  result, originality result, or Millennium-problem result.

With those boundaries retained, the mathematical audit verdict is
**PASS**.  The direct residual-square and R0.71F heat-volume-only routes are
closed for the quantified settings above.  R0.71J must seek a genuinely
different all-shell NSE budget or a structural theorem specific to the
preselected frame.
