# R0.75M certificate QA report

- Verdict: **PASS**
- Mathematical blockers: 0
- Python assertions: 19/19
- Ruby assertions: 20/20
- Negative mutations rejected: 130/130 Python; 130/130 Ruby
- Unknown mutations rejected fail-closed by both implementations: PASS
- PYTHONHASHSEED byte stability: PASS (0, 1, 42)
- Canonical JSON and both generated reports are regeneration-stable: PASS

## Release manifest

| path | SHA-256 |
|---|---|
| research/r075m_dyadic_packet_diffusive_flux_gain.md | 13434bbc15eabecd5a695eceef01a7d63415e96511b14c29cc8abcd1297c7bf7 |
| research/r075m_dyadic_packet_diffusive_flux_gain_primary_audit.md | 2b5ee050c09e3be925143c12c29082c3fe562a83b9a2d2669511a2bb1684d7dc |
| research/r075m_report-source.md | f8ed7af8ef5051b0efa73177d0530562917d55dfa6476b00b8f871db0da99d67 |
| scripts/r075m_dyadic_packet_diffusive_flux_gain_fixtures.json | b93d727b4bf0729af2064e51fbc0c1450d98806c9b92fe11727b4d5423fa157f |
| scripts/r075m_dyadic_packet_diffusive_flux_gain_expected.json | cef1705998bc935448f371d6f389d46059b59e99bf230bd75dad0489fb85a4f4 |
| scripts/r075m_dyadic_packet_diffusive_flux_gain_certificate.py | 8a55852a3eabcf8989feadcb25cb178db57b1dccbd2249e73d48e61e7755811b |
| scripts/r075m_dyadic_packet_diffusive_flux_gain_certificate_independent.rb | 6436063bc4ec623dfc27d7fc3edee8ee6751784f8a43ecdd5aa1b4170b35dd1b |
| scripts/r075m_dyadic_packet_diffusive_flux_gain_qa.sh | 9e61cb0e57f4116e371beda1d6709ca479ea146538758287d6451b2641e87cf2 |
| research/r075m_dyadic_packet_diffusive_flux_gain_certificate.json | 1794cee5294ed55a41697f74d6a4b0bbb5e31e59b3a74ed11f277d0ae8e17423 |
| research/r075m_dyadic_packet_diffusive_flux_gain_certificate_report.md | cd2882d59ec90471d1e74cb135426490c46863fbf6e6df3db3532926aaa5002f |
| research/r075m_dyadic_packet_diffusive_flux_gain_independent_audit.md | 507fdbb899f0e74abccc0477405949ca07f9379d4b20ce20ab3bd87e63a76881 |

The primary audit is checked against the frozen main SHA, PASS/0,
M.1--M.20, and 20/20 displays. The report-source is byte-bound only;
its literature search and access record are outside this finite certificate.

## Frozen dependency bindings

| path | SHA-256 |
|---|---|
| research/r075e_horizontal_cross_mode_flux_reduction.md | 99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049 |
| research/r075g_signed_flux_gain_threshold.md | f2b3424dddb7eee5938200c3433cd012a1820564e43ad446e0c88d8dfa39ff41 |
| research/r075l_single_harmonic_diffusive_signed_flux_gain.md | 52e25b2fdf1a224609c9e8fafa1c041b7f09a361f75f4b3e44ebcdddb756cdf5 |

## Checks

- Fourier convention, 2*pi spatial pairing, pi*B kernel, and d_0 cancellation: PASS.
- Schur row/column bounds, Parseval, no mode-count factor, and exact 1/4: PASS.
- Short-time L2/L3 factors and cubic lower bound: PASS.
- Inversion 4e(2*pi)^(1/3) and combined e(2*pi)^(1/3): PASS.
- Wiener--H1 weighted Cauchy--Schwarz and first/second derivative row: PASS.
- Normalization R^(1/3)omega^(1/3)K^(-2/3)p^(2/3): PASS.
- Strict threshold 27163/71442 and small-R power direction: PASS.
- Tags M.1--M.20, references, 20/20 displays, and control bytes: PASS.

The result covers arbitrary finite interference within one real dyadic packet
only. Inter-packet summation, cutoff Wiener calibration, collar/local Version-M
payment, nonconstant shear, low differences, E.24, complete clock, fixed
deletion, suitable-weak transfer, regularity, and singularity remain OPEN.
**NOT CLAY.**
