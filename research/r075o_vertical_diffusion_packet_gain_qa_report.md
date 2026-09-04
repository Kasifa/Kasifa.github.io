# R0.75O certificate QA report

- Verdict: **PASS**
- Mathematical blockers: 0
- Python assertions: 19/19
- Ruby assertions: 20/20
- Negative mutations rejected: 132/132 Python; 132/132 Ruby
- Unknown mutations rejected fail-closed by both implementations: PASS
- PYTHONHASHSEED byte stability: PASS (0, 1, 42)
- Canonical JSON and both generated reports are regeneration-stable: PASS

## Release manifest

| path | SHA-256 |
|---|---|
| research/r075o_vertical_diffusion_packet_gain.md | 3efb39d2624cf5b5a0e7f348f6cde2ef2416eca900f1aa3ecc90a6ad734849a9 |
| research/r075o_vertical_diffusion_packet_gain_primary_audit.md | 27f9341f93bd2b031dbd3fd0e8d745788d5ff36a085ddb8be4ef8e1c5553e69b |
| research/r075o_report-source.md | 9d2c234b0ba2a33b0f573a7933c26bcc751db6fe85919f2e146a0e6a18128c2b |
| scripts/r075o_vertical_diffusion_packet_gain_fixtures.json | 46dff6097c3a052dc968f1c712c3421105ea5be51d3c905c492cc463cc04f0ad |
| scripts/r075o_vertical_diffusion_packet_gain_expected.json | 228ac56e500a32b1f7c64c04d4110c78c4105c4d2a997fa8b108bd7449d59833 |
| scripts/r075o_vertical_diffusion_packet_gain_certificate.py | a92864e15193139d2bfe4dd352c8a398bbe2dc2942fa0e3c2820331cb45f6e05 |
| scripts/r075o_vertical_diffusion_packet_gain_certificate_independent.rb | 33d0c8d15b34e8638160548b287f4db3acbae734b4523f09a700d0c66650f917 |
| scripts/r075o_vertical_diffusion_packet_gain_qa.sh | 084cf638304a98360aecbcefb1d074f8d67aef00c1fb2c49bfd3602db4b8496e |
| research/r075o_vertical_diffusion_packet_gain_certificate.json | 71a737b18d67cd01d494abfd0485b42fd78fce9a8bc2085931e17e2aa4be8055 |
| research/r075o_vertical_diffusion_packet_gain_certificate_report.md | 32267743fcfea2a88c5b971912db9f18dd76725b39bba5bf674bd920a8573379 |
| research/r075o_vertical_diffusion_packet_gain_independent_audit.md | 51fc9e834dbdc525b2c75c9430a87d1e8504666f7a65b0ac9e86a22baeb7dac7 |

The primary audit is byte-bound and checked for PASS/0. By its explicit
design it delegates the final main SHA binding to this certificate.
The report-source is byte-bound; literature completeness is outside this finite suite.

## Frozen dependency bindings

| path | SHA-256 |
|---|---|
| research/r075e_horizontal_cross_mode_flux_reduction.md | 99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049 |
| research/r075g_signed_flux_gain_threshold.md | f2b3424dddb7eee5938200c3433cd012a1820564e43ad446e0c88d8dfa39ff41 |
| research/r075m_dyadic_packet_diffusive_flux_gain.md | 13434bbc15eabecd5a695eceef01a7d63415e96511b14c29cc8abcd1297c7bf7 |
| research/r075n_radial_collar_averaged_wiener_row.md | ba59a4df399d8580b35d8dbb3f0758f9d2ffcc7f97f1147e5804c428f3740318 |

## Checks

- O.9 difference index, sign, 2*pi pairing, outer pi*B, and d_0 cancellation: PASS.
- Arbitrary vertical-frequency heat contraction and Schur row/column bounds: PASS.
- Horizontal Parseval and exact energy coefficient 1/4: PASS.
- Total-frequency cap, K^2*T>=1, T^2 Holder, and O.17 constants: PASS.
- (16*pi)^(2/3)/4=(2*pi)^(2/3) and no vertical cardinality loss: PASS.
- Normalization R^(1/3)omega^(1/3)K^(-2/3)p^(2/3): PASS.
- Strict kappa*=98605/71442 and frozen exponent -4279/238140000: PASS.
- O.1--O.24, references, 24/24 displays, four dependencies, and control bytes: PASS.

O.1 allows arbitrary vertical frequencies only for the quadratic-energy row.
The cubic conversion retains a total-frequency cap and K^2*T>=1.
O.24 controls one packet against its own full-T^2 atom, not Version-M.
Collar localization, nonconstant shear, inter-packet and low-difference control,
cap removal, E.24, complete clock, fixed deletion, suitable-weak transfer,
regularity, and singularity remain OPEN. **NOT CLAY.**
