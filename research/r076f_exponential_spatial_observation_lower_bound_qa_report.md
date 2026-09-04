# R0.76F certificate QA report

- Verdict: **PASS**
- Mathematical blockers: 0
- Independent mathematical audit: PASS (blockers 0; alpha-rule fixture correction closed)
- Python assertions: 83/83
- Ruby assertions: 83/83
- Negative mutations rejected: 83/83 Python; 83/83 Ruby
- Unknown mutations rejected fail-closed by both implementations: PASS
- PYTHONHASHSEED byte stability: PASS (0, 1, 42)
- Python/Ruby exact section and mutation inventory: PASS
- Canonical outputs regeneration-stable: PASS
- Exact core inventory: 12/12 files

## Release manifest

| path | SHA-256 |
|---|---|
| research/r076f_exponential_spatial_observation_lower_bound.md | 48204fcbf8fe9af3f0fdc7720844c3dd8362d8767caf73de016eda7250b70973 |
| research/r076f_exponential_spatial_observation_lower_bound_primary_audit.md | abcaa220c56d1f90c4b34061191e7cd009b8d911be3f83d705e95aa51b4d84cc |
| research/r076f_report-source.md | 5e3939710dcfefcbc08b93761d8cdda1e655656a1bcd404b63fcea251ffd5e1e |
| scripts/r076f_exponential_spatial_observation_lower_bound_fixtures.json | 1b11049ab482eb9b6d6b99cfdabfb4cd0a34ac4f483e3e69c5ec178dce752b5a |
| scripts/r076f_exponential_spatial_observation_lower_bound_expected.json | 9703be8236b77e556085f9b358f4128ace4e32920a5391ebc1e2a900b232d37a |
| scripts/r076f_exponential_spatial_observation_lower_bound_certificate.py | 2882146fba7376d1f2d83d324c816b763729c59443fa4cb1f5fbcc47778c6994 |
| scripts/r076f_exponential_spatial_observation_lower_bound_certificate_independent.rb | 191b7ee7c0e7ed9157a33606c0ed00e3d0bd1db374260b26d8d5d5b64807bf32 |
| scripts/r076f_exponential_spatial_observation_lower_bound_qa.sh | ba4fb4db589a502fa28f4f4d307a46b046b5fe253e12e57487c5da0c52d51546 |
| research/r076f_exponential_spatial_observation_lower_bound_certificate.json | 0558eab8a7ce5ae36e1614fe0c2184debfa8550c655a86baab590fbb9ee6f259 |
| research/r076f_exponential_spatial_observation_lower_bound_certificate_report.md | 7de8bb9ce8b59704c4097616a14e09366c8cc9031acf2e2692b51bce9a785ea0 |
| research/r076f_exponential_spatial_observation_lower_bound_independent_audit.md | 8b90a9ab9b60a17f6e5cfc097f658c80ce4cb410142d72123b72bef6895ab7de |

## Checks

- F.1--F.18, display balance, references, UTF-8, CR, trailing whitespace, and prose screen: PASS.
- Exact q=4 sample: modes 4--7, binomial amplitudes 1,3,3,1, dyadic endpoint 7<=8: PASS.
- At delta=2pi/3, x=pi/6 and sin(3x)/sin(x)=2, giving the exact lower bound 2^3=8: PASS.
- Spatial-only, no-full-flux-lower-bound, literature, open-problem, and NOT CLAY boundaries: PASS.
- Formal scientific figure: not applicable; no simulation claim is made.

Finite certificates audit the exact ledger; they are not the continuum proof.
