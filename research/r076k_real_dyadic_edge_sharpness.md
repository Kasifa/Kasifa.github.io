# R0.76K -- real dyadic sharpness of the reconstructed edge scale

## 0. Result and exact boundary

R0.76J proves a bilateral edge estimate for arbitrary real-frequency
complex exponential sums and inserts it into the exact-shear full-plateau
upper bound.  This note asks the next necessary question: does the
Chebyshev factor `exp(Cq sqrt(d))` survive the reality, conjugacy, dyadic
band, integer-mode, and heat-shear restrictions of the benchmark, or is it
only an artefact of the larger complex class?

The answer is affirmative at a prescribed spatial-time slice.  Define the
real one-dyadic-band class

\[
 \mathcal R_q^{\rm dyad}:=\left\{
 g(t)=\sum_{j=0}^{q-1}A_j\cos(\nu_jt-\phi_j):
 A_j>0,\quad 0<\nu_0<\cdots<\nu_{q-1}\le2\nu_0
 \right\}.
 \tag{K.1}
\]

For every integer `q>=2` and `0<d<=1`,

\[
 \boxed{
 \sup_{0\ne g\in\mathcal R_q^{\rm dyad}}
 \frac{|g(1+d)|}{\|g\|_{L^2[-1,1]}}
 \ge \frac1{2\sqrt2}
 \exp\!\left((q-1)\operatorname {arcosh}(1+d)\right)
 \ge \frac1{2\sqrt2}e^{(q-1)\sqrt d}.}
 \tag{K.2}
\]

The same class satisfies the exterior-transfer lower bound

\[
 \boxed{
 \sup_{0\ne g\in\mathcal R_q^{\rm dyad}}
 \frac{\displaystyle\int_1^{1+d}|g(t)|^2dt}
      {\displaystyle\int_{-1}^1|g(t)|^2dt}
 \ge \frac d{128}
 \exp\!\left(2(q-1)\sqrt{\frac{7d}{8}}\right).}
 \tag{K.3}
\]

At the endpoint `d=0`,

\[
 \boxed{
 \sup_{0\ne g\in\mathcal R_q^{\rm dyad}}
 \frac{|g(1)|}{\|g\|_{L^2[-1,1]}}
 \ge\frac q{\sqrt2}.}
 \tag{K.4}
\]

Thus both indispensable pieces of the R0.76J pointwise scale are genuine
inside the real dyadic class: linear endpoint growth in the `L2` norm and
exponential near-edge growth of order `exp(cq sqrt(d))`.  Since a real
`q`-cosine packet has `2q` complex exponential branches, R0.76J correctly
uses `N<=2q`.  Here `q` counts positive cosine modes; K.2 is proved by
realification, not by an inclusion `R_q^dyad subset T_q`.  Zhang's separate
complex `T_q` lower bound is recorded in Proposition 7.1 of the cited v1.

There is also an exact integer heat-shear realization at any one prescribed
scaled time.  It shows that the spatial lower witnesses are not excluded by
the exact Navier--Stokes shear equations.  It does not prove that the same
profile persists over the complete clock, nor that the complete signed
collar flux divided by full plateau mass attains this lower scale.  Those
are separate spacetime and sign questions.  **NOT CLAY.**

## 1. Confluent polynomial-to-Fourier map

Let `p` be a real polynomial of exact degree `n=q-1`,

\[
 p(y)=\sum_{r=0}^na_ry^r,\qquad a_n\ne0,
 \tag{K.5}
\]

and, for `epsilon>0`, put

\[
 w_\epsilon(t):=\frac{e^{i\epsilon t}-1}{i\epsilon},
 \qquad h_\epsilon(t):=p(w_\epsilon(t)).
 \tag{K.6}
\]

Expanding either the powers in K.5 or the Taylor polynomial of `p` at
`i/epsilon` gives

\[
 h_\epsilon(t)=\sum_{j=0}^nb_j(\epsilon)e^{ij\epsilon t},
 \qquad
 b_j(\epsilon)
 =\sum_{r=j}^na_r(i\epsilon)^{-r}(-1)^{r-j}{r\choose j}
 =\frac{p^{(j)}(i/\epsilon)}{j!(i\epsilon)^j}.
 \tag{K.7}
\]

For each `j`,

