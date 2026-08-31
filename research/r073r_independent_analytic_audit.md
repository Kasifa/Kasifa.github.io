# R0.73R independent analytic audit

**Audited file:** `research/r073r_lp_caloric_certificate_proof.md`

**Audit mode:** independent reconstruction of the shell exponent, vector
Fourier identities, matched support, exact sixth moments, annular heat scale,
and Navier--Stokes boundary

**Final verdict:** `PASS_AFTER_NOTATION_AND_CLAIM_BOUNDARY_REVISIONS`

No fatal mathematical error was found.  The draft needed three explicit
revisions: repair several missing TeX control sequences, label the
heat--Besov equivalence as classical, and distinguish an exact evaluation of
\(\|P_jf\|_6\) from a cheaper a priori proxy.  Those revisions are present in
the audited file.

## 1. Verdict matrix

| Item | Verdict | Independent conclusion |
| --- | --- | --- |
| LP--caloric two-sided norm | `PASS_CLASSICAL` | the preserved double-shell kernel gives the \(\ell^4\) exponent; inverse heat multipliers give the lower bound |
| mean-zero and low block | `PASS` | a nonzero mean makes the infinite-time heat trace diverge; the finite low block is harmless |
| exact vector convolution | `PASS_EXACT` | the Fourier transform of \(|f_j|^2f_j\) gives the nonnegative \(\ell^2\) certificate |
| additive multiplicity | `PASS` | scalar Cauchy--Schwarz plus \(\||f|^2\|_3\le\sum_m\||f_m|^2\|_3\) gives the vector bound with no hidden dimension factor |
| support cardinality | `PASS_SHARP_EXPONENT` | Hausdorff--Young gives \(M_j^{1/3}\), and the two-dimensional Dirichlet patch saturates that power |
| matched Fourier data | `PASS_EXACT` | both families have exactly \(2m^2\) sites and coefficient magnitude \(1/(\sqrt2m)\) |
| carrier sixth moment | `PASS_EXACT` | the neutral coefficient is \(2^{-6}{6\choose3}=5/16\), leading to \(5/(2m^6)\) |
| Dirichlet sixth moment | `PASS_EXACT` | direct triple-sum enumeration gives \((11m^5+5m^3+4m)/20\) |
| Rudin--Shapiro bound | `PASS` | normalized monotonicity and flatness give \((5/2)^{1/6}\le\|W_{P,m}\|_6\le40^{1/6}\) |
| annular heat scaling | `PASS` | the common support lies in \([N,(\sqrt{82}/8)N]\); uniform heat and inverse multipliers give \(N^{-1/2}\|W\|_6\) |
| scaled separation | `PASS` | \(L^2\sim m^{-1/6}\), \(X_D\sim1\), \(X_P\sim m^{-2/3}\), and the common \(\dot H^{1/2}\sim m^{1/3}\) |
| Navier--Stokes interpretation | `PASS_WITH_STRICT_EXCLUSION` | the nonlinear term vanishes, so failure of the sufficient entrance does not indicate unsafe dynamics |

## 2. Shell exponent reconstruction

Let \(b_j=\|P_jf\|_6\) and \(a_j=2^{-j/2}b_j\).  The heat multiplier and
LP square function give

\[
 \|e^{t\Delta}f\|_{L_t^4L_x^6}^4
 \lesssim
 \sum_{j,k}{b_j^2b_k^2\over4^j+4^k}.
\]

The remaining kernel is

\[
 {2^{j+k}\over4^j+4^k}\le2^{-|j-k|}.
\]

Applying Young to \(a_j^2\) therefore gives \(\sum_ja_j^4\), not
\((\sum_ja_j^2)^2\).  Conversely, for a fixed interval
\(I_j=[A4^{-j},B4^{-j}]\), a uniformly bounded inverse heat multiplier gives

\[
 2^{-2j}b_j^4
 \lesssim\int_{I_j}\|e^{t\Delta}f\|_6^4\,dt.
\]

