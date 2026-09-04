# R0.75N certificate QA report

- Verdict: **PASS**
- Mathematical blockers: 0
- Python assertions: 16/16
- Ruby assertions: 17/17
- Negative mutations rejected: 107/107 Python; 107/107 Ruby
- Unknown mutations rejected fail-closed by both implementations: PASS
- PYTHONHASHSEED byte stability: PASS (0, 1, 42)
- Canonical JSON and both generated reports are regeneration-stable: PASS

## Release manifest

| path | SHA-256 |
|---|---|
| research/r075n_radial_collar_averaged_wiener_row.md | ba59a4df399d8580b35d8dbb3f0758f9d2ffcc7f97f1147e5804c428f3740318 |
| research/r075n_radial_collar_averaged_wiener_row_primary_audit.md | c43c063b1c003be22782e7d8e1ce0b3f42cdd3ef4d01912c9de34c876d8c9aba |
| research/r075n_report-source.md | ae9d5d630ee0549193c016fcbc07c599b0c678fbaf9c15c5d3c7f24bdf18e27c |
| scripts/r075n_radial_collar_averaged_wiener_row_fixtures.json | 2dee2146f94f3fa6d0d0c5828d8d6f354f0856f620e1261a133c9a2c81f8a0cb |
| scripts/r075n_radial_collar_averaged_wiener_row_expected.json | 31614fc11bc4355723fff7773bec8ab13bc44808ffffa0958c78ec1cfe2bba48 |
| scripts/r075n_radial_collar_averaged_wiener_row_certificate.py | 47256d34a25a188a32147e4cb9f0388819238f2c854e1e814612b9bfd217950e |
| scripts/r075n_radial_collar_averaged_wiener_row_certificate_independent.rb | 63836294b2924433afa0e95d07baee6427446c7c26c14a34dcd9a5818e0fed56 |
| scripts/r075n_radial_collar_averaged_wiener_row_qa.sh | 568b7934a403e076fb51ae0f18b142547f621a1a514c6ced14e01635c540c66e |
| research/r075n_radial_collar_averaged_wiener_row_certificate.json | 891774ec5c7e747a4f9c172f0b71e4f6f2af40d8a983bc7c69ebbd1756f405d7 |
| research/r075n_radial_collar_averaged_wiener_row_certificate_report.md | cad991130fb614d923c224a891001010119a746f9d32c1d17d0fbc5f6c56c0b5 |
| research/r075n_radial_collar_averaged_wiener_row_independent_audit.md | 779d359b62c2860a07e8889826d038d88cad8356af9c53ce31f5bfd1d85441b6 |

The primary audit is checked against the frozen main SHA, PASS/0,
N.1--N.17, and 17/17 displays. The report-source is byte-bound only;
its literature search and access record are outside this finite certificate.

## Frozen dependency bindings

| path | SHA-256 |
|---|---|
| research/r075b_bulk_clock_outer_padding_gate.md | 430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a |
| research/r075c_background_shear_packing_false_positive.md | 1f72f3c9d9d348f86188206690ce714df28aed661a9192c7b53bc1e5921f2f89 |
| research/r075e_horizontal_cross_mode_flux_reduction.md | 99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049 |
| research/r075m_dyadic_packet_diffusive_flux_gain.md | 13434bbc15eabecd5a695eceef01a7d63415e96511b14c29cc8abcd1297c7bf7 |

## Checks

- B leaves cutoff choice freedom; the radial collar is a selectable canonical cover, not universal necessity: PASS.
- Fourier normalization 1/(2*pi), d_ell=+i*ell*Xi_ell, and d_0=0: PASS.
- Low/high sampling split, two integrations by parts, tail O(R), and sum_l sup_z order: PASS.
- Exact disk slices, including tangencies, satisfy the uniform 4*pi*a*delta cap: PASS.
- Radial first/third derivatives and Fubini L1 bounds O(a) and O(a^2): PASS.
- x1/full averaging scales R/R^2; Wiener rows are O(a) and O(Ra^2): PASS.
- K>=R^(-3/2) yields K^(-2/3)<=R and outputs LR and L^2R^2: PASS.
- Tags N.1--N.17, references, 17/17 displays, dependencies, and control bytes: PASS.

This certifies only the selected canonical geometric coefficient rows.
It proves neither a universal cutoff statement nor a dynamical flux theorem.
Vertical diffusion, nonconstant shear, local cubic payment, inter-packet
summation, low differences, E.24, complete clock, fixed deletion,
suitable-weak transfer, regularity, and singularity remain OPEN. **NOT CLAY.**
