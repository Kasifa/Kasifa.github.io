# R0.73R candidate: shellwise sextic coherence and the heat-flow entrance

**Status:** frozen problem statement; the analytic proof and first independent
reconstruction agree, while the finite certificate, figure seal, and public
release are still pending

**Domain:** \(\mathbb T^3=[0,2\pi]^3\) with normalized Haar measure;
mean-zero real divergence-free trigonometric polynomials first, followed by
completion when the displayed budget is finite

## 1. Candidate entrance budget

Fix a smooth periodic Littlewood--Paley partition \((P_j)_{j\ge0}\) on
nonzero frequencies, with \(P_j\) supported where
\(c_0 2^j\le |k|\le C_0 2^j\).  Put

\[
 f_j=P_jf,\qquad E_j=\|f_j\|_2.
\]

For \(E_j>0\), define the normalized sextic concentration

\[
 \Theta_j(f):={\|f_j\|_6^6\over E_j^6};
 \tag{1.1}
\]

set \(\Theta_j(f)=0\) when \(E_j=0\).  The candidate shell-concentration
budget is

\[
 \mathcal C_{\rm sh}(f)
 :=\left(\sum_{j\ge0}
 2^{-2j}\Theta_j(f)^{2/3}E_j^4\right)^{1/4}
 =\left(\sum_{j\ge0}
 2^{-2j}\|P_jf\|_6^4\right)^{1/4}.
 \tag{1.2}
\]

The second expression is the familiar dyadic critical Besov quantity.  The
first expression is the local bookkeeping interface used in this note: it
separates shell energy from spatial concentration and admits an exact finite
Fourier formula.  No novelty is claimed for the heat--Besov equivalence.

### Candidate Theorem A: computable heat-flow equivalence and entrance

There are constants \(0<c_{\rm LP}\le C_{\rm LP}<\infty\), depending only
on the fixed periodic Littlewood--Paley partition, such that

\[
 \boxed{\quad
 c_{\rm LP}\mathcal C_{\rm sh}(f)
 \le \|e^{t\Delta}f\|_{L^4((0,\infty);L^6)}
 \le C_{\rm LP}\mathcal C_{\rm sh}(f).
 \quad}
 \tag{1.3}
\]

Consequently, for the fixed a priori global orbit \(u\) in R0.73Q, the
explicit condition

\[
 \mathcal C_{\rm sh}(f)<{\rho_{\mathfrak X}[u]\over C_{\rm LP}}
 \tag{1.4}
\]

places \(u(t_0)+f\) in the same global heat-flow stability tube for every
restart time \(t_0\ge0\).

This is a sufficient perturbative entrance around a fixed known global
orbit.  It is not an \(L^2\)-only theorem and is not a criterion for arbitrary
three-dimensional data.

## 2. Proof skeleton for Theorem A

The periodic square-function inequality and the annular heat multiplier give

\[
 \|e^{t\Delta}f\|_6
 \le C\left(\sum_j\|e^{t\Delta}f_j\|_6^2\right)^{1/2}
 \le C\left(\sum_j e^{-2c2^{2j}t}\|f_j\|_6^2\right)^{1/2}.
 \tag{2.1}
\]

Writing \(a_j=\|f_j\|_6\) and integrating the square of the last sum gives

\[
 \|e^{t\Delta}f\|_{L_t^4L_x^6}^4
 \le C\sum_{j,k\ge0}{a_j^2a_k^2\over 2^{2j}+2^{2k}}.
 \tag{2.2}
\]

Set \(b_j=2^{-j/2}a_j\).  Then

\[
 {a_j^2a_k^2\over 2^{2j}+2^{2k}}
 =b_j^2b_k^2{2^j2^k\over2^{2j}+2^{2k}}
 \le 2^{-|j-k|}b_j^2b_k^2.
 \tag{2.3}
\]

Young's inequality on \(\ell^2(\mathbb N_0)\), applied to
\(c_j=b_j^2\) and the \(\ell^1\) kernel \(2^{-|j|}\), yields

