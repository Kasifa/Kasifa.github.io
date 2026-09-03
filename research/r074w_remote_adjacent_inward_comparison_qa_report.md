# R0.74W certificate QA report

- Python: PASS, 33/33 checks, 33 cases.
- Independent Ruby: PASS, 6/6 groups, 56 assertions.
- Python mutations: 23/23 rejected.
- Ruby mutations: 24/24 rejected.
- PYTHONHASHSEED 0, 1, 42 and Ruby regeneration: byte-identical.
- Syntax, UTF-8, controls, delimiters, tags/references, JSON and scoped diff whitespace: PASS.

## Frozen inputs

- Main: `d818db13acc16ad26a2d9628f2681e4a654698c9966815dd6cf1712813830d10`
- Primary audit: `66ec78f67bba64c555a92e9a616c477d702ebb200b48bbfc08a353bdfde5bb73`
- Literature audit: `ec6259d95990fd6a8357d9685cc3f17e300e672c1add911a5eb64c6291f3bb99`

## Boundary

**FINITE EXACT ARITHMETIC/STRUCTURE ONLY.** No analytic Brownian-bridge lemma, whole-shell or fixed-deletion theorem, novelty result, regularity result, singularity result, or Clay claim is proved by this QA.
