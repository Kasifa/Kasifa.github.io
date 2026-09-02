# R0.74O milestone recap delta — independent audit

## 1. Binding, method, and verdict

This audit treats the current recap delta as the object under review and does
not accept its summaries as premises.  It binds exactly

| Object | SHA-256 | Lines | Role |
|---|---|---:|---|
| `research/r074o_milestone_recap_delta.md` | `c12c7f3fb5a30656669bcc73dbfe654b675a77d44f327974575f469283c120c2` | 250 | recap delta under audit |
| `public/recap-r0-61-r0-73x.html` | `44e38b7a6855edfd92842d2c5eb75792e03f5fb1ca6de6902a1402dcbe0a3776` | 475 | historical public recap used as the structural baseline |

The review was fail-closed.  I checked every one of the 17 nodes against its
current proof, handoff, gap matrix, and independent-audit record where those
objects exist; independently recomputed the R0.74N/O displayed exponent
relations; reran the R0.74O Python certificate byte comparison and the
independent Ruby reconstruction; and separately audited route retirement,
evidence labels, open boundaries, research voice, and publication instructions.

**Verdict: PASS.**  No mathematical strengthening, lost quantifier, route-
boundary error, evidence-class collapse, or publication-scope mismatch was
found in the bound recap delta.  The text is suitable for use by the separate
task titled **发布任务**, subject to that task taking all deployment hashes,
figure status, and site counts from the final freeze/handoff and deployed
objects rather than from this prose summary.

## 2. Seventeen-node reconstruction

The range is exact: R0.73Y, R0.73Z, and R0.74A--R0.74O give 17 distinct nodes.

| Node | Independent source check | Recap result |
|---|---|---|
| R0.73Y | `r073y_exact_shear_no_go.md` proves an exact smooth mean-zero periodic NSE shear with pointwise-zero production and positive amplitude-unbounded covariance/size. | PASS: the production-only coercive bridge, not regularity, is retired. |
| R0.73Z | `r073z_finiteness_obstruction_and_repair.md` proves the initial-endpoint energy-class obstruction for \(\int D_s^{3/2}\) and the scale-critical, cubic, energy-compatible \(D_s\sqrt{k_s}\) repair. | PASS: the endpoint qualification and repaired observable are not conflated. |
| R0.74A | `r074a_localized_kd_size_lemma.md` localizes the mixed observable and exposes the velocity-endpoint, gradient, and pressure tails; its packet/time-spike tests are explicitly function-class tests rather than NSE trajectories. | PASS: the recap uses them only to reject the larger tail-free claim class. |
| R0.74B | `r074b_buffered_tail_closure.md` proves the strict-buffer, doubled-radius closure \(X\lesssim P^{2/3}+P\), with the pure \(2/3\) conclusion only for small payment. | PASS. |
| R0.74C | `r074c_advected_shear_large_payment_obstruction.md` gives exact smooth periodic NSE solutions with \(X_R/P_R^{2/3}\to\infty\) for the fixed-centre ledger. | PASS: the recap does not extrapolate this to a co-moving frame. |
| R0.74D | `r074d_zero_mean_local_transport_obstruction.md` gives the corresponding exact zero-total-mean 2D3C obstruction for the constant-global-mean frame. | PASS: only the “subtract global mean” repair is retired. |
| R0.74E | `r074e_local_mollified_frame_gate.md` separates moved-only M from moved-and-subtracted F, proves the transformation identities, and proves that nonzero acceleration cannot be hidden in periodic pressure. | PASS: the complete arbitrary-solution endpoints remain unstated. |
| R0.74F | `r074f_two_packet_survival.md` constructs the exact smooth periodic mean-zero unforced 2D3C family, fixes the zero trajectory/acceleration by symmetry, retains all periodic windings, and proves the terminal-lobe lower bound for every passive amplitude. | PASS. |
| R0.74G | `r074g_complete_payment_counterexample.md` proves \(P_j\lesssim B_j^3R_j^3\) at normalized amplitude while \(X_j\gtrsim B_j^2L_jR_j^2\), rejecting both frozen pure-\(P^{2/3}\) local-frame endpoints. | PASS: small-payment conclusions are preserved. |
| R0.74H | `r074h_collar_flux_two_regime_closure.md` proves the positive-cumulative-collar repair \(X_R^\alpha\lesssim (P_R^\alpha)^{2/3}+\mathfrak C_R^\alpha\), the coarser two-regime bound, and the small-payment endpoint. | PASS: no independent smallness of \(\mathfrak C\) is claimed. |
| R0.74I | `r074i_suitable_weak_tube_and_log_obstruction.md` transfers the Version-M two-regime estimate to periodic suitable weak solutions at a fixed admissible scale and proves the conditional one-scale moving-tube epsilon implication.  It rejects every fixed \(\gamma<1/2\) on the exact family while leaving \(\gamma=1/2\) open at that node. | PASS: the recap states all three restrictions. |
| R0.74J | `r074j_matching_payment_law.md` supplies the fifth-shell lower bound and closes \(P_j\asymp B_j^3R_j^3\) with \(\log P_j=(3/320)L_j^2+O(1)\). | PASS: this is identified as a familywise payment law. |
| R0.74K | `r074k_single_collar_shear_lag_reduction.md` proves strict free-heat exponent reserve on every deeper inward shell but an explicit positive-volume wrong-sign margin on the nearest inward shell. | PASS: only the free-heat proof mechanism is rejected; the true-packet upper is not. |
| R0.74L | `r074l_forward_bridge_bv_reduction.md` closes the main target collar by the common-forward-law and short-clock BV route. | PASS: the recap does not assign it the nearest-inner or all-shell theorem. |
| R0.74M | `r074m_final_segment_expulsion.md` closes the complete signed nearest-inward \(k=j-1\) row by final-segment true-shear expulsion. | PASS: packet cancellation is not invoked. |
| R0.74N | `r074n_all_shell_synthesis.md` combines all inward shells, inherits the target-shell estimate, sums the outer shells absolutely, and closes the full familywise collar condition. | PASS: the endpoint energy has matching two-sided control, whereas the dissipation component has only an upper bound. |
| R0.74O | `r074o_amplitude_endpoint_counterexample.md` uses the free passive amplitude to preserve the complete scalar payment while making both \(X\) and \(\mathfrak C\) grow quadratically, thereby refuting scalar-payment-only endpoint bounds. | PASS: augmented-observable theorems, singularity, global regularity, novelty, and priority remain open. |

