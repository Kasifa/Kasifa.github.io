# R0.75V primary audit -- complete dyadic-pair signed-flux payment

## 0. Frozen objects and verdict

- Main note: `research/r075v_complete_two_harmonic_flux_payment.md`
- Audited main SHA-256:
  `6917ff77099b6271b005ca90335df589434a38b0a57001893dcae8b02fd34824`
- Source report: `research/r075v_report-source.md`
- Audited source SHA-256:
  `a099949ad6968468389b412e1d250c5e1a788ac046b949d4d69fbcf1501e9811`
- Current verdict: **PASS**
- Mathematical blocker count: **0**
- Release blocker count: **0**

This audit certifies V.3--V.4 only for the exact constant-coefficient heat
pair V.1 with `maR>=C_0`.  It does not certify low carriers, arbitrary
time-dependent damping, a Fourier projection of a larger velocity, or a
multimode packet theorem.

## 1. Exact integration-by-parts audit

For a self phase `theta(t)=theta_0+2kBt`,

\[
 B\sin\theta=-\frac1{2k}\frac d{dt}\cos\theta.
\]

Multiplication by the flux prefactor `J_(2k,R)/4` therefore gives boundary
and derivative coefficient

\[
 \frac{J_{2k,R}}{8k}=\frac14K_R(2k).
\]

For the sum phase, the corresponding coefficient is

\[
 \frac{J_{n,R}}{2n}=\frac12K_R(n).
\]

Thus the two self rows and the sum row combine with weights `1,1,2` inside
the common factor `1/4`.  Since `eta_R(0)=0`, only the right endpoint
survives.  Differentiating the amplitudes gives

\[
 (A_t^2)'=-2k^2A_t^2,
 \quad(C_t^2)'=-2m^2C_t^2,
 \quad(A_tC_t)'=-(k^2+m^2)A_tC_t.
\]

These identities reproduce V.27--V.28 with the stated signs and factors.
The integrations are performed before the common phase is factored, so no
spurious relative-phase derivative occurs.

## 2. Radial multiplier-jet audit

Scale `y=Rz` in the quotient `K_R(r)=J_(r,R)/r`.  Its even continuation at
zero can be represented by a compactly supported smooth amplitude and the
entire function `sin(rRz)/(rR)`.  The `j`-th `r` derivative contributes
`R^j` and a polynomial of degree at most `j+2` in `z`.  The support consists
of two intervals of fixed width centered at `+/-a`.  This gives

\[
 |\partial_r^jK_R(r)|
 \le C_{j,N}a^{j+2}R^{j+3}(1+rR)^{-N},
 \qquad j=0,1,2.
\]

For `n=k+m` and `d=k-m`, the dyadic condition gives

\[
 n-d=2m,\qquad n+d=2k,
 \qquad\frac23n\le n-d<n+d\le\frac43n.
\]

Taylor's theorem therefore retains both arbitrary high-frequency decay and
the first and second powers of `d aR`.  When `d aR>=1`, the direct bound
supplies the saturated version.  The carrier condition gives
`d/n<=(d aR)/(n aR)<=C min(1,d aR)`, so differentiation of the prefactor
`r^2/2` in `L_R` introduces no unrecorded loss.  This proves all rows of
V.16--V.17.

## 3. Quadratic cancellation audit

Let `u=A_t exp(i Delta_t/2)` and
`v=C_t exp(-i Delta_t/2)`.  Distance from `Delta_t` to the cancelling phase
`pi+2piZ` gives

\[
 |u+v|^2\lesssim(A_t-C_t)^2+A_tC_t\min\{1,\delta_t^2\}
 \le CH(t)^2.
\]

Also, with `epsilon=min(1,d aR)`,

\[
 \varepsilon^2(A_t+C_t)^2
 \le\varepsilon^2(A_t-C_t)^2+4\varepsilon^2A_tC_t
 \le CH(t)^2.
\]

The exact decomposition V.21 then has:

- a zeroth-order multiplier multiplying `(u+v)^2`;
- an even second multiplier difference multiplying `A_tC_t`;
- an odd first multiplier difference multiplying
  `(u-v)(u+v)`.

The jet factors are respectively `1,epsilon^2,epsilon`; every row is at
most `C Lambda H(t)^2`.  This proves V.22 without estimating either self
wave separately.

## 4. Heat quadratic-form audit

For `L_R(r)=r^2K_R(r)/2`, the self coefficients are exactly

\[
 L_R(2k)=2k^2K_R(2k),
 \qquad L_R(2m)=2m^2K_R(2m).
\]

The standard central cross coefficient from V.21 would be
`2L_R(n)A_tC_t=n^2K_R(n)A_tC_t`.  The actual coefficient is

\[
 2(k^2+m^2)K_R(n)A_tC_t
 =(n^2+d^2)K_R(n)A_tC_t.
\]

