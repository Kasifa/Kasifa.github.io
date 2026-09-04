# R0.76B primary mathematical audit

## Verdict

- Current verdict: **PASS**.
- Mathematical blocker count: **0**.
- Release blocker count: **0**.
- Scope: the analytic signed collar-flux estimate for each fixed finite real
  dyadic harmonic family under `n_1R<=1`.
- Audited main SHA-256:
  `a8a4cc853ec1029cb52afee724a4a783da156bd57de5399c58a7f42e2ab0306d`.

## 1. Quantifier and branch audit

The theorem fixes `q` before taking the frozen large-`L` regime and explicitly
quantifies `n_1,...,n_q in N` and `phi_j in R`.  Its constant may depend on
`q` and the frozen profiles, but not on `R`, the integer frequencies,
amplitudes, phases, or constant speed `B`.  The dyadic condition is
`n_q<=2n_1`, and the new physical carrier condition is `n_1R<=1`.

Set `alpha=n_1aR`.  The range splits without a gap:

- `alpha<8q` is R0.75X with its fixed constant `C_0=8q`;
- `8q<=alpha<=a` is proved in R0.76B;
- the equality `alpha=8q` belongs to the new branch;
- `alpha<=a` is algebraically equivalent to `n_1R<=1`.

For every fixed `q`, `a=pL` is eventually large enough for the frozen collar
support and for the high branch.  No conclusion uniform in `q=q(L)` is made.

## 2. Carrier-scaled value observation

At a fixed time the real field is an exponential polynomial with at most
`2q` complex terms and spatial exponents `+-i kappa_j`.  Under
`x=alpha z`, those exponents become `+-i r_j`, where `1<=r_j<=2`.

The scaling identity is

`int_(alpha I)|f|^3 dx = alpha int_I|g|^3 dz = alpha h_g`.

Therefore the subset on which `|f|^3<=2h_g` has measure at least
`alpha/2`.  The ambient interval `alpha J^+` has length `4alpha`, so the
length-to-subset ratio is at most eight.  Turan--Nazarov has no real-part
penalty here because the spatial exponents are purely imaginary, and its
power is at most `2q-1`.  This proves the value half of B.15 independently of
`alpha`, the carrier locations, or their gaps.

Zero amplitudes only reduce the number of active terms.  Frequency collisions
are not present for any fixed integer family, but the estimate remains stable
as scaled frequencies approach each other because no gap denominator occurs.

## 3. Local derivative observation

After carrier scaling, the field satisfies a constant-coefficient ODE of
order at most `2q` whose roots lie in the compact set `+-i[1,2]`.  To include
families with fewer than `q` active modes, one may multiply the annihilating
operator by repeated factors; this embeds them in the same compact order-`2q`
companion family.

For each companion matrix and initial jet, solution evaluation on a fixed
double unit window depends continuously on both.  If no uniform inverse bound
from the first-component `L^infinity` norm to the complete initial jet existed,
there would be a convergent sequence of parameters and unit jets whose first
components tend uniformly to zero.  The limiting solution would vanish on an
interval, so its full jet would vanish by ODE uniqueness, contradicting the
unit limiting jet.  The resulting jet bound controls the first derivative on
the concentric unit window.

The distance from `alpha J` to the boundary of `alpha J^+` is `alpha/2`.
Since the new branch has `alpha>=8q>=8`, every required double unit window is
contained in `alpha J^+`.  Returning to `z` contributes exactly one factor
`alpha` to the derivative.  This proves B.20--B.21 with no hidden carrier or
gap dependence.

## 4. Complete-clock trace

At fixed `z`, every cosine contributes two temporal exponential terms with
exponents

`-kappa_j^2/a^2 +/- i kappa_jv`.

The dyadic band and `alpha<=a` give `kappa_j<=2a`, hence the absolute real
parts are at most four.  The imaginary parts may be arbitrarily large because
`B` is unrestricted; Turan--Nazarov is uniform in those imaginary parts.

If `I_Q=int_0^4|Q|^3`, the set
`{|Q|^3<=I_Q/2}` has measure at least two.  Applying the measurable-set
estimate on `[0,4]` and then integrating the pointwise result over `z in I`
gives `h(4)<=C_qH`.  There is no exponent-gap division and no dependence on
`v`.

## 5. Full-real-field energy audit