\[
 \sum_{j,k}2^{-|j-k|}b_j^2b_k^2
 \le C\sum_j b_j^4
 =C\sum_j2^{-2j}\|f_j\|_6^4.
 \tag{2.4}
\]

Equations (2.1)--(2.4) prove the upper half of (1.3).  For the lower half,
choose a smooth fattened cutoff \(\widetilde P_j\) equal to one on the
support of \(P_j\).  For

\[
 t\in I_j=[A4^{-j},B4^{-j}],
 \tag{2.5}
\]

the inverse heat multiplier
\(\widetilde P_j e^{-t\Delta}\) has an \(L^6\) operator norm uniform in
\(j\) and \(t\).  Hence

\[
 \|P_jf\|_6\le C\|e^{t\Delta}f\|_6,
 \qquad t\in I_j.
 \tag{2.6}
\]

Since \(|I_j|\asymp4^{-j}\) and the intervals \(I_j\) have bounded overlap,

\[
 2^{-2j}\|P_jf\|_6^4
 \le C\int_{I_j}\|e^{t\Delta}f\|_6^4\,dt.
 \tag{2.7}
\]

Summing (2.7) proves the lower half.  This also shows that the sequence
exponent \(\ell^4\) is forced by the \(L_t^4\) trace; cross-shell phase
cancellation cannot evade that dyadic lower bound.

The mean-zero hypothesis is necessary for the infinite-time trace.  A
nonzero mean is fixed by the heat flow and gives an infinite
\(L^4((0,\infty);L^6)\) norm.  All nonzero low modes are placed in the
single \(j=0\) block and controlled by the periodic spectral gap.

## 3. Exact Fourier form of the sextic coherence

Write

\[
 f_j(x)=\sum_{k\in\mathbb Z^3}a_j(k)e^{ik\cdot x},
 \qquad a_j(k)\in\mathbb C^3.
\]

Define the vector autocorrelation

\[
 A_j(r):=\sum_k a_j(k+r)\cdot\overline{a_j(k)}.
 \tag{3.1}
\]

Up to the harmless sign convention in the Fourier transform,
\(A_j(r)=\widehat{|f_j|^2}(r)\), \(A_j(0)=E_j^2\), and

\[
 \|f_j\|_6^6
 =\sum_{r,s\in\mathbb Z^3}
 A_j(r)A_j(s)A_j(-r-s).
 \tag{3.2}
\]

Thus \(\Theta_j\) is exactly computable from finite Fourier data, including
phase and polarization:

\[
 \Theta_j(f)
 ={\displaystyle\sum_{r,s}A_j(r)A_j(s)A_j(-r-s)
   \over A_j(0)^3}.
 \tag{3.3}
\]

The total in (3.3) is real and nonnegative, although individual summands need
not be.

For a component-safe convolution certificate, put

\[
 \widetilde a_{j,r}(k)=\overline{a_{j,r}(-k)},
 \qquad
 T_{j,m}=\sum_{r=1}^3
 a_{j,r}*\widetilde a_{j,r}*a_{j,m}.
 \tag{3.4}
\]

These are the Fourier coefficients of \(|f_j|^2f_{j,m}\), so Parseval gives
the exact nonnegative identity

\[
 \boxed{\quad
 \|f_j\|_6^6=\sum_{m=1}^3\|T_{j,m}\|_{\ell^2}^2.
 \quad}
 \tag{3.5}
\]

Formula (3.5) is the preferred finite-certificate implementation of
\(\Theta_j\).  A discrete FFT implementation must use linear convolution
with zero padding; circular aliasing would create a false coherence value.

If \(m_j\) is the number of active Fourier sites in the shell, vector-valued
Hausdorff--Young followed by the finite-support comparison
\(\ell^{6/5}\hookrightarrow\ell^2\) gives the phase-blind bound

\[
 \|f_j\|_6\le C_{\rm vec}m_j^{1/3}E_j,
 \qquad
 \Theta_j(f)\le C_{\rm vec}^6m_j^2.
 \tag{3.6}
\]

