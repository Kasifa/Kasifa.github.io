# R0.73P critical-frequency gate figure

This is a source-complete, non-PDF preflight package for a three-panel formula
diagnostic. It is not a Navier--Stokes simulation and it is not a nonlinear
regularity certificate.

- Panel A compares the normalized band-limited thresholds
  \(N^{-3}\) and \(N^{-1/2}\).
- Panel B records the exact homogeneous Sobolev powers for one Fourier mode
  \(a_N=cN^{-\gamma}\): \(-\gamma\), \(1/2-\gamma\), and
  \(3-\gamma\).
- Panel C exhaustively evaluates the linear heat-semigroup lattice maximum
  \(\max_{k\in\mathbb Z^3\setminus\{0\}}|k|^3e^{-\tau|k|^2}\) on the
  configured \(\tau\)-grid and compares it with the continuous radial upper
  bound \((3/(2e\tau))^{3/2}\).

The current package deliberately omits `figure.pdf` and `qa-pdf.png`. The
non-PDF renderer cannot create either file. Consequently the package status is
`draft-preflight`, not `formal`; source-commit binding and PDF QA remain open.

Use the commands in `command.txt` from the repository root. `plot.py` defaults
to data-only generation. `--render-nonpdf` writes SVG, 600-dpi PNG, and the two
non-PDF QA rasters. `validate.py --preflight` checks the formula identities,
the exact finite lattice enclosure, the file inventory, hashes, and raster
dimensions. It also fails if any PDF is present during preflight.

The mathematical claim boundary is part of `contract.json`, `caption.md`, and
`chart-contract-and-source-data.md`. In particular, heat smoothing in Panel C
is a linear baseline only. It does not prove nonlinear entry into an
\(H^{1/2}\) or \(H^3\) stability tube.
