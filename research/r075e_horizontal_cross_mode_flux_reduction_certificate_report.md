# R0.75E reproducibility certificate report

- Verdict: **PASS**
- Assertions: 13/13
- Main SHA-256: 99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049
- Tags and displays: 24/24
- Finite real-pair example T/pi: -1/2
- Negative mutations declared: 39

## Frozen dependencies

- research/r075b_bulk_clock_outer_padding_gate.md: 430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a (main table row present)
- research/r075c_background_shear_packing_false_positive.md: 1f72f3c9d9d348f86188206690ce714df28aed661a9192c7b53bc1e5921f2f89 (main table row present)
- research/r075d_passive_gradient_route_screen.md: 54bcd703aff9a55f8fff522ded2bf1c5b629ee2497bd4f2255a6224e4bb747f6 (main table row present)

## Certified finite checks

For Xi(x)=2+cos(2x)+sin(2x) and F(x)=2cos(x)+sin(x), all Fourier
coefficients lie in the rational complex numbers. Direct Laurent
multiplication gives T/pi=-1/2. The independently assembled E.10 mode sum
also gives T/pi=-1/2. Diagonal terms and the zero mode give zero. A nonzero
complex singleton also gives zero but violates the real-field pairing,
whereas the real +/-1 pair gives a nonzero flux.

The certificate additionally recomputes every L, R, omega, pF, and pB
power in E.14--E.16, E.21, and E.23; checks the endpoint and transport
sign; binds the B/C/D source table; and verifies all 24 tags, references,
displays, and boundary sentinels.

The finite Laurent witness certifies the algebraic normalization in E.10;
it is not asserted to be a full E.1 spacetime trajectory or the actual
geometric collar cutoff.

The all-payment result is confined to the real horizontal zero-mode
subclass for L>=L0. The nonzero complex singleton is algebraic only, and a
real +/-n pair is not forced to vanish. E.24 for arbitrary real fields,
complete-clock extraction, fixed deletion, suitable-weak transfer, and
regularity remain OPEN. No Clay conclusion is certified. NOT CLAY.
