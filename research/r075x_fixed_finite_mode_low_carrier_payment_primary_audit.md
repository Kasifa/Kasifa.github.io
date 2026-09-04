# R0.75X primary mathematical audit

## Verdict

- Current verdict: **PASS**.
- Mathematical blocker count: **0**.
- Release blocker count: **0**.
- Scope: the analytic low-carrier theorem for every fixed finite real
  harmonic family in one dyadic band.
- Audited main SHA-256:
  `8e0c412528578c15d807b33b64f0996e62a2dabe2ebd58fa297f67c093929763`.

## 1. Quantifiers and claim audit

The theorem first fixes `q>=1`.  Its constant may depend on `q`, `C_0`,
and the frozen profiles, but is independent of `R`, the distinct integer
frequencies, amplitudes, phases, and constant shear speed.  The statement
assumes

`1<=n_1<...<n_q<=2n_1` and `n_1aR<C_0`.

These conditions imply `0<alpha_1<...<alpha_q<=2C_0`.  No lower frequency
gap is assumed.  The theorem is not uniform when `q=q(L)` and makes no
high-carrier claim for `q>=3`.

The amplitude/phase representation covers every real trigonometric
polynomial with the listed positive frequencies, including zero
coefficients.  The proof never divides by an amplitude, so those boundary
cases cause no loss.

## 2. Scaling audit

The substitutions

`t=R^2s`, `x_2=aRz`, `alpha_j=n_jaR`, and `v=BR/a`

give

`G_s+vG_z-a^(-2)G_zz=0`.

For the frozen cross-sectional derivative,

`D_R(aRz)aR dz=aR^2W_a(z)dz`.

Since `BR^2=avR`, the physical flux prefactor is exactly
`a^2R^3v/2`.  The plateau fibre has area
`4*pi*a*delta_0*R^2`; multiplication by `dt=R^2ds` and
`dx_2=aRdz` gives `4*pi*delta_0*a^2R^5H`.

Therefore

`a^2R^3(M/(a^2R^5))^(2/3)
 =a^(2/3)R^(-1/3)M^(2/3)`.

The normalization multiplies by `omega/R` and substitutes
`M=R^2omega^(-1)p`, cancelling every power of `R` and leaving
`a^(2/3)omega^(1/3)p^(2/3)`.  Its frozen logarithmic rate is
`-c_gamma/12=-2/11907`.

## 3. Companion-matrix observation audit

Expanding

`prod_j(D^2+alpha_j^2)`

gives

`D^(2q)+sigma_1D^(2q-2)+...+sigma_q`.

For the state ordered as `(g,g',...,g^(2q-1))`, the companion matrix final
row is

`(-sigma_q,0,-sigma_(q-1),0,...,-sigma_1,0)`.

Every coefficient is continuous on the compact parameter cube
`[0,K]^q`, including repeated and zero parameters.  The contradiction
proof normalizes the complete `2q`-jet at one point, not the original
Fourier coefficients.  This is essential: near colliding frequencies the
Fourier coefficients may diverge while the function converges to a
polynomial-times-exponential generalized solution.

If the local `L^3(I)` norm tends to zero along normalized jets, compactness
gives a limiting parameter vector and a nonzero limiting jet.  Uniform ODE
dependence gives convergence on the required compact interval.  The first
component of the limiting solution vanishes on the interval `I`; hence its
complete jet vanishes at an interior point.  ODE uniqueness contradicts
the normalized nonzero jet.  Uniform propagation then controls `g` and
`g'` on `J`.

This proves the precise fixed-`q` estimate used later.  It includes the
fully confluent polynomial space of degree at most `2q-1` and introduces no
inverse gap.

## 4. Temporal trace audit

At fixed `z`, each real harmonic contributes two complex exponentials in
`s`.  Thus there are at most `2q` terms, with exponents

`-alpha_j^2/a^2 +/- i alpha_jv`.

The real parts are uniformly bounded by `4C_0^2` when `a>=1`; the
imaginary parts are unrestricted because `B` is unrestricted.  Nazarov's
measurable-set inequality has the required dependence on term count and
real parts and has no imaginary-frequency or gap penalty.

