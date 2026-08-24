# R0.70U independent mathematical audit

**Verdict:** **PASS** for the locked snapshot below.  No blocker or major
issue remains.  The report proves a fixed-frame, fixed-frequency,
instantaneous obstruction to residual-only control above square-root order.
It does not prove a critical square-root upper bound, a time-integrated
estimate, an enstrophy closure, a singularity, global regularity, or a
solution of the Navier--Stokes Millennium problem.

## 1. Locked snapshot

I audited the R0.70U release on branch
codex/r070u-signed-sqrt-obstruction at base commit

\[
 \mathtt{f2eee85ebd09873004e2261c3e86e4dacc2acf2f}.
\]

The final files and SHA-256 digests are:

- research/r070u_report-source.md:
  d71082bdf6ae8465d93f43cfb9cc50d60f72e65ee323330462790184de8da8f3;
- research/r070u_exact_audit.py:
  4fdc44bd6df9c3b1902661c4504264f4e34754fa6bdd45c366798e08c5f63530;
- tests/r070u-signed-sqrt-obstruction-gate.test.mjs:
  a30a57053be4ddaa5ad94f2d6386884cc19554675035d2a93688ff6659adf0fc;
- research/certificates/r070u/README.md:
  0ffb9567b2f122980171d2dac1c76e1a31abd9106f139b47c65f9178e8d8ad88;
- research/certificates/r070u/command.txt:
  64f1fa7c6364d02edb2fa5228785583ac86f563277096d3f1db75745c6d681cc;
- research/certificates/r070u/environment.txt:
  087036c61c697d3d9ba82da09cdc4b45bf42bdca87ae7487682220d83210cfac;
- research/certificates/r070u/result.json:
  2b85e8f44f54eaddcba39463c63fc2480e79d6675969277df87fd8474f035684;
- research/certificates/r070u/SHA256SUMS:
  0b65b7431100487b188b6a8b9729949284b82259d9414ae7f56921b70288ce1c.

The manifest locks exactly five payload paths: the README, command,
environment, result, and producer.  The report and focused-test hashes are
recorded separately above.

## 2. Test and build record

The final lock passed:

| Check | Result | Boundary |
|---|---:|---|
| Focused R0.70U gate | 8/8 PASS | Includes raw producer-output byte equality, exact path-set locking, and all four machine groups |
| Certificate SHA manifest | 5/5 PASS | Every listed digest and the exact five-path set match |
| Full Node suite | 655/655 PASS | Repository-wide regression record |
| Direct i18n build | PASS | 105 pages, 9855 translations, 41 stale translations |
| Direct vinext build | 5/5 PASS | All five build stages completed |

The stale-translation count is a dictionary-maintenance statistic, not a
missing R0.70U page: this release remains an internal report and does not
authorize publication.

The exact producer uses Python 3.12.13 and SymPy 1.14.0.  Its archived local
virtual environment is intentionally ignored by Git.  The certificate README
now states how a clean checkout must recreate an equivalent interpreter and
identifies the archived JSON and raw-byte comparison as the reproducibility
targets.

## 3. Exact signed compression

With normalized Haar measure, row-gradient convention

\[
 B_{ij}=\partial_i u_{*,j},
 \qquad S=\frac12(B+B^{\mathsf T}),
\]

and complete-frame covariance

\[
 Q=\sum_\alpha T_\alpha\omega\otimes T_\alpha\omega
  =\lambda L+H,
\]

the R0.70T stretching identity gives

\[
 \mathfrak E_S
 =\int_{\mathbb T^3}
   S:(\omega\otimes\omega-Q)\,dx.
\]

Consequently,

\[
 \boxed{
 \mathfrak R_{\mathrm{sgn}}
 =-\int_{\mathbb T^3}u_*\cdot\mathcal A_L\,dx
  +\int_{\mathbb T^3}
    S:(\omega\otimes\omega-\lambda L)\,dx.}
\]

This is an exact reassembly.  It does not itself estimate the signed
remainder.

## 4. Pythagorean triad and Biot--Savart signs

For an integer \(m\ge2\), the report sets

\[
 a=m^2-1,\qquad b=2m,\qquad K=m^2+1,
\]

