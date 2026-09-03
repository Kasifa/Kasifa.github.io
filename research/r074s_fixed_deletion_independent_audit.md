# R0.74S Step 18 — independent Ruby audit

- Schema: r074s-fixed-deletion-independent-audit-v1
- Source note: research/r074s_fixed_deletion_simultaneous_height.md
- Source SHA-256: 305bf75f978c080a1790fbc42bb9bd725f56f537785ffe0fc45e3ca815aa5dc1
- Literature SHA-256: fea7470814c0c21399c6e2b25961e8b3791e584cc24612ac37e9d1be7ce707ce
- Independent groups: 8/8
- Exact assertions: 72144

## Verdict

**PASS**

The Ruby verifier is implementation-independent from the Python producer.
It recomputes all finite functional identities with Rational arithmetic
and checks the frozen source, literature, dependency, and primary-result
contracts.

## Group inventory

| Group | Result | Assertions |
|---|---:|---:|
| independent_minimax_hierarchy | PASS | 34854 |
| independent_layer_cake | PASS | 36408 |
| independent_completed_clock_payments | PASS | 36 |
| independent_triangular_clock_values | PASS | 769 |
| independent_fixed_N_ledger_obstruction | PASS | 54 |
| independent_source_structure | PASS | 9 |
| independent_hash_locks | PASS | 5 |
| independent_primary_certificate_contract | PASS | 9 |

## Analytic audit boundary

For each fixed deletion set S, Step 10 S.235 and Step 15 r <= z give

\[
 \sum_{k\notin S}K_k(\tau)
 \le \Pi_R^{\boldsymbol\lambda}
      +6\sum_{k\notin S}z_k(\tau)
\]

at every common good terminal time.  Continuity of the K vector into
\(\ell^1\) and density of the common good-time set close only the left
side to all terminal times; no continuity of the hybrid stops is assumed.
Taking the supremum for that same S and then the infimum proves S.484.

The converse target-scale comparison follows from
\(z_k(\tau)\le K_k(\tau)+\operatorname{TV}Q_k\).  Neither direction
proves that the common finite deletion exists with a quadratic bound.

## Claim boundary

- The triangular-clock strictness is abstract only.
- The Taylor compatibility screen uses R chosen after N as in S.451.
- The fixed-deletion and completed-clock gates remain open.
- Q.12, Q.1, scale contraction, regularity, and the Millennium problem remain open.

## Failures

None.
