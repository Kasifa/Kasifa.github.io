# R0.63 time-layer transfer certificate

This directory archives the exact transfer regression and six hostile-target
stress tests used in R0.63.

## Proven algebra checked by the audit

- the fixed-time three-ordering path sum equals the three weighted polynomial
  coefficients in the R0.63 note;
- the two-state Rudin--Shapiro recursion lifts exactly to eight cubic states;
- adding the target sign gives the natural sixteen-state closure, with carry
  shifts `-1, 0, 1, 2`.

The mathematical note, audit program, and test were committed at
`54898a2ba78e48ac075f6613ae6af5d77ce4f28d`.  The six numerical probes used the
unchanged R0.61 long-double path scanner from checkout
`4dfefb222d9be1b235fe1a3de140305e3083d317`.

## Finite evidence

The probe files evaluate the heat-weighted quartic sum at the target where the
ordinary unweighted cubic correlation is maximal for each listed `M`.  The
largest run contains 28,977,859,974 ordered paths.  All probe files identify
themselves as long-double evaluations and explicitly state that they are not
proofs.

## Boundary

This certificate does not prove `|S4,m| <= C L^2 M`, all-index positivity,
complete Picard control, or the Navier--Stokes Millennium problem.  It
certifies the exact transfer reduction and preserves the finite stress-test
inputs for the next operator-norm calculation.

`SHA256SUMS` covers this README, the six raw probe records, and the generated
transfer audit.  The checksum file does not hash itself.