\[
 k=(a,b,0),\qquad
 p=(a,-b,0),\qquad
 q=k+p=(2a,0,0),
\]

and

\[
 n_k=K^{-1}(-b,a,0).
\]

The exact identities

\[
 a^2+b^2=K^2,\qquad
 |k|=|p|=K,\qquad
 |q|=2a=2K-4
\]

put the first two modes on one radial multiplier shell and the third on a
nearby dyadic shell.

For \(A>\delta>0\),

\[
 w=A\bigl[n_k\cos(k\cdot x)+e_3\sin(k\cdot x)\bigr]
   +\delta e_3\cos(p\cdot x),
\]

\[
 h=e_2\cos(q\cdot x),\qquad
 \omega_\varepsilon=w+\varepsilon h.
\]

The sign convention is

\[
 \nabla\times w_1=-Kw_1.
\]

The mean-zero Biot--Savart velocities are

\[
 u_w
 =-\frac A K
   \bigl[n_k\cos(k\cdot x)+e_3\sin(k\cdot x)\bigr]
  +\frac{\delta}{K^2}(b,a,0)\sin(p\cdot x),
\]

\[
 u_h=-\frac1{2a}e_3\sin(q\cdot x).
\]

The machine producer constructs the actual complex Fourier coefficients,
checks every divergence coefficient, and recovers \(w\) and \(h\) by curl.
The parameter premise \(m\ge2\), \(A>\delta>0\) is now explicit in the
certificate and focused test.

Since the first helical block has constant magnitude \(A\),

\[
 |w|\ge A-\delta=:g_0>0.
\]

Thus the exact-rank base state is globally nonvanishing.

## 5. Fixed-frame overlap is analytic, not numerical

For the pinned radial multiplier, define

\[
 v(r)_j=\varphi(2^{-j}re_1).
\]

Tightness yields \(\|v(r)\|_{\ell^2}=1\).  Strict annular support permits at
most two adjacent nonzero entries.  Since

\[
 v(2r)_j=v(r)_{j-1},
\]

the shifted overlap obeys

\[
 |\langle v(r),v(2r)\rangle|\le\frac12.
\]

For

\[
 \gamma_m=\langle v(K),v(2a)\rangle
\]

and \(2a=2K-4\), smooth finite overlap gives

\[
 \|v(2a)-v(2K)\|_{\ell^2}
 \le\frac{C_\varphi}{K}.
\]

Hence every fixed admissible cutoff has an analytically selected
\(m_0(\varphi)\) such that, for \(m\ge m_0(\varphi)\),

\[
 |\gamma_m|\le\frac34.
\]

After one such finite \(m\) is fixed, put

\[
 \gamma=\gamma_m,\qquad
 \kappa=1-\gamma^2\ge\frac7{16},\qquad
 1-\gamma\ge\frac14.
\]

The order of quantifiers is essential: the cutoff is fixed, a sufficiently
large but finite \(m\) is selected analytically, and only then does
\(\varepsilon\to0\).  Neither the producer nor its \(m=3\) rational anchor
claims to evaluate a numerical \(m\) for an unspecified cutoff.

## 6. Covariance and residual order

Radiality and real-evenness give

\[
 T_jw=c_jw,\qquad T_jh=d_jh,
\]

with

\[
 \sum_jc_j^2=\sum_jd_j^2=1,
 \qquad
 \sum_jc_jd_j=\gamma.
\]

Therefore

\[
 Q_\varepsilon
 =w\otimes w
  +\varepsilon\gamma(w\otimes h+h\otimes w)
  +\varepsilon^2h\otimes h.
\]

Writing

\[
 z_\varepsilon=w+\varepsilon\gamma h,
\]

gives the exact positive factorization

\[
 \boxed{
 Q_\varepsilon
 =z_\varepsilon\otimes z_\varepsilon
  +\kappa\varepsilon^2h\otimes h.}
\]

The producer now derives, independently from the actual matrix,

\[
 \operatorname{tr}Q_\varepsilon
 =|w|^2+2\varepsilon\gamma\,w\cdot h
   +\varepsilon^2|h|^2
\]

and