The corresponding independent analytic audits all report PASS at their bound
source revisions.  In particular, the R0.74I weak-extension audit passes after
its recorded repair, the R0.74N all-shell audit preserves the dissipation-only
upper boundary, and the R0.74O amplitude audit binds the final proof, freeze,
and gap-matrix hashes.

## 3. Formula and quantifier audit

### 3.1 R0.74N boundary

The recap reproduces the all-shell theorem exactly:

\[
 \sup_{\tau\in I_{R_j}}[\mathcal I_j(\tau)]_+
 \le C\Gamma_jL_jR_j^5.
\]

Its normalized-family consequence is also exact:

\[
 X_j\asymp\mathfrak C_j
 \asymp B_j^2L_jR_j^2
 \asymp P_j^{2/3}\sqrt{1+\log_+P_j}.
\]

The prose then preserves the component statement

\[
 cT_j\le \mathcal U_{{\rm ext},j}^{\infty}
 \le X_j\le CT_j,
 \qquad
 0\le\mathcal D_{{\rm ext},j}\le CT_j,
 \qquad T_j=B_j^2L_jR_j^2,
\]

by saying that endpoint exterior velocity energy has matching two-sided
bounds and exterior dissipation has no matching lower bound.  It never turns
the latter upper bound into an equivalence.

### 3.2 R0.74O amplified frontier

The recap amplitude

\[
 \varkappa_j=L_j^{2/3}
 \exp\!\left(\frac{43}{1270080}L_j^2\right)
\]

is exact because

\[
 m=\frac{43}{423360},\qquad \frac m3=\frac{43}{1270080}.
\]

The payment identities remain

\[
 P_j^*\asymp B_j^3R_j^3,
 \qquad
 \log P_j^*=\frac3{320}L_j^2+O(1),
\]

and the independently recomputed exponents are

\[
 \delta_* = \frac{2m}{9\rho}=\frac{86}{11907},
 \qquad
 q_* = \frac23+\delta_*=\frac{8024}{11907}.
\]

Consequently the recap's two central displays are exact:

\[
 X_j^*\asymp\mathfrak C_j^*
 \asymp (P_j^*)^{8024/11907}
 (1+\log_+P_j^*)^{7/6},
\]

\[
 \frac{X_j^*}{(P_j^*)^{2/3}\sqrt{1+\log_+P_j^*}}
 \asymp
 \frac{\mathfrak C_j^*}{(P_j^*)^{2/3}\sqrt{1+\log_+P_j^*}}
 \asymp
 (P_j^*)^{86/11907}(1+\log_+P_j^*)^{2/3}\to\infty.
\]

Every large-payment comparator in the recap uses \(\log_+\).  The two bare
expressions \(\log P_j=(3/320)L_j^2+O(1)\) and
\(\log P_j^*=(3/320)L_j^2+O(1)\) are the intentional exact asymptotic payment
identities, not endpoint comparators.  The little-\(o\) statement is in the
large-payment paragraph following \(P_j^*\to\infty\), hence has the source
quantifier \(p\to\infty\):

