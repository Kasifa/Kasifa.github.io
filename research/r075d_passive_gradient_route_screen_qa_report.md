# R0.75D certificate QA report

- Verdict: **PASS**
- Python assertions: 20/20
- Ruby assertions: 23/23
- Negative mutations rejected: 41/41 Python; 41/41 Ruby
- Unknown mutations rejected fail-closed by both implementations: PASS
- PYTHONHASHSEED byte stability: PASS (0, 1, 42)
- Canonical JSON and both generated reports are regeneration-stable: PASS

## Release manifest

| path | SHA-256 |
|---|---|
| research/r075d_passive_gradient_route_screen.md | 54bcd703aff9a55f8fff522ded2bf1c5b629ee2497bd4f2255a6224e4bb747f6 |
| research/r075d_report-source.md | 5c415c3e280fea1569a42d64d99400fe4dfaf440d2808d637ca57cfc1d386c1f |
| research/r075d_passive_gradient_route_screen_primary_audit.md | f06e29971ea3f0b05c7a1c39983a2ae21aa241a8e46f02e2450632e07c5eaef7 |
| scripts/r075d_passive_gradient_route_screen_certificate.py | 5a79cafe4c7794367b23447cdfc09ba0ee49536e756074aa28aa219173fb0823 |
| scripts/r075d_passive_gradient_route_screen_certificate_independent.rb | 1a8066cfc4fe90266ff38163a60e752988699b21871482308bb307455be3b090 |
| scripts/r075d_passive_gradient_route_screen_qa.sh | 2c3b9e359b41f27733b29e301b105c56e73b2435e8d1c7f40a6615cdcef19557 |
| research/r075d_passive_gradient_route_screen_certificate.json | 9222dfa3c7051fbe7d5d78405f6ad8071e54b4eed736cd2afae97f96f617c639 |
| research/r075d_passive_gradient_route_screen_certificate_report.md | 24dfb6fa2ce6e1bce280a34a4f16c0d7aa84e75e08fb2408d7c4edae78f506a1 |
| research/r075d_passive_gradient_route_screen_independent_audit.md | 1b1c5e6ba1826b291d7fc649ac0db0cf1e5ae91ce3e8800d36c3ffce5f395439 |

The report-source file is hash-bound in this QA release manifest only.
Its literature content and the recorded HTTP status are outside the
finite arithmetic producer and independent Ruby verifier.
The primary audit is also release-bound and was checked for the frozen
main hash, PASS with zero blockers, and D.1--D.23 coverage.

## Certificate-side dependency boundary

| path | SHA-256 |
|---|---|
| research/r075b_bulk_clock_outer_padding_gate.md | 430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a |
| research/r075c_background_shear_packing_false_positive.md | 1f72f3c9d9d348f86188206690ce714df28aed661a9192c7b53bc1e5921f2f89 |

The main note has no embedded frozen-source table. These two hashes are
certificate-side bindings and are not represented as main-file rows.

## Checks

- Tags D.1--D.23, local references, B/C references, and 23/23 displays: PASS.
- D.4--D.7 Holder/R/L/omega/K powers and K-low exact rate: PASS.
- Modal equation, norm versus squared-norm damping, and zero-mode obstruction: PASS.
- D.10--D.11 forcing sign and exact Laplacian dissipation: PASS.
- Transition-band volume, short-block threshold, and intermediate gap: PASS.
- D.16--D.23 transport, pF/pB normalizations, mixed homogeneity, and exact rate: PASS.
- Small-payment direction and non-absorption on the frozen large-payment branch: PASS.
- Commutator, periodic-weight, interaction, and counterexample boundaries remain OPEN: PASS.

The exact fallback is P^(2/3)+P and closes only the small-payment regime.
The frozen branch has P tending to infinity; the linear term is not
absorbed. No exact counterexample or complete-clock result is
certified. **NOT CLAY.**