\[
 \sigma_2(Q_\varepsilon)
 =\kappa\varepsilon^2
   \bigl(|w|^2|h|^2-(w\cdot h)^2\bigr).
\]

This repair is important: an earlier candidate assigned the expected trace
and product formulas before expanding the smaller root, so its spectral check
was self-referential.  The final producer computes

\[
 \sigma_2(Q)
 =\frac12\bigl[(\operatorname{tr}Q)^2-\operatorname{tr}(Q^2)\bigr]
\]

directly from \(Q_\varepsilon\), compares it with the vector formula, and
locks both residuals to zero.

For \(|\varepsilon|\le g_0/4\), Weyl's inequalities give

\[
 \lambda_1\ge\frac{9g_0^2}{16},
 \qquad
 \lambda_2\le\frac{g_0^2}{16},
 \qquad
 \lambda_1-\lambda_2\ge\frac{g_0^2}{2}.
\]

Since \(Q_\varepsilon\) has rank at most two,

\[
 r_\varepsilon=\lambda_2,
\]

and

\[
 \lambda_1\lambda_2
 =\kappa\varepsilon^2|w\times h|^2.
\]

The uniform expansion is

\[
 \boxed{
 r_\varepsilon
 =\kappa\varepsilon^2|P_wh|^2
  +O(|\varepsilon|^3),}
\]

where

\[
 P_w=I-\frac{w\otimes w}{|w|^2}.
\]

At the origin,

\[
 |w(0)\times h(0)|^2
 =\delta^2+\frac{A^2b^2}{K^2}>0.
\]

Thus, for every \(1\le p\le\infty\),

\[
 \boxed{
 \|r_\varepsilon\|_{L^p}
 =\Theta(\varepsilon^2),}
\]

and the same order holds for \(r_\varepsilon/E_\varepsilon\).

This is an \(L^p\)-norm statement.  It is not a global pointwise lower bound:
\(h\), and hence the leading residual coefficient, vanishes on nodal planes.

## 7. Exact resonant coefficient and the repaired factor of two

Let \(S_w\) and \(S_h\) denote the strains of \(u_w\) and \(u_h\).  The
normalized Fourier average gives

\[
 I
 =\int_{\mathbb T^3}h\cdot S_ww\,dx
 =-\frac{A\delta a^2b}{2K^3}.
\]

The independent auxiliary coefficient is

\[
 J
 =\int_{\mathbb T^3}w\cdot S_hw\,dx
 =\frac{A\delta b}{4K}.
\]

The machine forms the full polynomials in \(\varepsilon\) and verifies

\[
 \mathscr P'(0)=2I+J,
\]

\[
 \left(\int S:Q\right)'_{\varepsilon=0}
 =2\gamma I+J.
\]

Consequently,

\[
 \boxed{
 \mathfrak E_S(\varepsilon)
 =2\varepsilon(1-\gamma)I
 =-\frac{(1-\gamma)A\delta a^2b}{K^3}
   \varepsilon.}
\]

During the audit, the displayed hand proof initially placed a coefficient
\(-2A\delta a^2b/K^3\) inside a bracket already multiplied by
\(\tfrac12\cos\psi\).  Read literally, that display produced half the
certified value.  The final report fixes it: the bracket coefficient is
\(-4A\delta a^2b/K^3\), and it explicitly records

\[
 \int_{\mathbb T^3}
 \cos\psi\cos\theta\cos\phi\,dx=\frac14.
\]

The report and exact Fourier producer now agree in sign and normalization.

The rational algebra anchor

\[
 m=3,\qquad A=2,\qquad\delta=1
\]

gives

\[
 I=-\frac{48}{125},\qquad
 J=\frac3{10},\qquad
 \mathscr P'(0)=-\frac{117}{250},
\]

\[
 \mathfrak E_S'(0)
 =-\frac{96}{125}(1-\gamma).
\]

This anchor checks signs and coefficients only.

## 8. Upgrade from the commutator to the whole signed remainder

The upgrade is valid.  Define the exact-rank comparator

\[
 \widetilde Q_\varepsilon
 =z_\varepsilon\otimes z_\varepsilon.
\]

