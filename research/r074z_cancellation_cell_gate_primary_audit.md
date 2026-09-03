# R0.74Z independent primary analytic audit -- cancellation-cell gate

## 0. Frozen object, verdict, and blockers

This audit reads the candidate byte-for-byte as

```text
research/r074z_cancellation_cell_gate.md
SHA-256 bb766da4002da760c35185294081f80df97c349ea08b198a5f76db31663aaf6a
bytes 28070
```

The seven inherited source hashes printed in Section 1 were recomputed from
the live files and all agree with the table in the candidate.

**Verdict: PASS.**  The exact common-shear algebra, the two successive
fourth-root weight shifts, the spacetime Hölder coercivity, and every displayed
rational identity checked below are correct.  The time-tame endpoint-to-tube
upgrade is correctly stated only as a conditional lemma requiring its
moving-neighborhood derivative envelope and all-winding uniformity.  The
candidate now keeps both the critical residence layer and the full completed-
clock Y.57 branch open.

**Blocker count: 0.**

Two previously dangerous inference boundaries were checked especially
closely and are handled correctly in the frozen candidate.

1. **Critical residence.**  Equations (Z.16)--(Z.19a) claim a strict no-go at
   exponential rate only when

   \[
   \limsup_{L\to\infty}\kappa_L<\kappa_*.
   \]

   The candidate explicitly says that \(\kappa_L=\kappa_*+o(1)\) is not
   decided by the rate calculation and places it in the open second branch of
   (Z.39).  No equality-case conclusion is asserted.

2. **The coercivity theorem compares payment with the strip kinetic floor
   \(h\), not with the full completed clock \(K\).**  Even when
   \((P_R^M)^{2/3}/h\to\infty\), the desired inequality
   \((P_R^M)^{2/3}=o(K)\) is not excluded unless one additionally proves, for
   example,

   \[
   K_{k_2-1,R}(t_2)\le e^{o(L^2)}h,
   \]

   or proves that any larger accumulated-dissipation contribution creates a
   matching payment.  The boxed verdict (Z.2), the proof-status ledger, and the
   final paragraph all preserve this distinction: only the W-kinetic route is
   conditionally blocked, while the full-clock Y.57 cell remains OPEN.

These are open boundaries, not blockers, because the candidate labels them as
such and does not use them to prove a stronger theorem.

No claim in this audit concerns arbitrary suitable weak solutions, regularity,
or singularity.  **NOT CLAY.**

## 1. Exact common-shear admissibility

Let

\[
\mathcal L_bF=(\partial_t+b(t,x_3)\partial_2-\Delta_{23})F,
\]

where the frozen odd shear satisfies
\(\partial_tb-\partial_3^2b=0\).  If \(F\) solves \(\mathcal L_bF=0\), then

\[
F^-(t,x_2,x_3):=-F(t,-x_2,-x_3)
\]

satisfies

\[
\begin{aligned}
\mathcal L_bF^-(t,x_2,x_3)
={}&-\partial_tF(t,-x_2,-x_3)
 +b(t,x_3)\partial_2F(t,-x_2,-x_3)\\
&+\Delta_{23}F(t,-x_2,-x_3)=0,
\end{aligned}
\]

because \(b(t,-x_3)=-b(t,x_3)\).  Hence arbitrary real linear
combinations of finitely many same-\(b\) solutions and their inversion
partners solve the same passive equation.  The paired sum is inversion odd
and therefore has zero spatial mean.

For

\[
u=(U,b,0),\qquad U=U_{\rm primary}+C,
\]

one has \(\nabla\cdot u=0\) and

\[
\partial_tu+u\cdot\nabla u-\Delta u
=
(\mathcal L_bU,\,\partial_tb-\partial_3^2b,\,0)=0.
\]

Thus (Z.6)--(Z.8) give an exact smooth periodic unforced Navier--Stokes
solution with constant pressure, which may be taken to be zero.  Negative
corrector coefficients are admissible.  This part passes.

The commutators are also correct:

\[
[\partial_2,\mathcal L_b]=0,
\qquad
[\partial_3,\mathcal L_b]=(\partial_3b)\partial_2.
\]

Consequently a horizontal derivative/translate is exact, whereas a vertical
derivative of an already evolved packet need not be.  For a literal time
translate \(\widehat C(t)=C_0(t-\tau)\), direct substitution gives

