# R0.76J certificate QA report

- Verdict: **PASS**
- Mathematical blockers: 0
- Independent mathematical rereads: PASS (2 lanes; blockers 0)
- Python assertions: 96/96
- Ruby assertions: 107/107
- Negative mutations rejected: 96/96 Python; 107/107 Ruby
- Unknown mutations rejected fail-closed by both implementations: PASS
- PYTHONHASHSEED byte stability: PASS (0, 1, 42)
- Independent Laguerre series/recurrence samples and tail margin: PASS
- Exact 20/19, 250/19, 1000/19, 2000/19 constant ledger: PASS
- Exact 5sqrt(2), 10sqrt(2), 20sqrt(2) exponent ledger: PASS
- q=o(L^(5/2)) and normalized -2/11907 rate ledger: PASS
- J.1--J.46, 48 displays, reference closure, hashes, and claim boundary: PASS
- Generated-output hash-cycle guard: PASS
- AGENTS.md excluded from bindings, inventory, and release manifest: PASS
- Canonical outputs regeneration-stable: PASS
- Exact core inventory: 12/12 files (11 manifest rows plus this self-generated QA report)

## Release manifest

| path | SHA-256 |
|---|---|
| research/r076j_local_edge_extrapolation_reconstruction.md | a3d67c8a27ef6ffb7068313732e8e8a08ba98931226df726ac4ee2140ab0f57f |
| research/r076j_local_edge_extrapolation_reconstruction_primary_audit.md | 1b2a608c6ffe16c35489b95fd384f0f47a1d4a79b22491a7825ac53382a746d5 |
| research/r076j_report-source.md | 371eac6e3f053d4ba51ded16f35024ba805d10c5a81c1f01879704ce583763c7 |
| scripts/r076j_local_edge_extrapolation_reconstruction_fixtures.json | f0957b65e763339d1ff8cc029a13e13231b22b44dff8796b3b21883ffb352c31 |
| scripts/r076j_local_edge_extrapolation_reconstruction_expected.json | 9e5ad2f9bed318cd1232319240d2e574f070eda0364f97957df9c013f35878e8 |
| scripts/r076j_local_edge_extrapolation_reconstruction_certificate.py | ed969fa1730597ecf33bc530ec1e40509080730f0a59552a1309182cd698f771 |
| scripts/r076j_local_edge_extrapolation_reconstruction_certificate_independent.rb | ab58a7e8d77434de9ef363b04c43a612d5b61e0504faf82299783f7ea1b171f3 |
| scripts/r076j_local_edge_extrapolation_reconstruction_qa.sh | d6364ed1896264a21173b2feb6b98e9b34522686d6300bd8066ef9dda18f0538 |
| research/r076j_local_edge_extrapolation_reconstruction_certificate.json | 23db36bc873a47e1992c9650e5ea04c5c1874f2e2a0bd17b6353bcb4452be89f |
| research/r076j_local_edge_extrapolation_reconstruction_certificate_report.md | a6c140ca114e73d975eff57de1804d85ba59fa080720fd5ac17e05d1bf7896d2 |
| research/r076j_local_edge_extrapolation_reconstruction_independent_audit.md | 63231761c982914b79e9e3eac271e3602737222fae41b30ea347941eaad056c7 |

## Boundary

The certificates audit a finite arithmetic, source, equation, and hash ledger.
They do not prove Plancherel, the continuum theorem, the imported literature,
or Navier--Stokes regularity or singularity. **NOT CLAY.**
