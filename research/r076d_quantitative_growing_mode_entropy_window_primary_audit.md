# R0.76D primary mathematical and release audit

## 0. Verdict

- Current verdict: **PASS**.
- Mathematical blocker count: **0**.
- Release blocker count: **0**.
- Audited main note SHA-256:
  `cd94e3384f01963cb7b8a14fdb8376c6197c361473447f15500db0acac5e958e`.
- Audited source report SHA-256:
  `f2358780d382dcace69b7ebef855bf3c8e63d15b581dc86b62b7e3c751fbd310`.

The result is an analytic estimate for the exact constant-shear family in
one dyadic band.  It is not a theorem for arbitrary Navier--Stokes fields and
does not prove regularity or exclude singularity.  **NOT CLAY.**

## 1. Imported theorem audit

### 1.1 Turan--Nazarov

The note uses the original positive-measure form for a complex exponential
polynomial.  On an interval `J` and a measurable subset `E`, the loss is an
absolute base to the power `N-1`, multiplied by the real-part factor.  There
is no dependence on the imaginary frequencies or their gaps.

In D.17 all exponents are purely imaginary.  The interval length is four and
the Chebyshev subset has measure at least one half, so the geometric ratio is
eight.  In D.21 the centered exponents have real parts in `[-3/2,3/2]`.
Applying the theorem on `[0,tau]` and multiplying back by
`exp(-5tau/2)` leaves `exp(-tau)`.  In D.27 the uncentered exponents have
nonpositive real parts, so the bounded-clock endpoint has no carrier factor.

### 1.2 Erdelyi point derivative inequality

The cited theorem applies to complex coefficients and ordered real
frequencies.  Combining repeated exponents and deleting zero coefficients
places D.14 in that class.  For `f(t)=g(z_0+t/2)`, the maximal rescaled
frequency is at most `alpha`; the theorem gives

`|f'(0)| <= (alpha+2e(N+1)) ||f||_infinity`.

Because `f'(0)=g'(z_0)/2` and `N<=2q`, the returned derivative costs only an
absolute multiple of `alpha+q`.  The observation interval lies inside
`J^+`.  No frequency-separation hypothesis has been inserted.

## 2. Local proof audit

### 2.1 Spatial row

Chebyshev gives a subset of `I` of measure at least one half on which
`|g|<=(2 h_g)^(1/3)`.  Turan--Nazarov propagates this value to `J^+` with
cost `D^(2q)`.  The derivative theorem then gives D.15 and D.19.  The
argument remains valid for `q=1`, fewer than `2q` active exponents, repeated
exponents after combination, arbitrarily small gaps, and arbitrarily large
imaginary frequencies.

### 2.2 Heat-tail row

Cubing the centered Turan--Nazarov estimate gives D.21.  Integration in `z`
is legitimate because its right side is nonnegative and measurable.  With
`m=2(N-1)`,

`2^m int_1^infinity tau^(m+1) exp(-2tau) dtau <= (m+1)!/4`.

For the endpoint, `T>=4` gives
`(1+T)^m <= (5/4)^m T^m`.  Multiplication by `T^(2/3)` and the global maximum
of `T^r exp(-2T)`, `r=m+2/3`, yields D.25--D.26.  Both losses are bounded by
`exp(CN log(N+1))`.  The proof also covers `N=1`.

### 2.3 Carrier split and endpoint

If `lambda<=1`, the original-clock real parts lie in `[-4,0]`, and D.27
pays the endpoint.  If `lambda>1`, the heat clock has `T=4lambda`,
`K_T=lambda H`, and real parts in `[-4,-1]`; the factors
`T^(-2/3)K_T^(2/3)` cancel exactly.  Neither branch depends on `v` or on
spectral gaps.

### 2.4 Complete-real energy row

The transport identity D.33 is taken before absolute values for the complete
real square.  The spatial derivative loss satisfies

`a^(-2)(alpha+q)^2 <= C(lambda+q^2/a^2)`.

For `lambda>1`, the cutoff onset `zeta(s)<=C_eta s` and the heat clock give
the exact exponent

`lambda * lambda^(-2) * (lambda H)^(2/3)=lambda^(-1/3)H^(2/3)`.

The remaining `q^2/a^2` factor is at most `q^2` because `a>=1`, and is
absorbed by `exp(Cq log(q+1))`.  The same exponential also absorbs all
`D^(cq)` factors.  The argument does not divide by `v`, so `B=0` is covered.

### 2.5 Physical and asymptotic rows

The flux factor is `a^2 R^3 v`; the plateau mass factor is `a^2 R^5 H`.
Replacing `H^(2/3)` therefore gives
`a^(2/3)R^(-1/3)M^(2/3)`.  Normalization cancels `R` and leaves
`a^(2/3)omega^(1/3)p^(2/3)`.  If
`q(L)log(q(L)+1)=o(L^2)`, both the modal-entropy term and `log a` vanish
after division by `L^2`, while `omega^(1/3)` contributes exactly
`-2/11907`.

## 3. Adversarial boundary audit

The following cases were checked against the stated hypotheses:

1. `q=1` and an active term count below the nominal maximum;
2. repeated or zero complex exponential terms after canonical reduction;
3. colliding or nearly colliding frequencies;
4. arbitrarily large carrier and transport imaginary parts;
5. `B=0`, where the signed flux vanishes without division by the speed;
6. `lambda=1`, assigned to the bounded branch;
7. `lambda` tending to infinity, where the onset clock gains
   `lambda^(-1/3)`;
8. growing `q`, for which the constant is explicitly not uniform; and
9. attempted application to a projection of a larger field, which the note
   explicitly forbids.

No case contradicts R0.75R.  That obstruction excludes a uniform
plateau-only statement for arbitrary growing packets; R0.76D retains an
explicit growing constant and stays inside the exact-shear family.

## 4. Source and claim boundary

The primary-source report identifies exactly two imported continuum inputs:
Nazarov's measurable-set inequality and Erdelyi's derivative inequality.
The factorial tail, clock split, energy payment, physical conversion, and
growing-mode corollary are local deductions.  The bounded collision screen
does not establish novelty, priority, sharpness, or literature completeness.

Finite certificates can check the exact factorial, branch, exponent, and
scale ledgers.  They are not proof of either imported continuum theorem or
of the analytic energy estimate.

## 5. Release audit

- D.1--D.41 occur once and in order; 41 display blocks close correctly.
- All internal D references resolve after the inserted endpoint comparison.
- UTF-8, control-byte, and TeX escape checks pass.
- The source ledger points to D.17, D.21, and D.27 for Turan--Nazarov,
  D.21--D.26 for the heat tail, D.32--D.39 with D.5 for the full collar
  constant, and D.40 for the frozen rate.
- No simulation or formal scientific figure is claimed for this analytic
  theorem.
- The required publication boundary is an ordinary note release, not a new
  cumulative recap.

Subject to byte-binding by the dual exact certificate, the note is ready for
the sole FIFO publisher after R0.76C is online-verified.
