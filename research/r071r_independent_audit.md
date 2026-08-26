# R0.71R independent audit

**Audit date:** 2026-08-26  
**Checker:** `research/r071r_independent_audit.py`  
**Independence boundary:** the checker imports neither the exact producer nor
any earlier release code.

## 1. Reconstructed statements

The independent checker reconstructs four finite statements:

1. for sampled scalar contraction semigroups, Duhamel's endpoint ratio

   \[
    \frac{|\int_0^he^{-a(h-s)}G(s)\,ds|^2}
    {h\int_0^h|G(s)|^2\,ds}
   \]

   is at most one;
2. scaling an even-touch observable by \(2^{-m}\) leaves its declared entry
   mass one and scales its source energy by \(4^{-m}\);
3. the scaled genuine NSE initial Fourier jet retains \(A_+=a^2/4\) while
   its \(\rho=2\) Taylor-jet surrogate grows like \(K^2\);
4. the squared-root polynomial family has \(N\) positive quadratic jets and,
   after an independently reconstructed normalization, source energy one;
5. the multi-component family has \(Q\) distinct positive quadratic entries
   and summed source energy below three.

The polynomial producer in the exact certificate integrates rational
coefficients exactly.  The independent checker instead evaluates the
sequential family by 2,048-point Gauss--Legendre quadrature and reconstructs
the component family with NumPy polynomial algebra.

## 2. Numerical boundary

The Duhamel test uses seed `71073`, 200,001 time samples per case, four
damping rates, and four window heights.  It is a corroborating numerical test,
not the proof of the semigroup inequality.  The proof is Cauchy--Schwarz after
the contraction estimate.

The high-degree polynomial test evaluates products at Gauss nodes instead of
expanded monomial coefficients.  This avoids a false loss of significance
near clustered rational roots.  Positivity of every quadratic leading
coefficient is evaluated from the product of squared root separations.

The frequency-jet checker independently reconstructs

\[
 Y=a^2K^2,
 \quad \|F\|_2^2=a^4K^2/4,
 \quad \|C_t\|_2^2=a^4K^6,
 \quad \langle F,C_t\rangle=a^4K^4/2.
\]

It audits only the exact initial jet and the resulting first-jet scaling
coefficient.  It does not time-step the Navier--Stokes equation.

## 3. Result boundary

The exact and independent certificates agree on the following method verdict:

- a quadratic forced-parabolic source budget can be normalized independently
  of the number of degree-zero positive-entry atoms in the abstract families;
- therefore a uniform lower incidence charge is additional dynamical content;
- the minimal Leray-matched \(\rho=2\) charge has a \(K^2\) Taylor-jet
  pressure, without a positive-time lower-bound claim;
- none of the numerical families is an NSE trajectory or an infinite-frame
  counterexample.

No time-stepped NSE simulation, fitted model, interval-arithmetic proof,
continuation theorem, singularity result, or global-regularity claim is part of
this audit.