\[
 (i\epsilon)^n b_j(\epsilon)
 \longrightarrow
 a_n(-1)^{n-j}{n\choose j}\ne0
 \qquad(\epsilon\downarrow0).
 \tag{K.8}
\]

Consequently all `q` coefficients are nonzero once `epsilon` is
sufficiently small.  This qualification is necessary: exact polynomial
degree alone does not make every `b_j(epsilon)` nonzero for every positive
`epsilon`.

Fix `M>0` and `theta in R`, and realify the polynomial by

\[
 \begin{aligned}
 g_{\epsilon,M,\theta}(t)
 &:=2\operatorname {Re}\left[
 e^{i\theta}e^{iMt}h_\epsilon(t)\right]\\
 &=\sum_{j=0}^n2|b_j(\epsilon)|
 \cos\!\left((M+j\epsilon)t+\theta+\arg b_j(\epsilon)\right).
 \end{aligned}
 \tag{K.9}
\]

If `n epsilon<=M`, its `q` positive frequencies lie in `[M,2M]` and
the negative frequencies are exactly their conjugates.  Hence K.9 belongs
to `R_q^dyad` for every sufficiently small strict choice
`n epsilon<M`; the closed endpoint in K.1 also covers equality.

For every fixed compact real interval, the elementary estimate

\[
 |w_\epsilon(t)-t|
 \le\frac{\epsilon t^2}{2}
 \tag{K.10}
\]

and continuity of the fixed polynomial imply

\[
 g_{\epsilon,M,\theta}(t)
 \longrightarrow
 2p(t)\cos(Mt+\theta)
 \tag{K.11}
\]

uniformly.  The lower results are therefore supremum statements witnessed
by a confluent sequence; no claim is made that the supremum is attained.

## 2. Chebyshev pointwise lower bound

Fix `0<d<=1`, choose

\[
 p=T_n,\qquad M=1,\qquad\theta=-(1+d),
 \tag{K.12}
\]

and let `epsilon` tend to zero through values with `n epsilon<1`.  Since
the limiting carrier is exactly one at `t=1+d`, K.11 gives

\[
 \lim_{\epsilon\downarrow0}
 |g_{\epsilon,1,-(1+d)}(1+d)|=2T_n(1+d),
 \qquad
 \lim_{\epsilon\downarrow0}
 \|g_{\epsilon,1,-(1+d)}\|_2
 =\|2T_n(t)\cos(t-(1+d))\|_2
 \le2\|T_n\|_2.
 \tag{K.13}
\]

Here and below unlabelled norms are over `[-1,1]`.  Since

\[
 \|T_n\|_2\le\sqrt2,
 \qquad
 T_n(1+d)=\cosh\!\left(n\operatorname {arcosh}(1+d)\right)
 \ge\frac12e^{n\operatorname {arcosh}(1+d)},
 \tag{K.14}
\]

the first inequality in K.2 follows.  For `0<=d<=1`, the elementary
comparison

\[
 \operatorname {arcosh}(1+d)\ge\sqrt d
 \tag{K.15}
\]

gives the second.  The range in K.15 is recorded explicitly; no all-`d`
version of this particular simplification is used.

## 3. One witness for the full exterior interval

Use the same choices K.12 and set

\[
 J_d:=\left[1+\frac{7d}{8},1+d\right].
 \tag{K.16}
\]

For every `t in J_d`,

\[
 |t-(1+d)|\le\frac d8\le\frac18,
 \qquad \cos^2(t-(1+d))\ge\frac12.
 \tag{K.17}
\]

The fixed lowest carrier `M=1` is essential here.  Merely aligning an
arbitrarily large carrier at `1+d` would permit rapid oscillation inside
`J_d` and would not prove K.17.

Chebyshev monotonicity on `[1,infinity)` and K.15 give

\[
 T_n(t)^2
 \ge\frac14
 \exp\!\left(2n\sqrt{\frac{7d}{8}}\right)
 \qquad(t\in J_d).
 \tag{K.18}
\]

The limiting profile `g_0(t)=2T_n(t)cos(t-(1+d))` therefore obeys

\[
 \int_1^{1+d}|g_0(t)|^2dt
 \ge\frac d{16}
 \exp\!\left(2n\sqrt{\frac{7d}{8}}\right),
 \qquad
 \int_{-1}^1|g_0(t)|^2dt\le8.
 \tag{K.19}
\]