\[
\mathcal L_b\widehat C
=\bigl[b(t,x_3)-b(t-\tau,x_3)\bigr]
  \partial_2C_0(t-\tau,x),
\]

so (Z.9)--(Z.10) also pass.  Re-centred vertical data and time-offset data
must indeed be re-evolved under the same actual coefficient \(b(t,x_3)\).

## 2. Clock and doubled-radius payment weights

The physical shell for the outer remote witness is \(k=k_2-1\).  Since the
frozen weights satisfy

\[
\gamma_{j-1}=\gamma_j^{1/4},
\]

and \(\Gamma=\gamma_{k_2}\), its endpoint clock weight is exactly

\[
\omega=\gamma_{k_2-1}=\Gamma^{1/4}.
\]

At radius \(2R\), the same physical annulus is

\[
A_{k_2-1}(R)=A_{k_2-2}(2R).
\]

Therefore the exterior payment weight on it is

\[
\gamma_{k_2-2}
=\gamma_{k_2-1}^{1/4}
=\omega^{1/4}
=\Gamma^{1/16}.
\]

This confirms (Z.11)--(Z.12).  In particular, reusing
\(\Gamma^{1/4}\) as the doubled-radius payment weight at the remote shell
would be wrong; the candidate does not make that error.

The one-sided moving strip (Z.12a) has the advertised volume

\[
2\left(\frac14\sqrt{pL}R\right)
\left(\frac14R\right)
\left(\frac12R\right)
=\frac1{16}\sqrt{pL}\,R^3.
\]

Its use requires the chosen one-sided interval to remain in \(I_R\) and the
constant in \(|Q_2(t)|\le c_0R\) to be smaller than the fixed shell margins.
Those restrictions are consistent with the “fixed sufficiently small”
choice in Section 3.1, but should be retained whenever the lemma is invoked.

## 3. Hölder spacetime payment and its exponential rate

From (Z.14), for almost every \(t\in J\),

\[
\int_{\Omega(t)}|u|^2\,dx\ge\frac{2Rh}{\omega}.
\]

Spatial Hölder and
\(|\Omega(t)|\le C_\Omega L^\nu R^3\) then give

\[
\begin{aligned}
\int_{\Omega(t)}|u|^3\,dx
&\ge |\Omega(t)|^{-1/2}
\left(\int_{\Omega(t)}|u|^2\,dx\right)^{3/2}\\
&\ge cC_\Omega^{-1/2}L^{-\nu/2}
h^{3/2}\omega^{-3/2}.
\end{aligned}
\]

Restricting the nonnegative exterior row to the moving tube and using
\(|J|=\theta_LR^3\) and \(W_{2R}\ge\omega^{1/4}\) yields

\[
\begin{aligned}
P_R^M
&\ge(2R)^{-2}\omega^{1/4}
\int_J\int_{\Omega(t)}|u|^3\,dx\,dt\\
&\ge cC_\Omega^{-1/2}\theta_Lh^{3/2}
R\omega^{-5/4}L^{-\nu/2}.
\end{aligned}
\]

Taking the two-thirds power proves exactly

\[
(P_R^M)^{2/3}
\ge cC_\Omega^{-1/3}\theta_L^{2/3}h
R^{2/3}\omega^{-5/6}L^{-\nu/3}.
\]

Thus the powers of \(R\), \(\omega\), \(L\), and \(\theta_L\) in
(Z.15)--(Z.16) all pass.  The argument uses the total velocity on the tube,
so no summandwise noncancellation hypothesis is hidden in this lemma.

Now

\[
\frac{\log R}{L^2}=-\frac\rho4,
\qquad
\frac{\log\omega}{L^2}=-\frac{c_\gamma}{4},
\qquad
\frac{\log\theta_L}{L^2}=-\kappa+o(1).
\]

Consequently

\[
\liminf_{L\to\infty}\frac1{L^2}
\log\frac{(P_R^M)^{2/3}}h
\ge
\frac5{24}c_\gamma-\frac\rho6-\frac23\kappa,
\]

which verifies (Z.18).  The cancellation of the primary amplitude and of
the remote Gaussian deficit is genuine because the same total kinetic mass
appears quadratically in \(h\) and cubically in the payment.

## 4. Exact rational ledger

Using

\[
c_\gamma=\frac8{3969},\qquad
\rho=\frac9{10000},\qquad
d=\frac7{32},\qquad
\mathsf a_0=\frac{131}{2},
\]

