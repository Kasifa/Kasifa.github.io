# R0.73I finite action-boundary figure

This package renders a 178 mm two-panel journal figure from the formal
finite diagnostic in `experiments/r073i/`.

Panel A shows the finite Fourier--Galerkin values
`A_N(D)/D` at cutoffs `N=24,48,96`, together with the rigorous continuum
numerical-abscissa upper bound
`c_H(0)=sqrt(19/180)` and the inherited rate reference `0.17035`.  Its
broken y axis is explicit: the upper-bound reference is far above the
magnified finite-action band.  `D_ub=sqrt(19/180)/392` is only a strict
upper bound for the existential `d0`, and `1/450` is a legacy comparison
outside the inherited theorem endpoint.

Panel B shows
`R_{Lambda,48}(D)-C_48(D)`, where
`R=log G_{Lambda,48}-Lambda A_48`.  The `Lambda^-1` segment is a visual
slope guide, not a fit, not a regression, and not an error bound or
asymptotic theorem.

`source-data.csv` is a lossless plotted-data extract.  Every row records
its upstream path, SHA256 digest, and row key.  The figure therefore remains
auditable even though the source experiment and this package may be committed
in a later release transaction.

Run `command.txt` from the repository root.  The archival masters are
`figure.pdf`, `figure.svg`, and `figure.png`; the PNG is 600 dpi.  The QA
surfaces are `qa-final-size.png`, `qa-grayscale.png`, and `qa-pdf.png`.
`validate.py` independently checks the numerical extract, dimensions,
formats, grayscale contrast, hashes, and fail-closed claim boundary.

All plotted colored marks and curves are finite binary64 diagnostics only.
They do not prove a continuum branch, a Fourier tail bound, a matching gain
action, or any Navier--Stokes regularity conclusion.
