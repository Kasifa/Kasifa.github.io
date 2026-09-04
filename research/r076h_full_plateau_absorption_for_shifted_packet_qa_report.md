# R0.76H certificate QA report

- Verdict: **PASS**
- Mathematical blockers: 0
- Independent mathematical rereads: PASS (2 audits; blockers 0)
- Python assertions: 126/126
- Ruby assertions: 126/126
- Negative mutations rejected: 126/126 Python; 126/126 Ruby
- Unknown mutations rejected fail-closed by both implementations: PASS
- PYTHONHASHSEED byte stability: PASS (0, 1, 42)
- Python/Ruby exact section and mutation inventory: PASS
- Canonical outputs regeneration-stable: PASS
- Exact core inventory: 12/12 files (11 hash-bound manifest rows plus this self-generated QA report)

## Release manifest

| path | SHA-256 |
|---|---|
| research/r076h_full_plateau_absorption_for_shifted_packet.md | 11490112a1893400a1099dd9f45b906ce78d7dab1ebcf549eaa7870241dc0ef4 |
| research/r076h_full_plateau_absorption_for_shifted_packet_primary_audit.md | 91e1f31f3adf19a9f352a8cd6defc8988971e51f0905e4a634f949223992c58d |
| research/r076h_report-source.md | 3e706ae12caace1118f941f92c85bc0a1a11ed4a6e158acf7258918a67616d87 |
| scripts/r076h_full_plateau_absorption_for_shifted_packet_fixtures.json | 035ff9b04f61c11744668c51e6fd8ef1e35da93de85fab2bd9b971acca79747d |
| scripts/r076h_full_plateau_absorption_for_shifted_packet_expected.json | f80cc1d8b6673a6f18069d6756f605de821ac661561d11295a40c468532e083b |
| scripts/r076h_full_plateau_absorption_for_shifted_packet_certificate.py | 65cd03fa1420eaffbf1a0e795d178b13b46829f79811963a724f2c25a9c72b2f |
| scripts/r076h_full_plateau_absorption_for_shifted_packet_certificate_independent.rb | 4b1d72ad23b82eb48eef6df96d98bb904aa8f72e4932724ac72557c881c46cb3 |
| scripts/r076h_full_plateau_absorption_for_shifted_packet_qa.sh | eea1b5f41b4c3959d1bdab214dc4c3b07fa05a0ca0f9a659c7ed8fa4fc565a02 |
| research/r076h_full_plateau_absorption_for_shifted_packet_certificate.json | 452e46b75a10d7fcb637d85234e1d3f76c471cd4ea1cec6b69b568260a8ff55e |
| research/r076h_full_plateau_absorption_for_shifted_packet_certificate_report.md | d9c80bc4af24f7f55046e2b5d13484841d3c430232c586913c10b23cbd425267 |
| research/r076h_full_plateau_absorption_for_shifted_packet_independent_audit.md | f3d301f7b29cd1d5ceb89604d4b14d306e3f1fb47c35a5cce1cd689fc8b16fbd |

## Checks

- H.1--H.39, displays, references, UTF-8, CR, trailing whitespace, and prose screen: PASS.
- Exact shell cross-section, aR^5 Jacobian, adjacent strip, and terminal-box powers: PASS.
- Exact m=4 moment coefficients, derivative, cap comparison exponents, and dyadic sample modes: PASS.
- Complete signed-flux positivity and two-sided full-plateau bounds: PASS.
- Raw 3/40000 and normalized -2/11907 logarithmic rates: PASS.
- Explicit-packet-only, arbitrary-packets-open, source, and NOT CLAY boundaries: PASS.
- Formal scientific figure: not applicable; no simulation claim is made.

Finite certificates audit the exact ledger; they are not the continuum proof.