Uniform convergence on `[-1,1+d]` passes both integrals to the limit and
proves K.3.  The same argument also gives, with a no-worse constant,

\[
 \sup_{0\ne g\in\mathcal R_q^{\rm dyad}}
 \frac{\displaystyle\int_1^{1+d}|g(t)|^2dt}
      {\left(\displaystyle\int_{-1}^1|g(t)|^3dt\right)^{2/3}}
 \ge \frac d{128}
 \exp\!\left(2(q-1)\sqrt{\frac{7d}{8}}\right),
 \tag{K.20}
\]

because `int_[-1,1]|g_0|^3<=16` and `16^(2/3)<8`.  Equation K.20 is the
norm pairing appearing in the spatial observation row of the plateau
proof.  It is still a fixed-time statement, not a flux theorem.

## 4. The endpoint polynomial factor

Let `P_m` be the Legendre polynomial normalized by `P_m(1)=1`, and use the
degree-`n` Christoffel kernel

\[
 p_n^*(t):=\sum_{m=0}^n\frac{2m+1}{2}P_m(t).
 \tag{K.21}
\]

Legendre orthogonality gives

\[
 p_n^*(1)=\frac{(n+1)^2}{2}=\frac{q^2}{2},
 \qquad
 \|p_n^*\|_2^2=\frac{(n+1)^2}{2}=\frac{q^2}{2}.
 \tag{K.22}
\]

Apply K.6--K.11 with `p=p_n^*` and choose `theta=-M`, so the limiting
carrier equals one at `t=1`.  Then

\[
 \limsup_{\epsilon\downarrow0}
 \frac{|g_{\epsilon,M,-M}(1)|}
      {\|g_{\epsilon,M,-M}\|_2}
 \ge\frac{p_n^*(1)}{\|p_n^*\|_2}
 =\frac q{\sqrt2},
 \tag{K.23}
\]

which proves K.4.

For comparison with the `L3` central payment, `|P_m(t)|<=1` on
`[-1,1]`, so `||p_n^*||_infinity<=q^2/2`.  Consequently

\[
 \|p_n^*\|_3^3
 \le\|p_n^*\|_\infty\|p_n^*\|_2^2
 \le\frac{q^4}{4},
 \qquad
 \sup_{g\in\mathcal R_q^{\rm dyad}}
 \frac{|g(1)|}{\|g\|_3}
 \ge2^{-1/3}q^{2/3}.
 \tag{K.24}
\]

After squaring, K.24 forces at least a `2^(-2/3)q^(4/3)` same-endpoint
factor for a universal `L3`-to-pointwise estimate.  It does not prove that
R0.76J's squared `q^2` factor is optimal for the `L3` pairing; the interval
between `q^(4/3)` and `q^2` remains open.

## 5. Exact integer heat-shear slice realization

Retain the R0.76J scaling

\[
 a=\frac{32}{63}L,\qquad R=e^{-\rho L^2/4},\quad\rho>0,\qquad
 e_a=1-\frac{\delta_0}{a},\qquad
 E_a=[-e_a,e_a],\qquad \eta_L=e_aaR,\qquad v=\frac{BR}{a},
 \tag{K.25}
\]

and the exact real shear

\[
 F(t,x_2)=\sum_{j=0}^{q-1}A_j e^{-n_j^2t}
 \cos(n_jx_2-\phi_j-n_jBt),
 \qquad u=(0,B,F(t,x_2)).
 \tag{K.26}
\]

For a prescribed scaled time `s_*`, put
`G(s,z)=F(R^2s,aRz)`.  Choose consecutive integers

\[
 n_j=n_0+j,\qquad n_0\ge\max\{1,q-1\},
 \qquad M_L=n_0\eta_L,
 \tag{K.27}
\]

and expand `p(w_(eta_L)(x))=sum_(j=0)^(q-1)b_j(eta_L)e^(ij eta_L x)`
as in K.7.  Whenever these coefficients are nonzero, define

\[
 A_j=2|b_j(\eta_L)|e^{n_j^2R^2s_*},
 \qquad
 \phi_j\equiv-\theta-\arg b_j(\eta_L)-n_jBR^2s_*
 \pmod{2\pi}.
 \tag{K.28}
\]

Direct substitution, with `x=z/e_a`, gives the exact identity

