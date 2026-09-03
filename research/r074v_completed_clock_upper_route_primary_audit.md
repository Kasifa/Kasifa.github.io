# R0.74V Step 21 primary analytic audit

- Schema: `r074v-completed-clock-upper-route-primary-audit-v1`
- Verdict: **PASS**
- Blocking findings: **none**
- Frozen candidate SHA-256: `031c9ca8600c776d9897b247147bc4ecebff68a71e6b3c5906b310463d5b627c`
- Frozen source commit: `d74e7b297928147334136f4c3cb29c5226d66381`
- Audit mode: independent formula reconstruction, exact rational arithmetic,
  source/hash binding, periodization audit, and claim-boundary audit

## 1. Decision

The frozen candidate passes this audit as a route memo.  Its exact algebra,
finite-table reductions, lifted-multiplicity bounds, and rational exponent
ledger are correct.  The document does not promote any proposed occupation
estimate, target-coordinate upper bound, adjacent-inward common-shear lower
bound, or all-shell theorem to an established result.

The earlier large-shell ambiguity is closed in this frozen version:

1. the periodized cutoff is treated as a sum with multiplicity, rather than
   as a projected \(0\)-\(1\) shell;
2. the global chord scale is \(s_k+s_k^3\), not a torus-length cap;
3. the common-shear volume is the exact lifted tiling integral; and
4. (V.46)--(V.50) are restricted to the six central-chart pairs (V.67),
   while the all-\(k\) lifted-copy summation remains explicitly open.

No blocking mathematical or claim-scope error remains in the audited file.

## 2. Frozen dependency and source binding

All dependency hashes were recomputed from both the working-tree bytes and
the corresponding blobs at the stated source commit.  Both computations give
the following values.

| Dependency | Recomputed SHA-256 | Result |
|---|---|---:|
| `research/r074e_local_mollified_frame_gate.md` | `3a0ea093c42016b78cb589738a666d7b40019fd860c934be9c46418cb1fb05d7` | PASS |
| `research/r074f_two_packet_survival.md` | `0dc16cefb3ce071ce0f309a7683bf2956ebcc9cbc91520544bd5a740edb4c2eb` | PASS |
| `research/r074h_collar_flux_two_regime_closure.md` | `8c1d43f08d5a2c9299ae50ebdd10c8c184f064c6830f1d663524e03fa90d88f1` | PASS |
| `research/r074p_temporal_observable_triage.md` | `a3cb872735b92b32ddfa7b96bc4184d70b0287ff2ce7d3da8cadbbcc494d0867` | PASS |
| `research/r074q_common_shear_multipacket_gate.md` | `60cb683ff6b602b16d64313b278c11a08d73f89e3bc2b1562b256a9911695695` | PASS |
| `research/r074q_relaxed_multipacket_cubic_obstruction.md` | `ba8897da349aa5c71c5ac355164a938599489c2691b09eb59760934b70617e8d` | PASS |
| `research/r074t_schedule_invariant_dwell_coercivity.md` | `8d56a66ff918fe1c25056617468022379b71ab37bacff2650599194501ea4fbd` | PASS |
| `research/r074u_intrinsic_certified_residence.md` | `e149243c81e6919c318ddcd4bc94c4830c74cfc586b776e29284f79a35336d99` | PASS |

The candidate hash was independently recomputed after the audit and still
equals the frozen value above.

## 3. Version-M clock and exact nonnegative ledger

### A1. General Version-M variables and good-time boundary — PASS

R0.74P (2.6)--(2.7) has the endpoint term

\[
 {\gamma_k\eta_R(t)\over2R}
 \int_{\mathbb T^3}\Psi_k^R(y)|v_R(t,y)|^2\,dy,
 \qquad v_R(t,y)=u(t,y+X_R(t)),
\]

and the total-dissipation term in physical coordinates with

\[
 \Psi_k^R(x-X_R(r)).
\]

After the exact decomposition

\[
 d\boldsymbol\mu
 =|\nabla u|^2\,dx\,dr+d\boldsymbol D,
 \qquad \boldsymbol D\ge0,
\]

