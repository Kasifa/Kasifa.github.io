# fig-r071g-residence-gate

This formal double-column figure separates three distinct conclusions from
R0.71G:

1. signed low-shell work in the exact global-smooth 2D3C family can remain
   positive for arbitrarily many viscous times as the coupling tends to zero;
2. fixed positive relative levels in the same family retain the critical
   viscous scale;
3. critical residence alone does not convert a \(K^{-2}\)-weighted heat bulk
   into an unweighted bottom trace.

## Reproduction

Run the commands in `command.txt` from this directory.  The archived
`data.csv` contains 5292 rows.  `generate_data.py` uses fixed-step complex
RK4 on the exact reduced sideband chain with \(|m|\le24\); it does not step a
3D PDE.  `independent_validate.py` compares the figure events with a separate
adaptive DOP853 checker at radii 12 and 18 and verifies the archival formats.

The formal outputs are `figure.pdf`, `figure.svg`, and the 600 dpi
`figure.png`.  `qa-original.png`, `qa-grayscale.png`, and `qa-report.md`
record the print-size and non-color checks.  `manifest.json` and
`SHA256SUMS` bind the files to this package.

## Compute boundary

The package was generated on the local Mac workstation with one process and
binary64 arithmetic.  No random seed is needed.  No DGX or GPU resource was
used.  This is a reduced-chain computation, not DNS, not fitted data, and not
3D PDE time stepping.

## Claim boundary

The arbitrary-duration sign result is proved by the analytic Duhamel estimate
in `research/r071g_report-source.md`; the finite curves are checks of the
exact reduced chain.  The relative-level curves apply only to this
global-smooth family.  Panel D is an abstract functional obstruction, not an
NSE trajectory.  The figure proves no general occupation law, singularity,
regularity theorem, originality, or Millennium-problem claim.
