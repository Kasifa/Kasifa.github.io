# R0.76L primary mathematical and source audit

## Verdict

**PASS -- for the explicit start-prepaid exact-shear family in
`sqrt(A)<<m=o(A^2)`; the high-degree route remains open.**

The main note proves a forward Chebyshev double-scale edge asymptotic,
transfers it uniformly to one exact real integer one-band heat shear,
controls both signs of the paired collar over the complete clock, pays the
full physical plateau, and obtains the exact frozen normalized rate
`-2/11907`.  It does not prove a theorem for arbitrary packets, enter the
mean-zero inversion-paired Version-M subclass, or establish Navier--Stokes
regularity or singularity.

## Frozen dependency boundary

The immediate upstream R0.76K release is bound to:

| artifact | SHA-256 |
|---|---|
| `research/r076k_real_dyadic_edge_sharpness.md` | `e293a3aa3e9c1dde443ed7a8c07afd2c709d3855d8b469b38033b04d71116bf2` |
| `research/r076k_real_dyadic_edge_sharpness_primary_audit.md` | `36a26cb421a108127b516e47a0008625d67ec43a1d009a14bef9d7684ef03671` |
| `research/r076k_report-source.md` | `21dbd71aae07ecbe910d4bcefbf6e1caccc3cddc41171a57ffd239c6eed34f3e` |
| `research/r076k_real_dyadic_edge_sharpness_certificate.json` | `4d5247ca82869758c01a398f9a4858bfce87e3bd7ab3ad2a37eac0e6bdea7f1d` |
| `research/r076k_real_dyadic_edge_sharpness_qa_report.md` | `b888919d4f1992c22e5206d6350983dbd89885df29bb62b3408b581298c511ec` |

The exact upstream research commit is
`8a89aee4fe0839de44e21a90ba827a9cc77b3062`.  The later Step62 handoff
commit does not alter the mathematical input.  Any dependency hash or
commit mismatch invalidates this audit until the change is reviewed.

## Edge saddle audit

For

\[
 Q_{m,A}(s,c)=
 \left(e^{sA^{-2}D^2}T_m\right)(1+c/A),
 \qquad \mu=(m^2/A)^{1/3},
\]

the positive-exterior Gaussian integral has, after `y=mu z`, the locally
uniform rate

\[
 \Phi_s(z)=\sqrt{2z}-\frac{z^2}{4s}.
\]

Solving `Phi_s'(z)=0` gives

\[
 z_s=2^{1/3}s^{2/3},\qquad
 F_s=3\,2^{-4/3}s^{1/3},\qquad
 G_s=\frac{z_s}{2s}=2^{-2/3}s^{-1/3}.
\]

At `s=4` these become `2^(5/3)`, `3*2^(-2/3)`, and
`2^(-4/3)`.  The powers follow exactly from `mu^3=m^2/A`; there is no
missing factor of two in either the Gaussian variance or the edge tilt.

The passage from concentration to the fixed-`c` ratio is not based on
weak convergence.  The revised proof explicitly treats the unbounded
weight `exp(cY/(2s))`: strict concavity gives a compact-complement loss
`-kappa mu^2+O(mu)`, while for large `z` the quadratic Gaussian term
dominates the linear tilt uniformly.  This is sufficient for positive and
negative bounded `c`, uniformly on positive compact time intervals.

On the negative exterior, Young's inequality gives

\[
 \frac m{\sqrt A}\sqrt{2u}
 \le \frac{u^2}{16s_1}+C\mu^2.
\]

Combining this with the square centered near `-2A` yields a uniform
supremum `-cA^2+Cmu^2+O(A)`.  Since `mu^2=o(A^2)`, both the negative
exterior and the bounded oscillatory middle are negligible relative to
the positive saddle.  L.17--L.29: **PASS**.

## Positive-series and terminal-layer audit

The endpoint derivatives satisfy

\[
 \frac{D_{k+1}}{D_k}=\frac{m^2-k^2}{2k+1},
\]

and expanding first at `x=1` and then in the terminating heat series gives
the exact positive double sum L.32.  For fixed `ell`, the ratio of
successive `j` weights is bounded by

\[
 \frac{C\mu^6}{(j+1)^3}.
\]

Thus every nonzero conditional row has mean `j=O(1+mu^2)`; zero-weight
rows are irrelevant.  The identity `partial_c^2 Q=partial_s Q` then gives
`partial_c log Q=O(1+mu)` on fixed positive edge intervals.  The terminal
width `h_L=(1+mu^2)^(-1)` consequently costs only a constant factor.
L.30--L.37: **PASS**.

## Exact integer shear and dynamic confluence audit

Every coefficient in

\[
 T_m(w_\eta(x))=\sum_{j=0}^m b_j(\eta)e^{ij\eta x}
\]

is nonzero because `b_j` is a nonzero constant at the top order and, below
it, evaluates a real-rooted nonconstant derivative at the nonreal point
`i/eta`.  Multiplication by the carrier `m eta` therefore produces exactly
the consecutive positive integer frequencies `m,...,2m`.  Direct
substitution verifies the real shear solves the unforced equation; this is
an exact solution statement, not a novelty statement about shears.

For finite `eta`, the exact conjugated operator is

\[
 \mathcal L_\eta=(1+i\eta w)^2D_w^2
 +i\eta(1+i\eta w)D_w.
\]

