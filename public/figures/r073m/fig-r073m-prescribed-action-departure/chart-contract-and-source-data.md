# R0.73M chart contract and source-data note

## Analytical question

On the sealed 15-case finite grid, does the gain remain bounded after
normalization by the separately computed finite inviscid action proxy, do the
registered \(a/b/c\) coefficients exhibit the expected
\(1,\varepsilon,\varepsilon^2\) hierarchy, and do the requested numerical
discrepancy families remain below their frozen gates?

## Supported finite takeaway

The plotted finite values place \(g^{(0)}_{N,\varepsilon}\) in a narrow
order-one band for all three cutoffs, place both registered coefficient ratios
on an order-one scale at \(N=64\), preserve the negative signed alignment of
both cubic paths, and keep every displayed gate-family maximum below one.
This is a finite-grid reproducibility statement; no limit in
\(N\) or \(\varepsilon\) is inferred.

## Chart map

| Panel | Family and variant | Grain | Scale cue |
| --- | --- | --- | --- |
| A | highlighted multi-series line | five epsilon values at each of \(N=40,48,64\) | logarithmic epsilon axis; focused vertical scale; benchmark one |
| B | two-series line-dot relationship | five epsilon values at \(N=64\) | logarithmic epsilon axis; coefficients divided by their registered powers |
| C | signed two-series line-dot relationship | five epsilon values at \(N=64\), split by cubic path | logarithmic epsilon axis; zero line shown |
| D | log-scale validation-margin dot plot | maximum ratio within cutoff, step, physical--kinetic, and independent families | neutral line at one is the fail threshold |

## Source-data derivation

`source-data.csv` contains one `finite_case` row for every configured
\((N,\varepsilon)\) pair and one `gate_component` row for every numerical
discrepancy included in panel D. Each row records the exact upstream path and
SHA-256 digest. The panel-D point for a family is the maximum of its component
ratios; `is_family_max=true` marks the selected row. Thus aggregation cannot
hide a failed component: any component at or above one would become a family
maximum at or above one.

The finite case rows are extracted from
`research/certificates/r073m/primary_results.json`. Gate components are
extracted from that file,
`research/certificates/r073m/independent_linear.json`, and
`research/certificates/r073m/independent_hierarchy.json`, with tolerances from
the sealed `config.json`. The certificate, validation, and manifest are also
bound as inputs and must all pass before rendering.

## Visual policy

The output uses a hard two-root palette cap (blue and gold) plus neutrals.
Line style, marker shape, open/filled markers, direct panel position, and the
zero/fail references carry distinctions in grayscale. The figure is fixed at
178 by 128 mm and exported as vector PDF, vector SVG, and 600-dpi PNG.

## Claim boundary

The figure does not identify the finite proxy \(A_{N,0}\) with the continuum
action, certify convergence of \(g^{(0)}_{N,\varepsilon}\), establish a
prefactor limit or a two-term WKB expansion, certify a uniform Taylor radius
or a fourth-order remainder, compute a full nonlinear Navier--Stokes
trajectory, prove fixed-background Lyapunov instability, close transverse
three-dimensional dynamics, prove finite-time singularity, or solve the Clay
problem.

