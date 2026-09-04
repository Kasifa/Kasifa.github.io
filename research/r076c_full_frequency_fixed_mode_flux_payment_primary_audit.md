# R0.76C primary mathematical audit

## Verdict

- Current verdict: **PASS**.
- Mathematical blocker count: **0**.
- Release blocker count: **0**.
- Scope: the analytic signed collar-flux estimate for every carrier in each
  fixed finite real dyadic harmonic family.
- Audited main SHA-256:
  `2b2f4a2b353645e72ca54bfc06495a9f52329498b9c16a9e451ca7b3456f6bbf`.

## 1. Quantifier and branch audit

The theorem first fixes an integer `q>=1`.  It explicitly quantifies ordered
integer modes, real phases, nonnegative amplitudes, and arbitrary real
constant speed `B`.  The constant may depend on `q` and the frozen profiles,
but not on `R`, the mode locations or gaps, amplitudes, phases, or `B`.

With `alpha=n_1aR`, the carrier range splits exhaustively:

- `alpha<=a`, equivalently `n_1R<=1`, is R0.76B;
- `alpha>a`, equivalently `lambda=(alpha/a)^2=(n_1R)^2>1`, is R0.76C;
- equality belongs to R0.76B, so no endpoint is omitted.

In the second branch `alpha>a=pL`.  Because `q` is fixed, every sufficiently
large frozen `L` has `alpha>8q`, which is exactly the hypothesis needed for
the gap-free spatial observation from R0.76B.  This implication would not be
uniform for `q=q(L)`, and no such conclusion is claimed.

## 2. Stable exponential-polynomial lemma

For

`Q(tau)=sum_(r=1)^N c_r exp(mu_r tau)`, `N<=2q`,

the real parts lie in `[-4,-1]`.  Multiplication by `exp(5 tau/2)` centers
them in `[-3/2,3/2]`.  On the Chebyshev subset

`E={r in [0,1]: |Q(r)|^3<=2 I_Q}`

one has `|E|>=1/2` and
`sup_E |exp(5r/2)Q(r)|<=exp(5/2)(2I_Q)^(1/3)`.
Turan--Nazarov on `[0,tau]` contributes

`exp(3 tau/2)(C tau/|E|)^(N-1)`.

After undoing the centering, the exponential factor is exactly
`exp(-tau)`.  Since `tau>=1`, the polynomial factor is bounded by
`C_q(1+tau)^(2q-1)`.  Cubing gives C.13.  The theorem depends on the
absolute real-part bound but contains no imaginary-frequency or
exponent-gap denominator.

The family statement in C.14 is restricted pointwise in `z`: every
`Q(.;z)` must satisfy C.12.  It is not a claim for an arbitrary measurable
time-dependent family.  Tonelli then gives

`k(tau)<=C_q(1+tau)^(3(2q-1))exp(-3tau)K_1`.

On `[0,1]`, Holder yields the weighted `K_T^(2/3)` bound.  On `[1,infinity)`,
the polynomial-exponential tail is integrable.  At `tau=T>=4`, the stronger
factor

`T^(2(2q-1)) exp(-2T)`

is bounded by `C_qT^(-2/3)`.  This establishes both statements of C.15.
The `T^(-2/3)` endpoint power is essential; a merely uniform endpoint trace
would not close the later `lambda` ledger.

## 3. Exact ultra-high time scaling

At each fixed `z`, `G(tau/lambda,z)` is a sum of at most `2q` exponentials
with exponents

`-kappa_j^2/alpha^2 +/- i kappa_jv/lambda`.

The dyadic band gives real parts in `[-4,-1]`.  Arbitrarily large `v` affects
only imaginary parts.  Frequencies may approach or collide after scaling;
the argument never divides by a gap.

The identities

`T=4lambda`, `K_T=lambda H`, and `zeta(s)<=C_eta s`

give, without suppressed powers,

`lambda int zeta h^(2/3) ds
 <=(C_eta/lambda) int tau k^(2/3) dtau
 <=C_q lambda^(-1/3)H^(2/3)`.

Because `lambda>1`, this is uniformly bounded.  For the terminal row,

`k(4lambda)^(2/3)
 <=C_q(4lambda)^(-2/3)(lambda H)^(2/3)
 =C_q4^(-2/3)H^(2/3)`.