independent exact reduction gives

| quantity | recomputation | reduced value | status |
|---|---:|---:|---|
| remote Gaussian field rate \(\beta\) | \(d^2/(4\mathsf a_0)\) | \(49/268288\) | PASS |
| time-tame reserve | \(\rho/4-\beta\) | \(7103/167680000\) | PASS |
| remote payment gap \(\Delta_{\rm rem}\) | \((5/24)c_\gamma-\rho/6\) | \(64279/238140000\) | PASS |
| residence threshold \(\kappa_*\) | \((3/2)\Delta_{\rm rem}\) | \(64279/158760000\) | PASS |
| two-centre target rate | \(d^2/(2\mathsf a_0)\) | \(49/134144\) | PASS |
| excess over \(1/5000\) | \(49/134144-1/5000\) | \(13857/83840000\) | PASS |
| escape-complexity coefficient | \(\rho/4-\beta+\kappa_*\) | \(476239/1064835072\) | PASS |

Every number declared positive is positive.  In particular,

\[
\Delta_{\rm rem}
=\frac5{24}\frac8{3969}-\frac16\frac9{10000}
=\frac{64279}{238140000}>0,
\]

and the coefficient in (Z.36) is exactly the sum of the persistence reserve
and \(\kappa_*\), not a decimal fit.

## 5. The critical-residence boundary

Put

\[
\kappa_L:=-\frac1{L^2}\log\theta_L
\]

after absorbing only explicitly controlled subexponential factors.  The
coercivity calculation supplies

\[
\frac1{L^2}\log\frac{(P_R^M)^{2/3}}h
\ge \frac23(\kappa_*-\kappa_L)+o(1).
\]

This proves exponential domination if

\[
\limsup_{L\to\infty}\kappa_L<\kappa_*.
\]

It does not prove domination when \(\kappa_L\to\kappa_*\).  For example,
if \(\kappa_L=\kappa_*-L^{-2}\), the displayed exponential contribution is
only a bounded factor, while the explicit \(L^{-\nu/3}\) term can still
decay.  Unspecified \(o(L^2)\) transition errors are likewise decisive at
equality.

Therefore (Z.19) is correct as a **necessary leading-rate condition** for a
payment-compatible escape, but not as an equality-case theorem.  The frozen
candidate states the proved sequence form precisely in (Z.19a):

\[
\limsup_{L\to\infty}\kappa_L<\kappa_*.
\]

It also explicitly records that the critical layer
\(\kappa_L=\kappa_*+o(1)\) is not decided because polynomial and
\(o(L^2)\) terms can then control the sign.  The first branch of (Z.39) uses
the same strict limsup hypothesis, and the second branch includes the
critical layer.  This quantifier audit passes.

## 6. Time-tame endpoint persistence

On the moving remote neighborhood, assume the uniform total-corrector bound

\[
R^2|\mathscr D_2C|
\le |\mathfrak a_2|e^{o(L^2)},
\qquad
\mathscr D_2=\partial_t+Q_2'(t)\partial_2,
\]

and the uniform endpoint estimate

\[
\sup_{x\in\mathcal S_{\rm rem}^{+}(t_2)}
|C(t_2,x)|=o(\mathcal A_{\rm rem})
\]

on a fixed enlargement of the strip.  Along a moving-frame characteristic,
an interval of length \(cR^3\) produces the relative variation

\[
\begin{aligned}
\frac{|C(t,x)-C(t_2,x_2-Q_2(t)+Q_2(t_2),x_3)|}
{\mathcal A_{\rm rem}}
&\le C R
\exp[\beta L^2+o(L^2)]\\
&=\exp[-(\rho/4-\beta)L^2+o(L^2)]\\
&\longrightarrow0.
\end{aligned}
\]

The exact reserve \(7103/167680000>0\) verifies (Z.24).  Provided the
primary W comparison is uniform on the same fixed moving enlargement, a
slightly shrunken strip retains its kinetic floor through a fixed multiple of
\(R^3\).  This proves (Z.25) under the stated uniform hypotheses.

The quantifier is important.  “Fixed/subexponential complexity” is sufficient
only when **all** of the following are absorbed in the
\(e^{o(L^2)}\) envelope: family size, coefficient condition number,
normalized spatial profile, and normalized moving-frame time derivative.
Subexponential cardinality alone does not imply (Z.22).  The candidate states
this qualification explicitly, especially in Sections 4 and 6.