The vector \(z_\varepsilon\) is divergence free and remains nowhere zero.
For a rank-one covariance generated by one nowhere-zero divergence-free
block,

\[
 \mathcal A_L(\widetilde Q_\varepsilon)=0.
\]

Moreover,

\[
 Q_\varepsilon-\widetilde Q_\varepsilon
 =\kappa\varepsilon^2h\otimes h
 =O_{C^1}(\varepsilon^2).
\]

On the uniform simple-top set, the maps from \((Q,\nabla Q)\) to the top
eigenvalue, its projector, the projector derivative, and
\(\mathcal A_L\) are smooth.  Therefore

\[
 \|\mathcal A_{L_\varepsilon}\|_{C^0}
 =O(\varepsilon^2).
\]

Positivity also gives

\[
 |H_\varepsilon|_F\le r_\varepsilon,
 \qquad
 \|H_\varepsilon\|_{C^0}=O(\varepsilon^2).
\]

Since the frequencies are fixed, \(u_\varepsilon\) and
\(S_\varepsilon\) stay uniformly bounded in every fixed smooth norm.  Hence

\[
 -\int u_\varepsilon\cdot\mathcal A_{L_\varepsilon}
 +\int S_\varepsilon:H_\varepsilon
 =O(\varepsilon^2).
\]

It follows that

\[
 \boxed{
 \mathfrak R_{\mathrm{sgn}}(\omega_\varepsilon)
 =-\frac{(1-\gamma)A\delta a^2b}{K^3}\varepsilon
  +O(\varepsilon^2).}
\]

Thus the first-order obstruction belongs to the whole signed remainder, not
only to the aggregate stretching commutator.

## 9. Exact-rank sign boundary

The frame response is real but is not assumed nonnegative.  Therefore
\(\kappa=0\) means \(\gamma=\pm1\), and the two cases differ:

\[
 \gamma=1:
 \qquad
 Q_\varepsilon=(w+\varepsilon h)^{\otimes2},
 \qquad
 \mathfrak E_S=0,
\]

whereas

\[
 \gamma=-1:
 \qquad
 Q_\varepsilon=(w-\varepsilon h)^{\otimes2},
\]

\[
 \mathfrak E_S
 =-2\varepsilon\frac{A\delta a^2b}{K^3}\ne0.
\]

An earlier scope formulation risked replacing
\(\kappa=0\) by the false implication
\(\mathfrak E_S=0\).  The final producer independently constructs and checks
both covariance branches, the physical/frame defects, and the two commutator
values.  The focused test locks the nonzero \(\gamma=-1\) branch.

The obstruction theorem itself avoids this degeneracy by fixing
\(|\gamma|\le3/4\).  It does not assert a universal exact-rank cancellation
theorem.

## 10. Precise no-go quantifiers

Fix the frame, the analytically selected finite \(m\), and \(A>\delta>0\).
For every \(1\le p\le\infty\),

\[
 \|r_\varepsilon\|_{L^p}
 =\Theta(\varepsilon^2),
\]

while

\[
 |\mathfrak R_{\mathrm{sgn}}(\omega_\varepsilon)|
 \ge c|\varepsilon|
\]

for all sufficiently small nonzero \(\varepsilon\).

Therefore, if \(\theta>1/2\) and

\[
 \sup_{0<|\varepsilon|<\varepsilon_0}F_\varepsilon<\infty,
\]

then

\[
 |\mathfrak R_{\mathrm{sgn}}|
 \le F_\varepsilon
      \|r_\varepsilon\|_{L^p}^{\theta}
\]

fails for every sufficiently small nonzero \(\varepsilon\).  The same
argument covers \(r/E\), bounded weights, and moduli

\[
 \Phi(s)=o(\sqrt s).
\]

The conclusion is limited to locally bounded prefactors along this family.
It does not exclude:

- the critical exponent \(\theta=1/2\);
- a positive square-root estimate;
- a coefficient that diverges as the residual vanishes;
- estimates retaining \(\omega\otimes\omega-Q\), projector derivatives,
  \(\mathcal J_P^{1/2}\), or \(\mathfrak C_S^{1/2}\);
- cancellation after time integration;
- a genuinely dynamical Navier--Stokes mechanism.