Thus the gradient and endpoint payments close independently of `lambda`.
The first calculation uses `zeta(0)=0` essentially; without onset one would
retain an uncompensated factor `lambda`.

## 4. Full-real-field energy audit

The proof applies the scalar transport-diffusion equation once to the whole
real field `G`.  Its square satisfies

`(G^2)_s+v(G^2)_z-a^(-2)(G^2)_zz=-2a^(-2)|G_z|^2`.

With `W_a=Xi_a'`, two spatial integrations by parts give

`v int W_aG^2=E'-a^(-2)int Xi_a''G^2
 +2a^(-2)int Xi_a|G_z|^2`.

Time integration against `zeta` has the signs displayed in C.30.  The
initial endpoint vanishes exactly.  The value half of the spatial observation
pays `E`, the cutoff derivative, and the `Xi_a''` row.  The derivative half
gives

`a^(-2) int Xi_a|G_z|^2<=C_q(alpha/a)^2h^(2/3)
 =C_q lambda h^(2/3)`,

and the clock calculation in C.26 pays it.  C.27 pays the terminal energy.
No positive or negative row is silently discarded.

This argument reassembles self, difference-frequency, sum-frequency, and
cross-group terms inside the complete real square before taking absolute
values.  It therefore does not use the unresolved analytic-density subblock
from R0.75Z, the false localized-current sign route rejected in R0.76A, or
the sharp-failure standalone carrier integration-by-parts route.

## 5. Physical scaling audit

The cross-section change of variables gives flux prefactor
`a^2R^3v/2`.  The plateau fibre area, `dt=R^2ds`, and `dx_2=aRdz` give

`M_plat>=4 pi delta_0 a^2R^5H`.

Consequently,

`a^2R^3(M/(a^2R^5))^(2/3)
 =a^(2/3)R^(-1/3)M^(2/3)`.

Multiplication by `omega/R` and substitution
`M=R^2omega^(-1)p` cancel the remaining `R` power and give

`a^(2/3)omega^(1/3)p^(2/3)`.

The frozen logarithmic rate is
`-c_gamma/12=-(8/3969)/12=-2/11907`.

## 6. Degeneracy and counterexample audit

- `B=0`: the flux is zero; the undivided identity is still valid.
- unbounded `|B|`: only temporal imaginary parts grow.
- zero amplitudes: the active term count decreases.
- nearly or exactly colliding temporal exponents: Turan--Nazarov has no gap
  denominator; repeated identical terms can be combined.
- `lambda downarrow 1`: R0.76B contains equality and R0.76C is uniform above
  it.
- `lambda to infinity`: the weighted row improves like
  `lambda^(-1/3)` and the terminal row remains constant.
- high spatial cancellation: R0.76B's carrier-scaled measurable-set and
  compact-ODE observation remains the operative bound.
- arbitrary measurable time family: excluded explicitly in C.14; omitting
  its exponential-polynomial hypothesis would make C.15 false.

The independent counterexample-first pre-audit found no mathematical
blocker and independently recomputed C.13, C.15, and C.26.  It identified
the C.14 family-quantifier ambiguity, which was corrected before this audit
was frozen.

## 7. Source and evidence boundary

The source report verifies Nazarov's original record and the
Friedland--Yomdin primary restatement.  Only the measurable-set
Turan--Nazarov inequality is imported.  The stable heat-clock corollary,
weighted tail, energy identity, onset gain, and scale conversion are local
proofs.

Finite exact arithmetic can verify one ultra-high family, exponent bands,
the scalar PDE at a point, the energy signs, the `lambda` ledger, and all
physical exponents.  It is not proof of the continuum Turan--Nazarov theorem
or of the uniform spatial observation already proved in R0.76B.

No formal figure is required.  A simulation cannot certify the fixed-order
uniform inequalities, and no simulation result enters the theorem.

## 8. Final boundary

R0.76C closes the carrier range only for each fixed finite exact real shear
family.  It does not give a usable bound for `q=q(L)`, arbitrary packets,
nonconstant shear, projection from a larger velocity, arbitrary-field E.24,
Version-M extraction, suitable-weak transfer, regularity, or singularity.
The constant-background shear is not promoted to the frozen mean-zero
Version-M subclass.  No completeness, novelty, or priority claim is made.
**NOT CLAY.**