The decisive object is the complete real field `G`, not an isolated analytic
cluster density.  Since `G` solves the scalar transport-diffusion equation,
its square satisfies

`(G^2)_s+v(G^2)_z-a^(-2)(G^2)_zz=-2a^(-2)|G_z|^2`.

With `W_a=Xi_a'`, two spatial integrations by parts give

`v int W_aG^2=E'-a^(-2)int Xi_a''G^2
 +2a^(-2)int Xi_a|G_z|^2`.

The terminal row is positive, the cutoff derivative row negative, the
`Xi_a''` row negative, and the localized gradient row positive.  No row is
dropped by sign.  The onset condition `zeta(0)=0` removes the initial endpoint
exactly.

The value observation pays `E` and the `Xi_a''` row; the latter uses
`||Xi_a''||_1<=Ca`, leaving the harmless factor `a^(-1)`.  The derivative
observation pays the last row with factor

`a^(-2) alpha^2 = (alpha/a)^2 <= 1`.

Holder on the fixed clock pays the three time-integrated rows, while the
terminal trace pays `E(4)`.  Thus the full dimensionless flux is bounded by
`C_qH^(2/3)`.

This argument reassembles all self, difference-frequency, sum-frequency, and
cross-group terms inside `G^2` before taking absolute values.  It neither
asserts positivity of the localized envelope current nor estimates the
original `W_a`-weighted carrier block by a standalone `1/alpha` integration
by parts.  The R0.76A sign counterexample and the sharp failure of that
standalone carrier-block method therefore do not apply to B.29--B.35.

## 6. Physical scaling audit

The cross-sectional rescaling gives the exact flux prefactor
`a^2R^3v/2`.  The plateau fibre has area
`4*pi*a*delta_0*R^2`; multiplication by `dt=R^2ds` and
`dx_2=aRdz` gives `4*pi*delta_0*a^2R^5H`.

Consequently,

`a^2R^3(M/(a^2R^5))^(2/3)
 =a^(2/3)R^(-1/3)M^(2/3)`.

Multiplication by `omega/R` and substitution
`M=R^2omega^(-1)p` cancel every power of `R` and leave
`a^(2/3)omega^(1/3)p^(2/3)`.  The frozen logarithmic rate is
`-c_gamma/12=-2/11907`.

## 7. Degeneracy and adversarial cases

- `B=0`: the flux vanishes, and the undivided identity remains valid.
- unbounded `|B|`: only imaginary temporal frequencies grow.
- zero amplitudes: the active dimension decreases.
- nearly colliding frequencies: both observation arguments remain gap-free.
- high spatial cancellation: Turan--Nazarov propagates value from a
  half-measure subset and the compact ODE controls the derivative.
- `alpha=a`: the gradient factor is exactly one and remains admissible.
- `alpha=8q`: the high branch includes the endpoint.
- `n_1R>1`: the proof loses `(alpha/a)^2<=1` and makes no claim.

An analytic-density decomposition may expose a positive full-gradient row
that is not separately controlled by an envelope estimate.  That is not the
present proof: the real scalar equation is applied to the entire `G` once,
and B.21 directly controls its actual derivative.

## 8. Source and evidence boundary

The source report verifies Nazarov's original record and the
Friedland--Yomdin primary restatement.  Only the measurable-set exponential-
polynomial inequality is imported.  The local derivative lemma, the energy
identity, and the scale conversion are proved in the main note.  Adjacent
Bernstein/Markov literature is context only.

Finite exact arithmetic can verify the branch endpoint, scaled frequencies,
real-part bound, window geometry, one pointwise PDE identity, and all scale
exponents.  It is not represented as proof of Turan--Nazarov or of the
continuum compactness lemma.

No formal figure is required.  A simulation cannot certify the uniform
measurable-set or companion-ODE statements, and no simulation result enters
the theorem.

## 9. Final boundary

R0.76B proves only a fixed-finite-dimensional exact-shear theorem through the
inverse-radius carrier scale.  It does not provide a quantitative constant
for growing `q`, an ultra-high-carrier estimate, arbitrary-packet control,
projection from a larger velocity, arbitrary-field E.24, Version-M
extraction, suitable-weak transfer, regularity, or singularity.  The exact
constant-background shear is not promoted to the frozen mean-zero Version-M
subclass.  No completeness, novelty, or priority claim is made.
**NOT CLAY.**