this is exactly (V.16), including the factors \(1/(2R)\), \(1/R\), the
shell weight \(\gamma_k\), and the time cutoff \(\eta_R\).  The endpoint uses
\(v_R\) and \(y\); the accumulated rows use \(u\), \(x-X_R(r)\), and physical
coordinates.  There is no \(v_R/X_R\) mismatch.

The hard-time convention is also correct.  The literal endpoint-plus-measure
identity is asserted only at local-energy good times.  At other times the
memo uses R0.74P's canonical absolutely continuous representative
\(K_{k,R}=Q_{k,R}+F_{k,R}\), rather than asserting a raw endpoint trace or a
half-open measure identity.  For the exact smooth family \(X_R=a_R=0\), so
the unshifted three-row formula holds at every time.

### A2. Three nonnegative rows — PASS

The completion contains exactly:

1. the nonnegative endpoint kinetic row;
2. accumulated ordinary viscosity; and
3. accumulated anomalous local-energy defect.

The last two rows are nondecreasing because their integrands are nonnegative.
The anomalous row vanishes for the smooth family but is correctly retained as
a separate obstruction before any suitable-weak extension.

### A3. Exact shear, packet, and cross-term absorption — PASS

For \(u=(G,b,0)\), component orthogonality gives

\[
 |u|^2=G^2+b^2,
 \qquad
 |\nabla u|^2=|\nabla_{23}G|^2+|\partial_3b|^2,
\]

which proves (V.17)--(V.18) without a signed remainder.  Expanding
\(G=g_1+g_2\) gives the endpoint and viscous cross rows in (V.20) with the
displayed factors \(1\) and \(2\).  Pointwise Young inequalities give

\[
 2|g_1g_2|\le g_1^2+g_2^2,
 \qquad
 2|\nabla g_1\!\cdot\!\nabla g_2|
 \le |\nabla g_1|^2+|\nabla g_2|^2,
\]

and hence (V.22)--(V.23).  The second application to the positive and
inverted components inside each \(G_m\) is valid with only a fixed factor.
The memo correctly keeps total variation separate from this pointwise upper
absorption.

### A4. Cutoff/source representation and non-duplication — PASS

Specializing R0.74P (2.8)--(2.9) to \(X_R=a_R=p=0\) gives exactly
\(Q^\eta+Q^\Delta+F^G\).  The \(\partial_1\Psi_k^R\) term integrates to zero
because the fields are independent of \(x_1\); the \(b^3\partial_2\Psi_k^R\)
term integrates to zero because \(b\) is independent of \(x_2\).  The
surviving flux is

\[
 {\gamma_k\over2R}\int\eta_R bG^2\partial_2\Psi_k^R.
\]

Thus (V.24)--(V.27) are an alternative signed balance for the same clock,
not additional completion rows.  The warning against adding the \(Q/F\)
ledger to (V.16) is correct.

## 4. Periodization, packet ceilings, and \(\Gamma\)-scales

### B1. Lifted-multiplicity chord — PASS

Let \(s_k=(2^{k+1}+1/8)R\).  For fixed torus coordinates
\((x_2,x_3)\), sum-periodization and Tonelli give the exact one-dimensional
tiling formula in (V.32).  At most \(C(1+s_k^2)\) lattice pairs
\((n_2,n_3)\) can meet the radius-\(s_k\) ball, and every corresponding
\(x_1\)-chord has length at most \(2s_k\).  Therefore

\[
 \sup_{x_2,x_3}\int_{\mathbb T}\Psi_k^R\,dx_1
 \le C(s_k+s_k^3)=C\ell_k.
\]

Combining this with the two-dimensional packet energy identity proves
(V.33) for all \(k\).  No projected-support or single-torus-volume cap is
used.

### B2. Exact periodized volume and all-shell shear summation — PASS

Full tiling gives

\[
 V_k=\int_{\mathbb T^3}\Psi_k^R
 =\int_{\mathbb R^3}\psi_k^R\le Cs_k^3.
\]

This retains every lifted copy.  The endpoint and four-\(R^2\) viscous
interval then give (V.38).  Since