A second, support-geometric bound retains additive multiplicity.  Let

\[
 R_j:=\max_n\#\{(k_1,k_2,k_3)\in S_j^3:
                    k_1+k_2+k_3=n\},
 \qquad S_j=\{k:a_j(k)\ne0\}.
 \tag{3.7}
\]

Then \(R_j\le m_j^2\), and Plancherel plus Cauchy--Schwarz on each triple
sum yields

\[
 \|f_j\|_6\le C_{\rm vec}R_j^{1/6}E_j.
 \tag{3.8}
\]

This is phase-independent but can be much sharper than raw cardinality.
The exact quantity (3.5) then records the remaining phase and polarization
coherence.

Therefore Theorem A has the cruder modal-count corollary

\[
 \|f\|_{\mathfrak X}
 \le C\left(\sum_j2^{-2j}m_j^{4/3}E_j^4\right)^{1/4}.
 \tag{3.9}
\]

The additive-multiplicity version is

\[
 \|f\|_{\mathfrak X}
 \le C\left(\sum_j2^{-2j}R_j^{2/3}E_j^4\right)^{1/4}.
 \tag{3.10}
\]

The hierarchy used for an auditable entry test is therefore

\[
 \|f_j\|_6
 \le\min\left\{
 \Big(\sum_m\|T_{j,m}\|_2^2\Big)^{1/6},
 C\|a_j\|_{\ell^{6/5}},
 CR_j^{1/6}E_j,
 Cm_j^{1/3}E_j,
 C2^jE_j
 \right\},
 \tag{3.11}
\]

where the first entry is in fact equality.  The alternatives trade exact
phase information for cheaper certificates.  Thresholding small Fourier
coefficients is not an exact support certificate unless the discarded tail
is bounded separately.

The matched family below is designed to show that (3.5) can lose a power even
when the support and every Fourier coefficient magnitude are fixed.

## 4. Candidate Theorem B: matched support, different phase coherence

Let \(m=2^r\), \(N=8m\), and

\[
 D_m(z)=\sum_{q=0}^{m-1}z^q.
 \tag{4.1}
\]

Let \(P_m\) be the Rudin--Shapiro polynomial generated by

\[
 P_1=Q_1=1,
 \qquad
 P_{2m}(z)=P_m(z)+z^mQ_m(z),
 \qquad
 Q_{2m}(z)=P_m(z)-z^mQ_m(z).
 \tag{4.2}
\]

Its coefficients are \(\pm1\), its support is
\(\{0,\ldots,m-1\}\), and

\[
 |P_m(e^{ix})|^2+|Q_m(e^{ix})|^2=2m,
 \qquad \|P_m\|_\infty\le\sqrt{2m}.
 \tag{4.3}
\]

For \(R\in\{D_m,P_m\}\), define the real field

\[
 W_{R,m}(x)
 ={\sqrt2\over m}e_3\,
 \operatorname{Re}\left[
 e^{iNx_1}R(e^{ix_1})R(e^{ix_2})
 \right].
 \tag{4.4}
\]

Both fields are mean zero and divergence free, because they have only an
\(e_3\) component and are independent of \(x_3\).  They have exactly the
same Fourier support and the same Fourier coefficient magnitudes.  The
choice \(N>6(m-1)\) removes every nonconstant carrier term in the exact
second and sixth moments, so

\[
 \|W_{R,m}\|_2=1,
 \qquad
 \|W_{R,m}\|_6^6
 ={5\over2m^6}\|R\|_6^{12}.
 \tag{4.5}
\]

For the Dirichlet polynomial,

\[
 \|D_m\|_6^6
 ={11m^5+5m^3+4m\over20},
 \tag{4.6}
\]

and therefore

\[
 \|W_{D,m}\|_6
 =\left[{5\over2m^6}
 \left({11m^5+5m^3+4m\over20}\right)^2\right]^{1/6}
 \asymp m^{2/3}.
 \tag{4.7}
\]