\[
 \boxed{
 G(s_*,e_ax)=2\operatorname {Re}\left[
 e^{i\theta}e^{iM_Lx}
 p\!\left(\frac{e^{i\eta_Lx}-1}{i\eta_L}\right)
 \right].}
 \tag{K.29}
\]

Thus the heat damping at one specified time is exactly prepaid by the
positive amplitudes in K.28, and the transport phase is exactly prepaid by
the real phases.  The quantifier is: for every prescribed `s_*` and `B`
there exists such a packet.  It is not one packet that realizes K.29 at
every time.

Since `n_(q-1)<=2n_0` in K.27, the physical integer frequencies lie in one
dyadic band.  For each fixed `q`, K.8 and `eta_L->0` ensure that all
coefficients are nonzero for large `L`.  Choosing

\[
 n_0(L)=\left\lceil\frac M{\eta_L}\right\rceil
 \tag{K.30}
\]

for fixed `M>0` also gives `M_L->M`, so K.29 converges uniformly on compact
real intervals to `2p(x)cos(Mx+theta)`.

There is a conservative uniform version when the degree grows.  If
`0<eta_L<=1/8` and `|x|<=2`, then K.10 gives

\[
 |w_{\eta_L}(x)-x|\le2\eta_L,
 \tag{K.31}
\]

and the segment between the two arguments lies in `|z|<=9/4`.  The
Chebyshev and Legendre recurrences give the coefficient bounds

\[
 \sum|\operatorname {coeff}(T_m)|\le(1+\sqrt2)^m,
 \qquad
 \sum|\operatorname {coeff}(P_m)|\le(1+\sqrt2)^m.
 \tag{K.32}
\]

Since `(9/4)(1+sqrt(2))<6`, the complex mean-value estimate yields

\[
 \begin{aligned}
 \sup_{|x|\le2}|T_{q-1}(w_{\eta_L}(x))-T_{q-1}(x)|
 &\le C\eta_Lq6^q,\\
 \sup_{|x|\le2}|p_q(w_{\eta_L}(x))-p_q(x)|
 &\le C\eta_Lq^26^q,
 \end{aligned}
 \tag{K.33}
\]

where the normalized endpoint polynomial is

\[
 p_q(x):=\frac1q\sum_{m=0}^{q-1}\frac{2m+1}{2}P_m(x).
 \tag{K.34}
\]

The same recurrences and the leading terms in K.8 show that all transformed
coefficients are nonzero eventually under the sufficient condition

\[
 \boxed{\eta_Lq(L)^27^{q(L)}\longrightarrow0.}
 \tag{K.35}
\]

Indeed, after multiplying K.7 by `(i eta_L)^(q-1)`, the sum of all
lower-degree terms is bounded by `C eta_L q 5^q`, whereas the Chebyshev
leading coefficient is at least `2^(q-2)`.  For the normalized Legendre
kernel K.34, its leading coefficient is explicitly

\[
 a_{q-1}(p_q)=\frac{2q-1}{2q}\,2^{-(q-1)}
 {2q-2\choose q-1}\ge\frac34.
 \tag{K.36}
\]

Condition K.35 makes each remainder smaller than its nonzero leading term
uniformly in `j`.  It also implies `eta_L q->0`, so the choice
`n_0=ceil(1/eta_L)` satisfies `n_0>=q-1` eventually.

Because

\[
 \eta_L=(a-\delta_0)R
 =\operatorname {poly}(L)e^{-\rho L^2/4},
 \tag{K.37}
\]

every integer-valued `q(L)=o(L^2)` satisfies K.35.  More generally it is
enough that

\[
 \limsup_{L\to\infty}\frac{q(L)}{L^2}
 <\frac{\rho}{4\log7}.
 \tag{K.38}
\]

Choose `n_0=ceil(1/eta_L)` and align `theta_L=-M_L(1+d)` for the
Chebyshev witness.  Equations K.29 and K.33 then prove the same endpoint
and exterior exponential orders inside exact integer heat-shear slices
throughout `q=o(L^2)`.  With the normalized K.34, they also prove the
linear endpoint order there.  The coarse sufficient condition does not
cover the full R0.76J upper window `q=o(L^(5/2))`; this is a limitation of
the present uniform approximation proof, not a counterexample beyond
`o(L^2)`.  No fixed-time identity by itself controls the complete clock.

