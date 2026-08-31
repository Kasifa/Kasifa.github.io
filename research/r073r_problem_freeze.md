# R0.73R problem freeze: what an energy spectrum cannot certify

**Frozen date:** 2026-08-31

**Domain:** the normalized periodic torus \(\mathbb T^3=[0,2\pi]^3\),
viscosity one, and real mean-zero divergence-free data

**Dependency:** the R0.73Q sufficient stability tube measured by

\[
 \|f\|_{\mathfrak X}
 :=\|e^{t\Delta}f\|_{L^4((0,\infty);L^6)}.
\]

## 1. Frozen question

R0.73Q gives a sufficient entrance but does not say which Fourier data are
enough to evaluate or upper-bound it.  R0.73R asks four bounded questions.

1. What shell sequence is exactly equivalent to \(\mathfrak X\)?
2. Which deterministic finite Fourier summaries give certified upper bounds?
3. Can two fields with the same support, coefficient magnitudes, \(L^2\), and
   every quadratic Sobolev norm have very different \(\mathfrak X\) norms?
4. What part of this interface is classical, what is an internal exact
   derivation, and what remains open?

The target is a computable entrance certificate around the same fixed a
priori global orbit as R0.73Q.  It is not a new arbitrary-data regularity
criterion.

## 2. Frozen notation

Fix one smooth periodic Littlewood--Paley decomposition \((P_j)_{j\ge0}\)
on the nonzero frequencies and put

\[
 f_j=P_jf,\qquad E_j=\|f_j\|_2,\qquad b_j=\|f_j\|_6,
\]

\[
 \Theta_j={b_j^6\over E_j^6}\quad(E_j>0),
 \qquad
 \mathcal C_{\rm sh}(f)
 =\left(\sum_j2^{-2j}\Theta_j^{2/3}E_j^4\right)^{1/4}.
\]

The exact Fourier diagnostic is the linear triple convolution representing
\(|f_j|^2f_j\).  Two phase-blind upper summaries are

\[
 M_j=|\operatorname{supp}\widehat f_j|
\]

and

\[
 R_j=\max_n\#\{(k_1,k_2,k_3)\in S_j^3:
                   k_1+k_2+k_3=n\}.
\]

## 3. Frozen candidate conclusions

The analytic gate may close only if the following statements survive an
independent reconstruction.

\[
 \|f\|_{\mathfrak X}\asymp\mathcal C_{\rm sh}(f)
 =\left(\sum_j2^{-2j}\|P_jf\|_6^4\right)^{1/4},
\]

\[
 \|f\|_{\mathfrak X}
 \lesssim\left(\sum_j2^{-2j}R_j^{2/3}E_j^4\right)^{1/4}
 \le
 C\left(\sum_j2^{-2j}M_j^{4/3}E_j^4\right)^{1/4}.
\]

The matched Dirichlet/Rudin--Shapiro construction must have identical
Fourier support and coefficient magnitudes, while its heat traces have ratio
\(\asymp m^{2/3}\).  After the common amplitude
\(\alpha_m=\sqrt8\,m^{-1/6}\), both \(L^2\) norms vanish, the coherent heat
trace stays of order one, and the Rudin--Shapiro heat trace vanishes like
\(m^{-2/3}\).

## 4. Literature exclusions fixed before publication

The following are treated as established or classical neighborhoods, not as
R0.73R novelty:

- negative-index heat-semigroup and Littlewood--Paley Besov
  characterizations;
- finite-support Bernstein/Nikolskii inequalities and \(\Lambda(p)\) theory;
- Rudin--Shapiro flatness and random-sign Khintchine improvement;
- refined Sobolev and spectral-cluster \(L^p\) estimates;
- high-frequency or oscillatory large-data Navier--Stokes constructions.

The exact divergence-free matched packaging was not found in the bounded
search, but absence from that search is not a novelty proof.

## 5. Exact exclusions

R0.73R will not claim:

- a bound of \(\mathfrak X\) by \(L^2\) alone;
- necessity of the R0.73Q sufficient entrance;
- instability, blow-up, or singularity when the entrance fails;
- a new periodic Besov characterization;
- a first sparse-spectrum, random-phase, or oscillatory-data theorem;
- a result for an arbitrary unknown reference orbit;
- arbitrary three-dimensional Navier--Stokes global regularity;
- any resolution or partial resolution of the Clay Millennium problem.

The matched fields have zero nonlinear term and are globally smooth exact
heat flows.  That fact must accompany every public interpretation of the
separation.