\[
 \sum_{k\ge1}\gamma_ks_k^3
 \le CR^3\sum_{k\ge1}e^{-4^{k-1}/32}(2^{3k}+1)
 \le CR^3,
\]

both all-shell estimates in (V.40) follow; the \(\ell^2\) bound also follows
from positivity and the \(\ell^1\) bound.

### B3. Target and cross-coordinate scales — PASS

Exact rational reconstruction gives

\[
 c_\gamma\lambda^2
 ={8\over3969}\left({63\over32}\right)^2={1\over128}.
\]

Consequently \(\Gamma_i=\gamma_{k_i}\), and \(L_2=2L_1\) gives
\(\Gamma_2=\Gamma_1^4\).  On the finite central table,
\(\ell_k\asymp2^kR\), so

\[
 H_{k\leftarrow m}
 \asymp\gamma_k\mathfrak a_m^2 2^kR^2.
\]

Substitution of
\(\mathfrak a_m^2=A_*^2/(\Gamma_mL_m)\) and
\(T=A_*^2R^2\) yields

\[
 H_{k_i\leftarrow i}\asymp T,
 \qquad
 {H_{k_2\leftarrow1}\over T}\asymp\Gamma_1^3,
 \qquad
 {H_{k_1\leftarrow2}\over T}\asymp\Gamma_1^{-3}.
\]

The exponentially large off-target packet-2 ceiling is therefore not
silently discarded.

### B4. Finite central-table boundary — PASS

The six pairs in (V.67) are central-chart pairs under \(L_2R\le5/144\).
The memo now limits (V.46)--(V.50) to exactly these pairs.  It separately
states that an all-\(k\) theorem must replace the single central-lift distance
by distances to every relevant lift and pay their multiplicities.  F7 and
the final “Not established” list prevent reuse of the finite-table distance
at large shell index.

## 5. Common-shear floor

### C1. Explicit box (V.39a)--(V.39b) — PASS

For the displayed box, the lower radial comparison is

\[
 {3\over4}-{1\over\lambda}={61\over252}>0.
\]

Its maximal normalized radius squared is \(171/256\), while

\[
 \left({2\over\lambda}\right)^2-{171\over256}
 ={369877\over1016064}>0.
\]

Hence the box lies inside \(A_{k_i}(R)\), and sum-periodization gives
\(\Psi_{k_i}^R\ge1\) there.  Its volume is exactly \(r_i^3/1024\).
The box is \(\asymp L_iR\) from the saturation transitions; heat-kernel
leakage on times \(t\asymp R^2\) is \(O(e^{-cL_i^2})\).  The endpoint row
therefore gives the claimed lower scale

\[
 K^b_{k_i,R}\gtrsim\Gamma_iB^2L_i^3R^2.
\]

Together with the upper estimate from (V.38), this verifies (V.39) and the
necessity of a strict common-shear budget at level \(\kappa T\).

## 6. Conditional target-coordinate superlevel algebra

### D1. Threshold direction and constants (V.51)--(V.57) — PASS

The baseline in (V.51) dominates the shear row, both terminal diagonal
viscous rows with the Young factor \(2\), and the anomalous row.  Therefore
(V.52) follows from (V.23).

If \(\mathcal B_i\le\kappa T/2\) and both endpoint diagonals were strictly
below \(\kappa T/8\), then

\[
 K_{k_i,R}< {\kappa T\over2}
 +2{\kappa T\over8}+2{\kappa T\over8}
 =\kappa T.
\]

The contrapositive is exactly the inclusion (V.54).  On \(I_R\),
\(\eta_R=1\), and the left side tested in (V.48) equals \(2E_k^m\).
Thus \(E_k^m\ge\kappa T/8\) corresponds to \(z=\kappa/4\), and the
flat-remainder gate \(CH\varepsilon\le zT/2\) becomes precisely
\(CH\varepsilon\le\kappa T/8\), as stated in (V.54a).