Thus fixed numbers of comparable-age \(R\)-width Gaussian packets with
coefficient-tame profiles, and polynomial Hermite/finite-difference orders
with polynomial conditioning, do fall under the conditional persistence
lemma.  An exponentially ill-conditioned family does not.

## 7. Two-centre Gaussian interpolation

For the equal-age free vertical Gaussian, division by the primary gives

\[
\frac{H_s(\eta)}{G_2(\eta)}
=\exp\!\left(\frac{2\eta s-s^2}{4\mathsf a_0}\right).
\]

The remote strip has

\[
\eta=\frac{x_3-h_2}{R}
=-dL+[-1,-1/2].
\]

Taking \(s=-dL+O(1)\), and normalizing the restoring Gaussian at one remote
point, makes its target-to-remote ratio

\[
\exp\left[-\frac{d^2}{2\mathsf a_0}L^2+O(L)\right].
\]

The exact leading rate is

\[
\zeta_{\rm 2c}=\frac{49}{134144}
>\frac1{5000}.
\]

Thus the two-point interpolation arithmetic in (Z.27)--(Z.28) passes.
However,

\[
\partial_\eta\log(H_s/G_2)
=\frac{s}{2\mathsf a_0}
=-\frac7{4192}L+O(1).
\]

Across the fixed width \(1/2\) of the remote strip, the ratio therefore
changes by an \(e^{\Theta(L)}\) factor.  It cannot be uniformly
\(1+o(1)\) there.  The conclusion in (Z.29) is correct for the one-restoring-
centre ansatz.  The text also correctly declines to extend this elementary
argument to arbitrarily many, arbitrarily ill-conditioned centres.

## 8. Complexity escape coefficient and its scope

Make the factor in Section 7 explicit by writing

\[
R^2|\mathscr D_2C|
\le |\mathfrak a_2|\mathcal N_Le^{o(L^2)}
\]

uniformly on the moving neighborhood.  Endpoint preservation then guarantees
at least

\[
\theta_L\gtrsim
\min\left\{1,
\frac{\exp[(\rho/4-\beta)L^2+o(L^2)]}{\mathcal N_L}
\right\}.
\]

If \(\log\mathcal N_L=n_LL^2\), avoiding a strict subcritical residence
rate requires

\[
n_L\ge \frac\rho4-\beta+\kappa_*+o(1)
=\frac{476239}{1064835072}+o(1).
\]

This validates (Z.35)--(Z.36) as a **necessary leading exponential-rate
condition**, not a sufficient construction.  It rigorously excludes fixed or
polynomial family size/order only when their total normalized conditioning and
derivative envelope are also subexponential.  The candidate correctly puts
exponentially large coefficients inside \(\mathcal N_L\).

At the equality coefficient, the same critical-layer caveat from Section 5
applies.  The estimate does not classify a family with

\[
\log\mathcal N_L
=\frac{476239}{1064835072}L^2+o(L^2).
\]

The narrow-width discussion (Z.37) is explicitly heuristic for general
finite sums, and the need for a cancellation-robust spectral observability
estimate is correctly left open.

## 9. Full-clock boundary and no-go scope

The deterministic theorem gives, schematically,

\[
(P_R^M)^{2/3}\ge A_Lh,
\]

where \(A_L\to\infty\) under a strict subcritical residence rate.  The
endpoint clock satisfies only

\[
K_{k_2-1,R}(t_2)\ge h.
\]

These inequalities do **not** order \((P_R^M)^{2/3}\) and
\(K_{k_2-1,R}(t_2)\).  It is logically possible under the displayed
estimates that

\[
K_{k_2-1,R}(t_2)/h
\]

grows faster than \(A_L\), for example because the accumulated ordinary
viscosity row is large.  That possibility may itself incur central-energy or
exterior payment, but the required lower bound is exactly part of the open
next proposition; it is not contained in (Z.15)--(Z.25).

Accordingly the following narrower statement is proved:

\[
\boxed{
\begin{gathered}
\text{A time-tame corrector cannot turn the persistent W-type remote}\\
\text{kinetic strip witness alone into a clock-over-payment counterexample}\\
\text{when its residence exponent stays strictly below }\kappa_*.
\end{gathered}}
\]

The following stronger statement is not yet proved:

\[
\boxed{
\text{No time-tame correction cell can satisfy the full Y.57 ratio.}}
\]

