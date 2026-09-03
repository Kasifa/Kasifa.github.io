# R0.74X independent primary audit — three-packet fixed-deletion gate

## 0. Audit verdict and frozen object

**Verdict: PASS.**  No mathematical blocker was found for the claims actually
made in the candidate.  In particular, the note proves a two-coordinate
endpoint obstruction normalized by (T_*), and then correctly proves that
this particular W-strip architecture cannot contradict the payment-normalized
fixed-deletion gate.  It does **not** claim that the gate itself is false.

The audited candidate is frozen byte-for-byte as

```text
research/r074x_three_packet_fixed_deletion_gate.md
SHA-256 4fdc9558605afd9557c557c4292ca1af50d52ff54f9aa11603f15c97a97b3ee3
```

The latest readback contains no duplicated Section 3 heading and no duplicated
Section 8 opening sentence. The payment-radius sentence now immediately
precedes (X.45), so the shell/weight identities and cubic lower bound form one
uninterrupted argument.

## 1. Frozen-source readback

All eight dependency hashes displayed in Section 1 were recomputed locally
and agree:

| dependency | recomputed SHA-256 |
|---|---|
| `r074p_temporal_observable_triage.md` | `a3cb872735b92b32ddfa7b96bc4184d70b0287ff2ce7d3da8cadbbcc494d0867` |
| `r074q_common_shear_multipacket_gate.md` | `60cb683ff6b602b16d64313b278c11a08d73f89e3bc2b1562b256a9911695695` |
| `r074q_relaxed_multipacket_cubic_obstruction.md` | `ba8897da349aa5c71c5ac355164a938599489c2691b09eb59760934b70617e8d` |
| `r074s_fixed_deletion_simultaneous_height.md` | `305bf75f978c080a1790fbc42bb9bd725f56f537785ffe0fc45e3ca815aa5dc1` |
| `r074t_schedule_invariant_dwell_coercivity.md` | `8d56a66ff918fe1c25056617468022379b71ab37bacff2650599194501ea4fbd` |
| `r074u_intrinsic_certified_residence.md` | `e149243c81e6919c318ddcd4bc94c4830c74cfc586b776e29284f79a35336d99` |
| `r074v_completed_clock_upper_route.md` | `031c9ca8600c776d9897b247147bc4ecebff68a71e6b3c5906b310463d5b627c` |
| `r074w_remote_adjacent_inward_comparison.md` | `d818db13acc16ad26a2d9628f2681e4a654698c9966815dd6cf1712813830d10` |

## 2. Exact solution and fixed-deletion quantifier

The finite-packet common-shear construction is closed under addition because
all three passive packets are re-evolved under the same coefficient (b).
Thus


\[
 U_3=\sum_{m=1}^3\mathfrak a_mG_m,
 \qquad u^{(3)}=(U_3,b,0),\qquad p^{(3)}=0
\]

is the exact smooth periodic unforced Navier--Stokes solution inherited from
R0.74Q Proposition 1.1.  Odd inversion and the even mollifier give the stated
zero frame.  The equal target-clock identity also recomputes exactly:

\[
 \Gamma_m\mathfrak a_m^2L_mR^2
 =\Gamma_m A_*^2(\Gamma_mL_m)^{-1}L_mR^2
 =A_*^2R^2=T_*.
\]

The deletion order in (X.5) is the required one:

\[
 \inf_{\#S\le1}\ \sup_{t\in\mathcal D}
 \sum_{k\notin S}K_{k,R}(t).
\]

The set (S) is fixed before the time supremum.  Therefore the different-time
pigeonhole in (X.43) is valid and does not require simultaneous peaks.
The revised text also states `I_R` is contained in `T_R`, explicitly takes
`D = T_R`, and writes the resulting left side in (X.44) as
`L^K_{1,R}(T_R)`. Thus the generic-domain pigeonhole is now visibly connected
to the domain of the actual gate.

## 3. Audit of “the times may also be chosen equal”

This sentence is valid. For each packet, (X.12) contains an independent
pre-translation constant determined by its chosen `tau_m`, while every
packet subsequently solves the same linear equation with the same shear
`b`. Nothing in exactness or the survival proof requires distinct
re-centring times. Choosing `tau_2 = tau_3 = tau` in `I_R` therefore gives
both strip comparisons at the same smooth time and proves (X.42).

Equal times are optional, not necessary: for arbitrary `tau_2, tau_3` the
fixed-deletion order still gives (X.43). The candidate keeps these two
statements separate.

## 4. Survival, all windings, and amplitude-weighted remote cross terms

For (L_2^2=4L_1^2) and (L_3^2=16L_1^2), the inherited reserve factors are

\[
 4q_{65}-a_S
 =\frac{3719797}{5811886080}>0,
 \qquad
 16q_{65}-a_S
 =\frac{72925813}{5811886080}>0.
\]

They give (X.26) for (m=2,3), uniformly over the full closed terminal slab.
The W representation retains the sum over every vertical winding; the
three-packet change affects only the finite amplitude-weighted cross audit.

Writing (r=L_j/L_m), direct substitution in

\[
 \delta_{m\leftarrow j}(a)
 =\frac{(c_hr-p)^2-d^2}{4a}-q(r^2-1)
\]

gives the following independently reduced minima.  The endpoint (a=66) is
used when the first numerator is positive and (a=65) when it is negative.

| ((m,j)) | (r) | worst (a) | exact margin |
|---|---:|---:|---:|
| ((2,1)) | (1/2) | 65 | (3667/70447104) |
| ((2,3)) | (2) | 66 | (100043/29804544) |
| ((3,2)) | (1/2) | 65 | (3667/70447104) |
| ((3,1)) | (1/4) | 65 | (147359/281788416) |

The intended inversion margin is independently

\[
 \frac{c_hp}{66}=\frac5{693}>0,
\]

and the largest-amplitude periodic-copy reserve is

\[
 c_*=\frac3{22}\left(\frac{144}{5}\right)^2-q
 =\frac{123450676}{1091475}>0.
\]

Hence (X.37) includes positive cross packets, negative inversion partners,
and all noncentral windings after the actual amplitudes are inserted.

## 5. Two distinct endpoint coordinates

The strip volume, target amplitude, adjacent shell weight, and squared free
kernel give the polynomial ledger

\[
 L_m^{1/2}\cdot L_m^{-1}=L_m^{-1/2},
\]

and exponent

\[
 \chi(a)=\frac34c_\gamma-\frac{d^2}{2a},
 \qquad
 \chi(65)=\frac{12191}{132088320}>0.
\]

Thus (X.40) proves endpoint lower bounds at the two distinct coordinates
(k_2-1=k_1) and (k_3-1=k_2), each normalized by the same (T_*).
Because all completed clocks are nonnegative, the two-coordinate
fixed-deletion pigeonhole is exact.

## 6. Section 8 packet-3 target-lobe dominance

The Section 8 dominance claim is sufficiently supported for the payment
lower bound.  It is not merely a diagonal assertion:

\[
 a_\times-3q=\frac{67}{242550}>0,
\]

\[
 \frac14a_\times+\frac34q
 =\frac{4601}{2910600}>0,
\]

and, for packet (1) on the packet-3 target lobe,

\[
 \frac9{16}a_\times+\frac{15}{16}q
 =\frac{32609}{11642400}>0.
\]

These are precisely the amplitude-weighted adjacent-outer,
adjacent-inner, and non-adjacent-inner margins needed for a three-packet
finite sum.  Negative partners are farther vertically, while (X.36) absorbs
all noncentral periodic copies.  Together with the inherited uniform
near-lobe lower bound, this proves full-sum dominance on the packet-3 lobe
throughout the retained (R^3)-length subinterval.  The lobe volume is
(asymp L_3R^3), so the exterior cubic row yields

\[
 P_R^M\ge
 c\mathfrak a_3^3\Gamma_3^{1/4}L_3R^4
 =cA_*^3R^4\Gamma_3^{-5/4}L_3^{-1/2}.
\]

This is an external nonnegative velocity-cubic payment; no cancellation or
signed-flux inference is used.

## 7. Payment normalization and independence of (A_*)

Taking the two-thirds power of the preceding lower bound and dividing by
(T_*=A_*^2R^2) cancels (A_*) exactly:

\[
 \frac{(P_R^M)^{2/3}}{T_*}
 \ge cR^{2/3}L_3^{-1/3}
       e^{(5/6)c_\gamma L_3^2}.
\]

Thus the revised Section 7 wording is correct: the forced ratio
((P_R^M)^{2/3}/T_*), rather than (P_R^M/T_*), is independent of the
common amplitude.  With (L_3^2=16L_1^2), its worst allowed exponential
rate is

\[
 \frac{40}{3}c_\gamma-\frac23a_S
 =\frac{3306805}{134120448}>0.
\]

The largest W-strip endpoint rate is (16\chi(66)), where

\[
 \chi(66)=\frac{15263}{134120448},
\]

and the strict rate gap is

\[
 \left(\frac{40}{3}c_\gamma-\frac23a_S\right)
 -16\chi(66)
 =\frac{3062597}{134120448}>0.
\]

## 8. Audit of (X.51)

Equation (X.51) does follow from the stated inputs.  The chain is:

1. The uniform relative comparison (X.37) gives, for sufficiently large
   scale, both a lower and an upper constant multiple of the free comparator
   for the actual full field on each audited strip.
2. The two-sided free-kernel estimates (the inherited W.16--W.18 bounds)
   give the upper endpoint scale
   (CT_*L_m^{-1/2}e^{\chi(66)L_m^2+CL_m}).
3. For (m=2,3), the largest exponent in (L_1^2)-units is
   (16\chi(66)).  The payment lower bound has the strictly larger rate
   computed above.  Its positive fixed gap absorbs every displayed
   polynomial and every (O(L_m)) transition correction.

Consequently

\[
 \frac{E_2^{\rm strip}+E_3^{\rm strip}}
 {(P_R^M)^{2/3}}\longrightarrow0.
\]

This is an upper bound only for the two explicitly integrated strip endpoint
contributions.  It is not an upper bound for either whole shell clock, for
accumulated dissipation, or for the fixed-deletion functional.

## 9. Formula, reference, and claim-boundary audit

The raw substring counts are indeed 62 occurrences of `\[` and 59 of
`\]`.  The three extra opening substrings are the table-spacing commands
`\\[4pt]`; they are not display delimiters.  Counting standalone delimiter
lines gives exactly 59 openings and 59 closings.  All tags X.1--X.52 are
unique and ordered, and every internal X-reference resolves.

The proved/not-proved boundary is internally consistent:

- exact three-packet NSE solution: proved for this smooth family;
- packet-2 and packet-3 relative survival: proved;
- two distinct (T_*)-normalized endpoint divergences: proved;
- simultaneous equal-time version: permitted and proved when that optional
  schedule is selected;
- fixed-deletion lower bound relative to (T_*): proved;
- payment-normalized W-strip route: proved insufficient;
- whole-shell clock upper/lower, accumulated-dissipation enhancement, and an
  actual counterexample to the payment-normalized fixed-deletion gate: open;
- arbitrary suitable weak solutions, regularity, singularity, or a
  Millennium conclusion: not addressed.

There are no blockers.  Publication should retain the candidate SHA above;
any byte change requires this audit to be rebound and re-run.

**NOT CLAY.**