Bounded overlap closes the lower bound.  This independently fixes the
sequence exponent at four.

## 3. Component-safe Fourier reconstruction

For vector coefficients \(A_m(k)\), define

\[
 T_m=\sum_{r=1}^3A_r*\widetilde A_r*A_m,
 \qquad \widetilde A_r(k)=\overline{A_r(-k)}.
\]

Then \(T_m\) is the Fourier sequence of \(|f|^2f_m\), so

\[
 \sum_m\|T_m\|_2^2=\||f|^2f\|_2^2=\|f\|_6^6.
\]

This is exact and phase-sensitive.  It is not an independent improvement of
the \(L^6\) norm; it is a finite Fourier evaluation of it.  For the cheaper
additive proxy, scalar triple-convolution Cauchy--Schwarz gives

\[
 \|f_m\|_6^2\le R^{1/3}\|A_m\|_2^2.
\]

Since

\[
 \|f\|_6^2=\||f|^2\|_3
 \le\sum_m\||f_m|^2\|_3,
\]

summing the component estimates proves \(\|f\|_6\le R^{1/6}\|f\|_2\).

## 4. Matched-family constants

With \(N=8m\), the positive sites are \((N+q,s,0)\),
\(0\le q,s<m\), and the negative sites are their conjugates.  They are
disjoint.  Expanding the real part shows that each coefficient has magnitude
\(1/(\sqrt2m)\), hence

\[
 \|W_{R,m}\|_2^2=2m^2{1\over2m^2}=1.
\]

Writing \(Z=e^{iNx_1}R(x_1)R(x_2)\), only \(Z^3\overline Z^3\) has zero
carrier in \((\operatorname{Re}Z)^6\).  Its coefficient is \(5/16\); after
multiplying by \((\sqrt2/m)^6\),

\[
 \|W_{R,m}\|_6^6={5\over2m^6}\|R\|_6^{12}.
\]

The Dirichlet triple-count identity gives

\[
 \|D_m\|_6^6={11m^5+5m^3+4m\over20},
\]

while the Rudin--Shapiro recursion gives
\(|P_m|^2+|Q_m|^2=2m\) and \(\|P_m\|_\infty\le\sqrt{2m}\).
All powers and constants in the audited proof follow.

## 5. Threshold and dynamics boundary

The statement \(\|\alpha_mW_{D,m}\|_{\mathfrak X}\asymp1\) does not by
itself order an unspecified heat-ball radius.  For a prescribed positive
radius, one may multiply both matched sequences by a fixed additional
constant chosen from the strict analytic lower bound.  The
Rudin--Shapiro sequence still tends to zero and eventually enters; the
Dirichlet sequence remains outside.

Both sequences nevertheless satisfy

\[
 (W_{R,m}\cdot\nabla)W_{R,m}=0.
\]

Their Navier--Stokes evolution is the heat flow and is globally smooth.  The
separation proves that energy spectra and quadratic Sobolev data do not
determine this sufficient entrance.  It proves neither necessity nor a
singularity mechanism.

## 6. Authorized ledger

```text
periodicHeatBesovEquivalence=VERIFIED_CLASSICAL
ell4ShellExponent=PASS
exactVectorTripleConvolution=PASS_EXACT_EVALUATION
additiveMultiplicityUpperBound=PASS
supportCardinalityExponent=PASS_SHARP_FROM_SUPPORT_ONLY
matchedSupportMagnitudeAndQuadraticNorms=PASS_EXACT
dirichletSixthMoment=PASS_EXACT
rudinShapiroUniformBound=PASS
annularHeatScaling=PASS
scaledPhaseSeparation=PASS
failureImpliesUnsafeDynamics=FALSE
uniformL2OnlyStrongRadius=OPEN
arbitraryThreeDimensionalGlobalRegularity=OPEN
clayConclusion=OPEN
noveltyOrPriorityClaim=FORBIDDEN
```