To promote the first box to the second, one needs either a full-clock upper
bound relative to \(h\) at exponential scale or a theorem coercing every
additional accumulated row into \(P_R^M\).  The frozen candidate does not
claim either missing theorem: (Z.2), the two boundary bullets after (Z.19a),
the proof-status ledger, and the closing paragraph all keep the complete
Y.57 clock OPEN.  Its no-go language is confined to the W-kinetic witness
under the time-tame and moving-strip hypotheses.  This scope audit passes.

## 10. Endpoint-only and analyticity boundaries

The candidate correctly keeps arbitrary finite, exponentially
ill-conditioned, endpoint-focused families OPEN.  In particular:

* a number of correctors that is finite for each \(R\) may still grow like
  \(e^{cL^2}\);
* qualitative unique continuation does not propagate
  \(e^{-\zeta L^2}\) target smallness without a quantitative frequency or
  global-norm bound;
* an endpoint value alone supplies no uniform \(R^3\) residence interval;
* an arbitrary network need not expose one individually identifiable
  corrector lobe in the total field.

The exact-vanishing analyticity observation in Section 5.4 is consistent for
the stated positive-time heat-kernel/derivative-heat class, provided spatial
analyticity under the actual common shear is invoked.  It should not be read
as a theorem for every arbitrary smooth solution introduced abstractly in
Section 2.  This is a presentation/support qualification, not a blocker for
the Hölder coercivity result.

The endpoint-only branch therefore remains OPEN, as required.  The proposed
spectral/observability dichotomy is the correct kind of next problem, but its
first branch must exclude the unresolved critical layer and its second branch
must control the complete clock/payment ledger.

## 11. Mechanical and provenance audit

The live inherited hashes were recomputed as follows:

| source | observed SHA-256 | status |
|---|---|---|
| `research/r074p_temporal_observable_triage.md` | `a3cb872735b92b32ddfa7b96bc4184d70b0287ff2ce7d3da8cadbbcc494d0867` | MATCH |
| `research/r074q_common_shear_multipacket_gate.md` | `60cb683ff6b602b16d64313b278c11a08d73f89e3bc2b1562b256a9911695695` | MATCH |
| `research/r074q_relaxed_multipacket_cubic_obstruction.md` | `ba8897da349aa5c71c5ac355164a938599489c2691b09eb59760934b70617e8d` | MATCH |
| `research/r074t_schedule_invariant_dwell_coercivity.md` | `8d56a66ff918fe1c25056617468022379b71ab37bacff2650599194501ea4fbd` | MATCH |
| `research/r074w_remote_adjacent_inward_comparison.md` | `d818db13acc16ad26a2d9628f2681e4a654698c9966815dd6cf1712813830d10` | MATCH |
| `research/r074x_three_packet_fixed_deletion_gate.md` | `4fdc9558605afd9557c557c4292ca1af50d52ff54f9aa11603f15c97a97b3ee3` | MATCH |
| `research/r074y_payment_compatible_route_screen.md` | `6144fe796d6c59a286fc32b3b0aa2b794c50006fdc7879d4595b5958c9646954` | MATCH |

The candidate contains 42 unique display tags, from (Z.1) through (Z.39)
including (Z.12a)--(Z.12b) and (Z.19a); no duplicate tag was found.  Display delimiters,
`aligned` environments, and `gathered` environments are balanced.  No hidden
control character was found.

## 12. Final audit disposition

The audit disposition is therefore:

\[
\boxed{
\begin{gathered}
\textbf{EXACT WEIGHTS, CUBIC COERCIVITY, AND FRACTIONS: PASS;}\\
\textbf{STRICTLY SUBCRITICAL PERSISTENT W-KINETIC NO-GO: PASS;}\\
\textbf{CRITICAL RESIDENCE LAYER: OPEN;}\\
\textbf{FULL Y.57 CLOCK AND CRITICAL LAYER: CORRECTLY LEFT OPEN;}\\
\textbf{ARBITRARY FINITE ENDPOINT-FOCUSED FAMILY: OPEN.}
\end{gathered}}
\]

Overall verdict: **PASS**, with blocker count \(0\).  The word “conditional”
in the candidate describes an explicitly assumed moving-strip lemma; it is
not being promoted to an unconditional theorem.
No novelty, regularity, singularity, or Millennium conclusion is audited or
claimed.  **NOT CLAY.**