In the weighted coefficient norm `sum |p_k|rho^k`, the operator difference
is `O(eta m^2)` and both semigroup generators are `O(m^2)`.  The nested
evaluation disks in the revised proof keep all real, complex-shifted, and
`w_eta` arguments strictly inside the coefficient radius.  Duhamel gives

\[
 \|e^{t\mathcal L_\eta}T_m-e^{tD^2}T_m\|_\rho
 \le Ct\eta m^2 C_\rho^m e^{Ctm^2},
 \qquad t=s/A^2.
\]

The carrier, scalar damping, imaginary displacement, and `w_eta-x`
replacement add only `eta poly(m,A)`.  Since `eta=AR`,
`m=o(A^2)`, and `A` is proportional to `L`, the total error is

\[
 \exp[-9L^2/40000+o(L^2)].
\]

L.38--L.47: **PASS**.

## Signed complete-clock audit

The fixed negative drift makes the positive cap edge coordinate exceed its
negative partner by `2gamma_L s`.  Uniformly for `3<=s<=4`, the squared
negative-to-positive ratio is at most `exp(-c beta mu)`.  Oddness of the
collar weight and the drift sign therefore make every paired contribution
in that time slab nonnegative.

The possible adverse interval `0<=s<=3` is at most
`C(beta/A)Q(3,C)^2`.  The terminal box contributes at least

\[
 c\frac\beta A h_L Q(4,c_-+4\gamma_L)^2.
\]

Their ratio is bounded by

\[
 Ch_L^{-1}
 \exp[-2(F_4-F_3)\mu^2+o(\mu^2)]\to0.
\]

This supplies the quantitative absorption missing in the first draft and
strictly proves eventual positivity, rather than relying on a terminal
slice alone.  L.48--L.55: **PASS**.

## Full-plateau and physical-scaling audit

The full shell projection is `|x|<=1+2delta_0/A`.  The endpoint derivative
majorant, parity, and positive exterior expansion control every projected
point by the terminal positive edge coordinate `c_p+4gamma_L`.  Since the
cross-sectional area is at most `Ca` over a bounded `z` interval,

\[
 \mathcal K_L\le CaQ(4,c_p+4\gamma_L)^3.
\]

On the explicit outer strip `delta_0<=c<=3delta_0/2`, the area is bounded
below by `ca`, while `dz=dc/a`; hence the area and Jacobian cancel and

\[
 \mathcal K_L\ge ch_LQ(4,\delta_0+4\gamma_L)^3.
\]

Together with the signed-flux bounds and the terminal edge ratio, these
give L.11.  The exact conversion

\[
 \mathcal T_L=\frac{a^2R^3}{2}\mathcal S_L,
 \qquad M_L^{\rm plat}=aR^5\mathcal K_L
\]

produces `a^(2/3)` in the lower bound and `a^(4/3)` in the upper bound.
No exponential factor is hidden in this algebra.

Finally,

\[
 \frac{\mathfrak X_L}{(p_L^{\rm plat})^{2/3}}
 =R^{1/3}\omega^{1/3}
  \frac{\mathcal T_L}{(M_L^{\rm plat})^{2/3}},
\]

and `mu=o(A)=o(L^2)` leaves only
`L^(-2)log(omega^(1/3))=-2/11907`.  Equivalently,
`omega^(1/3)=exp(-A^2/1536+o(A^2))`.  L.56--L.66: **PASS**.

## Formal high-degree boundary

For `m>>A^2`, the formal bulk-exterior stationary point uses the integration
variable `y_s~sqrt(2sm)`, or the physical edge displacement
`x_s-1=y_s/A`.  It predicts
`partial_c log Q~sqrt(m/(2s))`.  At `m=kappa A^4`, squaring the terminal
cap-to-plateau ratio gives the candidate exponent

\[
 \Delta_c\sqrt{\kappa/2}\,A^2,
\]

and hence the displayed formal threshold against `A^2/1536`.  None of the
edge asymptotics or finite-`eta` estimates proved in this release applies
in that regime.  L.70--L.72 are correctly marked **OPEN**, not extrapolated
as a theorem.

## Source and finite-evidence boundary

The source report correctly classifies heat-polynomial/Gaussian formulas,
Chebyshev identities, and fixed-scale Hermite--Chebyshev operational
relations as prior art.  The bounded collision search found no theorem with
the combined first-kind double-scale edge ratio and complete-clock exact
shear application, but the report explicitly denies that bounded absence
establishes novelty or priority.

The finite diagnostic checks the saddle, common amplitude, and unit-edge
tilt over sixteen cases.  Its numerical gates cover non-finite values,
stationary-point residuals, coarse/fine quadrature, and tail-truncation
sensitivity.  Its PDF/SVG/600-dpi PNG are presentation artifacts.  None is
used as proof of the continuum limit or PDE statement.

## Counterexample-first reread

An independent first audit identified three proof blockers: the unbounded
tilt, the growing-degree Duhamel transfer, and the quantitative absorption
of the early adverse clock.  All three were expanded into explicit
estimates.  The second independent reread returned **PASS** and found no
remaining constant, sign, geometry, `R`, or `omega` mismatch.  The release
is ready for dual finite certificates and clean-archive QA.  **NOT CLAY.**
