# R0.73S primary-literature audit

**Search date:** 2026-08-31

**Status:** targeted collision search complete; broad-search stop rule fired

**Question:** are the quadratic-autocorrelation (L^6) bound, the
difference-support exponent, or the Rudin--Shapiro moment inputs new?

## 1. Direct collision results

### 1.1 Finite-spectrum Nikolskii inequality

Nessel and Wilmes prove a Nikolskii inequality for trigonometric polynomials
with finite spectral support.  Their Theorem 1, printed page 9, equation
(2.3), gives, in the relevant range,

\[
 \|t\|_q
 \le |\operatorname{supp}\widehat t|^{1/p-1/q}\|t\|_p.
\]

Taking (t=|f|^2), (p=2), and (q=3) gives directly

\[
 \|f\|_6\le
 |\operatorname{supp}\widehat{|f|^2}|^{1/12}\|f\|_4.
\]

This is a complete collision.  The inequality is classical and cannot be
described as an R0.73S theorem.

- R. J. Nessel and G. Wilmes, *Nikolskii-type inequalities for
  trigonometric polynomials and entire functions of exponential type*,
  J. Austral. Math. Soc. 25 (1978), 7--18,
  [DOI](https://doi.org/10.1017/S1446788700038878),
  [official PDF](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/A8F27E1D551391BC9CE87515035AAD55/S1446788700038878a.pdf/nikolskiitype_inequalities_for_trigonometric_polynomials_and_entire_functions_of_exponential_type.pdf).
- Historical source chain: S. M. Nikol'skii, *Inequalities for entire
  functions of finite degree and their application in the theory of
  differentiable functions of several variables*, Trudy Mat. Inst. Steklov.
  38 (1951), 244--278,
  [MathNet record and scan](https://www.mathnet.ru/eng/tm1119).

### 1.2 Wiener-autocorrelation endpoint form

With (C=\widehat{|f|^2}), the proposed estimate

\[
 \|f\|_6^6\le\|C\|_1\|C\|_2^2
\]

is a three-line consequence of Hölder, the absolute Fourier-series bound,
and Parseval.  Equivalently, constant-one Hausdorff--Young followed by

\[
 \|C\|_{3/2}^3\le\|C\|_1\|C\|_2^2
\]

gives the same result.  Edwards supplies the compact-Abelian-group
Hausdorff--Young setting.  No separately named historical theorem with the
exact displayed packaging was needed: the proof mechanism itself is a
complete classical collision.

- R. E. Edwards, *Inequalities related to those of Hausdorff--Young*, Bull.
  Austral. Math. Soc. 6 (1972), 185--210,
  [DOI](https://doi.org/10.1017/S0004972700044427),
  [official PDF](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/4CDBCE8560E6EB270EF8A9B30014B26A/S0004972700044427a.pdf/inequalities-related-to-those-of-hausdorff-young.pdf).

### 1.3 Additive-energy identity

The identities

\[
 \|f\|_4^4=\|a*a\|_2^2,
 \qquad
 \|f\|_6^6=\|a*a*a\|_2^2
\]

are standard Fourier orthogonality statements: fourth and sixth moments are
the fourfold and sixfold additive energies.  Ben Green's author notes state
the general (2k)-energy identity on printed pages 69--70.

- B. Green, *Additive Combinatorics*,
  [author manuscript](https://people.maths.ox.ac.uk/greenbj/papers/additive-combinatorics.pdf).

The (L^4) statistic is also the (U^2) Fourier statistic on a finite
group.  (U^3), however, is an eight-vertex cube average and is not the
sixth moment.  R0.73S must not identify (L^6) with (U^3).

- T. Tao, *254B Notes 3: Linear patterns*, Exercise 18,
  [author notes](https://terrytao.wordpress.com/2010/04/23/254b-notes-3-linear-patterns/).

## 2. Rudin--Shapiro collision ledger

Rudin's 1959 paper gives the recursive construction and the flatness
identity

\[
 |P_m(z)|^2+|Q_m(z)|^2=2^{m+1}.
\]

- W. Rudin, *Some Theorems on Fourier Coefficients*, Proc. Amer. Math. Soc.
  10 (1959), 855--859,
  [official AMS scan](https://www.ams.org/journals/proc/1959-010-06/S0002-9939-1959-0116184-5/S0002-9939-1959-0116184-5.pdf),
  [DOI](https://doi.org/10.1090/S0002-9939-1959-0116184-5).

Høholdt, Jensen, and Justesen give the exact aperiodic autocorrelation square
sum and merit factor.  For (N=2^m), their result implies

\[
 \|P_m\|_4^4={4N^2-(-1)^mN\over3},
 \qquad
 F_m={3\over1-(-1/2)^m}\longrightarrow3.
\]

- T. Høholdt, H. E. Jensen, and J. Justesen, *Aperiodic Correlations and the
  Merit Factor of a Class of Binary Sequences*, IEEE Trans. Inform. Theory
  31 (1985), 549--552,
  [DOI](https://doi.org/10.1109/TIT.1985.1057071).

Doche and Habsieger compute exact low even moments, including

\[
 \|P_m\|_6^6=2\cdot8^m-(-4)^m.
\]

Rodgers later proves the full fixed-moment limiting distribution.  Thus
neither the exact (L^4), the exact (L^6), nor their asymptotic behavior
is an R0.73S novelty slot.

- C. Doche and L. Habsieger, *Moments of the Rudin--Shapiro Polynomials*,
  J. Fourier Anal. Appl. 10 (2004), 497--505,
  [DOI](https://doi.org/10.1007/s00041-004-3049-y).
- B. Rodgers, *On the distribution of Rudin--Shapiro polynomials and
  lacunary walks on SU(2)*, Adv. Math. 320 (2017), 993--1008,
  [DOI](https://doi.org/10.1016/j.aim.2017.09.022),
  [arXiv](https://arxiv.org/abs/1606.01637).
- J.-P. Allouche, S. Choi, A. Denise, T. Erdélyi, and B. Saffari, *Bounds
  on Autocorrelation Coefficients of Rudin--Shapiro Polynomials*, Anal.
  Math. 45 (2019), 705--726,
  [arXiv](https://arxiv.org/abs/1901.06832).

## 3. Exact novelty boundary

The following are classical and excluded from novelty claims:

- the (L^2\to L^q) finite-spectrum Nikolskii inequality;
- the Wiener/Parseval/Hölder autocorrelation bound;
- fourth and sixth moments as additive energies;
- Rudin--Shapiro construction, flatness, merit factor, (L^4), and (L^6)
  moments.

The local work that remains valid as an R0.73S contribution is narrower:

1. the exact normalization inside the R0.73R critical heat-flow shell
   budget;
2. the selected-shift magnitude-tail certificate;
3. a real, mean-zero, divergence-free fixed-annulus family proving the
   (D_C^{1/2}) obstruction at fixed quartic concentration;
4. an exact low-summary indistinguishability pair and its lacunary
   amplification;
5. the verified transfer to the matched R0.73R Dirichlet/Rudin--Shapiro
   fields.

These are presented as a quantitative synthesis and a reproducible no-go
architecture.  The bounded search did not test every possible historical
repackaging, so absence of the identical package is not a priority proof.

## 4. Discovery stop rule

The broad-search stop rule has fired.  The exact inequality, its
finite-spectrum specialization, additive-energy interpretation, and all
Rudin--Shapiro moment inputs have direct primary-source collisions.  Further
search is limited to a concrete theorem number, formula, or priority risk
raised by final readback.
