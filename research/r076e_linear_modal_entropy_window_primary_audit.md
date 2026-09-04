# R0.76E primary mathematical and release audit

## 0. Verdict

- Current verdict: **PASS**.
- Mathematical blocker count: **0**.
- Release blocker count: **0**.
- Audited main note SHA-256:
  `1494cb7e3863ef934f87746412f2a64ef98f78deb5ce81be3cece7d5a7571ca4`.
- Audited source report SHA-256:
  `10e506fa9d250b14d9f42f6eac7c2c83cfca934a85a2da6e223cd473f21e0c12`.

The result is an analytic estimate for the stated finite exact-shear family
in one dyadic band.  It is not an arbitrary-field estimate and does not
prove regularity or exclude singularity.  **NOT CLAY.**

## 1. Imported theorem audit

### 1.1 Centered Turan--Nazarov tail

R0.76E imports R0.76D's centered estimate only in E.13.  Centering a sum
whose real exponents lie in `[-4,-1]` moves them into `[-3/2,3/2]`.
Turan--Nazarov on `[0,tau]` and a half-measure subset of `[0,1]` costs an
absolute base to order `N` and `(1+tau)^(N-1)`.  Multiplication back by the
centering weight leaves `exp(-tau)`.  Cubing, integrating in `z`, and raising
to `2/3` gives E.14 with `m=2(N-1)`.

No imaginary-frequency size, gap, or spectral-gap denominator enters this
step.  The explicit spatial derivative row E.10 remains the already audited
R0.76D consequence of Turan--Nazarov and Erdelyi's point derivative bound.

### 1.2 Last-unit endpoint

For each fixed `z`, Chebyshev selects a subset of `[T-1,T]` of measure at
least one half on which the cube is at most twice its last-unit integral.
Turan--Nazarov propagates this bound to the endpoint `T`.  The interval has
fixed length and the real parts remain in `[-4,-1]`, so every geometric and
real-part factor is absorbed in one absolute base `D_1^(3N)`.  Integration
in `z` proves E.19.  This is a corollary of the imported measurable-set
theorem, not a new half-line Nikolskii theorem.

## 2. Local delayed-split proof

### 2.1 One split works for every term count

Let `m=2(N-1)` and `S_N=C_0 N log(N+1)`.  The main note explicitly bounds
`log S_N` by a fixed multiple of `log(N+1)`.  Therefore the logarithm of

`D_0^(2N) 2^m S_N^(m+1) exp(-2S_N)`

is bounded by `N log(N+1)` times a bracket whose negative term is
`-2C_0`, while its only nonlinear positive dependence on `C_0` is
logarithmic.  One sufficiently large absolute `C_0` makes the bracket
nonpositive for every `N>=1` and also gives `S_N>=max(4,m+1)`.

### 2.2 Early and late intervals

On `[0,min(T,S_N)]`, Holder with exponents `3/2` and `3` gives

`int tau k^(2/3) <= K_T^(2/3) (int_0^S tau^3)^(1/3)`.

This is E.16 and uses the full observed mass rather than `K_1`.  On the late
interval, `(1+tau)^m<=2^m tau^m`.  Since
`tau^(m+1)exp(-tau)` decreases for `tau>=S_N`, its product with the remaining
`exp(-tau)` integrates to at most `S_N^(m+1)exp(-2S_N)`.  E.15 then proves
E.17.  Combining the two intervals gives the polynomial weighted loss in
E.18.

### 2.3 Endpoint without a factorial

If `4<=T<=S_N`, E.19 and `S_N/T>=1` give E.20.  The factor
`D_1^(2N)S_N^(2/3)` is at most `exp(CN)` because `C_0` is fixed and
`log S_N=O(log(N+1))`.

If `T>=S_N`, the function `T^(m+2/3)exp(-2T)` is decreasing.  The stronger
power `m+1` in E.15 bounds the endpoint by the full mass `K_T`.  These two
branches give E.22 for all `T>=4`, including `N=1`.

