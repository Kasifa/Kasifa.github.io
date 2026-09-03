# Primary mathematical audit of R0.75I

## 0. Frozen object and verdict

Audited file:
`research/r075i_diffusion_safe_block_participation.md`.

Frozen SHA-256:
`c8511690dc52988b3f3715e589379c72dae0a892dcabd8d0ca218dddbe0fd3a7`.

**Verdict: PASS. Mathematical blocker count: 0. Release blocker count: 0.**

The note proves an algebraic one-block flux estimate for arbitrary fields
and an exact aggregation ledger in terms of a cubic participation count.
It does not prove that the frozen passive solution has small participation,
does not close E.24, and does not assert a Navier--Stokes regularity result.

The five frozen inputs recompute as

| input | SHA-256 |
|---|---|
| `research/r075b_bulk_clock_outer_padding_gate.md` | `430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a` |
| `research/r075c_background_shear_packing_false_positive.md` | `1f72f3c9d9d348f86188206690ce714df28aed661a9192c7b53bc1e5921f2f89` |
| `research/r075e_horizontal_cross_mode_flux_reduction.md` | `99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049` |
| `research/r075g_signed_flux_gain_threshold.md` | `f2b3424dddb7eee5938200c3433cd012a1820564e43ad446e0c88d8dfa39ff41` |
| `research/r075h_single_pass_transport_flux_closure.md` | `849379bea9cf22e0d892ac11ac05bb3b3bc2967a1735753dbc4a6ffc7bb7d7b9` |

## 1. One-block scale audit, I.5--I.14

On `Q_j=J_j times supp partial_2 xi`, the frozen bounds give

\[
 |Q_j|\lesssim (R^3)(L^2R^3)=L^2R^6
\]

and

\[
 |b\partial_2\xi|\lesssim R^{-2}R^{-1}=R^{-3}.
\]

Hence spacetime Holder yields

\[
 \begin{aligned}
 \frac\omega R|\mathcal T_j|
 &\lesssim \frac\omega R R^{-3}
 (L^2R^6)^{1/3}
 \left(\int_{Q_j}|F|^3\right)^{2/3}\\
 &=L^{2/3}\omega R^{-2}
 \left(R^2\omega^{-1}p_j\right)^{2/3}\\
 &=L^{2/3}\omega^{1/3}R^{-2/3}p_j^{2/3}.
 \end{aligned}
\]

This confirms every power in I.13.  The estimate uses only the pointwise
coefficient bounds, cylinder measure, and Holder.  It is valid for an
arbitrary measurable `F` with finite cubic integral; neither the transport
nor the advection--diffusion equation is silently invoked.

With

\[
 \log R/L^2=-\rho/4,
 \qquad
 \log\omega/L^2=-c_\gamma/4,
\]

the one-block coefficient has rate

\[
 -\frac{c_\gamma}{12}+\frac\rho6
 =-\frac{4279}{238140000}<0.
\]

## 2. Participation identity and finite inequalities, I.15--I.17

For nonnegative `p_j` and `p_A=sum_j p_j>0`, set

\[
 S_{2/3}:=\sum_jp_j^{2/3}.
\]

Subadditivity gives `S_(2/3)>=p_A^(2/3)`, so
`N_eff=S_(2/3)^3/p_A^2>=1`.  Holder for finite sums gives

\[
 S_{2/3}\le |A|^{1/3}p_A^{2/3},
\]

so `N_eff<=|A|`.  Moreover, the definition gives the exact identity

\[
 S_{2/3}=N_{\rm eff}^{1/3}p_A^{2/3}.
\]

The aggregate positive part satisfies

\[
 \left[\sum_j\mathcal T_j\right]_+
 \le\sum_j|\mathcal T_j|,
\]

so insertion of the one-block bounds proves I.17 without assuming common
sign.  Three exact diagnostics are consistent:

- one nonzero atom gives `N_eff=1`;
- `m` equal positive atoms give `N_eff=m`;
- atoms `(1,8)` give `N_eff=125/81`, strictly between `1` and `2`.

The last example rejects replacing `N_eff` by the number of merely nonzero
blocks as an identity.

## 3. Threshold audit, I.19--I.23

Under `N_eff<=C R^(-theta)`, the coefficient is

\[
 L^{2/3}\omega^{1/3}R^{-(2+\theta)/3}.
\]

Its exact exponential rate is

\[
 \frac{\rho(2+\theta)-c_\gamma}{12}.
\]

Strict negativity is equivalent to

\[
 \theta<\frac{c_\gamma}{\rho}-2
 =\frac{80000}{35721}-2
 =\frac{8558}{35721}.
\]

At equality the exponential rate vanishes, while `L^(2/3)` diverges, so
the strict sign in I.22 is necessary for this route.  The active-fraction
conversion gives

\[
 \beta=1-\theta>
 1-\frac{8558}{35721}
 =\frac{27163}{35721},
\]

exactly matching R0.75G.

## 4. Full-clock obstruction, I.24--I.26

An `O(R^2)` clock contains `O(R^(-1))` disjoint `O(R^3)` blocks.  Equal
payment across them has `N_eff asymp R^(-1)`, so `theta=1`.  The coefficient
then reduces to

\[
 L^{2/3}\omega^{1/3}R^{-1},
\]

with rate

\[
 \frac\rho4-\frac{c_\gamma}{12}
 =\frac{27163}{476280000}>0.
\]

Thus the note correctly rejects summing the favorable one-block estimate
over every block.  No favorable full-clock conclusion is inferred from a
negative one-block rate.

## 5. High-participation zero-flux audit, I.27

For `F=f_0(t,x_3)`, both `b|F|^2` and `eta_R` are independent of `x_2`.
Fubini and periodicity give

\[
 \int_{\mathbb T_{x_2}}\partial_2\xi\,dx_2=0
\]

for every fixed `(x_1,x_3)`, hence `mathcal T_j=0` on every block.  A
persistent nonzero zero mode may still have comparable `p_j>0` throughout
the clock, which gives `N_eff asymp R^(-1)`.  The main note therefore
correctly treats I.19 as a sufficient condition for the absolute
block-summation route, not as a necessary condition for E.24.  High
participation is neither an E.24 counterexample nor proof of a flux
obstruction.

## 6. Source and claim-boundary audit

The source report accurately separates literature context from the local
proof:

- Albritton--Dong treat passive advection--diffusion with divergence-free
  drift and identify bounded total speed as a special borderline class;
- Hu--Li provide a Davies-method off-diagonal framework for regular
  Dirichlet forms;
- Aronson supplies the classical Gaussian fundamental-solution context.

None is represented as proving I.19, E.24, or the Version-M ledger.  The
one-block theorem is derived in the main note rather than attributed to an
external result.  The bounded search is not promoted to novelty evidence.

## 7. Structural audit and final boundary

- Equation tags I.1--I.27 are unique and consecutive.
- Every internal I-reference resolves.
- All 27 display-math environments are paired.
- The five frozen input hashes match.
- The main note and source report contain no disallowed control bytes.
- The theorem is explicitly arbitrary-field and diffusion-safe, not an
  assertion that diffusion controls participation.
- `N_eff<=CR^(-theta)` remains a conditional dynamical input.
- Large `N_eff` is explicitly not presented as a counterexample or a
  necessary obstruction.
- E.24, complete-clock extraction, fixed deletion, suitable-weak transfer,
  regularity, and singularity remain open.
- No simulation, numerical fit, priority, or Clay claim is made.

The R0.75I mathematical claims are internally consistent and ready for an
independent finite certificate.  **NOT CLAY.**