The family consists of smooth admissible initial vorticities.  It is not a
finite-mode Navier--Stokes trajectory, and the three-mode form is not claimed
to persist.

## 11. Machine versus analytic boundary

The machine producer directly checks:

1. the symbolic Pythagorean geometry, Fourier divergence, curl recovery, and
   helicity sign;
2. the normalized zero-frequency triad contractions \(I\) and \(J\), the
   complete \(\varepsilon\)-polynomials, and the rational anchor;
3. the covariance factorization, physical covariance defect, determinant,
   matrix-derived trace and second spectral invariant, and the smaller-root
   leading coefficient;
4. the two \(\gamma=\pm1\) exact-rank branches;
5. the elementary exponent samples \(1-2\theta\).

The following remain analytic:

- complete countable-frame convergence and multiplier lifting inherited from
  R0.70P/R0.70T;
- the arbitrary-profile overlap derivative estimate and existence of
  \(m_0(\varphi)\);
- the global gap estimate and smooth eigenprojector perturbation;
- the uniform physical-space residual expansion and its \(L^p\) consequence;
- the upgrade
  \(\mathcal A_L,H=O(\varepsilon^2)\);
- the quantified locally bounded-prefactor and general-modulus conclusions;
- local strong-solution interpretation and every time-evolution statement.

The producer does not convert any of these analytic lemmas into a hard-coded
machine boolean.  The focused test instead locks their explicit report scope
and prevents those claims from silently broadening.

## 12. Repairs closed during the independent audit

The final lock incorporates the following corrections:

1. the hand proof of the resonant coefficient now has the correct factor
   \(4\) inside the bracket and the explicit normalized Haar average;
2. trace and \(\sigma_2(Q)\) are derived from the actual covariance matrix,
   eliminating the earlier spectral self-proof;
3. the \(\gamma=1\) and \(\gamma=-1\) exact-rank branches are independently
   machine-checked;
4. producer regeneration is compared with the archived result as raw text,
   not only as parsed JSON;
5. the focused test locks the whole signed-remainder bridge, the parameter
   premise, and the exact five-path SHA set;
6. the README separates inherited frame results from R0.70U's direct analytic
   arguments and documents clean-checkout interpreter recreation.

Each repair is present in the final hashes recorded in Section 1.

## 13. Literature and novelty boundary

The report distinguishes the present multiplication commutator from the
differentiated subgrid stress in filtered-vorticity work.  It also separates:

- Littlewood--Paley shell-transfer and frequency-localized regularity
  criteria;
- physical-vorticity direction coherence and its spatial Hölder exponent;
- variable-plane continuation criteria;
- Beltrami, helical, and narrow-shell structures;
- classical Fourier-triad analysis and finite-mode classifications.

In the bounded primary-source audit, no directly isomorphic result combining
the pinned covariance \(Q\), the spectral residual \(r\), and the same
residual-exponent obstruction was identified.  The report correctly labels
this as a search result, not a novelty or priority claim.

The algebraic triad and eigenvalue expansion are not presented as new general
harmonic-analysis principles.  A publishable PDE advance would still require
a positive critical or time-integrated estimate, or a substantially broader
impossibility theorem.

## 14. Findings by severity

### Blocker

None.

### Major

None.

### Minor

None remaining in the locked release.  The local ignored Python environment
is now an explicit reproducibility boundary with a clean-checkout recreation
instruction, not an unstated certificate dependency.

## 15. Final boundary

R0.70U rigorously proves that, for one fixed complete frame and one fixed
smooth finite-frequency family,

\[
 \|r_\varepsilon\|_{L^p}
 =\Theta(\varepsilon^2)
\]

while

\[
 \mathfrak R_{\mathrm{sgn}}(\omega_\varepsilon)
 =c_0\varepsilon+O(\varepsilon^2),
 \qquad c_0\ne0.
\]

It therefore excludes locally bounded residual-only control with exponent
\(\theta>1/2\), including linear residual and bounded-weight variants.

It does not establish a square-root upper bound, control enstrophy, propagate
the construction under Navier--Stokes evolution, or close any regularity
criterion.  No singularity or Millennium-problem conclusion follows.