The coordinate change also records the exact observation normalization:

\[
 \frac{|G(s_*,e_a(1+d))|}
      {\|G(s_*,\cdot)\|_{L^2(E_a)}}
 =e_a^{-1/2}
 \frac{|G(s_*,e_a(1+d))|}
      {\|G(s_*,e_a\,\cdot)\|_{L^2[-1,1]}}.
 \tag{K.39}
\]

## 6. Why the complete flux does not follow

Equation K.29 closes a class-membership question, not the spacetime lower
bound.  Away from `s_*`, the exact coefficients acquire unequal factors

\[
 e^{-n_j^2R^2(s-s_*)}
 \quad\hbox{and}\quad
 e^{-in_jBR^2(s-s_*)}.
 \tag{K.40}
\]

Reality and the two-cap sign do not by themselves force cancellation at
the selected slice.  Put `m=q-1` and write

\[
 A:=a-\delta_0,\qquad e_a=\frac Aa,\qquad
 d_p:=\frac{2\delta_0}{A},\qquad
 d_c^-:=\frac{r_c-h+\delta_0}{A},
 \tag{K.41}
\]

where the frozen positive subcap has
`delta_0<r_c-3h<r_c+3h<delta` and
`vartheta(r)>=c_vartheta>0` for `|r-r_c|<=3h`.  The full physical plateau projects into
`|x|<=1+d_p`.  For every paired collar point define

\[
 x_r:=\frac{a+r}{A},\qquad r\in[r_c-h,r_c+h],
 \tag{K.42}
\]

first on the displayed subcap; the same definition is used on all
`r in supp(vartheta) subset (-delta,delta)`.  On the subcap,
`x_r>=1+d_c^-`.  Hence

\[
 \begin{aligned}
 \Gamma_m
 &:=m\left[\operatorname {arcosh}(1+d_c^-)
           -\operatorname {arcosh}(1+d_p)\right]>0\\
 &=\frac m{\sqrt A}
 \left(\sqrt{2(r_c-h+\delta_0)}-2\sqrt{\delta_0}\right)
 +O\!\left(\frac m{A^{3/2}}\right).
 \end{aligned}
 \tag{K.43}
\]

For the ideal real profile

\[
 U_m(x):=2T_m(x)\cos\!\left(x-\frac\pi4\right),
 \tag{K.44}
\]

Chebyshev parity gives the exact paired identity

\[
 U_m(x_r)^2-U_m(-x_r)^2
 =4\sin(2x_r)T_m(x_r)^2
 \ge cT_m(x_r)^2
 \tag{K.45}
\]

for all sufficiently large `a`, uniformly on the entire fixed support of
`vartheta`, because there `x_r=1+O(1/a)` and `sin(2x_r)` stays positive.
The two values of `W_a` have equal magnitudes and opposite signs.  Choose
a fixed `v<0`, equivalently `B=va/R`.  Then every paired slice contribution
is nonnegative, while the chosen subcap supplies a uniform positive weight
and the exponent in K.43.
Combining K.43--K.45 with the full-plateau projection shows an
`exp(2 Gamma_m)` contrast, up to polynomial factors, between the signed cap
slice and the two-thirds power of the full-plateau spatial `L3` density.
For `q=o(L^2)`, K.29 and K.33--K.35 transfer the ideal profile uniformly
to the sufficiently-large-`L` exact integer slice, so its paired integral
has the same strict sign and exponential order.  This closes the signed
single-slice algebra only.

The exact dynamics explain why the clock cannot be filled by continuity
alone.  If `tau=s-s_*`, `D=partial_x`, and the complex half of K.29 is
denoted by `mathcal H_eta`, then direct heat-semigroup conjugation gives

\[
 \begin{aligned}
 \mathcal H_\eta(\tau,x)
 &=e^{i\theta-M_L^2\tau/A^2
       +iM_L(x-v\tau/e_a)}\\
 &\quad\times
 \left(e^{\tau A^{-2}D^2}h_\eta\right)
 \left(x-\frac{v\tau}{e_a}
       +\frac{2iM_L\tau}{A^2}\right).
 \end{aligned}
 \tag{K.46}
\]