The logarithmic distribution bound then gives (V.55).  Since every relevant
amplification has logarithm \(O(L_2^2)\), its square root is \(O(L_2)\),
which yields the conditional duration scale (V.56).  Formula (V.57) has the
correct inequality direction and collects the shear, clock-interval
viscosity, weighted flat errors, non-flat occupation error, and anomalous
floor.  Choosing its absolute constant \(c\) sufficiently small also pays
the separate endpoint gates (V.54a).

The memo explicitly leaves (V.47)--(V.50), and therefore (V.56), unproved.

## 7. Adjacent inward-shell comparator and exact fractions

### E1. Geometry and free-comparator scale — PASS

For shell \(k_m-1\), the outer radius is \(L_mR/\lambda\), while the packet
height at re-centring is \(c_hL_mR\).  Exact subtraction gives

\[
 d_0={15\over16}-{32\over63}={433\over1008}.
\]

A width-\(R\) core strip just inside the outer face, together with a fixed
width-\(R\) horizontal derivative-kernel interval, has an \(x_1\)-chord of
order \(\sqrt{L_m}R\), hence volume of order
\(\sqrt{L_m}R^3\).  The amplitude normalization contributes \(L_m^{-1}\),
so the geometric prefactor in the normalized endpoint energy is
\(L_m^{-1/2}\), exactly as in (V.64).

The shell-weight ratio is

\[
 {\gamma_{k_m-1}\over\Gamma_m}
 =\Gamma_m^{-3/4}
 =\exp\!\left({3\over4}c_\gamma L_m^2\right).
\]

The heat age is \(a_mR^2=(1+\tau_m/R^2)R^2\) with
\(65\le a_m\le66\).  Squaring the vertical heat kernel gives the cost
\(-d_0^2L_m^2/(2a_m)+O(L_m)\), so the leading exponent (V.61) is correct.

### E2. Exact rational recomputation — PASS

Independent rational arithmetic gives

\[
 \chi(65)
 ={12191\over132088320}
 \approx9.2294307324\times10^{-5}>0,
\]

\[
 \chi(66)
 ={15263\over134120448}
 \approx1.1380069354\times10^{-4}>0,
\]

and \(\chi'(a)=d_0^2/(2a^2)>0\), so positivity at \(65\) proves positivity
throughout the inherited slab.  Finally,

\[
 {1\over320}-4\chi(66)
 ={447593\over167650560}
 \approx2.6697972258\times10^{-3}>0.
\]

Thus the \(\rho-4\chi(66)\) reserve in (V.65) is exact.

### E3. Claim grade of (V.64)--(V.66) — PASS

The memo calls (V.64) a free-comparator prediction and expressly says that
it is not a lower bound for the common-shear solution.  Relative remote-strip
survival, inversion control, and noncancellation by the other packet remain
inputs to Proposition V.0.  Likewise (V.66) is only a candidate
exponential-accuracy gate; its polynomial \(P\) must be supplied by the
unproved V.0--V.1 estimates, and the generalized R0.74U assumptions are not
claimed to imply it.  This is the correct downgrade.

## 8. Structural and claim-boundary audit

The frozen markdown has:

- 76 equation tags and 76 unique tags;
- no duplicated tag and no equation reference to a missing tag;
- 77 matched display-math delimiter pairs;
- 203 matched inline-math delimiter pairs;
- 8 correctly nested and matched `begin/end` environment pairs; and
- balanced braces in every display block.

The status markers explicitly retain route-only, \(K\)-superlevel-open,
adjacent-inward-tail-gate, finite-central-table, and all-\(k\)
lifted-summation-open boundaries.  “NOT CLAY” appears both in the opening
scope and at the end.  The final established/not-established lists agree
with the body: no suitable-weak anomaly estimate, arbitrary-clock result,
all-shell upper, \(Y_2\) upper, regularity theorem, singularity theorem, or
Millennium conclusion is asserted.

## 9. Audit boundary

This PASS certifies the frozen memo's algebra, exact fractions, hash locks,
periodization bookkeeping, conditional implications, and claim grading.  It
does not prove the proposed finite-table occupation estimates (V.47)--(V.50),
Proposition V.0, the conditional conclusion (V.56), an all-\(k\) lifted-copy
summation, or any result listed as open in the memo.