\[
 \Phi(p)=o\!\left(p^{8024/11907}(1+\log_+p)^{7/6}\right).
\]

The fixed-logarithmic-power corollary also retains the critical quantifier
order: first fix \(\gamma\in\mathbb R\), then choose
\(M>\max\{0,\gamma-1/2\}\) and \(\varkappa_\gamma=L^M\).  The recap explicitly
states that the resulting family may depend on \(\gamma\); it does not claim
that one polynomial-amplitude sequence refutes every \(\gamma\) at once.

### 3.3 Finite reproduction

The Python Fraction producer regenerated a byte-identical current JSON.  The
independent Ruby Rational implementation reported

```text
RESULT: PASS (245/245 checks)
PASS 245/245
```

with certificate SHA-256
`30fd77ae3b4c88628e2d84207fc9b1728b1ab2343bf187fcd1141b080d6c5a5b`.
This supports the recap's FINITE count only; it is not used as proof of the
PDE, stochastic bridge, asymptotic theorem, or literature boundary.

## 4. Route-retirement and claim-boundary audit

All seven retired routes have the correct scope:

1. R0.73Y retires production-only coercivity, not a regularity criterion.
2. R0.73Z retires automatic initial-endpoint finiteness of the bare
   \(D_s^{3/2}\) observable, not its smooth interior use.
3. R0.74A's packet and time-spike tests retire the stated larger tail-free
   function class and are not represented as unforced NSE trajectories.
4. R0.74C and R0.74D retire, respectively, the fixed-centre and
   constant-global-mean repairs only.
5. R0.74G retires the frozen large-payment pure-\(P^{2/3}\) M/F inequalities
   while preserving the small-payment result.
6. R0.74K retires free-heat replacement on the nearest inner collar; R0.74L--N
   then close the true-dynamics familywise route.
7. R0.74O retires every fixed logarithmic correction at power \(2/3\) only
   when the right side depends on the frozen scalar payment alone.  The recap
   expressly excludes temporal, geometric, BV, Carleson, pressure, and flux
   observables from that no-go.

The evidence hierarchy is intact:

- **PROVED** contains the analytic exact-family, suitable-weak conditional
  gate, all-shell, and scalar no-go statements supported by their proofs and
  independent audits.
- **INHERITED** is restricted to prior framework/components and previously
  proved R0.74F--N inputs; it is not used to claim inherited novelty of the
  \(P/X/\mathfrak C\) asymptotics.
- **FINITE** is confined to arithmetic, exponent, metadata, and figure
  reproduction checks.
- **LITERATURE BOUNDARY** states only a bounded primary-source non-hit and
  explicitly denies novelty, priority, exhaustiveness, and publishability
  inference.
- **OPEN** retains augmented arbitrary-flow endpoints, weak stability and
  lower semicontinuity, prescribed good scales, payment-to-admissibility,
  the dissipation-component lower bound, arbitrary-data regularity or
  singularity, global smoothness, novelty, and priority.
- **NOT CLAY** is stated explicitly and no node count, certificate count, or
  route elimination is represented as Millennium-problem progress.

## 5. Next-route, voice, and publication audit

The four proposed gates for a new observable \(Y_R^\alpha\) are consistent
with the R0.74O necessity theorem and do not masquerade as proved sufficiency:

1. it must detect at least \(\varkappa_j^2B_j^2L_jR_j^2\) along the amplified
   exact family;
2. it must not merely rename \(\mathfrak C\);
3. it must be meaningful and stable enough at suitable-weak regularity; and
4. it must connect to a good/small scale at a possible singular point before
   it can support regularity.

The recap correctly labels
\(\widehat P=P+\mathfrak C^{3/2}\) as an identity-level safe payment rather
than an independent smallness mechanism.

Research choices are written in first-person singular (for example, “我没有把
这座桥当作既成事实” and “下一阶段我应冻结”), while theorem statements use
neutral mathematical prose.  No collective “我们” voice or novelty slogan is
introduced.

Finally, the update instruction is complete and correctly separated from
research work: **发布任务** must preserve the R0.61--R0.73X historical recap,
add all 17 nodes and the four new phases, rebuild counts from the final tree,
derive hashes and figure status from the final R0.74O handoff/freeze, generate
synchronized HTML/PDF from one audited source, update the home page and full
index, retain local translation without DGX, deploy only through GitHub Pages,
and byte-check the live page, PDF, primary figure, and home page.  A successful
push or green Actions run alone is expressly insufficient.

No public HTML, PDF, home page, or deployment object was modified by this
audit.

\[
 \boxed{\text{R0.74O MILESTONE RECAP DELTA: INDEPENDENT PASS; NOT CLAY.}}
\]