For `I_Q=int_0^4|Q|^3`, the complement of
`E={|Q|^3<=I_Q/2}` has measure at most two.  Hence `|E|>=2` and
`sup_E|Q|<=(I_Q/2)^(1/3)`.  Substitution gives
`|Q(4)|^3<=C_qI_Q`.  Pointwise application in `z` followed by Fubini gives
`h(4)<=C_qH`.

Coincident exponents reduce the number of distinct terms.  No division by
an exponent gap occurs.  The argument is uniform for `v=0` and unbounded
`|v|`.

## 5. Kernel and local-energy sign audit

The radial kernel `W_a` is odd, so its primitive `Xi_a` is compactly
supported.  Direct rescaling of the two transition intervals gives

`||W_a||_1+||Xi_a||_1+||Xi_a||_infinity<=C`

and `||Xi_a''||_1<=Ca`.  Since `a>=1`, the `a^(-2)` heat factor absorbs
the only growing kernel norm.

For `Q=G^2`, the scalar equation gives

`Q_s+vQ_z-a^(-2)Q_zz=-2a^(-2)|G_z|^2`.

With `W_a=Xi_a'`, integration by parts produces

`v int W_aG^2=E'-a^(-2)int Xi_a''G^2
 +2a^(-2)int Xi_a|G_z|^2`.

After time integration, the terminal row is positive, the cutoff derivative
row negative, the `Xi_a''` row negative, and the localized gradient row
positive.  The proof bounds all rows only after forming the exact identity;
it does not discard a term by sign.

The spatial observation controls both `G` and `G_z` on `supp Xi_a` by
`C_qh^(1/3)`.  The kernel norms therefore bound every nonterminal row by
`C_qint h^(2/3)`, and Holder on `[0,4]` gives `C_qH^(2/3)`.  The terminal
row is paid by the separate temporal trace.

## 6. Degeneracy audit

- `B=0`: the original flux vanishes; the energy identity remains exact.
- unbounded `|B|`: only imaginary temporal frequencies grow, and the trace
  constant is unchanged.
- colliding scaled frequencies: the full-jet compactness includes repeated
  characteristic roots.
- all scaled frequencies tending to zero: the closure is the degree
  `2q-1` polynomial space.
- zero amplitudes: the number of active terms decreases and no division is
  used.
- high-order centre cancellation: it is retained in the complete jet rather
  than replaced by a two-mode defect.

## 7. Dependence on `q`

The temporal trace displays an at-most-exponential factor in `q` for the
chosen half-measure set.  The spatial compactness proof gives a finite
constant for fixed `q` but no quantitative growth estimate.  Accordingly,
the theorem is valid for each fixed `q` and its strict `L^2` exponent is
unchanged, but it cannot be applied uniformly to a packet whose number of
modes grows with `L`.

This boundary is necessary.  The frozen R0.75R construction already shows
that a growing high-band packet may concentrate in an outer cap and defeat
plateau-only cubic payment.  X neither contradicts nor repairs that
obstruction.

## 8. Source, evidence, and figure boundary

The source report checks Nazarov's original record and the
Friedland--Yomdin primary restatement.  Only the frequency-gap-free
exponential-polynomial estimate is imported.  The companion-matrix lemma,
energy identity, and scale conversion are proved in the main note.

Finite exact arithmetic can verify companion coefficients, identity signs,
and scale exponents.  It is not represented as proof of the continuum ODE
compactness lemma or the Turan--Nazarov theorem.

No formal figure is required.  A plot would not verify the uniform
fixed-`q` compactness argument, and no simulation result enters the claim.

## 9. Final boundary

R0.75X proves only the low-carrier theorem for each fixed finite real
harmonic family.  Quantitative `q` growth, high carriers for three or more
modes, arbitrary packets, nonconstant shear, arbitrary-field E.24,
Version-M extraction, suitable-weak transfer, regularity, and singularity
remain open.  The exact constant-background shear is not promoted to the
frozen mean-zero Version-M subclass.  **NOT CLAY.**
