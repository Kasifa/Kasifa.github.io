# R0.76F primary audit -- exponential spatial-observation lower bound

## Current verdict

- Current verdict: **PASS**
- Mathematical blocker count: **0**
- Release blocker count: **0**

The independent counterexample-first reread reports PASS with zero blockers.
It checked the endpoint case `q=2, delta=2pi/3`, where the sine-ratio factor
is exactly two, and the limit `delta downarrow 0`, where the ratio tends to
`3^(q-1)`.  It also found one certificate-only typo: the fixture initially
encoded the rule for `alpha` as `q-delta`.  The fixture now says `q*delta`,
and both the Python and Ruby implementations validate that field together
with the displayed identity `alpha=qdelta`.

## Quantifier and class audit

The main theorem fixes `q>=2` and `0<delta<=2pi/3`.  The frequencies
`n_j=q+j-1` are positive integers, strictly increasing, and satisfy
`n_q=2q-1<=2n_1`.  The amplitudes are binomial coefficients and hence
nonnegative.  Arbitrary real phases are permitted by the exact-shear class.

Taking a real part introduces the conjugate negative frequencies required
for a real field, but F.3 still has exactly `q` positive cosine modes.  It
does not add a zero mode or repeated positive frequency.

## Phase audit

With

\[
 H(z)=e^{iq\delta z}(1-e^{i\delta z})^{q-1},
\]

the endpoint value at `z_*=3/2` is nonzero because
`0<3delta/2<=pi`.  A phase `theta=-arg H(z_*)` therefore exists and makes
`Re(e^(i theta)H(z_*))=|H(z_*)|`.

The coefficient of frequency `q+k` is
`e^(i theta)(-1)^k binom(q-1,k)`.  Since
`A cos(n delta z-phi)=Re(A e^(-i phi)e^(in delta z))`, the choice
`phi=-theta-kpi` is correct.

## Norm and trigonometric audit

On `I`, `|delta z/2|<=delta/4<=pi/6`, so sine is increasing in the
relevant absolute argument.  The interval has length one; hence the
`L^3(I)` norm is at most the displayed sup norm without an omitted measure
factor.

At `z_*=3/2`, the phase alignment gives the exact numerator value.  Setting
`x=delta/4` yields

\[
 \sin(3x)/\sin x=3-4\sin^2x\ge2
\]

for `0<x<=pi/6`.  Raising to `q-1` proves the lower bound.  The derivative
term in the inherited observation row is nonnegative and is not needed.

## Exact-shear audit

For `delta=aR`, `B=0`, and the stated data, the exact heat shear satisfies
the unforced Navier--Stokes equations.  Its scaled initial fibre is exactly
the constructed polynomial, with `alpha=qdelta`.  Thus a uniform spatial
row must cover this example.

The construction at `B=0` has zero transport flux.  The main note therefore
correctly refuses to infer an exponential lower bound for the complete
signed collar flux.

## Asymptotic and claim audit

The deduction `C_q>=2^(q-1)` rules out uniform and polynomial dependence in
the same spatial observation mechanism.  For quadratic mode counts it
changes the normalized exponential coefficient; it does not by itself
rule out a still-negative coefficient at sufficiently small quadratic
density.

The source report identifies broader sharp Remez results and makes no
novelty or priority claim.  Arbitrary packets, Version-M extraction,
regularity, and singularity remain open.  **NOT CLAY.**