Therefore nearly equal modal heat rates do not preserve the high-order
cancellation: in the confluent limit for fixed `m`, the polynomial becomes
`e^(tau A^(-2)D^2)T_m`, not `T_m` times a common scalar.  A concrete
backward-heat warning is already exact.  For `m=2n` and fixed `T>0`,

\[
 T_{2n}(x)=n\sum_{k=0}^n
 (-1)^{n-k}\frac{(n+k-1)!}{(n-k)!(2k)!}(2x)^{2k}.
 \tag{K.47}
\]

Termwise differentiation therefore gives

\[
 \begin{aligned}
 \left|\left(e^{-(T/A^2)D^2}T_{2n}\right)(0)\right|
 &=\sum_{j=0}^n
 \frac{n(n+j-1)!}{(n-j)!}\,
 \frac{(4T/A^2)^j}{j!}\\
 &\ge\exp\!\left(cT\frac{m^2}{A^2}\right)
 \qquad(m=o(A^2)).
 \end{aligned}
 \tag{K.48}
\]

All terms in K.48 have the same sign before the absolute value.  For
`j<=n/2`, the factorial coefficient before `(4T/A^2)^j/j!` is at least
`(n/2)^(2j)`.  With `X=Tn^2/A^2`, the sum therefore dominates
`sum_(j<=n/2)X^j/j!`.  The condition `m=o(A^2)` gives `X=o(n)`; the term
`j=floor(X)` and Stirling's bound, with `1+X` used when `X<1`, prove the
last line of K.48 for an absolute `c>0`.

In the overlapping range `A^(3/2)<<m=o(A^2)`, the proved backward cost
`m^2/A^2` is already larger
than the cap gap `Gamma_m=O(m/sqrt(A))`.  A terminal realization therefore
cannot be extended backward for free.  Even granting a terminal slab of
width comparable with `A/m^2`, whose logarithmic measure loss would be only
polynomial, one would still have neither a plateau-mass bound on the rest
of `[0,4]` nor an exclusion of oppositely signed contribution outside the
slab.  A complete lower bound
for the physical quotient would additionally have to prove all of the
following with one packet:

1. persistence on a time slab of positive, quantitatively controlled
   width;
2. favourable dominance after integration against the signed two-cap
   weight `W_a` and the frozen clock cutoff;
3. control by the full three-dimensional plateau mass, including fibres
   adjacent to the favourable cap;
4. preservation of the claimed exponent after physical normalization.

R0.76G--H show why the third item cannot be skipped: a packet may be
exponentially large relative to a central fibre while the adjacent full
plateau absorbs that contrast.  Until the four items close together,
K.2--K.4 and K.20 must not be advertised as sharpness of J.6 or of the
complete signed collar flux.

## 7. Claim boundary

**LITERATURE:** the Chebyshev confluent sequence and complex-class lower
bound are explicitly attributed to Ruizhe Zhang's 2026 arXiv v1
Proposition 7.1; Legendre orthogonality and `|P_m|<=1` on `[-1,1]` are
standard classical facts.

**PROVED LOCALLY:** the nonvanishing coefficient limit K.8; real
conjugate-paired dyadic construction K.9; pointwise and integrated lower
bounds K.2--K.3 and K.20; endpoint polynomial lower bounds K.4 and K.24;
the exact integer heat-shear slice identity K.29; and the conservative
varying-degree range K.31--K.39; signed two-cap slice identity K.41--K.45;
and the exact heat evolution and backward-growth warning K.46--K.48.

**FINITE COMPUTATION:** certificates may audit coefficient expansions,
sample dyadic indices, constants, phase signs, rational inequalities,
dependency hashes, and equation/reference inventories.  They cannot prove
uniform convergence, classical orthogonality, or the continuum supremum
statements.

**OPEN:** a quantitative slice range beyond K.35; persistence of the
Chebyshev witness over a
terminal slab; a matching lower bound for the complete signed flux divided
by full plateau mass; the optimal `L3` endpoint power between K.24 and the
J upper bound; multiple bands; nonconstant shear; arbitrary nonlinear
packets; arbitrary-field E.24; Version-M extraction; fixed deletion;
suitable-weak transfer; regularity; and singularity.

No simulation or formal scientific figure is needed for this analytic
result.  No novelty or priority claim is made.  It is a sharp class and
single-slice theorem for exact real shears, not a solution of the
millennium problem.  **NOT CLAY.**
