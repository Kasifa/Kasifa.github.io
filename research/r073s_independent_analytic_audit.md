# R0.73S independent analytic audit

**Result:** pass, with one strengthened embedding and two mandatory no-go
boundaries

## 1. Reconstructed upper certificate

Using normalized Haar measure, an independent convolution derivation starts
from (g=|f|^2), (C=\widehat g), and obtains

\[
 \|f\|_6^6
 =\langle C*C,C\rangle
 \le\|C\|_1\|C\|_2^2.
\]

The same reconstruction confirms

\[
 \|C\|_2^2=\|f\|_4^4,
 \qquad
 \|C\|_1\le ME^2,
 \qquad
 \|C\|_1\le\sqrt{D_C}\|C\|_2.
\]

All constants are one.  The first inequality has equality for the real
mean-zero divergence-free field

\[
 f(x)=(0,\cos x_1,\sin x_1),
\]

since (|f|\equiv1).

## 2. Sharpness reconstruction

For the Dirichlet-spike family with (x=m^{-1/2}), the independent algebra
gives

\[
 \Gamma_m
 ={5\over3}+2m^{-1/2}-3m^{-1}+{1\over3m^2},
\]

and

\[
\begin{aligned}
 \Theta_m={}&{11\over20}m^{1/2}+7-{15\over m}
 +{33\over4}m^{-3/2}+3m^{-2}\\
 &-3m^{-5/2}+{1\over5}m^{-7/2}.
\end{aligned}
\]

The exact autocorrelation support has (D_C=4m-1).  Retuning the positive
root of

\[
 (A_m-3)x^2+2x-{2\over3}=0
\]

fixes (Gamma=5/3) exactly while retaining
(Theta\sim(11/20)\sqrt m).  Therefore the (D_C^{1/2}) exponent is
unavoidable without a continuity assumption.

## 3. Strengthened real embedding

The initial scalar-to-real lift can be improved.  Take (N=3m), (K=32m),

\[
 H_m=e^{iKx_1}F_m(x_1),
 \qquad
 V_m=(0,\Re H_m,\Im H_m).
\]

Then (|V_m|=|F_m|) pointwise, so (E,Gamma,Theta,D_C) are preserved
exactly rather than up to carrier constants.  Its positive frequencies are
(32m) and (35m,\ldots,36m-1), with conjugates at the negatives.  Hence

\[
 32m\le|k|<36m,
 \quad M=2m+2,
 \quad D_\Delta=10m-1.
\]

The field is real, mean zero, divergence free, and
(V_m\cdot\nabla V_m=0).

## 4. Mandatory no-go boundaries

First, a triangular autocorrelation tail may satisfy

\[
 \|q\|_2^2\to0
 \quad\hbox{while}\quad
 \sum_{h+k+\ell=0}q_hq_kq_\ell\to\infty.
\]

Thus an (\ell^2)-tail-only selected-shift certificate cannot suppress the
(sqrt{D_{\rm tail}}) factor.

Second, the exact seed pair

\[
 A=1-z-z^2-z^3+z^4,
 \qquad B=1-z-z^2-z^3-z^4
\]

has common (L^2) and (L^4), but sixth moments (311) and (323).
Base-(q\ge14) lacunary products amplify the (L^6) ratio without changing
support or coefficient magnitudes.  This disproves constant-factor recovery
from those low-order summaries.

The complete autocorrelation is not covered by this no-go: it still
determines the sixth moment exactly.

## 5. Matched-family readback

For the R0.73R fields,

\[
 M=2m^2,
 \qquad D_\Delta=3(2m-1)^2.
\]

The Dirichlet branch has

\[
 A_D=2m^2,
 \quad
 Q_D={(2m^2+1)^2\over6m^2},
\]

so (A_DQ_D\asymp m^4), the correct power.  The dyadic
Rudin--Shapiro branch has

\[
 Q_P={(4m-(-1)^r)^2\over6m^2}=O(1),
\]

and (A_P=O(m)) from the difference-support bound.  After the common
R0.73R scaling, the quadratic proxy is order one for Dirichlet and
(O(m^{-1/2})) for Rudin--Shapiro.

## 6. Audit conclusion

The mathematics is internally correct under the frozen normalization.  The
release must say “quadratic interaction-order certificate,” not “universally
faster algorithm.”  It must also retain the safe-shear, sufficient-only,
fixed-orbit, and non-Clay exclusions.
