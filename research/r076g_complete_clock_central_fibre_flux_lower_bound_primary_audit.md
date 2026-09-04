# R0.76G primary analytic audit

## Verdict and audited scope

- Current verdict: **PASS**.
- Mathematical blocker count: **0**.
- Release blocker count: **0**.
- Scope: the complete-clock signed-flux lower bound against the central
  fibre, its exact NSE realization, and the non-transfer boundary for the
  full physical plateau.

This audit does not authorize publication.  The final certificate binds the
hashes after an independent reread.

## 1. Clock and sign audit

R0.75B defines the absolute interval from `61R^2` to `65R^2`, with the
cutoff equal to one on `(64R^2,65R^2)`.  After the explicit translation in
G.10, the terminal identity is `zeta=1` on `(3,4)`.  It is not inferred from
the weaker onset row in R0.76C--E.

The scaled cross-section is
`W_a(z)=-2pi a z vartheta(a(|z|-1))`.  Hence it is negative on the positive
cap and positive on the negative cap.  Since `v=-beta`, the positive cap is
favourable.  G.33 estimates the only adverse cap before the signed
contributions are combined.  No absolute value is placed around the full
flux in G.34.

## 2. Spectral and NSE audit

The envelope `(2sin(y/2))^(2m)` has exactly the integer frequencies
`-m,...,m`, all nonzero as coefficients.  Multiplication by `cos(3my)`
produces the disjoint supports `[-4m,-2m]` and `[2m,4m]`.  Therefore the real
field has exactly `q=2m+1` positive frequencies, with first `2m`, last `4m`,
and exact dyadic equality `4m=2(2m)`.  There is no zero mode or collision.

For `u=(0,B,F(x_2))`, divergence vanishes and the nonlinear term is
`(0,0,B partial_2 F)`.  Equation G.17 therefore gives a smooth unforced
three-dimensional Navier--Stokes solution with constant pressure.

## 3. Gaussian lemma audit

The heat-kernel formula G.20 follows from the exact periodic Gaussian
representation; the periodic datum permits using a real Gaussian without a
separate image sum.  Minkowski and
`(E|Z|^(2m))^(1/(2m))<=sqrt(2m)` give the allowance `4sqrt(m)/a` exactly
when `s<=4`.

For the lower row, on `|X|<=3` the sine ratio error is
`O(m epsilon^2)` and the cosine error is `O((m epsilon)^2)`.  Both vanish
because `m<=a^2/1024`, `epsilon=aR`, and `R` is exponentially small in
`L^2`.  The tail calculation G.26 uses
`||X||_(4m)<=8/5+sqrt(32m)/a<9/5` and the Gaussian threshold
`3-8/5=7/5`.  Its exponent dominates the possible factor
`(6/5)^(2m)`.  Jensen then supplies the retained moment `w^(2m)`.  This
checks uniformity over the whole cap-time rectangle.

## 4. Constant and exponent audit

The central window has `|w|<=26/25`.  The moment allowance is at most
`1/8`, and `233/200<7/6`.  The positive cap has lower base `3/2`; the
negative cap has upper base at most `2/3` after imposing
`delta/a<=1/24`.  Here `supp vartheta subset (-delta,delta)` and, for large
`L`, `delta/a+4beta<1/2`; hence `w<0` on the negative cap and the drift can
only decrease `|w|`.  Thus the adverse-to-favourable ratio decays like
`(4/9)^(4m)` and is absorbed for large `L`.

Dividing the flux base `3/2` by the central base `7/6` gives `9/7`; the
square and the `2/3` cubic power both produce exponent `4m`.  Since
`a^2/L^2=1024/3969`,

\[
 \frac{q}{L^2}\to\frac2{3969},\qquad
 \frac{4m}{L^2}\to\frac4{3969}.
\]

The normalized rate is
`4log(9/7)/3969-2/11907`.  The elementary lower bound
`log(1+x)>x/(1+x)` at `x=2/7` makes it greater than the exact rational
`2/35721>0`.

## 5. Claim-boundary audit

The lower denominator in G.8 is `H_L`, and G.36 is explicitly labelled a
central-fibre proxy.  It is not the physical plateau mass.  G.39--G.40 show
why the full plateau sees a nearby cap fibre and why no implication to
R0.76E E.3 is valid.  The note does not claim a counterexample to E.24,
Version-M, regularity, or smoothness.  It makes no novelty or priority claim.
No simulation or formal figure is used.  **NOT CLAY.**