The difference is exactly `d^2K_R(n)A_tC_t`.  Because
`(d/n)^2A_tC_t<=CH(t)^2`, it has the same
`C n^2 Lambda_N H(t)^2` bound as the grouped `L_R` form.  In the formal
cancelling state `A=C`, `Delta=pi`, and constant `K`, the polynomial identity

\[
 \frac{(n+d)^2+(n-d)^2}{2}-(n^2+d^2)=0
\]

checks that the heat row has no hidden zeroth- or first-order residue.

## 5. Endpoint trace audit

After `t=R^2s`, the clock has length four.  The product of the two
amplitudes is no smaller at an earlier time than at the right endpoint.
The periodic phase distance is piecewise affine.  A backward unit interval
therefore has one of two alternatives:

1. the phase moves slowly, so a fixed portion retains the terminal defect;
2. the phase moves rapidly, so a fixed portion of one or more periods has a
   phase distance bounded below.

Direct cubic integration gives V.33 uniformly in the phase speed, including
zero speed and crossings of the cancelling phase.

For the amplitude mismatch, let `x,y` be the two terminal amplitudes and
`epsilon=min(1,d aR)`.  If `xy=0`, one amplitude vanishes on the whole
clock and the other is monotone under backward time, so the cubic lower
bound is immediate.  Suppose `xy>0`.  If
`|x-y|<=4epsilon sqrt(xy)`, the spatial beat term already pays the mismatch.
Otherwise the backward amplitude ratio starts a fixed relative distance
from one.  It is monotone, its logarithmic speed is `d n R^2`, and the
common heat rates are `O((nR)^2)`.  On a terminal interval of scaled length
`c(1+(nR)^2)^(-1)`, the ratio retains a fixed fraction of its terminal
distance from one and the mismatch remains comparable to `|x-y|`.  Cubing
and integrating gives V.35.  The phase and mismatch rows give V.36;
multiplication by `(1+nR)^(-8)` is more than sufficient for V.31.

The proof uses the exact forward decays `e^(-k^2t),e^(-m^2t)` and the right
endpoint of the complete clock.  It would not justify arbitrary
time-dependent damping or forward-growing amplitudes.

## 6. Final scale audit

Let `I_H=int H^3`.  Holder on the length-`4R^2` clock gives

\[
 \int H^2\le CR^{2/3}I_H^{2/3}.
\]

With `b_8=Ca^2R^3(1+nR)^(-8)`, the three rows in V.37 have scales

\[
 \begin{array}{c|c}
 \text{row}&\text{upper scale after V.30--V.31}\\
 \hline
 \text{right endpoint}&Ca^2R^{5/3}I_H^{2/3}\\
 \eta_R'&Ca^2R^3R^{-2}R^{2/3}I_H^{2/3}\\
 \text{heat}&Ca^2R^3n^2(1+nR)^{-8}R^{2/3}I_H^{2/3}.
 \end{array}
\]

The cutoff row is exactly `a^2R^(5/3)I_H^(2/3)`.  The heat row has the
additional bounded factor `(nR)^2(1+nR)^(-8)`.  T gives
`M^plat>=ca^2R^3I_H`; its `2/3` power leaves

\[
 a^2R^{5/3}(a^2R^3)^{-2/3}
 =a^{2/3}R^{-1/3}.
\]

This verifies V.3.  Adding only the already proved U block verifies V.4.
Substitution of `M=R^2omega^(-1)p` cancels every power of `R`, and the
frozen `c_gamma=8/3969` gives `-c_gamma/12=-2/11907`.

## 7. PDE, source, and claim audit

Each harmonic in V.1 solves the transported heat equation, so their finite
sum does.  For `u=(0,B,F(t,x_2))`, incompressibility and the componentwise
Navier--Stokes identity are direct.  The nonzero constant background is
expressly not claimed to lie in the frozen mean-zero, inversion-paired
Version-M subclass.

The source report binds primary neighboring records on exact shearing-wave
solutions, shear mixing, torus observability, and the official Clay problem.
None is imported into the multiplier-jet, endpoint, or flux proof.  The
search is bounded and establishes no novelty, completeness, or priority
claim.

The open boundary is accurate: low carriers, three or more modes, arbitrary
packets, arbitrary-field E.24, Version-M extraction, suitable-weak transfer,
regularity, and singularity remain open.  **NOT CLAY.**

## 8. Finite-check boundary

Finite checks may bind exact integration-by-parts coefficients, frequency
relations, multiplier-jet powers, scale arithmetic, source hashes, formula
tags, and mutation rejection.  Random endpoint scans may look for a
counterexample.  Neither finite algebra nor sampling is represented as proof
of V.13, V.31, or the continuum theorem V.3.