For Rudin--Shapiro, (4.3), \(\|P_m\|_2^2=m\), and monotonicity of normalized
\(L^p\) norms give

\[
 (5/2)^{1/6}\le\|W_{P,m}\|_6\le40^{1/6}.
\tag{4.8}
\]

All active frequencies lie in one fixed-ratio annulus \(|k|\asymp N\).
The single-annulus heat estimate should therefore give

\[
 cN^{-1/2}\|W_{R,m}\|_6
 \le\|W_{R,m}\|_{\mathfrak X}
 \le CN^{-1/2}\|W_{R,m}\|_6.
 \tag{4.9}
\]

Combining (4.7)--(4.9),

\[
 \|W_{D,m}\|_{\mathfrak X}\asymp N^{-1/2}m^{2/3},
 \qquad
 \|W_{P,m}\|_{\mathfrak X}\asymp N^{-1/2}.
 \tag{4.10}
\]

Thus the ratio grows like \(m^{2/3}\), although shell scale, support,
coefficient magnitudes, and \(L^2\) norm agree exactly.

Finally put

\[
 \alpha_m=N^{1/2}m^{-2/3}=\sqrt8\,m^{-1/6}.
 \tag{4.11}
\]

Then both matched inputs satisfy \(\|\alpha_mW_{R,m}\|_2\to0\), while

\[
 \|\alpha_mW_{D,m}\|_{\mathfrak X}\asymp1,
 \qquad
 \|\alpha_mW_{P,m}\|_{\mathfrak X}\asymp m^{-2/3}\to0.
 \tag{4.12}
\]

This would prove that \(L^2\), maximum frequency, modal count, Fourier
support, and coefficient magnitudes do not determine entry into a small
heat-flow ball.  Phase coherence is an independent datum.

## 5. Exact dynamical boundary of the matched family

Every field in (4.4) has the form \(e_3g(x_1,x_2)\).  Hence

\[
 (W_{R,m}\cdot\nabla)W_{R,m}=0.
 \tag{5.1}
\]

Its Navier--Stokes evolution is exactly the linear heat flow and is globally
smooth.  Therefore the coherent sequence in (4.12), despite failing to
enter a small \(\mathfrak X\) ball, is not an unsafe sequence.  The example
tests the sharp information needed by this sufficient entrance only; it
does not show singularity, instability, or necessity of the R0.73Q norm.

## 6. Audit checklist

- Prove the periodic annular heat multiplier in (2.1) and the inverse
  multiplier in (2.6), uniformly in shell index and time.
- Check the low-shell convention and constants when the smooth LP supports
  overlap.
- Recompute (3.2) and the component-safe identity (3.5), and verify Fourier
  normalization.
- Prove the vector-valued modal-count constant in (3.4) without hiding a
  dependence on shell geometry.
- Independently count the Dirichlet sixth moment in (4.6).
- Verify the carrier cancellation and constants \(1/2\) and \(5/16\) behind
  (4.5).
- Prove both sides of the single-annulus heat equivalence (4.9).
- Check that the matched support lies inside one fixed-ratio annulus and
  intersects only a uniformly bounded number of the declared smooth LP
  shells.
- Search the primary literature for the same shellwise autocorrelation
  formulation and the same Dirichlet/Rudin--Shapiro divergence-free pair.
- Keep (1.3) labeled as a periodic Besov/heat-flow estimate, not as a new
  Navier--Stokes regularity theorem.
- Keep the exact phase-sensitive convolution labeled as an exact evaluation
  of the shell \(L^6\) norm, not as a cheaper a priori estimate.  The
  multiplicity and support-count bounds are cheaper but phase-blind.

## 7. Exact exclusions

- No arbitrary \(L^2\)-small global regularity result.
- No necessity of the shell budget.
- No implication from failure of the budget to blow-up or instability.
- No nonperturbative \(BMO^{-1}\) uniqueness claim.
- No novelty or priority claim.
- No arbitrary three-dimensional global regularity or Clay conclusion.