## 3. Carrier and energy ledgers

### 3.1 Heat-clock exponents

When `lambda>1`, the change `tau=lambda s` gives `T=4lambda` and
`K_T=lambda H`.  In the endpoint row,

`T^(-2/3) K_T^(2/3) = 4^(-2/3) H^(2/3)`.

In the onset row, the factors are

`lambda * lambda^(-1) * lambda^(-1) * lambda^(2/3)
= lambda^(-1/3)`.

Thus neither the terminal trace nor the weighted onset leaves a positive
carrier power.  The `lambda<=1` branch stays on the fixed original clock.

### 3.2 Complete-real identity

The note defines `zeta(s)=eta_R(R^2s)` before using `zeta'`.  It records
`zeta(0)=0`, `|zeta'|<=C_eta`, and `zeta(s)<=C_eta s`.  The transport
identity E.29 is formed for the complete real square before absolute values.
The spatial row gives

`a^(-2)(alpha+q)^2 <= C(lambda+q^2/a^2)`.

The endpoint estimate pays the terminal term, the weighted estimate pays
the `lambda` gradient term, and Holder pays the remaining integral terms.
Since `a>=1`, the last factor is at most `q^2`.  The spatial base,
`exp(Cq)` endpoint, and both polynomial factors are absorbed by one
`exp(C_*q)`.

The proof does not divide by the shear speed, so `B=0` remains covered.  It
does not use a density projection, localized-current sign, spectral-gap
division, or standalone carrier integration by parts.

## 4. Physical scale and asymptotic window

The flux prefactor is `a^2 R^3 v`, while the plateau mass contributes
`a^2 R^5 H`.  Substitution of `H^(2/3)` therefore gives

`a^(2/3) R^(-1/3) M^(2/3)`.

Multiplication by `omega/R` and substitution of
`p=R^(-2)omega M` cancel the remaining power of `R` and give E.4.  If
`q(L)=o(L^2)`, the modal term and `log a` vanish after division by `L^2`,
while `omega^(1/3)` contributes exactly `-2/11907`.

The new condition is genuinely weaker than the R0.76D condition.  For
example, a scale comparable with `L^2/log L` is `o(L^2)` but its product
with `log q` is not `o(L^2)`.

## 5. Adversarial boundary audit

The following cases were checked against the statement:

1. `N=1`, where `m=0` and the same split remains valid;
2. zero coefficients or repeated exponents after canonical combination;
3. colliding and arbitrarily large imaginary parts;
4. `T=S_N` and `lambda=1`, including consistent branch assignment;
5. arbitrarily large `lambda`, where the onset gains `lambda^(-1/3)`;
6. `B=0`, where the signed flux is zero without division by `B`;
7. growing `q`, with a constant explicitly exponential in `q`;
8. a projection of a larger field, which the note explicitly excludes; and
9. the R0.75R arbitrary-packet obstruction, whose mode scale and clock lie
   outside E.5.

No matching lower bound or sharpness result is claimed.

## 6. Source and release boundary

The source report separates imported continuum theorems from the local
delayed split.  Its bounded collision screen does not establish literature
completeness, novelty, priority, or sharpness.  Finite certificates may
check the split, branch, exponent, and scaling ledgers but are not proof of
Turan--Nazarov, Erdelyi, or the continuum flux theorem.

- E.1--E.34 occur once and in order.
- All 38 display blocks close; four explanatory or defining displays are
  intentionally unnumbered.
- Every internal E reference resolves.
- UTF-8, control-byte, CR, trailing-space, TeX-escape, and discouraged-phrase
  checks pass.
- No simulation or formal scientific figure is claimed for this analytic
  theorem.
- This is an ordinary note release, not a cumulative recap.

Subject to byte-binding by the dual exact certificate, the note is ready for
the sole FIFO publisher after all predecessor releases are online-verified.
