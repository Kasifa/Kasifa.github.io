# R0.69I localized strain-pressure commutator certificate

This archive locks the exact weighted pressure-orthogonality and Betchov
identities from
`research/localized_strain_pressure_commutator_note.md` to source commit
`b03985d6d2fd1f55ba5d600cb75859efb694876b`.

## Reproduce

From the repository root:

    tmp/r068b-venv/bin/python research/run_with_monitor.py \
      --output research/certificates/r069i/resources.csv --interval 0.05 -- \
      tmp/r068b-venv/bin/python \
      research/localized_strain_pressure_commutator_audit.py \
      --source-commit b03985d6d2fd1f55ba5d600cb75859efb694876b \
      --output \
      research/certificates/r069i/localized-strain-pressure-commutator.json

The certificate contains 14 checks, all passed. Exact Fourier convolution
gives the nonzero localized values

    integral phi S:H            = -676/40425,
    integral phi tr(A^3)        =  228/2695,

while both unweighted global pairings are exactly zero. The certificate also
checks the two weighted integration-by-parts identities, the pointwise cubic
reduction, the pressure Poisson equation, divergence freedom, and scaling
degree three for every localized commutator.

The monitored run took 5.04 seconds, with 73 process-tree samples, a maximum
observed CPU utilization of 100%, and a peak resident set size of 73.469 MiB.
It was an exact, deterministic, CPU-only audit; GPU execution would not
improve the evidence.

## Decision boundary

The result closes only bare cutoff localization as a source of sign or scale
gain. It does not rule out estimates that add harmonic-tail, multiscale,
Morrey, or geometric information. It gives no Navier--Stokes regularity or
singularity conclusion and does not solve the Millennium Problem.
